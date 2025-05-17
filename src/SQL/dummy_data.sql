INSERT INTO flights (airline, departure, arrival, status, gate, plane_type, total_seats, seats_taken, price, from_location, to_location, airline_icon) VALUES
('Brussels Airlines', '2025-06-01 06:30:00', '2025-06-01 07:45:00', 'On Time', 'A1', 'Airbus A319', 120, 45, 159.99, 'Brussels', 'Paris'),
('Ryanair', '2025-06-01 09:30:00', '2025-06-01 11:45:00', 'Delayed', 'B3', 'Airbus A320', 180, 30, 259.50, 'Brussels', 'Paris'),
('Air France', '2025-06-01 13:15:00', '2025-06-01 14:30:00', 'On Time', 'C2', 'Embraer 190', 100, 75, 189.00, 'Brussels', 'Paris'),
('Ryanair', '2025-06bookings-02 07:00:00', '2025-06-02 09:15:00', 'On Time', 'D4', 'Boeing 737', 160, 90, 149.99, 'Brussels', 'Paris'),
('Brussels Airlines', '2025-06-02 16:45:00', '2025-06-02 18:00:00', 'On Time', 'E5', 'Airbus A320', 180, 110, 219.50, 'Brussels', 'Paris'),
-- Multiple flights to London on different dates
('British Airways', '2025-06-01 08:15:00', '2025-06-01 08:45:00', 'On Time', 'F6', 'Airbus A320', 150, 60, 179.00, 'Brussels', 'London'),
('Air France', '2025-06-01 12:30:00', '2025-06-01 13:00:00', 'On Time', 'G7', 'Embraer 190', 100, 40, 199.00, 'Brussels', 'London'),
('Ryanair', '2025-06-02 10:45:00', '2025-06-02 11:15:00', 'Delayed', 'H8', 'Boeing 737', 160, 85, 129.99, 'Brussels', 'London'),
('Brussels Airlines', '2025-06-02 18:00:00', '2025-06-02 18:30:00', 'On Time', 'I9', 'Airbus A319', 120, 95, 209.50, 'Brussels', 'London'),
-- Multiple flights to Amsterdam on different dates
('KLM', '2025-06-01 07:00:00', '2025-06-01 07:45:00', 'On Time', 'J10', 'Embraer 175', 80, 30, 129.00, 'Brussels', 'Amsterdam'),
('KLM', '2025-06-01 14:00:00', '2025-06-01 14:45:00', 'On Time', 'K11', 'Boeing 737', 160, 110, 149.00, 'Brussels', 'Amsterdam'),
('Brussels Airlines', '2025-06-02 09:30:00', '2025-06-02 10:15:00', 'On Time', 'L12', 'Airbus A320', 180, 65, 139.99, 'Brussels', 'Amsterdam'),
('KLM', '2025-06-02 17:45:00', '2025-06-02 18:30:00', 'On Time', 'M13', 'Embraer 190', 100, 45, 159.00, 'Brussels', 'Amsterdam'),
-- Multiple long-haul flights to New York
('Brussels Airlines', '2025-06-01 09:00:00', '2025-06-01 12:30:00', 'On Time', 'N14', 'Airbus A330', 220, 150, 599.00, 'Brussels', 'New York'),
('Delta', '2025-06-01 15:30:00', '2025-06-01 19:00:00', 'On Time', 'O15', 'Boeing 767', 240, 180, 649.00, 'Brussels', 'New York'),
('United', '2025-06-02 10:45:00', '2025-06-02 14:15:00', 'On Time', 'P16', 'Boeing 787', 210, 120, 579.00, 'Brussels', 'New York'),
-- Multiple flights to Barcelona
('Ryanair', '2025-06-01 11:00:00', '2025-06-01 13:15:00', 'On Time', 'Q17', 'Boeing 737', 160, 95, 189.99, 'Brussels', 'Barcelona'),
('Vueling', '2025-06-01 18:30:00', '2025-06-01 20:45:00', 'On Time', 'R18', 'Airbus A320', 180, 110, 219.00, 'Brussels', 'Barcelona'),
('Brussels Airlines', '2025-06-02 08:15:00', '2025-06-02 10:30:00', 'On Time', 'S19', 'Airbus A319', 120, 75, 229.50, 'Brussels', 'Barcelona'),
-- Multiple flights to Rome
('Ryanair', '2025-06-01 07:45:00', '2025-06-01 10:00:00', 'On Time', 'T20', 'Boeing 737', 160, 85, 179.99, 'Brussels', 'Rome'),
('Alitalia', '2025-06-01 16:00:00', '2025-06-01 18:15:00', 'On Time', 'U21', 'Airbus A320', 180, 120, 249.00, 'Brussels', 'Rome'),
('Brussels Airlines', '2025-06-02 13:30:00', '2025-06-02 15:45:00', 'On Time', 'V22', 'Airbus A320', 180, 65, 259.50, 'Brussels', 'Rome'),
-- Multiple flights to Berlin
('Lufthansa', '2025-06-01 10:15:00', '2025-06-01 11:30:00', 'On Time', 'W23', 'Embraer 190', 100, 40, 169.00, 'Brussels', 'Berlin'),
('Eurowings', '2025-06-01 19:45:00', '2025-06-01 21:00:00', 'On Time', 'X24', 'Airbus A319', 120, 85, 149.99, 'Brussels', 'Berlin'),
('Brussels Airlines', '2025-06-02 11:00:00', '2025-06-02 12:15:00', 'On Time', 'Y25', 'Airbus A320', 180, 55, 179.50, 'Brussels', 'Berlin'),
-- Multiple flights to Madrid
('Iberia', '2025-06-01 08:30:00', '2025-06-01 10:45:00', 'On Time', 'Z26', 'Airbus A320', 180, 95, 199.00, 'Brussels', 'Madrid'),
('Ryanair', '2025-06-01 17:15:00', '2025-06-01 19:30:00', 'On Time', 'A27', 'Boeing 737', 160, 110, 169.99, 'Brussels', 'Madrid'),
('Brussels Airlines', '2025-06-02 14:45:00', '2025-06-02 17:00:00', 'On Time', 'B28', 'Airbus A319', 120, 70, 229.50, 'Brussels', 'Madrid'),
-- Multiple flights to Lisbon
('TAP Portugal', '2025-06-01 09:45:00', '2025-06-01 12:00:00', 'On Time', 'C29', 'Airbus A320', 180, 60, 219.00, 'Brussels', 'Lisbon'),
('Ryanair', '2025-06-01 20:30:00', '2025-06-01 22:45:00', 'On Time', 'D30', 'Boeing 737', 160, 90, 179.99, 'Brussels', 'Lisbon'),
('Brussels Airlines', '2025-06-02 12:15:00', '2025-06-02 14:30:00', 'On Time', 'E31', 'Airbus A320', 180, 45, 239.50, 'Brussels', 'Lisbon');
INSERT INTO users (id, username, first_name, last_name, role, password) VALUES
('1', 'admin', 'Alice', 'Smith', 'admin', 'gAAAAABoI5azn-H0T5DS9X8jr88DVKHsi1YJWQCy3jMBLij7LzhK0tUD-BwhUnH-TFObbSlMPG5JDbJ8cD3C02wfFIT454BwQA=='),
('2', 'admin2', 'Bob', 'Johnson', 'admin', 'gAAAAABoI5z17RxBwD0YHppcB4tjgh0ytfX91Z_EcYkiytzX3JPRECswaWd6Vc7D330Xx4SAXHl8dJVU6HsTe6FTNn7LoEzhqA=='),
('3', 'staff1', 'Charlie', 'Brown', 'staff', 'gAAAAABoJH3YHQBJRCn1fUWmPvYWVWpWBDpBehrw_GYPVPct6UXPl_l3UOevuGfa8wDEg63qskGOh4DSk9ecEo7vk0PJwvwclQ=='),
('4', 'staff2', 'Diana', 'Miller', 'staff', 'gAAAAABoJH4H1VKGT7UUZ5WNKHmOWg0CKhcz3C9QB1HLt-ceO_dtKZjSsBks4OVAcjOCCObUTduQpbfjgXywIJpAvMcliUdhCg=='),
('5', 'user1', 'Eve', 'Davis', 'user', 'gAAAAABoJH4lh0_nFd-mb_2-TM6yiTDEXTB74i9WdW3Y3bwJMuKmd8R0VQz9yy-4VDqNIcbJs1E7D-ZHmrgD_h7dMQpDpIaWnw=='),
('6', 'user2', 'Frank', 'Wilson', 'user', 'gAAAAABoJH4yAz8gYpJ8MMCKubWyIXcS6_43mZpBgTmm3BIsu7z5kBADwcLEISwrQfd_VSwTCWgZUbpcKM5VYvrlffs-LKd12g=='),
('7', 'user3', 'Grace', 'Lee', 'user', 'gAAAAABoJH5CmLU5eEe6m4ApD2qC-dTC8W_sxPPCIXE3BbxYsYNr6MDEsauJq-ykXKC7GmdkoK_JknPe_gAkdq-tRdyCTlMSwQ=='),
('8', 'staff3', 'Henry', 'Moore', 'staff', 'gAAAAABoJH5VnKbciBwn5rp54UgI28F0QBOuBXqJ3JpvGoB9ahnxfm1Qujtw47Q31pvI6lYY2ri-1s1BrrOlLriqXIzf5JeDWA=='),
('9', 'admin3', 'Isabel', 'Taylor', 'admin', 'gAAAAABoJH6Jvm_uTXvKTvdoS9kbErRpJBcmIZBytVtX-jjvnF35UtNzz1L9XEigiq1fmlexId2vfvkzxWb8tnRr6RGZUEILuA=='),
('10', 'user4', 'Jack', 'Anderson', 'user', 'gAAAAABoJH6WipWKnPxctokWRvnM4gWXZPe7HwZxTD8NkZPRa9eMTX6yOU2bzrAm_ausIr7xJW0Ee21xre0QRkR2UT-nfD_AvQ=='),
('11', 'KIOSK5', 'kiosk', 'kiosk', 'kiosk', 'gAAAAABoJH7HOe-yCeYMatLHNKoK3-I1mR8E_ioj8ZEDCwqHO3NfkCID8IvguBEGBHwlYq4yKib005xAHvN48Cx9LRFpwjHZ1Q=='),
('12', 'airline1', 'Brussels', 'Airlines', 'airline', 'gAAAAABoJH7sLaLEOvRO6KU41ynNv7VjjZKYd5k-kly3ZFEUig5VpwfnYelyUUEjJDAla8r9VNOVyeDuxewGdXl9ifYrUL531Q==');

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