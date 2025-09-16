# Voice Chat System - Debugging and Testing Guide

## Overview

This document provides instructions for debugging and testing the voice chat system with ASR and chatbot integration.

## System Components

1. **Voice Chat Server** (`voice_chat_server.py`) - Runs on port 8001
2. **ASR Chatbot Server** (`asr_chatbot.py`) - Runs on port 8765
3. **Frontend Client** (`voice_chat_client.html`)

## Debugging Steps

### 1. Start the System

```bash
python test_voice_chat_system.py
```

This will start both servers and keep them running.

### 2. Test Connectivity

Check that both servers are running:
```bash
# Check voice chat server
curl http://localhost:8001/

# Check that ports are open
lsof -i :8001
lsof -i :8765
```

### 3. Test with Frontend

1. Open `voice_chat_client.html` in your browser
2. Use the "Test ASR Input" field to send text messages
3. Verify that responses appear in the chat display area

### 4. Check Log Files

- `voice_chat_server.log` - Voice chat server logs
- `asr_chatbot_basic.log` - ASR chatbot logs

## Manual Testing

You can also start services manually:

```bash
# Terminal 1: Start voice chat server
python voice_chat_server.py

# Terminal 2: Start ASR chatbot server
python asr_chatbot.py

# Terminal 3: Run test client
python test_asr_chatbot_connection.py
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure both servers are running
2. **No Response Displayed**: Check browser console for errors
3. **ASR Text Not Processed**: Check server logs for message handling

### Log Analysis

Look for these key log messages:
- "ASR text received" - Voice chat server received ASR text
- "Processing ASR text" - ASR chatbot is processing the text
- "Generated response" - Chatbot generated a response
- "Bot response received" - Frontend received the response

## Key Changes Made

1. **Enhanced Logging**: Added detailed file and console logging
2. **Server Integration**: Voice chat server now connects to ASR chatbot
3. **Message Handling**: Added ASR text processing and response broadcasting
4. **UI Updates**: Added chat display area to show messages
5. **Testing Tools**: Added test scripts and debugging features

## Files Modified

- `voice_chat_server.py` - Added ASR chatbot integration
- `asr_chatbot.py` - Enhanced logging and message handling
- `integrated_asr_chatbot.py` - Enhanced logging
- `voice_chat_client.html` - Added chat display and test input
- `test_asr_chatbot_connection.py` - Test script for WebSocket connection
- `test_voice_chat_system.py` - Integration test script
- `DEBUGGING_SUMMARY.md` - This debugging summary