# app/worker.py
import time
from app.database import SessionLocal
from app.models import User
import os
from app.services import financial_analysis_service

def run_payment_prediction(user_id: int):
    """
    Orquesta el análisis financiero para un usuario.
    """
    print(f"--- [Worker] Iniciando análisis para user_id: {user_id} ---")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"Usuario {user_id} no encontrado.")
            return

        if user.financial_goals_doc_url and not user.financial_goals:
            print("Procesando metas financieras...")
            
            content = financial_analysis_service.get_document_content(
                user.google_creds_json, user.financial_goals_doc_url
            )
            
            if content:
                goals = financial_analysis_service.analyze_goals_with_gemini(content)
                if goals:
                    user.financial_goals = goals
                    db.commit()
                    print(f"Metas de Gemini guardadas para el usuario {user.email}")

        time.sleep(2)

    finally:
        db.close()
    
    print(f"--- [Worker] Finalizado análisis para user_id: {user_id} ---")
    return f"Task completed for user {user_id}"