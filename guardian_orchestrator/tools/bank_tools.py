# app/tools/bank_tools.py
import os
from ..clients.bank_of_anthos_client import BankOfAnthosClient

class BankTool:
    """A tool for interacting with the Bank of Anthos application."""

    def __init__(self):
        """Initializes the tool and the underlying bank client."""
        self.base_url = os.environ.get("BANK_OF_ANTHOS_URL", "http://34.173.134.229") 
        self.client = BankOfAnthosClient(base_url=self.base_url)
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
        Retrieves account balance and transactions and formats them using MCP.
        """
        if not self._is_logged_in:
            print("Cannot get account data: not logged in.")
            return None
        
        print("Fetching account data from bank...")
        raw_data = self.client.get_account_data()
        
        if not raw_data:
            return None
            
        print("Formatting account data as MCP.")
        return self._to_mcp(raw_data)

    def _to_mcp(self, data: dict) -> dict:
        """Converts raw bank data to the Model Context Protocol format."""
        
        mcp_transactions = []
        for tx in data.get('transactions', []):
            mcp_transactions.append({
                "@type": "FinancialTransaction",
                "description": tx.get("label"),
                "transactionAmount": {
                    "@type": "MonetaryAmount",
                    "value": tx.get("amount"),
                    "currency": "USD" 
                },
                "valueDate": tx.get("date")
            })

        return {
            "@type": "BankAccount",
            "url": self.base_url,
            "balance": {
                "@type": "MonetaryAmount",
                "value": data.get("balance"),
                "currency": "USD"
            },
            "transactions": mcp_transactions
        }