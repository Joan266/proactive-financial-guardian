# app/services/financial_analysis_service.py
import os
import json
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_document_content(credentials_json: str, document_url: str) -> str | None:
    """Usa las credenciales del usuario para leer un Google Doc."""
    try:
        credentials = Credentials.from_authorized_user_info(json.loads(credentials_json))
        
        service = build('docs', 'v1', credentials=credentials)
        
        document_id = document_url.split('/d/')[1].split('/')[0]
        
        document = service.documents().get(documentId=document_id).execute()
        doc_content = document.get('body').get('content')
        
        text = ''
        for element in doc_content:
            if 'paragraph' in element:
                for sub_element in element.get('paragraph').get('elements'):
                    text += sub_element.get('textRun', {}).get('content', '')
        
        print(f"Contenido del Doc extraído con éxito ({len(text)} caracteres).")
        return text
        
    except Exception as e:
        print(f"Error al leer Google Doc: {e}")
        return None
def analyze_goals_with_gemini(document_text: str) -> dict | None:
    """Envía el texto a Gemini y espera un JSON estructurado."""
    
    try:
        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)
    except KeyError:
        print("ERROR: La variable de entorno GOOGLE_API_KEY no está configurada.")
        return None

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    Eres un asistente financiero experto. Analiza el siguiente texto que contiene las metas financieras de un usuario.
    Extrae hasta 3 metas principales y devuélvelas en un formato JSON estricto.
    El JSON debe tener una clave "goals" que contenga una lista de objetos.
    Cada objeto debe tener dos claves: "name" (un nombre corto para la meta, ej: "Viaje a Japón") y "description" (una frase motivadora sobre la meta).
    Si no encuentras metas claras, devuelve un JSON con una lista vacía.

    Texto del usuario:
    ---
    {document_text}
    ---

    JSON:
    """
    try:
        response = model.generate_content(prompt)
        
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        
        print("Respuesta de Gemini recibida y parseada con éxito.")
        return json.loads(cleaned_response)
        
    except Exception as e:
        print(f"Error al analizar con Gemini: {e}")
        return None