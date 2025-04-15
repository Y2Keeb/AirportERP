import tkinter as tk
from tkinter import Menu,messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from view_manager import ViewManager
from config import set_theme


class BaseWindow:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.view_manager = ViewManager(root)
        set_theme()
        self.create_menu()
        self.root.grid_propagate(False)

    def create_menu(self):
        menubar = Menu(self.root)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.help_menu)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.about)

        account_menu = Menu(menubar, tearoff=0)
        account_menu.add_command(label="Logout", command=self.logout)
        account_menu.add_command(label="Exit", command=self.kill_window)

        menubar.add_cascade(label="Help", menu=help_menu)
        menubar.add_cascade(label="Account", menu=account_menu)

        self.root.config(menu=menubar)

    def about(self):
        CTkMessagebox(title="Info", message="(c) AirportERP\nBY Lindsey, Reza and Thomas")
    def help_menu(self):
        CTkMessagebox(title="Help", message="• Login by entering your username and password.\n• If you don't have a login, contact your administrator.")

    def logout(self):
        from views.login_screen import LoginScreen
        self.view_manager.reset()
        self.view_manager.pop_view()
        self.view_manager.show_view(LoginScreen)

    def kill_window(self):
        self.root.quit()

