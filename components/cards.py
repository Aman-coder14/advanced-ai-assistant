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
    # Determine icon by extension
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else "file"
    icon_map = {"pdf": "📕", "doc": "📘", "docx": "📘", "txt": "📃", "csv": "📊", "xlsx": "📊"}
    icon = icon_map.get(ext, "📄")

    st.markdown(
        f"""
        <div class="document-card">
            <div class="document-icon">{icon}</div>
            <div class="document-info">
                <div class="document-name">{name}</div>
                <div class="document-meta">
                    <span class="doc-badge">📦 {size}</span>
                    <span class="doc-badge">📅 {date}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_card(name, email):
    initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "?"
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-avatar">{initials}</div>
            <div class="profile-name">{name}</div>
            <div class="profile-email">{email}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )