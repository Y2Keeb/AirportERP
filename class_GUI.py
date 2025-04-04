"""All Function for building the GUI"""

import tkinter as tk
from tkinter import Menu
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import importlib
from config import mydb,set_theme


class BaseWindow:
    """Base class for common window functionality"""

    def __init__(self, root, title):
        set_theme()
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
        CTkMessagebox(
            title="Info", message="(c) AirportERP\n BY \n Lindsey, Reza And Thomas"
        )

    def help_menu(self):
        """Displays the Help dialog."""
        tk.messagebox.showinfo(
            message="Login by entering your username and password\n"
                    "If you don't have a login, contact your administrator"

        )

    def logout(self):
        """Logs out the user and returns to the login screen."""

        self.root.quit()
        self.root.destroy()

        login_module = importlib.import_module('login_screen')
        login_screen = login_module.LoginScreen(tk.Tk())
        self.root.mainloop()

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
        tk.messagebox.showinfo(
            "Manage Users", "User management functionality goes here."
        )

    def view_reports(self):
        """Handles viewing reports functionality."""
        tk.messagebox.showinfo(
            "View Reports", "Report viewing functionality goes here."
        )

    def view_tasks(self):
        """Handles viewing tasks functionality."""
        tk.messagebox.showinfo("View Tasks", "Task viewing functionality goes here.")

    def create_widgets(self):
        """Creates widgets for the main window"""
        self.add_image("docs/icons/plane-prop.png")

    def add_image(self, image_path):
        self.image = tk.PhotoImage(file=image_path)
        tk.Label(self.root, image=self.image).pack()
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
        self.root.geometry("800x500")

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id_result = cursor.fetchone()
        self.user_id = user_id_result[0] if user_id_result else None

        self.main_frame = ctk.CTkFrame(self.root, border_color="black", border_width=5)
        self.main_frame.pack(fill="both", expand=True)

        self.show_home_view()
        self.display_upcoming_flight()
    def show_home_view(self):
        """Show the default dashboard view using grid layout"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        greeting_label = ctk.CTkLabel(
            content_frame, text=f"Hi {self.username}!",
            font=("Arial", 24, "bold")
        )
        greeting_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="e")

        # Buttons Frame (Now Below Greeting)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="e", padx=20)

        btn_buy_tickets = ctk.CTkButton(buttons_frame, text="Buy Tickets", command=self.buy_tickets)
        btn_buy_tickets.grid(row=0, column=0, padx=5)

        btn_my_bookings = ctk.CTkButton(buttons_frame, text="My Bookings", command=self.my_bookings)
        btn_my_bookings.grid(row=0, column=1, padx=5)

        # Upcoming Flight Label
        upcoming_label = ctk.CTkLabel(content_frame, text="Upcoming flight:", font=("Arial", 16, "bold"))
        upcoming_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 2))

        # Upcoming Flight Frame
        self.upcoming_flight_frame = ctk.CTkFrame(content_frame, border_width=2, border_color="black")
        self.upcoming_flight_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")

        self.display_upcoming_flight()

        # Adjust grid proportions
        content_frame.grid_rowconfigure(3, weight=1)  # Allow flight section to expand
        content_frame.grid_columnconfigure((0, 1), weight=1)

    def buy_tickets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id_result = cursor.fetchone()
        user_id = user_id_result[0]

        ticket_module = importlib.import_module('ticket_system')
        ticket_system = ticket_module.TicketSystem(self.main_frame, user_id, parent=self)
        self.display_upcoming_flight()

    def my_bookings(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        my_bookings_module = importlib.import_module('my_bookings')
        my_bookings = my_bookings_module.MyBookings(self.main_frame, self.user_id, parent=self)
        self.display_upcoming_flight()

    def display_upcoming_flight(self):
        """Displays flight details dynamically from the database"""
        if not hasattr(self, 'upcoming_flight_frame') or not self.upcoming_flight_frame.winfo_exists():
            # Re-create the frame if it was destroyed
            self.upcoming_flight_frame = ctk.CTkFrame(self.main_frame, border_width=2, border_color="black")
            self.upcoming_flight_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")

        # Now proceed to clear and update the flight data as before
        for widget in self.upcoming_flight_frame.winfo_children():
            widget.destroy()

        try:
            cursor = mydb.cursor(dictionary=True)

            query = """
                    SELECT f.airline, f.departure, f.arrival, f.status, f.gate, f.plane_type,
                           f.total_seats, f.seats_taken, f.from_location, f.to_location, f.airline_icon
                    FROM bookings b
                    JOIN flights f ON b.flight_id = f.id
                    WHERE b.user_id = %s AND f.departure > NOW()  -- Only flights with departure in the future
                    ORDER BY f.departure ASC  -- Get the earliest upcoming flight
                    LIMIT 1
                    """
            cursor.execute(query, (self.user_id,))
            flight = cursor.fetchone()

            if not flight:
                no_flight_label = ctk.CTkLabel(
                    self.upcoming_flight_frame, text="No upcoming flights.",
                    font=("Arial", 14, "italic")
                )
                no_flight_label.grid(row=0, column=0, padx=10, pady=10)
                return

            flight_info_label = ctk.CTkLabel(
                self.upcoming_flight_frame,
                text=f"{flight['airline']} Flight\n"
                     f"{flight['from_location']} ➝ {flight['to_location']}",
                font=("Arial", 16, "bold"),
                justify="center"
            )
            flight_info_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))

            details = [
                ("Departure:", f"{flight['departure']}"),
                ("Arrival:", f"{flight['arrival']}"),
                ("Gate:", f"{flight['gate']}"),
                ("Status:", f"{flight['status']}"),
                ("Plane Type:", f"{flight['plane_type']}"),
            ]

            for i, (label, value) in enumerate(details):
                ctk.CTkLabel(self.upcoming_flight_frame, text=label, font=("Arial", 14)).grid(
                    row=i + 1, column=0, sticky="w", padx=10, pady=2
                )
                ctk.CTkLabel(self.upcoming_flight_frame, text=value, font=("Arial", 14)).grid(
                    row=i + 1, column=1, sticky="w", padx=10, pady=2
                )

            # QR code placeholder
            airline_icon = ctk.CTkLabel(self.upcoming_flight_frame, text="QR CODE HERE",
                                        font=("Arial", 20))  # Placeholder
            airline_icon.grid(row=1, column=2, rowspan=3, padx=20, pady=5, sticky="e")

            self.upcoming_flight_frame.grid_columnconfigure(1, weight=1)

        except Exception as e:
            print("Error fetching flight data:", e)

        finally:
            cursor.close()
