# Database Schema
## Overview
This document provides an overview of the database structure used in the Airport ERP System. The database stores all essential data related to users, employees, flights, and bookings, ensuring that all operations are efficiently handled and queried.

---

## 1. Users Table
Stores user login details

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each user             |
| `username`      | VARCHAR(255)  | Unique username for login                        |
| `first_name`    | VARCHAR(255)  | User's first name                                |
| `last_name`     | VARCHAR(255)  | User's last name                                 |
| `role`          | VARCHAR(50)   | Role of the user (e.g., user, admin, staff)      |
| `password`      | VARCHAR(255)  | Password for authentication                      |

---

## 2. Employees Table
Stores employee details (staff, managers, etc.).

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each employee         |
| `username`      | VARCHAR(255)  | Employee's username                              |
| `job_team`      | VARCHAR(255)  | Job position or team the employee is part of     |
| `salary`        | DECIMAL(10,2) | Employee's salary                                |

---

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
| `price`         | FLOAT         | Price of this flight                             |
| `from_location` | VARCHAR(255)  | Departure location of the flight                 |
| `to_location`   | VARCHAR(255)  | Arrival location of the flight                   |
| `airline_icon`  | VARCHAR(255)  | Path of airline icon                             |

---

## 4. Bookings Table
Tracks flight bookings by users.

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each booking          |
| `user_id`       | INTEGER       | Foreign Key referencing `id` in Users table      |
| `flight_id`     | INTEGER       | Foreign Key referencing `id` in Flights table    |
| `booking_date`  | DATETIME      | Date and time the booking was made               |
| `seat_class`    | VARCHAR(50)   | Class of seat (Economy, Business, etc.)          |

---

## 5. Pending Flights Table
Stores flight proposals awaiting approval.

| Column Name     | Data Type     | Description                                      |
|-----------------|---------------|--------------------------------------------------|
| `id`            | INTEGER       | Primary Key, Unique ID for each pending flight   |
| `airline`       | VARCHAR(255)  | Proposed airline company name                    |
| `departure`     | DATETIME      | Proposed departure date and time                 |
| `arrival`       | DATETIME      | Proposed arrival date and time                   |
| `status`        | VARCHAR(50)   | Approval status (default: 'Pending')             |
| `plane_type`    | VARCHAR(50)   | Proposed aircraft type                           |
| `total_seats`   | INTEGER       | Proposed total seats                             |
| `price`         | FLOAT         | Proposed price                                   |
| `from_location` | VARCHAR(255)  | Proposed departure location                      |
| `to_location`   | VARCHAR(255)  | Proposed arrival location                        |
| `submitted_by`  | INTEGER       | Foreign Key referencing `id` in Users table      |
| `submitted_at`  | TIMESTAMP     | Timestamp when flight was proposed               |

---

## 6. Discount Codes Table
Manages promotional discount codes.

| Column Name        | Data Type     | Description                                      |
|--------------------|---------------|--------------------------------------------------|
| `id`               | INTEGER       | Primary Key, Unique ID for each code             |
| `code`             | VARCHAR(20)   | Unique discount code (case-sensitive)            |
| `discount_percent` | DECIMAL(5,2)  | Percentage discount (e.g., 10.00 for 10%)        |
| `valid_from`       | DATE          | Date when code becomes active                    |
| `valid_until`      | DATE          | Date when code expires                           |
| `max_uses`         | INTEGER       | Maximum number of times code can be used         |
| `current_uses`     | INTEGER       | Number of times code has been used               |
| `is_active`        | BOOLEAN       | Whether code is currently active                 |

---

## Relationships
- **Users** can be linked to **Employees** if they have a staff role
- A **Flight** can have multiple **Bookings**
- A **User** can have multiple **Bookings**
- A **User** can submit multiple **Pending Flights**
- A **Discount Code** can be applied to multiple **Bookings** (tracked via current_uses)
- **Pending Flights** can be approved and moved to the **Flights** table

---

