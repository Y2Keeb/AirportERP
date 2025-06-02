from datetime import date
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
import PIL
from PIL import Image
from basewindow import BaseWindow
from config import get_logger, mydb, is_suspect_sql_input
from ui_helpers import show_sql_meme_popup

logger = get_logger(__name__)


class FlightPlannerScreen(BaseWindow):
    """
    A UI screen for planning flights.
    Allows staff members/flight planners to browse, filter, and manage both pending and planned flights.
    Supports selecting flights, viewing flight details, planning flights by assigning gates,
    and deleting pending flights.
    """

    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, "Flight Planner")

        self.view_manager = view_manager
        self.user_id = user_id
        self.username = username
        self.selected_flight = None
        self.cursor = mydb.cursor(dictionary=True)
        self.current_view_mode = "pending"
        self.departure_date_filter = None

        self.view_state = {"user_id": user_id, "username": username}

        for widget in root.winfo_children():
            widget.destroy()

        self.original_bg_image = PIL.Image.open("docs/icons/background.jpg").convert(
            "RGBA"
        )
        startup_image = self.original_bg_image.resize((1600, 950), Image.NEAREST)
        self.bg_image = ctk.CTkImage(
            light_image=startup_image, dark_image=startup_image, size=(1600, 950)
        )
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_menu_bar(["exit", "logout"])

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.place(
            relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.92
        )
        self.frame_main.grid_columnconfigure(1, weight=1)
        self.frame_main.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.frame_main, width=230)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.right_frame = ctk.CTkFrame(self.frame_main)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)  # Header
        self.right_frame.grid_rowconfigure(1, weight=1)  # TreeView
        self.right_frame.grid_rowconfigure(2, weight=0)  # Buttons
        self.right_frame.grid_rowconfigure(3, weight=0)  # Entry field (Gate)

        self.airline_filter_var = ctk.StringVar(value="All Airlines")
        self.departure_filter_var = ctk.StringVar(value="All Departures")
        self.arrival_filter_var = ctk.StringVar(value="All Arrivals")
        self.plane_filter_var = ctk.StringVar(value="All Plane Types")
        self.departure_date_var = ctk.StringVar(value="")

        self.create_header()
        self.create_flights_table()
        self.fetch_flights_with_filters()
        self.menu_bar.lift()

    def create_header(self):
        """
        Create the header section with title, filters, checkboxes, and buttons.
        Includes airline, departure, arrival, plane type, and date filters,
        plus options to toggle column visibility and reset filters.
        """
        self.title_label = ctk.CTkLabel(
            self.right_frame,
            text="Flight Planner - Pending flights ready for planning.",
            font=("Arial", 25, "bold"),
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(2, 60))

        self.filter_frame = ctk.CTkFrame(self.right_frame)
        self.filter_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(35, 5))

        self.filter_frame.grid_columnconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(1, weight=1)

        self.airline_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.airline_filter_var,
            command=self.on_filter_change,
            values=["All Airlines"],
            width=200,
        )
        self.airline_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.departure_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.departure_filter_var,
            command=self.on_filter_change,
            values=["All Departures"],
            width=200,
        )
        self.departure_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.arrival_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.arrival_filter_var,
            command=self.on_filter_change,
            values=["All Arrivals"],
            width=200,
        )
        self.arrival_dropdown.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.plane_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.plane_filter_var,
            command=self.on_filter_change,
            values=["All Plane Types"],
            width=200,
        )
        self.plane_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        date_label = ctk.CTkLabel(self.filter_frame, text="Departure Date:")
        date_label.grid(row=0, column=4, padx=(20, 0), pady=5, sticky="e")

        self.departure_date_picker = DateEntry(
            self.filter_frame,
            textvariable=self.departure_date_var,
            width=16,
            background="grey",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
        )
        self.departure_date_picker.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.departure_date_picker.bind(
            "<<DateEntrySelected>>", lambda e: self.on_filter_change()
        )
        self.refresh_filter_options()

        self.btn_pending_flights = ctk.CTkButton(
            self.sidebar_frame,
            text="Browse Pending Flights",
            command=lambda: self.switch_view_mode("pending"),
        )
        self.btn_pending_flights.pack(pady=(50, 15), fill="x", padx=10)

        self.btn_planned_flights = ctk.CTkButton(
            self.sidebar_frame,
            text="Browse Planned Flights",
            command=lambda: self.switch_view_mode("planned"),
        )
        self.btn_planned_flights.pack(pady=(15, 15), fill="x", padx=10)

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

        lbl_visible_fields = ctk.CTkLabel(
            self.sidebar_frame, text="Visible Fields:", anchor="w"
        ).pack(pady=(20, 5), padx=10)

        for field, var in self.column_options.items():
            ctk.CTkCheckBox(
                self.sidebar_frame,
                text=field,
                variable=var,
                command=self.refresh_treeview_columns,
            ).pack(anchor="w", padx=10, pady=(7, 7))

        self.btn_select_all_filters = ctk.CTkButton(
            self.sidebar_frame, text="Select All Fields", command=self.select_all_fields
        )
        self.btn_select_all_filters.pack(anchor="w", padx=10, pady=(20, 20))

        clear_btn = ctk.CTkButton(
            self.filter_frame,
            text="Clear Filters",
            command=self.clear_filters,
            width=100,
        )
        clear_btn.grid(row=0, column=6, padx=(100, 5), pady=5, sticky="e")
        self.departure_date_var.set("")

        self.update_button_styles()

    def select_all_fields(self):
        """
        Select all checkbox fields to display all available columns in the flight table.
        """
        for var in self.column_options.values():
            var.set(True)
        self.refresh_treeview_columns()

    def clear_filters(self):
        """
        Reset all filter dropdowns and date fields to their default values and refresh results.
        """
        self.airline_filter_var.set("All Airlines")
        self.departure_filter_var.set("All Departures")
        self.arrival_filter_var.set("All Arrivals")
        self.plane_filter_var.set("All Plane Types")
        self.departure_date_var.set("")
        self.fetch_flights_with_filters()

    def refresh_filter_options(self):
        """
        Update the dropdown filter options dynamically based on the current flight view mode.
        Fetches distinct values from the database for airlines, locations, and plane types.
        """
        try:
            table_name = (
                "pending_flights" if self.current_view_mode == "pending" else "flights"
            )

            self.cursor.execute(
                f"SELECT DISTINCT airline FROM {table_name} ORDER BY airline"
            )
            airlines = ["All Airlines"] + [
                row["airline"] for row in self.cursor.fetchall()
            ]
            self.airline_dropdown.configure(values=airlines)

            self.cursor.execute(
                f"SELECT DISTINCT from_location FROM {table_name} ORDER BY from_location"
            )
            departures = ["All Departures"] + [
                row["from_location"] for row in self.cursor.fetchall()
            ]
            self.departure_dropdown.configure(values=departures)

            self.cursor.execute(
                f"SELECT DISTINCT to_location FROM {table_name} ORDER BY to_location"
            )
            arrivals = ["All Arrivals"] + [
                row["to_location"] for row in self.cursor.fetchall()
            ]
            self.arrival_dropdown.configure(values=arrivals)

            self.cursor.execute(
                f"SELECT DISTINCT plane_type FROM {table_name} ORDER BY plane_type"
            )
            planes = ["All Plane Types"] + [
                row["plane_type"] for row in self.cursor.fetchall()
            ]
            self.plane_dropdown.configure(values=planes)

        except Exception as e:
            logger.error(f"Failed to load filter options: {str(e)}")
            messagebox.showerror("Error", "Failed to load filter options")

    def create_flights_table(self):
        """
        Create the TreeView table for displaying flight data, with style customization and a scrollbar.
        Also sets up selection event handling and an info frame for displaying details of the selected flight.
        """
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            rowheight=25,
        )
        style.configure(
            "Treeview.Heading",
            background="#3b3b3b",
            foreground="white",
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#22559b")])

        self.tree = ttk.Treeview(self.right_frame, show="headings", selectmode="browse")
        self.tree.grid(row=1, column=0, sticky="nsew")

        self.flight_info_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.flight_info_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        self.scrollbar = ttk.Scrollbar(
            self.right_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_flight_select)
        self.refresh_treeview_columns()

    def refresh_treeview_columns(self):
        """
        Update the TreeView columns based on selected checkboxes and fetch new flight data.
        """
        self.tree.delete(*self.tree.get_children())
        visible_cols = [col for col, var in self.column_options.items() if var.get()]
        self.tree["columns"] = visible_cols

        for col in visible_cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.fetch_flights_with_filters()

    def fetch_flights_with_filters(self):
        """
        Fetch flight data from the database using currently selected filters.

        Applies filters such as airline, locations, plane type, and departure date.
        Displays results in the TreeView and stores corresponding flight IDs.
        """
        self.tree.delete(*self.tree.get_children())
        self.flights_data = {}

        try:
            table_name = (
                "pending_flights" if self.current_view_mode == "pending" else "flights"
            )

            query = f"""
                SELECT id, airline, departure, arrival, from_location, 
                       to_location, plane_type, total_seats, price
                FROM {table_name}
                WHERE 1=1
            """
            params = []

            if self.airline_filter_var.get() != "All Airlines":
                query += " AND airline = %s"
                params.append(self.airline_filter_var.get())

            if self.departure_filter_var.get() != "All Departures":
                query += " AND from_location = %s"
                params.append(self.departure_filter_var.get())

            if self.arrival_filter_var.get() != "All Arrivals":
                query += " AND to_location = %s"
                params.append(self.arrival_filter_var.get())

            if self.plane_filter_var.get() != "All Plane Types":
                query += " AND plane_type = %s"
                params.append(self.plane_filter_var.get())

            selected_date_str = self.departure_date_var.get()
            if selected_date_str:
                query += " AND DATE(departure) = %s"
                params.append(selected_date_str)

            self.cursor.execute(query, tuple(params) if params else ())

            for row in self.cursor.fetchall():
                all_data = {
                    "Airline": row["airline"],
                    "Departure date": row["departure"],
                    "Arrival date": row["arrival"],
                    "Departure city": row["from_location"],
                    "Arrival city": row["to_location"],
                    "Plane Type": row["plane_type"],
                    "Total seats": row["total_seats"],
                    "Price": f"{float(row['price']):.2f}" if row["price"] else "0.00",
                }

                values = [all_data[col] for col in self.tree["columns"]]
                item_id = self.tree.insert("", "end", values=values)
                self.flights_data[item_id] = row["id"]

        except Exception as e:
            logger.error(f"Flight fetch with filters error: {str(e)}")
            messagebox.showerror("Error", "Failed to load filtered flight data")

    def on_flight_select(self, event):
        """
        Handle selection of a flight from the TreeView.

        Displays flight information, allows gate entry, and shows buttons for planning or canceling.
        Only applies to pending flights.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_flight = None
            return

        if self.current_view_mode != "pending":
            self.selected_flight = None
            for widget in self.flight_info_frame.winfo_children():
                widget.destroy()
            return
        try:
            item_id = selected_items[0]
            values = self.tree.item(item_id, "values")
            flight_id = self.flights_data[item_id]
            visible_columns = self.tree["columns"]

            if len(values) != len(visible_columns):
                raise ValueError("Mismatch between columns and values")

            flight_info = dict(zip(visible_columns, values))

            airline = flight_info.get("Airline", "Unknown")
            departure = flight_info.get("Departure date", "Unknown")
            arrival = flight_info.get("Arrival date", "Unknown")
            from_city = flight_info.get("Departure city", "Unknown")
            to_city = flight_info.get("Arrival city", "Unknown")
            price_str = flight_info.get("Price", "0.00")

            try:
                price = float("".join(c for c in price_str if c.isdigit() or c == "."))
            except:
                price = 0.00

            self.selected_flight = (
                flight_id,
                airline,
                departure,
                arrival,
                from_city,
                to_city,
                price,
            )

            for widget in self.flight_info_frame.winfo_children():
                widget.destroy()

            summary_text = (
                f"✈ Airline: {airline}\n"
                f"📅 Departure: {departure} → Arrival: {arrival}\n"
                f"🌍 From: {from_city} → To: {to_city}\n"
                f"💺 Price: {price:.2f} EUR"
            )
            summary_label = ctk.CTkLabel(
                self.flight_info_frame,
                text=summary_text,
                justify="left",
                font=("Arial", 14),
            )
            summary_label.pack(anchor="w", padx=10, pady=(0, 5))

            gate_frame = ctk.CTkFrame(self.flight_info_frame, fg_color="transparent")
            gate_frame.pack(fill="x", padx=10, pady=(0, 5))
            ctk.CTkLabel(gate_frame, text="Gate:", width=50).pack(side="left")
            self.gate_entry = ctk.CTkEntry(gate_frame, placeholder_text="e.g. A12")
            self.gate_entry.pack(side="left", padx=5)

            button_frame = ctk.CTkFrame(self.flight_info_frame, fg_color="transparent")
            button_frame.pack(fill="x", padx=10, pady=(10, 0))
            self.btn_plan = ctk.CTkButton(
                button_frame, text="Plan Flight", command=self.plan_flight
            )
            self.btn_plan.pack(side="left", padx=(0, 10))
            self.btn_cancel = ctk.CTkButton(
                button_frame,
                text="Delete Flight",
                fg_color="red",
                command=self.cancel_flight,
            )
            self.btn_cancel.pack(side="left")

        except Exception as e:
            logger.error(f"Flight selection error: {str(e)}")
            messagebox.showerror("Error", f"Could not process flight data:\n{str(e)}")
            self.selected_flight = None

    def on_filter_change(self, *args):
        """Handle changes in any filter dropdown"""
        self.fetch_flights_with_filters()

    def switch_view_mode(self, mode):
        """Switch between pending and planned flights views"""
        self.current_view_mode = mode

        if mode == "pending":
            self.title_label.configure(
                text="Flight Planner - Pending flights ready for planning."
            )
        else:
            self.title_label.configure(text="Flight Planner - Your planned flights")

        for widget in self.flight_info_frame.winfo_children():
            widget.destroy()
        self.selected_flight = None

        self.update_button_styles()
        self.refresh_filter_options()
        self.fetch_flights_with_filters()

    def update_button_styles(self):
        """Update button styles based on current view mode"""
        active_style = {"fg_color": ("#00c772", "#1f8d4b")}
        inactive_style = {"fg_color": ("gray75", "gray25")}

        if self.current_view_mode == "pending":
            self.btn_pending_flights.configure(**active_style)
            self.btn_planned_flights.configure(**inactive_style)
        else:
            self.btn_planned_flights.configure(**active_style)
            self.btn_pending_flights.configure(**inactive_style)

    def plan_flight(self):
        """
        Move a selected pending flight to the planned flights table.

        Validates input (gate), prevents SQL injection, copies flight data into the planned table,
        deletes it from pending, and updates the UI.
        """
        if self.current_view_mode != "pending":
            messagebox.showinfo("Info", "This flight is already planned")
            return

        if not self.selected_flight:
            messagebox.showwarning("Warning", "No flight selected")
            return

        try:
            flight_id = self.selected_flight[0]
            gate = self.gate_entry.get().strip()

            if is_suspect_sql_input(gate):
                show_sql_meme_popup(self.root)
                return

            if not gate:
                messagebox.showwarning("Input Required", "Please fill in gate field.")
                return

            self.cursor.execute(
                "SELECT * FROM pending_flights WHERE id = %s", (flight_id,)
            )
            flight_data = self.cursor.fetchone()

            if not flight_data:
                messagebox.showerror("Error", "Selected flight not found")
                return
            airline_icon = None
            insert_query = """
                INSERT INTO flights (
                    airline, departure, arrival, status, gate,
                    plane_type, total_seats, seats_taken, price,
                    from_location, to_location
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (
                flight_data["airline"],
                flight_data["departure"],
                flight_data["arrival"],
                "On Time",
                gate,
                flight_data["plane_type"],
                flight_data["total_seats"],
                0,
                flight_data["price"],
                flight_data["from_location"],
                flight_data["to_location"],
            )

            self.cursor.execute(insert_query, insert_values)
            self.cursor.execute(
                "DELETE FROM pending_flights WHERE id = %s", (flight_id,)
            )
            mydb.commit()

            messagebox.showinfo("Success", "Flight successfully planned")

            self.selected_flight = None
            self.btn_plan.configure(state="disabled")

            self.gate_entry.delete(0, "end")
            self.fetch_flights_with_filters()

        except Exception as e:
            logger.error(f"Failed to plan flight: {str(e)}")
            messagebox.showerror("Error", f"Failed to plan flight:\n{str(e)}")

    def cancel_flight(self):
        """
        Delete the selected pending flight after user confirmation.
        Only available in the 'pending' view mode.
        """
        if self.current_view_mode != "pending":
            messagebox.showinfo("Info", "Can't cancel a flight that's already planned")
            return

        if not self.selected_flight:
            messagebox.showwarning(
                "Warning", "Please select a pending flight to delete."
            )
            return

        flight_id = self.selected_flight[0]

        confirm = messagebox.askyesno(
            "Confirm Deletion", "Are you sure you want to delete this pending flight?"
        )
        if not confirm:
            return

        try:
            self.cursor.execute(
                "DELETE FROM pending_flights WHERE id = %s", (flight_id,)
            )
            mydb.commit()

            messagebox.showinfo("Success", "Pending flight successfully deleted.")
            self.selected_flight = None
            self.btn_plan.configure(state="disabled")
            self.fetch_flights_with_filters()

        except Exception as e:
            logger.error(f"Failed to delete pending flight: {str(e)}")
            messagebox.showerror("Error", f"Could not delete pending flight:\n{str(e)}")

    def logout(self):
        """
        Log the user out by destroying the current screen and returning to the login screen.
        Falls back to restarting the app if necessary.
        """
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

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, "cursor"):
            self.cursor.close()
        if hasattr(self, "frame_main") and self.frame_main.winfo_exists():
            self.frame_main.destroy()
