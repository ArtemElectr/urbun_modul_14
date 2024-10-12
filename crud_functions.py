import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT ,
        price INTEGER NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        """
    )
    connection.commit()


def get_all_products():
    cursor.execute('''
        SELECT * FROM Products
    ''')
    connection.commit()
    return cursor.fetchall()


def add_user(username, email, age):
    cursor.execute("""
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
    """, (username, email, age, 1000))
    connection.commit()


def is_included(username):
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    is_user = cursor.fetchone()
    if is_user:
        return True
    else:
        return False
