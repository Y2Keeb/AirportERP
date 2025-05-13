import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

def get_encryption_key():
    """Generate encryption key from SECRET_KEY."""
    salt = b'airporterpsalt1234'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(SECRET_KEY.encode()))
    return key

def encrypt_password(password):
    """Encrypt a password string."""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(password.encode())
        return encrypted_data.decode()
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return None

def decrypt_password(encrypted_password):
    """Decrypt an encrypted password string."""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_password.encode())
        return decrypted_data.decode()
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return None

def main():
    print("Password Encryption/Decryption CLI")
    print("1. Encrypt password")
    print("2. Decrypt password")
    choice = input("Choose (1/2): ").strip()
    if choice == "1":
        pw = input("Enter password to encrypt: ")
        enc = encrypt_password(pw)
        print(f"Encrypted: {enc}")
    elif choice == "2":
        enc = input("Enter encrypted password: ")
        dec = decrypt_password(enc)
        print(f"Decrypted: {dec}")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()