import streamlit as st

from auth.auth import validate_email, validate_password
from auth.login_manager import register_user
from auth.session_manager import start_session

def show_register():

    st.markdown(
        """
        <h1 style='text-align:center;'>
        📝 Create Account
        </h1>
        """,
        unsafe_allow_html=True
    )

    name = st.text_input(
        "Full Name",
        placeholder="Enter your name"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):
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
        if st.button("Back to Login"):
            st.session_state.page = "Login"
            st.rerun()