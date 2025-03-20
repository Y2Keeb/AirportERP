INSERT INTO flights (airline, departure, arrival, status, gate, plane_type, total_seats, seats_taken, price, from_location, to_location, airline_icon) VALUES
('Brussels Airlines', '2025-05-01 08:00:00', '2025-05-01 12:00:00', 'On Time', 'A1', 'Boeing 737', 150, 50, 199.99, 'Brussels', 'Los Angeles', 'docs/icons/brussels_airlines.png'),
('Ryanair', '2025-05-01 09:30:00', '2025-05-01 11:45:00', 'Delayed', 'B3', 'Airbus A320', 180, 30, 259.50, 'Brussels', 'Paris', 'docs/icons/ryanair.png'),
('KLM', '2025-05-02 14:00:00', '2025-05-02 16:30:00', 'On Time', 'C2', 'Boeing 777', 250, 120, 349.75, 'Brussels', 'Amsterdam', 'docs/icons/klm.png'),
('Air France', '2025-05-02 16:45:00', '2025-05-02 18:15:00', 'On Time', 'D4', 'Airbus A330', 200, 70, 229.00, 'Brussels', 'London', 'docs/icons/air_france.png'),
('Emirates', '2025-05-03 10:00:00', '2025-05-03 12:00:00', 'Cancelled', 'E5', 'Boeing 787', 220, 0, 499.99, 'Brussels', 'Dubai', 'docs/icons/emirates.png'),
('Lufthansa', '2025-05-03 18:30:00', '2025-05-03 20:00:00', 'On Time', 'F6', 'Airbus A350', 210, 100, 399.50, 'Brussels', 'Munich', 'docs/icons/lufthansa.png'),
('Qatar Airways', '2025-05-04 07:00:00', '2025-05-04 09:15:00', 'On Time', 'G7', 'Boeing 747', 300, 50, 499.00, 'Brussels', 'Doha', 'docs/icons/qatar_airways.png'),
('Turkish Airlines', '2025-05-04 21:00:00', '2025-05-05 01:00:00', 'On Time', 'H8', 'Airbus A380', 500, 400, 650.00, 'Brussels', 'Istanbul', 'docs/icons/turkish_airlines.png'),
('Wizz Air', '2025-05-05 12:00:00', '2025-05-05 14:30:00', 'Delayed', 'I9', 'Boeing 767', 180, 90, 279.95, 'Brussels', 'Budapest', 'docs/icons/wizz_air.png'),
('Air Canada', '2025-05-05 15:00:00', '2025-05-05 17:30:00', 'On Time', 'J10', 'Airbus A320', 160, 80, 199.00, 'Brussels', 'Toronto', 'docs/icons/air_canada.png');
INSERT INTO users (id, username, first_name, last_name, role, password) VALUES
(1, 'admin1', 'Alice', 'Smith', 'admin', 'adminpass123'),
(2, 'admin2', 'Bob', 'Johnson', 'admin', 'secureadmin456'),
(3, 'staff1', 'Charlie', 'Brown', 'staff', 'staffpass789'),
(4, 'staff2', 'Diana', 'Miller', 'staff', 'passwordstaff'),
(5, 'user1', 'Eve', 'Davis', 'user', 'userpass123'),
(6, 'user2', 'Frank', 'Wilson', 'user', 'letmein456'),
(7, 'user3', 'Grace', 'Lee', 'user', 'mypassword'),
(8, 'staff3', 'Henry', 'Moore', 'staff', 'flightstaff2025'),
(9, 'admin3', 'Isabel', 'Taylor', 'admin', 'rootadmin987'),
(10, 'user4', 'Jack', 'Anderson', 'user', 'welcomeuser');
