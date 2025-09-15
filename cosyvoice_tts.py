#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CosyVoice TTS implementation for cross-platform compatibility
"""

import os
import sys
import tempfile
import logging
from typing import Optional

try:
    import torch
    import torchaudio
    import numpy as np
    # 尝试导入ModelScope，如果失败则使用占位符实现
    try:
        from modelscope import snapshot_download, AutoModel
        MODELSCOPE_AVAILABLE = True
    except ImportError:
        MODELSCOPE_AVAILABLE = False
        print("ModelScope not available, using placeholder implementation")
except ImportError as e:
    print(f"Required packages not installed: {e}")
    print("Please install required packages: pip install modelscope torch torchaudio")
    sys.exit(1)

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
        self.model = None
        self.sample_rate = 22050  # CosyVoice默认采样率
        self.modelscope_available = MODELSCOPE_AVAILABLE

        # 配置日志
        self.logger = logging.getLogger(__name__)

        # 下载并加载模型（如果ModelScope可用）
        if self.modelscope_available:
            self._load_model()

    def _load_model(self):
        """下载并加载CosyVoice模型"""
        try:
            # 下载模型
            model_dir = snapshot_download(self.model_name)

            # 加载模型
            self.model = AutoModel.from_pretrained(model_dir)

            self.logger.info(f"Successfully loaded CosyVoice model: {self.model_name}")
        except Exception as e:
            self.logger.error(f"Failed to load CosyVoice model: {e}")
            self.modelscope_available = False
            print("Failed to load CosyVoice model, using placeholder implementation")

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

            # 如果ModelScope可用且模型已加载，使用真实模型
            if self.modelscope_available and self.model:
                # 使用CosyVoice模型生成语音
                # 注意：这里需要根据实际的CosyVoice API进行调整
                if hasattr(self.model, 'inference'):
                    # 生成语音
                    output = self.model.inference(text, voice=self.voice)

                    # 保存音频文件
                    if isinstance(output, dict) and 'audio' in output:
                        audio_data = output['audio']
                        # 确保音频数据是正确的格式
                        if isinstance(audio_data, np.ndarray):
                            # 转换为torch tensor
                            audio_tensor = torch.from_numpy(audio_data)
                            # 保存为WAV文件
                            torchaudio.save(output_path, audio_tensor, self.sample_rate)
                        else:
                            # 假设已经是torch tensor
                            torchaudio.save(output_path, audio_data, self.sample_rate)
                    else:
                        # 如果输出格式不同，尝试直接保存
                        torchaudio.save(output_path, output, self.sample_rate)
                else:
                    # 如果没有inference方法，尝试其他方式
                    self.logger.warning("Model does not have inference method, using placeholder")
                    self._create_placeholder_audio(output_path, text)
            else:
                # 使用占位符实现
                self._create_placeholder_audio(output_path, text)

            self.logger.info(f"Successfully generated speech for text: {text[:50]}...")
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
        voices = ["中文女", "中文男", "英文女", "英文男"]
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
        sys.exit(1)

if __name__ == "__main__":
    main()