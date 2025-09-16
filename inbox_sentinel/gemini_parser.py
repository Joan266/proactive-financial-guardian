# inbox_sentinel/gemini_parser.py
import os
import json
import google.generativeai as genai

class GeminiParser:
    """A parser that uses Gemini to extract bill information from email text."""

    def __init__(self):
        """Initializes the parser and configures the Gemini API."""
        try:
            # It's crucial to get the API key from environment variables
            # to avoid hardcoding secrets.
            google_api_key = os.environ["GOOGLE_API_KEY"]
            genai.configure(api_key=google_api_key)
        except KeyError:
            # Fail fast if the key is not configured.
            raise RuntimeError("GOOGLE_API_KEY environment variable not set.")

        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def parse_bill_from_email(self, email_content: str) -> dict | None:
        """
        Analyzes raw email text to extract bill details using a structured prompt.
        Returns a dictionary with the bill information or None if parsing fails.
        """
        prompt = f"""
        You are an expert financial parsing agent. Your task is to analyze the
        following email content and extract three specific pieces of information:
        the merchant's name, the total amount due, and the due date.

        Return the information in a strict JSON format with the following keys:
        "merchant", "amount" (as a float), and "due_date" (in YYYY-MM-DD format).

        If any piece of information is not found, use a value of null for that key.

        Email Content:
        ---
        {email_content}
        ---

        JSON:
        """
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to ensure it's valid JSON. LLMs often wrap
            # JSON in markdown backticks.
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            
            print("Successfully parsed bill data with Gemini.")
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"An error occurred during Gemini parsing: {e}")
            return None