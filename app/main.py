from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pathlib import Path
import secrets
import string
import pickle


def load_secrets():
    if filepath.stat().st_size > 0:
        with open('files/data.txt', 'rb') as src:
            secret_db = pickle.load(src)
    else:
        secret_db = {}
    return secret_db


def generate_unique_key(secret_db):
    while True:
        secret_key = ''.join(secrets.choice(alphabet) for i in range(20))
        if secret_key not in secret_db.keys():
            return secret_key


class Secret(BaseModel):
    text: str
    code_phrase: str


class Code(BaseModel):
    code_phrase: str

alphabet = string.ascii_letters + string.digits

Path('files').mkdir(parents=True, exist_ok=True)
filepath = Path('files') / Path('data.txt')
filepath.touch(exist_ok=True)

app = FastAPI()


@app.post('/generate/')
def generate_secret(secret: Secret):

    secret_db = load_secrets()

    secret_key = generate_unique_key(secret_db)

    secret_db[secret_key] = {
        'text': secret.text,
        'code_phrase': secret.code_phrase
    }

    with open('files/data.txt', 'wb') as src:
        pickle.dump(secret_db, src, protocol=3)
    return {'secret_key': secret_key}


@app.post('/secrets/{secret_key}/')
def get_secret(secret_key: str, code: Code):

    secret_db = load_secrets()

    if secret_key not in secret_db.keys():
        raise HTTPException(status_code=404, detail='key not found')
    if code.code_phrase == secret_db[secret_key]['code_phrase']:
        secret = secret_db.pop(secret_key)
        with open('files/data.txt', 'wb') as src:
            pickle.dump(secret_db, src, protocol=3)
        return {'secret': secret['text']}
    raise HTTPException(status_code=404, detail='invalid code')


@app.get('/')
def get_root():
    return {'hello': 'world'}
