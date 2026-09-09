import streamlit as st
from components.cards import document_card
from modules.file_loader import save_uploaded_file, extract_pdf_text
from modules.llm import generate_response
from modules import chunker
from modules import embeddings
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

                    # Chunk the extracted text and create embeddings for RAG
                    try:
                        chunks = chunker.chunk_text(full_text or "")
                        if chunks:
                            embeddings.create_embeddings(chunks)
                            st.info(f"Indexed {len(chunks)} chunks for RAG retrieval.")
                    except Exception as exc:
                        st.error(f"Failed to create embeddings for RAG: {exc}")

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

        # Try RAG retrieval from FAISS first if index exists
        try:
            index = embeddings.load_faiss_index()
        except Exception as exc:
            st.error(f"Failed to load RAG index: {exc}")
            index = None

        if index is not None:
            try:
                with st.spinner("Retrieving relevant chunks from document..."):
                    results = embeddings.search_similar_chunks(question, top_k=5)
            except Exception as exc:
                st.error(f"RAG retrieval failed: {exc}")
                results = []

            if results:
                # determine relevance by top score
                top_score = max(r.get("score", 0.0) for r in results)
                # threshold for relevance (cosine-like). Tunable.
                if top_score > 0.2:
                    retrieved_count = len(results)
                    retrieved_text = "\n\n".join([r.get("text", "") for r in results])
                    truncated = retrieved_text[:10000]
                    composed_prompt = (
                        "You are answering questions from retrieved PDF chunks.\n\n"
                        f"Retrieved Chunks:\n{truncated}\n\n"
                        f"Question:\n{question}\n\n"
                        "Answer only using information from the retrieved chunks.\n"
                        "If the answer is not found, say:\n"
                        '"The answer was not found in the uploaded document."'
                    )
                    try:
                        with st.spinner("Analyzing retrieved chunks..."):
                            answer = generate_response(composed_prompt)
                    except Exception as exc:
                        st.error(f"Failed to generate answer from chunks: {exc}")
                        answer = ""

                    st.session_state.last_pdf_qa = {"question": question, "answer": answer, "source": "Uploaded PDF (RAG)", "retrieved_count": retrieved_count}

                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Answer:** {answer}")
                    st.markdown(f"**Retrieved Chunks Count:** {retrieved_count}")
                    st.markdown("**Source:** Uploaded PDF (RAG)")
                    return

        # If RAG did not return a confident answer, fall back to full PDF text or web
        if pdf_text:
            truncated = pdf_text[:10000]
            composed_prompt = (
                "You are answering questions from an uploaded PDF.\n\n"
                f"PDF Content:\n{truncated}\n\n"
                f"Question:\n{question}\n\n"
                "Answer only using information from the PDF.\n"
                "If the answer is not found, say:\n"
                '"The answer was not found in the uploaded document."'
            )
            try:
                with st.spinner("Analyzing document..."):
                    pdf_answer = generate_response(composed_prompt)
            except Exception as exc:
                st.error(f"Failed while analyzing PDF: {exc}")
                pdf_answer = ""

            not_found_marker = "The answer was not found in the uploaded document."
            if pdf_answer and not_found_marker not in pdf_answer:
                answer = pdf_answer
                source = "Uploaded PDF"
            else:
                try:
                    with st.spinner("Querying web and AI..."):
                        answer = generate_response(question)
                    source = "AI/Web Search"
                except Exception as exc:
                    st.error(f"Failed to get fallback answer: {exc}")
                    answer = ""
                    source = "Error"

        else:
            # no pdf text — just query web/AI
            try:
                with st.spinner("Querying web and AI..."):
                    answer = generate_response(question)
                source = "AI/Web Search"
            except Exception as exc:
                st.error(f"Failed to get answer: {exc}")
                answer = ""
                source = "Error"

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