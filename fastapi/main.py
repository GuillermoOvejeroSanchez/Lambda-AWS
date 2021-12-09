import json

import requests
from mangum import Mangum

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users():
    return {"message": "Get Users!"}


@app.get("/hello")
def hello_world():
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "hello wilson", "location": ip.text.replace("\n", "")}
        ),
    }


handler = Mangum(app)
