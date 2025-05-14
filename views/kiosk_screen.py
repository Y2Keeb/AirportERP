import tkinter as tk
from tkinter import Menu,messagebox

import PIL
from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from config import mydb, set_theme, is_suspect_sql_input, encrypt_password, decrypt_password
from basewindow import BaseWindow
from ui_helpers import show_sql_meme_popup
from views.user_screen import UserScreen

class KioskLoginScreen(BaseWindow):
    def __init__(self, root,view_manager=None):
        super().__init__(root,title=" ")
        """
        Initialize the kiosk login screen.
        Creates the layout, background image, menu, and input areas.
        """
        self.root = root
        self.view_manager = view_manager
        self.create_menu_bar(["help"])

        self.original_bg_image = PIL.Image.open("docs/icons/background2.png").convert("RGBA")
        startup_image = self.original_bg_image.resize((1600, 950), Image.NEAREST)
        self.bg_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image, size=(1600, 950))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_main = ctk.CTkFrame(
            self.root,
            fg_color="transparent",
            bg_color="black"
        )
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        self.menu_bar.lift()

        self.frame_welcome = ctk.CTkFrame(self.frame_main, border_width=7,border_color="black",fg_color="gray11")
        self.frame_welcome.pack(side="left",fill="both",padx=(0,15),expand=True)
        self.frame_login= ctk.CTkFrame(self.frame_main, border_width=7,border_color="black",fg_color="gray11")
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
        self.checkbox_show_password = ctk.CTkCheckBox(self.frame_login_content, text=" Show Password", command=self.show_password)

        set_theme()
        self.create_widgets()

    def create_widgets(self):
        """
        Build the initial login layout inside the welcome and login frames.
        """
        ctk.CTkLabel(self.frame_welcome_content, text="Welcome!", font=("Comic Sans", 25)).pack()
        ctk.CTkLabel(self.frame_welcome_content, text="Log in to your account or create one.").pack()

        ctk.CTkLabel(self.frame_login_content, text="Username:").pack(pady=5)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_login_content, text="Password:").pack(pady=5)
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_login_content, text="Login", command=self.login)
        btn_login.pack(pady=10)
        self.checkbox_show_password.pack(pady=10)
        lbl_or = ctk.CTkLabel(self.frame_login_content,text="or")
        lbl_or.pack(pady=10)
        btn_register = ctk.CTkButton(self.frame_login_content, text="Register", command=self.show_register_form)
        btn_register.pack(pady=10)

    def login(self):
        """
        Handle user login by validating credentials and loading the UserScreen on success.
        Shows error messages on failure or if SQL injection is detected.
        """
        username = self.entry_username.get()
        password = self.entry_password.get()

        if is_suspect_sql_input(username) or is_suspect_sql_input(password):
            show_sql_meme_popup(self.root)
            return
        cursor = mydb.cursor()
        query = (
            "SELECT id, username, first_name, last_name, role, password FROM users "
            "WHERE username = %s"
        )
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            stored_encrypted_password = result[5]
            if decrypt_password(stored_encrypted_password) == password:
                pass
            else:
                result = None
        if result:
            role = result[4]

            self.destroy_menu_bar()
            self.frame_main.destroy()

            if role == "user":
                self.root.view_manager.show_view(
                    UserScreen,
                    username=username,
                    user_id=result[0],
                    role=role
                )
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_password(self):
        """Reveal the password by removing the '*' mask in the entry field."""
        self.entry_password.configure(show="")
        self.checkbox_show_password.configure(command=self.hide_password)

    def hide_password(self):
        """Hide the password again by masking it with '*'."""
        self.entry_password.configure(show="*")
        self.checkbox_show_password.configure(command=self.show_password)

    def show_register_form(self):
        """Replace login form with a registration form."""
        for widget in self.frame_login_content.winfo_children():
            widget.destroy()

        self.entry_reg_username = ctk.CTkEntry(self.frame_login_content, placeholder_text="Username")
        self.entry_reg_firstname = ctk.CTkEntry(self.frame_login_content, placeholder_text="First Name")
        self.entry_reg_lastname = ctk.CTkEntry(self.frame_login_content, placeholder_text="Last Name")
        self.entry_reg_password = ctk.CTkEntry(self.frame_login_content, placeholder_text="Password", show="*")

        self.entry_reg_username.pack(pady=5)
        self.entry_reg_firstname.pack(pady=5)
        self.entry_reg_lastname.pack(pady=5)
        self.entry_reg_password.pack(pady=5)

        btn_submit = ctk.CTkButton(self.frame_login_content, text="Create Account", command=self.register_user)
        btn_submit.pack(pady=10)

        btn_back = ctk.CTkButton(self.frame_login_content, text="Back to Login", command=self.back_to_login)
        btn_back.pack(pady=10)

    def register_user(self):
        """Insert new user into the database.
        Shows error messages on failure or if SQL injection is detected.
        """
        username = self.entry_reg_username.get()
        first_name = self.entry_reg_firstname.get()
        last_name = self.entry_reg_lastname.get()
        password = self.entry_reg_password.get()
        user_inputs = [username,first_name,last_name,password]

        if any(is_suspect_sql_input(value) for value in user_inputs):
            show_sql_meme_popup(self.root)
            return

        if any(not val for val in [username, first_name, last_name, password]):
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        if is_suspect_sql_input(username) or is_suspect_sql_input(password):
            show_sql_meme_popup(self.root)
            return

        cursor = mydb.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                return
            encrypted_password = encrypt_password(password)
            cursor.execute(
                "INSERT INTO users (username, first_name, last_name, role, password) VALUES (%s, %s, %s, %s, %s)",
                (username, first_name, last_name, "user", encrypted_password)
            )
            mydb.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.back_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create account.\n{e}")
        finally:
            cursor.close()

    def back_to_login(self):
        """Return to login form layout by clearing and rebuilding only the login frame."""
        for widget in self.frame_login_content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_login_content, text="Username:").pack(pady=5)
        self.entry_username = ctk.CTkEntry(self.frame_login_content)
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_login_content, text="Password:").pack(pady=5)
        self.entry_password = ctk.CTkEntry(self.frame_login_content, show="*")
        self.entry_password.pack(pady=5)

        self.checkbox_show_password = ctk.CTkCheckBox(self.frame_login_content, text=" Show Password",
                                                      command=self.show_password)
        self.checkbox_show_password.pack(pady=10)

        btn_login = ctk.CTkButton(self.frame_login_content, text="Login", command=self.login)
        btn_login.pack(pady=10)

        lbl_or = ctk.CTkLabel(self.frame_login_content, text="or")
        lbl_or.pack(pady=10)

        btn_register = ctk.CTkButton(self.frame_login_content, text="Register", command=self.show_register_form)
        btn_register.pack(pady=10)

    def help_menu(self):
        """
        Display a help popup with basic instructions for kiosk login.
        """
        CTkMessagebox(
            title="Info",
            icon="question",
            message="• Login by entering your username and password.\n"
                    "• If you don't have a login, create one or contact your administrator.",
        )

    def cleanup(self):
        """
        Remove the main frame from the root. Called on screen change.
        """
        self.frame_main.destroy()
