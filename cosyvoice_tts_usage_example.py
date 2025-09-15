#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CosyVoice TTS使用示例
展示如何在项目中集成和使用CosyVoice TTS
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from final_cosyvoice_tts import CosyVoiceTTS

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    # 创建TTS实例
    tts = CosyVoiceTTS(voice="中文女")

    # 生成语音
    text = "欢迎使用CosyVoice文本到语音系统！"
    output_file = tts.speak_to_file(text, "example_output.wav")

    print(f"语音已生成: {output_file}")
    print(f"文本: {text}")

def example_voice_selection():
    """语音选择示例"""
    print("\n=== 语音选择示例 ===")

    # 列出可用语音
    tts = CosyVoiceTTS()
    voices = tts.list_voices()

    # 使用不同语音生成
    texts = [
        ("你好，世界！", "中文女"),
        ("Hello, World!", "英文女"),
        ("こんにちは、世界！", "日语男")
    ]

    for text, voice in texts:
        tts.set_voice(voice)
        filename = f"example_{voice}.wav"
        output_file = tts.speak_to_file(text, filename)
        print(f"已生成 {voice} 语音: {output_file}")

def example_integration_with_chatbot():
    """与聊天机器人集成示例"""
    print("\n=== 与聊天机器人集成示例 ===")

    # 模拟聊天机器人响应
    responses = [
        "你好！我是你的AI助手。",
        "我可以帮助你回答问题、提供信息或进行对话。",
        "有什么我可以帮你的吗？"
    ]

    tts = CosyVoiceTTS(voice="中文女")

    for i, response in enumerate(responses):
        print(f"机器人: {response}")

        # 将响应转换为语音
        output_file = tts.speak_to_file(response, f"chat_response_{i+1}.wav")
        print(f"语音已生成: {output_file}")

def main():
    """主函数"""
    print("CosyVoice TTS使用示例")
    print("=" * 40)

    try:
        example_basic_usage()
        example_voice_selection()
        example_integration_with_chatbot()

        print("\n" + "=" * 40)
        print("🎉 所有示例运行完成！")
        print("请在当前目录查看生成的音频文件。")

    except Exception as e:
        print(f"❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())