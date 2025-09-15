import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:io';
import 'package:crypto/crypto.dart';

import '../models/asr_result.dart';
import '../utils/xf_utils.dart';

/// 科大讯飞ASR语音识别客户端
class XfAsrClient {
  final String appId;
  final String apiKey;
  final String apiSecret;
  final String host;
  final int port;

  static const String uri = "/v2/iat";
  static const String requestUrl = "wss://iat-api.xfyun.cn/v2/iat";

  XfAsrClient({
    required this.appId,
    required this.apiKey,
    required this.apiSecret,
    this.host = "iat-api.xfyun.cn",
    this.port = 443,
  });

  /// 建立WebSocket连接并开始语音识别
  Future<AsrResult> startAsr({
    String audioFormat = "raw",
    String language = "zh_cn",
    String accent = "mandarin",
    required Stream<Uint8List> audioStream,
    void Function(String)? onPartialResult,
  }) async {
    // 生成RFC1123格式的时间戳
    final date = DateTime.now().toUtc();
    final timestamp = XfUtils.toRfc1123String(date);

    // 构造HTTP请求头
    final signatureOrigin = 'host: $host\ndate: $timestamp\nGET $uri HTTP/1.1';
    final signatureSha = hmacSha256(signatureOrigin, apiSecret);
    final signature = base64.encode(signatureSha);

    final authorizationOrigin =
        'api_key="$apiKey", algorithm="hmac-sha256", headers="host date request-line", signature="$signature"';
    final authorization = base64.encode(utf8.encode(authorizationOrigin));

    // 构造WebSocket URL
    final url = '$requestUrl?authorization=$authorization&date=$timestamp&host=$host';

    // 连接WebSocket
    final ws = await _connectWebSocket(url);

    // 发送开始识别消息
    final startMessage = _buildStartMessage(audioFormat, language, accent);
    ws.add(startMessage);

    // 监听结果
    final resultCompleter = Completer<AsrResult>();
    final result = AsrResult();

    ws.listen(
      (message) {
        final response = jsonDecode(message);
        _handleAsrResponse(response, result, onPartialResult, resultCompleter);
      },
      onError: (error) {
        if (!resultCompleter.isCompleted) {
          resultCompleter.completeError(error);
        }
      },
      onDone: () {
        if (!resultCompleter.isCompleted) {
          resultCompleter.complete(result);
        }
      },
    );

    // 发送音频数据
    await _sendAudioData(ws, audioStream);

    // 发送结束消息
    final endMessage = _buildEndMessage();
    ws.add(endMessage);

    return resultCompleter.future;
  }

  /// 连接WebSocket
  Future<WebSocket> _connectWebSocket(String url) async {
    return WebSocket.connect(url);
  }

  /// 构造开始识别消息
  Map<String, dynamic> _buildStartMessage(String audioFormat, String language, String accent) {
    return {
      "common": {
        "app_id": appId,
      },
      "business": {
        "language": language,
        "accent": accent,
        "domain": "iat",
        "sample_rate": "16000",
        "voice_field": "off",
        "ent": "enteval",
        "dwa": "wpgs"
      },
      "data": {
        "status": 0,
        "format": audioFormat,
        "encoding": "raw",
        "audio": ""
      }
    };
  }

  /// 构造结束消息
  Map<String, dynamic> _buildEndMessage() {
    return {
      "data": {
        "status": 2,
        "audio": ""
      }
    };
  }

  /// 发送音频数据
  Future<void> _sendAudioData(WebSocket ws, Stream<Uint8List> audioStream) async {
    await audioStream.forEach((audioData) {
      final message = {
        "data": {
          "status": 1,
          "audio": base64.encode(audioData),
        }
      };
      ws.add(jsonEncode(message));
    });
  }

  /// 处理ASR响应
  void _handleAsrResponse(
    Map<String, dynamic> response,
    AsrResult result,
    void Function(String)? onPartialResult,
    Completer<AsrResult> completer,
  ) {
    try {
      final code = response['code'];
      if (code != 0) {
        final message = response['message'] ?? '未知错误';
        throw Exception('ASR错误: $code, $message');
      }

      final data = response['data'];
      if (data != null) {
        final resultData = data['result'];
        if (resultData != null) {
          final text = resultData['ws'] != null
              ? resultData['ws']
                  .map((w) => w['cw'][0]['w'])
                  .join()
              : '';

          // 更新结果
          result.text += text;
          result.isFinal = data['status'] == 2;

          // 调用部分结果回调
          if (!result.isFinal && onPartialResult != null) {
            onPartialResult(result.text);
          }

          // 如果是最终结果，完成Future
          if (result.isFinal && !completer.isCompleted) {
            completer.complete(result);
          }
        }
      }
    } catch (e) {
      if (!completer.isCompleted) {
        completer.completeError(e);
      }
    }
  }

  /// HMAC-SHA256加密
  Uint8List hmacSha256(String data, String key) {
    final keyBytes = utf8.encode(key);
    final dataBytes = utf8.encode(data);
    final hmac = Hmac(sha256, keyBytes);
    return hmac.convert(dataBytes).bytes;
  }
}