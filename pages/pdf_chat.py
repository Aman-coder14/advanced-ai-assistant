import streamlit as st

from chatbot.pdf_chat import read_pdf

st.title("📄 PDF Chat")

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_pdf:

    text = read_pdf(uploaded_pdf)

    st.write(text[:3000])