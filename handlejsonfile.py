import json

# File path for the JSON data file
JSON_FILE_PATH = "data/userdata.json"
#to do this will eventually replaced by database in next weeks
def read_data():
    """
    Read the user data from the JSON file and return it as a dictionary.
    If the file does not exist, return an empty dictionary.
    """
    try:
        with open(JSON_FILE_PATH, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    return data

def write_data(data):
    """
    Write the user data to the JSON file.
    """
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def add_user(firstname, lastname, username, password, phone, organization, street_address, city, state, zipcode):
    """
    Add a user to the user data.
    """
    data = read_data()
    data[username] = {
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
        "phone": phone,
        "organization": organization,
        "street_address": street_address,
        "city": city,
        "state": state,
        "zipcode": zipcode

    }
    write_data(data)

def check_user(username):
    """
    Check if the provided username and password are valid.
    """
    data = read_data()
    if username in data:
        return True
    else:
        return False

def authenticate(username,password):
    data = read_data()
    if username in data and data[username]["password"] == password:
        return True
    else:
        return False