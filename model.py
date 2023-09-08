import pandas as pd

class Data:
    def __init__(self, url:str)->None:
        self.df = pd.read_csv(url)
        
class Model(Data):
    pass

url = r'passwords.csv'
zn = Model(url=url)        