import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';

import 'xf_asr_client.dart';
import '../models/asr_result.dart';
import '../tts/tts_interface.dart';
import '../tts/tts_factory.dart';

/// FastRTC与科大讯飞ASR集成类
class FastRtcAsrIntegration {
  final XfAsrClient _asrClient;
  StreamSubscription<Uint8List>? _audioSubscription;
  bool _isListening = false;
  TtsInterface? _tts;

  FastRtcAsrIntegration({
    required String appId,
    required String apiKey,
    required String apiSecret,
    TtsModel? ttsModel,
    String? ttsApiKey,
    String? ttsApiUrl,
  }) : _asrClient = XfAsrClient(
          appId: appId,
          apiKey: apiKey,
          apiSecret: apiSecret,
        ) {
    // 初始化TTS
    if (ttsModel != null) {
      _tts = TtsFactory.createTts(
        model: ttsModel,
        apiKey: ttsApiKey,
        apiUrl: ttsApiUrl,
      );
    }
  }

  /// 开始语音识别
  Future<AsrResult> startListening({
    required Stream<Uint8List> audioStream,
    void Function(String)? onPartialResult,
    void Function(AsrResult)? onResult,
    void Function(Object)? onError,
    bool autoSpeakResult = false, // 新增参数：是否自动朗读结果
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

      // 如果启用了自动朗读且TTS可用，则朗读结果
      if (autoSpeakResult && _tts != null && result.text.isNotEmpty) {
        try {
          await _tts!.speak(result.text);
        } catch (e) {
          if (kDebugMode) {
            print('Failed to speak ASR result: $e');
          }
        }
      }

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

  /// 使用TTS朗读文本
  Future<void> speak(String text) async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.speak(text);
  }

  /// 停止TTS朗读
  Future<void> stopSpeaking() async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.stop();
  }

  /// 暂停TTS朗读
  Future<void> pauseSpeaking() async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.pause();
  }

  /// 恢复TTS朗读
  Future<void> resumeSpeaking() async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.resume();
  }

  /// 设置TTS语音
  Future<void> setTtsVoice(String voiceName) async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.setVoice(voiceName);
  }

  /// 设置TTS语速
  Future<void> setTtsRate(double rate) async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.setRate(rate);
  }

  /// 设置TTS音调
  Future<void> setTtsPitch(double pitch) async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.setPitch(pitch);
  }

  /// 设置TTS音量
  Future<void> setTtsVolume(double volume) async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    await _tts!.setVolume(volume);
  }

  /// 获取支持的TTS语音列表
  Future<List<String>> getAvailableTtsVoices() async {
    if (_tts == null) {
      throw StateError('TTS is not initialized');
    }
    return await _tts!.getAvailableVoices();
  }

  /// 检查是否支持TTS
  bool get isTtsSupported => _tts != null;
}