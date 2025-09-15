#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试所有修改后的TTS实现
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有修改后的文件导入"""
    print("Testing imports...")

    # 测试cosyvoice_tts.py
    try:
        from cosyvoice_tts import CosyVoiceTTS
        print("✓ cosyvoice_tts imported successfully")
    except Exception as e:
        print(f"✗ Error importing cosyvoice_tts: {e}")
        return False

    # 测试integrated_asr_chatbot.py
    try:
        # 由于这个文件依赖外部服务，我们只测试导入
        import integrated_asr_chatbot
        print("✓ integrated_asr_chatbot imported successfully")
    except Exception as e:
        print(f"✗ Error importing integrated_asr_chatbot: {e}")
        return False

    # 测试chatbot_app.py
    try:
        import chatbot_app
        print("✓ chatbot_app imported successfully")
    except Exception as e:
        print(f"✗ Error importing chatbot_app: {e}")
        return False

    # 测试final_chatbot.py
    try:
        import final_chatbot
        print("✓ final_chatbot imported successfully")
    except Exception as e:
        print(f"✗ Error importing final_chatbot: {e}")
        return False

    # 测试enhanced_chatbot_app.py
    try:
        import enhanced_chatbot_app
        print("✓ enhanced_chatbot_app imported successfully")
    except Exception as e:
        print(f"✗ Error importing enhanced_chatbot_app: {e}")
        return False

    # 测试simple_chatbot.py
    try:
        import simple_chatbot
        print("✓ simple_chatbot imported successfully")
    except Exception as e:
        print(f"✗ Error importing simple_chatbot: {e}")
        return False

    return True

def test_cosyvoice_tts():
    """测试CosyVoice TTS功能"""
    print("\nTesting CosyVoice TTS functionality...")

    try:
        from cosyvoice_tts import CosyVoiceTTS

        # 创建CosyVoice TTS实例
        tts = CosyVoiceTTS(voice="中文女")
        print("✓ CosyVoiceTTS instance created successfully")

        # 测试文本转语音
        text = "你好，这是一个测试。"
        output_path = tts.speak_to_file(text, "test_output.wav")
        print(f"✓ Speech generated successfully: {output_path}")

        # 检查文件是否存在
        if os.path.exists(output_path):
            print(f"✓ Output file exists: {output_path}")
            # 获取文件大小
            file_size = os.path.getsize(output_path)
            print(f"✓ File size: {file_size} bytes")
            # 清理测试文件
            os.remove(output_path)
        else:
            print("✗ Error: Output file not found")
            return False

    except Exception as e:
        print(f"✗ Error testing CosyVoice TTS: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

def main():
    """主函数"""
    print("Testing all modified TTS implementations...\n")

    # 测试导入
    if not test_imports():
        print("\n✗ Import tests failed")
        return 1

    print("\n✓ All import tests passed")

    # 测试功能
    if not test_cosyvoice_tts():
        print("\n✗ Functionality tests failed")
        return 1

    print("\n✓ All functionality tests passed")
    print("\n🎉 All tests passed! The TTS implementation has been successfully updated.")
    return 0

if __name__ == "__main__":
    sys.exit(main())