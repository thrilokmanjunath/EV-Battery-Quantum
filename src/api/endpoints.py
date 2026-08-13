import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

from src.worker.celery_app import celery_app
from src.middleware.log_sanitizer import LogSanitizer
from .auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError, ExpiredSignatureError

router = APIRouter()

async def get_user_from_query(token: str = Query(None)):
    if not token:
        return {"username": "demo_user"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/api/quantum/stream/{task_id}")
async def stream_telemetry(task_id: str, user: dict = Depends(get_user_from_query)):
    """
    Secure Server-Sent Events (SSE) endpoint to stream sanitized telemetry.
    Requires a valid JWT token in the query string.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        # Send an initial connection event
        event = LogSanitizer.sanitize("Secure SSE connection established.", level="INFO", module="SYSTEM")
        yield f"data: {event.to_json()}\n\n"

        task = celery_app.AsyncResult(task_id)
        last_meta_message = None
        
        while not task.ready():
            if task.state == 'PROGRESS':
                meta = task.info
                if isinstance(meta, dict):
                    msg = meta.get('message', 'Processing...')
                    if msg != last_meta_message:
                        last_meta_message = msg
                        event = LogSanitizer.sanitize(msg)
                        yield f"data: {event.to_json()}\n\n"
                        
            await asyncio.sleep(1)
            
        # Final state
        if task.state == 'SUCCESS':
            event = LogSanitizer.sanitize("QAOA optimization completed successfully.", level="SUCCESS")
            yield f"data: {event.to_json()}\n\n"
        elif task.state == 'FAILURE':
            error_info = str(task.info) if task.info else "Unknown error"
            event = LogSanitizer.sanitize(f"Optimization failed: {error_info}", level="ERROR")
            yield f"data: {event.to_json()}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")
