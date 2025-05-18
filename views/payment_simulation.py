import datetime
import os
import random,string

import customtkinter as ctk
from tkinter import messagebox
from threading import Thread

from config import mydb,get_logger,play_sound


class PaymentScreen(ctk.CTkToplevel):
    def __init__(self, root, view_manager, booking_id=None, amount=0, user_id=None, username=None, return_callback=None):
        super().__init__(root)
        self.root = root

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "docs", "icons", "favicon.ico")
        if os.path.exists(icon_path):
            self.root.wm_iconbitmap(icon_path)

        self.title("Pay here")
        self.booking_id = booking_id
        self.return_callback = return_callback
        self.view_manager = view_manager
        self.amount = amount
        self.user_id = user_id
        self.username =username

        self.txn_id = None
        self.remaining_time = 15 * 60
        self.active = True
        self.countdown_id = None
        self.update_countdown()
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.view_state = {
            'user_id': self.user_id,
            'username': self.username
        }

        width, height = 400, 300
        self.geometry(f"{width}x{height}")

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(self,text=f"Amount to pay: €{self.amount:.2f}",font=("Arial", 16)).pack(pady=10)

        ctk.CTkLabel(self,text="Please complete your payment within 15 minutes",font=("Arial", 16)).pack(pady=20)

        self.countdown_label = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"))
        self.countdown_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.pay_button = ctk.CTkButton(self, text="Pay Now", command=self.process_payment)
        self.pay_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_payment)
        self.cancel_button.pack(pady=10)

        self.update_countdown()

    def on_window_close(self):
        """Handle window close button (X)"""
        self.cancel_payment()

    def update_countdown(self):
        if not self.active or not hasattr(self, 'countdown_label'):
            return

        minutes, seconds = divmod(self.remaining_time, 60)
        self.countdown_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.countdown_id = self.after(1000, self.update_countdown)
        else:
            self.timeout()

    def process_payment(self):
        try:
            if self.return_callback:
                self.simulate_payment()
            else:
                messagebox.showinfo("Success", "Payment completed!")
                self.destroy()
        except Exception as e:
            if self.return_callback:
                self.return_callback(False)
            else:
                messagebox.showerror("Error", f"Payment failed: {str(e)}")

    def simulate_payment(self):
        self.pay_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
        self.status_label.configure(text="Processing payment...")
        self.active = False
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
        self.after(3000, self.payment_successful)

    def go_back(self, success=True):
        """Return to previous screen using ViewManager"""
        from views.user_screen import UserScreen
        self.active = False
        self.destroy()
        if success:
            self.view_manager.show_view(
                UserScreen,
                username=self.username,
                user_id=self.user_id
            )
        else:
            self.view_manager.go_back()

    def go_back_to_user(self):
        """Return to user screen after successful payment"""
        self.active = False
        self.destroy()

        try:
            from views.user_screen import UserScreen
            if hasattr(self, 'view_manager') and self.view_manager is not None:
                self.view_manager.show_view(
                    UserScreen,
                    username=self.username,
                    user_id=self.user_id
                )
            else:
                from views.user_screen import UserScreen
                UserScreen(self.root, username=self.username, user_id=self.user_id)
        except Exception as e:
            print(f"Error navigating back to user screen: {e}")
            self.destroy()

    def timeout(self):
        if self.active:
            messagebox.showwarning("Timeout", "Payment time has expired.")
            self.go_back(False)

    def cancel_payment(self):
        self.active = False
        if hasattr(self, '_countdown_id') and self.countdown_id:
            self.after_cancel(self.countdown_id)

        self.destroy()
        try:
            from views.buy_additional_packages_screen import AdditionalPackages
            if hasattr(self, 'view_manager') and self.view_manager is not None:
                self.view_manager.show_view(
                    AdditionalPackages,
                    username=self.username,
                    user_id=self.user_id,
                    booking_id=self.booking_id
                )
        except Exception as e:
            print(f"Error navigating back to AdditionalPackages: {e}")
            self.destroy()

    def payment_successful(self):
        self.active = False
        if hasattr(self, 'countdown_id') and self.countdown_id:
            self.after_cancel(self.countdown_id)

        transaction_id = "TXN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.txn_id = transaction_id

        try:
            cursor = mydb.cursor()
            print(f"Updating booking {self.booking_id} with transaction {transaction_id}")
            update_query = """
                UPDATE bookings 
                SET status = 'Booked',
                    booking_date = NOW(),
                    transaction_id = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (self.txn_id, self.booking_id))
            mydb.commit()

            cursor.execute("SELECT status, transaction_id FROM bookings WHERE id = %s", (self.booking_id,))
            result = cursor.fetchone()
            print(f"After update - Status: {result[0]}, Transaction ID: {result[1]}")

        except Exception as e:
            print(f"Error updating booking status: {e}")
            import traceback
            traceback.print_exc()
            try:
                mydb.rollback()

            except:
                pass
        finally:
            if 'cursor' in locals():
                cursor.close()

        for widget in self.winfo_children():
            widget.destroy()

        Thread(target=play_sound, args=("docs/sounds/payment_complete.mp3",)).start()

        success_label = ctk.CTkLabel(self, text="Payment Successful!", font=("Arial", 20))
        success_label.pack(pady=15)

        txn_label = ctk.CTkLabel(self, text=f"Transaction ID: {transaction_id}", font=("Arial", 14))
        txn_label.pack(pady=5)

        amount_label = ctk.CTkLabel(self, text=f"Amount Paid: €{self.amount:.2f}", font=("Arial", 14))
        amount_label.pack(pady=5)

        finish_btn = ctk.CTkButton(self, text="Finish", command=self.view_receipt_and_return)
        finish_btn.pack(pady=10)

    def view_receipt_and_return(self):
        """Show receipt and return to user screen after receipt is closed"""
        receipt_window = ctk.CTkToplevel(self)
        receipt_window.title("Receipt")
        receipt_window.geometry("400x300")
        receipt_window.grab_set()

        receipt_text = (
            f"--- Payment Receipt ---\n\n"
            f"Transaction ID: {self.txn_id}\n\n"
            f"Amount Paid: €{self.amount:.2f}\n\n"
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Status: Completed\n"
        )

        ctk.CTkLabel(receipt_window, text=receipt_text,
                     font=("Courier", 14), justify="left").pack(pady=20)

        receipt_window.update_idletasks()
        width = receipt_window.winfo_width()
        height = receipt_window.winfo_height()
        x = (receipt_window.winfo_screenwidth() // 2) - (width // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (height // 2)
        receipt_window.geometry(f'+{x}+{y}')

        ctk.CTkButton(receipt_window, text="Close",
                      command=lambda: [receipt_window.destroy(),self.go_back_to_user()]).pack(pady=10)

