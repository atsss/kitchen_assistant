from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from loguru import logger
from typing import Union, Any
from .classes.tts import TTS

class Message(BaseModel):
    content: str

class SlackSubscripion(BaseModel):
    token: str
    challenge: str
    type: str

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
def slack(message: Union[SlackSubscripion, Any]):
    # tts_client.start()
    # tts_client.speak(message.content)
    # tts_client.stop()
    logger.info('Detected slack message')
    if message.type == 'url_verification':
        logger.info('In verification')
        return message.challenge
    logger.info('Here', message)
    return Response(status_code=status.HTTP_200_OK)
