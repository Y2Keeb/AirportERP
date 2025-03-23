import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import mydb


class MyBookings:
    def __init__(self, root, user_id):
        """Initialize the My Bookings window"""
        self.root = root
        self.cursor = mydb.cursor()
        self.root.title("My Bookings")
        self.root.geometry("700x500")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("themes/marsh.json")

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.frame, text="My Bookings", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(0, 10))


        self.tree = ttk.Treeview(
            self.frame,
            columns=("Status", "Departure", "Destination", "Flight Info"),
            show="headings",
            height=6)

        self.user_id = user_id
        self.create_ui()
        self.load_bookings()

    def create_ui(self):
        """Creates the UI layout"""
        columns = [("Status", 100), ("Departure", 100), ("Destination", 100), ("Flight Info", 350)]

        self.tree = ttk.Treeview(self.frame, columns=[col[0] for col in columns], show="headings", height=6)

        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width)

        treeview_frame = ctk.CTkFrame(self.frame)
        treeview_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def load_bookings(self):
        """Fetches and displays user bookings from the database"""
        self.cursor.execute("SELECT id, flight_id, booking_date, status FROM bookings WHERE user_id = %s",
                            (self.user_id,))
        bookings = self.cursor.fetchall()
        if bookings:
            for booking in bookings:
                flight_info = self.get_flight_info(booking[1])
                departure_info = self.get_departure_location(booking[0])
                destination_info = self.get_destination_location(booking[0])
                self.tree.insert("", tk.END, values=(booking[3],departure_info,destination_info, flight_info))
        else:
            messagebox.showinfo("No Bookings", "No bookings found for this user.")

    def get_flight_info(self, flight_id):
        """Fetches flight information based on the flight_id."""
        self.cursor.execute("SELECT airline, departure, arrival FROM flights WHERE id = %s", (flight_id,))
        flight = self.cursor.fetchone()
        if flight:
            return f"{flight[0]} ({flight[1]} - {flight[2]})"
        return "Unknown Flight"

    def get_departure_location(self, booking_id):
        """Fetches the departure location (from_location) for a given booking."""
        self.cursor.execute("""
            SELECT f.from_location
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.id = %s
        """, (booking_id,))
        departure_location = self.cursor.fetchone()
        if departure_location:
            return departure_location[0]
        return "Unknown Departure Location"

    def get_destination_location(self, booking_id):
        """Fetches the destination location (to_location) for a given booking."""
        self.cursor.execute("""
            SELECT f.to_location
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.id = %s
        """, (booking_id,))
        destination_location = self.cursor.fetchone()
        if destination_location:
            return destination_location[0]
        return "Unknown Destination Location"