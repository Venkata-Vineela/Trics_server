import logging
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import handledata
import sqlite3

## sessions code here
from flask_session import Session  # Import Flask-Session

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

app.config['SESSION_TYPE'] = 'filesystem'  # You can choose other session storage options
Session(app)

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            username TEXT,
            friendusername TEXT,
            PRIMARY KEY (username, friendusername),
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (friendusername) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

@app.route('/search_unames', methods=['POST'])
def search_unames():
    if 'user' in session:
        data = request.get_json()
        query = data.get('searchText')
        posts = handledata.getunames(query)

        return jsonify(posts)
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/suggest_unames', methods=['POST'])
def suggest_unames():
    if 'user' in session:
        username = session['user']
        suggestions = handledata.get_uname_suggestions(username)
        return jsonify(suggestions)
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    if 'user' in session:
        data = request.get_json()
        username = data.get('username')
        userdata = handledata.get_user_data(username)

        return jsonify(userdata)
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route('/connectusers', methods=['POST'])
def connectusers():
    if 'user' in session:
        data = request.get_json()
        friendusername = data.get('username')
        username = session['user']
        handledata.add_friend_connection(username, friendusername)
        return jsonify({"message": "Friend connection added successfully"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/isfriend', methods=['POST'])
def isfriend():
    if 'user' in session:
        data = request.get_json()
        friendusername = data.get('username')
        username = session['user']
        value = handledata.isfriend(username, friendusername)
        return jsonify({"isfriend": {value}}), 200
    else:
        return jsonify({"message": "Unauthorized", "isfriend": "exception"}), 401

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
    logging.info('Request Headers in protected: %s', request.headers)

    if 'user' in session:
        # Get the username from the session
        session_username = session['user']
        return jsonify({"message": f"Protected resource accessed by {session_username}"})
    return jsonify({"message": "Unauthorized"}), 401
    # data = request.get_json()
    # username = data.get('username')
    # if username in session['user']:
    #     return jsonify({"message": "Protected resource accessed by "})
    # return jsonify({"message": "Unauthorized"}), 401

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    logging.info('session Data: %s', session)

    if handledata.authenticate(username, password):
        session['user'] = username  # Store the user in the session
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401

# Logout endpoint
@app.route('/logout')
def logout():
    logging.info('loggingout Data: %s', request)

    if 'user' in session:
        session.pop('user', None)
        return jsonify({"message": f"Logout successful"})
    else:
        return jsonify({"message": "Logout Failed. Please try again."})

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

    if handledata.check_user(username):
        return jsonify({"message": "username already exists"})
    else:
        handledata.add_user(firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode)

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