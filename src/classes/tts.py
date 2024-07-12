import os
import pyaudio
from piper import PiperVoice
from loguru import logger

class TTS:
    PARENT_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
    MODEL_PATH = os.path.join(PARENT_DIR, 'models', 'en_US-lessac-medium.onnx')
    CONFIG_PATH = os.path.join(PARENT_DIR, 'models', 'en_US-lessac-medium.onnx.json')

    def __init__(self) -> None:
        logger.debug(self.PARENT_DIR, self.MODEL_PATH, self.CONFIG_PATH)
        self.piper = PiperVoice.load(self.MODEL_PATH, config_path=self.CONFIG_PATH)
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def __del__(self) -> None:
        self.audio.terminate()

    def start(self):
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

    def speak(self, content: str) -> None:
        logger.debug('Speaking')
        for audio_data in self.piper.synthesize_stream_raw(content):
            # Play audio as wirting audio data to stream
            self.stream.write(audio_data)
