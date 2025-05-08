from tkinter import messagebox
from basewindow import BaseWindow
from config import set_theme,mydb
import customtkinter as ctk

class AirlineScreen(BaseWindow):
    def __init__(self, root,username=None, view_manager=None):
        super().__init__(root, "Airline Dashboard")
        self.username = username
        self.user_id = self._get_user_id()
        self.full_name = self.get_airline_name()
        self.view_state = {
            'role': 'airline'
        }
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame_content = ctk.CTkFrame(
            self.frame_main,
            border_color="black",
            border_width=3
        )
        self.frame_content.place(relx=0.5, rely=0.525, anchor="center", relwidth=0.4, relheight=0.75)
        set_theme()

        self.lbl_airline = ctk.CTkLabel(self.frame_content, text="Airline: ")
        self.lbl_from_location = ctk.CTkLabel(self.frame_content, text="From Location: ")
        self.lbl_to_location = ctk.CTkLabel(self.frame_content, text="To Location: ")
        self.lbl_departure_date = ctk.CTkLabel(self.frame_content, text="Departure date (YYYY-MM-DD): ")
        self.lbl_arrival_date = ctk.CTkLabel(self.frame_content, text="Arrival date (YYYY-MM-DD): ")
        self.lbl_plane_type = ctk.CTkLabel(self.frame_content, text="Plane Type: ")
        self.lbl_total_seats = ctk.CTkLabel(self.frame_content, text="Total Seats: ")
        self.lbl_price = ctk.CTkLabel(self.frame_content, text="Price: ")

        self.airline_entry = ctk.CTkEntry(self.frame_content, width=150)
        self.airline_entry.insert(0, self.full_name)
        self.from_location_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.to_location_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.departure_date_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.arrival_date_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.plane_type_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.total_seat_entry = ctk.CTkEntry(self.frame_content,width=150)
        self.price_entry = ctk.CTkEntry(self.frame_content,width=150)

        self.btn_offer_flight = ctk.CTkButton(self.frame_main, text="Offer Flight", command=self.complete_flight_offer)

        self.create_widgets()

    def create_widgets(self):
        greeting_label = ctk.CTkLabel(self.frame_main, text=f"Welcome {self.full_name}!\nAdd Available Flight Information Below.", font=("Arial", 20))
        greeting_label.grid(row=0, column=0, pady=15, padx=5, sticky="ew")
        #labels
        self.lbl_airline.grid(row=1, column=0,padx=15, pady=9,sticky="w")
        self.lbl_from_location.grid(row=2,column=0,padx=15,pady=9,sticky="w")
        self.lbl_to_location.grid(row=3,column=0,padx=15,pady=9,sticky="w")
        self.lbl_departure_date.grid(row=4,column=0,padx=15,pady=9,sticky="w")
        self.lbl_arrival_date.grid(row=5,column=0,padx=15,pady=9,sticky="w")
        self.lbl_plane_type.grid(row=6,column=0,padx=15,pady=9,sticky="w")
        self.lbl_total_seats.grid(row=7,column=0,padx=15,pady=9,sticky="w")
        self.lbl_price.grid(row=8,column=0,padx=15,pady=9,sticky="w")
        #entries
        self.airline_entry.grid(row=1, column=1, padx=15,pady=9,sticky="w")
        self.from_location_entry.grid(row=2, column=1, padx=15,pady=9,sticky="w")
        self.to_location_entry.grid(row=3, column=1, padx=15,pady=9,sticky="w")
        self.departure_date_entry.grid(row=4, column=1, padx=15,pady=9,sticky="w")
        self.arrival_date_entry.grid(row=5, column=1, padx=15,pady=9,sticky="w")
        self.plane_type_entry.grid(row=6, column=1, padx=15,pady=9,sticky="w")
        self.total_seat_entry.grid(row=7, column=1, padx=15,pady=9,sticky="w")
        self.price_entry.grid(row=8, column=1, padx=15,pady=9,sticky="w")
        #buttons
        self.btn_offer_flight.grid(row=2, column=0, padx=15,pady=9,sticky="sw")

    def get_airline_name(self):
        cursor = mydb.cursor()
        cursor.execute("SELECT concat(first_name,' ',last_name) FROM users WHERE id =%s", (self._get_user_id(),))
        result = cursor.fetchone()
        return result[0] if result else None

    def _get_user_id(self):
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

    def complete_flight_offer(self):
        to_location = self.to_location_entry.get()
        from_location = self.from_location_entry.get()
        departure_date = self.departure_date_entry.get()
        arrival_date = self.arrival_date_entry.get()
        plane_type = self.plane_type_entry.get()
        total_seats = self.total_seat_entry.get()
        price = self.price_entry.get()
        try:
            cursor = mydb.cursor()
            cursor.execute(
                "INSERT INTO pending_flights (airline, departure, arrival, status, plane_type,total_seats,price,from_location,to_location,submitted_by,submitted_at) "
                "VALUES (%s, %s,%s,'pending',%s,%s,%s,%s,%s,%s, NOW())",
                (self.full_name,departure_date,arrival_date,plane_type,total_seats,price,from_location,to_location,self._get_user_id())
    )
            mydb.commit()
            cursor.close()
            messagebox.showinfo("Success", "Flight offered to airport!")

        except Exception as e:
            messagebox.showinfo("Error", "An error occured")

