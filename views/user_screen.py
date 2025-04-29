from basewindow import BaseWindow
import customtkinter as ctk
from config import mydb
from views.ticket_booking_screen import TicketSystem
from views.user_bookings_overview_screen import MyBookings


class UserScreen(BaseWindow):
    def __init__(self, root, username=None, user_id=None, view_manager=None):
        super().__init__(root, f"User Dashboard - {username}")
        self.username = username
        self.view_manager = view_manager
        self.root.geometry("800x500")
        self.user_id = self._get_user_id()

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.pack(fill='both', expand=True)

        self.view_state = {
            'username': self.username,
            'user_id': self.user_id
        }

        self._build_ui()
        self.display_upcoming_flight()

    def _get_user_id(self):
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        return cursor.fetchone()[0]

    def _build_ui(self):
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        content_frame = ctk.CTkFrame(self.frame_main)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_main.grid_rowconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        greeting_label = ctk.CTkLabel(
            content_frame, text=f"Hi {self.username}!",
            font=("Arial", 24, "bold")
        )
        greeting_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="e")

        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="e", padx=20)

        btn_buy_tickets = ctk.CTkButton(buttons_frame, text="Buy Tickets", command=self._navigate_to_tickets)
        btn_buy_tickets.grid(row=0, column=0, padx=5)

        btn_my_bookings = ctk.CTkButton(buttons_frame, text="My Bookings", command=self._navigate_to_bookings)
        btn_my_bookings.grid(row=0, column=1, padx=5)

        upcoming_label = ctk.CTkLabel(content_frame, text="Upcoming flight:", font=("Arial", 16, "bold"))
        upcoming_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 2))

        self.upcoming_flight_frame = ctk.CTkFrame(content_frame, border_width=2, border_color="black")
        self.upcoming_flight_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")

        self.display_upcoming_flight()

        content_frame.grid_rowconfigure(3, weight=1)
        content_frame.grid_columnconfigure((0, 1), weight=1)

    def _navigate_to_tickets(self):
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.pack_forget()

        if self.view_manager:
            self.view_manager.push_view(
                TicketSystem,
                user_id=self.user_id,
                username=self.username
            )
        else:
            TicketSystem(self.root, user_id=self.user_id, username=self.username)

    def _navigate_to_bookings(self):
        if self.view_manager:
            self.view_manager.push_view(
                MyBookings,
                user_id=self.user_id,
                username=self.username
            )
        else:
            MyBookings(self.root, user_id=self.user_id, username=self.username)

    def display_upcoming_flight(self):

        if not hasattr(self, 'upcoming_flight_frame') or not self.upcoming_flight_frame.winfo_exists():
            self.upcoming_flight_frame = ctk.CTkFrame(self.frame_main, border_width=2, border_color="black")
            self.upcoming_flight_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")

        for widget in self.upcoming_flight_frame.winfo_children():
            widget.destroy()

        try:
            cursor = mydb.cursor(dictionary=True)

            query = """
                    SELECT f.airline, f.departure, f.arrival, f.status, f.gate, f.plane_type,
                           f.total_seats, f.seats_taken, f.from_location, f.to_location, f.airline_icon
                    FROM bookings b
                    JOIN flights f ON b.flight_id = f.id
                    WHERE b.user_id = %s AND f.departure > NOW()  -- Only flights with departure in the future
                    ORDER BY f.departure ASC  -- Get the earliest upcoming flight
                    LIMIT 1
                    """
            cursor.execute(query, (self.user_id,))
            flight = cursor.fetchone()

            if not flight:
                no_flight_label = ctk.CTkLabel(
                    self.upcoming_flight_frame, text="No upcoming flights.",
                    font=("Arial", 14, "italic")
                )
                no_flight_label.grid(row=0, column=0, padx=10, pady=10)
                return

            flight_info_label = ctk.CTkLabel(
                self.upcoming_flight_frame,
                text=f"{flight['airline']} Flight\n"
                     f"{flight['from_location']} ➝ {flight['to_location']}\n",
                font=("Arial", 16, "bold"),
                justify="center"
            )
            flight_info_label.grid(row=0, column=0, columnspan=2, pady=(15, 15))

            details = [
                ("Departure:", f"{flight['departure']}"),
                ("Arrival:", f"{flight['arrival']}"),
                ("Gate:", f"{flight['gate']}"),
                ("Status:", f"{flight['status']}"),
                ("Plane Type:", f"{flight['plane_type']}"),
            ]

            for i, (label, value) in enumerate(details):
                ctk.CTkLabel(self.upcoming_flight_frame, text=label, font=("Arial", 14)).grid(
                    row=i + 1, column=0, sticky="w", padx=10, pady=2
                )
                ctk.CTkLabel(self.upcoming_flight_frame, text=value, font=("Arial", 14)).grid(
                    row=i + 1, column=1, sticky="w", padx=10, pady=2
                )

            # QR code placeholder
            airline_icon = ctk.CTkLabel(self.upcoming_flight_frame, text="QR CODE HERE",
                                        font=("Arial", 20))  # Placeholder
            airline_icon.grid(row=1, column=2, rowspan=3, padx=20, pady=5, sticky="e")

            self.upcoming_flight_frame.grid_columnconfigure(1, weight=1)

        except Exception as e:
            print("Error fetching flight data:", e)

        finally:
            cursor.close()

    def cleanup(self):
        """Clean up resources when screen is closed"""
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()
