"""All Function for building the GUI"""

import tkinter as tk
from tkinter import messagebox, Menu
from config import mydb
import importlib


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
        login_module = importlib.import_module('login_screen')
        login_screen = login_module.LoginScreen(tk.Tk())
        tk.mainloop()

    def kill_window(self):
        """quit"""
        self.root.destroy()

class MainWindow(BaseWindow):
    """Main application window"""

    def __init__(self, root):
        super().__init__(root, "Dashboard")
        self.create_widgets()
        self.admin_dashboard()

    # moved role determination to login function

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
        tk.Label(self.root, text="Welcome Admin!", font=("Arial", 20)).pack(pady=10)

class StaffScreen(BaseWindow):
    """Staff dashboard"""
    def __init__(self, root):
        super().__init__(root, "Staff Dashboard")
        tk.Label(self.root, text="Welcome Staff!", font=("Arial", 20)).pack(pady=10)

class UserScreen(BaseWindow):
    """User dashboard"""
    def __init__(self, root, username):
        super().__init__(root, "User Dashboard")
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        greeting_label = tk.Label(self.root, text=f"Hi {self.username}!", font=("Arial", 20))
        greeting_label.pack(pady=10)

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        btn_buy_tickets = tk.Button(frame_buttons, text="Buy Tickets", width=20, command=self.buy_tickets)
        btn_buy_tickets.grid(row=0, column=0, padx=10)

        btn_my_bookings = tk.Button(frame_buttons, text="My Bookings", width=20,command=self.my_bookings)
        btn_my_bookings.grid(row=0, column=1, padx=10)

        frame_flight_info = tk.Frame(self.root, width=500, height=300, relief="solid")
        frame_flight_info.pack(pady=20)
        frame_flight_info.pack_propagate(False)

        tk.Label(frame_flight_info, text="Upcoming Flight Info Here", font=("Arial", 14)).pack(pady=20)

    def buy_tickets(self):
        """Handles the Buy Tickets button"""
        new_window = tk.Toplevel(self.root)
        ticket_module = importlib.import_module('ticket_system')
        ticket_system = ticket_module.TicketSystem(new_window)

    def my_bookings(self):
        """Handles the My Bookings button"""
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id_result = cursor.fetchone()
        user_id = user_id_result[0]
        # -> om user_id te krijgen ipv username, dus 5 ipv "user_1"

        new_window = tk.Toplevel(self.root)
        my_bookings_module = importlib.import_module('my_bookings')
        booking_module = my_bookings_module.MyBookings(new_window, user_id)