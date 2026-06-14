from services.chat_service import (
    clear_chat,
    create_new_chat,
    delete_chat,
    get_chat,
    get_or_create_user,
    get_messages,
    get_user_chats,
    load_chat,
    rename_chat,
    save_message,
)
from database.db import get_connection, init_db


def create_chat(user_id="default", title="New Chat"):
    chat_id = create_new_chat(_resolve_user_id(user_id))
    if title != "New Chat":
        rename_chat(chat_id, title)
    return chat_id


def add_message(chat_id, role, content):
    save_message(chat_id, role, content)


def list_chats(user_id="default", search=""):
    return get_user_chats(_resolve_user_id(user_id), search)


def messages_as_dicts(chat_id):
    return load_chat(chat_id)


def _resolve_user_id(user_id_or_email):
    init_db()
    value = str(user_id_or_email or "default").strip()
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM users WHERE id = ?", (value,)).fetchone()
    if row:
        return row["id"]
    return get_or_create_user(value).id
