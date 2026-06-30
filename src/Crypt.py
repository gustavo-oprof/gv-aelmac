import os
import hashlib
from cryptography.fernet import Fernet

fernet = Fernet(os.getenv('CRYPTO_KEY').encode())
HASH_SALT = os.getenv('HASH_SALT').encode()

def crypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()

def hash_query(value: str) -> str:
    return hashlib.sha256(HASH_SALT + value.strip().lower().encode()).hexdigest()
