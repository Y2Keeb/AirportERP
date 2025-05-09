import tkinter as tk
from tkinter import messagebox, Menu
import customtkinter as ctk
from CTkMessagebox import *
from basewindow import BaseWindow
from views.admin_screen import AdminScreen
from views.airline_screen import AirlineScreen
from views.flight_planner_screen import FlightPlannerScreen
from views.user_screen import UserScreen
from views.kiosk_screen import KioskLoginScreen
from config import mydb, set_theme
import PIL
from PIL import Image
from PIL import ImageFilter


class LoginScreen(BaseWindow):

    def __init__(self, root,view_manager=None):
        super().__init__(root, " ", menu_buttons=["help", "about","exit"])
        self.root = root
        self.view_manager = view_manager

        self.root.update_idletasks()  # Ensure geometry info is accurate
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        self.original_bg_image = PIL.Image.open("docs/icons/background.jpg").convert("RGBA")

        startup_image = self.original_bg_image.resize((window_width, window_height), PIL.Image.LANCZOS)
        self.bg_ctk_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image,
                                         size=(window_width, window_height))

        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_ctk_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.after(50, lambda: self._fade_in_background(
            self.original_bg_image,
            self.root.winfo_width(),
            self.root.winfo_height()
        ))

        self.root.bind("<Configure>", self._resize_background)
        self.menu_bar.lift()

        self.frame_main = ctk.CTkFrame(
            self.root,
            fg_color="transparent",
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
        self.root.configure(bg="black")  # Makes root black behind the image

        self.create_widgets()


    def _resize_background(self, event):
        if event.width < 100 or event.height < 100:
            return

        if hasattr(self, "_resize_after_id"):
            self.root.after_cancel(self._resize_after_id)

        self._resize_after_id = self.root.after(150, lambda: self._perform_resize(event.width, event.height))

    def _perform_resize(self, width, height):
        resized = self.original_bg_image.resize((width, height), PIL.Image.LANCZOS)
        self.bg_ctk_image = ctk.CTkImage(light_image=resized, dark_image=resized, size=(width, height))
        self.bg_label.configure(image=self.bg_ctk_image)

    def _fade_in_background(self, base_img, width, height, steps=10, delay=30):
        # Black background base
        black_bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        resized_image = base_img.resize((width, height), Image.LANCZOS).convert("RGBA")

        def fade_step(step):
            alpha = int(255 * (step / steps))
            blended = Image.blend(black_bg, resized_image, step / steps)
            self.bg_ctk_image = ctk.CTkImage(light_image=blended, dark_image=blended, size=(width, height))
            self.bg_label.configure(image=self.bg_ctk_image)

            if step < steps:
                self.root.after(delay, lambda: fade_step(step + 1))

        fade_step(0)

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
            elif role == "airline":
                self.root.view_manager.show_view(AirlineScreen,username=username)
            elif role == "kiosk":
                self.root.view_manager.show_view(KioskLoginScreen)
            elif role == "staff":
                self.root.view_manager.show_view(FlightPlannerScreen)
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
