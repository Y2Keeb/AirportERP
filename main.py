import customtkinter as ctk
from config import set_theme,get_logger
from views.login_screen import LoginScreen
from view_manager import ViewManager
import pywinstyles, sys


logger = get_logger(__name__)

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        screen_width=1920
        screen_height=1200
        app_width=1300
        app_height=900
        x = 150
        y = 17

        self.root.geometry(f"{app_width}x{app_height}+{x}+{y}")

        self.view_manager = ViewManager(self.root)
        self.root.view_manager = self.view_manager

        self.view_manager.show_view(LoginScreen)

        self.root.after(100, lambda: self.apply_dark_titlebar(self.root))

    def apply_dark_titlebar(self, root):
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(root, "#1c1c1c")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark")
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

    def run(self):
        logger.debug(f"Detected screen resolution: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.root.bind("<Return>", lambda event: app.view_manager.current_view.login())
    app.run()
