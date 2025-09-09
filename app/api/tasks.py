# app/api/tasks.py
from fastapi import APIRouter, HTTPException
from ..queues import guardian_queue
from ..worker import run_payment_prediction

router = APIRouter()

@router.post("/tasks/trigger/payment-prediction/{user_id}", tags=["Tasks"])
async def trigger_payment_prediction(user_id: int):
    """
    Test endpoint to manually trigger the payment prediction task for a user.
    """
    if guardian_queue is None:
        raise HTTPException(status_code=500, detail="Redis connection not available")

    job = guardian_queue.enqueue(run_payment_prediction, user_id)
    
    print(f"Enqueued job {job.id} for user {user_id}")
    
    return {"message": "Task enqueued successfully", "job_id": job.id}