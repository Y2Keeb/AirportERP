import time
from tkinter import ttk,messagebox
import customtkinter as ctk
import PIL
from PIL import Image
from tkcalendar import DateEntry
from basewindow import BaseWindow
from config import get_logger,mydb
from views.buy_additional_packages_screen import AdditionalPackageScreen

logger = get_logger(__name__)

class TicketSystem(BaseWindow):
    """
    Initialize the TicketSystem view.
    """
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

        self.original_bg_image = PIL.Image.open("docs/icons/background2.png").convert("RGBA")
        startup_image = self.original_bg_image.resize((1600, 950), Image.NEAREST)
        self.bg_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image, size=(1600, 950))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_main = ctk.CTkFrame(root,fg_color="gray11")
        self.frame_main.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.92)

        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_rowconfigure(2, weight=1)

        self.create_menu_bar(["help","logout"])
        self.menu_bar.lift()

        self.create_header()
        self.create_search_frame()
        self.create_flights_table()
        self.create_action_buttons()

    def create_header(self):
        """Create header section with title and back button"""
        header_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Buy Tickets",
            font=("Arial", 25, "bold")
        ).pack(side="left", padx=20,pady=(20,3))

        btn_back = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            command=self.go_back,
            fg_color="transparent",
            border_width=1,
            width=100
        )
        btn_back.pack(side="right", pady=(20,20),padx=20)

    def create_search_frame(self):
        """
        Create the search interface for flights, including:
        - From/To location entries
        - A date picker
        - A 'Show all dates' checkbox
        - A 'Search Flights' button
        """
        search_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=20,pady=20)

        self.entry_from = ctk.CTkEntry(search_frame, width=150, placeholder_text="From")
        self.entry_from.insert(0, "Brussels")
        self.entry_from.grid(row=0, column=0, padx=5)

        self.entry_to = ctk.CTkEntry(search_frame, width=150, placeholder_text="To")
        self.entry_to.grid(row=0, column=2, padx=5)

        btn_swap = ctk.CTkButton(
            search_frame,
            text="↔",
            width=40,
            command=self.swap_locations
        )
        btn_swap.grid(row=0, column=1, padx=5)

        self.entry_date = DateEntry(
            search_frame,
            width=12,
            background="darkgrey",
            foreground="white",
            borderwidth=2
        )
        self.entry_date.grid(row=0, column=3, padx=(10,10))

        self.lbl_or = ctk.CTkLabel(search_frame,text="or")
        self.lbl_or.grid(row=0, column=4, padx=(10,10))


        self.var_show_all_dates = ctk.BooleanVar(value=False)
        self.chk_all_dates = ctk.CTkCheckBox(
            search_frame,
            text="Show all dates",
            variable=self.var_show_all_dates
        )
        self.chk_all_dates.grid(row=0, column=5, padx=(10,10))

        btn_search = ctk.CTkButton(
            search_frame,
            text="Search Flights",
            command=self.fetch_flights
        )
        btn_search.grid(row=0, column=6, padx=(10,10))

    def create_flights_table(self):
        """
        Set up the Treeview to display the list of flights, with custom styling,
        scrollbars, and a selection event handler.
        """
        style = ttk.Style()
        style.theme_use('default')

        # ROW STYLE
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e",
                        rowheight=30,
                        font=('Arial', 14)
                        )
        # HEADER STYLE
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Arial', 15, 'bold')
                        )
        # SELECTED ROW STYLE
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

        self.tree.bind("<<TreeviewSelect>>", self.on_flight_select)

    def create_action_buttons(self):
        """
        Create the 'Select Flight & Continue' button to move to the next step
        after a flight is selected.
        """
        btn_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="e", pady=10)

        self.btn_book = ctk.CTkButton(
            btn_frame,
            text="Select Flight & Continue",
            command=self.navigate_to_packages,
            fg_color="#2e8b57",
            state="disabled"
        )
        self.btn_book.pack(side="right", padx=10)

    def swap_locations(self):
        """Swap the locations in the 'From' and 'To' fields."""
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()
        self.entry_from.delete(0, "end")
        self.entry_from.insert(0, to_location)
        self.entry_to.delete(0, "end")
        self.entry_to.insert(0, from_location)

    def fetch_flights(self):
        """
        Fetch available flights from the database based on the selected
        departure location, arrival location, and date (unless 'Show all dates'
        is checked).

        Populates the Treeview with search results.
        Displays error message on failure.
        """
        self.tree.delete(*self.tree.get_children())
        self.flights_data = {}

        from_loc = self.entry_from.get().strip()
        to_loc = self.entry_to.get().strip()
        selected_date = self.entry_date.get_date()

        try:
            if self.var_show_all_dates.get():
                query = """
                    SELECT id, airline, from_location,
                           CONCAT(departure, ' - ', arrival) AS flight_schedule,
                           to_location, price
                    FROM flights 
                    WHERE from_location = %s AND to_location = %s
                """
                params = (from_loc, to_loc)
            else:
                selected_date = self.entry_date.get_date()
                query = """
                    SELECT id, airline, from_location,
                           CONCAT(departure, ' - ', arrival) AS flight_schedule,
                           to_location, price
                    FROM flights 
                    WHERE from_location = %s AND to_location = %s
                      AND DATE(departure) = %s
                """
                params = (from_loc, to_loc, selected_date)

            self.cursor.execute(query, params)

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

    def navigate_to_packages(self):
        """
        Navigate to the 'AdditionalPackageScreen' after a flight is selected.
        Ensures a flight is selected before proceeding.

        Passes flight and user data to the next screen.
        """
        time.sleep(0.1)

        if not self.selected_flight:
            messagebox.showwarning("Selection Required", "Please select a flight first")
            return

        try:
            params = {
                'selected_flight': self.selected_flight,
                'user_id': self.user_id,
                'username': self.username,
                'package_price': 0
            }

            if self.view_manager:
                self.view_manager.push_view(AdditionalPackageScreen, **params)
            else:
                self.cleanup()
                AdditionalPackageScreen(
                    root=self.root,
                    view_manager=self.view_manager,
                    **params
                )
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            messagebox.showerror("Error", f"Failed to navigate: {str(e)}")

    def on_flight_select(self, event):
        """
        Handle Treeview flight selection by parsing the selected row
        and enabling the continue button.

        Validates and formats price, and stores flight data in memory.
        Displays error message if parsing fails.
        """
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
                flight_id,
                values[0],
                values[1],
                values[2],
                values[3],
                price
            )
            self.btn_book.configure(state="normal")

        except Exception as e:
            logger.error(f"Flight selection error: {str(e)}")
            messagebox.showerror("Error",
                                 f"Could not process flight data:\n{str(e)}")
            self.selected_flight = None
            self.btn_book.configure(state="disabled")

    def go_back(self):
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

    def logout(self):
        """logout that clears everything and shows login screen"""
        try:
            for widget in self.root.winfo_children():
                widget.destroy()

            from views.kiosk_screen import KioskLoginScreen
            kiosk_login_screen = KioskLoginScreen(self.root, view_manager=self.view_manager)

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error during logout: {e}")
            self.root.destroy()
            import os
            os.system("python main.py")