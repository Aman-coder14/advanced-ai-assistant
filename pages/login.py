import streamlit as st

from auth.login_manager import authenticate_user
from auth.session_manager import start_session


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
                try:
                    user = authenticate_user(email, password)
                    if user is None:
                        st.error("Invalid email or password.")
                    else:
                        start_session(user)
                        st.rerun()
                except Exception as exc:
                    st.error(f"Login failed: {exc}")

        with col2:
            if st.button("Create Account"):
                st.session_state.page = "Register"
                st.rerun()

    st.info("Frontend Demo Version")
