import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from config import mydb


class MyBookings:
    def __init__(self, root, user_id):
        """Initialize the My Bookings window"""
        self.root = root
        self.cursor = mydb.cursor()
        self.root.title("My Bookings")
        self.root.geometry("500x300")

        self.user_id = user_id
        self.create_ui()
        self.load_bookings()

    def create_ui(self):
        """Creates the UI layout"""
        columns = ("Booking ID", "Flight Number", "Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both")

    def load_bookings(self):
        """Fetches and displays user bookings from the database"""
        self.cursor.execute("SELECT id, flight_id, booking_date, status FROM bookings WHERE user_id = %s",
                            (self.user_id,))
        bookings = self.cursor.fetchall()
        for booking in bookings:
            flight_info = self.get_flight_info(booking[1])
            print(f"Adding booking to treeview: {booking[0]} - {flight_info} - {booking[2]} - {booking[3]}")
            self.tree.insert("", tk.END, values=(booking[0], flight_info, booking[2], booking[3]))

    def get_flight_info(self, flight_id):
        """Fetches flight information based on the flight_id."""
        self.cursor.execute("SELECT airline, departure, arrival FROM flights WHERE id = %s", (flight_id,))
        flight = self.cursor.fetchone()
        print(f"Flight fetched: {flight}")
        if flight:
            return f"{flight[0]} ({flight[1]} - {flight[2]})"
        return "Unknown Flight"
