import 'dart:typed_data';
import 'package:fast_rtc_asr/fast_rtc_asr.dart';

void main() async {
  // 初始化FastRTC ASR集成
  final asrIntegration = FastRtcAsrIntegration(
    appId: 'your_app_id',
    apiKey: 'your_api_key',
    apiSecret: 'your_api_secret',
  );

  // 模拟音频数据流（在实际应用中，这将来自FastRTC）
  final audioStream = Stream<Uint8List>.periodic(
    const Duration(milliseconds: 100),
    (count) => Uint8List(320), // 模拟16位16kHz单声道音频数据
  ).take(50); // 5秒的音频数据

  try {
    // 开始语音识别
    final result = await asrIntegration.startListening(
      audioStream: audioStream,
      onPartialResult: (text) {
        print('Partial result: $text');
      },
      onResult: (result) {
        print('Final result: ${result.text}');
      },
      onError: (error) {
        print('ASR error: $error');
      },
    );

    print('ASR completed: ${result.text}');
  } catch (e) {
    print('ASR failed: $e');
  }
}