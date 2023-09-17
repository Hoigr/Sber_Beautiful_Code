import streamlit as st
from PIL import Image

def infModel():
    st.image(r'page\images\modLogo.jpg', width=100, use_column_width=True)
    for i in range(1,23):
        url = r'page\images\s'
        if i < 10:
            url += f'0{i}.jpg'
        else:
            url += f'{i}.jpg'
            
        image = Image.open(url)
        st.image(image)

            
    