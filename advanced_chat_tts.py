#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import time
import os

class ChatTTS:
    def __init__(self, voice="Ting-Ting"):
        """
        初始化ChatTTS类
        :param voice: 语音名称，默认使用中文Ting-Ting
        """
        self.voice = voice
        self.available_voices = self._get_available_voices()

    def _get_available_voices(self):
        """
        获取系统可用的语音列表
        :return: 语音字典 {语言: [语音列表]}
        """
        try:
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            voices = {}

            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        voice_name = parts[0]
                        language = parts[1]

                        if language not in voices:
                            voices[language] = []
                        voices[language].append(voice_name)

            return voices
        except subprocess.CalledProcessError as e:
            print(f"获取语音列表出错: {e}")
            return {}

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
        # 验证语音是否可用
        all_voices = []
        for lang_voices in self.available_voices.values():
            all_voices.extend(lang_voices)

        if voice in all_voices:
            self.voice = voice
            print(f"语音已设置为: {voice}")
        else:
            print(f"语音 '{voice}' 不可用，使用默认语音: {self.voice}")

    def list_voices(self):
        """
        列出系统可用的语音
        """
        print("可用的语音 (按语言分组):")
        print("-" * 50)

        for language, voices in self.available_voices.items():
            print(f"{language}: {', '.join(voices)}")

        print("-" * 50)

    def list_chinese_voices(self):
        """
        列出中文语音
        """
        print("中文语音选项:")
        print("-" * 30)

        chinese_voices = []
        for lang_code, voices in self.available_voices.items():
            if 'zh' in lang_code.lower():
                chinese_voices.extend(voices)

        for voice in chinese_voices:
            print(f"- {voice}")

        print("-" * 30)
        return chinese_voices

def chatbot_response(user_input):
    """
    简单的chatbot响应函数
    :param user_input: 用户输入
    :return: chatbot响应
    """
    responses = {
        "你好": "你好！很高兴见到你。",
        "你是谁": "我是你的AI助手，可以帮你回答问题和提供信息。",
        "你能做什么": "我可以回答问题、提供信息、讲笑话，还可以和你聊天。",
        "再见": "再见！希望很快能再和你聊天。",
        "谢谢": "不客气！随时为你服务。",
        "默认": "这是一个示例响应。在实际应用中，这里会有更智能的回复。"
    }

    # 简单的关键词匹配
    for key in responses:
        if key in user_input:
            return responses[key]

    return responses["默认"]

def interactive_chat(chat_tts):
    """
    交互式聊天模式
    :param chat_tts: ChatTTS实例
    """
    print("欢迎使用AI语音助手！")
    print("输入 '退出' 或 'bye' 结束对话")
    print("输入 '语音列表' 查看可用语音")
    print("输入 '中文语音' 查看中文语音选项")
    print("输入 '设置语音 [语音名]' 更改语音")
    print("-" * 50)

    while True:
        try:
            user_input = input("你: ").strip()

            if user_input.lower() in ['退出', 'bye', 'quit']:
                print("Bot: 再见！祝你有美好的一天！")
                chat_tts.speak("再见！祝你有美好的一天！")
                break

            elif user_input == '语音列表':
                chat_tts.list_voices()
                continue

            elif user_input == '中文语音':
                chat_tts.list_chinese_voices()
                continue

            elif user_input.startswith('设置语音 '):
                voice_name = user_input[6:].strip()
                chat_tts.set_voice(voice_name)
                continue

            # 获取chatbot响应
            response = chatbot_response(user_input)
            print(f"Bot: {response}")

            # 朗读响应
            chat_tts.speak(response)

        except KeyboardInterrupt:
            print("\nBot: 再见！")
            chat_tts.speak("再见！")
            break
        except EOFError:
            print("\nBot: 再见！")
            chat_tts.speak("再见！")
            break

def main():
    # 创建ChatTTS实例
    chat_tts = ChatTTS()

    # 检查命令行参数
    if len(sys.argv) > 1:
        # 如果提供了命令行参数，直接朗读
        text = ' '.join(sys.argv[1:])
        print(f"正在朗读: {text}")
        chat_tts.speak(text)
    else:
        # 进入交互模式
        interactive_chat(chat_tts)

if __name__ == "__main__":
    main()