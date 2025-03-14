# Database Schema

## 1. Users Table
Stores user login details

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each user             |
| `Username`      | VARCHAR(255)  | Unique username for login                        |
| `First name`    | VARCHAR(255)  | User's first name                                |
| `Last name`     | VARCHAR(255)  | User's last name                                 |
| `Role`          | VARCHAR(50)   | Role of the user (e.g., user, admin, staff)      |
| `Password`      | VARCHAR(255)  | Password for authentication                      |

## 2. Employees Table
Stores employee details (staff, managers, etc.).

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each employee         |
| `Username`      | VARCHAR(255)  | Employee's username                              |
| `Job/Team`      | VARCHAR(255)  | Job position or team the employee is part of     |
| `Salary`        | DECIMAL(10,2) | Employee's salary                                |

## 3. Flights Table
Tracks flight information.

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each flight           |
| `airline`       | VARCHAR(255)  | Airline company name                             |
| `departure`     | DATETIME      | Scheduled departure date and time                |
| `arrival`       | DATETIME      | Scheduled arrival date and time                  |
| `status`        | VARCHAR(50)   | Current flight status (e.g., On Time, Delayed)   |
| `gate`          | VARCHAR(50)   | Gate number for the flight                       |
| `plane_type`    | VARCHAR(50)   | Type of aircraft (e.g., Airbus A320)             |
| `total_seats`   | INTEGER       | Total number of seats on the flight              |
| `seats_taken`   | INTEGER       | Number of seats already booked                   |

## Relationships
- A **User** can be linked to **Employees** if they have a staff role.
- A **Flight** can have multiple **Bookings** (TO DO)
