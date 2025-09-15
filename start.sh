#!/bin/bash

# ASR Chatbot启动脚本

echo "ASR Chatbot System"
echo "=================="

echo "1. 启动ASR聊天机器人服务 (端口 8765)"
echo "2. 启动WebRTC语音聊天服务器 (端口 8000)"
echo "3. 启动Gradio聊天界面演示"
echo "4. 启动所有服务"

read -p "请选择要启动的服务 (1-4): " choice

case $choice in
  1)
    echo "启动ASR聊天机器人服务..."
    python asr_chatbot.py
    ;;
  2)
    echo "启动WebRTC语音聊天服务器..."
    python voice_chat_server.py
    ;;
  3)
    echo "启动Gradio聊天界面演示..."
    python chatbot_app.py
    ;;
  4)
    echo "启动所有服务..."
    echo "在后台启动ASR聊天机器人服务..."
    python asr_chatbot.py &
    ASR_PID=$!

    echo "在后台启动WebRTC语音聊天服务器..."
    python voice_chat_server.py &
    WEBRTC_PID=$!

    echo "启动Gradio聊天界面演示..."
    python chatbot_app.py

    # 清理后台进程
    kill $ASR_PID $WEBRTC_PID 2>/dev/null
    ;;
  *)
    echo "无效选择"
    ;;
esac