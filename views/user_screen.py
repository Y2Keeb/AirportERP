import PIL

from basewindow import BaseWindow
import qrcode
from PIL import Image
import customtkinter as ctk
import io
from config import mydb
from views.ticket_booking_screen import TicketSystem
from views.user_bookings_overview_screen import MyBookings

class UserScreen(BaseWindow):
    def __init__(self, root, username=None, user_id=None, view_manager=None, **kwargs):
        super().__init__(root, f"User Dashboard - {username}")
        self.username = username
        self.view_manager = view_manager
        self.create_menu_bar(["help","logout"])

        self.original_bg_image = PIL.Image.open("docs/icons/background2.png").convert("RGBA")
        startup_image = self.original_bg_image.resize((1600, 950), Image.NEAREST)
        self.bg_image = ctk.CTkImage(light_image=startup_image, dark_image=startup_image, size=(1600, 950))
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.user_id = self.get_user_id()
        self.full_name = self.get_full_name()

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.95, relheight=0.92)
        self.role = kwargs.get('role', 'user')

        self.view_state = {
            'username': self.username,
            'user_id': self.user_id,
            'role': self.role
        }
        self.menu_bar.lift()
        self.build_ui()
        self.display_upcoming_flight()

    def get_full_name(self):
        """
           Query the database for the full name of the airline user based on user ID.
           Returns the full name as a string.
        """
        cursor = mydb.cursor()
        cursor.execute("SELECT concat(first_name,' ',last_name) FROM users WHERE id =%s", (self.get_user_id(),))
        result = cursor.fetchone()
        return result[0] if result else None

    def build_ui(self):
        for widget in self.frame_main.winfo_children():
            widget.destroy()

        content_frame = ctk.CTkFrame(self.frame_main,fg_color="gray11")
        content_frame.grid(row=0, column=0, sticky="nsew")

        self.frame_main.grid_rowconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        greeting_label = ctk.CTkLabel(
            content_frame, text=f"Hi {self.full_name}!",
            font=("Arial", 24, "bold")
        )
        greeting_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="e")

        subgreeting_lbl = ctk.CTkLabel(content_frame,text=f"Logged in as - {self.username}", font=("Arial", 15, "bold"))
        subgreeting_lbl.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="e")
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="e", padx=20)

        btn_buy_tickets = ctk.CTkButton(buttons_frame, text="Buy Tickets", command=self.navigate_to_tickets)
        btn_buy_tickets.grid(row=0, column=0, padx=5)

        btn_my_bookings = ctk.CTkButton(buttons_frame, text="My Bookings", command=self.navigate_to_bookings)
        btn_my_bookings.grid(row=0, column=1, padx=5)

        upcoming_label = ctk.CTkLabel(content_frame, text="Upcoming flight:", font=("Arial", 16, "bold"))
        upcoming_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 2))

        self.upcoming_flight_frame = ctk.CTkFrame(content_frame, border_width=2, border_color="black",fg_color="gray16")
        self.upcoming_flight_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(30,30), sticky="nsew")

        content_frame.grid_rowconfigure(3, weight=0)
        content_frame.grid_columnconfigure((0, 1), weight=1)

    def get_user_id(self):
        cursor = None
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def navigate_to_tickets(self):
        if self.view_manager:
            self.view_manager.push_view(
                TicketSystem,
                user_id=self.user_id,
                username=self.username
            )
        else:
            self.cleanup()
            TicketSystem(self.root, user_id=self.user_id, username=self.username)

    def navigate_to_bookings(self):
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
                           f.total_seats, f.seats_taken, f.from_location, f.to_location
                    FROM bookings b
                    JOIN flights f ON b.flight_id = f.id
                    WHERE b.user_id = %s AND f.departure > NOW()
                    ORDER BY f.departure ASC
                    LIMIT 1
                    """
            cursor.execute(query, (self.user_id,))
            flight = cursor.fetchone()
            print(flight)
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
                bottom_padding = (5, 30) if i == len(details) - 1 else (5,10)

                ctk.CTkLabel(self.upcoming_flight_frame, text=label, font=("Arial", 14)).grid(
                    row=i + 1, column=0, sticky="w", padx=10, pady=bottom_padding
                )
                ctk.CTkLabel(self.upcoming_flight_frame, text=value, font=("Arial", 14)).grid(
                    row=i + 1, column=1, sticky="w", padx=10, pady=bottom_padding
                )

            self.upcoming_flight_frame.grid_columnconfigure(1, weight=1)
            self.upcoming_flight_frame.grid_columnconfigure(2, weight=1)

            flight_data = f"""
            Airline: {flight['airline']}
            Route: {flight['from_location']} → {flight['to_location']}
            Departure: {flight['departure']}
            Arrival: {flight['arrival']}
            Gate: {flight['gate']}
            Status: {flight['status']}
            Plane: {flight['plane_type']}
            Passenger: {self.username}
            """

            self.upcoming_flight_frame.update()

            # QR Code Section
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=5,
                border=2,
            )
            qr_data =  f" Airline: {flight['airline']}\nRoute: {flight['from_location']} → {flight['to_location']}\nDeparture: {flight['departure']}\nArrival: {flight['arrival']}\nGate: {flight['gate']}\nStatus: {flight['status']}\nPlane: {flight['plane_type']}\nPassenger: {self.full_name}\n"

            qr.add_data(qr_data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_bytes = io.BytesIO()
            qr_img.save(qr_bytes, format="PNG")
            qr_bytes.seek(0)
            qr_pil_image = Image.open(qr_bytes)

            self.qr_ctk_image = ctk.CTkImage(light_image=qr_pil_image, dark_image=qr_pil_image, size=(150, 150))

            self.qr_label = ctk.CTkLabel(self.upcoming_flight_frame, text="", image=self.qr_ctk_image)
            self.qr_label.grid(row=0, column=3, rowspan=6, padx=(80,80), pady=(80,80), sticky="n")
            self.lbl_scan_me = ctk.CTkLabel(self.upcoming_flight_frame,text="Scan me!")
            self.lbl_scan_me.grid(row=4, column=3, rowspan=6, padx=20, pady=15, sticky="n")


        except Exception as e:
            print("Error fetching flight data:", e)

        finally:
            cursor.close()

    def cleanup(self):
        """Clean up resources when screen is closed"""
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            if hasattr(self, 'qr_label') and self.qr_label.winfo_exists():
                self.qr_label.destroy()
            if hasattr(self, 'qr_ctk_image'):
                del self.qr_ctk_image
            if hasattr(self, 'qr_img'):
                del self.qr_img

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