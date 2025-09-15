import asyncio
import websockets
import json
import uuid

async def test_client():
    # 生成随机客户端ID
    client_id = str(uuid.uuid4())
    room_id = "test_room"

    # 连接到WebSocket服务器
    uri = f"ws://localhost:8001/ws/{client_id}/{room_id}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server as {client_id}")

        # 发送获取用户列表的请求
        await websocket.send(json.dumps({
            "type": "get_users"
        }))

        # 等待并打印服务器响应
        try:
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(test_client())