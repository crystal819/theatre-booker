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
            "Server=localhost\\SQLEXPRESS;"
            "Database=TheatrePerformance;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        try:
            pyodbc.connect(conn_string_sch, timeout=3)
            self.conn_string = conn_string_sch
        except:
            self.conn_string = conn_string_home
        
    def _get_connection(self):
        return pyodbc.connect(self.conn_string)

    def convert_date_to_ISO(self, date): #converts dates from dd/mm/yyyy -> yyyy-mm-dd || human read-able to date standard iso 8601
        ISOstr = date[-4:] + '-' + date[3:5] + '-' + date[:2]
        return ISOstr

    def list_performances(self):
        today = date.today()

        sql1 = f"SELECT performanceID FROM performance WHERE performanceDate >= '{today}'" #gets all the performances that are running today or after
        with self._get_connection() as conn:
            _current_performances = conn.cursor().execute(sql1).fetchall()

        all_data = {
            'performances': []
        }
        for i in range(len(_current_performances)):
            #gets all the data necessary for each active performance
            sql2 = f"SELECT p.eventType, s.seatPos, p.performanceDate, p.description, s.performanceID FROM (SELECT seatPos, performanceID FROM seat WHERE performanceID = {_current_performances[i][0]}) s LEFT JOIN (SELECT eventType, performanceDate, description, performanceID FROM performance) p ON s.performanceID = p.performanceID ORDER BY s.performanceID ASC"
            with self._get_connection() as conn:
                record = conn.cursor().execute(sql2).fetchall()
                for j in range(len(record)):
                    if str(_current_performances[i][0]) not in all_data['performances']:
                        all_data['performances'].append(str(_current_performances[i][0])) #adds the performance to the performances list
                        all_data[str(_current_performances[i][0])] = [record[j][0], 199, record[j][2], record[j][3]] #stored event, seats available, date, description in that order
                    else:
                        all_data[str(_current_performances[i][0])][1] -= 1 #removed a seat if the performance is already present
        return all_data
    
    def create_account(self, data):

        with self._get_connection() as conn:
            username_check = conn.cursor().execute(f"SELECT * FROM users WHERE userName = '{data['userName']}'").fetchall()
        if len(username_check) != 0:
            print("user already registered")
            return False

        DoB = date(int(self.convert_date_to_ISO(data['dateOfBirth'])[:4]), int(self.convert_date_to_ISO(data['dateOfBirth'])[5:7]), int(self.convert_date_to_ISO(data['dateOfBirth'])[8:10]))
        if DoB > date.today():
            return False

        if not (data['email'][-10:] != '@gmail.com' or data['email'][-10:] != '@email.com'):
            return False
        
        if len(data['phoneNumber']) < 10 and len(data['phoneNumber']) > 11:
            return False
        print('2')
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
        print(sql)
        with self._get_connection() as conn:
            conn.cursor().execute(sql)
            print('Account created', sql)
        
        return True

    def login(self, data):
        with self._get_connection() as conn:
            sql = f"SELECT userName, passwordHash, userType FROM users WHERE userName = '{data['userName']}'"
            user = conn.cursor().execute(sql).fetchone()
        if user == None: #checks the userName exists
            return False
        
        old_hash = bytes.fromhex(user[1][:64].encode('utf-8')) #converts the string to bin which is currently in hex format and then converts hex to bytes
        salt = bytes.fromhex(user[1][65:97].encode('utf-8'))
        iterations = int(user[1][98:])

        new_hash = pbkdf2_hmac('sha256', data['password'].encode('utf-8'), salt, iterations)

        if new_hash != old_hash: #checks password hashes are the same for the userName entered
            return False
        
        return user[2] #returns the userType 

