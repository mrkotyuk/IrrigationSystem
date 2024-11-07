import asyncio
from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.agent import Agent
from models.watering import Watering

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, unique_identifier: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[unique_identifier] = websocket
        print(f"New agent connected: {unique_identifier}")

    def disconnect(self, unique_identifier: str):
        if unique_identifier in self.active_connections:
            del self.active_connections[unique_identifier]
            print(f"Agent disconnected: {unique_identifier}")

    async def send_message(self, unique_identifier: str, message: str):
        websocket = self.active_connections.get(unique_identifier)
        if websocket:
            try:
                await websocket.send_text(message)
                print(f"Send to {unique_identifier}: {message}")
            except Exception as e:
                print(f"Failed to send message to {unique_identifier}: {e}")
        else:
            print(f"Agent {unique_identifier} not connected.")


manager = ConnectionManager()


async def send_scheduled_message(
    unique_identifier: str,
    message: str,
    delay: float,
    watering_id: int,
):
    await asyncio.sleep(delay)
    await manager.send_message(unique_identifier, message)
    db = next(get_db())
    watering = db.query(Watering).filter(Watering.id == watering_id).first()
    db.delete(watering)
    db.commit()


@router.websocket("/ws/{unique_identifier}")
async def websocket_endpoint(
    websocket: WebSocket,
    unique_identifier: str,
    db: Session = Depends(get_db),
):
    agent = (
        db.query(Agent).filter(Agent.unigue_identificator == unique_identifier).first()
    )
    if not agent:
        await websocket.accept()
        await websocket.send_text("Not Authorized")
        await websocket.close()
        print(f"Unauthorized connection attempt: {unique_identifier}")
        return
    await manager.connect(unique_identifier, websocket)
    await websocket.send_text("Authorised")
    agent.is_online = True
    db.commit()
    db.refresh(agent)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(unique_identifier)
        agent.is_online = False
        db.commit()
        db.refresh(agent)
    except Exception as e:
        print(f"Error connecting to {unique_identifier}: {e}")
        manager.disconnect(unique_identifier)
