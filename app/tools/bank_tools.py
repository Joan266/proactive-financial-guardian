# app/tools/bank_tools.py
import os
from ..clients.bank_of_anthos_client import BankOfAnthosClient

class BankTool:
    """A tool for interacting with the Bank of Anthos application."""

    def __init__(self):
        """Initializes the tool and the underlying bank client."""
        base_url = os.environ.get("BANK_OF_ANTHOS_URL", "http://localhost:8080")
        self.client = BankOfAnthosClient(base_url=base_url)
        self._is_logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Logs into the bank application.
        Returns True for success, False for failure.
        """
        print(f"Attempting to log in user '{username}' to Bank of Anthos...")
        self._is_logged_in = self.client.login(username, password)
        if not self._is_logged_in:
            print("Bank login failed.")
        return self._is_logged_in

    def get_account_data(self) -> dict | None:
        """
        Retrieves account balance and transactions after a successful login.
        Returns a dictionary with 'balance' and 'transactions' or None on failure.
        """
        if not self._is_logged_in:
            print("Cannot get account data: not logged in.")
            return None
        
        print("Fetching account data from bank...")
        return self.client.get_account_data()