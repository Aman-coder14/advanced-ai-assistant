import sqlite3


def connect_db():
    conn = sqlite3.connect("data/chats.db")
    return conn


def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        ai_response TEXT
    )
    ''')

    conn.commit()
    conn.close()


create_table()

def save_chat(user_message, ai_response):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(user_message, ai_response) VALUES (?, ?)",
        (user_message, ai_response)
    )

    conn.commit()
    conn.close()


def get_all_chats():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chats")

    data = cursor.fetchall()

    conn.close()

    return data