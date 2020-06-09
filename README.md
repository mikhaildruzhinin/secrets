# secrets

This is an HTTP service for creating one-time secrets similar to [this one](https://onetimesecret.com/). It allows you to create secrets, set code phrases for them and generates secret keys that lets you read the secret once. I used [FastAPI](https://fastapi.tiangolo.com/) framework to build the app and [pytest](https://docs.pytest.org/) for the tests.

### How to install

[Docker](https://www.docker.com/) should be already installed. In most cases Docker already includes Docker Compose, but if you have to install it manually, please follow the instructions in the [official documentation](https://docs.docker.com/compose/install/).

After that just clone this repository.

### Launch

Open the directory containing cloned repo in the terminal and execute the following command:
```
docker-compose up
```
The app will be running on http://localhost:8000/.

### Requests

`POST /generate/` generates a new secret. It requires the following body:
```
{
  "text": "your secret",
  "code_phrase": "your code phrase"
}
```
and returns the secret key for your secret:
```
{"secret_key": "your secret key"}
```

`POST /secrets/{secret_key}` shows you the secret. It requires a string type `secret_key` parameter and the following body:
```
{"code_phrase": "your code phrase"}
```
and returns the text of your secret:
```
{"secret": "your secret text"}
```

For more information please see automatic interactive API documentation [here](http://localhost:8000/docs/) that will be generated once you run the app.

### Project Goals

The code is written as a test for [Avito](https://start.avito.ru/tech).
