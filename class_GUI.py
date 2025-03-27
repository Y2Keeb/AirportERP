"""All Function for building the GUI"""

import tkinter as tk
from tkinter import Menu
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tksheet
import importlib
from config import mydb,set_theme


class BaseWindow:
    """Base class for common window functionality"""

    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.create_menu()
        set_theme()

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
        try:
            self.root.quit()
            self.root.destroy()
        except tk.TclError:
            pass
        except Exception as e:
            print(f"Error while logging out: {e}")

        login_module = importlib.import_module('login_screen')
        login_screen = login_module.LoginScreen(tk.Tk())

    def kill_window(self):
        """quit"""
        self.root.destroy()

class MainWindow(BaseWindow):
    """Main application window"""

    def __init__(self, root):
        super().__init__(root, "Dashboard")
        self.create_widgets()
        self.admin_dashboard()

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


class UserScreen(BaseWindow):
    """User dashboard"""

    def __init__(self, root, username):
        super().__init__(root, "User Dashboard")
        self.username = username
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        set_theme()
        self.create_widgets()


    def create_widgets(self):

        greeting_label = ctk.CTkLabel(self.frame_main, text=f"Hi {self.username}!", font=("Arial", 20))
        greeting_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        btn_buy_tickets = ctk.CTkButton(self.frame_main, text="Buy Tickets", command=self.buy_tickets)
        btn_buy_tickets.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        btn_my_bookings = ctk.CTkButton(self.frame_main, text="My Bookings", command=self.my_bookings)
        btn_my_bookings.grid(row=1, column=1, pady=10, padx=20, sticky="w")

    def buy_tickets(self):
        """Handles the Buy Tickets button"""
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)

        ticket_module = importlib.import_module('ticket_system')
        ticket_system = ticket_module.TicketSystem(new_window,previous_window=self.root)

    def my_bookings(self):
        """Handles the My Bookings button"""
        self.root.withdraw()
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id_result = cursor.fetchone()
        user_id = user_id_result[0]
        # -> om user_id te krijgen ipv username, dus 5 ipv "user_1"

        new_window = tk.Toplevel(self.root)
        my_bookings_module = importlib.import_module('my_bookings')
        my_bookings_window = my_bookings_module.MyBookings(new_window, user_id, previous_window=self.root)

    def on_my_bookings_close(self):
        """When MyBookings is closed, show UserScreen again"""
        self.root.deiconify()

    def on_buytickets_close(self):
        self.root.deiconify()