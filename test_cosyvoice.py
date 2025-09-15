#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试CosyVoice TTS实现
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cosyvoice_tts import CosyVoiceTTS

def test_cosyvoice_tts():
    """测试CosyVoice TTS功能"""
    print("Testing CosyVoice TTS implementation...")

    try:
        # 创建CosyVoice TTS实例
        tts = CosyVoiceTTS(voice="中文女")

        # 测试文本转语音
        text = "你好，这是一个测试。"
        output_path = tts.speak_to_file(text, "test_output.wav")

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

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cosyvoice_tts()