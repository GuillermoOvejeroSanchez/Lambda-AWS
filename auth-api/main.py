import json
from datetime import datetime
from typing import Optional

from kafka import KafkaProducer
from mangum import Mangum
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKey, APIKeyHeader

BOOTSTRAP_SERVERS = "localhost:9092"

app = FastAPI()

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"

api_key = APIKeyHeader(name=API_KEY_NAME)


def send_event(producer: KafkaProducer, key, msg, topic="topic-events"):
    print("sending msg...")
    producer.send(
        topic,
        key=key.encode("utf-8"),
        value=msg,
    )


async def get_api_key(api_key: str = Security(api_key)):

    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")


class Event(BaseModel):
    event_id: str
    event_type: str
    optional_message: Optional[str] = None


@app.post("/event")
def event(event: Event, api_key: APIKey = Depends(get_api_key)):
    event_type = event.event_type
    event_id = event.event_id
    now_str = str(datetime.utcnow())
    body = f"id: {event_id} type: {event_type} sended to queue at: {now_str}"
    msg = {
        "event_id": event_id,
        "event_type": event_type,
        "message": event.optional_message,
    }

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    send_event(producer, event_id, msg)
    return {"message": body}


handler = Mangum(app)
