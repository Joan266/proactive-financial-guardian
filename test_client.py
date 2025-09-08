# test_client.py

from app.clients.bank_of_anthos_client import BankOfAnthosClient
import os
import json

# --- Configuration ---
BASE_URL = os.environ.get("BANK_OF_ANTHOS_URL", "http://34.173.134.229")
TEST_USERNAME = os.environ.get("BANK_USER", "testuser")
TEST_PASSWORD = os.environ.get("BANK_PASSWORD", "bankofanthos")

if __name__ == "__main__":
    print("--- Running BankOfAnthosClient Full Test ---")

    client = BankOfAnthosClient(base_url=BASE_URL)
    login_success = client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    if not login_success:
        print("❌ Test FAILED: Could not log in. Halting test.")
    else:
        print("\n--- Fetching Data ---")
        response = client.session.get(f"{client.base_url}/home")

        if response and response.status_code == 200:
            with open("home.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ Saved the received HTML to home.html for debugging.")

            account_data = client.get_account_data()

            print("\n--- Test Result ---")
            if account_data:
                print("✅ Test PASSED: Successfully fetched account data.")
                print("\nBalance:")
                if account_data['balance'] is not None:
                    print(f"  ${account_data['balance']:.2f}")
                else:
                    print("  ERROR: Balance could not be parsed.")

                print("\nTransactions:")
                print(json.dumps(account_data['transactions'], indent=2))
        else:
            print("❌ Test FAILED: Could not retrieve account data after login.")