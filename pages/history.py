import streamlit as st


def show_history():

    st.markdown(
        '<div class="page-title">📚 Chat History</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "🔍 Search Chats",
        placeholder="Search previous conversations..."
    )

    st.markdown(
        '<div class="section-title">Today</div>',
        unsafe_allow_html=True
    )

    with st.expander("DBMS Interview Questions"):
        st.write("Discussion about DBMS concepts.")

    with st.expander("AI Project Planning"):
        st.write("Frontend and backend architecture discussion.")

    st.markdown(
        '<div class="section-title">Yesterday</div>',
        unsafe_allow_html=True
    )

    with st.expander("C++ Inheritance"):
        st.write("Inheritance concepts and examples.")

    with st.expander("SQL Basics"):
        st.write("Introduction to SQL queries.")

    st.markdown(
        '<div class="section-title">Last Week</div>',
        unsafe_allow_html=True
    )

    with st.expander("Resume Review"):
        st.write("Resume optimization discussion.")

    with st.expander("AMCAT Preparation"):
        st.write("Aptitude and placement preparation.")