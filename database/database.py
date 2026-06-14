from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "chats.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL DEFAULT 'default',
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id)"
        )


def create_chat(user_id="default", title="New Chat"):
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO chats (user_id, title) VALUES (?, ?)",
            (user_id, title),
        )
        return cursor.lastrowid


def add_message(chat_id, role, content):
    init_db()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content),
        )
        conn.execute(
            "UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (chat_id,),
        )


def rename_chat(chat_id, title):
    init_db()
    with get_connection() as conn:
        conn.execute(
            "UPDATE chats SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (title.strip() or "New Chat", chat_id),
        )


def delete_chat(chat_id):
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))


def get_chat(chat_id):
    init_db()
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM chats WHERE id = ?",
            (chat_id,),
        ).fetchone()


def get_messages(chat_id):
    init_db()
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,),
        ).fetchall()


def list_chats(user_id="default", search=""):
    init_db()
    query = """
        SELECT
            c.id,
            c.title,
            c.created_at,
            c.updated_at,
            COUNT(m.id) AS message_count,
            (
                SELECT sm.content
                FROM messages sm
                WHERE sm.chat_id = c.id AND sm.role = 'user'
                ORDER BY sm.id DESC
                LIMIT 1
            ) AS preview
        FROM chats c
        LEFT JOIN messages m ON m.chat_id = c.id
        WHERE c.user_id = ?
    """
    params = [user_id]

    if search:
        query += """
            AND (
                c.title LIKE ?
                OR EXISTS (
                    SELECT 1
                    FROM messages sm
                    WHERE sm.chat_id = c.id AND sm.content LIKE ?
                )
            )
        """
        term = f"%{search}%"
        params.extend([term, term])

    query += """
        GROUP BY c.id
        ORDER BY c.updated_at DESC, c.id DESC
    """

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def messages_as_dicts(chat_id):
    return [
        {"role": row["role"], "content": row["content"]}
        for row in get_messages(chat_id)
    ]
