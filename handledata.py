import json
import sqlite3

# File path for the JSON data file
JSON_FILE_PATH = "data/userdata.json"
#to do this will eventually replaced by database in next weeks
def read_data():
    """
    Read the user data from the JSON file and return it as a dictionary.
    If the file does not exist, return an empty dictionary.
    """
    # try:
    #     with open(JSON_FILE_PATH, 'r') as json_file:
    #         data = json.load(json_file)
    # except FileNotFoundError:
    #     data = {}
    # return data
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    user_data = {}
    for row in data:
        username = row[3]  # Assuming that username is stored in the fourth column
        user_data[username] = {
            "firstname": row[1],
            "lastname": row[2],
            "password": row[4],
            "phone": row[5],
            "organization": row[6],
            "street_address": row[7],
            "city": row[8],
            "state": row[9],
            "zipcode": row[10]
        }
    return user_data

# def write_data(data):
#     """
#     Write the user data to the JSON file.
#     """
#     # with open(JSON_FILE_PATH, 'w') as json_file:
#     #     json.dump(data, json_file, indent=4)
#     conn = sqlite3.connect('user_data.db')
#     cursor = conn.cursor()
#
#     # Remove existing records in the 'users' table
#     cursor.execute('DELETE FROM users')
#
#     # Insert user data into the 'users' table
#     for username, user_info in data.items():
#         cursor.execute('''
#                 INSERT INTO users (
#                     firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', (
#             user_info["firstname"],
#             user_info["lastname"],
#             username,
#             user_info["password"],
#             user_info["phone"],
#             user_info["organization"],
#             user_info["street_address"],
#             user_info["city"],
#             user_info["state"],
#             user_info["zipcode"]
#         ))
#
#     conn.commit()
#     conn.close()

def add_user(firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode):
    """
    Add a user to the user data.
    """

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO users (
                firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode))
    conn.commit()
    conn.close()

def check_user(username):
    """
    Check if the provided username and password are valid.
    """
    # data = read_data()
    # if username in data:
    #     return True
    # else:
    #     return False
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def authenticate(username,password):
    data = read_data()
    username = username.strip()

    # Now, check if the username exists in the data dictionary
    if username in data and data[username]['password'] == password:
        return True
    else:
        return False


def getunames(query):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstname FROM users WHERE firstname LIKE ? LIMIT 4', ('%' + query + '%',))
    suggested_usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    return suggested_usernames

def get_uname_suggestions(username):
    username = username.strip()
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT organization,zipcode FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        organization, zipcode = row

        # Query for suggestions
        cursor.execute('''
                    SELECT firstname FROM users
                    WHERE (organization = ? AND username != ?) 
                     OR 
                     (zipcode = ? AND username != ?)
                    LIMIT 10
                  ''', (organization, username, zipcode, username))

        suggestions = [row[0] for row in cursor.fetchall()]

    conn.close()
    return suggestions