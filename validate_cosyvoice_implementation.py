#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
验证CosyVoice TTS实现的脚本
"""

import sys
import os

def check_files_modified():
    """检查文件是否已正确修改"""
    print("Checking if files have been correctly modified...")

    # 检查integrated_asr_chatbot.py
    with open("integrated_asr_chatbot.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "from cosyvoice_tts import CosyVoiceTTS" in content and "from gtts import gTTS" not in content:
            print("✓ integrated_asr_chatbot.py correctly modified")
        else:
            print("✗ integrated_asr_chatbot.py not correctly modified")
            return False

    # 检查chatbot_app.py
    with open("chatbot_app.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "from cosyvoice_tts import CosyVoiceTTS" in content and "from gtts import gTTS" not in content:
            print("✓ chatbot_app.py correctly modified")
        else:
            print("✗ chatbot_app.py not correctly modified")
            return False

    # 检查final_chatbot.py
    with open("final_chatbot.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "from cosyvoice_tts import CosyVoiceTTS" in content and "from gtts import gTTS" not in content:
            print("✓ final_chatbot.py correctly modified")
        else:
            print("✗ final_chatbot.py not correctly modified")
            return False

    # 检查enhanced_chatbot_app.py
    with open("enhanced_chatbot_app.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "from cosyvoice_tts import CosyVoiceTTS" in content and "from gtts import gTTS" not in content:
            print("✓ enhanced_chatbot_app.py correctly modified")
        else:
            print("✗ enhanced_chatbot_app.py not correctly modified")
            return False

    # 检查simple_chatbot.py
    with open("simple_chatbot.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "from cosyvoice_tts import CosyVoiceTTS" in content and "from gtts import gTTS" not in content:
            print("✓ simple_chatbot.py correctly modified")
        else:
            print("✗ simple_chatbot.py not correctly modified")
            return False

    return True

def check_requirements():
    """检查requirements.txt是否已更新"""
    print("\nChecking if requirements.txt has been updated...")

    with open("requirements.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if "modelscope" in content and "cosyvoice" in content:
            print("✓ requirements.txt correctly updated")
            return True
        else:
            print("✗ requirements.txt not correctly updated")
            return False

def check_cosyvoice_files():
    """检查CosyVoice相关文件是否存在"""
    print("\nChecking if CosyVoice files exist...")

    files = ["cosyvoice_tts.py", "simple_cosyvoice_tts.py"]
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} does not exist")
            return False

    return True

def main():
    """主函数"""
    print("Validating CosyVoice TTS Implementation...\n")

    # 检查文件修改
    if not check_files_modified():
        print("\n✗ File modification validation failed")
        return 1

    print("\n✓ All files correctly modified")

    # 检查依赖更新
    if not check_requirements():
        print("\n✗ Requirements validation failed")
        return 1

    print("\n✓ Requirements correctly updated")

    # 检查文件存在性
    if not check_cosyvoice_files():
        print("\n✗ File existence validation failed")
        return 1

    print("\n✓ All CosyVoice files exist")

    print("\n🎉 All validations passed! The CosyVoice TTS implementation has been successfully integrated.")
    print("\nNext steps:")
    print("1. Run 'pip install -r requirements.txt' to install the new dependencies")
    print("2. Test the implementation with your chatbot applications")
    print("3. The system will automatically download the CosyVoice model on first use")

    return 0

if __name__ == "__main__":
    sys.exit(main())