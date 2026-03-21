from flask import Flask, render_template, request, jsonify, redirect, session
from performance_db import PerformanceDB

app = Flask(__name__)
db = PerformanceDB()
app.secret_key = 'this_is_a_very_secret_key'

def gen_chair_imgs():
    chair=[0] #inserted a 0 to make the array 1-index based rather and 0-index based for ease of use with seat numbering
    for i in range(10):
        chair.append([])
        for _ in range(20):
            chair[i+1].append('static/img/available_chair.png') #sets the chairs image
    chair_class=[0]
    for i in range(10):
        chair_class.append([])
        for _ in range(20):
            chair_class[i+1].append('available') #sets the chairs class
    return chair, chair_class

@app.route('/', methods=['GET', 'POST'])
def index():
    chair, chair_class = gen_chair_imgs()

    return render_template('index.html', chair=chair, chair_class=chair_class)

@app.route('/performance-data')
def get_seats_available_performances():
    performance_data = db.list_performances()
    return jsonify(performance_data)

@app.route('/create-account', methods=['POST'])
def create_account():

    data = request.get_json()

    if db.create_account(data):
        return jsonify({'outcome': 'successful'})
    else:
        return jsonify({'outcome': 'unsuccessful',
                        'errorMsg': 'You entered invalid data or someone has already taken this username, try again'})

@app.route('/login', methods=['GET', 'POST'])
def login():

    data = request.get_json()

    
    userType = db.login(data)

    if userType != False:
        session['userName'] = data['userName']
        session['userType'] = userType
        return jsonify({'isSuccessful': 'true',
                        'redirect': '/dashboard'})
    else:
        return jsonify({'isSuccessful': 'false',
                        'errorMsg': 'You entered invalid data or someone has already taken this username, try again'})

@app.route('/dashboard')
def dashboard():
    if 'userType' not in session:
        return redirect("/")
    if session['userType'] == 'normal' or session['userType'] == 'specialGuest':
        days_until_performance = 783465926747364968706689089573404508945023489
        client_name = db.get_name(session['userName'])
        future_tickets = db.get_future_tickets(session['userName'])
        past_bookings = db.get_past_bookings(session['userName'])
        unapproved_tickets = db.get_unapproved_bookings(session['userName'])
        chair, chair_class = gen_chair_imgs()
        return render_template("customer_dashboard.html", days_until_performance = days_until_performance, client_name = client_name, future_tickets=future_tickets, past_bookings=past_bookings, chair=chair, chair_class=chair_class, unapproved_tickets=unapproved_tickets)
    elif session['userType'] == 'staff':
        unapproved_customer_tickets = db.get_unapproved_customer_bookings()
        chair, chair_class = gen_chair_imgs()
        client_name = db.get_name(session['userName'])
        return render_template("staff_dashboard.html", client_name = client_name, chair=chair, chair_class=chair_class, unapproved_customer_tickets=unapproved_customer_tickets)
    elif session['userType'] == 'admin':
        return render_template("admin_dahsboard.html")

@app.route('/calcPrice', methods=['GET', 'POST'])
def calculatePrice():
    data = request.get_json()

    seats = []
    seat = ''
    for i in range(len(data['seatsBooked'])):
        if data['seatsBooked'][i] != ',' and data['seatsBooked'][i] != ' ':
            seat += data['seatsBooked'][i]
        else:
            if seat != '':
                seats.append(seat)
            seat = ''

    if session['userType'] == 'normal':
        price = len(seats) * 10
    if session['userType'] == 'specialGuest':
        price = 0
    if session['userType'] == 'staff':
        price = len(seats) * 10
    if session['userType'] == 'admin':
        price = len(seats) * 10
    
    return jsonify({
        'isSuccessful': 'true',
        'price': str(price)
    })

@app.route('/bookSeats', methods=['GET', 'POST'])
def book_seats():

    data = request.get_json()

    seats = []
    seat = ''
    for i in range(len(data['seatsBooked'])):
        if data['seatsBooked'][i] != ',' and data['seatsBooked'][i] != ' ':
            seat += data['seatsBooked'][i]
        else:
            if seat != '':
                seats.append(seat)
            seat = ''


    if session['userType'] == 'normal':
        price = len(seats) * 10
    if session['userType'] == 'specialGuest':
        price = 0
    if session['userType'] == 'staff':
        price = len(seats) * 10
    if session['userType'] == 'admin':
        price = len(seats) * 10

    booking = db.book_seats(seats, data['performanceID'], session['userName'], price)
    if booking == None:
        return jsonify({})
    if booking['isSuccessful'] == True:
        return jsonify({
            'isSuccessful': 'true'
        })
    if booking['isSuccessful'] == False:
        return jsonify({
            'isSuccessful': 'false',
            'errorMsg': 'Seat'+booking['erroneousSeat']+'is invalid'
        })

@app.route('/search-customer', methods=['GET', 'POST'])
def search_customer():

    data = request.get_json()

    user_details = db.search_string(data['searchString'])

    if user_details['isSuccessful'] == True:
        user_details['tickets'] = db.get_past_bookings(user_details['data'][0])
    print(user_details)
    return jsonify(user_details)


if __name__ == '__main__':
    app.run(debug=True)