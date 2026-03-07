-- Users
INSERT INTO users (userName, passwordHash, firstName, lastName, email, DoB, phone, userType) VALUES
('taras999', '115e33d730d06da524b64bae8d7fef7f6489c5089ace0d68c3eef399524a4471$6bf2e17ba8b0ded8bbadc7078d750976$1000', 'Taras', 'Svynarchuk', 'tarascollyers@gmail.com', '2008-11-04', '07123456789', 'admin'), -- password: SuperSecure123
('alice123', '141032070ce3621a941d994134a8528f542b6caf9a84686c8f08d7d7b079c978$35a96d8694e62f81b18217bd50ba9ed2$1000', 'Alice', 'Johnson', 'alice.j@example.com', '1995-07-12', '07234567890', 'specialGuest'), -- password: AlicePass456
('bob456', 'b047fc1e33f63381471f3d7297d60b4f23c217610866a5f6d0b542b1b900e069$5ca9293a15ea10c531e4d7a3a8133f52$1000', 'Bob', 'Smith', 'bob.smith@example.com', '1988-03-23', '07345678901', 'normal'), -- password: BobSecret789
('carol789', 'f48f7d77b88ce6e4e11de13dd930e112aebb8bbb1830df5c4a0f4c3f5dcb154b$ee75ecf75b9e78e607fa91f9309ae106$1000', 'Carol', 'White', 'carol.white@example.com', '2000-09-30', '07456789012', 'staff'); -- password: CarolPwd321

-- Performance
INSERT INTO performance (performanceID, performanceDate, eventType, performanceName, description) VALUES
(1, '2026-04-15', 'Theatre', 'Hamlet', 'A Shakespearean tragedy performance'),
(2, '2026-04-20', 'Concert', 'Rock Night', 'An evening of classic rock music'),
(3, '2026-05-05', 'Opera', 'La Traviata', 'A famous opera by Verdi'),
(4, '2026-05-10', 'Comedy', 'Stand-Up Special', 'An evening of stand-up comedy with multiple comedians');

-- Booking
INSERT INTO booking (bookingID, userName, performanceID, approved, price, bookingDate) VALUES
(101, 'alice123', 1, 'taras999', 50, '2026-03-01'),
(102, 'bob456', 2, 'carol789', 75, '2026-03-02'),
(103, 'alice123', 3, 'taras999', 60, '2026-03-03'),
(104, 'bob456', 4, 'carol789', 40, '2026-03-04');
-- Additional Bookings
INSERT INTO booking (bookingID, userName, performanceID, approved, price, bookingDate) VALUES
(105, 'alice123', 2, 'taras999', 75, '2026-03-05'),
(106, 'bob456', 1, 'carol789', 50, '2026-03-05'),
(107, 'alice123', 4, 'taras999', 40, '2026-03-06'),
(108, 'bob456', 3, 'carol789', 60, '2026-03-06'),
(109, 'alice123', 1, 'taras999', 50, '2026-03-07'),
(110, 'bob456', 2, 'carol789', 75, '2026-03-07'),
(111, 'alice123', 3, 'taras999', 60, '2026-03-08'),
(112, 'bob456', 4, 'carol789', 40, '2026-03-08');

-- Seat
INSERT INTO seat (seatPos, bookingID, performanceID) VALUES
('A1', 101, 1),
('A2', 101, 1),
('B5', 102, 2),
('B6', 102, 2),
('C3', 103, 3),
('C4', 103, 3),
('D1', 104, 4),
('D2', 104, 4);
-- Additional Seats
INSERT INTO seat (seatPos, bookingID, performanceID) VALUES
('A3', 105, 2),
('A4', 105, 2),
('B7', 106, 1),
('B8', 106, 1),
('C5', 107, 4),
('C6', 107, 4),
('D3', 108, 3),
('D4', 108, 3),
('E1', 109, 1),
('E2', 110, 2),
('F1', 111, 3),
('F2', 112, 4);