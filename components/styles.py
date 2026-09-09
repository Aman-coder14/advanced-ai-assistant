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

    /* ==========================================================
       VOICE CHAT SPECIFIC STYLES (ChatGPT / Gemini Live Style)
       ========================================================== */

    .voice-header-card {
        background: linear-gradient(135deg, #161B22 0%, #1F2937 100%);
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .voice-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    .status-idle {
        background: rgba(139, 148, 158, 0.15);
        color: #8B949E;
        border: 1px solid #30363D;
    }

    .status-listening {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
        animation: pulse-border 1.5s infinite;
    }

    .status-processing {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid #F59E0B;
    }

    .status-speaking {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
        animation: pulse-glow 1.5s infinite;
    }

    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Sound wave bar animations */
    .sound-wave {
        display: flex;
        align-items: center;
        gap: 3px;
        height: 20px;
    }

    .sound-wave span {
        display: block;
        width: 3px;
        height: 100%;
        background-color: currentColor;
        border-radius: 3px;
        animation: wave-animation 1.2s infinite ease-in-out;
    }

    .sound-wave span:nth-child(1) { animation-delay: 0.0s; }
    .sound-wave span:nth-child(2) { animation-delay: 0.2s; }
    .sound-wave span:nth-child(3) { animation-delay: 0.4s; }
    .sound-wave span:nth-child(4) { animation-delay: 0.6s; }

    @keyframes wave-animation {
        0%, 100% { height: 4px; }
        50% { height: 18px; }
    }

    .voice-console-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 20px;
        padding: 24px;
        margin-top: 15px;
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)