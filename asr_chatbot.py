import os
import json
import logging
import asyncio
import websockets
from typing import Dict, Any, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('asr_chatbot_basic.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ASRChatbot:
    def __init__(self, api_key: str, model_name: str = "qwen-omni-turbo-realtime"):
        """
        初始化ASR Chatbot

        Args:
            api_key: 阿里云百炼平台的API密钥
            model_name: 使用的模型名称
        """
        self.api_key = api_key
        self.model_name = model_name

        # 初始化Qwen模型
        self.llm = ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )

        # 创建对话记忆
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # 创建对话模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个智能语音助手。请根据用户的语音输入提供相应的回答。保持回答简洁明了。"),
            ("placeholder", "{chat_history}"),
            ("user", "{input}")
        ])

        # 创建对话链
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)

    async def process_asr_text(self, text: str, session_id: Optional[str] = None) -> str:
        """
        处理ASR文本并生成回复

        Args:
            text: ASR识别的文本
            session_id: 会话ID（可选）

        Returns:
            模型生成的回复
        """
        try:
            logger.info(f"Processing ASR text: {text}")
            if not text or not text.strip():
                logger.warning("Received empty or whitespace-only ASR text")
                return "我没有听清楚您说什么，请您再说一遍。"

            # Log the input text length and first 50 characters for debugging
            logger.info(f"ASR text length: {len(text)}, first 50 chars: {text[:50]}")

            response = await self.chain.arun(input=text)
            logger.info(f"Generated response: {response}")

            if not response or not response.strip():
                logger.warning("Generated empty response from LLM")
                return "我没有理解您的意思，请您换个说法再试一次。"

            return response
        except Exception as e:
            logger.error(f"Error processing ASR text: {e}", exc_info=True)
            return "抱歉，处理您的请求时出现了错误。"

    async def handle_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理不同类型的消息

        Args:
            data: 消息数据

        Returns:
            回复消息
        """
        logger.info(f"ASR Chatbot handling message: {data}")
        msg_type = data.get("type", "")

        if msg_type == "asr_text":
            # 处理ASR文本
            asr_text = data.get("text", "")
            session_id = data.get("session_id", None)
            client_id = data.get("client_id", None)

            logger.info(f"Processing ASR text: '{asr_text}' from client {client_id} in session {session_id}")

            if asr_text:
                response_text = await self.process_asr_text(asr_text, session_id)
                logger.info(f"Generated response: '{response_text}' for client {client_id}")
                return {
                    "type": "bot_response",
                    "text": response_text,
                    "session_id": session_id,
                    "client_id": client_id
                }
            else:
                logger.warning("Received empty ASR text")
                return {
                    "type": "error",
                    "message": "收到空的ASR文本",
                    "session_id": session_id,
                    "client_id": client_id
                }

        elif msg_type == "reset_session":
            # 重置会话
            session_id = data.get("session_id", None)
            client_id = data.get("client_id", None)
            self.memory.clear()
            logger.info(f"Session reset for client {client_id} in session {session_id}")
            return {
                "type": "session_reset",
                "message": "会话已重置",
                "session_id": session_id,
                "client_id": client_id
            }

        else:
            logger.warning(f"Unknown message type: {msg_type}")
            return {
                "type": "error",
                "message": f"未知的消息类型: {msg_type}",
                "client_id": data.get("client_id", None)
            }

    async def websocket_server(self, websocket, path):
        """
        WebSocket服务器处理函数

        Args:
            websocket: WebSocket连接对象
            path: 请求路径
        """
        logger.info(f"New WebSocket connection established: {path}")
        try:
            async for message in websocket:
                try:
                    # 解析收到的消息
                    data = json.loads(message)
                    logger.info(f"Received message: {data}")

                    # 处理消息
                    reply = await self.handle_message(data)
                    logger.info(f"Sending reply: {reply}")

                    # 发送回复
                    await websocket.send(json.dumps(reply, ensure_ascii=False))

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON message: {e}")
                    error_reply = {
                        "type": "error",
                        "message": "JSON解析失败"
                    }
                    await websocket.send(json.dumps(error_reply, ensure_ascii=False))
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    error_reply = {
                        "type": "error",
                        "message": "处理消息时出现错误"
                    }
                    await websocket.send(json.dumps(error_reply, ensure_ascii=False))
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket error: {e}", exc_info=True)

    def run_websocket_server(self, host="localhost", port=8765):
        """
        启动WebSocket服务器

        Args:
            host: 服务器主机地址
            port: 服务器端口
        """
        start_server = websockets.serve(self.websocket_server, host, port)
        logger.info(f"WebSocket server started on {host}:{port}")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

def main():
    """
    主函数
    """
    # 从环境变量获取API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        logger.error("请设置DASHSCOPE_API_KEY环境变量")
        return

    # 创建并启动chatbot
    chatbot = ASRChatbot(api_key)

    # 启动WebSocket服务器
    chatbot.run_websocket_server()

if __name__ == "__main__":
    main()