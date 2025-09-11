# app/worker.py
import time
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import User
import os
from app.services import financial_analysis_service
from app.services import google_calendar_service

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
        print("Intentando crear un evento de calendario de prueba...")
        
        start_time = datetime.now() + timedelta(days=1)
        start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        google_calendar_service.create_calendar_event(
            credentials_json=user.google_creds_json,
            summary="Prueba de Guardián Financiero",
            description="Si ves esto, ¡la integración con Google Calendar funciona!",
            start_time=start_time,
            end_time=end_time
        )
        time.sleep(2)

    finally:
        db.close()
    
    print(f"--- [Worker] Finalizado análisis para user_id: {user_id} ---")
    return f"Task completed for user {user_id}"