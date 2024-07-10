from fastapi import FastAPI
from classes.tts import TTS

app = FastAPI()
tts_client = TTS()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/speak")
def root(message: str):
    # FIXME: Locate right after server starts
    tts_client.start()
    tts_client.speak(message)
    # FIXME: Locate right before sever stops
    tts_clinent.stop()
