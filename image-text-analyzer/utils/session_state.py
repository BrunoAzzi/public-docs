import streamlit as st

if 'key' not in st.session_state:
    st.session_state.key = ''

def save_open_ai_key(key: str):
    st.session_state.key = key

def get_user_ai_key(): 
    if 'key' not in st.session_state:
        st.session_state.key = ''
        
    return st.session_state.key