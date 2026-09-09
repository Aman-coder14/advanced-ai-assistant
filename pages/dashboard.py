import streamlit as st
from components.cards import metric_card, activity_card


def show_dashboard():

    st.markdown(
        '<div class="page-title">🏠 Dashboard</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Chats", "24")

    with col2:
        metric_card("Documents", "12")

    with col3:
        metric_card("Research Tasks", "7")

    with col4:
        metric_card("Status", "Active")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">⚡ Quick Actions</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.button("💬 New Chat")

    with q2:
        st.button("📄 Upload")

    with q3:
        st.button("🔍 Research")

    with q4:
        st.button("📚 History")

    st.markdown(
        '<div class="section-title">📌 Recent Activity</div>',
        unsafe_allow_html=True
    )

    activity_card(
        "DBMS Chat",
        "Asked questions about Normalization and SQL."
    )

    activity_card(
        "Uploaded Resume",
        "Resume.pdf uploaded successfully."
    )

    activity_card(
        "Research Task",
        "AI Jobs Market 2026 Analysis."
    )