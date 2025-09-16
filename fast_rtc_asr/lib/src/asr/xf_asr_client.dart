import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:io';
import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart';

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
    if (kDebugMode) {
      print('ASR: Starting ASR recognition process');
      print('ASR: Audio format: $audioFormat, Language: $language, Accent: $accent');
    }

    // 生成RFC1123格式的时间戳
    final date = DateTime.now().toUtc();
    final timestamp = XfUtils.toRfc1123String(date);
    if (kDebugMode) print('ASR: Generated timestamp: $timestamp');

    // 构造HTTP请求头
    final signatureOrigin = 'host: $host\ndate: $timestamp\nGET $uri HTTP/1.1';
    final signatureSha = hmacSha256(signatureOrigin, apiSecret);
    final signature = base64.encode(signatureSha);
    if (kDebugMode) print('ASR: Generated signature');

    final authorizationOrigin =
        'api_key="$apiKey", algorithm="hmac-sha256", headers="host date request-line", signature="$signature"';
    final authorization = base64.encode(utf8.encode(authorizationOrigin));
    if (kDebugMode) print('ASR: Generated authorization header');

    // 构造WebSocket URL
    final url = '$requestUrl?authorization=$authorization&date=$timestamp&host=$host';
    if (kDebugMode) print('ASR: Constructed WebSocket URL (authorization hidden for security)');

    try {
      // 连接WebSocket
      if (kDebugMode) print('ASR: Connecting to WebSocket...');
      final ws = await _connectWebSocket(url);
      if (kDebugMode) print('ASR: WebSocket connection established');

      // 发送开始识别消息
      final startMessage = _buildStartMessage(audioFormat, language, accent);
      if (kDebugMode) print('ASR: Sending start message: ${jsonEncode(startMessage)}');
      ws.add(jsonEncode(startMessage));

      // 监听结果
      final resultCompleter = Completer<AsrResult>();
      final result = AsrResult();

      ws.listen(
        (message) {
          if (kDebugMode) print('ASR: Received message from server: $message');
          try {
            final response = jsonDecode(message);
            _handleAsrResponse(response, result, onPartialResult, resultCompleter);
          } catch (e) {
            if (kDebugMode) print('ASR: Error parsing response: $e');
            if (!resultCompleter.isCompleted) {
              resultCompleter.completeError(e);
            }
          }
        },
        onError: (error) {
          if (kDebugMode) print('ASR: WebSocket error: $error');
          if (!resultCompleter.isCompleted) {
            resultCompleter.completeError(error);
          }
        },
        onDone: () {
          if (kDebugMode) print('ASR: WebSocket connection closed');
          if (!resultCompleter.isCompleted) {
            resultCompleter.complete(result);
          }
        },
      );

      // 发送音频数据
      if (kDebugMode) print('ASR: Starting to send audio data...');
      await _sendAudioData(ws, audioStream);
      if (kDebugMode) print('ASR: Finished sending audio data');

      // 发送结束消息
      final endMessage = _buildEndMessage();
      if (kDebugMode) print('ASR: Sending end message: ${jsonEncode(endMessage)}');
      ws.add(jsonEncode(endMessage));

      if (kDebugMode) print('ASR: Waiting for final result...');
      return resultCompleter.future;
    } catch (e) {
      if (kDebugMode) print('ASR: Error in startAsr: $e');
      rethrow;
    }
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
    int audioChunkCount = 0;
    int totalBytes = 0;

    if (kDebugMode) print('ASR: Starting audio data transmission');

    await audioStream.forEach((audioData) {
      audioChunkCount++;
      totalBytes += audioData.lengthInBytes;

      final encodedAudio = base64.encode(audioData);
      final message = {
        "data": {
          "status": 1,
          "audio": encodedAudio,
        }
      };

      if (kDebugMode) {
        print('ASR: Sending audio chunk #$audioChunkCount (${audioData.lengthInBytes} bytes)');
        // Log first 50 characters of encoded audio for debugging
        if (encodedAudio.length > 50) {
          print('ASR: Audio data (first 50 chars): ${encodedAudio.substring(0, 50)}...');
        } else {
          print('ASR: Audio data: $encodedAudio');
        }
      }

      ws.add(jsonEncode(message));
    });

    if (kDebugMode) {
      print('ASR: Finished audio data transmission');
      print('ASR: Total chunks sent: $audioChunkCount');
      print('ASR: Total bytes sent: $totalBytes');
    }
  }

  /// 处理ASR响应
  void _handleAsrResponse(
    Map<String, dynamic> response,
    AsrResult result,
    void Function(String)? onPartialResult,
    Completer<AsrResult> completer,
  ) {
    try {
      if (kDebugMode) print('ASR: Handling response: $response');

      final code = response['code'];
      if (kDebugMode) print('ASR: Response code: $code');

      if (code != 0) {
        final message = response['message'] ?? '未知错误';
        if (kDebugMode) print('ASR: Error response - code: $code, message: $message');
        throw Exception('ASR错误: $code, $message');
      }

      final data = response['data'];
      if (kDebugMode) print('ASR: Response data: $data');

      if (data != null) {
        final resultData = data['result'];
        if (kDebugMode) print('ASR: Result data: $resultData');

        if (resultData != null) {
          final text = resultData['ws'] != null
              ? resultData['ws']
                  .map((w) => w['cw'][0]['w'])
                  .join()
              : '';

          if (kDebugMode) print('ASR: Extracted text: "$text"');

          // 更新结果
          result.text += text;
          result.isFinal = data['status'] == 2;

          if (kDebugMode) {
            print('ASR: Updated result text: "${result.text}"');
            print('ASR: Is final result: ${result.isFinal}');
          }

          // 调用部分结果回调
          if (!result.isFinal && onPartialResult != null) {
            if (kDebugMode) print('ASR: Calling partial result callback with: "${result.text}"');
            onPartialResult(result.text);
          }

          // 如果是最终结果，完成Future
          if (result.isFinal && !completer.isCompleted) {
            if (kDebugMode) print('ASR: Final result reached, completing future with: "${result.text}"');
            completer.complete(result);
          }
        } else if (kDebugMode) {
          print('ASR: No result data in response');
        }
      } else if (kDebugMode) {
        print('ASR: No data in response');
      }
    } catch (e) {
      if (kDebugMode) print('ASR: Error in _handleAsrResponse: $e');
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