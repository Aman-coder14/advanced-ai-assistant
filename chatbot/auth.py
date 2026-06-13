import hashlib
import sqlite3
from datetime import datetime

DB_PATH = "data/users.db"


def init_users_table():
    """Initialize users table with secure password storage."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def signup(email: str, username: str, password: str) -> tuple[bool, str]:
    """Register a new user account."""
    try:
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        if not email or not username:
            return False, "Email and username are required."
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        pwd_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
            (email.lower().strip(), username.strip(), pwd_hash)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Account created successfully! Welcome, {username}."
        
    except sqlite3.IntegrityError:
        return False, "This email or username is already registered. Please login instead."
    except Exception as e:
        return False, f"Registration Error: {str(e)}"


def login(email: str, password: str) -> tuple[bool, str]:
    """Authenticate user login."""
    try:
        if not email or not password:
            return False, "Email and password are required."
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        pwd_hash = hash_password(password)
        
        cursor.execute(
            "SELECT username FROM users WHERE email = ? AND password_hash = ?",
            (email.lower().strip(), pwd_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, user[0]
        return False, "Invalid email or password. Please try again."
        
    except Exception as e:
        return False, f"Login Error: {str(e)}"


def user_exists(email: str) -> bool:
    """Check if user account exists."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email.lower().strip(),))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    except Exception:
        return False


def get_user_by_email(email: str) -> dict:
    """Get user profile by email."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT email, username, created_at FROM users WHERE email = ?",
            (email.lower().strip(),)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {"email": user[0], "username": user[1], "created_at": user[2]}
        return None
    except Exception:
        return None


# Initialize users table on import
init_users_table()