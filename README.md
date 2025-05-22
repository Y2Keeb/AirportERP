# Airport ERP

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
Our project is an airport ERP system that digitizes and optimizes the operational processes of an airport. It provides a centralized solution for flight management and passenger handling. Many airports struggle with fragmented systems and manual processes, leading to delays, miscommunication, and operational errors. Our system centralizes and streamlines these processes to improve efficiency and safety.

## Luchthaven ERP

Ons project is een luchthaven ERP-systeem dat de operationele processen van een luchthaven digitaliseert en optimaliseert.
Het biedt een centrale oplossing voor vluchtbeheer en passagiersafhandeling.
Veel luchthavens kampen met gefragmenteerde systemen en handmatige processen, wat leidt tot vertragingen, miscommunicatie en operationele fouten.
Ons systeem centraliseert en stroomlijnt deze processen om de efficiëntie en veiligheid te verbeteren.

## File structure

```plaintext
# File structure
/airportERP
│── /src                                      # Source code related to database setup (SQL scripts)
│    ├── create_tables.sql                    # SQL script to create all necessary database tables
│    ├── dummy_data.sql                       # SQL script to populate the database with dummy data
│
│── /views
│   ├── __init__.py                           # Initializes the views package
│   ├── admin_screen.py                       # Admin screen for managing users and flights
│   ├── airline_screen.py                     # Airline screen for managing flights and bookings
│   ├── bjorn_easter_egg.py                   # Easter egg screen for Bjorn to find
│   ├── buy_additional_packages_screen.py     # Screen for purchasing additional packages
│   ├── flight_planner_screen.py              # Flight planning and scheduling interface for airlines
│   ├── kiosk_screen.py                       # Kiosk interface for self-service check-in and boarding
│   ├── login_screen.py                       # User login screen
│   ├── payment_simulation.py                 # Handles payment simulation logic and UI
│   ├── splash_screen.py                      # Splash screen displayed before app startup
│   ├── ticket_booking_screen.py              # UI for selecting and booking flights
│   ├── user_bookings_overview_screen.py      # Displays user’s booked flights and details
│   └── user_screen.py                        # User dashboard/home screen after login
│
│── /themes                                   # UI themes, color schemes, and styling configurations
│
│── /docs                                     # Project documentation and design resources
│    ├── wireframes                           # Wireframe images showing UI layouts
│    ├── icons                                # Icons used in the UI
│    ├── grid_layout_docu                     # Documentation of UI grid layouts and placement logic
│    ├── roles_and_responsibilities.md        # Describes responsibilities of each user role in the system
│    ├── code_conventions.md                  # Coding standards and naming conventions for consistency
│    ├── DATABASE.md                          # Overview of database schema, ERD, and table relationships
│
├── .gitignore
├── app.log                                   # Log file for application events and errors
├── basewindow.py                             # Base window class for the application
├── baggage.py                                # Handles baggage management and tracking
├── config.py                                 # Configuration file for application settings and constants
├── LICENSE                                   # License file for the project
├── main.py                                   # Main entry point for the application
├── password_encrypter.py                     # a CLI tool for password encryption and decryption
├── README.md                                 # Project Readme file
├── requirements.txt                          # List of required Python packages and dependencies
├── scan_qr.py                                # QR code scanning functionality for boarding passes
├── theme_demo.py                             # Demo for theme usage and customization
├── ui_helpers.py                             # Helper functions for UI components and layouts
├── view_manager.py                           # Manages transitions and interactions between different views

```

## Roles and Responsibilities

See the detailed breakdown of roles and responsibilities [here](docs/roles_and_responsibilities.md).

## Technical

### Database

[![MySQL](https://img.shields.io/badge/MySQL-8.0.28-blue.svg)](https://dev.mysql.com/downloads/mysql/)

We will be using **MySQL** as the relational database management system. MySQL is chosen because of its scalability, and support for complex queries, which are necessary for handling large amounts of flight and user data. Our database will include tables for users, employees, flights, and bookings, with foreign keys linking related records.

- **Users** will store passenger and admin data.
- **Employees** will store staff information.
- **Flights** will contain details on scheduled flights.
- **Bookings** will track user flight reservations.
- **Discount_codes** will track discount codes and their availability
- **Pending_flights** will track flights put up for planning by airlines

### User Interface (UI)

[![Tkinter](https://img.shields.io/badge/Tkinter-8.6-blue.svg)](https://www.python.org/downloads/release/python-368/)
[![Custom Tkinter](https://img.shields.io/badge/Custom%20Tkinter-0.3.2-blue.svg)](https://github.com/TomSchimansky/CustomTkinter)

We will use **Custom Tkinter** for the graphical user interface (GUI) because it is simple to implement and well-suited for creating desktop applications. Tkinter allows for rapid development of interactive forms, data displays, and flight management screens.

Our application follows a **Model-View-Controller (MVC)** architecture. In this setup:

- **Models** handle the core data and logic (e.g., flight data, user info, bookings).
- **Views** represent individual screens (e.g., login screen, booking page, payment screen).
- A custom **ViewManager** acts as the controller and navigator, managing transitions between views and ensuring a modular, maintainable structure.

This pattern keeps our code organized and scalable, making it easier to update or expand the system as needed.

### External Packages

[![Pillow](https://img.shields.io/badge/Pillow-8.4.0-blue.svg)](https://python-pillow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-blue.svg)](https://flask.palletsprojects.com/)
[![MySQL Connector](https://img.shields.io/badge/MySQL%20Connector-8.0.26-blue.svg)](https://dev.mysql.com/downloads/connector/python/)

We will use **Pillow** for handling image processing. Specifically, we will use Pillow to load and display airline logos within the user interface. Pillow is lightweight and supports many image formats, making it ideal for our needs.

Other external libraries may include:

- **MySQL Connector**: To connect Python with our MySQL database and run SQL queries.
- **Flask**: If we decide to extend the project to include web-based functionality, Flask will provide a lightweight framework for building web pages.

### Security

[![Cryptography](https://img.shields.io/badge/Cryptography-3.4.7-blue.svg)](https://cryptography.io/en/latest/)
Security is a priority, and we will implement the following measures:

- **Password Hashing**: All user passwords will be hashed using **Fernet** a part of the **Cryptography** library for Python to ensure that plain-text passwords are not stored in the database.
- **Access Control**: Different roles (Admin, User, etc.) will have access to different parts of the application, ensuring proper access control.
