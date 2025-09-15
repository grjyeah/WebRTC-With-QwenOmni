# Flutter ASR集成更新：支持CosyVoice2 TTS模型

## 概述

本次更新为Flutter ASR集成添加了对CosyVoice2 TTS（文本转语音）模型的支持，实现了ASR（自动语音识别）和TTS的完整语音处理链。用户现在可以在识别语音后自动将文本转换为语音播放。

## 主要更新内容

### 1. 新增TTS接口和实现

- 创建了`TtsInterface`抽象类，定义了TTS功能的标准接口
- 实现了`CosyVoice2Tts`类，提供对CosyVoice2 TTS模型的具体支持
- 添加了`TtsFactory`工厂类，支持创建不同TTS模型的实例

### 2. 更新ASR集成

- 扩展了`FastRtcAsrIntegration`类，添加了TTS相关方法
- 添加了构造函数参数，支持初始化时配置TTS
- 新增`autoSpeakResult`参数，支持在ASR完成后自动朗读结果
- 添加了完整的TTS控制API（播放、停止、暂停、恢复、参数调节等）

### 3. 依赖和配置更新

- 更新了`pubspec.yaml`，添加了`http`依赖
- 更新了版本号从0.0.1到0.0.2
- 更新了描述信息，明确支持CosyVoice2 TTS模型

### 4. 文档和示例

- 全面更新了README文档，添加了TTS使用说明
- 创建了新的示例文件`main_with_tts.dart`，展示TTS功能的使用
- 更新了CHANGELOG，记录新增功能
- 添加了测试文件验证TTS功能

## 使用方法

### 初始化（带TTS支持）

```dart
final asrIntegration = FastRtcAsrIntegration(
  appId: 'your_app_id',
  apiKey: 'your_api_key',
  apiSecret: 'your_api_secret',
  ttsModel: TtsModel.cosyvoice2,
  ttsApiKey: 'your_cosyvoice2_api_key',
);
```

### 自动朗读ASR结果

```dart
final result = await asrIntegration.startListening(
  audioStream: audioStream,
  onPartialResult: (text) => print('Partial: $text'),
  onResult: (result) => print('Final: ${result.text}'),
  autoSpeakResult: true, // 自动朗读结果
);
```

### 单独使用TTS功能

```dart
if (asrIntegration.isTtsSupported) {
  await asrIntegration.speak('你好，世界！');
  await asrIntegration.setTtsVoice('cosyvoice2-female');
  await asrIntegration.setTtsRate(1.2);
}
```

## API新增功能

### 构造函数参数
- `ttsModel`: 指定TTS模型（如TtsModel.cosyvoice2）
- `ttsApiKey`: TTS服务的API密钥
- `ttsApiUrl`: TTS服务的API URL（可选）

### 新增方法
- `speak()`: 朗读文本
- `stopSpeaking()`: 停止朗读
- `pauseSpeaking()`: 暂停朗读
- `resumeSpeaking()`: 恢复朗读
- `setTtsVoice()`: 设置语音
- `setTtsRate()`: 设置语速
- `setTtsPitch()`: 设置音调
- `setTtsVolume()`: 设置音量
- `getAvailableTtsVoices()`: 获取支持的语音列表
- `isTtsSupported`: 检查TTS支持状态

## 测试和验证

添加了专门的测试文件`fast_rtc_asr_tts_test.dart`，验证：
- TTS工厂类正确创建实例
- ASR集成正确初始化TTS
- CosyVoice2 TTS实现正确处理参数
- 参数值正确限制在有效范围内

## 版本信息

- 版本号：0.0.2
- 兼容性：向后兼容0.0.1版本
- 依赖：新增http库依赖

## 注意事项

1. 需要有效的CosyVoice2 API密钥才能使用TTS功能
2. TTS服务是云端服务，需要网络连接
3. 参数值会自动限制在有效范围内（语速和音调：0.5-2.0，音量：0.0-1.0）
4. 在实际实现中，CosyVoice2 API调用需要替换示例代码