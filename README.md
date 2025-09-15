# 跨平台实时语音对话系统

这是一个基于WebRTC和Qwen-Omni AI的实时语音对话系统，支持跨平台运行。系统集成了科大讯飞ASR语音识别、CosyVoice TTS语音合成和Langchain聊天机器人，提供完整的语音对话解决方案。

## 功能特点

- 实时语音通信：基于WebRTC技术的实时音频流传输
- 语音识别：集成科大讯飞ASR实现高精度语音转文本
- 智能聊天机器人：使用阿里云Qwen-Omni-Turbo-Realtime模型
- 语音合成：集成CosyVoice2-0.5B TTS模型，支持多语言高质量语音输出
- 跨平台支持：可在Windows、Linux、macOS上运行
- 本地部署：支持离线运行，保护隐私
- 多用户支持：支持多人同时在线语音聊天
- Web界面：提供友好的Web客户端界面

## 系统架构

```
+------------------+     +------------------+     +------------------+
|   Web客户端      |     |   语音聊天服务器  |     |   聊天机器人      |
| (voice_chat_client.html)| (voice_chat_server.py)| (asr_chatbot.py)  |
+------------------+     +------------------+     +------------------+
         |                        |                        |
         |  WebRTC音频流          |  ASR文本               |  AI回复
         |----------------------->|----------------------->|------------>
         |                        |                        |            |
         |                        |  TTS音频               |  AI回复    |
         |  WebRTC音频流          |<-----------------------|<-----------|
         |<-----------------------|                        |
+------------------+     +------------------+     +------------------+
|   Gradio前端     |     |   CosyVoice TTS   |     |   模型文件        |
| (enhanced_chatbot_app.py)| (final_cosyvoice_tts.py)| (~/.cache/modelscope)|
+------------------+     +------------------+     +------------------+
```

## 系统要求

- Python 3.8+
- 支持WebRTC的浏览器
- 阿里云DashScope API密钥
- 科大讯飞ASR服务账号
- 磁盘空间：约2GB（用于CosyVoice模型文件）

## 安装和使用

### 1. 克隆项目

```bash
git clone https://github.com/grjyeah/WebRTC-With-QwenOmni.git
cd WebRTC-With-QwenOmni
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 设置环境变量

```bash
export DASHSCOPE_API_KEY=your_dashscope_api_key
export XF_APP_ID=your_iflytek_app_id
export XF_API_KEY=your_iflytek_api_key
export XF_API_SECRET=your_iflytek_api_secret
```

### 4. 启动系统

```bash
# 启动语音聊天服务器
python voice_chat_server.py

# 启动聊天机器人服务
python main_system.py

# 访问Web客户端
# 打开 voice_chat_client.html 进行语音聊天

# 访问Gradio前端
# 浏览器访问 http://localhost:7860
```

## 项目结构

```
.
├── voice_chat_server.py        # WebRTC语音聊天服务器
├── voice_chat_client.html      # WebRTC客户端界面
├── asr_chatbot.py             # Langchain聊天机器人
├── main_system.py             # 系统主入口
├── enhanced_chatbot_app.py    # Gradio前端界面
├── final_cosyvoice_tts.py     # CosyVoice TTS实现
├── fast_rtc_asr/              # 科大讯飞ASR Flutter集成
├── ~/.cache/modelscope/       # CosyVoice模型文件（自动下载）
├── requirements.txt           # 项目依赖
└── README.md                 # 项目说明文档
```

## 主要组件说明

### 1. WebRTC语音聊天服务器 (voice_chat_server.py)
- 基于FastAPI实现的WebSocket服务器
- 支持多用户房间管理
- 处理WebRTC信令交换
- 转发音频流和聊天消息

### 2. 科大讯飞ASR集成 (fast_rtc_asr/)
- Flutter实现的ASR客户端
- 实时音频流识别
- 支持多种语言识别

### 3. 聊天机器人 (asr_chatbot.py)
- 基于Langchain和Qwen-Omni-Turbo-Realtime模型
- 支持会话记忆
- 处理ASR文本并生成智能回复

### 4. CosyVoice TTS (final_cosyvoice_tts.py)
- 基于ModelScope的CosyVoice2-0.5B模型
- 跨平台支持
- 高质量多语言语音合成
- 本地模型加载，支持离线运行

## 自定义和扩展

你可以根据需要修改代码：

1. 更换聊天机器人模型
2. 添加新的TTS模型
3. 扩展ASR支持的语言
4. 自定义UI界面
5. 添加用户认证和权限管理
6. 集成数据库存储会话历史

## 注意事项

- 首次运行时会自动下载CosyVoice模型文件（约2GB）
- 需要有效的阿里云和科大讯飞API密钥
- 浏览器需要授予麦克风和摄像头权限
- 建议在支持WebRTC的现代浏览器中使用