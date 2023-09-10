from model import Model
from job import Job


def lessonModel():
    urlDf = r'passwords.csv'
    urlMod = r'model\\'
    zn = Model(urlDf=urlDf, urlMod=urlMod)
    zn.split()
    zn.ans(save=True)
    zn.vector(save=True)
    zn.boost(save=True)
    zn.lr(save=True)
    zn.metric()
    
def loadPredict(password:str=None):
    urlMod = r'model\\'
    pdm=Job()
    pdm.LoadMod(url=urlMod+'ans.pickle')
    pdm.LoadMod(url=urlMod+'lr.pickle')
    pdm.LoadMod(url=urlMod+'svc.pickle')
    pdm.LoadMod(url=urlMod+'boost.cbm')
    met = ['ans', 'vec', 'lr', 'boost']
    for m in met:
        for k in range(1,15):
            ch = 'a1'*k
            print(k, m, end=' ')
            out = pdm.predPass(password=ch, method=m)
            print(int(out),'\t', ch)

# lessonModel()    
loadPredict()