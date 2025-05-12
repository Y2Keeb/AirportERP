from tkinter import ttk,messagebox
import customtkinter as ctk

from basewindow import BaseWindow
from config import is_suspect_sql_input,set_theme,mydb
from ui_helpers import show_sql_meme_popup

class AirlineScreen(BaseWindow):
    def __init__(self, root,username=None, view_manager=None):
        super().__init__(root, "Airline Dashboard")
        """
           Initialize the AirlineScreen for a specific user.
           Sets up UI frames, retrieves user info, and prepares the dashboard interface.
        """
        self.username = username
        self.user_id = self.get_user_id()
        self.full_name = self.get_airline_name()
        self.view_manager = view_manager
        self.view_state = {
            'role': 'airline'
        }
        self.tree = None
        self.create_menu_bar(["help", "about","exit","logout"])

        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.9, relheight=0.9)
        self.frame_form = ctk.CTkFrame(self.frame_main, border_color="black", border_width=3)
        self.frame_tree = ctk.CTkFrame(self.frame_main, border_color="black", border_width=3)

        self.lbl_greeting = ctk.CTkLabel(self.frame_main,text=f"Welcome {self.full_name}!\nAdd Available Flight Information Below.",justify="left")
        self.lbl_greeting.place(relx=0.03, rely=0.035)

        lbl_pending_text = ctk.CTkLabel(self.frame_main, text="Current pending flights:", font=("Arial", 14, "bold"))
        lbl_pending_text.place(relx=0.53, rely=0.06)

        self.frame_form.place(relx=0.25, rely=0.50, anchor="center", relwidth=0.45, relheight=0.8)
        self.frame_tree.place(relx=0.75, rely=0.50, anchor="center", relwidth=0.45, relheight=0.8)

        self.create_pending_flights_table()
        self.refresh_flight_list()
        set_theme()

        self.lbl_airline = ctk.CTkLabel(self.frame_form, text="Airline: ")
        self.lbl_from_location = ctk.CTkLabel(self.frame_form, text="From Location: ")
        self.lbl_to_location = ctk.CTkLabel(self.frame_form, text="To Location: ")
        self.lbl_departure_date = ctk.CTkLabel(self.frame_form, text="Departure date (YYYY-MM-DD): ")
        self.lbl_arrival_date = ctk.CTkLabel(self.frame_form, text="Arrival date (YYYY-MM-DD): ")
        self.lbl_plane_type = ctk.CTkLabel(self.frame_form, text="Plane Type: ")
        self.lbl_total_seats = ctk.CTkLabel(self.frame_form, text="Total Seats: ")
        self.lbl_price = ctk.CTkLabel(self.frame_form, text="Price: ")

        self.entry_airline = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_airline.insert(0, self.full_name)
        self.entry_from_location = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_to_location = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_departure_date = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_arrival_date = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_plane_type = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_total_seat = ctk.CTkEntry(self.frame_form, width=150)
        self.entry_price = ctk.CTkEntry(self.frame_form, width=150)

        self.btn_offer_flight = ctk.CTkButton(self.frame_main, text="Offer Flight", command=self.complete_flight_offer)
        self.btn_clear_form = ctk.CTkButton(self.frame_main, text="Clear", command=self.clear_form)

        self.create_widgets()

    def refresh_flight_list(self):
        """
         Refresh the right-side TreeView with pending flights offered by this airline.
         Fetches data from the database and repopulates the table.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = mydb.cursor()
        cursor.execute("""
            SELECT departure, arrival, submitted_at, from_location, to_location, price
            FROM pending_flights
            WHERE submitted_by = %s AND status = 'pending'
            ORDER BY submitted_at DESC
        """, (self.user_id,))
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
        cursor.close()

    def create_pending_flights_table(self):
        """
         Creates a styled TreeView widget with a vertical scrollbar to display
         the airline's pending flights.
        """
        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",
                        rowheight=30,
                        font=("Helvetica", 10),
                        background="#2e2e2e",
                        foreground="white",
                        fieldbackground="#2e2e2e")

        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, "bold"),
                        background="#3c3c3c",
                        foreground="white")

        style.map("Treeview",
                  background=[('selected', '#555555')])

        columns = [
            ("Departure", 100),
            ("Arrival", 100),
            ("Submitted", 120),
            ("From", 100),
            ("To", 100),
            ("Price", 80)
        ]

        self.tree = ttk.Treeview(
            self.frame_tree,
            columns=[col[0] for col in columns],
            show="headings",
            height=15,
            selectmode="browse"
        )

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

    def create_widgets(self):
        """
          Layout the flight offer form on the left side of the screen, including labels,
          entry fields, and action buttons (Offer Flight and Clear).
        """
        fields = [
            ("Airline:", self.entry_airline),
            ("From Location:", self.entry_from_location),
            ("To Location:", self.entry_to_location),
            ("Departure date (YYYY-MM-DD):", self.entry_departure_date),
            ("Arrival date (YYYY-MM-DD):", self.entry_arrival_date),
            ("Plane Type:", self.entry_plane_type),
            ("Total Seats:", self.entry_total_seat),
            ("Price:", self.entry_price),
        ]

        for row, (label_text, entry_widget) in enumerate(fields, start=1):
            label = ctk.CTkLabel(self.frame_form, text=label_text)
            label.grid(row=row, column=0, padx=(30, 15), pady=(35,15), sticky="e")
            entry_widget.grid(row=row, column=1, padx=15, pady=(35,15), sticky="ew")

        self.btn_offer_flight.place(relx=0.30, rely=0.96, anchor="se")
        self.btn_clear_form.place(relx=0.47, rely=0.96, anchor="se")

    def get_airline_name(self):
        """
           Query the database for the full name of the airline user based on user ID.
           Returns the full name as a string.
        """
        cursor = mydb.cursor()
        cursor.execute("SELECT concat(first_name,' ',last_name) FROM users WHERE id =%s", (self.get_user_id(),))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_user_id(self):
        """
            Internal helper to get the user ID for the current username.
            Returns the user ID as an integer or None if not found.
        """
        cursor = None
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def complete_flight_offer(self):
        """
         Gathers form input and inserts a new flight into the 'pending_flights' table.
         - Prevents SQL injection using a validation helper.
         - Prevents duplicates based on key flight info.
         - Displays success or error messages as needed.
        """
        to_location = self.entry_to_location.get()
        from_location = self.entry_from_location.get()
        departure_date = self.entry_departure_date.get()
        arrival_date = self.entry_arrival_date.get()
        plane_type = self.entry_plane_type.get()
        total_seats = self.entry_total_seat.get()
        price = self.entry_price.get()

        user_inputs = [to_location,from_location, departure_date, arrival_date,
        plane_type, total_seats, price]

        if any(is_suspect_sql_input(value) for value in user_inputs):
            show_sql_meme_popup(self.root)
            return

        try:
            cursor = mydb.cursor()
            cursor.execute("""
                       SELECT id FROM pending_flights
                       WHERE airline = %s AND departure = %s AND arrival = %s AND from_location = %s AND to_location = %s
                   """, (self.full_name, departure_date, arrival_date, from_location, to_location))

            if cursor.fetchone():
                messagebox.showinfo("Duplicate", "This flight already exists in pending flights.")
                cursor.close()
                return

            cursor.execute(
                "INSERT INTO pending_flights (airline, departure, arrival, status, plane_type,total_seats,price,from_location,to_location,submitted_by,submitted_at) "
                "VALUES (%s, %s,%s,'pending',%s,%s,%s,%s,%s,%s, NOW())",
                (self.full_name,departure_date,arrival_date,plane_type,total_seats,price,from_location,to_location,self.get_user_id())
    )
            mydb.commit()
            cursor.close()
            messagebox.showinfo("Success", "Flight offered to airport!")
            self.refresh_flight_list()
        except Exception as e:
            messagebox.showinfo("Error", "An error occurred")

    def clear_form(self):
        """
        Clears all input fields in the flight offer form.
        Useful after a successful submission or reset.
        """
        self.entry_from_location.delete(0, 'end')
        self.entry_to_location.delete(0, 'end')
        self.entry_departure_date.delete(0, 'end')
        self.entry_arrival_date.delete(0, 'end')
        self.entry_plane_type.delete(0, 'end')
        self.entry_total_seat.delete(0, 'end')
        self.entry_price.delete(0, 'end')

    def logout(self):
        """Proper logout that clears everything and shows login screen"""
        try:
            for widget in self.root.winfo_children():
                widget.destroy()

            from views.login_screen import LoginScreen
            login_screen = LoginScreen(self.root, view_manager=self.view_manager)
            login_screen.load_view_content()

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error during logout: {e}")
            self.root.destroy()
            import os
            os.system("python main.py")