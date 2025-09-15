# Real-time Voice Conversation System

An integrated system that combines WebRTC voice communication, ASR (Automatic Speech Recognition), Langchain chatbot, TTS (Text-to-Speech), and Gradio frontend for a complete voice conversation experience.

## System Overview

This project implements a complete real-time voice conversation system with the following capabilities:

1. **Voice Communication**: Real-time peer-to-peer voice chat using WebRTC
2. **Speech Recognition**: Automatic conversion of speech to text
3. **AI Chatbot**: Intelligent responses using Langchain and Qwen model
4. **Text-to-Speech**: Conversion of text responses to audio
5. **Multiple Interfaces**: Both voice and text-based user interfaces

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Web Client    │◄──►│  FastRTC Server  │◄──►│  Audio Streams   │
│ (voice_chat_    │    │ (voice_chat_     │    │                  │
│  client.html)   │    │  server.py)      │    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                ▲
                                │ WebSocket
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Gradio Web UI  │◄──►│ ASR Chatbot API  │◄──►│  Langchain LLM   │
│ (enhanced_      │    │ (integrated_     │    │                  │
│  chatbot_app.py)│    │  asr_chatbot.py) │    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                ▲
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐
│  Audio Output   │◄──►│     TTS          │
│                 │    │                  │
└─────────────────┘    └──────────────────┘
```

## Key Components

### 1. FastRTC Service (`voice_chat_server.py`)
- WebRTC server for real-time audio streaming
- WebSocket signaling for peer-to-peer connections
- Manages user rooms and connections
- Runs on port 8000

### 2. ASR Chatbot (`integrated_asr_chatbot.py`)
- Processes ASR text and generates AI responses
- Integrates with Langchain and Qwen model
- Provides WebSocket API on port 8765
- Handles both voice and text inputs
- Integrated TTS functionality

### 3. TTS System
- Converts text responses to audio using gTTS
- Supports multiple languages
- Integrated directly into the chatbot

### 4. Gradio Frontend (`enhanced_chatbot_app.py`)
- Web interface for text-based interaction
- Real-time audio playback of AI responses
- Connects to chatbot via WebSocket
- User-friendly chat interface

### 5. Voice Client (`voice_chat_client.html`)
- Web-based client for voice communication
- Captures and streams audio via WebRTC
- Connects to FastRTC server

## Prerequisites

- Python 3.8+
- macOS, Linux, or Windows with WSL
- Microphone for voice input
- Speakers or headphones for audio output
- DashScope API key for Qwen model access

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MyProject3
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export DASHSCOPE_API_KEY=your_dashscope_api_key_here
   ```

## Usage

### Option 1: Start All Services with Main Coordinator

```bash
python main_system.py
```

### Option 2: Use Startup Scripts

```bash
# Start the integrated system
./start_integrated.sh

# Or start the original system
./start.sh
```

### Option 3: Start Components Manually

1. Start FastRTC server:
   ```bash
   python voice_chat_server.py
   ```

2. Start ASR chatbot:
   ```bash
   python integrated_asr_chatbot.py
   ```

3. Start Gradio interface:
   ```bash
   python enhanced_chatbot_app.py
   ```

## Accessing the System

- **Voice Chat Client**: Open `voice_chat_client.html` in a web browser
- **Text Chat Interface**: Visit `http://localhost:7860` after starting Gradio
- **FastRTC Server**: Available at `ws://localhost:8000`
- **ASR Chatbot API**: Available at `ws://localhost:8765`

## Project Structure

```
.
├── fast_rtc_asr/               # FastRTC Dart ASR implementation
├── voice_chat_server.py        # FastRTC WebRTC server
├── asr_chatbot.py              # Original ASR chatbot
├── integrated_asr_chatbot.py   # Enhanced ASR chatbot with TTS
├── chatbot_app.py              # Original Gradio interface
├── enhanced_chatbot_app.py     # Enhanced Gradio interface
├── main_system.py              # Main system orchestrator
├── voice_chat_client.html      # Web-based voice client
├── requirements.txt            # Python dependencies
├── start.sh                    # Original startup script
├── start_integrated.sh         # Integrated system startup script
├── COMPREHENSIVE_README.md     # This file
├── SYSTEM_ARCHITECTURE.md      # Detailed system architecture
├── INTEGRATED_SYSTEM_README.md # Comprehensive usage guide
├── VOICE_CHAT_README.md        # Voice chat component documentation
└── TTS_IMPLEMENTATION_SUMMARY.md # TTS implementation details
```

## Features

- Real-time voice communication using WebRTC
- Automatic speech recognition and transcription
- AI-powered chatbot responses using Qwen model
- Text-to-speech for audio responses
- Web-based text chat interface with Gradio
- Multi-user room support
- Cross-platform compatibility
- Modular architecture for easy extension

## Testing

Run the integration test to verify all components work together:

```bash
python test_integration.py
```

## Troubleshooting

1. **Connection Issues**: Ensure all services are running and ports are not blocked
2. **Audio Problems**: Check microphone and speaker permissions in your browser
3. **API Key Errors**: Verify your DASHSCOPE_API_KEY is set correctly
4. **Dependency Issues**: Run `pip install -r requirements.txt` to install all dependencies

## Extending the System

The modular architecture allows for easy extension:

1. Replace ASR with custom implementation
2. Integrate different LLM models
3. Add custom TTS engines
4. Implement additional frontend interfaces
5. Add database for conversation history

## License

This project is licensed under the MIT License - see the LICENSE file for details.