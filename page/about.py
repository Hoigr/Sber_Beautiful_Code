import streamlit as st
txt = '''### Красивый код соревнование от Сбера
### в дисциплине data science

https://beautifulcode.sber.ru/task/data_science

**Цель соревнования:**

* Построить модель, которая на основании размеченных данных будет предсказывать качество пароля
'''

def about():
    st.markdown(txt)