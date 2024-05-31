import os
import pyaudio
from piper import PiperVoice
from gpiozero import Button
from time import sleep

BUTTON_PIN = 17
button = Button(BUTTON_PIN)

def main():
    # Initialize Piper
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'en_US-lessac-medium.onnx')
    config_path = os.path.join(os.path.dirname(__file__), 'models', 'en_US-lessac-medium.onnx.json')
    piper = PiperVoice.load(model_path, config_path=config_path)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True)

    # Convert text to audio
    def speak():
        text = "Hello! I'm hungry and angry"
        for audio_data in piper.synthesize_stream_raw(text):
            # Play audio as wirting audio data to stream
            stream.write(audio_data)

    button.when_pressed = speak

    try:
        while True:
            sleep(0.1)
            pass
    except KeyboardInterrupt:
        print("Finished")

    print("Closing")
    # Close stream
    stream.stop_stream()
    stream.close()

    # Close Pyaudio
    p.terminate()

if __name__ == "__main__":
    main()
