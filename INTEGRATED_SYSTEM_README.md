# Real-time Voice Conversation System

An integrated system that combines WebRTC voice communication, ASR (Automatic Speech Recognition), Langchain chatbot, TTS (Text-to-Speech), and Gradio frontend for a complete voice conversation experience.

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

## Components

1. **FastRTC Service** (`voice_chat_server.py`)
   - WebRTC server for real-time audio streaming
   - WebSocket signaling for peer-to-peer connections
   - Runs on port 8000

2. **ASR Chatbot** (`integrated_asr_chatbot.py`)
   - Processes ASR text and generates AI responses
   - Integrates with Langchain and Qwen model
   - Provides WebSocket API on port 8765
   - Handles both voice and text inputs

3. **TTS System** (Integrated in chatbot)
   - Converts text responses to audio using gTTS
   - Supports multiple languages

4. **Gradio Frontend** (`enhanced_chatbot_app.py`)
   - Web interface for text-based interaction
   - Real-time audio playback of AI responses
   - Connects to chatbot via WebSocket

5. **Voice Client** (`voice_chat_client.html`)
   - Web-based client for voice communication
   - Captures and streams audio via WebRTC

## Prerequisites

- Python 3.8+
- macOS, Linux, or Windows with WSL
- Microphone for voice input
- Speakers or headphones for audio output

## Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export DASHSCOPE_API_KEY=your_api_key_here
   ```

## Usage

### Option 1: Start Individual Components

```bash
# Start the original system
./start.sh

# Or start the integrated system
./start_integrated.sh
```

### Option 2: Start All Services with Main Coordinator

```bash
python main_system.py
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

## Features

- Real-time voice communication using WebRTC
- Automatic speech recognition and transcription
- AI-powered chatbot responses using Qwen model
- Text-to-speech for audio responses
- Web-based text chat interface with Gradio
- Multi-user room support
- Cross-platform compatibility

## Development

### Project Structure

```
.
├── fast_rtc_asr/           # FastRTC Dart ASR implementation
├── voice_chat_server.py    # FastRTC WebRTC server
├── integrated_asr_chatbot.py # Enhanced ASR chatbot with TTS
├── enhanced_chatbot_app.py # Enhanced Gradio interface
├── main_system.py          # Main system orchestrator
├── voice_chat_client.html  # Web-based voice client
├── requirements.txt        # Python dependencies
├── start.sh                # Original startup script
├── start_integrated.sh     # Integrated system startup script
└── README.md              # This file
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