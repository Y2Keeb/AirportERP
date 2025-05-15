import os
import tkinter as tk
from tkinter import Menu,messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from view_manager import ViewManager
from config import set_theme

class BaseWindow:
    def __init__(self, root, title, menu_buttons=None):
        self.root = root
        self.root.configure(bg="black")  # Makes root black behind the image
        script_dir = os.path.dirname(os.path.abspath(__file__))  # basewindow.py location
        icon_path = os.path.join(script_dir, "docs", "icons", "favicon.ico")
        if os.path.exists(icon_path):
            self.root.wm_iconbitmap(icon_path)

        self.root.title(title)
        self.view_manager = ViewManager(root)
        set_theme()
        self.root.grid_propagate(False)

        self.create_menu_bar(menu_buttons or ["help", "about", "logout", "exit"])

    def create_menu_bar(self, menu_buttons):
        if hasattr(self, 'menu_bar') and self.menu_bar.winfo_exists():
            self.menu_bar.destroy()

        self.menu_bar = ctk.CTkFrame(self.root, fg_color="#1c1c1c", height=30)
        self.menu_bar.place(relx=0, rely=0, relwidth=1)

        if "help" in menu_buttons:
            help_button = ctk.CTkButton(self.menu_bar, text="Help", width=60, height=24, fg_color="transparent",
                                        text_color="white", hover_color="#333333", command=self.help_menu)
            help_button.pack(side="left", padx=10, pady=3)

        if "about" in menu_buttons:
            about_button = ctk.CTkButton(self.menu_bar, text="About", width=60, height=24, fg_color="transparent",
                                         text_color="white", hover_color="#333333", command=self.about)
            about_button.pack(side="left", padx=0, pady=3)

        if "logout" in menu_buttons:
            logout_button = ctk.CTkButton(self.menu_bar, text="Logout", width=70, height=24, fg_color="transparent",
                                          text_color="white", hover_color="#333333", command=self.logout)
            logout_button.pack(side="right", padx=10, pady=3)

        if "exit" in menu_buttons:
            exit_button = ctk.CTkButton(self.menu_bar, text="Exit", width=60, height=24, fg_color="transparent",
                                        text_color="white", hover_color="#333333", command=self.kill_window)
            exit_button.pack(side="right", padx=0, pady=3)

    def destroy_menu_bar(self):
        if hasattr(self, "menu_bar"):
            self.menu_bar.destroy()

    def about(self):
        CTkMessagebox(title="Info", message="(c) AirportERP\nBY Lindsey, Reza and Thomas")

    def help_menu(self):
        CTkMessagebox(title="Help", message="• Login by entering your username and password.\n• If you don't have a login, contact your administrator.")

    def logout(self):
        """Handle logout based on current user type"""
        self.cleanup()

        if hasattr(self, 'root') and self.root.winfo_exists():
            if hasattr(self, 'view_state') and self.view_state.get('role') == 'user':
                from views.kiosk_screen import KioskLoginScreen
                for widget in self.root.winfo_children():
                    widget.destroy()
                KioskLoginScreen(self.root, view_manager=self.view_manager)
            else:
                from views.login_screen import LoginScreen
                for widget in self.root.winfo_children():
                    widget.destroy()
                LoginScreen(self.root, view_manager=self.view_manager)

    def kill_window(self):
        self.root.quit()

    def cleanup(self):
        """Clean up all window resources"""
        if hasattr(self, 'menu_bar') and self.menu_bar.winfo_exists():
            self.menu_bar.destroy()
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()