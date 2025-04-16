import customtkinter as ctk
from tkinter import messagebox
from basewindow import BaseWindow
from config import mydb,get_logger
from datetime import datetime
from views.payment_simulation import PaymentScreen

logger = get_logger(__name__)

class AdditionalPackageScreen(BaseWindow):
    def __init__(self, root,view_manager, selected_flight, user_id, package_price=0, username=None):
        super().__init__(root, title=f"Additional Packages - {username}" if username else "Additional Packages")
        self.user_id = user_id
        self.cursor = mydb.cursor()
        self.view_manager = view_manager
        self.selected_flight = selected_flight
        flight_id, airline, from_location, departure, to_location, price = self.selected_flight
        flight_info = f"Flight: {airline} | {from_location} to {to_location} | {departure} | Price: {price}"
        self.package_price = package_price
        self.discount_applied = False
        self.discount_amount = 0
        self.discount_percent = 0

        # frame main
        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # frame with prices
        self.frame_total_price = ctk.CTkFrame(self.frame_main, corner_radius=10, border_width=2,
                                              border_color="black")
        self.frame_total_price.grid(row=2, column=1, padx=10, pady=10)
        # frame with additions
        self.frame_additions = ctk.CTkFrame(self.frame_main)
        self.frame_additions.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Widgets setup
        self.flight_info_label = ctk.CTkLabel(self.frame_main, text=flight_info, font=("Arial", 14, "bold"))
        self.lbl_success = ctk.CTkLabel(self.frame_main,
                                        text="Ticket reserved! Now choose your additional packages.")
        self.btn_package1 = ctk.CTkButton(self.frame_additions, text="Package 1: 30 €",
                                          command=lambda: self.package1_selected(price))
        self.lbl_package1 = ctk.CTkLabel(self.frame_additions, text="info over package 1")
        self.btn_package2 = ctk.CTkButton(self.frame_additions, text="Package 2: 25 €",
                                          command=lambda: self.package2_selected(price))
        self.lbl_package2 = ctk.CTkLabel(self.frame_additions, text="info over package 2")

        self.buy_button = ctk.CTkButton(self.frame_main, text="Buy", command=self._finalize_purchase)

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
        self.btn_apply_discount = ctk.CTkButton(self.frame_additions, text="Apply Discount", width=100,
                                                command=self.apply_discount)

        self.lbl_discount_label = ctk.CTkLabel(self.frame_total_price, text="Discount:")
        self.lbl_discount_amount = ctk.CTkLabel(self.frame_total_price, text="0.00 €")

        self.view_state = {
            'selected_flight' : self.selected_flight,
            'user_id': self.user_id,
            'package_price': self.package_price
        }
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

    def _place_widgets(self):
        """Position all widgets in the layout"""
        # Main grid configuration
        self.frame_main.grid_rowconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        # Flight info
        self.flight_info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Success message
        self.lbl_success.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Package selection
        self.frame_additions.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.btn_package1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lbl_package1.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Price display
        self.frame_total_price.grid(row=2, column=1, padx=10, pady=10)
        self.lbl_flight_price_label.grid(row=0, column=0, padx=10, pady=5)
        self.lbl_flight_price.grid(row=0, column=1, padx=10, pady=5)
        self.total_price_label.grid(row=2, column=0, padx=10, pady=5)
        self.total_price.grid(row=2, column=1, padx=10, pady=5)

        # Discount widgets
        self.lbl_discount.grid(row=3, column=0, padx=10, pady=(20, 5), sticky="w")
        self.entry_discount.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.btn_apply_discount.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Purchase button
        self.buy_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def _package_selected(self, amount):
        """Handle package selection"""
        self.package_price += amount
        self._update_total_price()

    def _update_total_price(self):
        """Update the total price display"""
        flight_price = float(self.selected_flight[-1])
        total = flight_price + self.package_price

        if self.discount_applied:
            total -= self.discount_amount

        self.total_price.configure(text=f"{total:.2f} €")

    def _finalize_purchase(self):
        """Complete the booking process with proper argument passing"""
        print("Finalize purchase called")  # First line of _finalize_purchase

        try:
            # Validate selected flight exists
            if not hasattr(self, 'selected_flight') or not self.selected_flight:
                raise ValueError("No flight selected")

            # Extract flight data
            flight_id = self.selected_flight[0]
            base_price = float(self.selected_flight[5])

            # Calculate total price
            package_price = float(getattr(self, 'package_price', 0))
            total_price = base_price + package_price

            # Apply discount if available
            if getattr(self, 'discount_applied', False):
                discount = float(getattr(self, 'discount_amount', 0))
                total_price = max(0, total_price - discount)

            # Create booking and get booking ID
            self.cursor.execute(
                "INSERT INTO bookings (user_id, flight_id, booking_date, status, total_price) "
                "VALUES (%s, %s, NOW(), 'Pending Payment', %s)",
                (self.user_id, flight_id, total_price)
            )

            # Get the newly created booking ID
            booking_id = self.cursor.lastrowid

            # Update seat count
            self.cursor.execute(
                "UPDATE flights SET seats_taken = seats_taken + 1 WHERE id = %s",
                (flight_id,)
            )

            mydb.commit()

            # Hide the current window
            self.frame_main.pack_forget()

            # Open payment screen with proper callback
            self.payment_screen = PaymentScreen(
                root=self.root,  # parent window
                view_manager=self.view_manager,
                booking_id=booking_id,
                amount=total_price,
                user_id=self.user_id,
                return_callback=self._payment_completed
            )

        except Exception as e:
            logger.exception("Error finalizing purchase")
            mydb.rollback()
            messagebox.showerror("Error", f"Failed to complete booking: {str(e)}")

    def _payment_completed(self, success):
        """Handle payment completion callback"""
        if success:
            # Show success message and close
            messagebox.showinfo("Success", "Payment completed successfully!")
            self.view_manager.show_view(
                'UserScreen',
                user_id=self.user_id,
                username=self.view_manager.current_username
            )
        else:
            # Show the package screen again
            messagebox.showwarning("Notice", "Payment was not completed")
            self.frame_main.pack()

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


