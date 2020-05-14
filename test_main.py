from fastapi.testclient import TestClient
from pathlib import Path
from app import app

client = TestClient(app)


def test_generate_secret():
    response = client.post(
        '/generate/',
        json = {
            'text': 'up, up, down, down, left, right, left, right, B, A',
            'code_phrase': 'Konami'
        }
    )
    assert response.status_code == 200
    global secret_key
    secret_key = response.json()['secret_key']
    assert len(secret_key) == 20


def test_get_secret_invalid_code():
    response = client.post(f'/secrets/{secret_key}/', json = {'code_phrase': 'code'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'invalid code'}


def test_get_secret_valid_code():
    response = client.post(f'/secrets/{secret_key}/', json = {'code_phrase': 'Konami'})
    assert response.status_code == 200
    assert response.json() == {'secret': 'up, up, down, down, left, right, left, right, B, A'}


def test_get_secret_wrong_key():
    response = client.post(f'/secrets/{secret_key}/', json = {'code_phrase': 'Konami'})
    Path('files/data.txt').unlink()
    Path('files').rmdir()
    assert response.status_code == 404
    assert response.json() == {'detail': 'key not found'}
