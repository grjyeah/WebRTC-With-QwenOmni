#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版CosyVoice TTS测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelscope import AutoModel

def test_cosyvoice_model():
    """测试CosyVoice模型加载"""
    print("Testing CosyVoice model loading...")

    try:
        # 使用本地模型路径
        model_path = os.path.expanduser("~/.cache/modelscope/hub/models/iic/CosyVoice2-0.5B")
        print(f"Loading model from: {model_path}")

        # 尝试加载模型
        model = AutoModel.from_pretrained(model_path)
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")

        # 列出模型属性
        print("\nModel attributes:")
        for attr in dir(model):
            if not attr.startswith('_'):
                print(f"  - {attr}")

    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cosyvoice_model()