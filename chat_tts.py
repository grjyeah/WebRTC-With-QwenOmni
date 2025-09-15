#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import time

class ChatTTS:
    def __init__(self, voice="Ting-Ting"):
        """
        初始化ChatTTS类
        :param voice: 语音名称，默认使用中文Ting-Ting
        """
        self.voice = voice

    def speak(self, text):
        """
        将文本转换为语音并播放
        :param text: 要朗读的文本
        """
        try:
            # 使用macOS系统say命令进行TTS
            subprocess.run(["say", "-v", self.voice, text], check=True)
        except subprocess.CalledProcessError as e:
            print(f"TTS播放出错: {e}")
        except FileNotFoundError:
            print("错误: 找不到say命令，请确保在macOS系统上运行")

    def set_voice(self, voice):
        """
        设置语音
        :param voice: 语音名称
        """
        self.voice = voice

    def list_voices(self):
        """
        列出系统可用的语音
        """
        try:
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, check=True)
            print("可用的语音:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"获取语音列表出错: {e}")

def simulate_chatbot():
    """
    模拟chatbot输出
    """
    responses = [
        "你好！我是你的AI助手。",
        "我可以帮助你回答问题、提供信息和完成各种任务。",
        "有什么我可以帮你的吗？",
        "如果你有任何问题，请随时问我。",
        "感谢使用我们的服务，祝你有美好的一天！"
    ]

    return responses

def main():
    # 创建ChatTTS实例
    chat_tts = ChatTTS()

    # 显示可用语音
    print("正在获取系统语音列表...")
    chat_tts.list_voices()

    # 等待用户查看语音列表
    time.sleep(2)

    print("\n开始模拟chatbot对话...")
    print("=" * 50)

    # 模拟chatbot对话
    responses = simulate_chatbot()

    for i, response in enumerate(responses, 1):
        print(f"Bot: {response}")
        # 朗读chatbot输出
        chat_tts.speak(response)
        # 添加间隔时间
        time.sleep(1)

        if i < len(responses):
            print("-" * 30)

    print("=" * 50)
    print("对话结束")

if __name__ == "__main__":
    main()