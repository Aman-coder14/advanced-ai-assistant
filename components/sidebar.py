import streamlit as st


def show_sidebar():
    st.sidebar.markdown("# 🚀 AI Workspace")

    st.sidebar.divider()

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Chat",
            "Documents",
            "Research",
            "History",
            "Profile",
            "Settings"
        ]
    )

    st.sidebar.divider()

    st.sidebar.info("Frontend Version 1.0")

    st.sidebar.button("🚪 Logout")

    return menu