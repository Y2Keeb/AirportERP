import tkinter as tk
from tkinter import Menu,messagebox

import PIL
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

from config import mydb, set_theme
from basewindow import BaseWindow
from views.user_screen import UserScreen


class KioskLoginScreen(BaseWindow):
    def __init__(self, root,view_manager=None):
        super().__init__(root, " ", menu_buttons=["help"])
        self.root = root
        self.view_manager = view_manager

        bg_image = PIL.Image.open("docs/icons/background.jpg")
        bg_image = bg_image.resize((800, 550))
        self.bg_ctk_image = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(800, 550))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_ctk_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_main = ctk.CTkFrame(
            self.root,
            border_color="black",
            border_width=7,
            corner_radius=20,
            fg_color="transparent"
        )
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        self.menu_bar.lift()

        self.frame_welcome = ctk.CTkFrame(self.frame_main, border_width=5,border_color="black",fg_color="transparent")
        self.frame_welcome.pack(side="left",fill="both", expand=True)
        self.frame_login= ctk.CTkFrame(self.frame_main, border_width=5,border_color="black",fg_color="transparent")
        self.frame_login.pack(side="right",fill="both", expand=True)

        self.frame_login_content = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        self.frame_login_content.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_welcome_content = ctk.CTkFrame(self.frame_welcome, fg_color="transparent")
        self.frame_welcome_content.place(relx=0.5, rely=0.5, anchor="center")

        pil_image = Image.open("docs/icons/airplane_white.png")
        pil_image = pil_image.resize((150, 150))
        self.ctk_image = ctk.CTkImage(light_image=pil_image,
                                      dark_image=pil_image,
                                      size=(150, 150))

        self.lbl_image = ctk.CTkLabel(self.frame_welcome_content,
                                      image=self.ctk_image,
                                      text="")
        self.lbl_image.pack(pady=20)
        self.entry_username = ctk.CTkEntry(self.frame_login_content)
        self.entry_password = ctk.CTkEntry(self.frame_login_content, show="*")

        set_theme()
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame_welcome_content, text="Welcome!", font=("Comic Sans", 25)).pack()
        ctk.CTkLabel(self.frame_welcome_content, text="Log in to your account or create one.").pack()

        ctk.CTkLabel(self.frame_login_content, text="Username:").pack(pady=5)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_login_content, text="Password:").pack(pady=5)
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_login_content, text="Login", command=self.login)
        btn_login.pack(pady=10)
        lbl_or = ctk.CTkLabel(self.frame_login_content,text="or")
        lbl_or.pack(pady=10)
        btn_register = ctk.CTkButton(self.frame_login_content, text="Register")
        btn_register.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        cursor = mydb.cursor()
        query = "SELECT id, username, first_name, last_name, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            role = result[4]  # Get the role from database

            self.destroy_menu_bar()
            self.frame_main.destroy()

            if role == "user":
                # Pass the role explicitly
                self.root.view_manager.show_view(
                    UserScreen,
                    username=username,
                    user_id=result[0],  # id from database
                    role=role  # Explicitly pass the role
                )
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    def help_menu(self):
        CTkMessagebox(
            title="Info",
            icon="question",
            message="• Login by entering your username and password.\n"
                    "• If you don't have a login, create one or contact your administrator.",
        )

    def cleanup(self):
        self.frame_main.destroy()

    @property
    def view_state(self):
        """Optional state-saving feature for ViewManager"""
        return {
            "username": self.entry_username.get()
        }
