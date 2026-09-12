import streamlit as st

from auth.login_manager import authenticate_user
from auth.session_manager import start_session


def show_login():

    # Centered layout using columns
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown(
            """
            <div class="auth-card">
                <div class="auth-logo">🚀</div>
                <div class="auth-title">AI Workspace</div>
                <div class="auth-subtitle">Sign in to your account to continue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input(
            "Email address",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sign In", use_container_width=True):
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
            if st.button("Create Account", use_container_width=True):
                st.session_state.page = "Register"
                st.rerun()

        st.markdown(
            """
            <div style="
                text-align: center;
                margin-top: 20px;
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                color: #475569;
            ">
                Frontend Demo Version · AI Workspace v1.0
            </div>
            """,
            unsafe_allow_html=True,
        )
