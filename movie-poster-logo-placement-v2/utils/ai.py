from utils.image import base64Image
from openai import OpenAI
import streamlit as st
import json
from PIL import Image

def get_client(user_ai_key: str):
    client = OpenAI(api_key=user_ai_key)
    return client

def process_image(user_ai_key: str, image_file_path: str, prompt: str):
    client = get_client(user_ai_key) 
    image = Image.open(image_file_path)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "user",
                "content": [
                    prompt,
                    "Image width: "+str(image.width),
                    "Image height: "+str(image.height),
                    {"image": base64Image(image_file_path), "resize": 512},
                ],
            },
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def process_image_list(user_ai_key: str, image_file_path_list: list, prompt: str, system_prompt: str = None, additional_prompt = None):
    client = get_client(user_ai_key)
    content  = [
        prompt,
        *map(lambda x: {"image": base64Image(x), "resize": 512}, image_file_path_list)
    ]

    if additional_prompt:
        content.append(additional_prompt)

    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]

    if system_prompt:
        messages.insert(0, {
            "role": "system",
            "content": system_prompt
        })

    st.text(messages)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={ "type": "json_object" },
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message.content

def generate_background(user_ai_key: str, image_file_path: str):
    return process_image(user_ai_key, image_file_path, "This is the background image of a movie poster. Return a json with width and height, a 'path' property with "+image_file_path+", a description of it and a label property with the type of image (asset, background or foreground).")

def generate_foreground(user_ai_key: str, image_file_path: str):
    return process_image(user_ai_key, image_file_path, "This is the foreground image of a movie poster. Return a json with width and height, a 'path' property with "+image_file_path+", a description of it and a label property with the type of image (asset, background or foreground).")

def generate_assets(user_ai_key: str,image_file_path_list: list):
    return process_image_list(
        user_ai_key,
        image_file_path_list, 
        "Also add the path to the json. Images are ordered as following: "+ ', '.join([x for x in image_file_path_list]),
        "You are going to receive a list of asset images for a movie poster. Return a json with width and height, a description of the image and a label property with the type of image (asset, background or foreground)."
    )

def get_text(choice):
    return choice.message.content

def get_message(response):
    choices = list(response.choices)
    return ' '.join(map(get_text, choices))

def get_logo_positioning(user_ai_key: str, background_path: str):
    
    response = process_image(user_ai_key, background_path, """
            You are a very skilled and talented designer. I want you to discover the x, y coordinates to insert a logo image.
            I'm sending a movie poster, and please avoid overlapping the text with the logo. Try to center the logo image, the top usually is the best position just after people names, but remember to not overlap the text.
            Don't worry much about characters as we will paste a foreground to cover the image, but if overlapping a character, make sure the log is visible as it was behind the character.
            Please return also the best size for the logo image, original image size is 998x189. Keep the logo aspect ratio and make it as big as possible, try to make full width, just keep a margin of 10% around the logo image and the edges of the poster.
            Also send which is the best match color to be more readable, 'white' or 'black'.
            
            response in this json format:
            
            {
                x: ...,
                y: ...,
                width: ...,
                height: ...,
                color: '...'
            }
        """)
    response = json.loads(response)
    return response

def position(user_ai_key: str, assets_descriptions, example_poster_images_list, additional_prompt = None):
    return process_image_list(user_ai_key, example_poster_images_list, assets_descriptions, '''
You are a graphic designer tasked with creating an IMAX movie poster.
                              
Images attached are an example of previous IMAX posters.

Given a json representation of the background,assets, and foreground.
Consider the width and height of the background as the boundaries of the poster. The background is the first layer, the assets are the second layer, and the foreground is the third layer. 
Position and resize the assets to create an IMAX movie poster.
                              
MAKE SURE THAT THE ASSETS WIDTH AND HEIGHT ARE NEVER OUTSIDE OF THE BOUNDARIES. AND THAT THE FOREGROUND HAS THE SAME SIZE WIDTH AND HEIGHT AS THE BACKGROUND.
NEVER ADD COMMENTS TO THE JSON.
NEVER RESIZE OR REPOSITION THE BACKGROUND AND FOREGROUND.
                                             
Respond with the following json structure:

{
    "layers": [
        {
            "path": string,
            "type": string,
            "width": number,
            "height": number,
            "x": number,
            "y": number
        },
        ...
    ]
}
    ''', additional_prompt)
