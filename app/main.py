from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pathlib import Path
import secrets
import string
import pickle

class Secret(BaseModel):
    text: str
    code_phrase: str

class Code(BaseModel):
    code_phrase: str

secret_db = {}

alphabet = string.ascii_letters + string.digits

app = FastAPI()

@app.post('/generate/')
def generate_secret(secret: Secret):
    # secret_key = ''.join(secrets.choice(alphabet) for i in range(20))
    secret_key = 'aaa'
    secret_db[secret_key] = {'text': secret.text, 'code_phrase': secret.code_phrase }

    Path('files').mkdir(parents=True, exist_ok=True)
    Path('files/data.txt').touch(exist_ok=True)
    with open('files/data.txt', 'wb') as src:
        pickle.dump(secret_db, src, protocol=3)
    return {'secret_key': secret_key}

@app.post('/secrets/{secret_key}/')
def get_secret(secret_key: str, code: Code):

    Path('files').mkdir(parents=True, exist_ok=True)
    Path('files/data.txt').touch(exist_ok=True)

    with open('files/data.txt', 'rb') as src:
        secret_db = pickle.load(src)
    if secret_key not in secret_db.keys():
        raise HTTPException(status_code=404, detail='key not found')
    if code.code_phrase == secret_db[secret_key]['code_phrase']:
        secret = secret_db.pop(secret_key)

        Path('files').mkdir(parents=True, exist_ok=True)
        Path('files/data.txt').touch(exist_ok=True)

        with open('files/data.txt', 'wb') as src:
            pickle.dump(secret_db, src, protocol=3)
        return {'secret': secret['text']}
    raise HTTPException(status_code=404, detail='invalid code')

@app.get('/')
def get_root():
    return {'hello': 'world'}
