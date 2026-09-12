import streamlit as st


def load_css():
    # ── 1. Global CSS ─────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* ============================================================
       GOOGLE FONTS
       ============================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ============================================================
       ROOT VARIABLES
       ============================================================ */
    :root {
        --bg-base:       #060A12;
        --bg-surface:    #0C1220;
        --bg-surface2:   #111827;
        --bg-surface3:   #1A2540;
        --bg-glass:      rgba(15, 22, 40, 0.70);
        --bg-glass2:     rgba(17, 24, 39, 0.65);
        --border:        #1E2D47;
        --border-bright: #2A3F66;
        --border-glow:   rgba(99,102,241,0.45);
        --accent:        #6366F1;
        --accent-2:      #8B5CF6;
        --accent-3:      #A78BFA;
        --accent-glow:   rgba(99,102,241,0.22);
        --accent-glow2:  rgba(99,102,241,0.45);
        --text-primary:  #F1F5F9;
        --text-secondary:#94A3B8;
        --text-muted:    #64748B;
        --success:       #10B981;
        --warning:       #F59E0B;
        --error:         #EF4444;
        --radius-sm:     8px;
        --radius-md:     12px;
        --radius-lg:     16px;
        --radius-xl:     22px;
        --radius-2xl:    28px;
        --transition-fast: 0.18s cubic-bezier(0.4,0,0.2,1);
        --transition-med:  0.30s cubic-bezier(0.4,0,0.2,1);
        --transition-slow: 0.50s cubic-bezier(0.4,0,0.2,1);
    }

    /* ============================================================
       BASE RESET & TYPOGRAPHY
       ============================================================ */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ============================================================
       MAIN APP BACKGROUND
       ============================================================ */
    .stApp {
        background: var(--bg-base) !important;
        background-image:
            radial-gradient(ellipse 90% 55% at 50% -15%, rgba(99,102,241,0.14) 0%, transparent 65%),
            radial-gradient(ellipse 60% 45% at 85% 85%, rgba(139,92,246,0.09) 0%, transparent 55%),
            radial-gradient(ellipse 50% 40% at 10% 70%, rgba(99,102,241,0.06) 0%, transparent 50%) !important;
        color: var(--text-primary) !important;
    }

    /* Ensure main content sits ABOVE the canvas */
    .main .block-container {
        position: relative;
        z-index: 2;
    }

    /* Hide default streamlit decoration */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Scrollbar ──────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-surface); }
    ::-webkit-scrollbar-thumb {
        background: var(--border-bright);
        border-radius: 99px;
        transition: background var(--transition-fast);
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ============================================================
       GLOBAL ANIMATIONS
       ============================================================ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.96); }
        to   { opacity: 1; transform: scale(1); }
    }

    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 18px rgba(99,102,241,0.2), 0 0 36px rgba(99,102,241,0.08); }
        50%       { box-shadow: 0 0 28px rgba(99,102,241,0.38), 0 0 60px rgba(139,92,246,0.18); }
    }

    @keyframes borderGlow {
        0%, 100% { border-color: var(--border-bright); }
        50%       { border-color: var(--accent-3); }
    }

    @keyframes floatBob {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-5px); }
    }

    @keyframes pulse-border {
        0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
        70%  { box-shadow: 0 0 0 10px rgba(239,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
    }

    @keyframes pulse-glow {
        0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); }
        70%  { box-shadow: 0 0 0 12px rgba(16,185,129,0); }
        100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
    }

    @keyframes wave-animation {
        0%, 100% { height: 4px; }
        50%       { height: 18px; }
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ============================================================
       SIDEBAR — Glassmorphism
       ============================================================ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(10,16,32,0.97) 0%,
            rgba(12,20,40,0.95) 50%,
            rgba(8,12,24,0.97) 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.15) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        box-shadow: 4px 0 30px rgba(0,0,0,0.4), inset -1px 0 0 rgba(99,102,241,0.08) !important;
        position: relative !important;
        z-index: 100 !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }

    /* Sidebar radio nav items */
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-fast) !important;
        cursor: pointer !important;
        display: block !important;
        margin: 2px 0 !important;
        letter-spacing: 0.1px !important;
        border: 1px solid transparent !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(99,102,241,0.12) !important;
        color: #C4B5FD !important;
        border-color: rgba(99,102,241,0.2) !important;
        transform: translateX(3px) !important;
    }

    section[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.20) 0%, rgba(139,92,246,0.12) 100%) !important;
        color: #A5B4FC !important;
        border-color: rgba(99,102,241,0.3) !important;
        box-shadow: 0 2px 12px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    }

    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(99,102,241,0.1) !important;
        margin: 14px 0 !important;
    }

    /* Sidebar info box */
    section[data-testid="stSidebar"] .stAlert {
        background: rgba(99,102,241,0.07) !important;
        border: 1px solid rgba(99,102,241,0.18) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 12px !important;
        color: var(--text-muted) !important;
    }

    /* ============================================================
       GLOBAL BUTTONS
       ============================================================ */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        height: auto !important;
        min-height: 42px !important;
        transition: all var(--transition-fast) !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.28), inset 0 1px 0 rgba(255,255,255,0.12) !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        transition: left var(--transition-med);
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(99,102,241,0.45), 0 2px 8px rgba(0,0,0,0.3) !important;
        filter: brightness(1.08) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 10px rgba(99,102,241,0.25) !important;
    }

    /* Secondary/ghost buttons — sidebar & minor actions */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(15,22,40,0.6) !important;
        border: 1px solid var(--border-bright) !important;
        color: var(--text-secondary) !important;
        box-shadow: none !important;
        backdrop-filter: blur(8px) !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: var(--error) !important;
        color: var(--error) !important;
        background: rgba(239,68,68,0.10) !important;
        box-shadow: 0 0 14px rgba(239,68,68,0.15) !important;
        transform: translateY(-1px) !important;
    }

    /* ============================================================
       INPUTS & TEXT AREAS
       ============================================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(17,24,39,0.80) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        transition: border-color var(--transition-fast), box-shadow var(--transition-fast), background var(--transition-fast) !important;
        backdrop-filter: blur(8px) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow), 0 0 18px rgba(99,102,241,0.12) !important;
        background: rgba(17,24,39,0.95) !important;
        outline: none !important;
    }

    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stSlider > label,
    .stCheckbox > label,
    .stFileUploader > label {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 5px !important;
    }

    /* File uploader drop zone */
    .stFileUploader > div {
        background: rgba(17,24,39,0.60) !important;
        border: 2px dashed var(--border-bright) !important;
        border-radius: var(--radius-lg) !important;
        transition: all var(--transition-fast) !important;
        backdrop-filter: blur(8px) !important;
    }

    .stFileUploader > div:hover {
        border-color: var(--accent) !important;
        background: rgba(99,102,241,0.06) !important;
        box-shadow: 0 0 24px rgba(99,102,241,0.10) !important;
    }

    /* Chat input */
    .stChatInput > div {
        background: rgba(17,24,39,0.85) !important;
        border: 1px solid var(--border-bright) !important;
        border-radius: var(--radius-xl) !important;
        backdrop-filter: blur(16px) !important;
        transition: all var(--transition-fast) !important;
    }

    .stChatInput > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow), 0 0 30px rgba(99,102,241,0.14) !important;
    }

    /* ============================================================
       STREAMLIT NATIVE ALERTS
       ============================================================ */
    .stAlert {
        border-radius: var(--radius-md) !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        backdrop-filter: blur(8px) !important;
    }

    div[data-testid="stNotification"] {
        border-radius: var(--radius-md) !important;
    }

    .element-container .stAlert[data-baseweb="notification"] {
        background: rgba(16,185,129,0.10) !important;
        border-left: 3px solid var(--success) !important;
    }

    div[data-testid="stInfo"] {
        background: rgba(99,102,241,0.08) !important;
        border: 1px solid rgba(99,102,241,0.2) !important;
        border-radius: var(--radius-md) !important;
        color: #A5B4FC !important;
    }

    /* ============================================================
       EXPANDER
       ============================================================ */
    .streamlit-expanderHeader {
        background: rgba(17,24,39,0.70) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: all var(--transition-fast) !important;
        backdrop-filter: blur(8px) !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--accent) !important;
        color: var(--text-primary) !important;
        background: rgba(99,102,241,0.08) !important;
    }

    .streamlit-expanderContent {
        background: rgba(12,18,32,0.80) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: 16px !important;
        backdrop-filter: blur(8px) !important;
    }

    /* ============================================================
       SLIDER
       ============================================================ */
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
        color: var(--text-muted) !important;
    }

    /* ============================================================
       METRICS (native)
       ============================================================ */
    [data-testid="stMetric"] {
        background: rgba(17,24,39,0.70) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 16px !important;
        backdrop-filter: blur(12px) !important;
        transition: all var(--transition-fast) !important;
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--border-bright) !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.12) !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ============================================================
       DIVIDER
       ============================================================ */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
        margin: 20px 0 !important;
    }

    /* ============================================================
       CAPTION & MARKDOWN TEXT
       ============================================================ */
    .stMarkdown p, .stText {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }

    .stCaption {
        color: var(--text-muted) !important;
        font-size: 12px !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.3px !important;
    }

    /* ============================================================
       CUSTOM COMPONENT CLASSES
       ============================================================ */

    /* ── Page Title ──────────────────────────────────────────── */
    .page-title {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 30px;
        font-weight: 700;
        background: linear-gradient(135deg, #F1F5F9 0%, #A5B4FC 45%, #C4B5FD 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -0.6px;
        animation: shimmer 4s linear infinite, fadeInUp 0.5s ease both;
    }

    .page-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 30px;
        font-weight: 400;
        animation: fadeInUp 0.6s ease 0.1s both;
    }

    /* ── Section Title ───────────────────────────────────────── */
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 30px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.2px;
    }

    /* ── Metric Card ─────────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(145deg, rgba(17,24,39,0.85) 0%, rgba(15,22,36,0.75) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 22px 20px;
        text-align: center;
        transition: all var(--transition-med);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        animation: fadeInScale 0.5s ease both;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
        background-size: 200% auto;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        animation: gradientShift 3s linear infinite;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99,102,241,0.09) 0%, transparent 70%);
        pointer-events: none;
        border-radius: inherit;
    }

    .metric-card:hover {
        transform: translateY(-6px) scale(1.01);
        border-color: rgba(99,102,241,0.5);
        box-shadow:
            0 12px 40px rgba(99,102,241,0.22),
            0 4px 14px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.06);
    }

    .metric-title {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }

    .metric-value {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 34px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--text-primary) 0%, #A5B4FC 60%, #C4B5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        position: relative;
        z-index: 1;
    }

    /* ── Activity Card ───────────────────────────────────────── */
    .custom-card {
        background: linear-gradient(135deg, rgba(17,24,39,0.80) 0%, rgba(15,22,36,0.70) 100%);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-md);
        padding: 16px 20px;
        margin-bottom: 10px;
        transition: all var(--transition-fast);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        animation: fadeInUp 0.4s ease both;
    }

    .custom-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 60% 80% at 0% 50%, rgba(99,102,241,0.06) 0%, transparent 70%);
        pointer-events: none;
        border-radius: inherit;
        transition: opacity var(--transition-fast);
        opacity: 0;
    }

    .custom-card:hover {
        transform: translateX(4px);
        border-color: var(--border-bright);
        border-left-color: var(--accent-3);
        box-shadow: 0 6px 24px rgba(99,102,241,0.14), -2px 0 14px rgba(99,102,241,0.08);
    }

    .custom-card:hover::after { opacity: 1; }

    .custom-card h4 {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin: 0 0 6px 0 !important;
    }

    .custom-card p {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        color: var(--text-muted) !important;
        margin: 0 !important;
    }

    /* ── Document Card ───────────────────────────────────────── */
    .document-card {
        background: rgba(17,24,39,0.75);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 16px 20px;
        margin-bottom: 10px;
        transition: all var(--transition-fast);
        display: flex;
        align-items: center;
        gap: 14px;
        backdrop-filter: blur(12px);
    }

    .document-card:hover {
        border-color: rgba(99,102,241,0.45);
        box-shadow: 0 6px 24px rgba(99,102,241,0.14);
        transform: translateY(-2px);
    }

    .document-icon {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, rgba(99,102,241,0.22) 0%, rgba(139,92,246,0.18) 100%);
        border-radius: var(--radius-sm);
        border: 1px solid rgba(99,102,241,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        transition: all var(--transition-fast);
    }

    .document-card:hover .document-icon {
        background: linear-gradient(135deg, rgba(99,102,241,0.35) 0%, rgba(139,92,246,0.28) 100%);
        box-shadow: 0 0 16px rgba(99,102,241,0.25);
    }

    .document-info { flex: 1; }

    .document-name {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 5px 0;
    }

    .document-meta {
        display: flex;
        gap: 10px;
    }

    .doc-badge {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: var(--text-muted);
        background: rgba(26,37,64,0.8);
        padding: 3px 9px;
        border-radius: 99px;
        border: 1px solid var(--border);
    }

    /* ── Profile Card ────────────────────────────────────────── */
    .profile-card {
        background: linear-gradient(145deg, rgba(17,24,39,0.85) 0%, rgba(15,22,36,0.75) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 36px 28px;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all var(--transition-med);
    }

    .profile-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse 90% 55% at 50% 0%, rgba(99,102,241,0.14) 0%, transparent 70%);
        pointer-events: none;
    }

    .profile-card:hover {
        border-color: rgba(99,102,241,0.3);
        box-shadow: 0 10px 40px rgba(99,102,241,0.16);
    }

    .profile-avatar {
        width: 76px;
        height: 76px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 700;
        margin: 0 auto 16px auto;
        box-shadow: 0 8px 32px rgba(99,102,241,0.40), 0 0 0 3px rgba(99,102,241,0.15);
        transition: all var(--transition-fast);
    }

    .profile-card:hover .profile-avatar {
        box-shadow: 0 12px 44px rgba(99,102,241,0.55), 0 0 0 4px rgba(99,102,241,0.25);
        transform: scale(1.04);
    }

    .profile-name {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 5px 0;
    }

    .profile-email {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }

    /* ── Auth Card ───────────────────────────────────────────── */
    .auth-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 0 16px;
    }

    .auth-card {
        background: linear-gradient(145deg, rgba(17,24,39,0.92) 0%, rgba(12,18,32,0.88) 100%);
        border: 1px solid rgba(99,102,241,0.20);
        border-radius: var(--radius-xl);
        padding: 40px 36px;
        box-shadow:
            0 24px 70px rgba(0,0,0,0.50),
            0 0 0 1px rgba(255,255,255,0.04),
            inset 0 1px 0 rgba(255,255,255,0.06);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        animation: fadeInScale 0.6s cubic-bezier(0.34,1.56,0.64,1) both;
    }

    .auth-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse 110% 65% at 50% 0%, rgba(99,102,241,0.10) 0%, transparent 70%);
        pointer-events: none;
    }

    .auth-card::after {
        content: '';
        position: absolute;
        top: 0; left: -60%; width: 40%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
        transform: skewX(-15deg);
        transition: left 0.7s ease;
    }

    .auth-card:hover::after {
        left: 130%;
    }

    .auth-logo {
        text-align: center;
        margin-bottom: 10px;
        font-size: 32px;
        animation: floatBob 3s ease-in-out infinite;
        display: block;
    }

    .auth-title {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #F1F5F9 0%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 0 0 7px 0;
        letter-spacing: -0.5px;
    }

    .auth-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        text-align: center;
        margin-bottom: 30px;
    }

    /* ── Sidebar Brand ───────────────────────────────────────── */
    .sidebar-brand {
        padding: 22px 18px 16px 18px;
        border-bottom: 1px solid rgba(99,102,241,0.12);
        margin-bottom: 10px;
        position: relative;
    }

    .sidebar-brand::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 18px; right: 18px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.35), transparent);
    }

    .sidebar-brand-logo {
        font-size: 20px;
        font-weight: 800;
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        background: linear-gradient(135deg, #A5B4FC 0%, #C4B5FD 60%, #DDD6FE 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        animation: gradientShift 4s ease infinite;
    }

    .sidebar-brand-tagline {
        font-size: 11px;
        color: var(--text-muted);
        font-family: 'Inter', sans-serif;
        margin-top: 3px;
        letter-spacing: 0.3px;
    }

    /* ── Quick Action Buttons ────────────────────────────────── */
    .quick-action-card {
        background: rgba(17,24,39,0.70);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 22px 16px;
        text-align: center;
        transition: all var(--transition-fast);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
    }

    .quick-action-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(99,102,241,0.10) 0%, rgba(139,92,246,0.06) 100%);
        opacity: 0;
        transition: opacity var(--transition-fast);
        border-radius: inherit;
    }

    .quick-action-card:hover {
        border-color: rgba(99,102,241,0.45);
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 10px 30px rgba(99,102,241,0.20);
    }

    .quick-action-card:hover::after { opacity: 1; }

    .quick-action-icon {
        font-size: 28px;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
    }

    .quick-action-label {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: var(--text-secondary);
        position: relative;
        z-index: 1;
    }

    /* ── Chat Message Bubbles ────────────────────────────────── */
    .chat-msg-user {
        background: linear-gradient(135deg, rgba(99,102,241,0.20) 0%, rgba(139,92,246,0.14) 100%);
        border: 1px solid rgba(99,102,241,0.32);
        border-radius: 16px 16px 4px 16px;
        padding: 14px 18px;
        margin: 10px 0 10px 60px;
        position: relative;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(99,102,241,0.12);
        transition: all var(--transition-fast);
        animation: fadeInUp 0.3s ease both;
    }

    .chat-msg-user:hover {
        border-color: rgba(99,102,241,0.50);
        box-shadow: 0 6px 28px rgba(99,102,241,0.20);
    }

    .chat-msg-ai {
        background: linear-gradient(135deg, rgba(17,24,39,0.85) 0%, rgba(15,22,36,0.75) 100%);
        border: 1px solid var(--border);
        border-radius: 16px 16px 16px 4px;
        padding: 14px 18px;
        margin: 10px 60px 10px 0;
        position: relative;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all var(--transition-fast);
        animation: fadeInUp 0.3s ease both;
    }

    .chat-msg-ai:hover {
        border-color: var(--border-bright);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    .chat-msg-label {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        margin-bottom: 8px;
    }

    .chat-msg-user .chat-msg-label { color: #A5B4FC; }
    .chat-msg-ai  .chat-msg-label  { color: var(--text-muted); }

    .chat-msg-content {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-primary);
        white-space: pre-wrap;
        line-height: 1.70;
    }

    /* ── Answer / Result Card ────────────────────────────────── */
    .answer-card {
        background: rgba(17,24,39,0.80);
        border: 1px solid var(--border);
        border-left: 3px solid var(--success);
        border-radius: var(--radius-md);
        padding: 18px 20px;
        margin-top: 12px;
        backdrop-filter: blur(12px);
        transition: all var(--transition-fast);
    }

    .answer-card:hover {
        box-shadow: 0 4px 20px rgba(16,185,129,0.12);
    }

    .answer-label {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--success);
        margin-bottom: 8px;
    }

    .answer-content {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-primary);
        line-height: 1.70;
    }

    /* ── Result section cards (Research) ─────────────────────── */
    .result-section {
        background: rgba(17,24,39,0.75);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 18px 20px;
        margin-bottom: 14px;
        backdrop-filter: blur(12px);
        transition: all var(--transition-fast);
    }

    .result-section:hover {
        border-color: var(--border-bright);
        box-shadow: 0 4px 20px rgba(99,102,241,0.10);
    }

    .result-section-title {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 700;
        color: var(--accent-3);
        margin-bottom: 10px;
    }

    .result-section-content {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.70;
    }

    /* ── Empty State ─────────────────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 50px 20px;
        color: var(--text-muted);
        font-family: 'Inter', sans-serif;
        animation: fadeInUp 0.5s ease both;
    }

    .empty-state-icon {
        font-size: 44px;
        margin-bottom: 16px;
        opacity: 0.45;
        display: block;
        animation: floatBob 3.5s ease-in-out infinite;
    }

    .empty-state-text {
        font-size: 14px;
        color: var(--text-muted);
    }

    /* ── Settings Section ────────────────────────────────────── */
    .settings-section {
        background: rgba(17,24,39,0.75);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 22px 24px;
        margin-bottom: 16px;
        backdrop-filter: blur(12px);
        transition: all var(--transition-fast);
    }

    .settings-section:hover {
        border-color: var(--border-bright);
    }

    .settings-section-title {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-muted);
        margin-bottom: 18px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }

    /* ==========================================================
       VOICE CHAT SPECIFIC STYLES
       ========================================================== */

    .voice-header-card {
        background: linear-gradient(135deg, rgba(17,24,39,0.85) 0%, rgba(26,37,64,0.75) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 16px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        backdrop-filter: blur(16px);
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
        font-family: 'Inter', sans-serif;
    }

    .status-idle {
        background: rgba(100,116,139,0.15);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }

    .status-listening {
        background: rgba(239,68,68,0.20);
        color: #EF4444;
        border: 1px solid #EF4444;
        animation: pulse-border 1.5s infinite;
    }

    .status-processing {
        background: rgba(245,158,11,0.20);
        color: #F59E0B;
        border: 1px solid #F59E0B;
    }

    .status-speaking {
        background: rgba(16,185,129,0.20);
        color: #10B981;
        border: 1px solid #10B981;
        animation: pulse-glow 1.5s infinite;
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

    .voice-console-card {
        background: rgba(17,24,39,0.80);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 24px;
        margin-top: 15px;
        text-align: center;
        backdrop-filter: blur(16px);
    }

    /* ============================================================
       CHECKBOX & RADIO
       ============================================================ */
    .stCheckbox > label,
    .stRadio > label {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }

    /* ============================================================
       SPINNER
       ============================================================ */
    .stSpinner > div {
        border-top-color: var(--accent) !important;
    }

    /* ============================================================
       PARTICLE CANVAS — sits behind everything
       ============================================================ */
    #star-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
        display: block;
    }

    </style>
    """, unsafe_allow_html=True)

    # ── 2. Particle Canvas HTML + JS ──────────────────────────────────────────
    st.markdown("""
    <canvas id="star-canvas"></canvas>

    <script>
    (function() {
        // Respect reduced-motion preference
        const prefersReduced = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const canvas = document.getElementById('star-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        // ── Config ────────────────────────────────────────────────
        const CFG = {
            COUNT:        160,
            CONNECT_DIST: 130,
            REPEL_DIST:   110,
            REPEL_FORCE:  0.012,
            RETURN_FORCE: 0.025,
            MAX_SPEED:    0.45,
            DRIFT_SPEED:  0.006,
            LINE_OPACITY: 0.18,
        };

        let W, H, stars = [];
        let mouse = { x: -9999, y: -9999 };
        let animId;

        // ── Resize ────────────────────────────────────────────────
        function resize() {
            W = canvas.width  = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize, { passive: true });
        resize();

        // ── Star factory ─────────────────────────────────────────
        function mkStar() {
            const r = Math.random() * 1.6 + 0.3;
            const bright = 0.3 + Math.random() * 0.7;
            return {
                x:   Math.random() * W,
                y:   Math.random() * H,
                ox:  0, oy: 0,          // will be set below
                vx:  (Math.random() - 0.5) * 0.25,
                vy:  (Math.random() - 0.5) * 0.25,
                dvx: 0, dvy: 0,         // displacement velocity (repulsion)
                r:   r,
                baseR: r,
                bright: bright,
                phase: Math.random() * Math.PI * 2,
                speed: 0.003 + Math.random() * CFG.DRIFT_SPEED,
                hue:  Math.random() < 0.85 ? 220 + Math.random()*40 : 260 + Math.random()*30,
            };
        }

        function initStars() {
            stars = [];
            for (let i = 0; i < CFG.COUNT; i++) {
                const s = mkStar();
                s.ox = s.x;
                s.oy = s.y;
                stars.push(s);
            }
        }
        initStars();

        // ── Mouse tracking ────────────────────────────────────────
        window.addEventListener('mousemove', function(e) {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        }, { passive: true });
        window.addEventListener('mouseleave', function() {
            mouse.x = -9999;
            mouse.y = -9999;
        }, { passive: true });

        // ── Draw connecting lines ─────────────────────────────────
        function drawLines() {
            for (let i = 0; i < stars.length; i++) {
                const a = stars[i];
                for (let j = i + 1; j < stars.length; j++) {
                    const b = stars[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist > CFG.CONNECT_DIST) continue;
                    const alpha = CFG.LINE_OPACITY * (1 - dist / CFG.CONNECT_DIST);
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(140, 150, 255, ${alpha})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.stroke();
                }
            }
        }

        // ── Main render loop ──────────────────────────────────────
        function tick(now) {
            animId = requestAnimationFrame(tick);
            ctx.clearRect(0, 0, W, H);

            for (let i = 0; i < stars.length; i++) {
                const s = stars[i];

                // Natural sinusoidal drift
                s.phase += s.speed;
                s.ox = s.x;
                s.oy = s.y;

                // Cursor repulsion
                const mdx = s.x - mouse.x;
                const mdy = s.y - mouse.y;
                const mdist = Math.sqrt(mdx*mdx + mdy*mdy);

                if (mdist < CFG.REPEL_DIST && mdist > 0) {
                    const force = (CFG.REPEL_DIST - mdist) / CFG.REPEL_DIST;
                    const angle = Math.atan2(mdy, mdx);
                    s.dvx += Math.cos(angle) * force * CFG.REPEL_FORCE * (W / 1400);
                    s.dvy += Math.sin(angle) * force * CFG.REPEL_FORCE * (H / 900);
                    // Brighten on hover
                    s.r = Math.min(s.baseR * (1 + force * 1.8), s.baseR * 2.8);
                } else {
                    s.r += (s.baseR - s.r) * 0.08;
                }

                // Return displacement toward zero (spring)
                s.dvx *= (1 - CFG.RETURN_FORCE);
                s.dvy *= (1 - CFG.RETURN_FORCE);

                // Clamp displacement velocity
                const dspeed = Math.sqrt(s.dvx*s.dvx + s.dvy*s.dvy);
                if (dspeed > CFG.MAX_SPEED) {
                    s.dvx = (s.dvx / dspeed) * CFG.MAX_SPEED;
                    s.dvy = (s.dvy / dspeed) * CFG.MAX_SPEED;
                }

                // Natural drift velocity
                s.vx += (Math.random() - 0.5) * 0.004;
                s.vy += (Math.random() - 0.5) * 0.004;
                s.vx *= 0.98;
                s.vy *= 0.98;

                // Apply velocities
                s.x += s.vx + s.dvx;
                s.y += s.vy + s.dvy;

                // Wrap at edges
                if (s.x < -10)    s.x = W + 10;
                if (s.x > W + 10) s.x = -10;
                if (s.y < -10)    s.y = H + 10;
                if (s.y > H + 10) s.y = -10;

                // ── Draw star ────────────────────────────────────
                const alpha = s.bright * (0.65 + 0.35 * Math.sin(s.phase));
                const grd = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 3.5);
                grd.addColorStop(0,   `hsla(${s.hue}, 80%, 82%, ${alpha})`);
                grd.addColorStop(0.4, `hsla(${s.hue}, 70%, 70%, ${alpha * 0.55})`);
                grd.addColorStop(1,   `hsla(${s.hue}, 60%, 60%, 0)`);

                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r * 3.5, 0, Math.PI * 2);
                ctx.fillStyle = grd;
                ctx.fill();

                // Solid center dot
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${s.hue}, 90%, 92%, ${alpha})`;
                ctx.fill();
            }

            // Draw connecting lines after stars
            drawLines();
        }

        if (prefersReduced) {
            // Static render for reduced-motion users — just draw once
            for (let i = 0; i < stars.length; i++) {
                const s = stars[i];
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${s.hue}, 80%, 85%, ${s.bright * 0.5})`;
                ctx.fill();
            }
        } else {
            tick(0);
        }

        // ── Re-init on resize to redistribute stars ───────────────
        window.addEventListener('resize', function() {
            resize();
            initStars();
        }, { passive: true });

    })();
    </script>
    """, unsafe_allow_html=True)