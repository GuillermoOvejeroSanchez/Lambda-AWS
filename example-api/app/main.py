import os
from typing import Any

from mangum import Mangum
from starlette.middleware.gzip import GZipMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import APIKeyHeader

app = FastAPI(title="test API", description="users API endpoints", version="1.2.0")
app.add_middleware(GZipMiddleware, minimum_size=1000)


X_API_KEY = APIKeyHeader(name="x-api-key")


def get_api_key(x_api_key: str = Depends(X_API_KEY)) -> str:
    if x_api_key == os.environ.get("X_API_KEY", "1234"):  # Example
        return x_api_key
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


@app.get("/health", summary="Health check.", tags=["HEALTH"])
def health() -> Any:
    return {"UP"}


"""
curl -X 'POST' \
  'http://127.0.0.1:8000/users/12345678'\
  -H 'accept: application/json' \
  -H 'x-api-key: 1234'
"""


@app.post("/users/{userid}")
def userInformation(userid: str, ign: str = Depends(get_api_key)):
    print(ign)
    response = {
        "user": userid,
        "description": "This message returns information about the user",
        "code": 200,
    }
    return response


handler = Mangum(app)
