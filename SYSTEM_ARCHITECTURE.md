# Real-time Voice Conversation System Architecture

## System Components

1. **FastRTC Service (WebRTC Server)**
   - Handles real-time audio streaming between clients
   - Manages WebSocket connections for signaling
   - Implemented in `voice_chat_server.py`

2. **ASR Processing**
   - Processes audio stream and converts speech to text
   - Implemented in FastRTC Dart components

3. **Langchain Chatbot**
   - Processes text input and generates intelligent responses
   - Implemented in `asr_chatbot.py`

4. **TTS System**
   - Converts text responses to audio
   - Implemented in `chat_tts.py` and `advanced_chat_tts.py`

5. **Gradio Frontend**
   - Provides user interface for text-based interaction
   - Implemented in `chatbot_app.py` and `final_chatbot.py`

## Integration Flow

1. **Voice Path**:
   - Client speaks → FastRTC captures audio → ASR converts to text → Langchain chatbot processes text → TTS converts response to audio → Client hears response

2. **Text Path**:
   - User types in Gradio interface → Langchain chatbot processes text → TTS converts response to audio → User hears response

## Communication Architecture

- FastRTC Server (port 8000): Handles WebRTC signaling
- ASR Chatbot Server (port 8765): Processes ASR text and generates responses
- Gradio Interface (port 7860): Provides web UI for text interaction

## Data Flow

1. Audio stream from client → FastRTC server → ASR processing → Text to chatbot
2. Chatbot response → TTS processing → Audio stream to client
3. Text input from Gradio → Chatbot → TTS processing → Audio output in browser