import streamlit as st
from oModel  import infModel
from checkPass import pageCh
from about import about

st.set_page_config(
    page_title="SBER Beautiful Code",
    page_icon=r"icon.png",
)

         

PAGES = {
    "Главная": about,
    "Модель": infModel,
    "Проверка пароля": pageCh,
}

st.sidebar.title("Меню")
selection = st.sidebar.radio(label=" ", options=list(PAGES.keys()))

page = PAGES[selection]
page()

