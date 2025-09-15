/// ASR识别结果
class AsrResult {
  /// 识别文本
  String text = '';

  /// 是否为最终结果
  bool isFinal = false;

  /// 置信度
  double confidence = 0.0;

  /// 错误信息
  String? error;

  AsrResult({
    this.text = '',
    this.isFinal = false,
    this.confidence = 0.0,
    this.error,
  });

  @override
  String toString() {
    return 'AsrResult{text: $text, isFinal: $isFinal, confidence: $confidence, error: $error}';
  }
}