import streamlit as st
from components.cards import profile_card


def show_profile():

    st.markdown(
        '<div class="page-title">👤 Profile</div>',
        unsafe_allow_html=True
    )

    profile_card(
        "Aman Singh",
        "aman@example.com"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Chats", "24")

    with col2:
        st.metric("Documents", "12")

    st.markdown("### Account Information")

    st.write("📅 Joined: January 2026")
    st.write("🎓 Student")
    st.write("💻 CSE Engineer")
    st.write("🚀 AI Workspace User")

    st.button("✏ Edit Profile")