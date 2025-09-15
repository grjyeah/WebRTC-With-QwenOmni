#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify the integration of all system components.
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
    print("Connected to ASR chatbot server")

    # Send test messages
    def send_test_messages():
        time.sleep(1)

        # Test 1: Simple text message
        test_msg1 = {
            "type": "text_message",
            "text": "你好，你是谁？",
            "session_id": "test_session_1"
        }
        print("Sending test message 1...")
        ws.send(json.dumps(test_msg1, ensure_ascii=False))

        time.sleep(3)

        # Test 2: Another text message
        test_msg2 = {
            "type": "text_message",
            "text": "今天天气怎么样？",
            "session_id": "test_session_1"
        }
        print("Sending test message 2...")
        ws.send(json.dumps(test_msg2, ensure_ascii=False))

        time.sleep(3)

        # Test 3: Reset session
        test_msg3 = {
            "type": "reset_session",
            "session_id": "test_session_1"
        }
        print("Sending session reset...")
        ws.send(json.dumps(test_msg3, ensure_ascii=False))

        time.sleep(1)
        ws.close()

    # Start sending messages in a separate thread
    threading.Thread(target=send_test_messages, daemon=True).start()

def test_chatbot_connection():
    """Test connection to the chatbot server"""
    print("Testing connection to ASR chatbot server...")

    try:
        # Create WebSocket connection
        ws = websocket.WebSocketApp("ws://localhost:8765",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

        # Run the WebSocket connection
        ws.run_forever()

    except Exception as e:
        print(f"Failed to connect to chatbot server: {e}")
        print("Please ensure the ASR chatbot server is running on port 8765")

if __name__ == "__main__":
    test_chatbot_connection()