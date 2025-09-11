# app/models.py
from .database import Base
from sqlalchemy import Column, Integer, String, Text, JSON , LargeBinary

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    bank_username = Column(String)
    encrypted_bank_password = Column(LargeBinary, nullable=True) 
    google_creds_json = Column(LargeBinary, nullable=True) 
   
    financial_goals_doc_url = Column(String, nullable=True)
    financial_goals = Column(JSON, nullable=True) 