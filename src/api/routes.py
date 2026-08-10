from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
from .auth import get_current_user
from typing import Dict, Any
from ..services.cache_service import cache_response
from ..services.optimization_service import run_optimization_task
from .metrics import optimization_requests_total, optimization_processing_seconds
import time

router = APIRouter()

class OptimizationRequest(BaseModel):
    parameters: Dict[str, Any]

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/optimize")
@cache_response(ttl=60)
def start_optimization(request: OptimizationRequest, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    start_time = time.time()
    optimization_requests_total.inc()
    task = run_optimization_task.delay(request.parameters)
    process_time = time.time() - start_time
    optimization_processing_seconds.observe(process_time)
    return {"message": "Optimization started", "task_id": task.id}

@router.get("/status/{run_id}")
@cache_response(ttl=60)
async def get_status(run_id: int):
    # This endpoint will check the status of the optimization run from the DB
    return {"run_id": run_id, "status": "unknown"}
