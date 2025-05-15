import mysql.connector
import customtkinter as ctk
import logging
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Establish connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",
)

# Configure logging to write detailed logs to app.log
LOG_FILENAME = "app.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,  # Log everything (DEBUG, INFO, WARNING, ERROR, CRITICAL) debug is lowest level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# Suppress PIL's verbose internal logs
logging.getLogger("PIL").setLevel(logging.WARNING)


def is_suspect_sql_input(text: str) -> bool:
    """
    Detect basic SQL injection patterns in user input.
    Returns True if input contains suspicious SQL patterns.
    """
    suspicious = [
        "' OR",
        "'--",
        "';",
        "DROP TABLE",
        "UNION SELECT",
        "'='",
        "1=1",
        '" OR',
        '"--',
        "EXEC",
        "INSERT INTO",
    ]
    return any(keyword in text.upper() for keyword in suspicious)


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
