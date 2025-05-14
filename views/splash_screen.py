import customtkinter as ctk
from PIL import Image, ImageSequence

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        gif_path = "docs/icons/loading_plane.gif"
        gif = Image.open(gif_path)

        self.frame_size = (174, 321)

        self.frames = [
            ctk.CTkImage(
                light_image=frame.copy().convert("RGBA").resize(self.frame_size, Image.LANCZOS),
                dark_image=frame.copy().convert("RGBA").resize(self.frame_size, Image.LANCZOS),
                size=self.frame_size
            )
            for frame in ImageSequence.Iterator(gif)
        ]

        self.label = ctk.CTkLabel(self, text="", image=self.frames[0])
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.current_frame = 0
        self.animate()

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.configure(image=self.frames[self.current_frame])
        self.after(80, self.animate)

    def cleanup(self):
        self.destroy()
