from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from celery.result import AsyncResult

ws_router = APIRouter()

@ws_router.websocket("/ws/logs/{task_id}")
async def websocket_logs(websocket: WebSocket, task_id: str):
    await websocket.accept()
    try:
        while True:
            state = AsyncResult(task_id).state
            await websocket.send_text(f"Task {task_id} state: {state}")
            if state in ["SUCCESS", "FAILURE", "REVOKED"]:
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Client disconnected from task {task_id}")
