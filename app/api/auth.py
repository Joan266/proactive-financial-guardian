# app/api/auth.py
import os 
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import SessionLocal

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# --- Configuration ---
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/documents.readonly",
    "openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"
]

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login/google", tags=["Authentication"])
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_callback")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    request.session["state"] = state
    return RedirectResponse(authorization_url)

@router.get("/callback", name="auth_callback", tags=["Authentication"])
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    state = request.session["state"]
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=request.url_for("auth_callback")
    )
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    user_email = user_info['email']

    db_user = crud.get_user_by_email(db, email=user_email)
    if not db_user:
        user_data = {
            "email": user_email,
            "bank_username": "testuser",
            "bank_password": "bankofanthos",
            "google_creds_json": credentials.to_json()
        }
        crud.create_user(db, user_data=user_data)
        print(f"New user {user_email} created and credentials saved.")
    else:
        print(f"User {user_email} already exists.")
        
    return HTMLResponse(content=f"<h1>Authentication successful for {user_email}!</h1><p>You can close this tab.</p>")