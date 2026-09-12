import streamlit as st


def show_settings():

    st.markdown(
        """
        <div class="page-title">⚙️ Settings</div>
        <div class="page-subtitle">Customize your AI Workspace experience.</div>
        """,
        unsafe_allow_html=True,
    )

    # ── Appearance ────────────────────────────────────────────
    st.markdown(
        '<div class="settings-section-title">🎨 Appearance</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        theme = st.selectbox(
            "Theme",
            ["Dark", "Light", "System"],
        )

    # ── AI Model ──────────────────────────────────────────────
    st.markdown(
        '<div class="settings-section-title" style="margin-top:20px;">🤖 AI Model</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        model = st.selectbox(
            "Model",
            [
                "Llama 4",
                "DeepSeek",
                "GPT",
                "Custom",
            ],
        )

    # ── Temperature ───────────────────────────────────────────
    st.markdown(
        '<div class="settings-section-title" style="margin-top:20px;">🌡️ Temperature</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        temperature = st.slider(
            "Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
        )

    # ── Notifications ─────────────────────────────────────────
    st.markdown(
        '<div class="settings-section-title" style="margin-top:20px;">🔔 Notifications</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        email_notifications = st.checkbox(
            "Email Notifications",
            value=True,
        )

        app_notifications = st.checkbox(
            "In-App Notifications",
            value=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 Save Settings", use_container_width=False):
        st.success("Settings saved successfully (Demo)")