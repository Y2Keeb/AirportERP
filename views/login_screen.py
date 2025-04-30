import tkinter as tk
from tkinter import messagebox, Menu
import customtkinter as ctk
from CTkMessagebox import *
from basewindow import BaseWindow
from views.admin_screen import AdminScreen
from views.staff_screen import StaffScreen
from views.user_screen import UserScreen
from views.kiosk_screen import KioskLoginScreen
from config import mydb, set_theme
import PIL
from PIL import Image


class LoginScreen(BaseWindow):

    def __init__(self, root,view_manager=None):
        super().__init__(root, " ", menu_buttons=["help", "about","exit"])
        self.root = root
        self.view_manager = view_manager

        bg_image = PIL.Image.open("docs/icons/background.jpg")
        bg_image = bg_image.resize((800, 550))
        self.bg_ctk_image = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(800, 550))

        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_ctk_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.menu_bar.lift()

        self.frame_main = ctk.CTkFrame(
            self.root,
            border_color="black",
            border_width=5
        )
        self.frame_main.place(relx=0.5, rely=0.525, anchor="center", relwidth=0.4, relheight=0.9)

        pil_image = Image.open("docs/icons/login_logo.png")
        pil_image = pil_image.resize((120, 120))
        self.ctk_image = ctk.CTkImage(light_image=pil_image,
                                      dark_image=pil_image,
                                      size=(120, 120))

        self.lbl_image = ctk.CTkLabel(self.frame_main,
                                      image=self.ctk_image,
                                      text="")
        self.lbl_image.pack(pady=35)
        self.entry_username = ctk.CTkEntry(self.frame_main)
        self.entry_password = ctk.CTkEntry(self.frame_main, show="*")

        set_theme()
        self.create_widgets()


    def create_widgets(self):
        ctk.CTkLabel(
            self.frame_main,
            text="Welcome Back!",
            fg_color="transparent",
            font=("Arial", 22)
        ).pack()
        ctk.CTkLabel(self.frame_main, text="Log in to your account",fg_color="transparent").pack()

        ctk.CTkLabel(self.frame_main, text="Username:").pack(pady=5)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_main, text="Password:").pack(pady=5)
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_main, text="Login", command=self.login)
        btn_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        cursor = mydb.cursor()
        query = "SELECT id, username, first_name, last_name, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            role = result[4]

            self.destroy_menu_bar()
            self.frame_main.destroy()

            if role == "admin":
                self.root.view_manager.show_view(AdminScreen)
            elif role == "staff":
                self.root.view_manager.show_view(StaffScreen)
            elif role == "kiosk":
                self.root.view_manager.show_view(KioskLoginScreen)
            else:
                self.root.view_manager.show_view(UserScreen, username=username)
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def cleanup(self):
        self.frame_main.destroy()

    @property
    def view_state(self):
        """Optional state-saving feature for ViewManager"""
        return {
            "username": self.entry_username.get()
        }
