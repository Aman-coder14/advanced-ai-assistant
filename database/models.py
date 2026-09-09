from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	__tablename__ = "users"

	id: Mapped[str] = mapped_column(String(36), primary_key=True)
	email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
	name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
	password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
	created_at: Mapped[str] = mapped_column(String, nullable=False, server_default=text("CURRENT_TIMESTAMP::text"))
	chats: Mapped[list["ChatModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ChatModel(Base):
	__tablename__ = "chats"

	id: Mapped[str] = mapped_column(String(36), primary_key=True)
	user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	title: Mapped[str] = mapped_column(String(255), nullable=False, default="New Chat")
	created_at: Mapped[str] = mapped_column(String, nullable=False, server_default=text("CURRENT_TIMESTAMP::text"))
	updated_at: Mapped[str] = mapped_column(String, nullable=False, server_default=text("CURRENT_TIMESTAMP::text"))
	user: Mapped[UserModel] = relationship(back_populates="chats")
	messages: Mapped[list["MessageModel"]] = relationship(back_populates="chat", cascade="all, delete-orphan")

	__table_args__ = (
		Index("idx_chats_user_id", "user_id"),
		Index("idx_chats_updated_at", "updated_at"),
	)


class MessageModel(Base):
	__tablename__ = "messages"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	chat_id: Mapped[str] = mapped_column(String(36), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
	role: Mapped[str] = mapped_column(String(20), nullable=False)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	timestamp: Mapped[str] = mapped_column(String, nullable=False, server_default=text("CURRENT_TIMESTAMP::text"))
	chat: Mapped[ChatModel] = relationship(back_populates="messages")

	__table_args__ = (
		CheckConstraint("role IN ('user', 'assistant', 'system')", name="ck_messages_role"),
		Index("idx_messages_chat_id", "chat_id"),
		Index("idx_messages_timestamp", "timestamp"),
	)
