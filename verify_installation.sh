#!/bin/bash

echo "Verifying Real-time Voice Conversation System Installation"
echo "========================================================"

echo "Checking Python version..."
python --version

echo ""
echo "Checking required packages..."
pip list | grep -E "fastapi|uvicorn|websockets|numpy|aiortc|langchain|openai|gradio|gtts|websocket-client"

echo ""
echo "Testing module imports..."

# Test core modules
echo "Testing main_system import..."
python -c "import main_system; print('✓ main_system imported successfully')"

echo "Testing integrated_asr_chatbot import..."
python -c "import integrated_asr_chatbot; print('✓ integrated_asr_chatbot imported successfully')"

echo "Testing enhanced_chatbot_app import..."
python -c "import enhanced_chatbot_app; print('✓ enhanced_chatbot_app imported successfully')"

echo "Testing voice_chat_server import..."
python -c "import voice_chat_server; print('✓ voice_chat_server imported successfully')"

echo ""
echo "Checking API key..."
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "⚠ Warning: DASHSCOPE_API_KEY environment variable not set"
    echo "  Please set it with: export DASHSCOPE_API_KEY=your_api_key_here"
else
    echo "✓ DASHSCOPE_API_KEY is set"
fi

echo ""
echo "Checking required files..."
REQUIRED_FILES=(
    "voice_chat_server.py"
    "integrated_asr_chatbot.py"
    "enhanced_chatbot_app.py"
    "main_system.py"
    "voice_chat_client.html"
    "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
    fi
done

echo ""
echo "Installation verification complete!"
echo "Run 'python main_system.py' to start the integrated system."