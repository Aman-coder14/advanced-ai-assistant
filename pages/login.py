import streamlit as st

from services.chat_service import get_or_create_user


def show_login():

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🚀 AI Workspace
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Login")

    with st.container():

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                user = get_or_create_user(email.strip() or "default")
                st.session_state.logged_in = True
                st.session_state.user_id = user.id
                st.session_state.user_email = user.email
                st.session_state.active_chat_id = st.session_state.get("active_chat_id")
                st.session_state.page = "Dashboard"
                st.rerun()

        with col2:
            if st.button("Create Account"):
                st.session_state.page = "Register"
                st.rerun()

    st.info("Frontend Demo Version")
