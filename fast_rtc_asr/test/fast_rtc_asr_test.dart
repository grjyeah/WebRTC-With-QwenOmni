import 'package:flutter_test/flutter_test.dart';
import 'package:fast_rtc_asr/fast_rtc_asr.dart';

void main() {
  group('FastRtcAsrIntegration', () {
    late FastRtcAsrIntegration asrIntegration;

    setUp(() {
      // 初始化ASR集成实例
      asrIntegration = FastRtcAsrIntegration(
        appId: 'test_app_id',
        apiKey: 'test_api_key',
        apiSecret: 'test_api_secret',
      );
    });

    test('should create instance', () {
      expect(asrIntegration, isNotNull);
    });

    // 注意：由于需要网络连接和有效的API密钥，实际的集成测试需要在真实环境中运行
  });
}