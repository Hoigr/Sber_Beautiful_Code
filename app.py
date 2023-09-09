from fastapi import FastAPI

api = FastAPI()

@api.get('/')
def index():
    return {'message':'start api'}

@api.get('/info')
def info():
    return {'message':'Здесь будет опсание модели'}

@api.post('/predict')
def predict():
    return {'predict':'predict password'}

@api.get('/check')
def check():
    return {'message':'проверка пароля введенного в поле'}