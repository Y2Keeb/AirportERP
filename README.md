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
│── /src                                      # Source code (main Python)
│── /docs                                     # Documentation (wireframes, info,...)
│    ├── /grid_layout_docu                    # Documentation for the grid layout
│    ├── /icons                               # Icons used in the project
│    ├── wireframes                           # Wireframes (designs of the UI screens)
│    ├── roles_and_responsibilities.md        # Detailed breakdown of user roles and responsibilities
│    ├── DATABASE.md                          # Database schema, table structures, and relationships
│── .gitignore                                # Files to ignore in Git (like __pycache__, .idea,...)
│── LICENCE.md                                # License file describing the terms under which the project is shared
│── README.md                                 # Project description and overview
│── requirements.txt                          # Non Built-in external dependencies (e.g., bcrypt, pillow)
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

### User Interface (UI)
We will use **Tkinter** for the graphical user interface (GUI) because it is simple to implement and suitable for creating desktop applications. Tkinter allows us to create an interface quickly, which is ideal for building interactive forms, data displays, and flight management screens.

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


# TO DO
- add comments to all code
- Admin page (Thomas)
- login screen: use bcrypt to encrypt passwords of our users so its not in our DB as plain text
- user screen: add my bookings page
- user screen: if booking is found, add info on user screen 1 as a main overview
- user screen: qr code generator
- ticket system: add kill when switching from user screen to ticket finder since it now stays open.
- ticket system: add little airline icons instead of airline name in the flight finder treeview, can't get this to work just yet
- ticket system: user selects flight from available flights
- ticket system: user can add additional packages which should be added to price and database
- ticket system: user confirms - dummy payment screen
- ticket system: in background program will remove 1 available seat after user confirms from flight
  
