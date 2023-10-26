import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import handlejsonfile
import sqlite3

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Sample user data (you would typically have a database)
# users = {
#     'user1': {'password': 'password1'},
#     'user2': {'password': 'password2'}
# }


# Define the database initialize function
def initialize_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            username TEXT UNIQUE,
            password TEXT,
            phone TEXT,
            organization TEXT,
            street_address TEXT,
            city TEXT,
            state TEXT,
            zipcode TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()


@app.before_request
def log_request_info():
    # Log request information for each incoming request
    logging.info('Request Headers: %s', request.headers)
    logging.info('Request Method: %s', request.method)
    logging.info('Request URL: %s', request.url)
    logging.info('Request Data: %s', request.get_data())


# Sample protected endpoint
@app.route('/protected')
def protected():
    user = "true"
    if user:
        return jsonify({"message": f"Protected resource accessed by {user}"})
    return jsonify({"message": "Unauthorized"}), 401

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if handlejsonfile.authenticate(username, password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401

# Logout endpoint
@app.route('/logout')
def logout():
    # if 'user' in session:
    #     session.pop('user', None)
    return jsonify({"message": "Logged out"})

@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    firstname = data.get("firstName")
    lastname = data.get("lastName")
    username = data.get("username")
    password = data.get("pass")
    phone = data.get("phone")
    organization = data.get("organization")
    street_address = data.get("street_address")
    city = data.get("city")
    state = data.get("state")
    zipcode = data.get("zip")

    if handlejsonfile.check_user(username):
        return jsonify({"message": "username already exists"})
    else:
        handlejsonfile.add_user(firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode)

    logging.info('firstname is: %s, lastname: %s, phone: %s, organization: %s', firstname, lastname, phone, organization)
    logging.info(', street: %s, city: %s, state: %s, zipcode: %s', street_address, city, state, zipcode)
    logging.info('username in signup : %s', username)
    logging.info('password fetched from data: %s', password)

    # You can now access the signup data in the 'data' variable
    # Implement your signup logic here
    return jsonify({"message": "Signup successful"})

if __name__ == '__main__':
    print("started app")
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)