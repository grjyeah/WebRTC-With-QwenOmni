#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
验证CosyVoice TTS集成的完整测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_loading():
    """测试模型加载"""
    print("=== 测试模型加载 ===")
    try:
        from modelscope import AutoModel
        print("✓ ModelScope导入成功")

        # 检查模型文件是否存在
        model_path = os.path.expanduser("~/.cache/modelscope/hub/models/iic/CosyVoice2-0.5B")
        if os.path.exists(model_path):
            print("✓ 本地模型文件存在")
            # 检查关键文件
            key_files = ['llm.pt', 'flow.pt', 'hift.pt']
            found_files = [f for f in key_files if any(f in file for file in os.listdir(model_path))]
            if len(found_files) >= 2:
                print("✓ 关键模型文件存在")
            else:
                print("⚠ 部分关键模型文件缺失")
        else:
            print("⚠ 本地模型文件不存在")

    except Exception as e:
        print(f"✗ 模型加载测试失败: {e}")
        return False

    return True

def test_tts_implementation():
    """测试TTS实现"""
    print("\n=== 测试TTS实现 ===")
    try:
        from final_cosyvoice_tts import CosyVoiceTTS
        print("✓ CosyVoiceTTS类导入成功")

        # 创建实例
        tts = CosyVoiceTTS(voice="中文女")
        print("✓ CosyVoiceTTS实例创建成功")

        # 测试语音列表
        voices = tts.list_voices()
        if len(voices) > 0:
            print("✓ 语音列表获取成功")
        else:
            print("⚠ 语音列表为空")

    except Exception as e:
        print(f"✗ TTS实现测试失败: {e}")
        return False

    return True

def test_speech_generation():
    """测试语音生成"""
    print("\n=== 测试语音生成 ===")
    try:
        from final_cosyvoice_tts import CosyVoiceTTS

        # 创建实例
        tts = CosyVoiceTTS(voice="中文女")

        # 生成语音
        text = "集成测试成功"
        output_path = tts.speak_to_file(text, "integration_test_output.wav")

        # 检查输出文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 0:
                print("✓ 语音生成成功")
                print(f"  输出文件: {output_path}")
                print(f"  文件大小: {file_size} 字节")
                return True
            else:
                print("⚠ 输出文件为空")
        else:
            print("✗ 输出文件未生成")

    except Exception as e:
        print(f"✗ 语音生成测试失败: {e}")
        return False

    return False

def main():
    """主测试函数"""
    print("CosyVoice TTS集成验证测试")
    print("=" * 40)

    # 运行所有测试
    tests = [
        test_model_loading,
        test_tts_implementation,
        test_speech_generation
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"测试结果: {passed}/{len(tests)} 通过")

    if passed == len(tests):
        print("🎉 所有测试通过！CosyVoice TTS集成成功！")
        return 0
    else:
        print("❌ 部分测试失败，请检查上述错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())