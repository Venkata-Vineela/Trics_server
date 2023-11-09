import sqlite3
from flask import Flask, request, jsonify, session
def delete(username):
    friendusername = 'V@gmail.com'

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM friendrequests WHERE username = ? AND friendusername = ?", (friendusername, username))
    conn.commit()

    conn.close()


if __name__ == '__main__':
    username = 'Va@gmail.com'

    delete(username)



