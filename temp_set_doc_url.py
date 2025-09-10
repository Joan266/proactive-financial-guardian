# temp_set_doc_url.py
from app.database import SessionLocal
from app.models import User

USER_EMAIL_TO_UPDATE = "joanalemany26@gmail.com"
GOOGLE_DOC_URL = "https://docs.google.com/document/d/1K8pT3Mc2Kupf2hRnHPc9a-jTLfV6igAL4Us8b9gGe3A/edit?tab=t.0"


db = SessionLocal()

user = db.query(User).filter(User.email == USER_EMAIL_TO_UPDATE).first()

if user:
  
    user.financial_goals_doc_url = GOOGLE_DOC_URL
    db.commit()
    print(f"URL del documento actualizada con éxito para {user.email}")
else:
    print(f"Error: No se encontró al usuario con el email {USER_EMAIL_TO_UPDATE}")

db.close()