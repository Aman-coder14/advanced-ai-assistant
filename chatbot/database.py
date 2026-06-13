import sqlite3
from datetime import datetime

# Database paths
CHATS_DB_PATH = "data/chats.db"
USERS_DB_PATH = "data/users.db"

# ==========================================
# CHAT HISTORY DATABASE (Simple chats)
# ==========================================

def connect_chats_db():
    """Connect to chats database."""
    conn = sqlite3.connect(CHATS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_chats_table():
    """Initialize chats table for storing user and AI responses."""
    conn = connect_chats_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


def save_chat(user_message, ai_response):
    """Save a single chat exchange."""
    try:
        conn = connect_chats_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO chats(user_message, ai_response, created_at) VALUES (?, ?, ?)",
            (user_message, ai_response, datetime.now().isoformat())
        )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Save Chat Error: {e}")
        return False


def get_all_chats():
    """Retrieve all saved chats."""
    try:
        conn = connect_chats_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM chats ORDER BY created_at DESC")
        data = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in data]
    except Exception as e:
        print(f"Get Chats Error: {e}")
        return []


def clear_all_chats():
    """Clear all chat history."""
    try:
        conn = connect_chats_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Clear Chats Error: {e}")
        return False


# ==========================================
# SESSION & USER DATABASE
# ==========================================

def init_session_tables():
    """Initialize session and message tracking tables."""
    conn = sqlite3.connect(USERS_DB_PATH)
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


def create_new_session(session_id, user_email, title):
    """Create a new chat session."""
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR IGNORE INTO chat_sessions (session_id, user_email, title) VALUES (?, ?, ?)",
            (session_id, user_email, title)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Create Session Error: {e}")
        return False


def save_message(session_id, role, content):
    """Save a message in a session."""
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Save Message Error: {e}")
        return False


def get_session_messages(session_id):
    """Retrieve all messages from a session."""
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        messages = cursor.fetchall()
        conn.close()
        
        return [{"role": msg[0], "content": msg[1], "timestamp": msg[2]} for msg in messages]
    except Exception as e:
        print(f"Get Messages Error: {e}")
        return []


def get_user_sessions(user_email):
    """Get all sessions for a user."""
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT session_id, title, created_at FROM chat_sessions WHERE user_email = ? ORDER BY created_at DESC",
            (user_email,)
        )
        sessions = cursor.fetchall()
        conn.close()
        
        return [{"session_id": s[0], "title": s[1], "created_at": s[2]} for s in sessions]
    except Exception as e:
        print(f"Get Sessions Error: {e}")
        return []

# Initialize database tables on import
init_chats_table()
init_session_tables()