CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'admin', 'staff')),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    job_team VARCHAR(255) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    airline VARCHAR(255) NOT NULL,
    departure DATETIME NOT NULL,
    arrival DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    gate VARCHAR(50) NOT NULL,
    plane_type VARCHAR(50) NOT NULL,
    total_seats INTEGER NOT NULL CHECK (total_seats > 0),
    seats_taken INTEGER NOT NULL DEFAULT 0,
    price FLOAT NOT NULL,
    from_location VARCHAR(255) NOT NULL,
    to_location VARCHAR(255) NOT NULL
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES Flights(id) ON DELETE CASCADE
);
ALTER TABLE flights ADD COLUMN airline_icon VARCHAR(255) NOT NULL;


