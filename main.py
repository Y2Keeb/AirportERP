"""
The mainscreen
"""

import tkinter as tk
from login_screen import LoginScreen

root = tk.Tk()
app = LoginScreen(root)
root.bind("<Return>", lambda event: app.login())
root.mainloop()


