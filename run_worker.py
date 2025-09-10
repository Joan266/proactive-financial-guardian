# run_worker.py
from app.queues import redis_conn, guardian_queue
from rq import SimpleWorker

if __name__ == '__main__':
    if redis_conn and guardian_queue:
        print("Starting RQ SimpleWorker in permanent mode...")
        worker = SimpleWorker([guardian_queue], connection=redis_conn)
        
        # Simplemente llamamos a .work() sin parámetros.
        # El worker se quedará escuchando para siempre.
        worker.work()
        
    else:
        print("Cannot start worker, Redis connection not available.")