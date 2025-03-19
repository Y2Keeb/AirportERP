"""
The mainscreen
"""
import tkinter as tk
from tkinter import messagebox, Menu
import mysql.connector
from class_GUI import LoginScreen

root = tk.Tk()
app = LoginScreen(root)
root.bind("<Return>", lambda event: app.login())
root.mainloop()
