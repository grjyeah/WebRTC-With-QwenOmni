import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';

import 'xf_asr_client.dart';
import '../models/asr_result.dart';

/// FastRTC与科大讯飞ASR集成类
class FastRtcAsrIntegration {
  final XfAsrClient _asrClient;
  StreamSubscription<Uint8List>? _audioSubscription;
  bool _isListening = false;

  FastRtcAsrIntegration({
    required String appId,
    required String apiKey,
    required String apiSecret,
  }) : _asrClient = XfAsrClient(
          appId: appId,
          apiKey: apiKey,
          apiSecret: apiSecret,
        );

  /// 开始语音识别
  Future<AsrResult> startListening({
    required Stream<Uint8List> audioStream,
    void Function(String)? onPartialResult,
    void Function(AsrResult)? onResult,
    void Function(Object)? onError,
  }) async {
    if (_isListening) {
      throw StateError('Already listening');
    }

    _isListening = true;

    try {
      // 启动ASR识别
      final result = await _asrClient.startAsr(
        audioStream: audioStream,
        onPartialResult: onPartialResult,
      );

      _isListening = false;
      onResult?.call(result);
      return result;
    } catch (e) {
      _isListening = false;
      onError?.call(e);
      rethrow;
    }
  }

  /// 停止语音识别
  void stopListening() {
    _audioSubscription?.cancel();
    _audioSubscription = null;
    _isListening = false;
  }

  /// 处理来自FastRTC的音频数据
  void handleAudioData(Uint8List audioData) {
    // 在实际实现中，这里会将音频数据发送到ASR引擎
    // 示例代码仅作演示
    if (kDebugMode) {
      print('Received audio data: ${audioData.lengthInBytes} bytes');
    }
  }
}