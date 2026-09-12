import os
import streamlit as st
from PIL import Image

from modules.image_ai import analyze_image


def show_image_chat():

    st.markdown(
        """
        <div class="page-title">🖼️ Image Chat</div>
        <div class="page-subtitle">Upload an image and ask AI to analyze it.</div>
        """,
        unsafe_allow_html=True,
    )

    upload_dir = "uploads/images"
    os.makedirs(upload_dir, exist_ok=True)

    uploaded_file = st.file_uploader(
        "Drop an image here or click to browse",
        type=["png", "jpg", "jpeg", "webp"],
    )

    if uploaded_file is not None:

        image_path = os.path.join(upload_dir, uploaded_file.name)

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        image = Image.open(image_path)

        st.image(
            image,
            caption=uploaded_file.name,
            use_container_width=True,
        )

        question = st.text_input(
            "Your question about the image",
            placeholder="Describe what you see, ask for details...",
        )

        if st.button("🔍 Analyze Image", use_container_width=False):

            if not question.strip():
                st.warning("Please enter a question.")
                return

            with st.spinner("Analyzing image..."):

                try:
                    answer = analyze_image(
                        image_path,
                        question,
                    )

                    st.success("Analysis Complete")

                    st.markdown(
                        f"""
                        <div class="answer-card">
                            <div class="answer-label">✦ Image Analysis Result</div>
                            <div class="answer-content"><strong>Q:</strong> {question}<br><br>{answer}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                except Exception as e:
                    st.error(f"Error: {e}")