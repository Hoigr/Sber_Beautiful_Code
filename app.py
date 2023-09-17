import streamlit as st
from page.oModel  import infModel
from page.checkPass import pageCh
from page.about import about

st.set_page_config(
    page_title="SBER Beautiful Code",
    page_icon=r"page\images\icon.png",
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

