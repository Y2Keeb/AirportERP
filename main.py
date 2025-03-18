"""
The mainscreen
"""
import tkinter as tk
from tkinter import messagebox, Menu

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Dashboard')
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = Menu(self.root)
        help_ = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        self.root.config(menu=menubar)

    def create_widgets(self):
        image = tk.PhotoImage(file="docs/icons/plane-prop.png")
        tk.Label(self.root, image=image).pack()
        self.root.image = image  

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
