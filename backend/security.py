import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

KEY = os.getenv("ENCRYPTION_KEY")

if not KEY:
    raise Exception("No key called ENCRYPTION KEY inside of .env file" )

fernet = Fernet(KEY.encode())

def encrypt_data(txt2encrypt: str) -> str:

    encrypted_bytes = fernet.encrypt(txt2encrypt.encode())

    return encrypted_bytes.decode()

def decrypt_data(txt2decrypt: str) -> str:
    decrypted_bytes = fernet.decrypt(txt2decrypt)

    return decrypted_bytes.decode()