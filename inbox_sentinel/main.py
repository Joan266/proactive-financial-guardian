# inbox_sentinel/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# This is a common pattern to allow the main application to import modules
# from a directory above it, which is necessary to access the orchestrator's
# models and database session for retrieving user credentials.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .gmail_client import GmailClient
from .gemini_parser import GeminiParser
from guardian_orchestrator.database import SessionLocal
from guardian_orchestrator.models import User
from guardian_orchestrator.security import decrypt_data

# Initialize our FastAPI app and the tools for the agent
app = FastAPI(title="Inbox Sentinel Agent API")
gemini_parser = GeminiParser()

class AnalysisRequest(BaseModel):
    user_id: int

@app.post("/analyze-inbox")
async def analyze_inbox(request: AnalysisRequest):
    """
    Endpoint to trigger the analysis of a user's inbox for the latest bill.
    """
    db = SessionLocal()
    try:
        # Step 1: Retrieve the user and their encrypted credentials from the database.
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user or not user.google_creds_json:
            raise HTTPException(status_code=404, detail="User or credentials not found.")

        print(f"Inbox Sentinel: Starting analysis for user_id {request.user_id}.")
        decrypted_creds = decrypt_data(user.google_creds_json)

        # Step 2: Initialize the GmailClient with the user's credentials.
        gmail_client = GmailClient(credentials_json=decrypted_creds)

        # Step 3: Search for emails with common bill-related keywords.
        search_query = "subject:(bill OR invoice OR due OR receipt)"
        messages = gmail_client.search_emails(query=search_query, max_results=1)

        if not messages:
            print("Inbox Sentinel: No recent bill emails found.")
            return {"message": "No new bills found."}

        # Step 4: Get the content of the most recent email.
        latest_message_id = messages[0]['id']
        email_content = gmail_client.get_email_content(latest_message_id)

        if not email_content:
            print("Inbox Sentinel: Could not retrieve readable content from the latest email.")
            return {"message": "Could not retrieve readable content from the latest email."}
        bill_data = gemini_parser.parse_bill_from_email(email_content)

        if not bill_data:
            raise HTTPException(status_code=500, detail="Failed to parse bill data.")

        print("Inbox Sentinel: Analysis complete. Returning bill data.")
        return bill_data

    finally:
        db.close()

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"}