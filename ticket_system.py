import customtkinter as ctk
from tkinter import ttk,messagebox
import tkinter as tk
from tkcalendar import DateEntry
from config import *
from datetime import datetime

logger = get_logger(__name__) #zet module naam als log naam


class TicketSystem:
    def __init__(self, parent_frame,user_id,parent=None):
        """Sets up the UI and prepares the database connection."""
        self.parent = parent
        self.user_id = user_id
        self.cursor = mydb.cursor()

        self.frame_main = ctk.CTkFrame(parent_frame)
        self.frame_main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_search = ctk.CTkFrame(self.frame_main)
        self.frame_search.grid(row=1, column=0,columnspan=2, pady=10, padx=20, sticky="w")
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
            height=6)
        # -> Treeview table widget for displaying flight data.

        self.create_widgets()
        # -> Calls create_widgets() which actually places these elements inside the UI.

    def create_widgets(self):
        """Creates and positions all widgets in the UI."""

        ctk.CTkLabel(
            self.frame_main, text="Buy Tickets", font=("Arial", 25, "bold")
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

        btn_back = ctk.CTkButton(self.frame_main,text="← Back to Dashboard",command=self.go_back,fg_color="transparent",border_width=1)
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
        self.tree.bind("<ButtonRelease-1>", self.on_flight_select)

        # -> Configure headings and column widths using a loop
        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)  # Set column header text
            self.tree.column(col_name, width=width)  # Set column width
        btn_book_ticket = ctk.CTkButton(self.frame_main, text="Book Ticket", command=self.book_ticket)
        btn_book_ticket.grid(row=3, column=1, padx=10)

    def go_back(self):
        if self.parent:
            self.parent.show_home_view()

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

    def on_flight_select(self, event):
        """Get selected flight details and store them, including id."""
        selected_item = self.tree.selection()

        if not selected_item:
            return

        tree_id = selected_item[0]
        flight_values = self.tree.item(tree_id, "values")
        flight_id = self.flights_data.get(tree_id)

        self.selected_flight = (flight_id,) + flight_values
        logger.info(f"User ID:{self.user_id}, Selected a flight in booking system: {self.selected_flight}")

    def book_ticket(self):
        """Proceed to additional package screen after booking the ticket."""
        if not hasattr(self, "selected_flight"):
            print("No flight selected!")
            return

        for widget in self.frame_main.winfo_children():
            widget.grid_forget()
            widget.pack_forget()

        self.additional_package_screen = AdditionalPackageScreen(self.frame_main,selected_flight=self.selected_flight,user_id=self.user_id,package_price=0)

    def open_package_screen(self):
        package_window = tk.Toplevel(self.frame_main)
        package_screen = AdditionalPackageScreen(package_window, selected_flight=self.selected_flight,user_id=self.user_id)

    def refresh_flights(self):
        """Refresh the Treeview to reflect the current flight list."""
        self.tree.delete(*self.tree.get_children())
        self.fetch_flights()

class AdditionalPackageScreen:
    def __init__(self, parent_frame, selected_flight, user_id, package_price):
        self.user_id = user_id
        self.cursor = mydb.cursor()
        self.parent_frame = parent_frame  # Use the parent frame passed in
        self.selected_flight = selected_flight
        flight_id, airline, from_location, departure, to_location, price = self.selected_flight
        flight_info = f"Flight: {airline} | {from_location} to {to_location} | {departure} | Price: {price}"
        self.package_price = package_price

        self.discount_applied = False
        self.discount_amount = 0
        self.discount_percent = 0

        # frame main
        self.frame_main = ctk.CTkFrame(parent_frame)
        self.frame_main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # frame with prices
        self.frame_total_price = ctk.CTkFrame(self.frame_main, corner_radius=10, border_width=2, border_color="black")
        self.frame_total_price.grid(row=2, column=1, padx=10, pady=10)
        # frame with additions
        self.frame_additions = ctk.CTkFrame(self.frame_main)
        self.frame_additions.grid(row=2, column=0, padx=10, pady=10,sticky="w")

        # Widgets setup
        self.flight_info_label = ctk.CTkLabel(self.frame_main, text=flight_info, font=("Arial", 14, "bold"))
        self.lbl_success = ctk.CTkLabel(self.frame_main, text="Ticket reserved! Now choose your additional packages.")
        self.btn_package1 = ctk.CTkButton(self.frame_additions, text="Package 1: 30 €", command=lambda: self.package1_selected(price))
        self.lbl_package1 = ctk.CTkLabel(self.frame_additions, text="info over package 1")
        self.btn_package2 = ctk.CTkButton(self.frame_additions, text="Package 2: 25 €", command=lambda: self.package2_selected(price))
        self.lbl_package2 = ctk.CTkLabel(self.frame_additions, text="info over package 2")

        self.buy_button = ctk.CTkButton(self.frame_main, text="Buy", command=self.finalize_purchase)

        # Create widgets for the price frame
        self.lbl_flight_price_label = ctk.CTkLabel(self.frame_total_price, text="Flight: ")
        self.lbl_flight_price = ctk.CTkLabel(self.frame_total_price, text=f"{float(price):.2f} €")
        self.lbl_additional_package_label = ctk.CTkLabel(self.frame_total_price, text="Selected packages:")
        self.lbl_addpackage_price = ctk.CTkLabel(self.frame_total_price, text="0.00 €")

        total_price = float(package_price) + float(price)
        self.total_price_label = ctk.CTkLabel(self.frame_total_price, text="Total: ")
        self.total_price = ctk.CTkLabel(self.frame_total_price, text=f"{total_price:.2f} €")

        self.lbl_discount = ctk.CTkLabel(self.frame_additions, text="Discount Code:")
        self.entry_discount = ctk.CTkEntry(self.frame_additions, width=150)
        self.btn_apply_discount = ctk.CTkButton(self.frame_additions,text="Apply Discount",width=100,command=self.apply_discount)

        self.lbl_discount_label = ctk.CTkLabel(self.frame_total_price, text="Discount:")
        self.lbl_discount_amount = ctk.CTkLabel(self.frame_total_price, text="0.00 E€")


        self.create_widgets()

    def create_widgets(self):
        self.flight_info_label.grid(row=0, column=0,columnspan = 2,padx=10, pady=10,sticky="ew")
        self.lbl_success.grid(row=1, column=0, columnspan = 2,padx=10, pady=10, sticky="ew")
        self.btn_package1.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lbl_package1.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.btn_package2.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.lbl_package2.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.buy_button.grid(row=9, column=0, padx=10, pady=10)
        #price frame
        self.lbl_flight_price_label.grid(row=2, column=1, padx=10, pady=10)
        self.lbl_flight_price.grid(row=2, column=2, padx=10, pady=10)
        self.lbl_additional_package_label.grid(row=3, column=1, padx=10, pady=10)
        self.lbl_addpackage_price.grid(row=3, column=2, padx=10, pady=10)
        self.total_price_label.grid(row=6, column=1, padx=10, pady=10)
        self.total_price.grid(row=6, column=2, padx=10, pady=10)
        self.lbl_discount_label.grid(row=5, column=1, padx=10, pady=10)
        self.lbl_discount_amount.grid(row=5, column=2, padx=10, pady=10)

        self.lbl_discount.grid(row=7, column=0, padx=10, pady=(20, 5), sticky="w")
        self.entry_discount.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.btn_apply_discount.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    def apply_discount(self):
        """Apply discount code if valid and update prices"""
        try:
            entered_code = self.entry_discount.get().strip()
            if not entered_code:
                messagebox.showwarning("Error", "Please enter a discount code")
                return

            if hasattr(self, 'discount_applied') and self.discount_applied:
                messagebox.showinfo("Notice", "Discount already applied")
                return

            flight_price = float(self.selected_flight[-1])

            query = """
                SELECT id, discount_percent, valid_from, valid_until, 
                       max_uses, current_uses, is_active
                FROM discount_codes
                WHERE UPPER(code) = UPPER(%s)
            """
            self.cursor.execute(query, (entered_code,))
            result = self.cursor.fetchone()

            if not result:
                messagebox.showwarning("Invalid", "Discount code not found")
                return

            (code_id, discount_percent, valid_from, valid_until,
             max_uses, current_uses, is_active) = result

            today = datetime.now().date()
            if not is_active:
                messagebox.showwarning("Invalid", "This code is inactive")
                return

            if today < valid_from:
                messagebox.showwarning("Invalid", f"Code valid from {valid_from}")
                return

            if today > valid_until:
                messagebox.showwarning("Invalid", f"Code expired on {valid_until}")
                return

            if max_uses and current_uses >= max_uses:
                messagebox.showwarning("Invalid", "Usage limit reached")
                return

            discount_percent = float(result[1])  # Convert the DECIMAL to float
            subtotal = float(flight_price) + float(self.package_price)
            self.discount_amount = subtotal * (discount_percent / 100)
            self.discount_applied = True
            self.discount_percent = discount_percent

            update_query = """
                        UPDATE discount_codes
                        SET current_uses = current_uses + 1
                        WHERE id = %s
                    """
            self.cursor.execute(update_query, (code_id,))
            mydb.commit()

            self.update_total_price(self.selected_flight[-1])

            messagebox.showinfo("Success", f"{discount_percent}% discount applied!")

        except Exception as e:
            mydb.rollback()
            messagebox.showerror("Error", f"Failed to apply discount: {str(e)}")

    def update_total_price(self, flight_price):
        """Update all price displays with proper type conversion"""
        try:
            # Convert all values to float to ensure proper math
            flight_price = float(flight_price)
            package_price = float(self.package_price)
            discount_amount = float(getattr(self, 'discount_amount', 0))

            # Calculate the correct total
            subtotal = flight_price + package_price
            total = subtotal - discount_amount

            # Update package price display
            self.lbl_addpackage_price.configure(text=f"+ {package_price:.2f} €")

            # Update discount display
            if hasattr(self, 'discount_applied') and self.discount_applied:
                self.lbl_discount_amount.configure(text=f"- {discount_amount:.2f} €")
                self.lbl_discount_label.configure(text=f"Discount ({getattr(self, 'discount_percent', 0)}%): -")
            else:
                self.lbl_discount_amount.configure(text="- 0.00 €")
                self.lbl_discount_label.configure(text="Discount: -")

            # Update total price (THIS WAS MISSING PROPER UPDATE)
            self.total_price.configure(text=f"{total:.2f} €")

            # Force immediate GUI update
            self.frame_main.update_idletasks()

        except Exception as e:
            print(f"Error in update_total_price: {str(e)}")
            messagebox.showerror("Error", f"Failed to update prices: {str(e)}")
    def package1_selected(self, price):
        self.package_price += 30  # Add package price
        self.update_total_price(price)

    def package2_selected(self, price):
        self.package_price += 25  # Add package price
        self.update_total_price(price)

    def finalize_purchase(self):
        # Finalize booking and update the database
        if not hasattr(self, "selected_flight"):
            print("No flight selected!")
            return

        flight_id, airline, from_location, departure, to_location, price = self.selected_flight
        user_id = self.user_id

        query = """
            INSERT INTO bookings (user_id, flight_id, booking_date, status)
            VALUES (%s, %s, NOW(), 'Booked')
        """
        self.cursor.execute(query, (user_id, flight_id))
        mydb.commit()

        update_query = """
            UPDATE flights
            SET seats_taken = seats_taken + 1
            WHERE id = %s
        """
        self.cursor.execute(update_query, (flight_id,))
        mydb.commit()
        logger.info(f"Booking for user ID '{self.user_id}' succesful!")
        messagebox.showinfo("Success", "Ticket booked successfully!")

