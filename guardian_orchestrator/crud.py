# app/crud.py
from sqlalchemy.orm import Session
from .models import User
from . import security 
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    encrypted_password = security.encrypt_data(user_data["bank_password"])
    encrypted_creds = security.encrypt_data(user_data["google_creds_json"])
    
    db_user = User(
        email=user_data["email"],
        bank_username=user_data["bank_username"],
        encrypted_bank_password=encrypted_password, 
        google_creds_json=encrypted_creds  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user