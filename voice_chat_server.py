from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import uuid
import logging
from typing import Dict, Set
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Real-time Voice Chat Server")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储连接的客户端
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str, room_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

        # 加入房间
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(client_id)

        logger.info(f"Client {client_id} connected to room {room_id}")

        # 通知房间内其他用户有新用户加入
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "client_id": client_id
        }, exclude_client=client_id)

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

        # 从所有房间中移除
        for room_id, clients in self.rooms.items():
            if client_id in clients:
                clients.remove(client_id)
                # 通知房间内其他用户该用户离开
                asyncio.create_task(self.broadcast_to_room(room_id, {
                    "type": "user_left",
                    "client_id": client_id
                }, exclude_client=client_id))

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_client: str = None):
        if room_id in self.rooms:
            for client_id in self.rooms[room_id]:
                if client_id != exclude_client and client_id in self.active_connections:
                    try:
                        await self.active_connections[client_id].send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"Error sending message to client {client_id}: {e}")

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Real-time Voice Chat Server is running"}

@app.websocket("/ws/{client_id}/{room_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, room_id: str):
    await manager.connect(websocket, client_id, room_id)
    try:
        while True:
            # 接收来自客户端的消息
            data = await websocket.receive_text()
            message = json.loads(data)

            # 处理不同类型的消息
            msg_type = message.get("type")

            if msg_type == "offer":
                # 转发offer给房间内其他用户
                await manager.broadcast_to_room(room_id, {
                    "type": "offer",
                    "sender": client_id,
                    "sdp": message.get("sdp")
                }, exclude_client=client_id)

            elif msg_type == "answer":
                # 转发answer给指定用户
                target_client = message.get("target")
                if target_client in manager.active_connections:
                    await manager.send_personal_message(json.dumps({
                        "type": "answer",
                        "sender": client_id,
                        "sdp": message.get("sdp")
                    }), target_client)

            elif msg_type == "ice_candidate":
                # 转发ICE候选给房间内其他用户
                await manager.broadcast_to_room(room_id, {
                    "type": "ice_candidate",
                    "sender": client_id,
                    "candidate": message.get("candidate")
                }, exclude_client=client_id)

            elif msg_type == "get_users":
                # 返回房间内所有用户
                if room_id in manager.rooms:
                    await manager.send_personal_message(json.dumps({
                        "type": "users_list",
                        "users": list(manager.rooms[room_id])
                    }), client_id)

    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
    finally:
        manager.disconnect(client_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)