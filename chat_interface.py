import gradio as gr
import time

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

# 创建Gradio聊天界面
demo = gr.ChatInterface(
    fn=chatbot_response,
    title="Chatbot with TTS",
    description="与chatbot实时对话"
)

# 启动应用
if __name__ == "__main__":
    demo.launch(share=True)