import sqlite3

if __name__ == '__main__':
    username = "Va@gmail.com"
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
              ''', (organization, username,zipcode, username))

        suggestions = [row[0] for row in cursor.fetchall()]

    conn.close()
    #print(suggestions)
    #return suggestions