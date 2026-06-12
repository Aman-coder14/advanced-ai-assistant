import streamlit as st


def show_research():

    st.markdown(
        '<div class="page-title">🔍 Research Assistant</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Research Topic",
        placeholder="Enter topic..."
    )

    if st.button("🚀 Start Research"):

        st.success(
            "Demo research generated successfully."
        )

        st.markdown("## Summary")

        st.info("""
        Artificial Intelligence continues to transform
        industries including software development,
        healthcare, finance, and education.
        """)

        st.markdown("## Analysis")

        st.write("""
        AI adoption is growing rapidly.
        Companies increasingly automate repetitive
        tasks while requiring engineers with AI skills.
        """)

        st.markdown("## Sources")

        st.write("- Source 1")
        st.write("- Source 2")
        st.write("- Source 3")

    else:

        st.info(
            "Enter a topic and click Start Research."
        )