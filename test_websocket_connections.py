#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple test to verify WebSocket connections between voice chat server and ASR chatbot.
"""

import asyncio
import websockets
import json

async def test_connections():
    """Test WebSocket connections"""
    print("Testing WebSocket connections...")

    try:
        # Test connection to voice chat server
        print("1. Testing connection to voice chat server (port 8001)...")
        voice_uri = "ws://localhost:8001/ws/test_client/test_room"
        async with websockets.connect(voice_uri) as voice_ws:
            print("   ✓ Connected to voice chat server")

            # Test connection to ASR chatbot server
            print("2. Testing connection to ASR chatbot server (port 8765)...")
            asr_uri = "ws://localhost:8765"
            async with websockets.connect(asr_uri) as asr_ws:
                print("   ✓ Connected to ASR chatbot server")

                # Test sending a message through voice chat server to ASR chatbot
                print("3. Testing message flow...")

                # Send ASR text to voice chat server
                test_message = {
                    "type": "asr_text",
                    "text": "你好，测试消息",
                    "client_id": "test_client",
                    "session_id": "test_room"
                }

                await voice_ws.send(json.dumps(test_message, ensure_ascii=False))
                print("   ✓ Sent ASR text to voice chat server")

                # Wait for response (with timeout)
                try:
                    response = await asyncio.wait_for(voice_ws.recv(), timeout=10.0)
                    response_data = json.loads(response)
                    print(f"   ✓ Received response: {response_data}")

                    if response_data.get("type") == "bot_response":
                        print("   ✓ Message flow working correctly")
                        print(f"   ✓ Bot response: {response_data.get('text')}")
                    else:
                        print(f"   ! Unexpected response type: {response_data.get('type')}")

                except asyncio.TimeoutError:
                    print("   ! Timeout waiting for response")

        print("\n✓ All connection tests completed")

    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connections())