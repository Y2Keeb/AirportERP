import mysql.connector
import customtkinter as ctk

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",
)
def set_theme():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("themes/marsh.json")