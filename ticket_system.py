import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from config import mydb


class TicketSystem:
    def __init__(self, root):
        self.root = root
        self.cursor = mydb.cursor()

        self.frame_search = tk.Frame(self.root)
        self.entry_from = tk.Entry(self.frame_search, width=15)
        self.entry_to = tk.Entry(self.frame_search, width=15)
        self.date_entry = DateEntry(self.frame_search, width=12, background="darkgrey", foreground="white",borderwidth=2)
        self.tree = ttk.Treeview(self.root, columns=("Airline", "From"," ", "To", "Price"), show="headings", height=6)

        self.create_widgets()

    def create_widgets(self):
        """Create UI elements for the ticket system"""
        tk.Label(self.root, text="Buy Tickets", font=("Arial", 25, "bold")).grid(row=0, column=0, pady=20, padx=20,sticky="w")
        self.frame_search.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.entry_from.insert(0, "Brussels")
        self.entry_from.grid(row=1, column=0, padx=5)

        btn_swap_to_from = tk.Button(self.frame_search, text="↔", width=3, command=self.swap_locations)
        btn_swap_to_from.grid(row=1, column=1, padx=5)

        self.entry_to.grid(row=1, column=2, padx=5)
        self.date_entry.grid(row=1, column=3, padx=5)

        btn_search = tk.Button(self.root, text="Search", command=self.fetch_flights)
        btn_search.grid(row=1, column=1, padx=20, sticky="e")

        self.tree.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        self.tree.heading("Airline", text="Airline")
        self.tree.heading("From", text="From")
        self.tree.heading(" ", text="")
        self.tree.heading("To", text="To")
        self.tree.heading("Price", text="Price")

        self.tree.column("Airline", width=150)
        self.tree.column("From", width=100)
        self.tree.column(" ", width=250)
        self.tree.column("To", width=100)
        self.tree.column("Price", width=100)

    def swap_locations(self):
        """Swap the locations in the 'From' and 'To' fields."""
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()
        self.entry_from.delete(0, tk.END)
        self.entry_from.insert(0, to_location)
        self.entry_to.delete(0, tk.END)
        self.entry_to.insert(0, from_location)

    def fetch_flights(self):
        """Fetch flights from the database based on the user's input."""
        self.tree.delete(*self.tree.get_children())
        from_location = self.entry_from.get()
        to_location = self.entry_to.get()

        sql_query = "SELECT airline, from_location, CONCAT(departure, ' - ', arrival) AS flight_schedule, to_location, price FROM flights WHERE from_location=%s AND to_location=%s"
        self.cursor.execute(sql_query, (from_location, to_location))

        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

def main():
    root = tk.Tk()
    root.title("Buy Tickets")
    root.geometry("740x500")
    ticket_system = TicketSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
