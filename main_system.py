#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main orchestration file for the real-time voice conversation system.
Integrates all components: FastRTC service, ASR, Langchain chatbot, TTS, and Gradio frontend.
"""

import subprocess
import sys
import time
import signal
import os
from typing import List

class VoiceConversationSystem:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.is_running = False

    def start_fast_rtc_server(self):
        """Start the FastRTC WebRTC server"""
        print("Starting FastRTC WebRTC server...")
        process = subprocess.Popen([
            sys.executable, "voice_chat_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(process)
        print("✓ FastRTC server started on port 8001")
        return process

    def start_asr_chatbot(self):
        """Start the ASR chatbot server"""
        print("Starting ASR chatbot server...")
        process = subprocess.Popen([
            sys.executable, "asr_chatbot.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(process)
        print("✓ ASR chatbot server started on port 8765")
        return process

    def start_gradio_interface(self):
        """Start the Gradio frontend interface"""
        print("Starting Gradio interface...")
        process = subprocess.Popen([
            sys.executable, "chatbot_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(process)
        print("✓ Gradio interface started")
        return process

    def start_all_services(self):
        """Start all system services"""
        print("Starting real-time voice conversation system...")
        print("=" * 50)

        try:
            # Start services
            self.start_fast_rtc_server()
            self.start_asr_chatbot()
            self.start_gradio_interface()

            self.is_running = True
            print("=" * 50)
            print("All services started successfully!")
            print("Access the system at:")
            print("- Voice chat client: http://localhost:8001 (WebSocket server)")
            print("- Gradio interface: http://localhost:7860")
            print("- Press Ctrl+C to stop all services")
            print("=" * 50)

            # Keep the main thread alive
            while self.is_running:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nShutting down services...")
            self.stop_all_services()
        except Exception as e:
            print(f"Error starting services: {e}")
            self.stop_all_services()

    def stop_all_services(self):
        """Stop all running services"""
        print("Stopping all services...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error stopping process: {e}")

        self.processes.clear()
        self.is_running = False
        print("All services stopped.")

def signal_handler(sig, frame):
    """Handle system signals for graceful shutdown"""
    print('\nReceived interrupt signal. Shutting down...')
    sys.exit(0)

def main():
    """Main function to run the integrated system"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create and start the system
    system = VoiceConversationSystem()

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Real-time Voice Conversation System")
        print("Usage: python main_system.py [options]")
        print("Options:")
        print("  --help     Show this help message")
        print("")
        print("The system will start all required services:")
        print("1. FastRTC WebRTC server (port 8000)")
        print("2. ASR chatbot server (port 8765)")
        print("3. Gradio web interface (port 7860)")
        return

    # Start all services
    system.start_all_services()

if __name__ == "__main__":
    main()