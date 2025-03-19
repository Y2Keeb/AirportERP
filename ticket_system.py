# 🗸 search for flights based on filters.

#2 user selects flight from available flights
#3 user can add additional packages which should be added to price and database
#4 user confirms - dummy payment screen
#in background program will remove 1 available seat after user confirms from flight

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from config import mydb

cursor = mydb.cursor() #cursor nodig om SQL code te kunnen executen

root = tk.Tk()
root.title("Buy Tickets")
root.geometry("950x600")

tk.Label(root, text="Buy Tickets", font=("Arial", 25, "bold")).grid(row=0, column=0, pady=20, padx=20, sticky="w") #titel

frame_search = tk.Frame(root)
frame_search.grid(row=1, column=0, pady=10, padx=20, sticky="w") #frame in root voor search balken

entry_from = tk.Entry(frame_search, width=15)
entry_from.insert(0, "Brussels")
entry_from.grid(row=1, column=0, padx=5)

btn_swap_to_from = tk.Button(frame_search, text="↔", width=3, command=lambda: swap_locations())
btn_swap_to_from.grid(row=1, column=1, padx=5)

entry_to = tk.Entry(frame_search, width=15)
entry_to.grid(row=1, column=2, padx=5)

date_entry = DateEntry(frame_search, width=12, background="darkgrey", foreground="white", borderwidth=2)
date_entry.grid(row=1, column=3, padx=5)

btn_search = tk.Button(root, text="Search", command=lambda: fetch_flights())
btn_search.grid(row=1, column=1, padx=20, sticky="e")

columns = ("Airline", "From"," ", "To", "Price"," ")
tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
tree.grid(row=2, column=0, columnspan=2, pady=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

def swap_locations():
    from_location = entry_from.get()
    to_location = entry_to.get()

    entry_from.delete(0, tk.END)
    entry_from.insert(0, to_location)
    entry_to.delete(0, tk.END)
    entry_to.insert(0, from_location)

def fetch_flights():
    tree.delete(*tree.get_children())
    from_location = entry_from.get()
    to_location = entry_to.get()

    sql_query = "SELECT airline,from_location,CONCAT(departure, ' - ', arrival) AS flight_schedule,from_location, price FROM flights WHERE from_location=%s AND to_location=%s"
    cursor.execute(sql_query, (from_location, to_location))

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

root.mainloop()

