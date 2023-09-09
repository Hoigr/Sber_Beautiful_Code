from model import Model
from catboost import CatBoostClassifier
import pandas as pd

import pickle

class Job(Model):    
    def LoadMod(self,  url:str=None)->None:
        if 'pickle' in url:
            with open(url, 'rb') as file:
                if 'ans.pickle' in url:
                    self.modAns = pickle.load(file)
                elif 'lr.pickle' in url:
                    self.modLr = pickle.load(file)
                elif 'svc.pickle' in url:
                    self.modVec = pickle.load(file)
        elif 'boost.cbm' in url:
            self.modBoost = CatBoostClassifier()
            self.modBoost.load_model(url)
        else:
            print('Неизвестная модель -', url)

        self.models = {'ans':self.modAns,
                       'lr':self.modLr,
                       'boost':self.modBoost,
                       'vec':self.modVec}

    def predPass(self, password:str, method:str='ans' )->int:
        if method.lower() not in  self.models.keys():
            print('Неправильно задано имя модели -', method)
            print('Доступные названия моделей -',  *list(self.models.keys()))
            return -1
        if self.models[method.lower()] == None:
            print('Необходимо сначало загрузить модель -',method)
            return -1

        data = pd.DataFrame(data=[password], columns=['password'])
        data = self.aggFeatures(data)
        col = [i for i in data if i!='password' ]
        yPred = self.models[method.lower()].predict(data[col])
        return int(yPred[0])