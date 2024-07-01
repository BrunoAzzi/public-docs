import streamlit as st
from PIL import Image
import io
import base64
from rembg import remove
import json

def base64Image(path):
    with Image.open(path) as image:
        image_rgb = image.convert('RGB')
        buffer = io.BytesIO()
        image_rgb.save(buffer, format='JPEG')
        byte_data = buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode()

    return base64_str

def remove_background(image_path):
    image = Image.open(image_path)

    output = remove(image)
    output.save(image_path.replace('.','_foreground.'))
    return image_path.replace('.','_foreground.')

def trim_background(image_path: str):
    im = Image.open(image_path)

    if im.size != im.getbbox():
        im2 = im.crop(im.getbbox())
        im2.save(image_path)

    return image_path

def flatten_image(background_path, foreground_path, logo_base64_string, response):
    poster = Image.open(background_path)
    foreground = Image.open(foreground_path)

    image = io.BytesIO(base64.b64decode(logo_base64_string))
    logo = Image.open(image)

    new_width = int(response['width'])
    new_height = int(response['height'])

    logo = logo.resize((new_width, new_height))

    x = int(response['x'])
    y = int(response['y'])
    poster.paste(logo, (x, y), logo)

    poster.paste(foreground, (0,0), foreground)

    poster.save(background_path.replace('.png', '_with_logo.png'))
    return poster

def render_image(response):
    with st.expander("Json", expanded = True):
        st.text(response)

    with st.expander("Image", expanded = True):
        layers = json.loads(response)['layers']
        
        final_image = None

        for image in layers:
            current_layer = Image.open(image['path'])    
            width = int(image['width'])
            height = int(image['height'])
            x = int(image['x'])
            y = int(image['y'])
            type = image['type']
            size = (width, height)
            

            # if type == 'asset':
            if final_image is not None:
                size = (max(final_image.width, width), max(final_image.height, height))
                
            if current_layer.width != width or current_layer.height != height:
                current_layer = current_layer.resize((width, height))

            img_trans = Image.new("RGBA", size)
            img_trans.paste(current_layer, (x, y))

            current_layer = img_trans

            if final_image:
                final_image = Image.alpha_composite(final_image, current_layer)
            else:
                final_image = current_layer

        st.image(final_image, caption="Final image", use_column_width=True)
