import 'dart:async';
import 'dart:typed_data';

import 'package:fast_rtc_asr/fast_rtc_asr.dart';

void main() async {
  // 初始化ASR集成（带TTS支持）
  final asrIntegration = FastRtcAsrIntegration(
    appId: 'your_app_id',
    apiKey: 'your_api_key',
    apiSecret: 'your_api_secret',
    ttsModel: TtsModel.cosyvoice2,
    ttsApiKey: 'your_cosyvoice2_api_key',
  );

  print('ASR and TTS integration initialized');

  // 检查TTS是否可用
  if (asrIntegration.isTtsSupported) {
    print('TTS is supported');

    // 获取支持的语音列表
    try {
      final voices = await asrIntegration.getAvailableTtsVoices();
      print('Available voices: $voices');

      // 设置TTS参数
      await asrIntegration.setTtsVoice('cosyvoice2-female');
      await asrIntegration.setTtsRate(1.0);
      await asrIntegration.setTtsPitch(1.0);
      await asrIntegration.setTtsVolume(1.0);

      // 朗读欢迎词
      await asrIntegration.speak('欢迎使用FastRTC ASR和TTS集成');
    } catch (e) {
      print('Error setting up TTS: $e');
    }
  } else {
    print('TTS is not supported');
  }

  // 模拟音频流（在实际应用中，这将来自FastRTC）
  final audioStream = Stream<Uint8List>.periodic(
    Duration(milliseconds: 100),
    (count) => Uint8List.fromList(List.generate(320, (i) => 0)), // 生成静音音频数据
  ).take(100); // 生成100个音频包

  try {
    print('Starting ASR recognition...');

    // 开始语音识别（自动朗读结果）
    final result = await asrIntegration.startListening(
      audioStream: audioStream,
      onPartialResult: (text) {
        print('Partial result: $text');
      },
      onResult: (result) {
        print('Final ASR result: ${result.text}');
      },
      onError: (error) {
        print('ASR error: $error');
      },
      autoSpeakResult: true, // 自动朗读识别结果
    );

    print('ASR completed: ${result.text}');
  } catch (e) {
    print('ASR failed: $e');
  }

  print('Example completed');
}