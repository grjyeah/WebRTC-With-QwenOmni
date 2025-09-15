# FastRTC ASR 集成

将科大讯飞Linux SDK的ASR语音识别功能集成到FastRTC中的Dart库。

## 功能

- 实现与科大讯飞ASR服务的WebSocket连接
- 支持实时语音识别
- 提供部分结果和最终结果回调
- 易于集成到FastRTC项目中

## 安装

在 `pubspec.yaml` 中添加依赖：

```yaml
dependencies:
  fast_rtc_asr:
    path: ./path/to/fast_rtc_asr
```

## 使用方法

### 1. 初始化ASR集成

```dart
import 'package:fast_rtc_asr/fast_rtc_asr.dart';

final asrIntegration = FastRtcAsrIntegration(
  appId: 'your_app_id',
  apiKey: 'your_api_key',
  apiSecret: 'your_api_secret',
);
```

### 2. 开始语音识别

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
  );

  print('ASR completed: ${result.text}');
} catch (e) {
  print('ASR failed: $e');
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

主要的集成类，用于管理ASR功能。

#### 构造函数

```dart
FastRtcAsrIntegration({
  required String appId,
  required String apiKey,
  required String apiSecret,
})
```

#### 方法

##### startListening

开始语音识别过程。

```dart
Future<AsrResult> startListening({
  required Stream<Uint8List> audioStream,
  void Function(String)? onPartialResult,
  void Function(AsrResult)? onResult,
  void Function(Object)? onError,
})
```

##### stopListening

停止语音识别过程。

```dart
void stopListening()
```

## 注意事项

1. 需要有效的科大讯飞开发者账号和相应的App ID、API Key、API Secret
2. 音频数据应为16位16kHz单声道PCM格式
3. 网络连接是必需的，因为ASR服务是云端服务
4. 请确保遵守科大讯飞的服务条款和隐私政策

## 许可证

MIT