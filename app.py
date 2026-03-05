from flask import Flask, render_template, request, jsonify, redirect, session
from performance_db import PerformanceDB

app = Flask(__name__)
db = PerformanceDB()
app.secret_key = 'this_is_a_very_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
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

    return render_template('index.html', chair=chair, chair_class=chair_class)



@app.route('/performance-data', methods=['GET'])
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
        return redirect('/dashboard')
    else:
        return jsonify({'outcome': 'unsuccessful',
                        'errorMsg': 'You entered invalid data or someone has already taken this username, try again'})

@app.route('/dashboard')
def dashboard():
    if session['userType'] == 'normal' or session['userType'] == 'specialGuest':
        return render_template("customer_dashboard.html")
    elif session['userType'] == 'staff':
        return render_template("staff_dashboard.html")
    elif session['userType'] == 'admin':
        return render_template("admin_dahsboard.html")


if __name__ == '__main__':
    app.run(debug=True)