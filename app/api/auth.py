# app/api/auth.py
import os
import traceback
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import SessionLocal

# --- Configuration ---
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/documents.readonly",
    "openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"
]

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login/google", tags=["Authentication"])
async def login_google(request: Request):
    print("\n--- [LOGIN START] ---")
    try:
        base_url = os.environ.get("APP_BASE_URL")
        if base_url:
            redirect_uri = f"{base_url}/callback"
            print(f"DEBUG: Using redirect_uri from APP_BASE_URL: {redirect_uri}")
        else:
            redirect_uri = request.url_for("auth_callback")
            print(f"DEBUG: Using redirect_uri from request.url_for: {redirect_uri}")

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline", prompt="consent", include_granted_scopes="true"
        )
        request.session["state"] = state
        print(f"DEBUG: Stored state in session: {state}")
        print("--- [LOGIN] Redirecting user to Google...")
        return RedirectResponse(authorization_url)
    except Exception as e:
        print(f"CRITICAL ERROR in /login/google: {traceback.format_exc()}")
        return HTMLResponse("An error occurred during login.", status_code=500)


@router.get("/callback", name="auth_callback", tags=["Authentication"])
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    print("\n--- [CALLBACK START] ---")
    try:
        state = request.session.get("state")
        if not state:
            print("CRITICAL ERROR: 'state' not found in session upon callback.")
            return HTMLResponse("Session state missing. Please try again.", status_code=400)
        
        print(f"DEBUG: Retrieved state from session: {state}")

        base_url = os.environ.get("APP_BASE_URL", str(request.base_url)).rstrip('/')
        redirect_uri = f"{base_url}/callback"

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=redirect_uri
        )
        authorization_response = str(request.url)
        print(f"DEBUG: Fetching token with response: {authorization_response}")
        flow.fetch_token(authorization_response=authorization_response)
        
        credentials = flow.credentials
        print("DEBUG: Successfully fetched token.")
        
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        user_email = user_info['email']

        db_user = crud.get_user_by_email(db, email=user_email)
        if not db_user:
            user_data = {
                "email": user_email, "bank_username": "testuser",
                "bank_password": "bankofanthos", "google_creds_json": credentials.to_json()
            }
            crud.create_user(db, user_data=user_data)
        
        print("--- [CALLBACK SUCCESS] ---")
        return HTMLResponse(content=f"<h1>Authentication successful for {user_email}!</h1>")
    except Exception as e:
        print(f"CRITICAL ERROR in /callback: {traceback.format_exc()}")
        return HTMLResponse("An error occurred during callback.", status_code=500)