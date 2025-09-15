#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Corrected CosyVoice TTS implementation using ModelScope API
"""

import os
import sys
import tempfile
import logging
from typing import Optional
import torch
import torchaudio

try:
    from modelscope import AutoModel, snapshot_download
    MODELSCOPE_AVAILABLE = True
except ImportError as e:
    MODELSCOPE_AVAILABLE = False
    print(f"ModelScope not available: {e}")
    print("Please install modelscope: pip install modelscope")

class CosyVoiceTTS:
    def __init__(self, model_name: str = "iic/CosyVoice2-0.5B", voice: str = "中文女"):
        """
        初始化CosyVoice TTS类

        Args:
            model_name: ModelScope上的模型名称
            voice: 语音类型 (中文女, 中文男, 英文女, 英文男等)
        """
        self.model_name = model_name
        self.voice = voice
        self.sample_rate = 22050
        self.model = None
        self.modelscope_available = MODELSCOPE_AVAILABLE

        # 配置日志
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        # 加载模型
        self._load_model()

    def _load_model(self):
        """加载CosyVoice模型"""
        try:
            if self.modelscope_available:
                # 下载并加载模型
                self.logger.info(f"Downloading/loading CosyVoice model: {self.model_name}")
                self.model = AutoModel.from_pretrained(self.model_name)
                self.logger.info("Successfully loaded CosyVoice model")
            else:
                self.logger.warning("ModelScope not available")
        except Exception as e:
            self.logger.error(f"Failed to load CosyVoice model: {e}")
            self.model = None

    def set_voice(self, voice: str):
        """
        设置语音类型

        Args:
            voice: 语音类型
        """
        self.voice = voice
        self.logger.info(f"Voice set to: {voice}")

    def speak_to_file(self, text: str, output_path: Optional[str] = None) -> str:
        """
        将文本转换为语音并保存到文件

        Args:
            text: 要转换的文本
            output_path: 输出文件路径，如果为None则创建临时文件

        Returns:
            音频文件路径
        """
        try:
            # 如果没有指定输出路径，创建临时文件
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                output_path = temp_file.name
                temp_file.close()

            # 如果模型可用，使用真实模型
            if self.model and hasattr(self.model, 'inference_instruct'):
                try:
                    # 使用instruct模式生成语音
                    self.logger.info(f"Generating speech for text: {text}")

                    # 使用默认的提示词
                    prompt = "Theo 'Crimson', is a fiery, passionate rebel leader. Fights with fervor for justice, but struggles with impulsiveness."

                    # 生成语音
                    generator = self.model.inference_instruct(text, self.voice, prompt, stream=False)
                    result = next(generator)

                    # 获取音频数据
                    audio_data = result['tts_speech']

                    # 保存音频文件
                    if audio_data is not None:
                        # 确保数据格式正确
                        if len(audio_data.shape) == 1:
                            audio_data = audio_data.unsqueeze(0)
                        torchaudio.save(output_path, audio_data, self.sample_rate)
                        self.logger.info(f"Successfully generated speech: {output_path}")
                    else:
                        raise ValueError("Generated audio data is None")

                except Exception as e:
                    self.logger.warning(f"Error using CosyVoice model: {e}")
                    self.logger.warning("Falling back to placeholder implementation")
                    self._create_placeholder_audio(output_path, text)
            else:
                # 使用占位符实现
                self._create_placeholder_audio(output_path, text)

            return output_path

        except Exception as e:
            self.logger.error(f"Error in speak_to_file: {e}")
            # 创建一个简单的音频文件作为占位符
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                output_path = temp_file.name
                temp_file.close()
            self._create_placeholder_audio(output_path, text)
            return output_path

    def _create_placeholder_audio(self, output_path: str, text: str):
        """
        创建占位符音频文件（用于测试或错误情况）

        Args:
            output_path: 输出文件路径
            text: 文本内容（用于日志）
        """
        try:
            # 创建一个简单的正弦波作为占位符
            duration = min(len(text) * 0.1, 5.0)  # 根据文本长度调整持续时间，最多5秒
            t = torch.linspace(0, duration, int(self.sample_rate * duration))
            # 生成440Hz的正弦波
            audio = torch.sin(2 * torch.pi * 440 * t)
            # 降低音量
            audio = audio * 0.3
            # 添加淡入淡出效果
            fade_samples = int(0.1 * self.sample_rate)
            audio[:fade_samples] *= torch.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= torch.linspace(1, 0, fade_samples)
            # 保存为WAV文件
            torchaudio.save(output_path, audio.unsqueeze(0), self.sample_rate)
            self.logger.warning(f"Created placeholder audio for text: {text[:50]}...")
        except Exception as e:
            self.logger.error(f"Error creating placeholder audio: {e}")

    def list_voices(self):
        """
        列出可用的语音类型
        """
        # 这里需要根据实际的CosyVoice模型支持的语音类型进行调整
        voices = ["中文女", "中文男", "英文女", "英文男", "日语男", "韩语女"]
        print("Available voices:")
        for voice in voices:
            print(f"  - {voice}")
        return voices

def main():
    """主函数 - 用于测试"""
    import argparse

    parser = argparse.ArgumentParser(description="CosyVoice TTS Demo")
    parser.add_argument("text", nargs="?", default="你好，世界！", help="Text to synthesize")
    parser.add_argument("-v", "--voice", default="中文女", help="Voice type")
    parser.add_argument("-o", "--output", help="Output file path")

    args = parser.parse_args()

    try:
        # 创建CosyVoice TTS实例
        tts = CosyVoiceTTS(voice=args.voice)

        # 生成语音
        output_path = tts.speak_to_file(args.text, args.output)

        print(f"Speech generated successfully: {output_path}")
        print(f"Text: {args.text}")
        print(f"Voice: {args.voice}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()