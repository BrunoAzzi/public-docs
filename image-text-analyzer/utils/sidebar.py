import streamlit as st
from utils.session_state import save_open_ai_key, get_user_ai_key

user_ai_key = get_user_ai_key()

def sidebar():
    with st.sidebar:
        open_ai_api_key = st.text_input('OpenAI API Key', key="file_qa_api_key", value=user_ai_key)
        if st.button("Save"):
            save_open_ai_key(open_ai_api_key)
            st.rerun()