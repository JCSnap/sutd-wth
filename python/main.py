import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv


def record_audio_to_mp3(filename):
    fs = 44100
    seconds = 3

    print("Recording...")

    # Specify mono channel to avoid invalid channel error
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)

    sd.wait()
    print("Recording finished")

    # Convert to wav
    wav_filename = filename + ".wav"
    write(wav_filename, fs, myrecording)

    # Convert wav to mp3
    mp3_filename = filename + ".mp3"
    wv.write(mp3_filename, myrecording, fs, sampwidth=2)

    print(f"Saved recordings as {wav_filename} and {mp3_filename}")


record_audio_to_mp3('test')
