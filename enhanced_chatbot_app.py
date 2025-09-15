import gradio as gr
import time
import websocket
import json
import threading
import base64
import os
import tempfile
from gtts import gTTS

# Global variables for WebSocket connection
ws_connection = None
latest_response = None
response_lock = threading.Lock()

def connect_to_chatbot():
    """Connect to the ASR chatbot WebSocket server"""
    global ws_connection

    try:
        ws_connection = websocket.WebSocket()
        ws_connection.connect("ws://localhost:8765")
        print("Connected to chatbot server")
        return True
    except Exception as e:
        print(f"Failed to connect to chatbot server: {e}")
        return False

def send_message_to_chatbot(message):
    """Send message to chatbot and get response"""
    global ws_connection, latest_response

    if not ws_connection or not ws_connection.connected:
        if not connect_to_chatbot():
            return "无法连接到聊天机器人服务器"

    try:
        # Prepare message
        msg = {
            "type": "text_message",
            "text": message
        }

        # Send message
        ws_connection.send(json.dumps(msg))

        # Wait for response
        response = ws_connection.recv()
        response_data = json.loads(response)

        if response_data.get("type") == "bot_response":
            # Save the response for audio playback
            with response_lock:
                latest_response = response_data
            return response_data.get("text", "无响应内容")
        else:
            return "处理消息时出现错误"

    except Exception as e:
        print(f"Error communicating with chatbot: {e}")
        return "与聊天机器人通信时出现错误"

def text_to_speech(text):
    """Convert text to speech"""
    try:
        if not text:
            return None

        # Create temporary file to save audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts = gTTS(text, lang='zh')
            tts.save(tmpfile.name)
            return tmpfile.name
    except Exception as e:
        print(f"TTS error: {e}")
        return None

def respond(message, chat_history):
    """Main response function"""
    # Get chatbot response
    bot_message = send_message_to_chatbot(message)

    # Update chat history (user message)
    chat_history.append({"role": "user", "content": message})

    # Update chat history (assistant message)
    chat_history.append({"role": "assistant", "content": bot_message})

    # Generate TTS audio
    audio_file = text_to_speech(bot_message)

    return "", chat_history, audio_file

def clear_history():
    """Clear conversation history"""
    global latest_response
    with response_lock:
        latest_response = None
    return None, [], None

def retry_last_audio():
    """Retry playing the last audio response"""
    global latest_response
    with response_lock:
        if latest_response and "text" in latest_response:
            return text_to_speech(latest_response["text"])
    return None

# Create Gradio interface
with gr.Blocks(title="智能语音对话系统") as demo:
    gr.Markdown("# 智能语音对话系统")
    gr.Markdown("与AI助手实时对话，支持语音和文字输入")

    # Chat history
    chatbot = gr.Chatbot(label="对话记录", type="messages")

    # User input
    msg = gr.Textbox(label="输入消息", placeholder="输入你的消息或点击麦克风说话...")

    # TTS audio output
    tts_audio = gr.Audio(label="AI语音回复", autoplay=True, interactive=False, visible=True)

    # Control buttons
    with gr.Row():
        clear = gr.Button("清除对话")
        retry_audio = gr.Button("重播语音")

    # Status display
    status = gr.Textbox(label="系统状态", interactive=False)

    # Event handling
    msg.submit(respond, [msg, chatbot], [msg, chatbot, tts_audio])
    clear.click(clear_history, None, [msg, chatbot, tts_audio], queue=False)
    retry_audio.click(retry_last_audio, None, tts_audio)

    # Initialize connection status
    def update_status():
        if connect_to_chatbot():
            return "✓ 已连接到AI助手"
        else:
            return "✗ 无法连接到AI助手，请确保服务器正在运行"

    demo.load(update_status, None, status)

# Launch application
if __name__ == "__main__":
    demo.launch(share=True, inline=False)