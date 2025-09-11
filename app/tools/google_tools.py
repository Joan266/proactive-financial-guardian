# app/tools/google_tools.py
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.generativeai as genai
import os

class GoogleApisTool:
    """A tool for interacting with various Google APIs."""

    def __init__(self, credentials_json: str):
        """Initializes the tool with the user's credentials."""
        self.credentials = Credentials.from_authorized_user_info(json.loads(credentials_json))

    def read_document_content(self, document_url: str) -> str | None:
        """Reads the text content of a Google Doc."""
        try:
            service = build('docs', 'v1', credentials=self.credentials)
            document_id = document_url.split('/d/')[1].split('/')[0]
            document = service.documents().get(documentId=document_id).execute()
            content = document.get('body').get('content')
            
            text = ''
            for element in content:
                if 'paragraph' in element:
                    for sub_element in element.get('paragraph').get('elements'):
                        text += sub_element.get('textRun', {}).get('content', '')
            
            print(f"Successfully extracted Doc content ({len(text)} characters).")
            return text
        except Exception as e:
            print(f"Error reading Google Doc: {e}")
            return None

    def analyze_text_with_gemini(self, document_text: str) -> dict | None:
        """Analyzes text with Gemini to extract financial goals."""
        try:
            GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
            genai.configure(api_key=GOOGLE_API_KEY)
        except KeyError:
            print("ERROR: GOOGLE_API_KEY environment variable is not set.")
            return None

        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        You are an expert financial assistant. Analyze the following text containing a user's financial goals.
        Extract up to 3 main goals and return them in a strict JSON format with a "goals" key containing a list of objects.
        Each object must have a "name" and a "description".

        Text:
        ---
        {document_text}
        ---

        JSON:
        """
        try:
            response = model.generate_content(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            print("Successfully received and parsed Gemini response.")
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"Error analyzing with Gemini: {e}")
            return None

    def create_calendar_event(self, summary: str, description: str, start_time: datetime, end_time: datetime) -> bool:
        """Creates an event in the user's Google Calendar."""
        try:
            service = build('calendar', 'v3', credentials=self.credentials)
            event = {
                'summary': summary,
                'description': description,
                'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Madrid'},
                'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Madrid'},
            }
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Successfully created event: {created_event.get('htmlLink')}")
            return True
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return False