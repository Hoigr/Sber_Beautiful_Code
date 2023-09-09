from matplotlib import pyplot as plt
import seaborn as sns

import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split as tts

from string import ascii_lowercase, ascii_uppercase, digits, punctuation



class Data:
    def __init__(self, urlDf:str=None, urlMod:str=None)->None:
        self.urlMod = urlMod
        self.urlDf = urlDf
        self.xTrain = None
        self.xTest = None
        self.yTrain = None
        self.yTest = None
        self.seed = 1024
        self.model = None
        self.data = pd.DataFrame()
        self.df = None
        if urlDf != None:
            self.__openData()

    def __openData(self)->None:
        self.df = pd.read_csv(self.urlDf)
        self.df = self.aggFeatures(self.df)

    # Разбиение датасета на тренировочную и тестовую часть
    def split(self)->None:
        colY = 'strength'
        colX = [i for i in self.df.columns if i not in ('strength', 'password')]
        self.xTrain, self.xTest, self.yTrain, self.yTest = tts(self.df[colX],
                                                               self.df[colY],
                                                               test_size=0.25,
                                                               random_state=self.seed)
        self.data['strength'] = self.yTest

    def dsStats(self)->None:
        for col in self.df.columns:
            nan = 100*self.df[col].isna().sum()/len(self.df[col])
            print(f'{col}: кол-во пропущенных значений - {nan}%')
        sns.histplot(self.df['strength'])
        plt.show()

    # Добавим дополнительный агрегированные признаки
    def aggFeatures(self, df:pd.DataFrame):
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

        # Агрегированные признаки - кол-во латинских букв строчных
        df['lowCount'] = df['password'].map(lambda x:check(x, ascii_lowercase))
        # Агрегированные признаки - кол-во латинских букв заглавных
        df['upCount'] = df['password'].map(lambda x:check(x, ascii_uppercase))
        # Агрегированные признаки - кол-во чисел
        df['digitCount'] = df['password'].map(lambda x:check(x, digits))
        # Агрегированные признаки - кол-во специальных символов
        df['symbolCount'] = df['password'].map(lambda x:check(x, punctuation))
        # Агрегированные признаки - кол-во всех остальных символов
        df['otherCount'] = df['password'].map(lambda x:checkNot(x))

        # Агрегированные признаки - кол-во латинских букв строчных
        df['UniqLowCount'] = df['password'].map(lambda x:check(set(x), ascii_lowercase))
        # Агрегированные признаки - кол-во латинских букв заглавных
        df['UniqUpCount'] = df['password'].map(lambda x:check(set(x), ascii_uppercase))
        # Агрегированные признаки - кол-во чисел
        df['UniqDigitCount'] = df['password'].map(lambda x:check(set(x), digits))
        # Агрегированные признаки - кол-во специальных символов
        df['UniqSymbolCount'] = df['password'].map(lambda x:check(set(x), punctuation))
        # Агрегированные признаки - кол-во всех остальных символов
        df['UniqOtherCount'] = df['password'].map(lambda x:checkNot(set(x)))

        # Агрегированные признаки - кол-во всех уникальных символов
        df['uniq'] = df['password'].map(lambda x: len(set(x)))
        # Агрегированные признаки - длинна пароля
        df['len'] = df['password'].map(lambda x:len(x))
        # Агрегированные признаки - кол-во бит энтропии
        df['entrop'] = (df['digitCount']+df['upCount']+df['lowCount'])*5.9542+(df['symbolCount']+df['otherCount'])*6.5699
        df['entrop'] = df['entrop'].map(lambda x: int(x))
        return df

    # Метрики моделей обучения
    def metric(self)->None:
        for col in [i for i in self.data.columns if i!= 'strength']:
            print(f'\t{col}')
            print(classification_report(self.data['strength'], self.data[col]))