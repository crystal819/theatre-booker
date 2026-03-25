import pyodbc
from datetime import date
from hashlib import pbkdf2_hmac
import os




class PerformanceDB:
    def __init__(self):
        conn_string_sch = (
            'Driver={SQL Server};'
            'Server=svr-cmp-01;'
            'Database=25svynarchT230;'
            'Trusted_Connection=yes;'
        )

        conn_string_home = (
            "Driver={SQL Server};"
            "Server=LAPTOP-T;"
            "Database=TheatrePerformance;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        try:
            self.conn = pyodbc.connect(conn_string_sch, timeout=3)
        except:
            try:
                self.conn = pyodbc.connect(conn_string_home)
            except:
                print("ERROR CONNECTING TO THE DATABASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def convert_date_to_ISO(self, date): #converts dates from dd/mm/yyyy -> yyyy-mm-dd || human read-able to date standard iso 8601
        ISOstr = date[-4:] + '-' + date[3:5] + '-' + date[:2]
        return ISOstr

    def list_performances(self, userName=None):
        today = date.today()

        sql1 = f"SELECT performanceID FROM performance WHERE performanceDate >= '{today}'" #gets all the performances that are running today or after
        _current_performances = self.conn.cursor().execute(sql1).fetchall()

        all_data = {
            'performances': []
        }
        for i in range(len(_current_performances)):
            #gets all the data necessary for each active performance
            sql2 = f'''SELECT p.eventType, s.seatPos, p.performanceDate, p.description, s.performanceID, s.occupied, b.userName FROM 
                    (SELECT seatPos, performanceID, occupied, bookingID FROM seat WHERE performanceID = {_current_performances[i][0]}) s 
                    LEFT JOIN 
                    (SELECT userName, bookingID FROM booking) b
                    ON b.bookingID = s.bookingID
                    LEFT JOIN
                    (SELECT eventType,performanceDate, description, performanceID FROM performance) p 
                    ON s.performanceID = p.performanceID 
                    ORDER BY s.performanceID ASC'''
            record = self.conn.cursor().execute(sql2).fetchall()
            for j in range(len(record)):
                if str(_current_performances[i][0]) not in all_data['performances']:
                    all_data['performances'].append(str(_current_performances[i][0])) #adds the performance to the performances list
                    if record[j][5] == 'booked':
                        if record[j][6] == userName:
                            all_data[str(_current_performances[i][0])] = [record[j][0], [], record[j][2], record[j][3], [], str(_current_performances[i][0]), [record[j][1]]] 
                        else:
                            all_data[str(_current_performances[i][0])] = [record[j][0], [record[j][1]], record[j][2], record[j][3], [], str(_current_performances[i][0]), []] #stored event, seatsBooked, date, description, seatsBlocked, performanceID, seatsBought in that order
                    elif record[j][5] == 'blocked':
                        all_data[str(_current_performances[i][0])] = [record[j][0], [], record[j][2], record[j][3], [record[j][1]], str(_current_performances[i][0]), []]
                else:
                    if record[j][5] == 'booked':
                        all_data[str(_current_performances[i][0])][1].append(record[j][1]) #adds seatBooked to the array of the seatsBooked
                    elif record[j][5] == 'blocked':
                        all_data[str(_current_performances[i][0])][4].append(record[j][1]) #adds seatBlocked to the array of the seatsBlocked
                    elif record[j][6] == userName:
                        all_data[str(_current_performances[i][0])][6].append(record[j][1]) #adds seatBought to the array of seatsBought
        return all_data
    
    def create_account(self, data):

        username_check = self.conn.cursor().execute(f"SELECT * FROM users WHERE userName = '{data['userName']}'").fetchall()
        if len(username_check) != 0:
            return False

        DoB = date(int(self.convert_date_to_ISO(data['dateOfBirth'])[:4]), int(self.convert_date_to_ISO(data['dateOfBirth'])[5:7]), int(self.convert_date_to_ISO(data['dateOfBirth'])[8:10]))
        if DoB > date.today():
            return False

        if not (data['email'][-10:] != '@gmail.com' or data['email'][-10:] != '@email.com'):
            return False
        
        if len(data['phoneNumber']) < 10 and len(data['phoneNumber']) > 11:
            return False
        try:
            temp = int(data['phoneNumber'])
        except ValueError:
            return False
        
        if len(data['firstName']) > 20 or len(data['lastName']) > 20 or len(data['email']) > 30 or len(data['userName']) > 20:
            return False
        
        if len(data['firstName']) < 1 or len(data['password']) < 1:
            return False
        
        #hash to encrypt the users password
        password = data['password'].encode('utf-8') #converts the password str to bin
        salt = os.urandom(16) #generates a random sequence of bin
        iterations = 1000

        hashed = pbkdf2_hmac('sha256', password, salt, iterations)
        
        password_hash = hashed.hex()+'$'+salt.hex()+'$'+str(iterations)

        sql = f"INSERT INTO users VALUES ('{data['userName']}', '{password_hash}', '{data['firstName']}', '{data['lastName']}', '{data['email']}', '{self.convert_date_to_ISO(data['dateOfBirth'])}', '{data['phoneNumber']}', '{data['userType']}')"
        self.conn.cursor().execute(sql)
        
        return True

    def login(self, data):
        sql = f"SELECT userName, passwordHash, userType FROM users WHERE userName = '{data['userName']}'"
        user = self.conn.cursor().execute(sql).fetchone()
        if user == None: #checks the userName exists
            return False
        
        old_hash = bytes.fromhex(user[1][:64]) #converts the string to bin which is currently in hex format and then converts hex to bytes
        salt = bytes.fromhex(user[1][65:97])
        iterations = int(user[1][98:])

        new_hash = pbkdf2_hmac('sha256', data['password'].encode('utf-8'), salt, iterations)

        if new_hash != old_hash: #checks password hashes are the same for the userName entered
            return False
        
        return user[2] #returns the userType 
    
    def get_name(self, userName):
        sql = f"SELECT firstName, lastName FROM users WHERE userName = '{userName}'"
        name = self.conn.cursor().execute(sql).fetchall()
        if name[0][1] != None:
            return name[0][0] + ' ' + name[0][1] #returns first name and last name together if the user has entered a last name when creating their account
        return name[0]

    def get_future_tickets(self, userName):
        future_tickets = []

        sql1 = f"SELECT performanceID FROM performance WHERE performanceDate >= '{date.today()}'"
        performanceIDs = self.conn.cursor().execute(sql1).fetchall()

        for i in range(len(performanceIDs)):
            sql2 = f"SELECT bookingID FROM booking WHERE userName = '{userName}' AND performanceID = {performanceIDs[i][0]}"
            bookingIDs = self.conn.cursor().execute(sql2).fetchall()

            for j in range(len(bookingIDs)):
                sql3 = f"SELECT b.bookingID, p.performanceName, p.performanceDate, b.price FROM (SELECT bookingID, price, performanceID FROM booking WHERE bookingID = {bookingIDs[j][0]}) b LEFT JOIN (SELECT performanceName, performanceDate, performanceID FROM performance WHERE performanceID = (SELECT performanceID FROM booking WHERE bookingID = {bookingIDs[j][0]})) p ON b.performanceID = p.performanceID"
                booking = self.conn.cursor().execute(sql3).fetchall()

                sql4 = f"SELECT seatPos FROM seat WHERE bookingID = '{bookingIDs[j][0]}'"
                seats = self.conn.cursor().execute(sql4).fetchall()

                seats_str = ''
                for k in range(len(seats)):
                    seats_str += seats[k][0] + ', '
                seats_str = seats_str[:-2]
                future_tickets.append((booking[0][0], booking[0][1], booking[0][2], seats_str, booking[0][3]))
        return future_tickets
    
    def get_past_bookings(self, userName):
        past_bookings = []

        sql1 = f"SELECT bookingID FROM booking WHERE userName = '{userName}' AND approved != 'false'"
        bookingIDs = self.conn.cursor().execute(sql1).fetchall()
        
        for i in range(len(bookingIDs)):
            sql2 = f"SELECT b.bookingID, p.performanceName, p.performanceDate, b.price FROM (SELECT bookingID, price, performanceID FROM booking WHERE bookingID = {bookingIDs[i][0]}) b LEFT JOIN (SELECT performanceName, performanceDate, performanceID FROM performance WHERE performanceID = (SELECT performanceID FROM booking WHERE bookingID = {bookingIDs[i][0]})) p ON b.performanceID = p.performanceID"
            booking = self.conn.cursor().execute(sql2).fetchall()

            sql3 = f"SELECT seatPos FROM seat WHERE bookingID = '{bookingIDs[i][0]}'"
            seats = self.conn.cursor().execute(sql3).fetchall()
            seats_str = ''
            for j in range(len(seats)):
                seats_str += seats[j][0] + ', '
            seats_str = seats_str[:-2]
            past_bookings.append((booking[0][0], booking[0][1], booking[0][2], seats_str, booking[0][3]))
        return past_bookings

    def book_seats(self, seats, performanceID, user_name, price):
        for i in range(len(seats)):
            sql = f"SELECT occupied FROM seat WHERE seatPos = '{seats[i]}' and performanceID = '{performanceID}'"
            result = self.conn.cursor().execute(sql).fetchone()
            if result == 'booked' or result == 'blocked':
                return {
                    'isSuccessful': False,
                    'erroneousSeat': seats[i]
                 }
            
        booking_sql = f"INSERT INTO booking (userName, performanceID, approved, price, bookingDate) OUTPUT INSERTED.bookingID VALUES ('{user_name}', {performanceID}, Null, {price}, '{date.today()}')"
        bookingID = self.conn.cursor().execute(booking_sql).fetchone()

        for i in range(len(seats)):
            seat_sql = f"INSERT INTO seat (seatPos, bookingID, performanceID, occupied) VALUES ('{seats[i]}', {bookingID[0]}, {performanceID}, 'booked')"
            self.conn.cursor().execute(seat_sql)

        return {
            'isSuccessful': True,
            'bookingID': bookingID
        }

    def get_unapproved_bookings(self, userName): #gets the unapproved tickets for the specified user
        unapproved_bookings = []

        sql1 = f"SELECT bookingID FROM booking WHERE userName = '{userName}' AND approved IS NULL"
        bookingIDs = self.conn.cursor().execute(sql1).fetchall()
        
        for i in range(len(bookingIDs)):
            sql2 = f"SELECT b.bookingID, p.performanceName, p.performanceDate, b.price FROM (SELECT bookingID, price, performanceID FROM booking WHERE bookingID = {bookingIDs[i][0]}) b LEFT JOIN (SELECT performanceName, performanceDate, performanceID FROM performance WHERE performanceID = (SELECT performanceID FROM booking WHERE bookingID = {bookingIDs[i][0]})) p ON b.performanceID = p.performanceID"
            booking = self.conn.cursor().execute(sql2).fetchall()

            sql3 = f"SELECT seatPos FROM seat WHERE bookingID = '{bookingIDs[i][0]}'"
            seats = self.conn.cursor().execute(sql3).fetchall()
            seats_str = ''
            for j in range(len(seats)):
                seats_str += seats[j][0] + ', '
            seats_str = seats_str[:-2]
            unapproved_bookings.append((booking[0][0], booking[0][1], booking[0][2], seats_str, booking[0][3]))
            
        return unapproved_bookings

    def get_unapproved_customer_bookings(self): #gets all unapproved bookings into a list: [bookingID, userName, performanceID, price, bookingDate, [seats_list] ]

        sql1 = "SELECT bookingID, userName, performanceID, price, bookingDate FROM Booking WHERE approved = NULL"
        bookings = self.conn.cursor().execute(sql1).fetchall()

        seats_list = []
        for i in range(len(bookings)):
            sql2 = f"SELECT SeatPos FROM seat WHERE BookingID = {bookings[i][0]}"
            seats = self.conn.cursor().execute(sql2).fetchall()
            for j in range(len(seats)):
                seats_list.append(seats[j][0])
            bookings[i].append(seats_list)

        return bookings

    def search_string(self, search_string, admin=False): #ranking = userName, email, lastName, firstName
        if admin == False: #allows for admins to see all types of users but non admins can only see customers
            usertype_selection = " and (userType = 'normal' or userType = 'specialGuest')"
        else:
            usertype_selection = ""
        sql = f"SELECT * FROM users WHERE userName = '{search_string}'" + usertype_selection
        user = self.conn.cursor().execute(sql).fetchone() #searches by userName
        if user is None:
            if '@' in search_string:
                sql = f"SELECT * FROM users WHERE email LIKE '{search_string}%'" + usertype_selection
                user = self.conn.cursor().execute(sql).fetchone() #searches by email
            if user is None:
                sql = f"SELECT * FROM users WHERE lastName = '{search_string}'" + usertype_selection
                user = self.conn.cursor().execute(sql).fetchone() #searches by lastName
                if user is None:
                    sql = f"SELECT * FROM users WHERE firstName = '{search_string}'" + usertype_selection
                    user = self.conn.cursor().execute(sql).fetchone() #searches by firstName
                    if user is None:
                        return {'isSuccessful': False}
                    
                    return {'isSuccessful': True,
                            'match': 'First Name',
                            'data': list(user)}
                else:
                    return {'isSuccessful': True,
                            'match': 'Last Name',
                            'data': list(user)}
            else:
                return {'isSuccessful': True,
                        'match': 'Email',
                        'data': list(user)}
        else:
            return {'isSuccessful': True,
                    'match': 'User Name',
                    'data': list(user)}

    def block_seats(self, performanceID, seats):
        sql = ''
        for i in range(len(seats)):
            seat_registered_check = self.conn.cursor().execute(f"SELECT * FROM seat WHERE seatPos = '{seats[i]}' and performanceID = '{performanceID}'").fetchall()
            if len(seat_registered_check) == 0:
                sql += f"INSERT INTO seat (seatPos, bookingID, performanceID, occupied) VALUES ('{seats[i]}', NULL, '{performanceID}', 'blocked') "
            else:
                return {'isSuccessful': False,
                        'reason': f'seat {seats[i]} is already blocked or booked'}
        try:
            self.conn.cursor().execute(sql)
            return {'isSuccessful': True}
        except:
            return {'isSuccessful': False,
                    'reason': ''}




