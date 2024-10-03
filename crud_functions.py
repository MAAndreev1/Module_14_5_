import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    );
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    if not is_included(username):
        cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (username, email, age, 1000))

    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    all_users = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()

    connection.commit()
    connection.close()

    return all_users is not None


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

def delete_all_users():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Users')

    connection.commit()
    connection.close()
