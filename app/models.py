# app/models.py
from sqlalchemy import Column, Integer, String, Text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    bank_username = Column(String)
    encrypted_bank_password = Column(String) # Placeholder for now
    google_creds_json = Column(Text)