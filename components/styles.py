import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Main App */
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }

    /* Cards */
    .custom-card {
        background: #161B22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363D;
        margin-bottom: 15px;
        transition: 0.3s;
    }

    .custom-card:hover {
        transform: translateY(-3px);
        border-color: #58A6FF;
    }

    /* Metric Cards */
    .metric-card {
        background: #161B22;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #30363D;
    }

    .metric-title {
        font-size: 16px;
        color: #8B949E;
    }

    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: white;
    }

    /* Titles */
    .page-title {
        font-size: 32px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Chat Messages */
    .user-msg {
        background: #238636;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        color: white;
    }

    .bot-msg {
        background: #21262D;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        color: white;
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
    }

    /* Inputs */
    .stTextInput input {
        border-radius: 10px;
    }

    /* Profile */
    .profile-card {
        background: #161B22;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #30363D;
    }

    </style>
    """, unsafe_allow_html=True)