from tkcalendar import DateEntry
from class_GUI import BaseWindow
import customtkinter as ctk
from tkinter import ttk,messagebox
from config import get_logger,mydb
from views.buy_additional_packages_screen import AdditionalPackageScreen

logger = get_logger(__name__)

class TicketSystem(BaseWindow):
    def __init__(self, root, user_id, username):
        super().__init__(root, "Ticket Purchase")
        self.user_id = user_id
        self.username = username
        self.selected_flight_id = None
        self.cursor = mydb.cursor()


        self.view_state = {
            'user_id': user_id,
            'username': username
        }

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.pack(fill='both', expand=True)

        self.header_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.frame_search = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.frame_search.grid(row=1, column=0, sticky="ew", pady=10, padx=20)
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
            height=7)

        self._build_ui()

    def _build_ui(self):
        """Creates and positions all widgets in the UI."""
        self.frame_main.grid_rowconfigure(0, weight=0)  # Header row

        ctk.CTkLabel(
            self.header_frame, text="Buy Tickets", font=("Arial", 25, "bold")
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

        btn_back = ctk.CTkButton(self.header_frame,text="← Back to Dashboard",command=self.go_back,fg_color="transparent",border_width=1)
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
        self.tree.bind("<ButtonRelease-1>", self._on_flight_select)

        # -> Configure headings and column widths using a loop
        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)  # Set column header text
            self.tree.column(col_name, width=width)  # Set column width

        self.btn_book_ticket = ctk.CTkButton(
            self.frame_main,
            text="Select Flight & Choose Extras",
            command=self._navigate_to_packages,
            fg_color="#2e8b57",
            state="disabled"  # Disabled until flight is selected
        )
        self.btn_book_ticket.grid(row=3, column=0, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self._on_flight_select)


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

    def _navigate_to_packages(self):
        """Navigate to additional packages screen"""
        if hasattr(self, 'selected_flight') and self.selected_flight:
            self.root.view_manager.push_view(
                AdditionalPackageScreen,
                selected_flight=self.selected_flight,  # Pass the complete tuple
                user_id=self.user_id,
                username=self.username
            )
        else:
            messagebox.showwarning("Warning", "No flight selected")

    def _on_flight_select(self, event):
        """Handle flight selection event"""
        selected_items = self.tree.selection()
        if selected_items:
            values = self.tree.item(selected_items[0], 'values')
            flight_id = self.flights_data[selected_items[0]]  # Get DB ID

            self.btn_book_ticket.configure(state="normal")

            self.selected_flight = (
                flight_id,  # Actual DB ID (int)
                values[0],  # Airline (str)
                values[1],  # From (str)
                values[2],  # Departure (str)
                values[3],  # To (str)
                float(values[4])  # Price (float)
            )
        else:
            self.selected_flight = None
            self.btn_book_ticket.configure(state="disabled")

    def cleanup(self):
        if hasattr(self, 'frame_main'):
            self.frame_main.destroy()

    def go_back(self):
        self.root.view_manager.pop_view()

