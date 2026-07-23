import streamlit as st


def show_sidebar():
    st.sidebar.markdown("# AI Workspace")

    st.sidebar.divider()

    pages = [
        "Dashboard",
        "Chat",
        "Voice Chat",
        "Documents",
        "Image Chat",
        "Research",
        "History",
        "Profile",
        "Settings",
    ]
    current_page = st.session_state.get("page", "Dashboard")
    if current_page not in pages:
        current_page = "Dashboard"

    menu = st.sidebar.radio(
        "Navigation",
        pages,
        index=pages.index(current_page),
    )
    st.session_state.page = menu

    st.sidebar.divider()

    st.sidebar.info("Frontend Version 1.0")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()

    return menu
