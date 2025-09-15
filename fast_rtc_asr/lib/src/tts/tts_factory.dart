import 'tts_interface.dart';
import 'cosyvoice2_tts.dart';

/// TTS工厂类
class TtsFactory {
  /// 创建TTS实例
  static TtsInterface createTts({
    required TtsModel model,
    String? apiKey,
    String? apiUrl,
  }) {
    switch (model) {
      case TtsModel.cosyvoice2:
        if (apiKey == null) {
          throw ArgumentError('apiKey is required for CosyVoice2');
        }
        return CosyVoice2Tts(
          apiKey: apiKey,
          apiUrl: apiUrl ?? 'https://api.cosyvoice2.example.com/v1/tts',
        );

      // 可以在这里添加其他TTS模型
      // case TtsModel.google:
      //   return GoogleTts();

      default:
        throw UnsupportedError('Unsupported TTS model: $model');
    }
  }
}

/// TTS模型枚举
enum TtsModel {
  cosyvoice2,
  // google,
  // amazon,
  // microsoft,
}