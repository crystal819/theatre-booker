from flask import Flask, render_template, request, jsonify, redirect
from performance_db import PerformanceDB

app = Flask(__name__)
db = PerformanceDB()

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
        return render_template('index.html')
    else:
        return jsonify({'errorMsg': 'You entered invalid data or someone has already taken this username, try again'})



if __name__ == '__main__':
    app.run(debug=True)