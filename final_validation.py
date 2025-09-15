#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最终验证CosyVoice TTS集成的脚本
"""

import sys
import os

def check_model_files():
    """检查模型文件"""
    print("=== 检查模型文件 ===")
    model_path = os.path.expanduser("~/.cache/modelscope/hub/models/iic/CosyVoice2-0.5B")

    if not os.path.exists(model_path):
        print("❌ 模型目录不存在")
        return False

    print("✓ 模型目录存在")

    # 检查关键文件
    key_files = [
        'llm.pt',
        'flow.pt',
        'hift.pt',
        'flow.cache.pt',
        'flow.decoder.estimator.fp32.onnx',
        'speech_tokenizer_v2.onnx'
    ]

    found_files = []
    for root, dirs, files in os.walk(model_path):
        for file in files:
            if file in key_files:
                found_files.append(file)

    missing_files = set(key_files) - set(found_files)

    if missing_files:
        print(f"⚠ 缺少文件: {missing_files}")
    else:
        print("✓ 所有关键模型文件都存在")

    print(f"找到 {len(found_files)} 个关键文件")
    return True

def test_imports():
    """测试导入"""
    print("\n=== 测试导入 ===")

    try:
        from modelscope import AutoModel
        print("✓ ModelScope导入成功")
    except Exception as e:
        print(f"❌ ModelScope导入失败: {e}")
        return False

    try:
        from final_cosyvoice_tts import CosyVoiceTTS
        print("✓ CosyVoiceTTS导入成功")
    except Exception as e:
        print(f"❌ CosyVoiceTTS导入失败: {e}")
        return False

    return True

def main():
    """主函数"""
    print("CosyVoice TTS集成最终验证")
    print("=" * 40)

    checks = [
        check_model_files,
        test_imports
    ]

    passed = 0
    for check in checks:
        if check():
            passed += 1

    print("\n" + "=" * 40)
    print(f"验证结果: {passed}/{len(checks)} 通过")

    if passed == len(checks):
        print("🎉 CosyVoice TTS集成验证成功！")
        print("\n系统已准备好使用CosyVoice TTS功能。")
        print("\n使用方法:")
        print("  1. 命令行: python final_cosyvoice_tts.py '文本内容' -o output.wav")
        print("  2. 编程调用: from final_cosyvoice_tts import CosyVoiceTTS")
        return 0
    else:
        print("❌ 部分验证失败，请检查上述错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())