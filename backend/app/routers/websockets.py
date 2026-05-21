"""
app/routers/websockets.py
Real-time WebSocket handlers:
  - /ws/meeting/{meeting_id}  →  WebRTC signaling (offer/answer/ICE)
  - /ws/chat/{channel_id}     →  Live team chat broadcast
"""
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["websockets"])


class RoomManager:
    """Thread-safe (asyncio-safe) connection pool keyed by room string."""

    def __init__(self):
        self._rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room: str, ws: WebSocket) -> None:
        await ws.accept()
        self._rooms[room].append(ws)
        logger.info("WS connect  room=%s  total=%d", room, len(self._rooms[room]))

    def disconnect(self, room: str, ws: WebSocket) -> None:
        self._rooms[room].remove(ws)
        if not self._rooms[room]:
            del self._rooms[room]
        logger.info("WS disconnect room=%s", room)

    async def broadcast(self, room: str, payload: dict, exclude: WebSocket | None = None) -> None:
        dead: list[WebSocket] = []
        for ws in self._rooms.get(room, []):
            if ws is exclude:
                continue
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._rooms[room].remove(ws)

    def room_size(self, room: str) -> int:
        return len(self._rooms.get(room, []))


manager = RoomManager()


# ── WebRTC Signaling ──────────────────────────────────────────────
@router.websocket("/ws/meeting/{meeting_id}")
async def meeting_signaling(meeting_id: str, ws: WebSocket):
    """
    WebRTC signaling room.

    Clients send JSON:
      { "type": "offer"|"answer"|"ice_candidate", "data": {...}, "from": "peer_id" }

    Server broadcasts the message to all OTHER peers in the room.
    On connect / disconnect, a presence event is broadcast:
      { "type": "peer_joined"|"peer_left", "count": <int> }
    """
    room = f"meeting:{meeting_id}"
    await manager.connect(room, ws)
    await manager.broadcast(room, {"type": "peer_joined", "count": manager.room_size(room)}, exclude=ws)

    try:
        while True:
            data = await ws.receive_json()
            # Relay signal data to all other peers
            await manager.broadcast(room, data, exclude=ws)
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
        await manager.broadcast(room, {"type": "peer_left", "count": manager.room_size(room)})
    except Exception as exc:
        logger.error("WS error in room %s: %s", room, exc)
        manager.disconnect(room, ws)


# ── Real-time Chat ────────────────────────────────────────────────
@router.websocket("/ws/chat/{channel_id}")
async def chat_broadcast(channel_id: int, ws: WebSocket):
    """
    Live team chat.

    Clients send JSON:
      { "sender": "Alex Thompson", "content": "Hello!", "type": "text" }

    Server stamps it with a timestamp and broadcasts to ALL connections
    in the channel room (including sender — so the UI can confirm delivery).
    """
    room = f"chat:{channel_id}"
    await manager.connect(room, ws)

    try:
        while True:
            data = await ws.receive_json()
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
            data.setdefault("type", "text")
            await manager.broadcast(room, data)
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
    except Exception as exc:
        logger.error("Chat WS error channel=%d: %s", channel_id, exc)
        manager.disconnect(room, ws)
