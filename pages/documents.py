import streamlit as st
from components.cards import document_card
from modules.file_loader import save_uploaded_file, extract_pdf_text
from modules.llm import generate_response
from datetime import datetime


def show_documents():

    st.markdown(
        '<div class="page-title">📄 Documents</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if "uploaded_pdf_text" not in st.session_state:
        st.session_state.uploaded_pdf_text = ""

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                saved_path = save_uploaded_file(uploaded_file)
                st.success(f"{uploaded_file.name} uploaded successfully")

                try:
                    num_pages, full_text = extract_pdf_text(saved_path)
                    # store extracted text in session state (append)
                    header = f"\n\n---\nFile: {uploaded_file.name}\nPages: {num_pages}\n---\n"
                    st.session_state.uploaded_pdf_text += header + (full_text or "")
                    preview = full_text[:2000] + ("..." if len(full_text) > 2000 else "")

                    st.markdown(
                        f"<div class=\"section-title\">{uploaded_file.name}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"<p>Pages: {num_pages}</p>", unsafe_allow_html=True)
                    st.text_area("Preview", value=preview, height=240)
                except Exception as exc:
                    st.error(f"Failed to extract text from {uploaded_file.name}: {exc}")

            except Exception as exc:
                st.error(f"Failed to save {uploaded_file.name}: {exc}")

    # --- PDF Question Answering UI ---
    st.markdown(
        '<div class="section-title">Ask about the uploaded PDF</div>',
        unsafe_allow_html=True,
    )

    question = st.text_input("Ask a question about this PDF")
    ask_clicked = st.button("Ask")

    if ask_clicked and question:
        pdf_text = st.session_state.get("uploaded_pdf_text", "").strip()
        if not pdf_text:
            st.warning("Please upload a PDF first to ask questions about it.")
        else:
            truncated = pdf_text[:10000]
            composed_prompt = (
                "You are answering questions from an uploaded PDF.\n\n"
                f"PDF Content:\n{truncated}\n\n"
                f"Question:\n{question}\n\n"
                "Answer only using information from the PDF.\n"
                "If the answer is not found, say:\n"
                '"The answer was not found in the uploaded document."'
            )
            # First, try to answer from the uploaded PDF
            try:
                with st.spinner("Analyzing document..."):
                    pdf_answer = generate_response(composed_prompt)
            except Exception as exc:
                st.error(f"Failed while analyzing PDF: {exc}")
                pdf_answer = ""

            # If PDF explicitly reports not found, fall back to general model/search
            not_found_marker = "The answer was not found in the uploaded document."

            if pdf_answer and not_found_marker not in pdf_answer:
                answer = pdf_answer
                source = "Uploaded PDF"
            else:
                # No useful answer in PDF — use regular generate_response (which may use web search)
                try:
                    with st.spinner("Querying web and AI..."):
                        answer = generate_response(question)
                    source = "AI/Web Search"
                except Exception as exc:
                    st.error(f"Failed to get fallback answer: {exc}")
                    answer = ""
                    source = "Error"

            # store last QA with source
            st.session_state.last_pdf_qa = {"question": question, "answer": answer, "source": source}

            st.markdown(f"**Question:** {question}")
            st.markdown(f"**Answer:** {answer}")
            st.markdown(f"**Source:** {source}")

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