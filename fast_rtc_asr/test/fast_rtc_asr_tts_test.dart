import 'package:flutter_test/flutter_test.dart';
import 'package:fast_rtc_asr/fast_rtc_asr.dart';

void main() {
  group('FastRtcAsrIntegration TTS Tests', () {
    test('TtsFactory creates CosyVoice2Tts instance', () {
      final tts = TtsFactory.createTts(
        model: TtsModel.cosyvoice2,
        apiKey: 'test_api_key',
      );
      expect(tts, isA<CosyVoice2Tts>());
    });

    test('FastRtcAsrIntegration initializes with TTS', () {
      final integration = FastRtcAsrIntegration(
        appId: 'test_app_id',
        apiKey: 'test_api_key',
        apiSecret: 'test_api_secret',
        ttsModel: TtsModel.cosyvoice2,
        ttsApiKey: 'test_tts_api_key',
      );
      expect(integration.isTtsSupported, isTrue);
    });

    test('FastRtcAsrIntegration initializes without TTS', () {
      final integration = FastRtcAsrIntegration(
        appId: 'test_app_id',
        apiKey: 'test_api_key',
        apiSecret: 'test_api_secret',
      );
      expect(integration.isTtsSupported, isFalse);
    });

    test('CosyVoice2Tts getAvailableVoices returns voices', () async {
      final tts = CosyVoice2Tts(apiKey: 'test_api_key');
      final voices = await tts.getAvailableVoices();
      expect(voices, isNotEmpty);
      expect(voices, contains('cosyvoice2-default'));
    });

    test('CosyVoice2Tts setRate clamps values', () async {
      final tts = CosyVoice2Tts(apiKey: 'test_api_key');
      // These should not throw exceptions
      await tts.setRate(0.1); // Should clamp to 0.5
      await tts.setRate(3.0); // Should clamp to 2.0
      await tts.setRate(1.0); // Should remain 1.0
    });

    test('CosyVoice2Tts setPitch clamps values', () async {
      final tts = CosyVoice2Tts(apiKey: 'test_api_key');
      // These should not throw exceptions
      await tts.setPitch(0.1); // Should clamp to 0.5
      await tts.setPitch(3.0); // Should clamp to 2.0
      await tts.setPitch(1.0); // Should remain 1.0
    });

    test('CosyVoice2Tts setVolume clamps values', () async {
      final tts = CosyVoice2Tts(apiKey: 'test_api_key');
      // These should not throw exceptions
      await tts.setVolume(-0.5); // Should clamp to 0.0
      await tts.setVolume(1.5); // Should clamp to 1.0
      await tts.setVolume(0.5); // Should remain 0.5
    });
  });
}