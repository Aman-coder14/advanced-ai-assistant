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


    # Just copy and paste this to the bottom of your existing database.py file:

def init_chat_tables(conn_or_path="data/chatbot.db"):
    """Creates the chat tracking tables inside your existing database structure."""
    import sqlite3
    conn = sqlite3.connect(conn_or_path)
    cursor = conn.cursor()
    
    # Session tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            user_email TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Message storage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def create_new_session(session_id, user_email, title, db_path="data/chatbot.db"):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO chat_sessions (session_id, user_email, title) VALUES (?, ?, ?)",
            (session_id, user_email, title)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def save_message(session_id, role, content, db_path="data/chatbot.db"):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_user_sessions(user_email, db_path="data/chatbot.db"):
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chat_sessions WHERE user_email = ? ORDER BY created_at DESC",
        (user_email,)
    )
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_session_messages(session_id, db_path="data/chatbot.db"):
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row["role"], "content": row["content"]} for row in rows]