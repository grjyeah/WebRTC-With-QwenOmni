# Real-time Voice Chat Server

This is a real-time voice chat server implementation using WebRTC and FastAPI.

## Features

- Real-time voice communication between multiple users
- Room-based chat system
- WebSocket-based signaling
- WebRTC peer-to-peer connections

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python voice_chat_server.py
   ```

   The server will start on `http://localhost:8001`

## Usage

1. Open `voice_chat_client.html` in a web browser
2. Enter a room ID and click "Connect"
3. Click "Start Voice Chat" to begin voice communication
4. Multiple users can join the same room for group voice chat

## API Endpoints

- `GET /` - Server status endpoint
- `WebSocket /ws/{client_id}/{room_id}` - WebSocket endpoint for real-time communication

## WebSocket Message Types

### Client to Server

1. `offer` - WebRTC offer for establishing connection
2. `answer` - WebRTC answer in response to an offer
3. `ice_candidate` - ICE candidate for NAT traversal
4. `get_users` - Request list of users in the room

### Server to Client

1. `user_joined` - Notification when a user joins the room
2. `user_left` - Notification when a user leaves the room
3. `offer` - Forwarded WebRTC offer from another user
4. `answer` - Forwarded WebRTC answer from another user
5. `ice_candidate` - Forwarded ICE candidate from another user
6. `users_list` - List of users in the room

## How it Works

1. Clients connect to the server via WebSocket with a client ID and room ID
2. When a client wants to start voice chat, they request the list of users in the room
3. For each user in the room, the client creates a WebRTC peer connection
4. The signaling process (offer/answer/ICE candidates) is exchanged through the WebSocket server
5. Once the WebRTC connection is established, voice data flows directly between clients

## Security Considerations

This is a basic implementation for demonstration purposes. For production use, consider:

- Adding authentication and authorization
- Using HTTPS/WSS in production
- Validating all incoming messages
- Implementing rate limiting