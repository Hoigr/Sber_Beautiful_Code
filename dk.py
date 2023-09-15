import pandas as pd
from string import ascii_uppercase
from data import getEntrop, check
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pickle
from catboost import CatBoostClassifier

df = pd.read_csv(r'passwords.csv')
df['len'] = df['password'].map(lambda x: len(x))
df['entrop'] = df['password'].map(lambda x: getEntrop(x))
df['UniqUpCount'] = df['password'].map(lambda x: check(set(x), ascii_uppercase))
df['upCount'] = df['password'].map(lambda x:check(x, ascii_uppercase))

def saveModel(model, name:str)->None:
    urlMod = r'model\\'
    with open(urlMod+name+'.pickle', 'wb') as file:
        pickle.dump(model, file)
        
xCol = [i for i in df.columns if i not in ('strength', 'password')]
yCol = 'strength'
x_train, x_test, y_train, y_test = train_test_split(df[xCol],
                                                    df[yCol],
                                                    test_size=0.25,
                                                    random_state=1024)

lrModel = LogisticRegression( solver='newton-cg', random_state=1024, max_iter=150)
xCol = ['len', 'entrop', 'UniqUpCount', 'upCount']
lrModel.fit(x_train[xCol], y_train)
saveModel(lrModel, 'lrModel')
svcModel = SVC(kernel='rbf')
svcModel.fit(x_train[xCol], y_train)
saveModel(svcModel, 'svcModel')
boostModel = CatBoostClassifier(iterations=1000,
                           learning_rate=0.01,
                           random_state=1024,
                           verbose=False)

boostModel.fit(x_train[xCol], y_train)
urlMod = r'model\\'
boostModel.save_model(urlMod+'boostModel.cbm', format="cbm")        