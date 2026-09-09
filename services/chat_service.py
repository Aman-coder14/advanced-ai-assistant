from __future__ import annotations

import re
import uuid

from sqlalchemy import text

from database.db import get_connection, init_db
from models.chat_model import Chat, Message, User


DEFAULT_CHAT_TITLE = "New Chat"


def _execute(connection, query: str, params=()):
    values = {}
    if isinstance(params, dict):
        values = params
    else:
        for index, value in enumerate(params):
            query = query.replace("?", f":param_{index}", 1)
            values[f"param_{index}"] = value
    return connection.execute(text(query), values).mappings()


def get_or_create_user(email: str = "default", name: str = "") -> User:
    init_db()
    clean_email = (email or "default").strip().lower()
    clean_name = (name or clean_email.split("@")[0] or "User").strip()

    with get_connection() as conn:
        row = _execute(conn,
            "SELECT id, email, name, created_at FROM users WHERE email = ?",
            (clean_email,),
        ).fetchone()
        if row:
            return _user_from_row(row)

        user_id = str(uuid.uuid4())
        _execute(conn,
            "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
            (user_id, clean_email, clean_name),
        )
        row = _execute(conn,
            "SELECT id, email, name, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return _user_from_row(row)


def create_new_chat(user_id: str) -> str:
    init_db()
    chat_id = str(uuid.uuid4())
    with get_connection() as conn:
        _execute(conn,
            "INSERT INTO chats (id, user_id, title) VALUES (?, ?, ?)",
            (chat_id, user_id, DEFAULT_CHAT_TITLE),
        )
    return chat_id


def load_chat(chat_id: str) -> list[dict[str, str]]:
    init_db()
    with get_connection() as conn:
        rows = _execute(conn,
            """
            SELECT id, chat_id, role, content, timestamp
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,),
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def save_message(chat_id: str, role: str, content: str) -> None:
    init_db()
    clean_role = (role or "").strip().lower()
    clean_content = (content or "").strip()
    if clean_role not in {"user", "assistant", "system"}:
        raise ValueError(f"Invalid message role: {role}")
    if not clean_content:
        return

    with get_connection() as conn:
        chat = _execute(conn,
            "SELECT id, title FROM chats WHERE id = ?",
            (chat_id,),
        ).fetchone()
        if not chat:
            raise ValueError("Cannot save message because chat does not exist.")

        _execute(conn,
            """
            INSERT INTO messages (chat_id, role, content)
            VALUES (?, ?, ?)
            """,
            (chat_id, clean_role, clean_content),
        )
        _execute(conn,
            "UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (chat_id,),
        )

        if clean_role == "user" and chat["title"] == DEFAULT_CHAT_TITLE:
            title = generate_chat_title(clean_content)
            _execute(conn,
                """
                UPDATE chats
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND title = ?
                """,
                (title, chat_id, DEFAULT_CHAT_TITLE),
            )


def clear_chat(chat_id: str) -> None:
    init_db()
    with get_connection() as conn:
        _execute(conn, "DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        _execute(conn,
            "UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (chat_id,),
        )


def delete_chat(chat_id: str) -> None:
    init_db()
    with get_connection() as conn:
        _execute(conn, "DELETE FROM chats WHERE id = ?", (chat_id,))


def rename_chat(chat_id: str, new_title: str) -> None:
    init_db()
    title = (new_title or DEFAULT_CHAT_TITLE).strip() or DEFAULT_CHAT_TITLE
    with get_connection() as conn:
        _execute(conn,
            """
            UPDATE chats
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title[:80], chat_id),
        )


def get_user_chats(user_id: str, search: str = "") -> list[Chat]:
    init_db()
    params: list[str] = [user_id]
    where = "WHERE c.user_id = ?"
    if search:
        where += """
            AND (
                c.title LIKE ?
                OR EXISTS (
                    SELECT 1
                    FROM messages sm
                    WHERE sm.chat_id = c.id AND sm.content LIKE ?
                )
            )
        """
        term = f"%{search.strip()}%"
        params.extend([term, term])

    with get_connection() as conn:
        rows = _execute(conn,
            f"""
            SELECT
                c.id,
                c.user_id,
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
            {where}
            GROUP BY c.id
            ORDER BY c.updated_at DESC, c.created_at DESC
            """,
            params,
        ).fetchall()
    return [_chat_from_row(row) for row in rows]


def get_chat(chat_id: str) -> Chat | None:
    init_db()
    with get_connection() as conn:
        row = _execute(conn,
            """
            SELECT
                c.id,
                c.user_id,
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
            WHERE c.id = ?
            GROUP BY c.id
            """,
            (chat_id,),
        ).fetchone()
    return _chat_from_row(row) if row else None


def get_latest_or_create_chat(user_id: str) -> str:
    chats = get_user_chats(user_id)
    if chats:
        return chats[0].id
    return create_new_chat(user_id)


def get_messages(chat_id: str) -> list[Message]:
    init_db()
    with get_connection() as conn:
        rows = _execute(conn,
            """
            SELECT id, chat_id, role, content, timestamp
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,),
        ).fetchall()
    return [_message_from_row(row) for row in rows]


def generate_chat_title(prompt: str) -> str:
    text = re.sub(r"\s+", " ", (prompt or "").strip())
    text = re.sub(r"[?!.]+$", "", text)
    if not text:
        return DEFAULT_CHAT_TITLE

    lower = text.lower()
    if "ipl" in lower and re.search(r"\b(won|winner|win)\b", lower):
        year = re.search(r"\b(20\d{2})\b", text)
        return f"IPL {year.group(1)} Winner" if year else "IPL Winner"

    text = re.sub(
        r"^(explain|what is|what are|who is|who was|who won|tell me about|write about|give me|show me)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )
    words = [word for word in re.split(r"\s+", text) if word]
    words = words[:6]
    title_words = [_format_title_word(word) for word in words]
    return (" ".join(title_words) or DEFAULT_CHAT_TITLE)[:80]


def _format_title_word(word: str) -> str:
    clean = re.sub(r"^[^\w]+|[^\w]+$", "", word)
    if not clean:
        return ""
    if clean.isupper() or clean.isdigit():
        return clean
    if re.match(r"^[A-Za-z]+\d+$", clean):
        return clean.upper()
    return clean.capitalize()


def _user_from_row(row) -> User:
    return User(
        id=row["id"],
        email=row["email"],
        name=row["name"],
        created_at=row["created_at"],
    )


def _chat_from_row(row) -> Chat:
    return Chat(
        id=row["id"],
        user_id=row["user_id"],
        title=row["title"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        message_count=row["message_count"] or 0,
        preview=row["preview"],
    )


def _message_from_row(row) -> Message:
    return Message(
        id=row["id"],
        chat_id=row["chat_id"],
        role=row["role"],
        content=row["content"],
        timestamp=row["timestamp"],
    )
