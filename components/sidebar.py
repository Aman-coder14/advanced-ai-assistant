import streamlit as st

from auth.session_manager import end_session


# Page icons for navigation
_PAGE_ICONS = {
    "Dashboard":  "⬡",
    "Chat":       "💬",
    "Voice Chat": "🎙️",
    "Documents":  "📄",
    "Image Chat": "🖼️",
    "Research":   "🔍",
    "History":    "🕐",
    "Profile":    "👤",
    "Settings":   "⚙️",
}


def show_sidebar():
    # ── Branded header ──────────────────────────────────────────
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-logo">⬡ AI Workspace</div>
            <div class="sidebar-brand-tagline">Powered by Groq &amp; Gemini</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    # Icon-prefixed labels
    labeled_pages = [f"{_PAGE_ICONS.get(p, '')}  {p}" for p in pages]

    selected_label = st.sidebar.radio(
        "Navigation",
        labeled_pages,
        index=pages.index(current_page),
        label_visibility="collapsed",
    )

    # Map back to plain page name
    menu = pages[labeled_pages.index(selected_label)]
    st.session_state.page = menu

    st.sidebar.divider()

    st.sidebar.markdown(
        """
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            color: #475569;
            text-align: center;
            padding: 4px 0;
            letter-spacing: 0.3px;
        ">
            Frontend v1.0 &nbsp;·&nbsp; AI Workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    if st.sidebar.button("⏻  Logout", use_container_width=True):
        end_session()
        st.rerun()

    return menu
