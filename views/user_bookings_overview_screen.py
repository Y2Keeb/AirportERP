from basewindow import BaseWindow
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import mydb, get_logger

logger = get_logger(__name__)

class MyBookings(BaseWindow):
    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, f"My Bookings - {username}" if username else "My Bookings")
        """
        Initialize the booking view and layout the main interface.
        """
        self.user_id = user_id
        self.username = username
        self.view_manager = view_manager
        self.create_menu_bar(["logout"])

        self.view_state = {
            'user_id': user_id,
            'username': username
        }

        self.frame_main = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(60, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="My Bookings",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        btn_back = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            command=self.handle_back,
            fg_color="transparent",
            border_width=1
        )
        btn_back.grid(row=0, column=1, sticky="e")

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        self.menu_bar.lift()
        self.create_bookings_table()
        self.load_bookings()

    def create_bookings_table(self):
        """Create table with custom styling"""
        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",
                        rowheight=30,
                        font=("Helvetica", 10),
                        background="#2e2e2e",
                        foreground="white",
                        fieldbackground="#2e2e2e")

        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, "bold"),
                        background="#3c3c3c",
                        foreground="white")

        style.map("Treeview",
                  background=[('selected', '#555555')])

        columns = [
            ("Airline", 150),
            ("Departure", 150),
            ("From", 120),
            ("To", 120),
            ("Status", 100)
        ]

        table_frame = ctk.CTkFrame(self.frame_main)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=[col[0] for col in columns],
            show="headings",
            height=15,
            selectmode="browse"
        )

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_bookings(self):
        """Load bookings from database"""
        try:
            cursor = mydb.cursor(dictionary=True)
            query = """
                SELECT 
                    b.id,
                    f.airline as flight,
                    f.departure,
                    f.from_location,
                    f.to_location,
                    b.status
                FROM bookings b
                JOIN flights f ON b.flight_id = f.id
                WHERE b.user_id = %s
                ORDER BY f.departure DESC
            """
            cursor.execute(query, (self.user_id,))
            bookings = cursor.fetchall()

            if not bookings:
                messagebox.showinfo("No Bookings", "You don't have any bookings yet.")
                return

            for booking in bookings:
                self.tree.insert("", "end", values=(
                    booking["flight"],
                    booking["departure"],
                    booking["from_location"],
                    booking["to_location"],
                    booking["status"]
                ))

        except Exception as e:
            logger.error(f"Error loading bookings: {e}")
            messagebox.showerror("Error", "Failed to load bookings")
        finally:
            cursor.close()

    def handle_back(self):
        """
        Handle the action of going back to the dashboard.

        Uses the view manager to pop the current view if present.
        If not, manually destroys current widgets and returns to UserScreen.
        """
        self.cleanup()

        if self.view_manager:
            role = getattr(self, 'role', 'user')
            self.view_manager.pop_view(role=role)
        else:
            from views.user_screen import UserScreen
            for widget in self.root.winfo_children():
                widget.destroy()
            UserScreen(self.root,
                       username=self.username,
                       user_id=self.user_id,
                       view_manager=self.view_manager)

    def cleanup(self):
        """
        Cleanup widgets and cancel any scheduled events.
        Called when switching away from this view.
        """
        if hasattr(self, 'menu_bar') and self.menu_bar.winfo_exists():
            self.menu_bar.destroy()
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()

    def logout(self):
        """logout that clears everything and shows login screen"""
        try:
            for widget in self.root.winfo_children():
                widget.destroy()

            from views.kiosk_screen import KioskLoginScreen
            kiosk_login_screen = KioskLoginScreen(self.root, view_manager=self.view_manager)

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error during logout: {e}")
            self.root.destroy()
            import os
            os.system("python main.py")