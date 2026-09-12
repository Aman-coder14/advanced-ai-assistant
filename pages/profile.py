import streamlit as st
from components.cards import profile_card


def show_profile():

    st.markdown(
        """
        <div class="page-title">👤 Profile</div>
        <div class="page-subtitle">Your account information and workspace stats.</div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 2, 1])
    with center:
        profile_card(
            "Aman Singh",
            "aman@example.com",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Chats", "24")

    with col2:
        st.metric("Documents", "12")

    st.markdown(
        '<div class="section-title">ℹ️ Account Information</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="custom-card">
            <p>📅 &nbsp;<strong>Joined:</strong> January 2026</p>
            <p>🎓 &nbsp;<strong>Role:</strong> Student</p>
            <p>💻 &nbsp;<strong>Major:</strong> CSE Engineer</p>
            <p>🚀 &nbsp;<strong>Plan:</strong> AI Workspace User</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("✏ Edit Profile", use_container_width=False)