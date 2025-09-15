#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试更新后的CosyVoice TTS实现
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from updated_cosyvoice_tts import CosyVoiceTTS

def test_updated_cosyvoice_tts():
    """测试更新后的CosyVoice TTS功能"""
    print("Testing updated CosyVoice TTS implementation...")

    try:
        # 使用本地模型路径创建CosyVoice TTS实例
        model_path = os.path.expanduser("~/.cache/modelscope/hub/models/iic/CosyVoice2-0.5B")
        tts = CosyVoiceTTS(model_path=model_path, voice="中文女")

        # 测试文本转语音
        text = "你好，这是一个测试。"
        output_path = tts.speak_to_file(text, "test_output_updated.wav")

        print(f"Speech generated successfully: {output_path}")
        print(f"Text: {text}")
        print(f"Voice: 中文女")

        # 检查文件是否存在
        if os.path.exists(output_path):
            print(f"Output file exists: {output_path}")
            # 获取文件大小
            file_size = os.path.getsize(output_path)
            print(f"File size: {file_size} bytes")
        else:
            print("Error: Output file not found")

        # 测试不同的语音类型
        print("\nTesting different voices...")
        tts.list_voices()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_updated_cosyvoice_tts()