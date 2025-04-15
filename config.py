import mysql.connector
import customtkinter as ctk
import logging

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",
)
LOG_FILENAME = "app.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,  # Log everything (DEBUG, INFO, WARNING, ERROR, CRITICAL) debug is laagste level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger('PIL').setLevel(logging.WARNING)

def get_logger(name):
    return logging.getLogger(name)

def set_theme():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("themes/marsh.json")