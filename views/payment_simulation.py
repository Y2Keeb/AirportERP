import datetime
import customtkinter as ctk
import random,string
from tkinter import messagebox


class PaymentScreen(ctk.CTkToplevel):
    def __init__(self, root, view_manager, booking_id=None, amount=0, user_id=None, username=None, return_callback=None):
        super().__init__(root)
        self.title("Pay here")
        self.booking_id = booking_id
        self.return_callback = return_callback
        self.view_manager = view_manager
        self.amount = amount
        self.user_id = user_id
        self.username =username
        self.txn_id = None
        self.remaining_time = 15 * 60
        self._active = True
        self._countdown_id = None
        self._update_countdown()
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self.view_state = {
            'user_id': self.user_id,
            'username': self.username
        }
        ctk.CTkLabel(
            self,
            text=f"Amount to pay: €{self.amount:.2f}",
            font=("Arial", 16)
        ).pack(pady=10)

        ctk.CTkLabel(
            self,
            text="Please complete your payment within 15 minutes",
            font=("Arial", 16)
        ).pack(pady=20)

        self.countdown_label = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"))
        self.countdown_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.pay_button = ctk.CTkButton(self, text="Pay Now", command=self._process_payment)
        self.pay_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self._cancel_payment)
        self.cancel_button.pack(pady=10)

        self._update_countdown()

    def _on_window_close(self):
        """Handle window close button (X)"""
        self._cancel_payment()

    def _update_countdown(self):
        if not self._active or not hasattr(self, 'countdown_label'):
            return

        minutes, seconds = divmod(self.remaining_time, 60)
        self.countdown_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self._countdown_id = self.after(1000, self._update_countdown)
        else:
            self._timeout()

    def _process_payment(self):
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
        self._active = False
        if self._countdown_id:
            self.after_cancel(self._countdown_id)
        self.after(3000, self.payment_successful)

    def _go_back(self, success=True):
        """Return to previous screen using ViewManager"""
        from views.user_screen import UserScreen
        self._active = False
        self.destroy()
        if success:
            self.view_manager.show_view(
                UserScreen,
                username=self.username,
                user_id=self.user_id
            )
        else:
            self.view_manager.go_back()

    def _timeout(self):
        if self._active:
            messagebox.showwarning("Timeout", "Payment time has expired.")
            self._go_back(False)

    def _cancel_payment(self):
        self._active = False
        if hasattr(self, '_countdown_id') and self._countdown_id:
            self.after_cancel(self._countdown_id)
        if self.return_callback:
            self.return_callback(success=False)
        self.destroy()

    def payment_successful(self):
        self._active = False
        if hasattr(self, '_countdown_id') and self._countdown_id:
            self.after_cancel(self._countdown_id)

        for widget in self.winfo_children():
            widget.destroy()

        transaction_id = "TXN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.txn_id = transaction_id

        success_label = ctk.CTkLabel(self, text="Payment Successful!", font=("Arial", 20))
        success_label.pack(pady=15)

        txn_label = ctk.CTkLabel(self, text=f"Transaction ID: {transaction_id}", font=("Arial", 14))
        txn_label.pack(pady=5)

        amount_label = ctk.CTkLabel(self, text=f"Amount Paid: €{self.amount:.2f}", font=("Arial", 14))
        amount_label.pack(pady=5)

        finish_btn = ctk.CTkButton(self, text="Finish", command=self._go_back_to_user)
        finish_btn.pack(pady=10)

        receipt_btn = ctk.CTkButton(self, text="View Receipt", command=self._view_receipt_and_return)
        receipt_btn.pack(pady=10)


    def _go_back_to_user(self):
        """Properly return to user screen after payment"""
        from views.user_screen import UserScreen
        self._active = False
        if hasattr(self, '_countdown_id') and self._countdown_id:
            self.after_cancel(self._countdown_id)

        # Destroy the payment window
        self.destroy()

        # Return to UserScreen through the view manager
        if self.view_manager:
            self.view_manager.show_view(
                UserScreen,
                view_manager=self.view_manager,
                username=self.username,
                user_id=self.user_id
            )
        else:
            # Fallback without view manager
            from views.user_screen import UserScreen
            UserScreen(self._root,
                       username=self.username,
                       user_id=self.user_id,
                       view_manager=self.view_manager)
    def _view_receipt_and_return(self):
        """Show receipt and return to user screen after receipt is closed"""
        receipt_window = ctk.CTkToplevel(self)
        receipt_window.title("Receipt")
        receipt_window.geometry("400x300")

        # Make it modal so it stays on top
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

        def close_and_return():
            receipt_window.destroy()
            self._go_back_to_user()

        ctk.CTkButton(receipt_window, text="Close",
                      command=close_and_return).pack(pady=10)

