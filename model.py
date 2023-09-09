from data import Data
from catboost import CatBoostClassifier

import pickle

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier

class Model(Data):
    def __init__(self, urlDf:str=None, urlMod:str=None):
        super().__init__(urlDf=urlDf, urlMod=urlMod)
        self.modAns = None
        self.modLr = None
        self.modBoost = None
        self.modVec = None
        self.models = {'ans':self.modAns,
                       'lr':self.modLr,
                       'boost':self.modBoost,
                       'vec':self.modVec}

    # Стэкинг ансамбль обучения
    def ans(self, save:bool=False):
        vec = svm.SVC(kernel='rbf', random_state=self.seed)
        boost = CatBoostClassifier(iterations=1000,
                                   learning_rate=0.01,
                                   random_state=self.seed,
                                   verbose=False)
        lr = LogisticRegression(solver='newton-cholesky')
        estimators = [('vec', vec),
                      ('boost', boost),
                      ('lr', lr)]


        self.modAns = StackingClassifier( estimators=estimators,
                                 final_estimator=LogisticRegression())
        self.modAns.fit(self.xTrain, self.yTrain)
        self.data['ans'] = self.modAns.predict(self.xTest)
        if save:
            with open(self.urlMod+'ans.pickle', 'wb') as file:
                pickle.dump(self.modAns, file)


    # Метод опорных векторов
    def vector(self, save:bool=False)->None:
        self.modVec = svm.SVC(kernel='rbf',
                        random_state=self.seed)
        self.modVec.fit(self.xTrain, self.yTrain)
        self.data['svc'] = self.modVec.predict(self.xTest)
        if save:
            with open(self.urlMod+'svc.pickle', 'wb') as file:
                pickle.dump(self.modVec, file)

    # Градиентный бустиннг
    def boost(self, save:bool=False)->None:
        self.modBoost = CatBoostClassifier(iterations=600,
                                   learning_rate=0.01,
                                   random_state=self.seed,
                                   verbose=False)
        self.modBoost.fit(self.xTrain, self.yTrain)
        self.data['boost'] = self.modBoost.predict(self.xTest)
        if save:
            self.modBoost.save_model(self.urlMod+'boost.cbm', format="cbm")

    def lr(self, save:bool=False):
        self.modLr = LogisticRegression(solver='newton-cholesky')
        self.modLr.fit(self.xTrain, self.yTrain)
        self.data['lr'] = self.modLr.predict(self.xTest)
        if save:
            with open(self.urlMod+'lr.pickle', 'wb') as file:
                pickle.dump(self.modLr, file)