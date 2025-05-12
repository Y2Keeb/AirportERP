import mysql.connector
import customtkinter as ctk
import logging

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
logging.getLogger('PIL').setLevel(logging.WARNING)

def is_suspect_sql_input(text: str) -> bool:
    """
    Detect basic SQL injection patterns in user input.
    Returns True if input contains suspicious SQL patterns.
    """
    suspicious = [
        "' OR", "'--", "';", "DROP TABLE",
        "UNION SELECT", "'='", "1=1",
        "\" OR", "\"--", "EXEC", "INSERT INTO"
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
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("themes/marsh.json")