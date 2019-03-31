import sqlite3
#import project
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import json
from flask import Flask, request, render_template

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('news.db', check_same_thread=False)


    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()

class UserModel:
    def __init__(self, connection):
        self.connection = connection


    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             age INTEGER,
                             email VARCHAR(128),
                             sex VARCHAR(10)
                             )''')
        cursor.close()
        self.connection.commit()


    def insert(self, user_name, password_hash, age, email, sex):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users
                          (user_name, password_hash, age, email, sex)
                          VALUES (?,?,?,?,?)''', (user_name, password_hash, age, email, sex))
        cursor.close()
        self.connection.commit()


    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def get_id(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE user_name = ?",
                       (user_name,))
        row = cursor.fetchone()
        return row


    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class FilmModel:
    def __init__(self, connection):
        self.connection = connection


    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS films
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             film_name VARCHAR(50),
                             genre VARCHAR(128),
                             description VARCHAR(512),
                             yearf INTEGER
                             )''')
        cursor.close()
        self.connection.commit()


    def insert(self,film_name, genre, description, yearf):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO films
                          (film_name, genre, description, yearf)
                          VALUES (?,?,?,?)''', (film_name, genre, description, yearf))
        cursor.close()
        self.connection.commit()


    def get(self, film_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name, description FROM films WHERE film_name = ?", (film_name,))
        rows = cursor.fetchall()
        return rows

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films")
        rows = cursor.fetchall()
        return rows

    def get_year(self, yearf):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films WHERE yearf = ?", (yearf,))
        rows = cursor.fetchall()
        return rows

    def get_id(self, film_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM films WHERE film_name = ?",
                       (film_name,))
        row = cursor.fetchone()
        return row

    def exists(self, film_name, yearf):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films WHERE film_name = ? AND yearf = ?",
                       (film_name, yearf))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class CommentModel:
    def __init__(self, connection):
        self.connection = connection


    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             film_id INTEGER,
                             user_id INTEGER,
                             about VARCHAR(512),
                             rate INTEGER
                             )''')
        cursor.close()
        self.connection.commit()


    def insert(self, film_id, user_id, about, rate):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO comments
                          (film_id, user_id, about, rate)
                          VALUES (?,?,?,?)''', (film_id, user_id, about, rate))
        cursor.close()
        self.connection.commit()


    def get(self, film_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id, about FROM comments WHERE film_id = ?", (film_id,))
        rows = cursor.fetchall()
        return rows

    def getRate(self, film_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT rate FROM comments WHERE film_id = ?", (film_id,))
        rows = cursor.fetchall()
        return rows

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films")
        rows = cursor.fetchall()
        return rows

    def exists(self, film_id, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE film_id = ? AND user_id = ?",
                       (film_id, user_id))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


