from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split as tts
import seaborn as sns
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

 
class Data:
    def __init__(self, url:str)->None:
        self.df = pd.read_csv(url)
        self.xTrain = None
        self.xTest = None
        self.yTrain = None
        self.yTest = None
        
    # Разбиение датасета на тренировочную и тестовую часть 
    def split(self)->None:
        colY = 'strength'
        colX = [i for i in self.df.columns if i in ('strength', 'password')]
        self.xTrain, self.xTest, self.yTrain, self.yTest = tts(self.df[colX],
                                                               self.df[colY],
                                                               test_size=0.25)
        
    def dsStats(self)->None:
        for col in self.df.columns:
            nan = 100*self.df[col].isna().sum()/len(self.df[col])
            print(f'{col}: кол-во пропущенных значений - {nan}%')
        sns.histplot(self.df['strength'])
        plt.show()
    # Добавим дополнительный агрегированные признаки    
    def aggFeatures(self)->None:
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
        self.df['lowCount'] = self.df['password'].map(lambda x:check(x, ascii_lowercase))
        # Агрегированные признаки - кол-во латинских букв заглавных
        self.df['upCount'] = self.df['password'].map(lambda x:check(x, ascii_uppercase))
        # Агрегированные признаки - кол-во чисел
        self.df['digitCount'] = self.df['password'].map(lambda x:check(x, digits))
        # Агрегированные признаки - кол-во специальных символов
        self.df['symbolCount'] = self.df['password'].map(lambda x:check(x, punctuation))
        # Агрегированные признаки - кол-во всех остальных символов
        self.df['allCount'] = self.df['password'].map(lambda x:checkNot(x))
        # Агрегированные признаки - длинна пароля
        self.df['len'] = self.df['password'].map(lambda x:len(x))
        # Агрегированные признаки - кол-во бит энтропии
        self.df['entrop'] = (self.df['digitCount']+self.df['upCount']+self.df['lowCount'])*5.9542+(self.df['symbolCount']+self.df['allCount'])*6.5699
        self.df['entrop'] = self.df['entrop'].map(lambda x: int(x))
        
class Model(Data):
    def sklearn(self):
        pass
    def boost(self):
        pass
    def nn(self):
        pass
    def ans(self):
        pass

url = r'passwords.csv'
zn = Model(url=url)
# zn.dsStats()    
zn.aggFeatures()    