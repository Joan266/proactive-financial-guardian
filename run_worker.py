# run_worker.py
from app.queues import redis_conn, guardian_queue
from rq import Worker

if __name__ == '__main__':
    if redis_conn and guardian_queue:
        print("Starting RQ worker in BURST mode (for Windows compatibility)...")
        worker = Worker([guardian_queue], connection=redis_conn)
        
        worker.work(burst=True)
        
        print("Worker finished job and is shutting down.")
    else:
        print("Cannot start worker, Redis connection not available.")