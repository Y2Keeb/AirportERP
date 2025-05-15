import customtkinter as ctk
from tkinter import messagebox

from basewindow import BaseWindow
from config import mydb,get_logger
from datetime import datetime
from views.payment_simulation import PaymentScreen
from views.bjorn_easter_egg import BjornEasterEgg

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
        self.username=username
        self.discount_applied = False
        self.discount_amount = 0
        self.discount_percent = 0
        self.total_price_label = 0

        self.frame_main = ctk.CTkFrame(root,fg_color="gray11")
        self.frame_main.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.92)

        self.frame_content = ctk.CTkFrame(self.frame_main,fg_color="transparent")
        self.frame_content.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.8, relheight=0.8)
        self.frame_content.columnconfigure(0, weight=1)
        self.frame_content.columnconfigure(1, weight=1)

        self.frame_total_price = ctk.CTkFrame(self.frame_content, corner_radius=10)
        self.frame_total_price.grid(row=2, column=1, padx=10, pady=10,sticky="e")

        self.frame_additions = ctk.CTkFrame(self.frame_content, corner_radius=10)
        self.frame_additions.grid(row=2, column=0, padx=10, pady=(3,10), sticky="w")

        self.flight_info_label = ctk.CTkLabel(self.frame_content, text=flight_info, font=("Arial", 14, "bold"))
        self.lbl_success = ctk.CTkLabel(self.frame_content,text="Ticket reserved! Now choose your additional packages.",justify="left")

        self.package1_var = ctk.BooleanVar()
        self.checkbox_package1 = ctk.CTkCheckBox(self.frame_additions, text="Priority boarding – 15 €",
                                                 variable=self.package1_var,
                                                 command=self.update_checkbox_total)
        self.lbl_package1 = ctk.CTkLabel(self.frame_additions, text="Board the plane first.")


        self.package2_var = ctk.BooleanVar()
        self.checkbox_package2 = ctk.CTkCheckBox(self.frame_additions, text="Unaccompanied minor service – 55 €",
                                                 variable=self.package2_var,
                                                 command=self.update_checkbox_total)
        self.lbl_package2 = ctk.CTkLabel(self.frame_additions, text="We will supply a babysitter,while you enjoy a drink in first class!")

        self.package3_var = ctk.BooleanVar()
        self.checkbox_package3 = ctk.CTkCheckBox(self.frame_additions, text="Pet in cabin + 10 €",
                                                 variable=self.package3_var,
                                                 command=self.update_checkbox_total)
        self.lbl_package3 = ctk.CTkLabel(self.frame_additions,
                                         text="Pets fly in the cabin? Absolutely. Dogs, cats, emotional support hamsters,we’re here for it!\nIn fact, we will even GIVE you money to bring one!", justify="left")

        self.buy_button = ctk.CTkButton(self.frame_content, text="Buy", command=self.finalize_purchase)

        self.lbl_flight_price_label = ctk.CTkLabel(self.frame_total_price, text="Flight: ")
        self.lbl_flight_price = ctk.CTkLabel(self.frame_total_price, text=f"{float(price):.2f} €")
        self.lbl_additional_package_label = ctk.CTkLabel(self.frame_total_price, text="Selected packages:")
        self.lbl_addpackage_price = ctk.CTkLabel(self.frame_total_price, text="0.00 €")

        total_price = float(package_price) + float(price)
        self.total_label = ctk.CTkLabel(self.frame_total_price, text="Total: ")
        self.total_price_label = ctk.CTkLabel(self.frame_total_price, text=f"{total_price:.2f} €")

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
        self.create_menu_bar(["logout"])
        self.menu_bar.lift()
        self.create_widgets()

    def create_widgets(self):
        """
        Place and configure all widgets on the screen, including checkboxes, labels,
        discount code entry, and price display layout.
        """
        self.flight_info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.lbl_success.grid(row=1, column=0, columnspan = 2,padx=10, pady=10, sticky="w")

        self.checkbox_package1.grid(row=2, column=0, padx=10, pady=(30,5), sticky="w")
        self.lbl_package1.grid(row=3, column=0, padx=10, pady=(5,30), sticky="w")

        self.checkbox_package2.grid(row=4, column=0, padx=10, pady=(30,5), sticky="w")
        self.lbl_package2.grid(row=5, column=0, padx=10, pady=(5,30), sticky="w")

        self.checkbox_package3.grid(row=6, column=0, padx=10, pady=(30, 5), sticky="w")
        self.lbl_package3.grid(row=7, column=0, padx=10, pady=(5, 30), sticky="w")

        self.buy_button.grid(row=10, column=0, padx=(10,20), pady=10)

        #price frame
        self.lbl_flight_price_label.grid(row=2, column=0, padx=25, pady=(40,10), sticky="w")
        self.lbl_flight_price.grid(row=2, column=1, padx=25,pady=(40,10))
        self.lbl_additional_package_label.grid(row=3, column=0, padx=25, pady=10, sticky="w")
        self.lbl_addpackage_price.grid(row=3, column=1, padx=25, pady=10)
        self.lbl_discount_label.grid(row=5, column=0, padx=25, pady=10, sticky="w")
        self.lbl_discount_amount.grid(row=5, column=1, padx=25, pady=10)
        self.total_label.grid(row=6, column=0, padx=25,pady=(10,40), sticky="w")
        self.total_price_label.grid(row=6, column=1, padx=25,pady=(10,40))

        self.lbl_discount.grid(row=8, column=0, padx=10, pady=(20, 5), sticky="w")
        self.entry_discount.grid(row=9, column=0, padx=10, pady=(5,50), sticky="w")
        self.btn_apply_discount.grid(row=9, column=1, padx=10, pady=(5,50), sticky="w")

    def finalize_purchase(self):
        """
        Finalize the booking by calculating the total price, applying any discounts,
        inserting the booking in the database, and launching the payment screen.
        """
        try:
            if not hasattr(self, 'selected_flight') or not self.selected_flight:
                raise ValueError("No flight selected")

            flight_id = self.selected_flight[0]
            base_price = float(self.selected_flight[5])

            package_price = float(getattr(self, 'package_price', 0))
            self.total_price_label = base_price + package_price

            if getattr(self, 'discount_applied', False):
                discount = float(getattr(self, 'discount_amount', 0))
                self.total_price_label = max(0, self.total_price_label - discount)

            self.cursor.execute(
                "INSERT INTO bookings (user_id, flight_id, booking_date, status, total_price) "
                "VALUES (%s, %s, NOW(), 'Pending Payment', %s)",
                (self.user_id, flight_id, self.total_price_label)
            )

            booking_id = self.cursor.lastrowid

            self.cursor.execute(
                "UPDATE flights SET seats_taken = seats_taken + 1 WHERE id = %s",
                (flight_id,)
            )

            mydb.commit()

            self.frame_main.pack_forget()

            self.payment_screen = PaymentScreen(
                root=self.root,  # parent window
                view_manager=self.view_manager,
                booking_id=booking_id,
                amount=self.total_price_label,
                user_id=self.user_id,
                username=self.username,
                return_callback=self.payment_completed
            )
            self.payment_screen.after(100, lambda: (
                self.payment_screen.focus_force(),
                self.payment_screen.lift(),
                self.payment_screen.attributes('-topmost', True),
                self.payment_screen.attributes('-topmost', False)
            ))
            self.payment_screen.grab_set()

        except Exception as e:
            logger.exception("Error finalizing purchase")
            mydb.rollback()
            messagebox.showerror("Error", f"Failed to complete booking: {str(e)}")

    def payment_completed(self, success):
        """
        Handle the outcome of the payment screen and return to the user screen if successful.
        """
        if success:
            messagebox.showinfo("Success", "Payment completed successfully!")
            self.view_manager.show_view(
                'UserScreen',
                user_id=self.user_id,
                username=self.username
            )
        else:
            messagebox.showwarning("Notice", "Payment was not completed")
            self.frame_main.pack()

    def apply_discount(self):
        """
        Validate and apply a discount code to the current booking.
        Includes support for easter egg code 'BJORN'.
        """
        try:
            entered_code = self.entry_discount.get().strip().upper()
            if not entered_code:
                messagebox.showwarning("Error", "Please enter a discount code")
                return

            if entered_code == "BJORN":
                BjornEasterEgg(self.root)
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

            discount_percent = float(result[1])
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
        """
        Recalculate and display the updated total price after selecting packages
        or applying a discount.
        """
        try:
            flight_price = float(flight_price)
            package_price = float(self.package_price)
            discount_amount = float(getattr(self, 'discount_amount', 0))

            subtotal = flight_price + package_price
            total = subtotal - discount_amount

            self.lbl_addpackage_price.configure(text=f"+ {package_price:.2f} €")

            if hasattr(self, 'discount_applied') and self.discount_applied:
                self.lbl_discount_amount.configure(text=f"- {discount_amount:.2f} €")
                self.lbl_discount_label.configure(text=f"Discount ({getattr(self, 'discount_percent', 0)}%): -")
            else:
                self.lbl_discount_amount.configure(text="- 0.00 €")
                self.lbl_discount_label.configure(text="Discount: -")

            self.total_price_label.configure(text=f"{total:.2f} €")

            self.frame_main.update_idletasks()

        except Exception as e:
            print(f"Error in update_total_price: {str(e)}")
            messagebox.showerror("Error", f"Failed to update prices: {str(e)}")

    def update_checkbox_total(self):
        """
        Recalculate package price based on which checkboxes are selected.
        Updates the total price immediately.
        """
        base_price = float(self.selected_flight[-1])
        self.package_price = 0

        if self.package1_var.get():
            self.package_price += 15
        if self.package2_var.get():
            self.package_price += 55
        if self.package3_var.get():
            self.package_price -= 10
        self.update_total_price(base_price)

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

