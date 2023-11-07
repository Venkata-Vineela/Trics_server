
import sqlite3



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

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def authenticate(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Check if the provided username and password match a user record in the database
    cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    conn.close()

    # If a user is found, return True (authenticated); otherwise, return False
    return result is not None


def getunames(query):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, firstname FROM users WHERE firstname LIKE ? LIMIT 4', ('%' + query + '%',))
    # suggested_usernames = [row[0] for row in cursor.fetchall()]


    searchres_usernames = [{'username': row[0], 'firstname': row[1]} for row in cursor.fetchall()]
    conn.close()


    return searchres_usernames

def get_user_data(username):
    username = username.strip()
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstname, lastname, organization FROM users WHERE username = ?', (username,))
    user_data = [{'firstname': row[0], 'lastname': row[1], 'organization': row[2]} for row in cursor.fetchall()]
    conn.close()

    return user_data;


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
                    SELECT username, firstname FROM users
                    WHERE (organization = ? AND username != ?) 
                     OR 
                     (zipcode = ? AND username != ?)
                    LIMIT 10
                  ''', (organization, username, zipcode, username))

        suggestions = [{'username': row[0], 'firstname': row[1]} for row in cursor.fetchall()]

    conn.close()
    return suggestions


def add_friend_connection(username, friendusername):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Insert the friend connection into the 'friends' table
    cursor.execute("INSERT INTO friends (username, friendusername) VALUES (?, ?)", (username, friendusername))

    conn.commit()
    conn.close()


def isfriend(username, friendusername):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Insert the friend connection into the 'friends' table
    cursor.execute(
        "SELECT * FROM friends WHERE (username = ? AND friendusername = ?) OR (username = ? AND friendusername = ?)",
        (username, friendusername, friendusername, username))
    result = cursor.fetchone()

    conn.commit()
    conn.close()
    return result is not None
