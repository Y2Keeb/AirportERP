import customtkinter as ctk


class BjornEasterEgg(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("BJORN MODE ACTIVATED")
        self.geometry("800x600")

        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

        self.label = ctk.CTkLabel(
            self,
            text="✨ You found the BJORN Easter Egg! ✨",
            font=("Comic Sans MS", 20, "bold"),
        )
        self.label.pack(pady=30)

        self.lbl_temp = ctk.CTkLabel(self, text="Because wine not", font=("Arial", 14))
        self.lbl_temp.pack(pady=10)

        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=20)
