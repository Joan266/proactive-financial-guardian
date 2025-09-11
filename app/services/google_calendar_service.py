# app/services/google_calendar_service.py
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_calendar_event(credentials_json: str, summary: str, description: str, start_time: datetime, end_time: datetime):
    """
    Crea un nuevo evento en el Google Calendar principal del usuario.

    Args:
        credentials_json: Las credenciales del usuario en formato JSON string.
        summary: El título del evento.
        description: La descripción del evento.
        start_time: El objeto datetime de cuándo empieza el evento.
        end_time: El objeto datetime de cuándo termina el evento.
    """
    try:
        credentials = Credentials.from_authorized_user_info(json.loads(credentials_json))
        
        service = build('calendar', 'v3', credentials=credentials)
        
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Europe/Madrid', 
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Europe/Madrid',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Evento creado con éxito: {created_event.get('htmlLink')}")
        return True

    except Exception as e:
        print(f"Error al crear el evento de calendario: {e}")
        return False