# app/clients/bank_of_anthos_client.py

import requests
from bs4 import BeautifulSoup
import re

class BankOfAnthosClient:
    """
    A client for interacting with the Bank of Anthos web application.
    Handles authentication, session management, and data scraping.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password) -> bool:
        login_url = f"{self.base_url}/login"
        payload = {"username": username, "password": password}
        print(f"Attempting to log in user '{username}' at {login_url}...")
        try:
            response = self.session.post(login_url, data=payload, allow_redirects=False)
            response.raise_for_status()
            if response.status_code == 302:
                print("Login successful! Session cookie stored.")
                return True
            else:
                print(f"Login failed. Received status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during login: {e}")
            return False

    def get_account_data(self) -> dict | None:
        home_url = f"{self.base_url}/home"
        print("Fetching account data from /home...")
        try:
            response = self.session.get(home_url)
            response.raise_for_status()
            if response.status_code == 200:
                print("Successfully fetched account page.")
                soup = BeautifulSoup(response.text, "html.parser")
                balance = self._parse_balance(soup)
                transactions = self._parse_transactions(soup)
                return {"balance": balance, "transactions": transactions}
            else:
                print(f"Failed to fetch account page. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching account data: {e}")
            return None

    def _parse_balance(self, soup: BeautifulSoup) -> float | None:
        balance_tag = soup.find('span', id='current-balance')
        if not balance_tag:
            print("DEBUG: Could not find balance tag with id='current-balance'")
            return None
        
        balance_text = balance_tag.get_text(strip=True)
        print(f"DEBUG: Found balance text: '{balance_text}'")
        
        cleaned_text = re.sub(r'[^\d.-]', '', balance_text)
        if not cleaned_text:
            print(f"DEBUG: Balance text was empty after cleaning.")
            return None
            
        try:
            return float(cleaned_text)
        except ValueError:
            print(f"DEBUG: Could not convert cleaned balance text '{cleaned_text}' to a float.")
            return None

    def _parse_transactions(self, soup: BeautifulSoup) -> list:
        transactions = []
        transaction_list_tbody = soup.find('tbody', id='transaction-list')
        if not transaction_list_tbody:
            print("DEBUG: Could not find transaction table with id='transaction-list'")
            return []

        for row in transaction_list_tbody.find_all('tr'):
            date_tag = row.find('td', class_='transaction-date')
            label_tag = row.find('td', class_='transaction-label')
            amount_tag = row.find('td', class_='transaction-amount')

            if date_tag and label_tag and amount_tag:
                date = date_tag.get_text(strip=True)
                label = label_tag.get_text(strip=True)
                amount_text = amount_tag.get_text(strip=True)
                cleaned_amount_text = re.sub(r'[^\d.-]', '', amount_text)
                try:
                    amount = float(cleaned_amount_text)
                    transactions.append({"date": date, "label": label, "amount": amount})
                except (ValueError, TypeError):
                    continue
        
        print(f"Parsed {len(transactions)} transactions.")
        return transactions