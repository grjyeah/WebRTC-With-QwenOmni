import gradio as gr
import time
import tempfile
import os
# 将gTTS替换为CosyVoice TTS
from cosyvoice_tts import CosyVoiceTTS

# 模拟chatbot回复函数
def chatbot_response(message, history):
    # 模拟处理时间
    time.sleep(1)
    if "你好" in message:
        response = "你好！很高兴见到你。有什么我可以帮助你的吗？"
    elif "天气" in message:
        response = "今天天气很好，阳光明媚，温度适宜。"
    elif "名字" in message:
        response = "我是你的AI助手，你可以叫我小助手。"
    else:
        response = f"你说了: '{message}'。我已经收到了你的消息，正在思考如何更好地帮助你。"
    return response

# TTS函数 - 将文本转换为语音
def text_to_speech(text):
    try:
        # 使用CosyVoice TTS生成语音
        tts = CosyVoiceTTS(voice="中文女")
        # 创建临时文件来保存音频（使用.wav格式）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            output_path = tts.speak_to_file(text, tmpfile.name)
            return output_path
    except Exception as e:
        print(f"TTS错误: {e}")
        return None

# 响应函数
def respond(message, chat_history):
    # 获取chatbot回复
    bot_message = chatbot_response(message, chat_history)

    # 更新聊天历史
    chat_history.append((message, bot_message))

    # 生成TTS音频
    audio_file = text_to_speech(bot_message)

    return "", chat_history, audio_file

# 清除函数
def clear_history():
    return None, [], None

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# Chatbot with TTS")
    gr.Markdown("与chatbot实时对话，机器人回复将通过TTS朗读")

    # 聊天历史记录
    chatbot = gr.Chatbot(label="对话记录")

    # 用户输入
    msg = gr.Textbox(label="输入消息", placeholder="输入你的消息...")

    # TTS音频输出
    tts_audio = gr.Audio(label="TTS朗读", autoplay=True, interactive=False, visible=True)

    # 清除按钮
    clear = gr.Button("清除对话")

    # 当用户提交消息时
    msg.submit(respond, [msg, chatbot], [msg, chatbot, tts_audio])

    # 清除对话历史
    clear.click(clear_history, None, [msg, chatbot, tts_audio], queue=False)

# 启动应用
if __name__ == "__main__":
    demo.launch(share=True)