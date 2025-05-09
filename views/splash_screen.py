import customtkinter as ctk

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=24)).pack(expand=True)

    def cleanup(self):
        self.destroy()