import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

# Dummy flight data based on the provided SQL insert
flight_data = [
    {"flight_id": "12345", "day": "2025-05-01", "hour": "08:00:00", "destination": "Los Angeles", "airline": "Brussels Airlines"},
    {"flight_id": "12346", "day": "2025-05-01", "hour": "09:30:00", "destination": "Paris", "airline": "Ryanair"},
    {"flight_id": "12347", "day": "2025-05-02", "hour": "14:00:00", "destination": "Amsterdam", "airline": "KLM"},
    # Add all your flight data here from the SQL example
]

def generate_qr_code(data):
    """Generate a QR code from the provided data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

def open_flight_info(frame, flight_info):
    """Display flight info after QR scan."""
    # Clear the frame before adding the new data
    for widget in frame.winfo_children():
        widget.destroy()

    # Create labels for flight information
    tk.Label(frame, text="Flight Information", font=("Helvetica", 16, "bold")).pack(pady=10)

    for key, value in flight_info.items():
        tk.Label(frame, text=f"{key}: {value}", font=("Helvetica", 12)).pack(pady=5)

    # Add a manage flight button
    manage_button = tk.Button(frame, text="Manage Flight", command=lambda: manage_flight(frame))
    manage_button.pack(pady=20)

    # Add a help button
    help_button = tk.Button(frame, text="Help", command=show_help)
    help_button.pack(pady=10)

def manage_flight(frame):
    """Manage flight functionality (for now just a message)."""
    messagebox.showinfo("Manage Flight", "This is where you can manage your flight.")

def show_help():
    """Show help information."""
    messagebox.showinfo("Help", "To manage your flight, use the 'Manage Flight' button. If you need further assistance, please contact customer service.")

def on_qr_scan(frame, qr_code_data):
    """Simulate QR scan and show flight information."""
    # Extract relevant flight info (based on the scanned QR code)
    flight_info = flight_data[int(qr_code_data)]  # Assuming qr_code_data is the index or ID of the flight
    open_flight_info(frame, flight_info)

# Main window setup
root = tk.Tk()
root.title("Flight Information")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

# Create QR code for a specific flight (for example, flight 1)
qr_code_data = "0"  # Example: data for the first flight in the list
qr_img = generate_qr_code(qr_code_data)

qr_img_tk = ImageTk.PhotoImage(qr_img)

# Create label for QR code
qr_label = tk.Label(frame, image=qr_img_tk)
qr_label.pack(pady=10)

# Add a button to simulate QR scan
scan_button = tk.Button(frame, text="Scan QR", command=lambda: on_qr_scan(frame, qr_code_data))
scan_button.pack(pady=20)

# Run the application
root.mainloop()
