import tkinter as tk
from PIL import Image, ImageTk

def show_sql_meme_popup(root):
    """
    Display a popup warning when SQL injection is detected.
    """
    top = tk.Toplevel(root)
    top.title("SQL Injection Detected!")
    top.geometry("500x500")
    try:
        img = Image.open("docs/icons/you_naughty_naughty.png")
        img = img.resize((480, 360))
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(top, image=img_tk)
        label.image = img_tk
        label.pack(pady=20)

        caption = tk.Label(top, text="Nice try, Hackerman...", font=("Arial", 14))
        caption.pack()

    except Exception as e:
        label = tk.Label(top, text="Couldn't load meme image :(\n" + str(e), fg="red")
        label.pack(pady=20)
