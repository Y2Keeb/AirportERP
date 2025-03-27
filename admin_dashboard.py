"""The admin dashboard"""

import tkinter as tk
import customtkinter as ctk
from class_GUI import MainWindow, AdminScreen
from config import mydb


root = tk.Tk()
app = AdminScreen(root)
root.mainloop()
