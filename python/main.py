# Combined script to record audio and convert it to text

# For audio recording
import sounddevice as sd
from scipy.io.wavfile import write

# For audio to text conversion
import speech_recognition as sr
from pydub import AudioSegment

# For classification
import os
import openai
import constant

def record_audio_to_wav(filename):
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    print("Recording...")

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    print("Recording finished.")

    wav_filename = filename + ".wav"
    write(wav_filename, fs, myrecording)  # Save as WAV file

    print(f"Saved recording as {wav_filename}")

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    audio = AudioSegment.from_file(audio_file_path, format="wav")
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"

def textToEmotion(text):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": constant.SYSTEM_MESSAGE},
        {"role": "user", "content": text}
    ]
    )

    emotion = completion.choices[0].message.content
    print(emotion)
    return emotion

if __name__ == "__main__":
    filename = "test"
    record_audio_to_wav(filename)

    audio_file_path = filename + ".wav"
    text = audio_to_text(audio_file_path)
    print(f"Transcribed text: {text}")
    emotion = textToEmotion(text)
    print(f"Emotion: {emotion}")
