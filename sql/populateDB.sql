insert into users values
('admin1', '$2b$12$KIX8mFz9YwqJz3Qk0pR2re9uC8yF7nT6uQvLxH1oZk9mJt3pWqR5C', 'Alice', 'Johnson', 'admin1@email.com', '1980-05-12', 701111111, 45, 'admin'),
('staff1', '$2b$12$LZp9xQvH7mW2kR8tYf3sDe1nC4uB6aJkL9pQ2rT5vW8xYz1A3bC6D', 'Mark', 'Stevens', 'mark.s@email.com', '1985-09-22', 702222222, 40, 'staff'),
('jdoe', '$2b$12$AbC123xYz987LmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZ12', 'John', 'Doe', 'jdoe@email.com', '1998-02-14', 703333333, 28, 'customer'),
('swhite', '$2b$12$ZxY987wVuTsRqPoNmLkJiHgFeDcBaZyXwVuTsRqPoNmLkJiHgFeDcB1', 'Sophie', 'White', 's.white@email.com', '1995-11-03', 704444444, 30, 'customer'),
('bking', '$2b$12$QwErTyUiOpAsDfGhJkLzXcVbNmQwErTyUiOpAsDfGhJkLzXcVbNm12', 'Ben', 'King', 'ben.k@email.com', '2001-07-19', 705555555, 24, 'customer'),
('lgreen', '$2b$12$MnBvCxZlKjHgFdSaQwErTyUiOpMnBvCxZlKjHgFdSaQwErTyUiOp12', 'Lucy', 'Green', 'lucy.g@email.com', '1999-04-08', 706666666, 26, 'customer');

insert into performance values
(201, '2026-04-10', 'Drama', 'Hamlet', 'A Shakespeare tragedy'),
(202, '2026-04-15', 'Comedy', 'LaughNight', 'Stand-up comedy evening'),
(203, '2026-04-20', 'Musical', 'BroadwayMix', 'A mix of famous musicals'),
(204, '2026-04-25', 'Dance', 'UrbanMoves', 'Street and contemporary dance'),
(205, '2026-05-01', 'Opera', 'LaTraviata', 'Classic Italian opera');

insert into booking values
(2001, 'jdoe', 201, 'admin1'),
(2002, 'swhite', 201, 'staff1'),
(2003, 'swhite', 202, NULL),
(2004, 'bking', 203, 'admin1'),
(2005, 'jdoe', 204, NULL);

insert into seat values
('A1', 2001, 201),
('A2', 2002, 201),
('B1', 2003, 202),
('C3', 2004, 203),
('D4', NULL, 204),     -- seat exists but not booked
('E1', 2005, 204),
('F2', NULL, 205);     -- performance exists but no bookings
