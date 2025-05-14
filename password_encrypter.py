import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import get_encryption_key, SECRET_KEY, encrypt_password, decrypt_password


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