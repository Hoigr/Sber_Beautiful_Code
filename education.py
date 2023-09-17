import pandas as pd
from data import getEntrop
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import pickle

class Data:
    def __init__(self, url:str):
        self.df = pd.read_csv(url)
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.seed = 1024
        self.__addData()
        
    def __addData(self):
        self.df['len'] = self.df['password'].map(len)
        self.df['entrop'] = self.df['password'].map(getEntrop)
        xCol = [i for i in self.df.columns if i not in ('password', 'strength')]
        yCol = 'strength'
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.df[xCol],
                                                                                self.df[yCol],
                                                                                test_size=0.25,
                                                                                random_state=self.seed)
            
class Model(Data):
    def _saveModel(self, model, name:str)->None:
        with open(name+'.pickle', 'wb') as file:
            pickle.dump(model, file)
    
    def logReg(self, save:bool=False)->None:
        lrModel = LogisticRegression(solver='newton-cg',
                                     random_state=self.seed,
                                     max_iter=150)
        lrModel.fit(self.x_train, self.y_train)
        if save:
            self._saveModel(model=lrModel, name=r'model\lrModel')
    
    def svcModel(self, save:bool=False)->None:
        svcModel = SVC(kernel='rbf')
        svcModel.fit(self.x_train, self.y_train)
        if save:
            self._saveModel(model=svcModel, name=r'model\svcModel')
            
    def boost(self, save:bool=False)->None:
        boostModel = CatBoostClassifier(iterations=1000,
                                        learning_rate=0.01,
                                        random_state=self.seed,
                                        verbose=False)
        boostModel.fit(self.x_train, self.y_train)
        if save:
            boostModel.save_model(r'model\boostModel.cbm', format="cbm")
        
            
        

if __name__ == '__main__':
    urlDf = r'passwords.csv'
    md = Model(url=urlDf)
    md.boost(save=True)
    md.logReg(save=True)
    md.svcModel(save=True)
