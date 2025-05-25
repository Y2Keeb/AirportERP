import time

import customtkinter as ctk
from config import get_logger, init_sound
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
        screen_width = 1920
        screen_height = 1200
        app_width = 1300
        app_height = 900
        x = 150
        y = 17

        self.root.geometry(f"{app_width}x{app_height}+{x}+{y}")

        self.view_manager = ViewManager(self.root)
        self.root.view_manager = self.view_manager

        self.splash_min_time_passed = False
        self.login_ready = False

        self.splash = SplashScreen(self.root)
        self.splash.pack(fill="both", expand=True)
        self.root.update_idletasks()

        self.root.after(1000, self.mark_splash_time_passed)
        threading.Thread(target=self.prepare_login_screen, daemon=True).start()

        init_sound()

    def prepare_login_screen(self):
        time.sleep(2)
        login_view = LoginScreen(self.root, view_manager=self.view_manager)

        def build_view():
            login_view.load_view_content()
            self.login_view = login_view
            self.login_ready = True
            self.check_splash_done()

        self.root.after(0, build_view)

    def mark_splash_time_passed(self):
        self.splash_min_time_passed = True
        self.check_splash_done()

    def check_splash_done(self):
        if self.splash_min_time_passed and self.login_ready:
            self.splash.cleanup()  # Destroy the splash screen frame
            self.view_manager.show_view(lambda root: self.login_view)

    def apply_dark_titlebar(self, root):
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(root, "#1c1c1c")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark")
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

    def run(self):
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.root.bind("<Return>", lambda event: app.view_manager.current_view.login())
    app.run()
