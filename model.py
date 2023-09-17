import pickle
from catboost import CatBoostClassifier
import pandas as pd
from data import getEntrop, getDf

xCol = ['len', 'entrop']
def lenModel(**kwarg):
    def getClass(password:str)->int:
            if 0 < len(password) <= 7:
                return 0
            elif 8 <= len(password) <= 13:
                return 1
            elif 14 <= len(password):
                return 2

    if 'password' in kwarg:
        return getClass(password=kwarg['password'])
    if 'df' in kwarg:
        kwarg['df']['Длинна пароля'] = kwarg["df"]['password'].map(lambda x: getClass(x))
        return kwarg['df']
    
    
def entropModel(**kwarg ):
    def getClass(password:str)->int:
        dataEntrop = getEntrop(password)
        if dataEntrop < 47:
            return 0
        elif 47 <= dataEntrop <= 82:
            return 1
        elif dataEntrop >= 83:
            return 2
    if 'password' in kwarg:
        return getClass(password=kwarg['password'])
    if 'df' in kwarg:
        kwarg['df']['Энтропия пароля'] = kwarg['df']['password'].map(getClass)
        return kwarg['df']   

def lrModel(**kwarg):
    with open(r'lrModel.pickle', 'rb') as file:
        model = pickle.load(file)
    if 'password' in kwarg:
        return model.predict(getDf(kwarg['password']))[0]
    if 'df' in kwarg:       
        kwarg['df']['Логистическая регрессия'] = model.predict(kwarg['df'][xCol])
        return kwarg['df'] 

def svcModel(**kwarg):
    with open(r'svcModel.pickle', 'rb') as file:
        model = pickle.load(file)
    if 'password' in kwarg:
        return model.predict(getDf(kwarg['password']))[0]
    if 'df' in kwarg:
        kwarg['df']['Метод опорных векторов'] = model.predict(kwarg['df'][xCol])
        return kwarg['df']

def boostModel(**kwarg):
    model = CatBoostClassifier()
    model.load_model(r'boostModel.cbm')
    if 'password' in kwarg:
        return int(model.predict(getDf(kwarg['password']))[0])
    if 'df' in kwarg:
        kwarg['df']['Градиентный бустинг'] = model.predict(kwarg['df'][xCol])
        return kwarg['df']

def Predict(**kwarg):
    if kwarg['model'] == 'Длинна пароля':
        return lenModel(**kwarg)
    elif kwarg['model'] == 'Энтропия пароля':
        return entropModel(**kwarg)
    elif kwarg['model'] == 'Логистическая регрессия':
        return lrModel(**kwarg)
    elif kwarg['model'] == 'Метод опорных векторов':
        return svcModel(**kwarg)
    elif kwarg['model'] == 'Градиентный бустинг':
        return boostModel(**kwarg)
    else:
        print('Выбрана неправильная модель')

        
        