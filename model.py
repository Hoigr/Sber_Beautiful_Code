import pickle
from catboost import CatBoostClassifier

from data import getEntrop, getDf


def lenModel(password:str)->int:
    if 0 < len(password) <= 7:
        return 0
    elif 8 <= len(password) <= 13:
        return 1
    elif 14 <= len(password):
        return 2
    
def entropModel(password:str)->int:
    dataEntrop = getEntrop(password)
    if dataEntrop < 47:
        return 0
    elif 47 <= dataEntrop <= 82:
        return 1
    elif dataEntrop >= 83:
        return 2    

def lrModel(password:str)->int:
    with open(r'model\lrModel.pickle', 'rb') as file:
        model = pickle.load(file)
    return model.predict(getDf(password))[0]

def svcModel(password:str)->int:
    with open(r'model\svcModel.pickle', 'rb') as file:
        model = pickle.load(file)
    return model.predict(getDf(password))[0]

def boostModel(password:str)->int:
    model = CatBoostClassifier()
    model.load_model(r'model\boostModel.cbm')
    return int(model.predict(getDf(password))[0])

def Predict(password:str, model:str)->int:
    if len(password) == 0:
        return -1
    if model == 'len':
        return lenModel(password)
    elif model == 'entrop':
        return entropModel(password)
    elif model == 'lr':
        return lrModel(password)
    elif model == 'svm':
        return svcModel(password)
    elif model == 'boost':
        return boostModel(password)
    else:
        print('Выбрана неправильная модель')

        
        