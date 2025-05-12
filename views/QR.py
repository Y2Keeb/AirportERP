import customtkinter as ctk # Make sure ctk is the alias for customtkinter
from tkinter import ttk, messagebox
from PIL import Image # Keep PIL.Image for generating/resizing
# Remove ImageTk import if no longer needed elsewhere
# from PIL import ImageTk
import qrcode
from urllib.parse import urlencode

# Assuming these are correctly defined elsewhere
from basewindow import BaseWindow
from config import mydb, get_logger
# from views.user_screen import UserScreen # Keep if needed

logger = get_logger(__name__)

class MyBookings(BaseWindow):
    # ... (keep __init__, _create_bookings_table, _load_bookings, _handle_back, cleanup as before) ...

    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, f"My Bookings - {username}" if username else "My Bookings")
        self.user_id = user_id
        self.username = username
        self.view_manager = view_manager
        self.qr_img = None # Initialize instance variable - will hold CTkImage

        self.view_state = {
            'user_id': user_id,
            'username': username
        }

        # --- Main Frame Setup ---
        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # --- Widgets ---
        btn_back = ctk.CTkButton(
            self.frame_main,
            text="← Back to Dashboard",
            command=self._handle_back,
            fg_color="transparent",
            border_width=1
        )
        btn_back.pack(anchor="ne", pady=10, padx=10)

        ctk.CTkLabel(
            self.frame_main,
            text="My Bookings",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 10))

        # --- Bookings Table ---
        self._create_bookings_table()
        self._load_bookings()

        # --- Prepare QR Code Data (as a URL) ---
        qr_url_data = "https://example.com/no_user_info" # Default/fallback URL
        if self.user_id and self.username:
            base_url = "https://my-dummy-flightapp.test/show_booking_user" # <<< CHANGE THIS BASE URL
            params = {'user': self.username, 'id': str(self.user_id)}
            query_string = urlencode(params)
            full_url = f"{base_url}?{query_string}"
            qr_url_data = full_url
            logger.info(f"Generated QR code URL: {qr_url_data}")
        else:
            logger.warning("User ID or Username missing, using default QR URL.")

        # --- Add QR Code (containing the URL) to the GUI ---
        self._add_qr_code(data=qr_url_data)

    # --- Definition for _create_bookings_table here ---
    def _create_bookings_table(self):
        # ... (code as before) ...
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            style.theme_use('default')

        style.configure("Treeview", rowheight=30, font=("Helvetica", 10), background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#3c3c3c", foreground="white")
        style.map("Treeview", background=[('selected', '#555555')])

        columns = [("Airline", 150), ("Departure", 150), ("From", 120), ("To", 120), ("Status", 100)]

        table_frame = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=[col[0] for col in columns], show="headings", height=15, selectmode="browse", style="Treeview")

        for col_name, width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")


    # --- Definition for _load_bookings here ---
    def _load_bookings(self):
        # ... (code as before) ...
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.user_id:
             logger.warning("Cannot load bookings: user_id is not set.")
             return

        try:
            cursor = mydb.cursor(dictionary=True)
            query = """
                SELECT b.id, f.airline as flight, f.departure, f.from_location, f.to_location, b.status
                FROM bookings b JOIN flights f ON b.flight_id = f.id
                WHERE b.user_id = %s ORDER BY f.departure DESC
            """
            cursor.execute(query, (self.user_id,))
            bookings = cursor.fetchall()

            if not bookings:
                logger.info(f"No bookings found for user_id {self.user_id}")
                return

            for booking in bookings:
                departure_str = booking["departure"].strftime('%Y-%m-%d %H:%M') if hasattr(booking["departure"], 'strftime') else str(booking["departure"])
                self.tree.insert("", "end", values=(
                    booking["flight"], departure_str, booking["from_location"],
                    booking["to_location"], booking["status"]
                ), iid=booking["id"])

        except Exception as e:
            logger.error(f"Error loading bookings for user_id {self.user_id}: {e}")
            messagebox.showerror("Database Error", f"Failed to load bookings.\nError: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                 cursor.close()


    # MODIFIED METHOD
    def _add_qr_code(self, data="https://example.com/error"):
        """Generates and displays a QR code using CTkImage."""
        try:
            # 1. Generate PIL Image using qrcode library
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3, # This controls the raw pixel size in the PIL image
                border=2
            )
            qr.add_data(data)
            qr.make(fit=True)
            img_qr_pil = qr.make_image(fill_color="black", back_color="white").convert("RGB") # Ensure RGB

            # --- CHANGE IS HERE ---
            # 2. Define the desired display size
            display_size = (90, 90) # The size you want it to appear in the GUI

            # 3. Create CTkImage from the PIL Image
            #    We provide the same PIL image for both light and dark mode
            #    since the QR code itself is black/white.
            #    CTkImage handles the scaling.
            self.qr_img = ctk.CTkImage(light_image=img_qr_pil,
                                       dark_image=img_qr_pil,  # Can use the same for b/w
                                       size=display_size)
            # --- END OF CHANGE ---

            # 4. Display using CTkLabel (this part remains the same)
            if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
                # Pass the CTkImage object stored in self.qr_img
                qr_label = ctk.CTkLabel(self.frame_main, image=self.qr_img, text="") # No change here
                qr_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
            else:
                logger.error("Cannot add QR code: main frame does not exist.")

        except Exception as e:
            logger.error(f"Failed to generate or display QR code for data '{data}': {e}")


    # --- Definition for _handle_back here ---
    def _handle_back(self):
        # ... (code as before) ...
        if self.view_manager:
            self.view_manager.pop_view()
        else:
            logger.warning("No view manager found for back navigation.")
            self.frame_main.destroy()
            # from views.user_screen import UserScreen
            # UserScreen(self.root, username=self.username, user_id=self.user_id)


    # --- Definition for cleanup here ---
    def cleanup(self):
        # ... (code as before) ...
        logger.debug(f"Cleaning up MyBookings view for user {self.username}")
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()
        self.qr_img = None # Clear reference