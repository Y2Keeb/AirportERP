import time

from tkcalendar import DateEntry
from basewindow import BaseWindow
import customtkinter as ctk
from tkinter import ttk,messagebox
from config import get_logger,mydb
from views.buy_additional_packages_screen import AdditionalPackageScreen

logger = get_logger(__name__)


class FlightPlannerScreen(BaseWindow):
    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, "Flight Planner")
        self.view_manager = view_manager
        self.user_id = user_id
        self.username = username
        self.selected_flight = None
        self.cursor = mydb.cursor(dictionary=True)

        self.view_state = {
            'user_id': user_id,
            'username': username
        }

        for widget in root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_rowconfigure(2, weight=1)

        self._create_header()
        self._create_flights_table()
        self._fetch_flights()

    def _create_header(self):
        """Create header section with title and back button"""
        header_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Flight Planner - Pending flights ready for planning.",
            font=("Arial", 25, "bold")
        ).pack(side="left", padx=10)

        btn_back = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            command=self._go_back,
            fg_color="transparent",
            border_width=1,
            width=100
        )
        btn_back.pack(side="right", padx=10)


    def _create_flights_table(self):
        """Create flights results table"""
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#22559b')])

        self.tree = ttk.Treeview(
            self.frame_main,
            columns=("Airline", "Departure date", "Arrival date","Departure city", "Arrival city", "Plane Type", "Total seats","Price"),
            show="headings",
            height=8,
            selectmode="browse"
        )

        columns = [
            ("Airline", 150),
            ("Departure date", 120),
            ("Arrival date", 200),
            ("Departure city", 120),
            ("Arrival city",150),
            ("Plane Type",150),
            ("Total seats",150),
            ("Price", 100)
        ]

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.frame_main,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_flight_select)

    def _fetch_flights(self):
        """Fetch flights from database with consistent formatting"""
        self.tree.delete(*self.tree.get_children())
        self.flights_data = {}


        try:
            query = """
                SELECT id, airline, from_location,to_location,plane_type,total_seats,departure,arrival, price
                FROM pending_flights 
            """
            self.cursor.execute(query)

            for row in self.cursor.fetchall():
                price_str = f"{float(row['price']):.2f}" if row['price'] else "0.00"

                values = (
                    row['airline'],
                    row['departure'],
                    row['arrival'],
                    row['from_location'],
                    row['to_location'],
                    row['plane_type'],
                    row['total_seats'],
                    price_str
                )

                item_id = self.tree.insert("", "end", values=values)
                self.flights_data[item_id] = row['id']

        except Exception as e:
            logger.error(f"Flight fetch error: {str(e)}")
            messagebox.showerror("Error", "Failed to load flight data")
    def _on_flight_select(self, event):
        """Handle flight selection event with robust error handling"""
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_flight = None
            self.btn_plan.configure(state="disabled")
            return

        try:
            values = self.tree.item(selected_items[0], 'values')
            flight_id = self.flights_data[selected_items[0]]

            print(f"Selected flight values: {values}")

            if len(values) < 5:
                raise ValueError("Incomplete flight data")

            try:
                price = float(values[4])
            except ValueError:
                price_str = ''.join(c for c in values[4] if c.isdigit() or c == '.')
                price = float(price_str) if price_str else 0.0

            self.selected_flight = (
                flight_id,
                values[0],
                values[1],
                values[2],
                values[3],
                price
            )
            self.btn_plan.configure(state="normal")

        except Exception as e:
            logger.error(f"Flight selection error: {str(e)}")
            messagebox.showerror("Error",
                                 f"Could not process flight data:\n{str(e)}")
            self.selected_flight = None
            self.btn_book.configure(state="disabled")

    def _go_back(self):
        """Handle back navigation"""
        if self.view_manager:
            self.view_manager.pop_view()
        else:
            from views.login_screen import LoginScreen
            self.cleanup()
            LoginScreen(self.root)

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()

