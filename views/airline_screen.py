from tkinter import ttk
from tkinter import messagebox
from basewindow import BaseWindow
from config import set_theme,mydb
import customtkinter as ctk
from config import is_suspect_sql_input
from ui_helpers import show_sql_meme_popup

class AirlineScreen(BaseWindow):
    def __init__(self, root,username=None, view_manager=None):
        super().__init__(root, "Airline Dashboard")
        self.username = username
        self.user_id = self._get_user_id()
        self.view_manager = view_manager
        self.full_name = self.get_airline_name()
        self.view_state = {
            'role': 'airline'
        }
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.9, relheight=0.9)

        self.frame_form = ctk.CTkFrame(self.frame_main, border_color="black", border_width=3)
        self.frame_tree = ctk.CTkFrame(self.frame_main, border_color="black", border_width=3)

        self.lbl_greeting = ctk.CTkLabel(
            self.frame_main,
            text=f"Welcome {self.full_name}!\nAdd Available Flight Information Below.",
            font=("Arial", 20),
            justify="left"
        )
        self.lbl_greeting.place(relx=0.03, rely=0.035)
        pending_label = ctk.CTkLabel(self.frame_main, text="Current pending flights:", font=("Arial", 14, "bold"))
        pending_label.place(relx=0.53, rely=0.06)

        self.frame_form.place(relx=0.25, rely=0.50, anchor="center", relwidth=0.45, relheight=0.8)
        self.frame_tree.place(relx=0.75, rely=0.50, anchor="center", relwidth=0.45, relheight=0.8)

        self._create_pending_flights_table()
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

        self.airline_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.airline_entry.insert(0, self.full_name)
        self.from_location_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.to_location_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.departure_date_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.arrival_date_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.plane_type_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.total_seat_entry = ctk.CTkEntry(self.frame_form, width=150)
        self.price_entry = ctk.CTkEntry(self.frame_form, width=150)

        self.btn_offer_flight = ctk.CTkButton(self.frame_main, text="Offer Flight", command=self.complete_flight_offer)
        self.btn_clear_form = ctk.CTkButton(self.frame_main, text="Clear", command=self.clear_form)

        self.create_widgets()

    def refresh_flight_list(self):
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

    def _create_pending_flights_table(self):
        """Styled Treeview for showing pending flights"""
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
        fields = [
            ("Airline:", self.airline_entry),
            ("From Location:", self.from_location_entry),
            ("To Location:", self.to_location_entry),
            ("Departure date (YYYY-MM-DD):", self.departure_date_entry),
            ("Arrival date (YYYY-MM-DD):", self.arrival_date_entry),
            ("Plane Type:", self.plane_type_entry),
            ("Total Seats:", self.total_seat_entry),
            ("Price:", self.price_entry),
        ]

        for row, (label_text, entry_widget) in enumerate(fields, start=1):
            label = ctk.CTkLabel(self.frame_form, text=label_text)
            label.grid(row=row, column=0, padx=(30, 15), pady=(35,15), sticky="e")
            entry_widget.grid(row=row, column=1, padx=15, pady=(35,15), sticky="ew")

        self.btn_offer_flight.place(relx=0.30, rely=0.96, anchor="se")
        self.btn_clear_form.place(relx=0.47, rely=0.96, anchor="se")

    def get_airline_name(self):
        cursor = mydb.cursor()
        cursor.execute("SELECT concat(first_name,' ',last_name) FROM users WHERE id =%s", (self._get_user_id(),))
        result = cursor.fetchone()
        return result[0] if result else None

    def _get_user_id(self):
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
        to_location = self.to_location_entry.get()
        from_location = self.from_location_entry.get()
        departure_date = self.departure_date_entry.get()
        arrival_date = self.arrival_date_entry.get()
        plane_type = self.plane_type_entry.get()
        total_seats = self.total_seat_entry.get()
        price = self.price_entry.get()

        user_inputs = [to_location,from_location, departure_date, arrival_date,
        plane_type, total_seats, price
    ]
        if any(is_suspect_sql_input(value) for value in user_inputs):
            show_sql_meme_popup(self.root)
            return

        try:
            cursor = mydb.cursor()
            cursor.execute(
                "INSERT INTO pending_flights (airline, departure, arrival, status, plane_type,total_seats,price,from_location,to_location,submitted_by,submitted_at) "
                "VALUES (%s, %s,%s,'pending',%s,%s,%s,%s,%s,%s, NOW())",
                (self.full_name,departure_date,arrival_date,plane_type,total_seats,price,from_location,to_location,self._get_user_id())
    )
            mydb.commit()
            cursor.close()
            messagebox.showinfo("Success", "Flight offered to airport!")
            self.refresh_flight_list()
        except Exception as e:
            messagebox.showinfo("Error", "An error occured")

    def clear_form(self):
        self.from_location_entry.delete(0, 'end')
        self.to_location_entry.delete(0, 'end')
        self.departure_date_entry.delete(0, 'end')
        self.arrival_date_entry.delete(0, 'end')
        self.plane_type_entry.delete(0, 'end')
        self.total_seat_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')

    def logout(self):
        """Simplified logout to login screen"""
        self.cleanup()

        for widget in self.root.winfo_children():
            widget.destroy()

        from views.login_screen import LoginScreen
        LoginScreen(self.root, view_manager=self.view_manager)
