from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from loguru import logger
from typing import Dict, Any
from .classes.tts import TTS

class Message(BaseModel):
    content: str

app = FastAPI()
tts_client = TTS()

@app.middleware("http")
async def log_request_body(request: Request, call_next):
    body = await request.body()

    logger.info(f"Request Headers: {request.headers}")
    logger.info(f"Request Body: {body.decode()}")

    # await request.body()

    return await call_next(request)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/speak")
def speak(message: Message):
    tts_client.start()
    tts_client.speak(message.content)
    tts_client.stop()
    return Response(status_code=status.HTTP_200_OK)

@app.post("/slack")
def slack(message: Dict[Any, Any]):
    # tts_client.start()
    # tts_client.speak(message.content)
    # tts_client.stop()
    logger.info('Detected slack message')
    if message.get('type', None) == 'url_verification':
        logger.info('In verification')
        return message.get('challenge', None)
    logger.info('Slack text', message.get('event', {}).get('text', None))
    return Response(status_code=status.HTTP_200_OK)
