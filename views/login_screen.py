import tkinter as tk
from tkinter import messagebox
import PIL
from PIL import Image
import customtkinter as ctk

from basewindow import BaseWindow
from config import is_suspect_sql_input, mydb, set_theme
from ui_helpers import show_sql_meme_popup
from views.admin_screen import AdminScreen
from views.airline_screen import AirlineScreen
from views.flight_planner_screen import FlightPlannerScreen
from views.kiosk_screen import KioskLoginScreen
from views.user_screen import UserScreen
from config import  encrypt_password

class LoginScreen(BaseWindow):
    def __init__(self, root,view_manager=None):
        super().__init__(root, " ", menu_buttons=["help", "about","exit"])
        """
         Initialize the LoginScreen window and declare all instance variables.
        """
        self.root = root
        self.view_manager = view_manager

        # The instance variables are already declared as None here in __init__, so the program knows they exist already.
        # They are fully initialized later in a separate method (load_view_content),
        # this is to avoid slowing down the startup process.
        self.username_image = None
        self.password_image = None
        self.original_bg_image = None
        self.login_logo_image = None
        self.bg_image = None
        self.bg_label = None
        self.frame_main = None
        self.lbl_logo = None
        self.frame_content = None
        self.frame_username_row = None
        self.lbl_username_icon = None
        self.entry_username = None
        self.frame_password_row = None
        self.lbl_password_icon = None
        self.entry_password = None
        self.checkbox_show_password = None
        self.btn_login = None

    def load_view_content(self):
        """
        Load and build the entire login screen interface:
        - Loads images and icons
        - Sets up background with fade-in animation
        - Builds login panel with username/password inputs
        - Applies visual theme
        """
        icon_size = (25,25)

        username_pil = PIL.Image.open("docs/icons/user.png").resize(icon_size)
        self.username_image = ctk.CTkImage(light_image=username_pil, dark_image=username_pil, size=icon_size)
        password_pil = PIL.Image.open("docs/icons/lock.png").resize(icon_size)
        self.password_image = ctk.CTkImage(light_image=password_pil, dark_image=password_pil, size=icon_size)

        self.original_bg_image = PIL.Image.open("docs/icons/background.jpg").convert("RGBA")

        startup_image = self.original_bg_image.resize((1600, 950), Image.NEAREST)

        self.bg_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image,size=(1600, 950))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.fade_in_background(self.original_bg_image, 1600, 950)

        self.root.after(150, self.menu_bar.lift)

        self.frame_main = ctk.CTkFrame(self.root,fg_color="transparent",border_color="black",border_width=5)
        self.frame_main.place(relx=0.5, rely=0.525, anchor="center", relwidth=0.4, relheight=0.9)

        pil_image = Image.open("docs/icons/login_logo.png").resize((250, 207))
        self.login_logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(250, 207))

        self.lbl_logo = ctk.CTkLabel(self.frame_main, image=self.login_logo_image, text="")
        self.lbl_logo.grid(row=0, column=0, pady=(140, 0))

        self.frame_content = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.frame_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_main.grid_rowconfigure(1, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        self.frame_username_row = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        self.lbl_username_icon = ctk.CTkLabel(self.frame_username_row, text="", image=self.username_image, fg_color="transparent")
        self.entry_username = ctk.CTkEntry(self.frame_username_row, placeholder_text="Username", width=200)

        self.frame_password_row = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        self.lbl_password_icon = ctk.CTkLabel(self.frame_password_row, text="", image=self.password_image, fg_color="transparent")
        self.entry_password = ctk.CTkEntry(self.frame_password_row, placeholder_text="Password", show="*", width=200)

        self.checkbox_show_password = ctk.CTkCheckBox(self.frame_content, text=" Show Password", command=self.show_password)
        self.btn_login = ctk.CTkButton(self.frame_content, text="Login", command=self.login)

        set_theme()
        self.create_widgets()

    def show_password(self):
        """Reveal the password by removing the '*' mask in the entry field."""
        self.entry_password.configure(show="")
        self.checkbox_show_password.configure(command=self.hide_password)

    def hide_password(self):
        """Hide the password again by masking it with '*'."""
        self.entry_password.configure(show="*")
        self.checkbox_show_password.configure(command=self.show_password)

    def fade_in_background(self, base_img, width, height, steps=20, delay=30):
        """
        Animate a smooth fade-in from black to the background image.

        Parameters:
        - base_img: PIL image to fade in
        - width, height: Target size for the background
        - steps: How many frames in the fade animation
        - delay: Delay between each frame in ms
        """
        black_bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        resized_image = base_img.resize((width, height), Image.NEAREST).convert("RGBA")

        def fade_step(step):
            blended = Image.blend(black_bg, resized_image, step / steps)
            self.bg_image = ctk.CTkImage(light_image=blended, dark_image=blended, size=(width, height))
            self.bg_label.configure(image=self.bg_image)

            if step < steps:
                self.root.after(delay, lambda: fade_step(step + 1))

        fade_step(0)

    def create_widgets(self):
        """
        Organize and place the visible widgets in the login form:
        - Greeting labels
        - Username and password input fields
        - Show password checkbox
        - Login button
        """
        self.frame_content.grid_columnconfigure(0, weight=1)
        self.frame_content.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_content,text="Welcome Back!",fg_color="transparent",font=("Arial", 22)
        ).grid(row=1, column=0, columnspan=2, pady=(35, 2), sticky="n")

        ctk.CTkLabel(self.frame_content,text="Log in to your account",fg_color="transparent"
        ).grid(row=2, column=0, columnspan=2, pady=(0, 30), sticky="n")

        self.frame_username_row.grid(row=3, column=0, columnspan=2, pady=5)
        self.lbl_username_icon.pack(side="left", padx=(0, 10))
        self.entry_username.pack(side="left")

        self.frame_password_row.grid(row=4, column=0, columnspan=2, pady=15)
        self.lbl_password_icon.pack(side="left", padx=(0, 10))
        self.entry_password.pack(side="left")

        self.checkbox_show_password.grid(row=5, column=0, columnspan=2, pady=15)

        self.btn_login.grid(row=6, column=0, columnspan=2, pady=(20, 10))

    def login(self):
        """
        Handle the login logic:
        - Validate input against SQL injection
        - Query database for matching user
        - Show appropriate screen based on user role
        - Show error popup if login fails
        """
        username = self.entry_username.get()
        password = self.entry_password.get()

        if is_suspect_sql_input(username) or is_suspect_sql_input(encrypt_password(password)):
            show_sql_meme_popup(self.root)
            return

        cursor = mydb.cursor()
        query = ("SELECT id, username, first_name, last_name, role FROM users "
                "WHERE username = %s AND password = %s")
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
        """Remove the main login frame from the screen (called on view change)."""
        self.frame_main.destroy()