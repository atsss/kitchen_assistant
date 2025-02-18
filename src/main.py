from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from loguru import logger
from typing import Dict, Any
from .classes.tts import TTS
import re

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
    logger.info('Detected slack message')
    if message.get('type', None) == 'url_verification':
        logger.info('In verification')
        return message.get('challenge', None)

    text = message.get('event', {}).get('text', None)
    logger.info(f"Slack text {text}")
    if text is not None:
        content = re.sub(r'<@U07DG05L1UY>\s*', '', text)
        logger.info(f"Content to speack {content}")

        tts_client.start()
        tts_client.speak(content)
        tts_client.stop()

    return Response(status_code=status.HTTP_200_OK)
