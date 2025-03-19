"""
This module provides a login screen for the Airport ERP system.
This file is deprecate replaced by main.py this will be deleted later
"""

import tkinter as tk
from tkinter import messagebox, Menu
from main import MainWindow
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airport",
)


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Venster")
        self.root.geometry("400x500")
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        image = tk.PhotoImage(file="docs/icons/plane-prop.png")
        tk.Label(self.root, image=image).pack()
        self.root.image = image

        tk.Label(self.root, text="Welcome Back!", font=("Comics-sans", 25)).pack()
        tk.Label(self.root, text="Log in to your account").pack()

        tk.Label(self.root, text="username:").pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)

        tk.Label(self.root, text="password:").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*",)
        self.entry_password.pack(pady=5)

        btn_login = tk.Button(self.root, text="Login", command=self.login) 
        btn_login.pack(pady=20)

    def create_menu(self):
        menubar = Menu(self.root)
        help_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        self.root.config(menu=menubar)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = mydb.cursor()
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            tk.messagebox.showinfo("Login Success", "Welcome!")
            self.root.destroy()
            root.mainloop()

        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def about(self):
        tk.messagebox.showinfo(
            message="(c) AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        tk.messagebox.showinfo(
            message="login by entering your username and password\n"
            "if you don't have a login contact your administrator"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.bind('<Return>', lambda event: app.login())
    root.mainloop()
