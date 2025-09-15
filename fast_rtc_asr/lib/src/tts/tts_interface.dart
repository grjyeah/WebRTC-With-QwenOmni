/// TTS接口定义
abstract class TtsInterface {
  /// 将文本转换为语音
  Future<void> speak(String text);

  /// 停止当前的语音播放
  Future<void> stop();

  /// 暂停语音播放
  Future<void> pause();

  /// 恢复语音播放
  Future<void> resume();

  /// 设置语音参数
  Future<void> setVoice(String voiceName);

  /// 设置语速 (0.5-2.0)
  Future<void> setRate(double rate);

  /// 设置音调 (0.5-2.0)
  Future<void> setPitch(double pitch);

  /// 设置音量 (0.0-1.0)
  Future<void> setVolume(double volume);

  /// 获取支持的语音列表
  Future<List<String>> getAvailableVoices();
}