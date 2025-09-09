# app/crud.py
from sqlalchemy.orm import Session
from .models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    db_user = User(
        email=user_data["email"],
        bank_username=user_data["bank_username"],
        encrypted_bank_password=user_data["bank_password"],
        google_creds_json=user_data["google_creds_json"]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user