import customtkinter as ctk
import pygame
import os
from PIL import Image, ImageTk


class BjornEasterEgg(ctk.CTkToplevel):
    def __init__(self, parent, video_path="docs/icons/easteregg.gif"):
        super().__init__(parent)
        self.title("BJORN MODE ACTIVATED")
        self.geometry("800x600")

        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

        pygame.mixer.init()

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(fill="both", expand=True)

        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=20)

        self.play_media(video_path)

    def play_media(self, media_path):
        """Handle both GIF and attempt to play sound"""
        audio_path = os.path.splitext(media_path)[0] + ".mp3"
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(loops=-1)

        if media_path.lower().endswith(".gif"):
            self.play_gif(media_path)
        else:
            self.video_label.configure(
                text="Unsupported video format\n(Please use .gif)", font=("Arial", 16)
            )

    def play_gif(self, gif_path):
        """Animate a GIF"""
        try:
            self.gif = Image.open(gif_path)
            self.frames = []

            # Extract all frames
            for i in range(self.gif.n_frames):
                self.gif.seek(i)
                frame = ctk.CTkImage(
                    light_image=self.gif.copy(),
                    dark_image=self.gif.copy(),
                    size=self.gif.size,
                )
                self.frames.append(frame)

            # Start animation
            self.current_frame = 0
            self.animate_gif()

        except Exception as e:
            self.video_label.configure(
                text=f"Error loading GIF:\n{str(e)}", text_color="red"
            )

    def animate_gif(self):
        """Update GIF frames"""
        if self.current_frame < len(self.frames):
            self.video_label.configure(image=self.frames[self.current_frame])
            self.current_frame += 1
            self.after(100, self.animate_gif)
        else:
            self.current_frame = 0
            self.animate_gif()

    def destroy(self):
        """Clean up resources"""
        pygame.mixer.music.stop()
        if hasattr(self, "gif"):
            self.gif.close()
        super().destroy()
