import streamlit as st

from model import Predict

st.set_page_config(
    page_title="SBER Beautiful Code",
    page_icon=r"icon.png",
)



# Функция отображения главной страницы
def main():
    st.title("Многостраничное приложение")
    st.write("Добро пожаловать на главную страницу!")

# Функция отображения страницы 1
def page1():
    st.title("Описание модели")
    st.write("Вы находитесь на странице 1!")

# Функция отображения страницы 2
def page2():
    st.title("Проверить пароль")
    password = st.text_input('Введите пароль для проверки')
    out = Predict(password, 'len')
    if out == -1:
        st.write('Пароль не может быть пустым')
    else:
        st.write(f'Класс пароля - {out}')

PAGES = {
    "Главная": main,
    "Модель": page1,
    "Проверка пароля": page2
}
# Отображение бокового меню для выбора страницы
st.sidebar.title("Меню")
selection = st.sidebar.radio("", list(PAGES.keys()))

# Отображение выбранной страницы
page = PAGES[selection]
page()
