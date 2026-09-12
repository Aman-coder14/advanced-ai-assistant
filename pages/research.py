import streamlit as st


def show_research():

    st.markdown(
        """
        <div class="page-title">🔍 Research Assistant</div>
        <div class="page-subtitle">Enter any topic and get an AI-generated research overview.</div>
        """,
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Research topic",
        placeholder="e.g. AI in Healthcare, Quantum Computing, Climate Change...",
    )

    if st.button("🚀 Start Research", use_container_width=False):

        st.success("Research generated successfully.")

        st.markdown(
            """
            <div class="result-section">
                <div class="result-section-title">📋 Summary</div>
                <div class="result-section-content">
                    Artificial Intelligence continues to transform industries including software development,
                    healthcare, finance, and education.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="result-section">
                <div class="result-section-title">📊 Analysis</div>
                <div class="result-section-content">
                    AI adoption is growing rapidly. Companies increasingly automate repetitive
                    tasks while requiring engineers with AI skills.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="result-section">
                <div class="result-section-title">🔗 Sources</div>
                <div class="result-section-content">
                    · Source 1<br>· Source 2<br>· Source 3
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-text">Enter a topic above and click <strong>Start Research</strong> to generate an AI-powered report.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )