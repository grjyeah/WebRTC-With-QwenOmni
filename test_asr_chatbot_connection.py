#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify the connection between voice chat server and ASR chatbot.
"""

import websocket
import json
import time
import threading

def on_message(ws, message):
    """Handle incoming messages"""
    print(f"Received: {message}")
    try:
        data = json.loads(message)
        if data.get("type") == "bot_response":
            print(f"Bot response: {data.get('text')}")
        elif data.get("type") == "error":
            print(f"Error: {data.get('message')}")
    except Exception as e:
        print(f"Error parsing message: {e}")

def on_error(ws, error):
    """Handle WebSocket errors"""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure"""
    print("WebSocket connection closed")

def on_open(ws):
    """Handle WebSocket opening"""
    print("Connected to voice chat server")

    # Send test ASR text message
    def send_test_messages():
        time.sleep(1)

        # Test ASR text message
        test_msg = {
            "type": "asr_text",
            "text": "你好，你是谁？"
        }
        print("Sending ASR text message...")
        ws.send(json.dumps(test_msg, ensure_ascii=False))

        time.sleep(3)
        ws.close()

    # Start sending messages in a separate thread
    threading.Thread(target=send_test_messages, daemon=True).start()

def test_voice_chat_connection():
    """Test connection to the voice chat server"""
    print("Testing connection to voice chat server...")

    try:
        # Create WebSocket connection to voice chat server (port 8001)
        ws = websocket.WebSocketApp("ws://localhost:8001/ws/test_client/test_room",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

        # Run the WebSocket connection
        ws.run_forever()

    except Exception as e:
        print(f"Failed to connect to voice chat server: {e}")
        print("Please ensure the voice chat server is running on port 8001")

if __name__ == "__main__":
    test_voice_chat_connection()