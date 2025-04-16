import customtkinter as ctk
import random,string
from tkinter import messagebox

class PaymentScreen(ctk.CTkToplevel):
    def __init__(self, root,view_manager,booking_id=None, amount=0,user_id=None,return_callback=None):
        super().__init__(root)  # Remove title from here
        self.title("Pay here")
        self.booking_id = booking_id
        self.return_callback = return_callback
        self.view_manager = view_manager
        self.amount = amount
        self.user_id = user_id
        self.remaining_time = 15 * 60  # 15 minutes in seconds
        self._active = True  # Flag to track if screen is active

        # Add amount display
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

    def _update_countdown(self):
        if not self._active:  # Check if screen is still active
            return

        minutes, seconds = divmod(self.remaining_time, 60)
        self.countdown_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.after(1000, self._update_countdown)
        else:
            self._timeout()

    def _process_payment(self):
        try:
            # Process payment logic...
            if self.return_callback:
                self.simulate_payment()  # This should eventually call the callback
            else:
                messagebox.showinfo("Success", "Payment completed!")
                self.destroy()
        except Exception as e:
            if self.return_callback:
                self.return_callback(False)  # Payment failed
            else:
                messagebox.showerror("Error", f"Payment failed: {str(e)}")

    def simulate_payment(self):
        self.pay_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
        self.status_label.configure(text="Processing payment...")

        self.after(3000, self.payment_successful)

    def payment_successful(self):
        self._active = False

        for widget in self.winfo_children():
            widget.destroy()

        transaction_id = "TXN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        ctk.CTkLabel(self, text="Payment Successful!", font=("Arial", 20)).pack(pady=15)
        ctk.CTkLabel(self, text=f"Transaction ID: {transaction_id}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self, text=f"Amount Paid: €{self.amount:.2f}", font=("Arial", 14)).pack(pady=5)

        ctk.CTkButton(self, text="Finish", command=self._go_back).pack(pady=10)

    def _go_back(self, success=True):
        """Return to previous screen using ViewManager"""
        self._active = False
        if success:
            self.view_manager.show_view(
                'UserScreen',
                user_id=self.view_manager.current_user_id,
                username=self.view_manager.current_username
            )
        else:
            self.view_manager.go_back()

    def _timeout(self):
        if self._active:  # Only proceed if screen is still active
            messagebox.showwarning("Timeout", "Payment time has expired.")
            self._go_back(False)

    def _cancel_payment(self):
        if self.return_callback:
            self.return_callback(success=False)

    def view_receipt(self, txn_id):
        receipt_window = ctk.CTkToplevel(self)
        receipt_window.title("Receipt")
        receipt_window.geometry("350x200")

        receipt_text = (
            f"--- Receipt ---\n"
            f"Transaction ID: {txn_id}\n"
            f"Amount Paid: {self.amount}\n"
            f"Payment Method: VISA\n"
            f"Status: Completed\n"
        )
        ctk.CTkLabel(receipt_window, text=receipt_text, font=("Courier", 12), justify="left").pack(pady=20)
        ctk.CTkButton(receipt_window, text="Close", command=receipt_window.destroy).pack()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Payment Screen")
    app.geometry("400x400")

    def return_callback(success):
        print("Payment success:", success)
        app.destroy()

    screen = PaymentScreen(app, return_callback)
    screen.pack(fill='both', expand=True)

    app.mainloop()
