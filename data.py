from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import pandas as pd

def check(obj:str, sample:str)->int:
    out = 0
    for i in obj:
        if i in sample:
            out += 1
    return out

def checkNot(obj:str)->int:
            out = 0
            for i in obj:
                if i not in ascii_lowercase + ascii_uppercase + digits + punctuation:
                    out +=1
            return out

def getEntrop(password:str)->int:
    out = check(password, digits)
    out += check(password, ascii_uppercase)
    out += check(password, ascii_lowercase)
    out *= 5.9542
    out += (check(password, punctuation)+checkNot(password))*6.5699
    return int(out)        

def getDf(password:str)->pd.DataFrame:
    out = pd.DataFrame()
    out['len'] = [len(password)]
    out['entrop'] = [getEntrop(password)]
    return out
      