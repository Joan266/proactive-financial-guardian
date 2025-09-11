# app/security.py
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

try:
    ENCRYPTION_KEY = os.environ["ENCRYPTION_KEY"]
    if not ENCRYPTION_KEY:
        raise KeyError
except KeyError:
    raise RuntimeError("ENCRYPTION_KEY is not set in the environment variables or .env file.")

_cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> bytes:
    """Encrypts a string and returns bytes."""
    return _cipher_suite.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypts bytes and returns a string."""
    return _cipher_suite.decrypt(encrypted_data).decode('utf-8')