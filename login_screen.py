"""
This module provides a login screen for the Airport ERP system.
"""

import tkinter as tk
from tkinter import Menu
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from class_GUI import BaseWindow, UserScreen, AdminScreen, StaffScreen
from config import mydb


class LoginScreen(BaseWindow):
    """Login screen class"""

    def __init__(self, root):
        super().__init__(root, "Login Window")
        self.root.geometry("300x500")
        self.create_widgets()

    def create_widgets(self):
        image = tk.PhotoImage(file="docs/icons/plane-prop.png")
        tk.Label(self.root, image=image).pack()
        self.root.image = image

        ctk.CTkLabel(self.root, text="Welcome Back!", font=("Comics-sans", 25)).pack()
        ctk.CTkLabel(self.root, text="Log in to your account").pack()

        ctk.CTkLabel(self.root, text="username:").pack(pady=5)
        self.entry_username = ctk.CTkEntry(self.root)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.root, text="password:").pack(pady=5)
        self.entry_password = ctk.CTkEntry(
            self.root,
            show="*",
        )
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.root, text="Login", command=self.login)
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
        query = "SELECT id, username, first_name, last_name, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            role = result[4]
            CTkMessagebox(
                message=f"Login Successful! Welcome, {username}!",
                icon="check",
                option_1="Thanks",
            )
            
            self.new_root = tk.Tk()
            if role == "admin":
                AdminScreen(self.new_root)
            elif role == "staff":
                StaffScreen(self.new_root)
            else:
                UserScreen(self.new_root, username)

        else:
            CTkMessagebox(
                title="Error", message="Invalid username or password.", icon="cancel"
            )

    def about(self):
        CTkMessagebox(
            title="Info", message="(c) AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        CTkMessagebox(
            title="Info",
            icon="question",
            message="login by entering your username and password\n"
            "if you don't have a login contact your administrator",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.bind("<Return>", lambda event: app.login())
    root.mainloop()
