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
    to_location VARCHAR(255) NOT NULL,
    airline_icon VARCHAR(255) NOT NULL
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

CREATE TABLE pending_flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(255) NOT NULL,
    departure DATETIME NOT NULL,
    arrival DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    plane_type VARCHAR(50),
    total_seats INT NOT NULL,
    price FLOAT NOT NULL,
    from_location VARCHAR(255) NOT NULL,
    to_location VARCHAR(255) NOT NULL,
    submitted_by INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submitted_by) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE discount_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    discount_percent DECIMAL(5,2) NOT NULL,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    max_uses INT DEFAULT NULL,
    current_uses INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

