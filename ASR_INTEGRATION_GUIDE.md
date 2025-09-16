# ASR Integration Guide

## Current System Architecture

1. **Frontend (voice_chat_client.html)**: WebRTC client that captures audio and sends it peer-to-peer
2. **Backend (voice_chat_server.py)**: WebSocket server that routes messages between clients and the ASR chatbot
3. **ASR Chatbot (asr_chatbot.py)**: Processes ASR text and generates responses
4. **iFlytek ASR Service**: External service for speech recognition (accessed via Flutter client)

## Identified Issues

1. **Missing ASR Integration**: Audio captured by WebRTC is not being sent to the iFlytek ASR service
2. **Incomplete Flow**: The system can send test text directly but doesn't convert audio to text

## Required Fixes

### 1. Audio Processing Integration

The current implementation needs to:

1. Capture audio via WebRTC `getUserMedia()`
2. Process audio chunks in real-time
3. Send audio to iFlytek ASR service
4. Receive text results and forward to the chatbot

### 2. Implementation Options

#### Option A: JavaScript WebSocket ASR Client
Create a JavaScript implementation that connects directly to iFlytek ASR service.

#### Option B: Server-side Audio Processing
Send audio data to the backend server which then processes it with the ASR service.

#### Option C: Hybrid Approach
Use the existing Flutter ASR client but integrate it with the WebRTC flow.

## Recommended Solution

Modify the HTML client to:

1. Capture audio via WebRTC
2. Process audio chunks in real-time
3. Send audio chunks to a dedicated ASR WebSocket endpoint
4. Receive text results and send to the existing chat flow

## Implementation Steps

1. Add audio processing to capture and convert audio chunks
2. Implement WebSocket connection to iFlytek ASR service
3. Handle ASR responses and forward to existing text flow
4. Add proper error handling and logging

## Current Status

The ASR client implementation in Flutter (xf_asr_client.dart) has been enhanced with comprehensive logging to trace the ASR processing flow. However, the integration between WebRTC audio capture and ASR processing is missing in the HTML client.

To fully resolve this issue, a complete ASR integration solution needs to be implemented that bridges the gap between WebRTC audio capture and iFlytek ASR processing.