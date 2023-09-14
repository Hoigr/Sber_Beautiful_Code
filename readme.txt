https://beautifulcode.sber.ru/task/data_science

Постройте наилучшую модель, которая на основании размеченных данных будет предсказывать качество пароля, введенного пользователем. Данные состоят из примеров паролей и их оценок: 0 (слабый), 1 (средний) и 2 (сильный).

Дополнительные требования:

Предусмотреть возможность проверки новых паролей.
Прокомментировать и обосновать преобразования данных, выбор метода и метрики для оценивания результата предсказания модели.

import streamlit as st
import pandas as pd
from PIL import Image
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

def check(obj:str, sample:str)->int:
    out = 0
    for i in obj:
        if i in sample:
            out += 1
    return out

def checkNot(obj:str)->int:
            out = 0
            for i in obj:
                if i not in ascii_lowercase + ascii_uppercase + digits + punctuation:
                    out +=1
            return out
def getEntrop(password:str)->int:
    out = check(password, digits)
    out += check(password, ascii_uppercase)
    out += check(password, ascii_lowercase)
    out *= 5.9542
    out += (check(password, punctuation)+checkNot(password))*6.5699
    return int(out)
        
def infModel():
    df = pd.read_csv(r'passwords.csv')
    st.title('Описание разработки модели')
    st.code('''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

url = r'passwords.csv'
df = pd.read_csv(url)''')
    st.markdown('''## Описание данных
* password - пароль
* strength (target) - оценка пароля: 0 - слабый, 1 - средний, 2 - сильный. Целевая переменная''')
    st.code('''df.head(5)''')
    st.write(df.head(5))
    st.code('''df.tail(5)''')
    st.write(df.tail(5))
    st.markdown('''## Исследование данных''')
    st.markdown('''Размер датасета''')
    st.write(df.shape)
    st.markdown('''Информация о типах данных и пропущенных значениях''')
    st.code('''RangeIndex: 100000 entries, 0 to 99999
Data columns (total 2 columns):
 #   Column    Non-Null Count   Dtype
---  ------    --------------   -----
 0   password  100000 non-null  object
 1   strength  100000 non-null  int64
dtypes: int64(1), object(1)
memory usage: 1.5+ MB ''')
    st.code('''df.describe(include='object')''')
    st.write(df.describe(include='object'))
    st.markdown('''Основные числовые характеристики целевой переменной''')
    st.code('''df['strength'].describe()''')
    st.write(df['strength'].describe())
    st.write('Посмотрим на распределение оценок')
    st.image(Image.open(r'page\bar.png'))
    st.markdown('''* В данных отсутствуют пропущенные значения
* Пароли все уникальные
* Аномалий в оценках класса пароля нет
## Добавление агрегированных признаков
Функция подсчета символов изопределенного набора в пароле''')
    st.code('''def check(obj:str, sample:str)->int:
    out = 0
    for i in obj:
        if i in sample:
            out += 1
    return out

def checkNot(obj:str)->int:
            out = 0
            for i in obj:
                if i not in ascii_lowercase + ascii_uppercase + digits + punctuation:
                    out +=1
            return out''')
    st.write('Функция рассчета энтропии')
    st.code('''def getEntrop(password:str)->int:
    out = check(password, digits)
    out += check(password, ascii_uppercase)
    out += check(password, ascii_lowercase)
    out *= 5.9542
    out += (check(password, punctuation)+checkNot(password))*6.5699
    return int(out)''')
    
