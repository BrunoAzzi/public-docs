import streamlit as st
from utils.ai import generate_foreground, generate_background, generate_assets, position
from utils.file import save_file
from utils.image import remove_background, trim_background, render_image
from sidebar import sidebar
from utils.session_state import get_user_ai_key

embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 8000 

sidebar()

user_ai_key = get_user_ai_key()

uploaded_background = st.file_uploader("background", type=("png"))
uploaded_assets = st.file_uploader("Assets", type=("png", "jpeg", "jpg"), accept_multiple_files=True)
additional_prompt = st.text_area("Additional instructions", "Please make the logo as wide as possible, leaving some padding so it doesn't touch the edges.")
posters_examples = st.file_uploader("Examples", type=("png", "jpeg", "jpg"), accept_multiple_files=True)

submit = st.button("Generate Poster")

if submit:
    assetList = []
    if uploaded_assets:
        for uploaded_file in uploaded_assets:
            path = save_file(uploaded_file)
            trim_background(path)
            assetList.append(path)

    example_poster_images_list = []
    if posters_examples:
        for poster in posters_examples:
            path = save_file(poster)
            example_poster_images_list.append(path)

    background = save_file(uploaded_background)

    foreground_path = remove_background(background)

    response_background = generate_background(user_ai_key, background)
    response_foreground = generate_foreground(user_ai_key, foreground_path)
    response_assets = generate_assets(user_ai_key, assetList)

    assets_descriptions = '''
{response_background}

{response_foreground}

{response_assets}
    '''.format(response_background=response_background, response_foreground=response_foreground, response_assets=response_assets)
            
    response = position(user_ai_key, assets_descriptions, example_poster_images_list, additional_prompt)

    render_image(response)

    

    




