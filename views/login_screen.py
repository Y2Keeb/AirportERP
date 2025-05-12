import tkinter as tk
from tkinter import messagebox, Menu
import customtkinter as ctk
from customtkinter import CTkImage

from basewindow import BaseWindow
from views.admin_screen import AdminScreen
from views.airline_screen import AirlineScreen
from views.flight_planner_screen import FlightPlannerScreen
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

    def load_view_content(self):
        """Heavy UI elements and image setup"""
        icon_size = (25,25)

        username_pil = PIL.Image.open("docs/icons/user.png").resize(icon_size)
        self.username_image = ctk.CTkImage(light_image=username_pil, dark_image=username_pil, size=icon_size)
        password_pil = PIL.Image.open("docs/icons/lock.png").resize(icon_size)
        self.password_image = ctk.CTkImage(light_image=password_pil, dark_image=password_pil, size=icon_size)



        self.original_bg_image = PIL.Image.open("docs/icons/background.jpg").convert("RGBA")

        window_width = 1300
        window_height = 900
        startup_image = self.original_bg_image.resize((window_width, window_height), PIL.Image.LANCZOS)

        self.bg_ctk_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image,
                                         size=(window_width, window_height))

        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_ctk_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.after(100, lambda: self._fade_in_background(
            self.original_bg_image,
            self.root.winfo_width(),
            self.root.winfo_height()
        ))

        self.root.bind("<Configure>", self._resize_background)
        self.root.after(200, self.menu_bar.lift)

        self.frame_main = ctk.CTkFrame(
            self.root,
            fg_color="transparent",
            border_color="black",
            border_width=5
        )
        self.frame_main.place(relx=0.5, rely=0.525, anchor="center", relwidth=0.4, relheight=0.9)

        pil_image = Image.open("docs/icons/login_logo.png").resize((250, 207))
        self.ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(250, 207))

        self.lbl_image = ctk.CTkLabel(self.frame_main, image=self.ctk_image, text="")
        self.lbl_image.grid(row=0, column=0, pady=(140, 0))

        self.content_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_main.grid_rowconfigure(1, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        # Username row frame
        self.username_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.username_icon = ctk.CTkLabel(self.username_row, text="", image=self.username_image, fg_color="transparent")
        self.entry_username = ctk.CTkEntry(self.username_row, placeholder_text="Username", width=200)

        # Password row frame
        self.password_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.password_icon = ctk.CTkLabel(self.password_row, text="", image=self.password_image, fg_color="transparent")
        self.entry_password = ctk.CTkEntry(self.password_row, placeholder_text="Password", show="*", width=200)

        self.show_password_btn = ctk.CTkCheckBox(self.content_frame, text=" Show Password",command=self.show_password)

        self.btn_login = ctk.CTkButton(self.content_frame, text="Login", command=self.login)

        set_theme()
        self.create_widgets()
    def show_password(self):
        self.entry_password.configure(show="")
        self.show_password_btn.configure(command=self.hide_password)

    def hide_password(self):
        self.entry_password.configure(show="*")
        self.show_password_btn.configure(command=self.show_password)

    def _resize_background(self, event):
        if event.width < 100 or event.height < 100:
            return

        if hasattr(self, "_resize_after_id"):
            self.root.after_cancel(self._resize_after_id)

        self._resize_after_id = self.root.after(50, lambda: self._perform_resize(event.width, event.height))

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
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)  # entry

        ctk.CTkLabel(
            self.content_frame,
            text="Welcome Back!",
            fg_color="transparent",
            font=("Arial", 22)
        ).grid(row=1, column=0, columnspan=2, pady=(35, 2), sticky="n")

        ctk.CTkLabel(
            self.content_frame,
            text="Log in to your account",
            fg_color="transparent"
        ).grid(row=2, column=0, columnspan=2, pady=(0, 30), sticky="n")

        # Username row
        self.username_row.grid(row=3, column=0, columnspan=2, pady=5)
        self.username_icon.pack(side="left", padx=(0, 10))
        self.entry_username.pack(side="left")

        # Password row
        self.password_row.grid(row=4, column=0, columnspan=2, pady=15)
        self.password_icon.pack(side="left", padx=(0, 10))
        self.entry_password.pack(side="left")

        # Show password checkbox
        self.show_password_btn.grid(row=5, column=0, columnspan=2, pady=15)

        # Login button
        self.btn_login.grid(row=6, column=0, columnspan=2, pady=(20, 10))

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
