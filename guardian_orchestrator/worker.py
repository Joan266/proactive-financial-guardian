# app/worker.py
from datetime import datetime, timedelta
from guardian_orchestrator.database import SessionLocal
from guardian_orchestrator.models import User
from guardian_orchestrator.tools.google_tools import GoogleApisTool
from guardian_orchestrator.tools.bank_tools import BankTool
from . import security
def run_financial_agent_task(user_id: int):
    """
    The main agent task that orchestrates various tools to perform financial analysis.
    """
    print(f"--- [Agent Worker] Starting task for user_id: {user_id} ---")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"User {user_id} not found.")
            return

        decrypted_creds = security.decrypt_data(user.google_creds_json)
        google_tool = GoogleApisTool(credentials_json=decrypted_creds) 
        
        bank_tool = BankTool()

        if user.financial_goals_doc_url and not user.financial_goals:
            print("Agent Thought: I need to understand the user's financial goals.")
            
            content = google_tool.read_document_content(user.financial_goals_doc_url)
            
            if content:
                goals = google_tool.analyze_text_with_gemini(content)
                if goals:
                    user.financial_goals = goals
                    db.commit()
                    print(f"Agent Action: Saved financial goals for user {user.email}")
        
   
        print("Agent Thought: I will create a reminder for the user.")
        start_time = datetime.now() + timedelta(days=1)
        start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        google_tool.create_calendar_event(
            summary="Financial Guardian Check-in",
            description="This is a test event to confirm the agent is working.",
            start_time=start_time,
            end_time=end_time
        )

    finally:
        db.close()
    
    print(f"--- [Agent Worker] Task finished for user_id: {user_id} ---")
    return f"Agent task completed for user {user_id}"