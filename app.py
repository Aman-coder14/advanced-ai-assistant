import streamlit as st

from components.styles import load_css
from components.sidebar import show_sidebar

from pages.login import show_login
from pages.register import show_register
from pages.dashboard import show_dashboard
from pages.chat import show_chat
from pages.image_chat import show_image_chat
from pages.documents import show_documents
from pages.research import show_research
from pages.history import show_history
from pages.profile import show_profile
from pages.settings import show_settings


st.set_page_config(
    page_title="AI Workspace",
    page_icon="🚀",
    layout="wide"
)

load_css()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"


# -------------------
# AUTH PAGES
# -------------------

if not st.session_state.logged_in:

    if st.session_state.page == "Login":
        show_login()

    elif st.session_state.page == "Register":
        show_register()

# -------------------
# MAIN APP
# -------------------

else:

    selected_page = show_sidebar()

    if selected_page == "Dashboard":
        show_dashboard()

    elif selected_page == "Chat":
        show_chat()

    elif selected_page == "Documents":
        show_documents()

    elif selected_page == "Research":
        show_research()

    elif selected_page == "History":
        show_history()

    elif selected_page == "Profile":
        show_profile()

    elif selected_page == "Settings":
        show_settings()

    elif selected_page == "Image Chat":
        show_image_chat()