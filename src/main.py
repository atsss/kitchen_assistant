from fastapi import FastAPI
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
def root(message: Message):
    # FIXME: Locate right after server starts
    tts_client.start()
    tts_client.speak(message.content)
    # FIXME: Locate right before sever stops
    tts_client.stop()
