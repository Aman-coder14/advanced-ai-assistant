import streamlit as st


def show_settings():

    st.markdown(
        '<div class="page-title">⚙ Settings</div>',
        unsafe_allow_html=True
    )

    st.subheader("Appearance")

    theme = st.selectbox(
        "Theme",
        ["Dark", "Light", "System"]
    )

    st.subheader("AI Model")

    model = st.selectbox(
        "Model",
        [
            "Llama 4",
            "DeepSeek",
            "GPT",
            "Custom"
        ]
    )

    st.subheader("Temperature")

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.subheader("Notifications")

    email_notifications = st.checkbox(
        "Email Notifications",
        value=True
    )

    app_notifications = st.checkbox(
        "In-App Notifications",
        value=True
    )

    if st.button("💾 Save Settings"):
        st.success(
            "Settings saved successfully (Demo)"
        )