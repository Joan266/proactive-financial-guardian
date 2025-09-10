# app/worker.py
import time


def run_payment_prediction(user_id: int):
    """
    The main background task to analyze a user's financial data.
    """
    print(f"--- [Worker] Starting payment prediction for user_id: {user_id} ---")
    
    # TODO: This is where we will add the full logic in our next step.
    # 1. Load user from PostgreSQL.
    # 2. Log in to Bank of Anthos.
    # 3. Find recurring payments.
    # 4. Create Google Calendar event.
    time.sleep(5)
    
    print(f"--- [Worker] Finished payment prediction for user_id: {user_id} ---")
    return f"Task completed for user {user_id}"
