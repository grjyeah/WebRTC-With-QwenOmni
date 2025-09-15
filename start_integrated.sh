#!/bin/bash

# Integrated Real-time Voice Conversation System Startup Script

echo "Integrated Real-time Voice Conversation System"
echo "============================================="

echo "1. 启动集成ASR聊天机器人服务 (端口 8765)"
echo "2. 启动WebRTC语音聊天服务器 (端口 8000)"
echo "3. 启动增强Gradio聊天界面演示"
echo "4. 启动完整的集成系统 (所有服务)"
echo "5. 启动主系统协调器"

read -p "请选择要启动的服务 (1-5): " choice

case $choice in
  1)
    echo "启动集成ASR聊天机器人服务..."
    python integrated_asr_chatbot.py
    ;;
  2)
    echo "启动WebRTC语音聊天服务器..."
    python voice_chat_server.py
    ;;
  3)
    echo "启动增强Gradio聊天界面演示..."
    python enhanced_chatbot_app.py
    ;;
  4)
    echo "启动完整的集成系统..."
    echo "在后台启动集成ASR聊天机器人服务..."
    python integrated_asr_chatbot.py &
    ASR_PID=$!

    echo "在后台启动WebRTC语音聊天服务器..."
    python voice_chat_server.py &
    WEBRTC_PID=$!

    echo "启动增强Gradio聊天界面演示..."
    python enhanced_chatbot_app.py

    # Clean up background processes
    kill $ASR_PID $WEBRTC_PID 2>/dev/null
    ;;
  5)
    echo "启动主系统协调器..."
    python main_system.py
    ;;
  *)
    echo "无效选择"
    ;;
esac