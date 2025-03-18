"""All Function for building the GUI"""

import tkinter as tk
from tkinter import messagebox, Menu
from config import mydb

class LoginScreen:
    """This module is used to create the Login screen"""

    def __init__(self, root):
        self.root = root
        self.root.title("Login Venster")
        self.root.geometry("300x500")
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        """This creates the Login screen"""
        image = tk.PhotoImage(file="docs/icons/plane-prop.png")
        tk.Label(self.root, image=image).pack()
        self.root.image = image

        tk.Label(self.root, text="Welcome Back!", font=("Comics-sans", 25)).pack()
        tk.Label(self.root, text="Log in to your account").pack()

        tk.Label(self.root, text="username:").pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)

        tk.Label(self.root, text="password:").pack(pady=5)
        self.entry_password = tk.Entry(
            self.root,
            show="*",
        )
        self.entry_password.pack(pady=5)

        btn_login = tk.Button(self.root, text="Login", command=self.login)
        btn_login.pack(pady=20)

    def create_menu(self):
        """Creates a menu bar for the application window."""
        menubar = Menu(self.root)
        help_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        self.root.config(menu=menubar)

    def login(self):
        """
        Handles the login function
        it querrys the database for a username and password if the result is negative
        a messagebox appears to tell the user
        on succelfull login the window is closed and the MainWindow is opened
        """
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = mydb.cursor()
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            tk.messagebox.showinfo("Login Success", "Welcome!")
            self.root.destroy()
            root = tk.Tk()
            app = MainWindow(root)
            root.mainloop()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    def about(self):
        tk.messagebox.showinfo(
            message="(c) 2025 AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        tk.messagebox.showinfo(
            message="login by entering your username and password\n"
            "if you don't have a login contact your administrator"
        )

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Dashboard')
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = Menu(self.root)
        help_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        self.root.config(menu=menubar)

    def about(self):
        tk.messagebox.showinfo(
            message="(c) 2025 AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        tk.messagebox.showinfo(
            message="login by entering your username and password\n"
            "if you don't have a login contact your administrator"
        )

    def create_widgets(self):
        image = tk.PhotoImage(file="docs/icons/plane-prop.png")
        tk.Label(self.root, image=image).pack()
        self.root.image = image

