from tkcalendar import DateEntry
from basewindow import BaseWindow
import customtkinter as ctk
from tkinter import ttk,messagebox
from config import get_logger,mydb
from views.buy_additional_packages_screen import AdditionalPackageScreen

logger = get_logger(__name__)


class TicketSystem(BaseWindow):
    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, "Ticket Purchase")
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
        self._create_search_frame()
        self._create_flights_table()
        self._create_action_buttons()

    def _create_header(self):
        """Create header section with title and back button"""
        header_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Buy Tickets",
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

    def _create_search_frame(self):
        """Create search controls"""
        search_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=10)

        # From/To fields
        self.entry_from = ctk.CTkEntry(search_frame, width=150, placeholder_text="From")
        self.entry_from.insert(0, "Brussels")
        self.entry_from.grid(row=0, column=0, padx=5)

        self.entry_to = ctk.CTkEntry(search_frame, width=150, placeholder_text="To")
        self.entry_to.grid(row=0, column=2, padx=5)

        btn_swap = ctk.CTkButton(
            search_frame,
            text="↔",
            width=40,
            command=self._swap_locations
        )
        btn_swap.grid(row=0, column=1, padx=5)

        self.entry_date = DateEntry(
            search_frame,
            width=12,
            background="darkgrey",
            foreground="white",
            borderwidth=2
        )
        self.entry_date.grid(row=0, column=3, padx=5)

        btn_search = ctk.CTkButton(
            search_frame,
            text="Search Flights",
            command=self._fetch_flights
        )
        btn_search.grid(row=0, column=4, padx=5)

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
            columns=("Airline", "From", "Schedule", "To", "Price"),
            show="headings",
            height=8,
            selectmode="browse"
        )

        columns = [
            ("Airline", 150),
            ("From", 120),
            ("Schedule", 200),
            ("To", 120),
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

    def _create_action_buttons(self):
        """Create action buttons"""
        btn_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="e", pady=10)

        self.btn_book = ctk.CTkButton(
            btn_frame,
            text="Select Flight & Continue",
            command=self._navigate_to_packages,
            fg_color="#2e8b57",
            state="disabled"
        )
        self.btn_book.pack(side="right", padx=10)

    def _swap_locations(self):
        """Swap the locations in the 'From' and 'To' fields."""
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()
        self.entry_from.delete(0, "end")
        self.entry_from.insert(0, to_location)
        self.entry_to.delete(0, "end")
        self.entry_to.insert(0, from_location)

    def _fetch_flights(self):
        """Fetch flights from database with consistent formatting"""
        self.tree.delete(*self.tree.get_children())
        self.flights_data = {}

        from_loc = self.entry_from.get().strip()
        to_loc = self.entry_to.get().strip()

        try:
            query = """
                SELECT id, airline, from_location, CONCAT(departure, ' - ', arrival) as flight_schedule,to_location, price
                FROM flights 
                WHERE from_location = %s AND to_location = %s
            """
            self.cursor.execute(query, (from_loc, to_loc))

            for row in self.cursor.fetchall():
                price_str = f"{float(row['price']):.2f}" if row['price'] else "0.00"

                values = (
                    row['airline'],
                    row['from_location'],
                    row['flight_schedule'],
                    row['to_location'],
                    price_str
                )

                item_id = self.tree.insert("", "end", values=values)
                self.flights_data[item_id] = row['id']

        except Exception as e:
            logger.error(f"Flight fetch error: {str(e)}")
            messagebox.showerror("Error", "Failed to load flight data")

    def _navigate_to_packages(self):
        """Navigate to additional packages screen"""
        if self.selected_flight:
            if self.view_manager:
                self.view_manager.push_view(
                    AdditionalPackageScreen,
                    selected_flight=self.selected_flight,
                    user_id=self.user_id,
                    username=self.username
                )
            else:
                self.cleanup()
                self.view_manager.push_view(
                    AdditionalPackageScreen,
                    self.root,
                    self.view_manager,
                    self.selected_flight,
                    self.user_id,
                    username=self.username
                )
        else:
            messagebox.showwarning("Selection Required", "Please select a flight first")

    def _on_flight_select(self, event):
        """Handle flight selection event with robust error handling"""
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_flight = None
            self.btn_book.configure(state="disabled")
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
                flight_id,  # Actual DB ID (int)
                values[0],  # Airline (str)
                values[1],  # From (str)
                values[2],  # Schedule (str)
                values[3],  # To (str)
                price  # Price (float)
            )
            self.btn_book.configure(state="normal")

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
            from views.user_screen import UserScreen
            self.cleanup()
            UserScreen(self.root, user_id=self.user_id, username=self.username)

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()

