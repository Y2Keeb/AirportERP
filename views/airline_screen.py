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
        set_theme()

        self.lbl_airline = ctk.CTkLabel(self.frame_main, text="Airline: ")
        self.airline_entry = ctk.CTkEntry(self.frame_main, width=150)
        self.airline_entry.insert(0, self.full_name)
        self.lbl_from_location = ctk.CTkLabel(self.frame_main, text="From Location: ")
        self.lbl_to_location = ctk.CTkLabel(self.frame_main, text="To Location: ")

        self.create_widgets()

    def create_widgets(self):
        greeting_label = ctk.CTkLabel(self.frame_main, text=f"Welcome {self.full_name}!\nAdd New Flight Information!", font=("Arial", 20))
        greeting_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.lbl_airline.grid(row=1, column=0,padx=10, pady=10,sticky="w")
        self.airline_entry.grid(row=1, column=1, padx=10,pady=10,sticky="w")
        self.lbl_from_location.grid(row=2,column=0,padx=10,pady=10,sticky="w")
        self.lbl_to_location.grid(row=3,column=0,padx=10,pady=10,sticky="w")


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
"""
'from_location'
'to_location'
'departure date'
'arrival date'
'plane_type'
'total_seats'
'price'
'flight_id'
"""