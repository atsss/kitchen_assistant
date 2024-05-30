import io
import pyaudio
from piper import PiperVoice

def main():
    # Initialize Piper
    model_path = './models/en_US-lessac-medium.onnx'
    config_path = './models/en_US-lessac-medium.onnx.json'
    piper = PiperVoice.load(model_path, config_path=config_path)


    # Convert text to audio
    text = "Hello! I'm hungry and angry"
    audio_data = piper.synthesize_stream_raw(text)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True)

    # Play audio as wirting audio data to stream
    stream.write(audio_data)

    # Close stream
    stream.stop_stream()
    stream.close()

    # Close Pyaudio
    p.terminate()

if __name__ == "__main__":
    main()
