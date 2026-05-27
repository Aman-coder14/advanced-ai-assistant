import streamlit as st

from chatbot.image_ai import open_image

st.title("🖼 Image Chat")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    image = open_image(uploaded_file)

    st.image(image)