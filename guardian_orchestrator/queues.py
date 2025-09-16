# app/queues.py
import os
import redis
from rq import Queue

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379

try:
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    redis_conn.ping()
    print("Successfully connected to Redis.")
    
    guardian_queue = Queue("guardian_tasks", connection=redis_conn)

except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    redis_conn = None
    guardian_queue = None