from __future__ import annotations

import uuid

from sqlalchemy import text

from auth.auth import hash_password, validate_email, validate_password, verify_password
from database.db import get_connection, init_db
from models.chat_model import User


def register_user(email: str, name: str, password: str, confirmation: str) -> User:
	clean_email = (email or "").strip().lower()
	clean_name = (name or "").strip() or clean_email.split("@")[0]
	email_error = validate_email(clean_email)
	password_error = validate_password(password, confirmation)
	if email_error:
		raise ValueError(email_error)
	if password_error:
		raise ValueError(password_error)

	init_db()
	with get_connection() as connection:
		existing = connection.execute(
			text("SELECT 1 FROM users WHERE email = :email"),
			{"email": clean_email},
		).scalar_one_or_none()
		if existing:
			raise ValueError("An account with this email already exists.")

		user_id = str(uuid.uuid4())
		connection.execute(
			text(
				"""
				INSERT INTO users (id, email, name, password_hash)
				VALUES (:id, :email, :name, :password_hash)
				"""
			),
			{
				"id": user_id,
				"email": clean_email,
				"name": clean_name,
				"password_hash": hash_password(password),
			},
		)
	return User(id=user_id, email=clean_email, name=clean_name, created_at="")


def authenticate_user(email: str, password: str) -> User | None:
	clean_email = (email or "").strip().lower()
	if validate_email(clean_email) or not password:
		return None

	init_db()
	with get_connection() as connection:
		row = connection.execute(
			text(
				"""
				SELECT id, email, name, created_at, password_hash
				FROM users
				WHERE email = :email
				"""
			),
			{"email": clean_email},
		).mappings().fetchone()

	if not row or not verify_password(password, row["password_hash"]):
		return None
	return User(
		id=row["id"],
		email=row["email"],
		name=row["name"],
		created_at=row["created_at"],
	)
