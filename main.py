"""
The mainscreen using CustomTkinter
"""
import customtkinter
from login_screen import LoginScreen

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("themes/rime.json")

root = customtkinter.CTk()
root.title("Airport ERP Login")

app = LoginScreen(root)

root.bind("<Return>", lambda event: app.login())

root.mainloop()
