import streamlit as st
from PIL import Image

def infModel():
    for i in range(1,18):
        url = r'page\images\s'
        if i < 10:
            url += f'0{i}.jpg'
        else:
            url += f'{i}.jpg'
            
        image = Image.open(url)
        st.image(image)

            
    