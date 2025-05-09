import customtkinter as ctk
from config import set_theme,get_logger
from views.login_screen import LoginScreen
from view_manager import ViewManager
import pywinstyles, sys
import threading


from views.splash_screen import SplashScreen

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

        self.view_manager.show_view(SplashScreen)
        self.root.after(100, lambda: self.apply_dark_titlebar(self.root))

        threading.Thread(target=self.prepare_login_screen, daemon=True).start()

    def prepare_login_screen(self):
        login_view = LoginScreen(self.root, view_manager=self.view_manager)
        login_view.load_view_content()

        self.root.after(1500, lambda: self.view_manager.show_view(lambda root: login_view))

    def load_login_screen(self):
        self.view_manager.show_view(LoginScreen)


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
