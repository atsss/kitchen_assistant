import io
import pyaudio
from piper import Piper

def main():
    # Initialize Piper
    model_path = "path_to_your_model_directory"
    piper = Piper(model_path=model_path)


    # Convert text to audio
    text = "Hello! I'm hungry and angry"
    audio_data = piper.tts(text)

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
