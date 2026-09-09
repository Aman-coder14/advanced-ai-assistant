import os
import streamlit as st
from PIL import Image

from modules.image_ai import analyze_image


def show_image_chat():
    st.title("🖼️ Image Chat")

    upload_dir = "uploads/images"
    os.makedirs(upload_dir, exist_ok=True)

    uploaded_file = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:

        image_path = os.path.join(upload_dir, uploaded_file.name)

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        image = Image.open(image_path)

        st.image(
            image,
            caption=uploaded_file.name,
            use_container_width=True
        )

        question = st.text_input(
            "Ask about this image"
        )

        if st.button("Analyze Image"):

            if not question.strip():
                st.warning("Please enter a question.")
                return

            with st.spinner("Analyzing image..."):

                try:
                    answer = analyze_image(
                        image_path,
                        question
                    )

                    st.success("Analysis Complete")

                    st.markdown("### Answer")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")