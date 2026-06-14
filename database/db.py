from __future__ import annotations

import os
import sqlite3
import uuid
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("CHAT_DB_PATH", BASE_DIR / "chats.db"))


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        _migrate_legacy_schema(conn)
        _create_tables(conn)
        _create_indexes(conn)


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT 'New Chat',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE
        )
        """
    )


def _create_indexes(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chats_updated_at ON chats(updated_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")


def _migrate_legacy_schema(conn: sqlite3.Connection) -> None:
    if not _table_exists(conn, "chats"):
        return

    columns = _table_columns(conn, "chats")
    if columns.get("id", "").upper() == "TEXT" and "user_id" in columns:
        _migrate_messages_timestamp(conn)
        return

    legacy_chats = conn.execute("SELECT * FROM chats ORDER BY id ASC").fetchall()
    legacy_messages = []
    if _table_exists(conn, "messages"):
        legacy_messages = conn.execute("SELECT * FROM messages ORDER BY id ASC").fetchall()

    if _table_exists(conn, "legacy_chats"):
        conn.execute("DROP TABLE legacy_chats")
    if _table_exists(conn, "legacy_messages"):
        conn.execute("DROP TABLE legacy_messages")

    conn.execute("ALTER TABLE chats RENAME TO legacy_chats")
    if _table_exists(conn, "messages"):
        conn.execute("ALTER TABLE messages RENAME TO legacy_messages")

    _create_tables(conn)

    default_user_id = str(uuid.uuid4())
    conn.execute(
        "INSERT OR IGNORE INTO users (id, email, name) VALUES (?, ?, ?)",
        (default_user_id, "default", "Default User"),
    )

    id_map: dict[str, str] = {}
    for legacy_chat in legacy_chats:
        old_id = str(legacy_chat["id"])
        new_id = str(uuid.uuid4())
        id_map[old_id] = new_id
        conn.execute(
            """
            INSERT INTO chats (id, user_id, title, created_at, updated_at)
            VALUES (?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP), COALESCE(?, CURRENT_TIMESTAMP))
            """,
            (
                new_id,
                default_user_id,
                legacy_chat["title"] or "New Chat",
                _row_get(legacy_chat, "created_at"),
                _row_get(legacy_chat, "updated_at"),
            ),
        )

    for legacy_message in legacy_messages:
        old_chat_id = str(legacy_message["chat_id"])
        new_chat_id = id_map.get(old_chat_id)
        if not new_chat_id:
            continue
        conn.execute(
            """
            INSERT INTO messages (chat_id, role, content, timestamp)
            VALUES (?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP))
            """,
            (
                new_chat_id,
                legacy_message["role"],
                legacy_message["content"],
                _row_get(legacy_message, "timestamp") or _row_get(legacy_message, "created_at"),
            ),
        )

    conn.execute("DROP TABLE legacy_chats")
    if _table_exists(conn, "legacy_messages"):
        conn.execute("DROP TABLE legacy_messages")


def _migrate_messages_timestamp(conn: sqlite3.Connection) -> None:
    if not _table_exists(conn, "messages"):
        return
    columns = _table_columns(conn, "messages")
    if "timestamp" not in columns:
        conn.execute("ALTER TABLE messages ADD COLUMN timestamp TEXT")
        conn.execute(
            """
            UPDATE messages
            SET timestamp = COALESCE(created_at, CURRENT_TIMESTAMP)
            WHERE timestamp IS NULL
            """
        )


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _table_columns(conn: sqlite3.Connection, table_name: str) -> dict[str, str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"]: row["type"] for row in rows}


def _row_get(row: sqlite3.Row, key: str):
    return row[key] if key in row.keys() else None
