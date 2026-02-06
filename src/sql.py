import sqlite3
import datetime
import os

if not os.path.exists("../data"):
        os.mkdir("../data")
connection = sqlite3.connect("../data/data.db")

def init_db():

    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        user TEXT NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)
    connection.commit()

def add_message(chat_message: tuple[str, str]):
    user: str = chat_message[0].removeprefix("@")
    message: str = chat_message[1]

    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (name) VALUES (?)",
        (user,)  
    )
    time: str = str(datetime.datetime.now())
    cursor.execute("INSERT INTO messages (user, message, time) VALUES (?, ?, ?)",
        (user, message, time)  
    )
    connection.commit()