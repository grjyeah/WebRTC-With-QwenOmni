# FastRTC ASR 集成

将科大讯飞Linux SDK的ASR语音识别功能集成到FastRTC中的Dart库，同时支持CosyVoice2 TTS文本转语音模型。

## 功能

- 实现与科大讯飞ASR服务的WebSocket连接
- 支持实时语音识别
- 提供部分结果和最终结果回调
- 易于集成到FastRTC项目中
- 支持CosyVoice2 TTS文本转语音模型
- 支持多种TTS语音、语速、音调和音量调节

## 安装

在 `pubspec.yaml` 中添加依赖：

```yaml
dependencies:
  fast_rtc_asr:
    path: ./path/to/fast_rtc_asr
```

## 使用方法

### 1. 初始化ASR集成（带TTS支持）

```dart
import 'package:fast_rtc_asr/fast_rtc_asr.dart';

final asrIntegration = FastRtcAsrIntegration(
  appId: 'your_app_id',
  apiKey: 'your_api_key',
  apiSecret: 'your_api_secret',
  ttsModel: TtsModel.cosyvoice2, // 启用CosyVoice2 TTS
  ttsApiKey: 'your_tts_api_key',
  ttsApiUrl: 'your_tts_api_url', // 可选
);
```

### 2. 开始语音识别（自动朗读结果）

```dart
// 假设你有一个音频数据流（来自FastRTC）
final audioStream = getAudioStreamFromFastRTC();

try {
  final result = await asrIntegration.startListening(
    audioStream: audioStream,
    onPartialResult: (text) {
      // 处理部分识别结果
      print('Partial result: $text');
    },
    onResult: (result) {
      // 处理最终识别结果
      print('Final result: ${result.text}');
    },
    onError: (error) {
      // 处理错误
      print('ASR error: $error');
    },
    autoSpeakResult: true, // 自动朗读识别结果
  );

  print('ASR completed: ${result.text}');
} catch (e) {
  print('ASR failed: $e');
}
```

### 3. 单独使用TTS功能

```dart
// 检查TTS是否可用
if (asrIntegration.isTtsSupported) {
  // 朗读文本
  await asrIntegration.speak('你好，世界！');

  // 设置TTS参数
  await asrIntegration.setTtsVoice('cosyvoice2-female');
  await asrIntegration.setTtsRate(1.2);
  await asrIntegration.setTtsPitch(1.1);
  await asrIntegration.setTtsVolume(0.8);

  // 获取支持的语音列表
  final voices = await asrIntegration.getAvailableTtsVoices();
  print('Available voices: $voices');
}
```

## 在FastRTC中的集成

要在FastRTC中集成ASR功能，您需要:

1. 在您的FastRTC应用中获取音频流
2. 将音频流传递给ASR集成模块
3. 处理识别结果并更新UI

示例代码:

```dart
class FastRtcWithAsr {
  final FastRtcAsrIntegration _asrIntegration;

  FastRtcWithAsr()
    : _asrIntegration = FastRtcAsrIntegration(
        appId: 'your_app_id',
        apiKey: 'your_api_key',
        apiSecret: 'your_api_secret',
      );

  void startVoiceCommunication() {
    // 获取FastRTC音频流
    final audioStream = getAudioStreamFromFastRTC();

    // 启动ASR识别
    _asrIntegration.startListening(
      audioStream: audioStream,
      onPartialResult: (text) {
        // 更新UI显示部分识别结果
        updateTranscriptionUI(text, isFinal: false);
      },
      onResult: (result) {
        // 更新UI显示最终识别结果
        updateTranscriptionUI(result.text, isFinal: true);
      },
    );
  }

  void stopVoiceCommunication() {
    _asrIntegration.stopListening();
  }
}
```

## API参考

### FastRtcAsrIntegration

主要的集成类，用于管理ASR和TTS功能。

#### 构造函数

```dart
FastRtcAsrIntegration({
  required String appId,
  required String apiKey,
  required String apiSecret,
  TtsModel? ttsModel,        // 可选：TTS模型
  String? ttsApiKey,         // 可选：TTS API密钥
  String? ttsApiUrl,         // 可选：TTS API URL
})
```

#### ASR方法

##### startListening

开始语音识别过程。

```dart
Future<AsrResult> startListening({
  required Stream<Uint8List> audioStream,
  void Function(String)? onPartialResult,
  void Function(AsrResult)? onResult,
  void Function(Object)? onError,
  bool autoSpeakResult = false, // 是否自动朗读结果
})
```

##### stopListening

停止语音识别过程。

```dart
void stopListening()
```

#### TTS方法

##### speak

使用TTS朗读文本。

```dart
Future<void> speak(String text)
```

##### stopSpeaking

停止TTS朗读。

```dart
Future<void> stopSpeaking()
```

##### pauseSpeaking

暂停TTS朗读。

```dart
Future<void> pauseSpeaking()
```

##### resumeSpeaking

恢复TTS朗读。

```dart
Future<void> resumeSpeaking()
```

##### setTtsVoice

设置TTS语音。

```dart
Future<void> setTtsVoice(String voiceName)
```

##### setTtsRate

设置TTS语速。

```dart
Future<void> setTtsRate(double rate)
```

##### setTtsPitch

设置TTS音调。

```dart
Future<void> setTtsPitch(double pitch)
```

##### setTtsVolume

设置TTS音量。

```dart
Future<void> setTtsVolume(double volume)
```

##### getAvailableTtsVoices

获取支持的TTS语音列表。

```dart
Future<List<String>> getAvailableTtsVoices()
```

##### isTtsSupported

检查是否支持TTS。

```dart
bool get isTtsSupported
```

## 注意事项

1. 需要有效的科大讯飞开发者账号和相应的App ID、API Key、API Secret
2. 音频数据应为16位16kHz单声道PCM格式
3. 网络连接是必需的，因为ASR服务是云端服务
4. 请确保遵守科大讯飞的服务条款和隐私政策
5. 如果使用TTS功能，需要有效的CosyVoice2 API密钥
6. TTS服务也是云端服务，需要稳定的网络连接
7. 请确保遵守CosyVoice2的服务条款和隐私政策

## 许可证

MIT