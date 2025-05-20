import mysql.connector
import customtkinter as ctk
import logging
import base64
import os
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pygame
from threading import Thread

def init_sound():
    pygame.mixer.init()

def play_sound(sound_file):
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",
)

LOG_FILENAME = "app.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("PIL").setLevel(logging.WARNING)


def load_sql_patterns(file_path="sql_patterns.txt") -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def is_suspect_sql_input(text: str, patterns: list[str] = None) -> bool:
    if patterns is None:
        patterns = load_sql_patterns()
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

def get_logger(name):
    """
    Return a configured logger for the given name.
    """
    return logging.getLogger(name)


def set_theme():
    """
    Set the global appearance and color theme for the application using customtkinter.
    """
    theme_path = os.path.join(os.path.dirname(__file__), "themes", "marsh.json")
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(theme_path)


SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")


def get_encryption_key():
    """Generate encryption key from SECRET_KEY."""
    salt = b"airporterpsalt1234"
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
        logger.error(f"Encryption error: {str(e)}")
        return None


def decrypt_password(encrypted_password):
    """Decrypt an encrypted password string."""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_password.encode())
        return decrypted_data.decode()
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return None
