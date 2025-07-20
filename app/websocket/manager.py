"""WebSocket connection manager."""

import uuid
from typing import Dict, Set
from fastapi import WebSocket
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and messaging."""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_ids: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """Accept a WebSocket connection and assign it an ID."""
        await websocket.accept()

        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        self.connection_ids[websocket] = connection_id

        logger.info(f"WebSocket connection established: {connection_id}")
        return connection_id

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket connection."""
        connection_id = self.connection_ids.get(websocket)
        if connection_id:
            self.active_connections.pop(connection_id, None)
            self.connection_ids.pop(websocket, None)
            logger.info(f"WebSocket connection closed: {connection_id}")

    async def send_message(self, websocket: WebSocket, message: str) -> None:
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            connection_id = self.connection_ids.get(websocket, "unknown")
            logger.error(f"Error sending message to {connection_id}: {e}")
            raise

    async def broadcast(self, message: str) -> None:
        """Broadcast a message to all active connections."""
        disconnected = []

        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(websocket)

        # Clean up disconnected connections
        for websocket in disconnected:
            self.disconnect(websocket)

    def get_connection_count(self) -> int:
        """Get the number of active connections."""
        return len(self.active_connections)

    def get_connection_id(self, websocket: WebSocket) -> str:
        """Get the ID of a WebSocket connection."""
        return self.connection_ids.get(websocket, "unknown")

# Global connection manager instance
connection_manager = ConnectionManager()
