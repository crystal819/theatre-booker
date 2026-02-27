create table users (userName varchar(20) primary key not null, firstName varchar(20) not null, lastName varchar(20), email varchar(30), DoB date not null, phone int, userType varchar(20) not null)
create table performance (performanceID int primary key not null, performaceDate date, eventType varchar(20), description varchar(200))
create table booking (bookingID int primary key not null, userName varchar(20), foreign key (userName) references users (userName), price int)
create table seat (seatPos varchar(10), bookingID int, foreign key (bookingID) references booking (bookingID), performanceID int, foreign key (performanceID) references performance (performanceID))
