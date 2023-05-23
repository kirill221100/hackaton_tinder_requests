from fastapi import WebSocket
from typing import Dict

PROFILE_CONNECTIONS = {}
USER_CONNECTIONS = {}


class ProfileManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = PROFILE_CONNECTIONS

    async def connect(self, websocket: WebSocket, connection_id: int):
        await websocket.accept()
        self.active_connections[connection_id] = websocket

    def disconnect(self, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: dict):
        user_ws = self.get_ws(message["profile_id"])
        if user_ws:
            websocket: WebSocket = user_ws
            await websocket.send_json(message)
            return True
        return False

    def get_ws(self, user_id: int):
        return self.active_connections.get(user_id)


class UserManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = USER_CONNECTIONS

    async def connect(self, websocket: WebSocket, connection_id: int):
        await websocket.accept()
        self.active_connections[connection_id] = websocket

    def disconnect(self, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: dict):
        user_ws = self.get_ws(message["user_id"])
        if user_ws:
            websocket: WebSocket = user_ws
            await websocket.send_json(message)
            return True
        return False

    def get_ws(self, user_id: int):
        return self.active_connections.get(user_id)


profile_manager = ProfileManager()
user_manager = UserManager()
