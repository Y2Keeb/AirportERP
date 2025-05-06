from basewindow import BaseWindow
from config import set_theme
import customtkinter as ctk

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

    def manage_users(self):
        """Handles user management functionality."""
        ctk.messagebox.showinfo(
            "Manage Users", "User management functionality goes here."
        )

    def view_reports(self):
        """Handles viewing reports functionality."""
        ctk.messagebox.showinfo(
            "View Reports", "Report viewing functionality goes here."
        )

    def view_tasks(self):
        """Handles viewing tasks functionality."""
        ctk.messagebox.showinfo("View Tasks", "Task viewing functionality goes here.")

    def create_widgets(self):
        """Creates widgets for the main window"""
        self.add_image("docs/icons/plane-prop.png")