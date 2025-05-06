INSERT INTO flights (airline, departure, arrival, status, gate, plane_type, total_seats, seats_taken, price, from_location, to_location, airline_icon) VALUES
('Brussels Airlines', '2025-06-01 06:30:00', '2025-06-01 07:45:00', 'On Time', 'A1', 'Airbus A319', 120, 45, 159.99, 'Brussels', 'Paris', 'docs/icons/brussels_airlines.png'),
('Ryanair', '2025-06-01 09:30:00', '2025-06-01 11:45:00', 'Delayed', 'B3', 'Airbus A320', 180, 30, 259.50, 'Brussels', 'Paris', 'docs/icons/ryanair.png'),
('Air France', '2025-06-01 13:15:00', '2025-06-01 14:30:00', 'On Time', 'C2', 'Embraer 190', 100, 75, 189.00, 'Brussels', 'Paris', 'docs/icons/air_france.png'),
('Ryanair', '2025-06-02 07:00:00', '2025-06-02 09:15:00', 'On Time', 'D4', 'Boeing 737', 160, 90, 149.99, 'Brussels', 'Paris', 'docs/icons/ryanair.png'),
('Brussels Airlines', '2025-06-02 16:45:00', '2025-06-02 18:00:00', 'On Time', 'E5', 'Airbus A320', 180, 110, 219.50, 'Brussels', 'Paris', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to London on different dates
('British Airways', '2025-06-01 08:15:00', '2025-06-01 08:45:00', 'On Time', 'F6', 'Airbus A320', 150, 60, 179.00, 'Brussels', 'London', 'docs/icons/british_airways.png'),
('Air France', '2025-06-01 12:30:00', '2025-06-01 13:00:00', 'On Time', 'G7', 'Embraer 190', 100, 40, 199.00, 'Brussels', 'London', 'docs/icons/air_france.png'),
('Ryanair', '2025-06-02 10:45:00', '2025-06-02 11:15:00', 'Delayed', 'H8', 'Boeing 737', 160, 85, 129.99, 'Brussels', 'London', 'docs/icons/ryanair.png'),
('Brussels Airlines', '2025-06-02 18:00:00', '2025-06-02 18:30:00', 'On Time', 'I9', 'Airbus A319', 120, 95, 209.50, 'Brussels', 'London', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to Amsterdam on different dates
('KLM', '2025-06-01 07:00:00', '2025-06-01 07:45:00', 'On Time', 'J10', 'Embraer 175', 80, 30, 129.00, 'Brussels', 'Amsterdam', 'docs/icons/klm.png'),
('KLM', '2025-06-01 14:00:00', '2025-06-01 14:45:00', 'On Time', 'K11', 'Boeing 737', 160, 110, 149.00, 'Brussels', 'Amsterdam', 'docs/icons/klm.png'),
('Brussels Airlines', '2025-06-02 09:30:00', '2025-06-02 10:15:00', 'On Time', 'L12', 'Airbus A320', 180, 65, 139.99, 'Brussels', 'Amsterdam', 'docs/icons/brussels_airlines.png'),
('KLM', '2025-06-02 17:45:00', '2025-06-02 18:30:00', 'On Time', 'M13', 'Embraer 190', 100, 45, 159.00, 'Brussels', 'Amsterdam', 'docs/icons/klm.png'),
-- Multiple long-haul flights to New York
('Brussels Airlines', '2025-06-01 09:00:00', '2025-06-01 12:30:00', 'On Time', 'N14', 'Airbus A330', 220, 150, 599.00, 'Brussels', 'New York', 'docs/icons/brussels_airlines.png'),
('Delta', '2025-06-01 15:30:00', '2025-06-01 19:00:00', 'On Time', 'O15', 'Boeing 767', 240, 180, 649.00, 'Brussels', 'New York', 'docs/icons/delta.png'),
('United', '2025-06-02 10:45:00', '2025-06-02 14:15:00', 'On Time', 'P16', 'Boeing 787', 210, 120, 579.00, 'Brussels', 'New York', 'docs/icons/united.png'),
-- Multiple flights to Barcelona
('Ryanair', '2025-06-01 11:00:00', '2025-06-01 13:15:00', 'On Time', 'Q17', 'Boeing 737', 160, 95, 189.99, 'Brussels', 'Barcelona', 'docs/icons/ryanair.png'),
('Vueling', '2025-06-01 18:30:00', '2025-06-01 20:45:00', 'On Time', 'R18', 'Airbus A320', 180, 110, 219.00, 'Brussels', 'Barcelona', 'docs/icons/vueling.png'),
('Brussels Airlines', '2025-06-02 08:15:00', '2025-06-02 10:30:00', 'On Time', 'S19', 'Airbus A319', 120, 75, 229.50, 'Brussels', 'Barcelona', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to Rome
('Ryanair', '2025-06-01 07:45:00', '2025-06-01 10:00:00', 'On Time', 'T20', 'Boeing 737', 160, 85, 179.99, 'Brussels', 'Rome', 'docs/icons/ryanair.png'),
('Alitalia', '2025-06-01 16:00:00', '2025-06-01 18:15:00', 'On Time', 'U21', 'Airbus A320', 180, 120, 249.00, 'Brussels', 'Rome', 'docs/icons/alitalia.png'),
('Brussels Airlines', '2025-06-02 13:30:00', '2025-06-02 15:45:00', 'On Time', 'V22', 'Airbus A320', 180, 65, 259.50, 'Brussels', 'Rome', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to Berlin
('Lufthansa', '2025-06-01 10:15:00', '2025-06-01 11:30:00', 'On Time', 'W23', 'Embraer 190', 100, 40, 169.00, 'Brussels', 'Berlin', 'docs/icons/lufthansa.png'),
('Eurowings', '2025-06-01 19:45:00', '2025-06-01 21:00:00', 'On Time', 'X24', 'Airbus A319', 120, 85, 149.99, 'Brussels', 'Berlin', 'docs/icons/eurowings.png'),
('Brussels Airlines', '2025-06-02 11:00:00', '2025-06-02 12:15:00', 'On Time', 'Y25', 'Airbus A320', 180, 55, 179.50, 'Brussels', 'Berlin', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to Madrid
('Iberia', '2025-06-01 08:30:00', '2025-06-01 10:45:00', 'On Time', 'Z26', 'Airbus A320', 180, 95, 199.00, 'Brussels', 'Madrid', 'docs/icons/iberia.png'),
('Ryanair', '2025-06-01 17:15:00', '2025-06-01 19:30:00', 'On Time', 'A27', 'Boeing 737', 160, 110, 169.99, 'Brussels', 'Madrid', 'docs/icons/ryanair.png'),
('Brussels Airlines', '2025-06-02 14:45:00', '2025-06-02 17:00:00', 'On Time', 'B28', 'Airbus A319', 120, 70, 229.50, 'Brussels', 'Madrid', 'docs/icons/brussels_airlines.png'),
-- Multiple flights to Lisbon
('TAP Portugal', '2025-06-01 09:45:00', '2025-06-01 12:00:00', 'On Time', 'C29', 'Airbus A320', 180, 60, 219.00, 'Brussels', 'Lisbon', 'docs/icons/tap_portugal.png'),
('Ryanair', '2025-06-01 20:30:00', '2025-06-01 22:45:00', 'On Time', 'D30', 'Boeing 737', 160, 90, 179.99, 'Brussels', 'Lisbon', 'docs/icons/ryanair.png'),
('Brussels Airlines', '2025-06-02 12:15:00', '2025-06-02 14:30:00', 'On Time', 'E31', 'Airbus A320', 180, 45, 239.50, 'Brussels', 'Lisbon', 'docs/icons/brussels_airlines.png');
INSERT INTO users (id, username, first_name, last_name, role, password) VALUES
(1, 'admin', 'Alice', 'Smith', 'admin', 'admin'),
(2, 'admin2', 'Bob', 'Johnson', 'admin', 'secureadmin456'),
(3, 'staff1', 'Charlie', 'Brown', 'staff', 'staffpass789'),
(4, 'staff2', 'Diana', 'Miller', 'staff', 'passwordstaff'),
(5, 'user1', 'Eve', 'Davis', 'user', 'userpass123'),
(6, 'user2', 'Frank', 'Wilson', 'user', 'letmein456'),
(7, 'user3', 'Grace', 'Lee', 'user', 'mypassword'),
(8, 'staff3', 'Henry', 'Moore', 'staff', 'flightstaff2025'),
(9, 'admin3', 'Isabel', 'Taylor', 'admin', 'rootadmin987'),
(10, 'user4', 'Jack', 'Anderson', 'user', 'welcomeuser'),
(11, 'KIOSK5', 'kiosk', 'kiosk', 'kiosk', 'kiosklogin123');
INSERT INTO pending_flights (airline, departure, arrival, status, plane_type, total_seats, price, from_location, to_location, submitted_by)
VALUES
('Brussels Airlines', '2025-07-01 08:30:00', '2025-07-01 12:45:00', 'Pending', 'Boeing 737', 150, 299.99, 'Brussels', 'Berlin', 1),
('Ryanair', '2025-07-02 10:15:00', '2025-07-02 12:30:00', 'Pending', 'Airbus A320', 180, 149.50, 'Brussels', 'Rome', 2),
('KLM','2025-07-03 13:45:00', '2025-07-03 16:00:00', 'Pending', 'Boeing 777', 250, 399.75, 'Brussels', 'Madrid', 3),
('Turkish Airlines', '2025-07-04 17:30:00', '2025-07-04 21:00:00', 'Pending', 'Airbus A330', 200, 275.00, 'Brussels', 'Istanbul', 4),
('Emirates', '2025-07-05 22:00:00', '2025-07-06 02:30:00', 'Pending', 'Boeing 787', 220, 599.99, 'Brussels', 'Dubai', 5);
INSERT INTO discount_codes (code, discount_percent, valid_from, valid_until, max_uses, is_active) 
VALUES 
    ('WELCOME10', 10.00, '2025-01-01', '2025-12-31', 100, TRUE),
    ('SUMMER20', 20.00, '2025-06-01', '2025-08-31', 50, TRUE),
    ('FLY15', 15.00, '2025-01-01', '2025-12-31', NULL, TRUE), -- Unlimited uses
    ('EXPIRED5', 5.00, '2023-01-01', '2023-12-31', 200, TRUE), -- Expired code
    ('INACTIVE25', 25.00, '2025-01-01', '2025-12-31', 30, FALSE), -- Inactive code
    ('ONETIME50', 50.00, '2025-01-01', '2025-12-31', 1, TRUE), -- Single use only
    ('WEEKEND10', 10.00, '2025-01-01', '2025-12-31', NULL, TRUE),
    ('BUSINESS15', 15.00, '2025-01-01', '2025-12-31', 100, TRUE),
    ('STUDENT20', 20.00, '2025-09-01', '2025-12-31', 200, TRUE), -- Valid only in second half of year
    ('FREQUENT25', 25.00, '2025-01-01', '2025-12-31', 10, TRUE); -- Limited to 10 uses