from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from .classes.tts import TTS

class Message(BaseModel):
    content: str

app = FastAPI()
tts_client = TTS()

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
def slack():
    # tts_client.start()
    # tts_client.speak(message.content)
    # tts_client.stop()
    return Response(status_code=status.HTTP_200_OK)
