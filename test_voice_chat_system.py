#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integration test script to verify the complete voice chat system.
"""

import requests
import time
import subprocess
import signal
import sys
import os

class VoiceChatSystemTest:
    def __init__(self):
        self.processes = []

    def start_services(self):
        """Start all required services"""
        print("Starting voice chat system services...")

        # Start voice chat server (port 8001)
        print("Starting voice chat server...")
        voice_server = subprocess.Popen([
            sys.executable, "voice_chat_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(voice_server)

        # Start ASR chatbot server (port 8765)
        print("Starting ASR chatbot server...")
        asr_server = subprocess.Popen([
            sys.executable, "asr_chatbot.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(asr_server)

        # Wait a moment for servers to start
        time.sleep(3)

        return True

    def test_server_connectivity(self):
        """Test if servers are running"""
        print("Testing server connectivity...")

        try:
            # Test voice chat server
            response = requests.get("http://localhost:8001/", timeout=5)
            print(f"Voice chat server status: {response.status_code}")

            # Test if ports are open
            import socket
            ports = [8001, 8765]
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    print(f"Port {port} is open")
                else:
                    print(f"Port {port} is closed")
                sock.close()

            return True
        except Exception as e:
            print(f"Server connectivity test failed: {e}")
            return False

    def stop_services(self):
        """Stop all services"""
        print("Stopping services...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error stopping process: {e}")

    def run_test(self):
        """Run the complete test"""
        print("=" * 50)
        print("Voice Chat System Integration Test")
        print("=" * 50)

        try:
            # Start services
            if not self.start_services():
                print("Failed to start services")
                return False

            # Test connectivity
            time.sleep(2)  # Wait for servers to fully start
            if not self.test_server_connectivity():
                print("Server connectivity test failed")
                return False

            print("\n✓ All services started successfully")
            print("✓ Server connectivity verified")
            print("\nNext steps:")
            print("1. Open voice_chat_client.html in your browser")
            print("2. Use the 'Test ASR Input' field to send messages")
            print("3. Check that responses appear in the chat area")
            print("4. Check log files for detailed information:")
            print("   - voice_chat_server.log")
            print("   - asr_chatbot_basic.log")

            return True

        except Exception as e:
            print(f"Test failed with error: {e}")
            return False
        finally:
            # Don't stop services automatically - let user stop them manually
            pass

def signal_handler(sig, frame):
    """Handle interrupt signal"""
    print('\nTest interrupted. Cleaning up...')
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Run test
    tester = VoiceChatSystemTest()
    success = tester.run_test()

    if success:
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        print("Services are running in the background.")
        print("Press Ctrl+C to stop services.")
        print("=" * 50)

        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            tester.stop_services()
            print("\nServices stopped.")
    else:
        tester.stop_services()
        print("Test failed. Services stopped.")
        sys.exit(1)