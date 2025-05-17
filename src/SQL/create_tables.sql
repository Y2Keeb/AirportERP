CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'admin', 'staff','kiosk','airline')),
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
    total_price DECIMAL(10,2) NOT NULL,
	status VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(50) NULL,
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



-- DELETE ALL TABLES FROM DATABSE TO RENEW DATABASE, WARNING ALL TABLES WILL BE DELETED 
SET FOREIGN_KEY_CHECKS = 0;
SET GROUP_CONCAT_MAX_LEN=32768;

SELECT CONCAT('DROP TABLE IF EXISTS ', GROUP_CONCAT(table_name), ';') 
INTO @drop_sql
FROM information_schema.tables 
WHERE table_schema = 'airport';

PREPARE stmt FROM @drop_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SET FOREIGN_KEY_CHECKS = 1;