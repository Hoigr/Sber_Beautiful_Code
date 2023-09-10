from fastapi import FastAPI
from job import Job


api = FastAPI()

  
@api.get('/')
def index():
    return {'message':'start api'}

@api.get('/info')
def info():
    return {'message':'Здесь будет опсание модели'}

@api.post('/predict/')
def predict(password:str):
    if password == '':
        return  {'messadge': 'Отсутствует пароль'}
    if isinstance(password,(str, int)):
        urlMod = r'model\\'
        check=Job()
        check.LoadMod(url=urlMod+'ans.pickle')
        check.LoadMod(url=urlMod+'lr.pickle')
        check.LoadMod(url=urlMod+'svc.pickle')
        check.LoadMod(url=urlMod+'boost.cbm')
        met = ['ans', 'vec', 'lr', 'boost']
        out = {i:check.predPass(password=password, method=i) for i in met}
        return {password: out}
    else:
        return {'messadge':f'Пароль должен иметь строковый тип вместо {str(type(password))}'}

@api.get('/check')
def check():
    return {'message':'проверка пароля введенного в поле'}
