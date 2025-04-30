import customtkinter as ctk
from config import set_theme
from views.login_screen import LoginScreen
from view_manager import ViewManager
import pywinstyles, sys

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("800x550")

        self.view_manager = ViewManager(self.root)
        self.root.view_manager = self.view_manager

        self.view_manager.show_view(LoginScreen)

        self.root.after(100, lambda: self.apply_dark_titlebar(self.root))

    def apply_dark_titlebar(self, root):
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            # Windows 11
            pywinstyles.change_header_color(root, "#1c1c1c")
        elif version.major == 10:
            # Windows 10
            pywinstyles.apply_style(root, "dark")
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.root.bind("<Return>", lambda event: app.view_manager.current_view.login())
    app.run()
