from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        print(f"📡 Broadcasting to {len(self.active_connections)} clients: {message}")
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()
