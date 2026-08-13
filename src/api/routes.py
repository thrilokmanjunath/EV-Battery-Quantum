from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
from .auth import get_current_user
from typing import Dict, Any
from ..services.cache_service import cache_response
from ..services.optimization_service import run_optimization_task
from .metrics import optimization_requests_total, optimization_processing_seconds
from src.worker.celery_app import celery_app
import time

router = APIRouter()

class OptimizationRequest(BaseModel):
    parameters: Dict[str, Any]

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/optimize")
@cache_response(ttl=60)
def start_optimization(request: OptimizationRequest, background_tasks: BackgroundTasks):
    start_time = time.time()
    optimization_requests_total.inc()
    task = run_optimization_task.delay(request.parameters)
    process_time = time.time() - start_time
    optimization_processing_seconds.observe(process_time)
    return {"message": "Optimization started", "task_id": task.id}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }
