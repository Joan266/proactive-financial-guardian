# inbox_sentinel/gmail_client.py
import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GmailClient:
    """A client for interacting with the Gmail API."""

    def __init__(self, credentials_json: str):
        """Initializes the client with the user's credentials."""
        self.credentials = Credentials.from_authorized_user_info(json.loads(credentials_json))
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def search_emails(self, query: str, max_results: int = 1) -> list:
        """Searches for emails matching the given query."""
        try:
            result = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results
            ).execute()
            messages = result.get('messages', [])
            print(f"Found {len(messages)} email(s) for query: '{query}'")
            return messages
        except Exception as e:
            print(f"An error occurred while searching emails: {e}")
            return []

# inbox_sentinel/gmail_client.py

    def get_email_content(self, message_id: str) -> str | None:
        """
        Retrieves the text content of a specific email, preferring plain text
        but falling back to HTML if necessary.
        """
        try:
            message = self.service.users().messages().get(userId='me', id=message_id).execute()
            payload = message.get('payload', {})
            parts = payload.get('parts', [])
            
            text_content = None

            if not parts: # Handle non-multipart emails
                body_data = payload.get('body', {}).get('data')
                if body_data:
                    text_content = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    # If it's HTML, strip the tags
                    if 'text/html' in payload.get('mimeType', ''):
                        import re
                        text_content = re.sub('<[^<]+?>', '', text_content)

            else: # Handle multipart emails
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            text_content = base64.urlsafe_b64decode(data).decode('utf-8')
                            break 
                
                # If no plain text was found, search for an HTML part as a fallback
                if not text_content:
                    for part in parts:
                        if part['mimeType'] == 'text/html':
                            data = part['body'].get('data')
                            if data:
                                html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                                # Use regex to strip HTML tags
                                import re
                                text_content = re.sub('<[^<]+?>', '', html_content).strip()
                                break

            if text_content:
                print(f"Successfully extracted text content from message {message_id}.")
                return text_content
            
            print(f"Warning: Could not find any usable text part in message {message_id}.")
            return None
        except Exception as e:
            print(f"An error occurred while getting email content: {e}")
            return None