import customtkinter as ctk
from config import set_theme
from views.login_screen import LoginScreen
from view_manager import ViewManager

class App:
    def __init__(self):
        self.root = ctk.CTk()

        set_theme()
        self.root.geometry("800x600")

        self.view_manager = ViewManager(self.root)
        self.root.view_manager = self.view_manager

        self.view_manager.show_view(LoginScreen)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.root.bind("<Return>", lambda event: app.view_manager.current_view.login())
    app.run()
