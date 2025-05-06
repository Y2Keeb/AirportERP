from basewindow import BaseWindow
from config import set_theme
import customtkinter as ctk

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
