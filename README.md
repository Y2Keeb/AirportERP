# Airport ERP
Our project is an airport ERP system that digitizes and optimizes the operational processes of an airport. It provides a centralized solution for flight management and passenger handling. Many airports struggle with fragmented systems and manual processes, leading to delays, miscommunication, and operational errors. Our system centralizes and streamlines these processes to improve efficiency and safety.

### Luchthaven ERP
Ons project is een luchthaven ERP-systeem dat de operationele processen van een luchthaven digitaliseert en optimaliseert.
Het biedt een centrale oplossing voor vluchtbeheer en passagiersafhandeling.
Veel luchthavens kampen met gefragmenteerde systemen en handmatige processen, wat leidt tot vertragingen, miscommunicatie en operationele fouten.
Ons systeem centraliseert en stroomlijnt deze processen om de efficiëntie en veiligheid te verbeteren.

# File structure
```
/airportERP
│── /src                                      # Source code related to database setup (SQL scripts)
│    ├── create_tables.sql                    # SQL script to create all necessary database tables
│    ├── dummy_data.sql                       # SQL script to populate the database with dummy data
│
│── /views                                    # All UI screen modules used in the application
│    ├── __init__.py                          # Initializes the views package
│    ├── login_screen.py                      # User login screen (authentication logic)
│    ├── admin_screen.py                      # Admin dashboard for managing system operations
│    ├── staff_screen.py                      # Staff interface
│    ├── user_screen.py                       # User dashboard/home screen after login
│    ├── user_bookings_overview_screen.py     # Displays user’s booked flights and details
│    ├── ticket_booking_screen.py             # UI for selecting and booking flights
│    ├── buy_additional_packages_screen.py    # Screen for purchasing extra services (e.g., luggage, meals)
│    ├── payment_simulation.py                # Handles payment simulation logic and UI
│
│── /themes                                   # UI themes, color schemes, and styling configurations
│
│── /docs                                     # Project documentation and design resources
│    ├── wireframes                           # Wireframe images showing UI layouts
│    ├── icons                                # Custom or standard icons used in the UI
│    ├── grid_layout_docu                     # Documentation of UI grid layouts and placement logic
│    ├── roles_and_responsibilities.md        # Describes responsibilities of each user role in the system
│    ├── code_conventions.md                  # Coding standards and naming conventions for consistency
│    ├── DATABASE.md                          # Overview of database schema, ERD, and table relationships
│
│── .gitignore                                # Specifies files and folders to be ignored by Git
│── LICENCE.md                                # Open-source license for the project
│── README.md                                 # Overview of the project and main features
│── requirements.txt                          # List of Python packages required to run the app
│── basewindow.py                             # Base class/window inherited by all major screens
│── config.py                                 # Configuration settings (DB connection, theme,logging etc.)
│── main.py                                   # Application entry point; initializes and launches the UI
│── view_manager.py                           # Manages switching between UI views/screens


```
## Roles and Responsibilities
See the detailed breakdown of roles and responsibilities [here](docs/roles_and_responsibilities.md).

# Technical
### Database
We will be using **MySQL** as the relational database management system. MySQL is chosen because of its scalability, and support for complex queries, which are necessary for handling large amounts of flight and user data. Our database will include tables for users, employees, flights, and bookings, with foreign keys linking related records.

- **Users** will store passenger and admin data.
- **Employees** will store staff information.
- **Flights** will contain details on scheduled flights.
- **Bookings** will track user flight reservations.
- **Discount_codes** will track discount codes and their availability
- **Pending_flights** will track flights put up for planning by airlines


### User Interface (UI)
We will use **Custom Tkinter** for the graphical user interface (GUI) because it is simple to implement and suitable for creating desktop applications. Tkinter allows us to create an interface quickly, which is ideal for building interactive forms, data displays, and flight management screens.

Key screens include:
- **Login Page**: Allows users and admins to authenticate.
- **Flight Management Page**: For admins and flight planners to add and modify flight details.
- **User Dashboard**: Allows passengers to view flight details, book tickets, and manage bookings.

### External Packages
We will use **Pillow** for handling image processing. Specifically, we will use Pillow to load and display airline logos within the user interface. Pillow is lightweight and supports many image formats, making it ideal for our needs.

Other external libraries may include:
- **MySQL Connector**: To connect Python with our MySQL database and run SQL queries.
- **Flask**: If we decide to extend the project to include web-based functionality, Flask will provide a lightweight framework for building web pages.

### Security
Security is a priority, and we will implement the following measures:
- **Password Hashing**: All user passwords will be hashed using **bcrypt** to ensure that plain-text passwords are not stored in the database.
- **Access Control**: Different roles (Admin, User, etc.) will have access to different parts of the application, ensuring proper access control.

  
