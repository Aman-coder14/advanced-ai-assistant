from __future__ import annotations

import streamlit as st

from models.chat_model import User


def start_session(user: User) -> None:
	st.session_state.logged_in = True
	st.session_state.user_id = user.id
	st.session_state.user_email = user.email
	st.session_state.page = "Dashboard"
	st.session_state.pop("active_chat_id", None)
	st.session_state.pop("messages", None)


def end_session() -> None:
	for key in (
		"logged_in",
		"user_id",
		"user_email",
		"active_chat_id",
		"messages",
		"chat_history",
	):
		st.session_state.pop(key, None)
	st.session_state.logged_in = False
	st.session_state.page = "Login"
