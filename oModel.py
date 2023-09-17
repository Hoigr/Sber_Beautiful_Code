import streamlit as st
from PIL import Image

def infModel():
    for i in range(1,23):
        url = r's'
        if i < 10:
            url += f'0{i}.jpg'
        else:
            url += f'{i}.jpg'
            
        image = Image.open(url)
        st.image(image)

            
    