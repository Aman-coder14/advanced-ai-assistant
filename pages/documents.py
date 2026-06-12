import streamlit as st
from components.cards import document_card


def show_documents():

    st.markdown(
        '<div class="page-title">📄 Documents</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:
        st.success(
            f"{uploaded_file.name} uploaded successfully (Demo)"
        )

    st.markdown(
        '<div class="section-title">Uploaded Documents</div>',
        unsafe_allow_html=True
    )

    document_card(
        "DBMS Notes.pdf",
        "2.3 MB",
        "12 June 2026"
    )

    document_card(
        "Resume.pdf",
        "350 KB",
        "10 June 2026"
    )

    document_card(
        "OOP Notes.docx",
        "1.1 MB",
        "8 June 2026"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.button("👁 View Selected")

    with col2:
        st.button("🗑 Delete Selected")