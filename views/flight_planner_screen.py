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
        self.frame_main.pack(fill="both", expand=True)

        self.frame_main.grid_columnconfigure(1, weight=1)  # Make right side expandable
        self.frame_main.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.frame_main, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.right_frame = ctk.CTkFrame(self.frame_main)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_rowconfigure(1, weight=1)  # Let treeview expand
        self.right_frame.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_flights_table()
        self._fetch_flights()

    def _create_header(self):
        """Create header section with title and back button"""

        ctk.CTkLabel(self.right_frame,text="Flight Planner - Pending flights ready for planning.",font=("Arial", 25, "bold")).pack(side="left", padx=10)
        btn_pending_flights = ctk.CTkButton(self.sidebar_frame, text="Browse Pending Flights").pack(pady=(10, 5), fill='x', padx=10)
        btn_planned_flights = ctk.CTkButton(self.sidebar_frame, text="Browse Planned Flights").pack(pady=5, fill='x', padx=10)

        btn_back = ctk.CTkButton(self.right_frame,text="← Back to Dashboard",command=self._go_back,fg_color="transparent",border_width=1,width=100)
        btn_back.pack(side="right", padx=10)

        # Checkboxes for fields
        self.column_options = {
            "Airline": ctk.BooleanVar(value=True),
            "Departure date": ctk.BooleanVar(value=True),
            "Arrival date": ctk.BooleanVar(value=True),
            "Departure city": ctk.BooleanVar(value=True),
            "Arrival city": ctk.BooleanVar(value=True),
            "Plane Type": ctk.BooleanVar(value=True),
            "Total seats": ctk.BooleanVar(value=True),
            "Price": ctk.BooleanVar(value=True),
        }

        lbl_visible_fields = ctk.CTkLabel(self.sidebar_frame, text="Visible Fields:", anchor="w").pack(pady=(20, 5), padx=10)

        for field, var in self.column_options.items():
            ctk.CTkCheckBox(
                self.sidebar_frame,
                text=field,
                variable=var,
                command=self._refresh_treeview_columns
            ).pack(anchor='w', padx=10)

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

        self.tree = ttk.Treeview(self.right_frame, show="headings", selectmode="browse")
        self.tree.grid(row=1, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_flight_select)
        self._refresh_treeview_columns()

    def _refresh_treeview_columns(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = []
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)

        visible_cols = [col for col, var in self.column_options.items() if var.get()]
        self.tree["columns"] = visible_cols

        for col in visible_cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self._fetch_flights()

    def _fetch_flights(self):
        self.tree.delete(*self.tree.get_children())
        self.flights_data = {}

        try:
            self.cursor.execute("""
                SELECT id, airline, departure, arrival, from_location, to_location,
                       plane_type, total_seats, price
                FROM pending_flights
            """)
            for row in self.cursor.fetchall():
                all_data = {
                    "Airline": row["airline"],
                    "Departure date": row["departure"],
                    "Arrival date": row["arrival"],
                    "Departure city": row["from_location"],
                    "Arrival city": row["to_location"],
                    "Plane Type": row["plane_type"],
                    "Total seats": row["total_seats"],
                    "Price": f"{float(row['price']):.2f}" if row['price'] else "0.00",
                }

                values = [all_data[col] for col in self.tree["columns"]]
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

