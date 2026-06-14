from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    email: str
    name: str
    created_at: str


@dataclass(frozen=True)
class Chat:
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0
    preview: str | None = None


@dataclass(frozen=True)
class Message:
    id: int
    chat_id: str
    role: str
    content: str
    timestamp: str
