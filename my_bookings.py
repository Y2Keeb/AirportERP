import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import mydb, get_logger

logger = get_logger(__name__)


class MyBookings:
    def __init__(self, parent_frame, user_id, parent=None):
        """Initialize the bookings frame"""
        self.parent = parent  # Reference to UserScreen
        self.user_id = user_id

        # Main frame
        self.frame_main = ctk.CTkFrame(parent_frame)
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        # Back button
        btn_back = ctk.CTkButton(
            self.frame_main,
            text="← Back to Dashboard",
            command=self.go_back,
            fg_color="transparent",
            border_width=1
        )
        btn_back.pack(anchor="nw", pady=10)

        # Title
        ctk.CTkLabel(
            self.frame_main,
            text="My Bookings",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Treeview for bookings
        self.create_bookings_table()
        self.load_bookings()

    def create_bookings_table(self):
        """Create the bookings display table"""
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        columns = [
            ("Flight", 150),
            ("Departure", 120),
            ("From", 120),
            ("To", 120),
            ("Status", 100),
            ("Booking Date", 120)
        ]

        self.tree = ttk.Treeview(
            self.frame_main,
            columns=[col[0] for col in columns],
            show="headings",
            height=10,
            selectmode="none"
        )

        # Configure columns
        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame_main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_bookings(self):
        """Fetch and display bookings from database"""
        try:
            cursor = mydb.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    b.id,
                    f.airline as flight,
                    f.departure,
                    f.from_location,
                    f.to_location,
                    b.status,
                    DATE_FORMAT(b.booking_date, '%%Y-%%m-%%d') as booking_date
                FROM bookings b
                JOIN flights f ON b.flight_id = f.id
                WHERE b.user_id = %s
                ORDER BY f.departure DESC
            """, (self.user_id,))

            bookings = cursor.fetchall()

            if not bookings:
                messagebox.showinfo("No Bookings", "You don't have any bookings yet.")
                return

            for booking in bookings:
                self.tree.insert("", "end", values=(
                    booking["flight"],
                    booking["departure"],
                    booking["from_location"],
                    booking["to_location"],
                    booking["status"],
                    booking["booking_date"]
                ))

        except Exception as e:
            logger.error(f"Error loading bookings: {e}")
            messagebox.showerror("Error", "Failed to load bookings")

    def go_back(self):
        """Return to the dashboard"""
        if self.parent:
            self.parent.show_home_view()