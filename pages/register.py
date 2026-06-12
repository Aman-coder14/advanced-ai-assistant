import streamlit as st


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
            st.success(
                "Frontend Demo: Account Created"
            )

    with col2:
        if st.button("Back to Login"):
            st.session_state.page = "Login"
            st.rerun()