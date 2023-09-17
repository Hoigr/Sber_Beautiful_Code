import streamlit as st
from model import Predict
import pandas as pd
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import randint, sample
from data import getEntrop


def pageCh():
    st.image(r'passLogo.webp', width=250)
    tab1, tab2, tab3 = st.tabs(["Проверить пароль", "Проверить файл с паролями", "Сгенерировать пароль"])
    with tab1:
        st.title("Проверить пароль") 
        options = st.multiselect(
            label='Выберите модель для предсказания класса пароля',
            options=['Градиентный бустинг', 
             'Метод опорных векторов', 
             'Логистическая регрессия', 
             'Энтропия пароля', 
             'Длинна пароля'],
            default=['Энтропия пароля'], 
            key=0)   
        password = st.text_input(label='Введите пароль для проверки')
        
        if len(password) == 0:
            st.write('Пароль не может быть пустым')
        else:
            if len(options) > 0:
                for i in options:
                    clPass = Predict(model=i, password=password)
                    st.write(f'Модель {i} - {clPass}')
                r1 = f'- Увеличить длинну пароля от {9-len(password)} до {12-len(password)} символов что бы пароль подпадал под класс 1'
                r2 = f'- Увеличить длинну пароля от {15-len(password)} символов что бы пароль подпадал под класс 2'
                if clPass == 0:  
                    st.markdown('''##### Рекомендация:''')
                    st.write(r1)
                    st.write(r2)
                elif clPass == 1:
                    st.markdown('''##### Рекомендация:''')
                    st.write(r2)
            else:
                st.write('Не выбрана модель')

    with tab2:
        st.header("Проверить файл с паролями")
        st.text('Загрузите файл с паролями для проверки в формате csv.')
        st.text('Файл должен содержать столбец password который будет проверятся.') 
        options = st.multiselect(
            label='Выберите модель для предсказания класса пароля',
            options=['Градиентный бустинг', 
             'Метод опорных векторов', 
             'Логистическая регрессия', 
             'Энтропия пароля', 
             'Длинна пароля'],
            default=['Энтропия пароля'], key=1)
        uploaded_file = st.file_uploader(label="Загрузите файл CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            col = [i for i in df.columns]
            if 'password' not in col:
                st.write('Отсутствует столбец password')
            elif len(options) > 0:
                df = df[df['password'] != '']
                df['len'] = df['password'].map(len)
                df['entrop'] = df['password'].map(getEntrop)
                df = df[['password', 'len', 'entrop']]

                for met in options:
                    Predict(model=met, df=df)
                df = df[[i for i in df.columns if i not in ('len', 'entrop')]]
                st.write(df)
                def download_csv(dataframe):
                    csv = dataframe.to_csv(index=False)
                    return csv

                csv_data = download_csv(df)
                st.download_button(label='Нажмите, чтобы скачать', 
                                    data=csv_data, 
                                    file_name='predict.csv', 
                                    mime='text/csv')
          
    
    with tab3:
        st.title("Сгенерировать пароль")
        cls = st.slider(label='Выберите класс пароля', min_value=0, max_value=2, value=1, step=1, key=3)
        number = st.number_input(label='Выбирите число паролей не более 50',min_value=1, max_value=50, value=5, step=1)
        gen = st.button(label="Сгенерировать", type="primary")
        out = []
        symbol = ascii_lowercase+ascii_uppercase+digits+punctuation
        if gen:
            if cls == 0:
                for _ in range(number):
                    out.append(''.join(sample(symbol, randint(1,6))))
            elif cls == 1:
                for _ in range(number):
                    out.append(''.join(sample(symbol, randint(8,12))))
            elif cls == 2:
                for _ in range(number):
                    out.append(''.join(sample(symbol, randint(14,50))))
            password = pd.DataFrame(out, columns=['password'])
            st.dataframe(password)
            def download_csv(dataframe):
                csv = dataframe.to_csv(index=False)
                return csv

            csv_data = download_csv(password)
            st.download_button(label='Скачать пароли', 
                           data=csv_data, 
                           file_name='password.csv', 
                           mime='text/csv')

                 
   
    