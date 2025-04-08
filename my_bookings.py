import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import mydb, get_logger

logger = get_logger(__name__)


class MyBookings:
    def __init__(self, parent_frame, user_id, parent=None):
        """Initialize the bookings frame"""
        self.parent = parent
        self.user_id = user_id

        self.frame_main = ctk.CTkFrame(parent_frame)
        self.frame_main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_back = ctk.CTkButton(
            self.frame_main,
            text="← Back to Dashboard",
            command=self.go_back,
            fg_color="transparent",
            border_width=1
        )
        btn_back.pack(anchor="e", pady=10)

        ctk.CTkLabel(
            self.frame_main,
            text="My Bookings",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.create_bookings_table()
        self.load_bookings()

    def create_bookings_table(self):
        """Create the bookings display table"""
        style = ttk.Style()

        style.configure("Treeview",
                        rowheight=30,
                        font=("Helvetica", 10),
                        background="#2e2e2e",  # Dark grey background
                        foreground="white")  # White text
        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, "bold"),
                        background="#3c3c3c",  # Dark grey header background
                        foreground="grey")  #header text
        style.map("Treeview",
                  background=[('selected', '#555555')])  # Change selected row color

        columns = [
            ("Flight", 150),
            ("Departure", 120),
            ("From", 120),
            ("To", 120),
            ("Status", 100)
        ]

        self.tree = ttk.Treeview(
            self.frame_main,
            columns=[col[0] for col in columns],
            show="headings",
            height=10,
            selectmode="browse"
        )

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center", minwidth=50)

        self.tree.tag_configure("empty", background="#2e2e2e")  # Ensure empty columns are dark as well

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
                    b.status
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
                    booking["status"]
                ))

        except Exception as e:
            logger.error(f"Error loading bookings: {e}")
            messagebox.showerror("Error", "Failed to load bookings")

    def go_back(self):
        """Return to the dashboard"""
        if self.parent:
            self.parent.show_home_view()