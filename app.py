# import streamlit as st
# from chatbot.llm import get_response

# st.set_page_config(page_title="My Advanced AI Chatbot")

# st.title("My Advanced AI Chatbot")

# user_input = st.text_input("Ask Something")

# if user_input:

#     response = get_response(user_input)

#     st.write(response)
import streamlit as st
from chatbot.llm import get_response

st.set_page_config(
    page_title="Advanced AI Assistant",
    layout="wide"
)

st.title("🤖 Advanced AI Assistant")

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Chatbot"]
)

# Chatbot Page
if page == "Chatbot":

    st.header("💬 AI Chat")

    user_input = st.text_input("Ask Something")

    if user_input:

        response = get_response(user_input)

        st.write("### AI Response")
        st.write(response)