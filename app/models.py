# app/models.py
from .database import Base
from sqlalchemy import Column, Integer, String, Text, JSON 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    bank_username = Column(String)
    encrypted_bank_password = Column(String)
    google_creds_json = Column(Text)

    # --- NUEVOS CAMPOS ---
    financial_goals_doc_url = Column(String, nullable=True)
    financial_goals = Column(JSON, nullable=True) # Para el JSON de Gemini