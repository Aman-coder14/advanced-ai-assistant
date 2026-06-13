import streamlit as st

from modules.llm import generate_response


def show_chat():

    st.markdown(
        '<div class="page-title">💬 AI Chat</div>',
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello Aman 👋 How can I help you today?"
            }
        ]

    left, right = st.columns([1, 4])

    with left:

        st.subheader("Chats")

        st.button("➕ New Chat")

        st.button("✏ Rename")

        st.button("🗑 Delete")

        st.divider()

        st.write("Chat 1")
        st.write("Chat 2")
        st.write("Chat 3")

    with right:

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input(
            "Type your message..."
        )

        if prompt:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            try:
                # If PDF text is present in session state, include it as context
                context_text = st.session_state.get("uploaded_pdf_text", "")
                if context_text:
                    truncated = context_text[:10000]
                    composed_prompt = (
                        "You are answering based on the uploaded PDF.\n\n"
                        f"PDF Content:\n{truncated}\n\n"
                        f"Question:\n{prompt}\n\n"
                        "Answer only from the PDF content.\n"
                        "If the answer is not present, say:\n"
                        '"The answer was not found in the uploaded document."'
                    )
                else:
                    composed_prompt = prompt

                with st.spinner("Thinking..."):
                    assistant_response = generate_response(composed_prompt)

                # Add source indication when PDF context was used
                if context_text:
                    assistant_response = f"{assistant_response}\n\nAnswer generated from uploaded PDF"
            except Exception as exc:
                assistant_response = (
                    "I'm sorry, I couldn't generate a response right now. "
                    "Please try again in a moment."
                )
                st.error(f"AI service error: {exc}")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )

            st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            st.button("📋 Copy Last Response")

        with col2:
            if st.button("🧹 Clear Chat"):
                st.session_state.messages = []
                st.rerun()