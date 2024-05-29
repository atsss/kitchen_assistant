import io
import pyaudio
from piper import Piper

def main():
    # Piperの初期化
    model_path = "path_to_your_model_directory"
    piper = Piper(model_path=model_path)

    # 読み上げるテキスト
    text = "こんにちは、これはテキストから音声への変換のデモです。"

    # テキストを音声に変換
    audio_data = piper.tts(text)

    # PyAudioの設定
    p = pyaudio.PyAudio()

    # ストリームを開く
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True)

    # 音声データをストリームに書き込んで再生
    stream.write(audio_data)

    # ストリームを閉じる
    stream.stop_stream()
    stream.close()

    # PyAudioの終了処理
    p.terminate()

if __name__ == "__main__":
    main()
