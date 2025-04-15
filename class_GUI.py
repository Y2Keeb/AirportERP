
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
        self.root.grid_propagate(False)  # Prevent window from resizing to smallest possible

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
        CTkMessagebox(title="About", message="AirportERP\nDeveloped by Your Team")

    def help_menu(self):
        CTkMessagebox(title="Help", message="Contact administrator for assistance")

    def logout(self):
        from views.login_screen import LoginScreen
        self.view_manager.reset()
        self.view_manager.pop_view()
        self.view_manager.show_view(LoginScreen)

    def kill_window(self):
        self.root.quit()

class MainWindow(BaseWindow):
    """Main application window"""

    def __init__(self, root):
        super().__init__(root, "Dashboard")
        self.create_widgets()
        self.admin_dashboard()

    def manage_users(self):
        """Handles user management functionality."""
        tk.messagebox.showinfo(
            "Manage Users", "User management functionality goes here."
        )

    def view_reports(self):
        """Handles viewing reports functionality."""
        tk.messagebox.showinfo(
            "View Reports", "Report viewing functionality goes here."
        )

    def view_tasks(self):
        """Handles viewing tasks functionality."""
        tk.messagebox.showinfo("View Tasks", "Task viewing functionality goes here.")

    def create_widgets(self):
        """Creates widgets for the main window"""
        self.add_image("docs/icons/plane-prop.png")

class AdminScreen(BaseWindow):
    """Admin dashboard"""

    def __init__(self, root):
        super().__init__(root, "Admin Dashboard")
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        set_theme()
        self.create_widgets()

    def create_widgets(self):
        greeting_label = ctk.CTkLabel(self.frame_main, text=f"Welcome Admin!", font=("Arial", 20))
        greeting_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
class StaffScreen(BaseWindow):
    """Staff dashboard"""

    def __init__(self, root):
        super().__init__(root, "Staff Dashboard")
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        set_theme()
        self.create_widgets()

    def create_widgets(self):
        greeting_label = ctk.CTkLabel(self.frame_main, text=f"Welcome Staff!", font=("Arial", 20))
        greeting_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
