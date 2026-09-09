from __future__ import annotations

import re

import bcrypt


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> str | None:
	clean_email = (email or "").strip().lower()
	if not EMAIL_PATTERN.fullmatch(clean_email):
		return "Enter a valid email address."
	return None


def validate_password(password: str, confirmation: str | None = None) -> str | None:
	if len(password or "") < 8:
		return "Password must be at least 8 characters long."
	if confirmation is not None and password != confirmation:
		return "Passwords do not match."
	return None


def hash_password(password: str) -> str:
	return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
	if not password_hash:
		return False
	try:
		return bcrypt.checkpw(
			password.encode("utf-8"), password_hash.encode("utf-8")
		)
	except (ValueError, TypeError):
		return False
