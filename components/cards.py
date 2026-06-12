import streamlit as st


def metric_card(title, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def activity_card(title, description):
    st.markdown(
        f"""
        <div class="custom-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def document_card(name, size, date):
    st.markdown(
        f"""
        <div class="custom-card">
            <h4>📄 {name}</h4>
            <p>Size: {size}</p>
            <p>Uploaded: {date}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_card(name, email):
    st.markdown(
        f"""
        <div class="profile-card">
            <h2>👤 {name}</h2>
            <p>{email}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )