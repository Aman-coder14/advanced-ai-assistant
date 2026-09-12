import streamlit as st

from auth.auth import validate_email, validate_password
from auth.login_manager import register_user
from auth.session_manager import start_session

def show_register():

    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown(
            """
            <div class="auth-card">
                <div class="auth-logo">📝</div>
                <div class="auth-title">Create Account</div>
                <div class="auth-subtitle">Join AI Workspace — it's free</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
        )

        email = st.text_input(
            "Email address",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Register", use_container_width=True):
                email_error = validate_email(email)
                password_error = validate_password(password, confirm_password)
                if email_error:
                    st.error(email_error)
                elif password_error:
                    st.error(password_error)
                else:
                    try:
                        user = register_user(email, name, password, confirm_password)
                        start_session(user)
                        st.success("Account created successfully.")
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
                    except Exception as exc:
                        st.error(f"Registration failed: {exc}")

        with col2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()