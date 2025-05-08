from tkinter import messagebox, Menu
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox # Corrected import casing
# Assuming BaseWindow is a simple class or you define it if needed
# from class_GUI import BaseWindow,UserScreen,AdminScreen,StaffScreen # We won't use User/Admin/StaffScreen here
from config import mydb, set_theme # Assuming these work
from PIL import Image

# --- Define BaseWindow if not imported ---
# Example placeholder if class_GUI isn't available
class BaseWindow:
    def __init__(self, root, title="Window"):
        self.root = root
        self.root.title(title)
# ------------------------------------------


# --- Copied Flight Data and Window Class ---
# You would normally import these from their own file

all_flights_data = [
    ('Brussels Airlines', '2025-07-01 08:30:00', '2025-07-01 12:45:00', 'Pending', 'Boeing 737', 150, 299.99, 'Brussels', 'Berlin', 1),
    ('Ryanair', '2025-07-02 10:15:00', '2025-07-02 12:30:00', 'Pending', 'Airbus A320', 180, 149.50, 'Brussels', 'Rome', 2),
    ('KLM', '2025-07-03 13:45:00', '2025-07-03 16:00:00', 'Pending', 'Boeing 777', 250, 399.75, 'Brussels', 'Madrid', 3),
    # Add more flights if needed
]

class FlightInfoWindow:
    def __init__(self, root, flight_info_tuple):
        self.root = root
        # --- IMPORTANT: Adjust geometry AFTER login screen is destroyed ---
        # Set geometry for the flight info window
        self.root.geometry("500x600")
        self.root.title("Flight Information") # Set title again if needed

        self.flight_data = {
            'airline': flight_info_tuple[0],
            'departure': flight_info_tuple[1],
            'arrival': flight_info_tuple[2],
            'status': flight_info_tuple[3],
            'plane_type': flight_info_tuple[4],
            'total_seats': flight_info_tuple[5],
            'price': flight_info_tuple[6],
            'from_location': flight_info_tuple[7],
            'to_location': flight_info_tuple[8],
            'flight_id': flight_info_tuple[9]
        }

        # Re-apply theme settings if necessary (usually root window keeps them)
        # self.set_theme() # Might not be needed if set globally before

        # Create the main frame for this window
        self.frame_main = ctk.CTkFrame(self.root)
        self.frame_main.pack(fill="both", expand=True, padx=5, pady=5)

        self.create_widgets()

    def set_theme(self): # Keep this method if you need specific theme changes
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

    def create_widgets(self):
        header_label = ctk.CTkLabel(self.frame_main, text="Flight Information", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=10)

        self.flight_entries = {}

        airline_frame = ctk.CTkFrame(self.frame_main)
        airline_frame.pack(fill="x", padx=20, pady=(10, 5))
        airline_label_title = ctk.CTkLabel(airline_frame, text="Airline:", font=("Helvetica", 12, "bold"), width=100, anchor='w')
        airline_label_title.pack(side="left", padx=(0, 10))
        airline_value_label = ctk.CTkLabel(airline_frame, text=self.flight_data['airline'], font=("Helvetica", 12))
        airline_value_label.pack(side="left", fill="x", expand=True)

        editable_details = [
            ("Departure", 'departure'), ("Arrival", 'arrival'), ("Status", 'status'),
            ("Plane Type", 'plane_type'), ("Total Seats", 'total_seats'),
            ("Price (€)", 'price'), ("From Location", 'from_location'), ("To Location", 'to_location')
        ]

        for label, key in editable_details:
            frame = ctk.CTkFrame(self.frame_main)
            frame.pack(fill="x", padx=20, pady=5)
            label_widget = ctk.CTkLabel(frame, text=f"{label}:", font=("Helvetica", 12), width=100, anchor='w')
            label_widget.pack(side="left", padx=(0, 10))
            entry = ctk.CTkEntry(frame, font=("Helvetica", 12))
            entry.insert(0, str(self.flight_data[key]))
            entry.pack(side="left", fill="x", expand=True)
            self.flight_entries[key] = entry

        save_button = ctk.CTkButton(self.frame_main, text="Save Changes", font=("Helvetica", 12, "bold"),
                                    command=self.save_changes)
        save_button.pack(pady=20)

    def save_changes(self):
        updated_data = {key: entry.get() for key, entry in self.flight_entries.items()}
        updated_data['airline'] = self.flight_data['airline']
        updated_data['flight_id'] = self.flight_data['flight_id']
        print("Updated Flight Information Ready to Save:")
        print(updated_data)
        print("-" * 20)

# --- End of Copied Code ---


class LoginScreen(BaseWindow):
    """Login screen class"""

    def __init__(self, root):
        # Set initial geometry for login screen
        super().__init__(root, "Login Window")
        self.root.geometry("350x550") # Login screen size

        self.frame_main = ctk.CTkFrame(self.root, border_color="black", border_width=5)
        self.frame_main.pack(fill="both", expand=True)

        # Load Image
        try:
            pil_image = Image.open("docs/icons/plane-prop.png")
            pil_image = pil_image.resize((150, 150))
            self.ctk_image = ctk.CTkImage(light_image=pil_image,
                                          dark_image=pil_image,
                                          size=(150, 150))

            self.lbl_image = ctk.CTkLabel(self.frame_main,
                                          image=self.ctk_image,
                                          text="")
            self.lbl_image.pack(pady=20)
        except FileNotFoundError:
            print("Warning: Image file 'docs/icons/plane-prop.png' not found.")
            # Optionally add a placeholder label if image fails to load
            ctk.CTkLabel(self.frame_main, text="[Image Placeholder]", font=("Arial", 10)).pack(pady=20)


        # Apply theme (ensure set_theme() is defined in config.py or here)
        try:
             set_theme() # Call theme setting function
        except NameError:
             print("Warning: set_theme() function not found. Using default theme.")
             ctk.set_appearance_mode("System") # Default
             ctk.set_default_color_theme("blue") # Default

        self.create_widgets()
        # self.create_menu() # Add menu if needed


    def create_widgets(self):
        """Creates widgets for the login screen."""
        ctk.CTkLabel(self.frame_main, text="Welcome Back!", font=("Comics-sans", 25)).pack()
        ctk.CTkLabel(self.frame_main, text="Log in to your account").pack()

        ctk.CTkLabel(self.frame_main, text="username:").pack(pady=5)
        self.entry_username = ctk.CTkEntry(self.frame_main, placeholder_text="Enter username")
        self.entry_username.pack(pady=5)

        ctk.CTkLabel(self.frame_main, text="password:").pack(pady=5)
        self.entry_password = ctk.CTkEntry(self.frame_main, show="*", placeholder_text="Enter password")
        self.entry_password.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_main, text="Login", command=self.login)
        btn_login.pack(pady=20)

    # --- create_menu, about, help_menu methods remain the same ---
    def create_menu(self):
        menubar = Menu(self.root, bg="black", fg="white", activebackground="gray", activeforeground="white")
        help_ = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="gray", activeforeground="white")
        menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Help", command=self.help_menu)
        help_.add_separator()
        help_.add_command(label="About AirportERP", command=self.about)
        self.root.config(menu=menubar)

    def about(self):
        CTkMessagebox(title="Info", message="(c) AirportERP\n BY \n Lindsey, Reza And Thomas")

    def help_menu(self):
         CTkMessagebox(title="Info", icon="question",
                       message="• Login by entering your username and password.\n"
                               "• If you don't have a login, contact your administrator.")


    # --- MODIFIED LOGIN METHOD ---
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # --- Database Check ---
        cursor = None # Initialize cursor
        try:
            if mydb and mydb.is_connected(): # Check if mydb is valid and connected
                 cursor = mydb.cursor()
                 query = "SELECT id, username, first_name, last_name, role FROM users WHERE username = %s AND password = %s"
                 # Use parameterized query to prevent SQL injection
                 cursor.execute(query, (username, password))
                 result = cursor.fetchone()
                 # print(f"DB Result for {username}: {result}") # Debug print
            else:
                 print("Error: Database connection not available.")
                 messagebox.showerror("Login Error", "Database connection unavailable.")
                 result = None # Ensure result is None if DB fails

        except Exception as e:
             print(f"Database error during login: {e}")
             messagebox.showerror("Login Error", f"An error occurred during login: {e}")
             result = None # Ensure result is None on DB error
        finally:
             if cursor:
                 cursor.close() # Always close the cursor
        # -----------------------


        if result:
            # --- SUCCESSFUL LOGIN ---
            print(f"Login successful for user: {username}, Role: {result[4]}") # Debug print

            # 1. Destroy the current login frame
            self.frame_main.pack_forget() # Hide the frame
            self.frame_main.destroy()     # Destroy the frame and its widgets

            # 2. Select the flight data to display (e.g., the first flight)
            #    In a real app, you might fetch user-specific data here
            selected_flight_data = all_flights_data[0] # Display the first flight

            # 3. Create the FlightInfoWindow
            #    The FlightInfoWindow's __init__ should handle setting the new geometry
            FlightInfoWindow(self.root, selected_flight_data)

            # ---- OLD Role-based logic (REMOVED) ----
            # role = result[4]
            # if role == "admin":
            #     AdminScreen(self.root)
            # elif role == "staff":
            #     StaffScreen(self.root)
            # else:
            #     UserScreen(self.root,username)
            # ------------------------------------

        else:
            # --- FAILED LOGIN ---
            print(f"Login failed for user: {username}") # Debug print
            # Use CTkMessagebox for consistent look
            CTkMessagebox(title="Login Failed", message="Invalid username or password.", icon="cancel")
            # tk.messagebox.showerror("Login Failed", "Invalid username or password.")


if __name__ == "__main__":
    # Use CTk main window for consistency
    root = ctk.CTk() # Changed from tk.Tk()
    app = LoginScreen(root)
    # Bind Enter key to login function
    root.bind("<Return>", lambda event: app.login()) # Simplified binding slightly
    root.mainloop()
