"""All Function for building the GUI"""

import tkinter as tk
from tkinter import messagebox, Menu
from config import mydb


class BaseWindow:
    """Base class for common window functionality"""

    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.create_menu()
  

    def create_menu(self):
        """Creates a menu bar for the application window."""
        menubar = Menu(self.root)
        help_ = Menu(menubar, tearoff=0)
        logout_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_)
        menubar.add_cascade(label="Logout", menu=logout_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        logout_.add_command(label="Logout", command=self.logout)
        logout_.add_command(label="Quit", command=self.kill_window)
        self.root.config(menu=menubar)

    def about(self):
        """Displays the About dialog."""
        tk.messagebox.showinfo(
            message="(c) 2025 AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        """Displays the Help dialog."""
        tk.messagebox.showinfo(
            message="Login by entering your username and password\n"
            "If you don't have a login, contact your administrator"
        )

    def logout(self):
        """Logs out the user and returns to the login screen."""
        self.root.destroy()
        root = tk.Tk()
        LoginScreen(root)
        root.mainloop()

    def kill_window(self):
        """quit"""
        self.root.destroy()


class LoginScreen(BaseWindow):
    """This module is used to create the Login screen"""

    def __init__(self, root):
        super().__init__(root, "Login Venster")
        self.root.geometry("300x500")
        self.create_widgets()

    def create_widgets(self):
        """Creates the Login screen"""
        self.add_image("docs/icons/plane-prop.png")

        tk.Label(self.root, text="Welcome Back!", font=("Comics-sans", 25)).pack()
        tk.Label(self.root, text="Log in to your account").pack()

        self.entry_username = self.create_labeled_entry("username:")
        self.entry_password = self.create_labeled_entry("password:", show="*")

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def create_labeled_entry(self, label_text, **kwargs):
        """Creates a labeled entry widget"""
        tk.Label(self.root, text=label_text).pack(pady=5)
        entry = tk.Entry(self.root, **kwargs)
        entry.pack(pady=5)
        return entry

    def add_image(self, image_path):
        """Adds an image to the window"""
        image = tk.PhotoImage(file=image_path)
        tk.Label(self.root, image=image).pack()
        self.root.image = image

    def login(self):
        """
        Handles the login function
        Queries the database for a username and password.
        On successful login, opens the MainWindow.
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
            MainWindow(root)
            root.mainloop()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")


class MainWindow(BaseWindow):
    """Main application window"""

    def __init__(self, root):
        super().__init__(root, "Dashboard")
        self.create_widgets()
        self.admin_dashboard()

    def admin_dashboard(self): # made with ai for reference only -Thomas
        """
        Displays the admin dashboard based on the user's role.
        Queries the database for the user's role and updates the UI accordingly.
        """
        cursor = mydb.cursor()
        query = "SELECT role FROM Users WHERE username = %s"
        username = "admin"  # Replace with the actual logged-in username
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            role = result[0]
            if role == "admin":
                tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20)).pack(pady=10)
                tk.Button(self.root, text="Manage Users", command=self.manage_users).pack(pady=5)
                tk.Button(self.root, text="View Reports", command=self.view_reports).pack(pady=5)
            elif role == "staff":
                tk.Label(self.root, text="Staff Dashboard", font=("Arial", 20)).pack(pady=10)
                tk.Button(self.root, text="View Tasks", command=self.view_tasks).pack(pady=5)
            else:
                tk.Label(self.root, text="Welcome!", font=("Arial", 20)).pack(pady=10)
        else:
            tk.messagebox.showerror("Error", "Unable to fetch user role.")

    def manage_users(self):
        """Handles user management functionality."""
        tk.messagebox.showinfo("Manage Users", "User management functionality goes here.")

    def view_reports(self):
        """Handles viewing reports functionality."""
        tk.messagebox.showinfo("View Reports", "Report viewing functionality goes here.")

    def view_tasks(self):
        """Handles viewing tasks functionality."""
        tk.messagebox.showinfo("View Tasks", "Task viewing functionality goes here.")



    def create_widgets(self):
        """Creates widgets for the main window"""
        self.add_image("docs/icons/plane-prop.png")

    def add_image(self, image_path):
        """Adds an image to the window"""
        image = tk.PhotoImage(file=image_path)
        tk.Label(self.root, image=image).pack()
        self.root.image = image
