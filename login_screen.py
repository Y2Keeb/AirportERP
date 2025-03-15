"""
This module provides a login screen for the Airport ERP system.
"""

import tkinter as tk
from tkinter import messagebox, Menu
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",  # works on my machine!
)


def login():
    """
    Authenticates the user by checking the username and password against the database.
    """
    username = entry_username.get()
    password = entry_password.get()

    cursor = mydb.cursor()
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        tk.messagebox.showinfo("Login Success", "Welcome!")
    else:
        tk.messagebox.showerror("Login Failed", "Invalid username or password.")


def about():
    """simple about section that can be selected in the menu"""
    tk.messagebox.showinfo(message="(c) AirportERP\n BY \n Lindsey, Reza And Thomas")


def help():
    """"""
    tk.messagebox.showinfo(
        message="login by entering your username and password\n"
        "if you don't have a login contact your administrator"
    )


root = tk.Tk()
root.title("Login Venster")
root.geometry("300x200")

"""The menubar"""
menubar = Menu(root)
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_)
help_.add_command(label="Tk Help", command=help)
help_.add_separator()
help_.add_command(label="About AirportERP", command=about)


tk.Label(root, text="username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)


btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=20)

root.config(menu=menubar)
root.mainloop()
