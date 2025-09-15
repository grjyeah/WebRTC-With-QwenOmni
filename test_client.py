import asyncio
import websockets
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_asr_chatbot():
    """
    测试ASR Chatbot
    """
    uri = "ws://localhost:8765"

    try:
        async with websockets.connect(uri) as websocket:
            # 测试ASR文本处理
            test_messages = [
                {
                    "type": "asr_text",
                    "text": "你好，今天天气怎么样？",
                    "session_id": "session_1"
                },
                {
                    "type": "asr_text",
                    "text": "你能告诉我现在几点了吗？",
                    "session_id": "session_1"
                }
            ]

            for msg in test_messages:
                # 发送消息
                await websocket.send(json.dumps(msg, ensure_ascii=False))
                logger.info(f"Sent: {msg}")

                # 接收回复
                reply = await websocket.recv()
                logger.info(f"Received: {reply}")

                # 解析回复
                try:
                    reply_data = json.loads(reply)
                    print(f"Bot: {reply_data.get('text', '')}")
                except json.JSONDecodeError:
                    print(f"Failed to parse reply: {reply}")

                # 等待一段时间再发送下一个消息
                await asyncio.sleep(2)

            # 测试会话重置
            reset_msg = {
                "type": "reset_session",
                "session_id": "session_1"
            }

            await websocket.send(json.dumps(reset_msg, ensure_ascii=False))
            logger.info(f"Sent: {reset_msg}")

            # 接收回复
            reply = await websocket.recv()
            logger.info(f"Received: {reply}")

    except Exception as e:
        logger.error(f"Error connecting to WebSocket server: {e}")

if __name__ == "__main__":
    asyncio.run(test_asr_chatbot())