import streamlit as st
from utils.ai import get_logo_positioning
from utils.file import save_file
from utils.image import remove_background, trim_background, flatten_image
from sidebar import sidebar
from utils.session_state import get_user_ai_key
from utils.logos import white_logo, black_logo

embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 8000 

sidebar()

user_ai_key = get_user_ai_key()

uploaded_background = st.file_uploader("background", type=("png"))

submit = st.button("Generate Poster")

if submit:
    background = save_file(uploaded_background)
    background_path = trim_background(background)
    foreground_path = remove_background(background)
    
    logo_positioning = get_logo_positioning(user_ai_key, background_path)
    if logo_positioning['color'] == 'white':
        logo_base64 = white_logo()
    else:
        logo_base64 = black_logo()
    
    image = flatten_image(background_path, foreground_path, logo_base64, logo_positioning)
    
    if image is not None:
        st.image(image)
else:
    if uploaded_background:
        st.image(uploaded_background)




