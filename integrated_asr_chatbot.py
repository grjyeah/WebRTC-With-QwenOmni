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
import tempfile
# 将gTTS替换为CosyVoice TTS
from cosyvoice_tts import CosyVoiceTTS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('asr_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntegratedASRChatbot:
    def __init__(self, api_key: str, model_name: str = "qwen-omni-turbo-realtime"):
        """
        初始化集成ASR Chatbot

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
            ("system", "你是一个智能语音助手。请根据用户的语音输入提供相应的回答。保持回答简洁明了。如果是简短的回应，可以直接回复。如果是较长的回答，可以分段回复。"),
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
            logger.info(f"Session ID: {session_id}")

            # Log the current memory state
            memory_context = self.memory.load_memory_variables({})
            logger.info(f"Memory context: {memory_context}")

            response = await self.chain.arun(input=text)
            logger.info(f"Generated response: {response}")

            # Log the updated memory state
            updated_memory = self.memory.load_memory_variables({})
            logger.info(f"Updated memory context: {updated_memory}")

            return response
        except Exception as e:
            logger.error(f"Error processing ASR text: {e}", exc_info=True)
            return "抱歉，处理您的请求时出现了错误。"

    def text_to_speech(self, text: str) -> str:
        """
        将文本转换为语音文件

        Args:
            text: 要转换的文本

        Returns:
            音频文件路径
        """
        try:
            # 使用CosyVoice TTS生成语音
            tts = CosyVoiceTTS(voice="中文女")
            # 创建临时文件来保存音频（使用.wav格式）
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                output_path = tts.speak_to_file(text, tmpfile.name)
                return output_path
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None

    async def handle_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理不同类型的消息

        Args:
            data: 消息数据

        Returns:
            回复消息
        """
        logger.info(f"Handling message: {data}")
        msg_type = data.get("type", "")

        if msg_type == "asr_text":
            # 处理ASR文本
            asr_text = data.get("text", "")
            session_id = data.get("session_id", None)
            client_id = data.get("client_id", None)

            logger.info(f"ASR text received: '{asr_text}' from client {client_id} in session {session_id}")

            if asr_text:
                response_text = await self.process_asr_text(asr_text, session_id)
                audio_file = self.text_to_speech(response_text)

                logger.info(f"Generated response text: '{response_text}' for client {client_id}")

                return {
                    "type": "bot_response",
                    "text": response_text,
                    "audio_file": audio_file,
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

        elif msg_type == "text_message":
            # 处理文本消息（来自Gradio界面）
            user_text = data.get("text", "")
            session_id = data.get("session_id", None)
            client_id = data.get("client_id", None)

            logger.info(f"Text message received: '{user_text}' from client {client_id} in session {session_id}")

            if user_text:
                response_text = await self.process_asr_text(user_text, session_id)
                audio_file = self.text_to_speech(response_text)

                logger.info(f"Generated response text: '{response_text}' for client {client_id}")

                return {
                    "type": "bot_response",
                    "text": response_text,
                    "audio_file": audio_file,
                    "session_id": session_id,
                    "client_id": client_id
                }
            else:
                logger.warning("Received empty text message")
                return {
                    "type": "error",
                    "message": "收到空的文本消息",
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
        try:
            async for message in websocket:
                try:
                    # 解析收到的消息
                    data = json.loads(message)
                    logger.info(f"Received message: {data}")

                    # 处理消息
                    reply = await self.handle_message(data)

                    # 发送回复
                    await websocket.send(json.dumps(reply, ensure_ascii=False))

                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON message")
                    error_reply = {
                        "type": "error",
                        "message": "JSON解析失败"
                    }
                    await websocket.send(json.dumps(error_reply, ensure_ascii=False))
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    error_reply = {
                        "type": "error",
                        "message": "处理消息时出现错误"
                    }
                    await websocket.send(json.dumps(error_reply, ensure_ascii=False))
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")

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
    chatbot = IntegratedASRChatbot(api_key)

    # 启动WebSocket服务器
    chatbot.run_websocket_server()

if __name__ == "__main__":
    main()