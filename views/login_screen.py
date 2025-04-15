import tkinter as tk
from tkinter import messagebox, Menu
import customtkinter as ctk
from CTkMessagebox import *
from class_GUI import BaseWindow, AdminScreen, StaffScreen
from views.user_screen import UserScreen
from config import mydb, set_theme
from PIL import Image


class LoginScreen(BaseWindow):
    """Login screen class"""

    def __init__(self, root, **kwargs):
        super().__init__(root, "Login Window")
        self.root = root
        self.root.geometry("800x500")

        self.frame_main = ctk.CTkFrame(self.root, border_color="black", border_width=5)
        self.frame_main.pack(fill="both", expand=True)

        pil_image = Image.open("docs/icons/plane-prop.png")
        pil_image = pil_image.resize((150, 150))
        self.ctk_image = ctk.CTkImage(light_image=pil_image,
                                      dark_image=pil_image,
                                      size=(150, 150))

        self.lbl_image = ctk.CTkLabel(self.frame_main,
                                      image=self.ctk_image,
                                      text="")
        self.lbl_image.pack(pady=20)

        set_theme()
        self.create_widgets()

        self.create_menu()

    def create_widgets(self):
        ctk.CTkLabel(self.frame_main, text="Welcome Back!", font=("Comic Sans", 25)).pack()
        ctk.CTkLabel(self.frame_main, text="Log in to your account").pack()

        ctk.CTkLabel(self.frame_main, text="Username:").pack(pady=5)
        self.entry_username = ctk.CTkEntry(self.frame_main)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_main, text="Password:").pack(pady=5)
        self.entry_password = ctk.CTkEntry(self.frame_main, show="*")
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_main, text="Login", command=self.login)
        btn_login.pack(pady=20)

    def create_menu(self):
        menubar = Menu(self.root, bg="black", fg="white", activebackground="gray", activeforeground="white")
        help_ = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="gray", activeforeground="white")
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

            self.frame_main.destroy()

            if role == "admin":
                self.root.view_manager.show_view(AdminScreen)
            elif role == "staff":
                self.root.view_manager.show_view(StaffScreen)
            else:
                self.root.view_manager.show_view(UserScreen, username=username)
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def about(self):
        CTkMessagebox(
            title="Info", message="(c) AirportERP\nBY Lindsey, Reza and Thomas"
        )

    def help_menu(self):
        CTkMessagebox(
            title="Info",
            icon="question",
            message="• Login by entering your username and password.\n"
                    "• If you don't have a login, contact your administrator.",
        )

    def cleanup(self):
        self.frame_main.destroy()

    @property
    def view_state(self):
        """Optional state-saving feature for ViewManager"""
        return {
            "username": self.entry_username.get()
        }
