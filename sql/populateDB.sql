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
INSERT INTO seat (seatPos, bookingID, performanceID, occupied) VALUES
('1a', 101, 1, 'booked'),
('2a', 101, 1, 'booked'),
('5b', 102, 2, 'booked'),
('6b', 102, 2, 'booked'),
('3c', 103, 3, 'booked'),
('4c', 103, 3, 'booked'),
('1d', 104, 4, 'booked'),
('2d', 104, 4, 'booked');
-- Additional Seats
INSERT INTO seat (seatPos, bookingID, performanceID, occupied) VALUES
('3a', 105, 2, 'booked'),
('4a', 105, 2, 'booked'),
('7b', 106, 1, 'booked'),
('8b', 106, 1, 'booked'),
('5c', 107, 4, 'booked'),
('6c', 107, 4, 'booked'),
('3d', 108, 3, 'booked'),
('4d', 108, 3, 'booked'),
('1e', 109, 1, 'booked'),
('2e', 110, 2, 'booked'),
('1f', 111, 3, 'booked'),
('2f', 112, 4, 'booked');

-- Blocked Seats (no booking, unavailable for booking)
INSERT INTO seat (seatPos, bookingID, performanceID, occupied) VALUES
('10a', NULL, 1, 'blocked'),
('10b', NULL, 1, 'blocked'),
('10c', NULL, 2, 'blocked'),
('10d', NULL, 2, 'blocked'),
('10e', NULL, 3, 'blocked'),
('10f', NULL, 3, 'blocked'),
('10g', NULL, 4, 'blocked'),
('10h', NULL, 4, 'blocked');
