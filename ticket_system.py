import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

from Demos.win32ts_logoff_disconnected import username
from tkcalendar import DateEntry
from config import *

logger = get_logger(__name__) #zet module naam als log naam


class TicketSystem:
    def __init__(self, root,user_id,previous_window=None):
        """Sets up the UI and prepares the database connection."""
        self.root = root
        self.cursor = mydb.cursor()
        self.previous_window = previous_window

        self.user_id = user_id

        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        # -> Create main frame that holds everything.

        self.frame_search = ctk.CTkFrame(self.frame_main)
        self.frame_search.grid(row=1, column=0,columnspan=2, pady=10, padx=20, sticky="w")
        # -> Create search frame, to separate the search bar from the rest of the UI.

        self.entry_from = ctk.CTkEntry(self.frame_search, width=150, placeholder_text="From")
        self.entry_to = ctk.CTkEntry(self.frame_search, width=150, placeholder_text="To")
        # -> Create "From" and "To" Entry Fields with placeholder text.

        self.entry_date = DateEntry(self.frame_search, width=12, background="darkgrey", foreground="white", borderwidth=2)
        # -> DateEntry from tkcalendar package, lets the user pick a date from calendar instead of typing

        self.tree = ttk.Treeview(
            self.frame_main,
            columns=("Airline", "From", "Schedule", "To", "Price"),
            show="headings",
            height=6)
        # -> Treeview table widget for displaying flight data.

        self.create_widgets()
        # -> Calls create_widgets() which actually places these elements inside the UI.

    def create_widgets(self):
        """Creates and positions all widgets in the UI."""

        ctk.CTkLabel(
            self.frame_main, text="Buy Tickets", font=("Arial", 25, "bold")
        ).grid(row=0, column=0, pady=20, padx=20, sticky="w")
        # -> Create main title label and place it at the top of the main frame

        self.entry_from.insert(0, "Brussels")
        self.entry_from.grid(row=1, column=0, padx=5)
        # -> fill "From" entry with "Brussels" and place it in the search frame

        btn_swap_to_from = ctk.CTkButton(self.frame_search, text="↔", width=40, command=self.swap_locations)
        btn_swap_to_from.grid(row=1, column=1, padx=5)
        # -> Button to swap "From" and "To" locations

        self.entry_to.grid(row=1, column=2, padx=5)
        # -> Position the "To" entry field

        self.entry_date.grid(row=1, column=3, padx=5)
        # -> Position the date selection widget

        btn_back = ctk.CTkButton(self.frame_main, text="<-",command=self.go_back)
        btn_back.grid(row=0, column=1, padx=10,sticky="e")
        # -> Create and position the Back button

        btn_search = ctk.CTkButton(self.frame_search, text="Search", command=self.fetch_flights)
        btn_search.grid(row=1, column=4, padx=10)
        # -> Create and position the Search button

        self.tree.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        # -> Place the flight results TreeView in the main frame

        columns = [("Airline", 150), ("From", 100), ("Schedule", 250), ("To", 100), ("Price", 100)]
        # -> Define column names and their widths for the TreeView

        self.tree["columns"] = [col[0] for col in columns]
        # -> Set column names
        self.tree.bind("<ButtonRelease-1>", self.on_flight_select)

        # -> Configure headings and column widths using a loop
        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)  # Set column header text
            self.tree.column(col_name, width=width)  # Set column width
        btn_book_ticket = ctk.CTkButton(self.frame_main, text="Book Ticket", command=self.book_ticket)
        btn_book_ticket.grid(row=3, column=1, padx=10)

    def go_back(self):
        if self.previous_window:
            self.previous_window.deiconify()
        self.root.destroy()

    def swap_locations(self):
        """Swap the locations in the 'From' and 'To' fields."""
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()
        self.entry_from.delete(0, "end")
        self.entry_from.insert(0, to_location)
        self.entry_to.delete(0, "end")
        self.entry_to.insert(0, from_location)

    def fetch_flights(self):
        """Fetch flights from the database based on the user's input."""
        self.tree.delete(*self.tree.get_children())
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()

        sql_query = "SELECT id, airline, from_location, CONCAT(departure, ' - ', arrival) AS flight_schedule, to_location, price FROM flights WHERE from_location=%s AND to_location=%s"
        self.cursor.execute(sql_query, (from_location, to_location))

        self.flights_data = {}

        for row in self.cursor.fetchall():
            flight_id, airline, from_location, flight_schedule, to_location, price = row
            self.tree.insert("", "end", values=(airline, from_location, flight_schedule, to_location, price))

            tree_id = self.tree.get_children()[-1]
            self.flights_data[tree_id] = flight_id

    def on_flight_select(self, event):
        """Get selected flight details and store them, including id."""
        selected_item = self.tree.selection()

        if not selected_item:
            return

        tree_id = selected_item[0]
        flight_values = self.tree.item(tree_id, "values")
        flight_id = self.flights_data.get(tree_id)

        self.selected_flight = (flight_id,) + flight_values
        logger.info(f"User ID:{self.user_id}, Selected a flight in booking system: {self.selected_flight}")

    def book_ticket(self):
        """Proceed to additional package screen after booking the ticket."""
        if not hasattr(self, "selected_flight"):
            print("No flight selected!")
            return

        package_window = tk.Toplevel(self.root)
        package_screen = AdditionalPackageScreen(package_window, selected_flight=self.selected_flight,user_id=self.user_id)

    def open_package_screen(self):
        package_window = tk.Toplevel(self.master)
        package_screen = AdditionalPackageScreen(package_window, selected_flight=self.selected_flight,user_id=self.user_id)

    def refresh_flights(self):
        """Refresh the Treeview to reflect the current flight list."""
        self.tree.delete(*self.tree.get_children())
        self.fetch_flights()

class AdditionalPackageScreen:
    def __init__(self, root, selected_flight, user_id):
        self.root = root
        self.selected_flight = selected_flight
        self.frame_main = ctk.CTkFrame(self.root, border_color="black", border_width=5)
        self.frame_main.pack(fill="both", expand=True)
        self.user_id = user_id
        self.cursor = mydb.cursor()
        set_theme()

        flight_id, airline, from_location, departure, to_location, price = self.selected_flight
        flight_info = f"Flight: {airline} | {from_location} to {to_location} | {departure} | Price: {price}"

        self.flight_info_label = ctk.CTkLabel(self.frame_main, text=flight_info, font=("Arial", 14, "bold"))
        self.flight_info_label.pack(pady=10)

        self.success_label = ctk.CTkLabel(self.frame_main, text="Ticket reserved! Now choose your additional packages.")
        self.success_label.pack(pady=10)

        self.package1_button = ctk.CTkButton(self.frame_main, text="Package 1", command=self.package1_selected)
        self.package1_button.pack(pady=5)

        self.package2_button = ctk.CTkButton(self.frame_main, text="Package 2", command=self.package2_selected)
        self.package2_button.pack(pady=5)

        self.buy_button = ctk.CTkButton(self.frame_main, text="Buy", command=self.finalize_purchase)
        self.buy_button.pack(pady=10)

    def package1_selected(self):
        print("Package 1 selected")

    def package2_selected(self):
        print("Package 2 selected")

    def finalize_purchase(self):
        if not hasattr(self, "selected_flight"):
            print("No flight selected!")
            return

        flight_id, airline, from_location, departure, to_location, price = self.selected_flight
        user_id = self.user_id

        query = """
            INSERT INTO bookings (user_id, flight_id, booking_date, status)
            VALUES (%s, %s, NOW(), 'Booked')
        """
        self.cursor.execute(query, (user_id, flight_id))
        mydb.commit()

        update_query = """
            UPDATE flights
            SET seats_taken = seats_taken + 1
            WHERE id = %s
        """
        self.cursor.execute(update_query, (flight_id,))
        mydb.commit()
        logger.info(f"Booking for user ID '{self.user_id}' succesful!")
