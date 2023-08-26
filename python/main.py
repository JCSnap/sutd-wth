# Combined script to record audio and convert it to text

# For audio recording
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write

# For record audio based on silence
import pyaudio
import wave
import audioop

# For audio to text conversion
import speech_recognition as sr
from pydub import AudioSegment

# For classification
import os
import openai
import constant

# For text to speech
from gtts import gTTS
import pygame

# For loudness measurement
import librosa


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


def record_voice(thresh=constant.THRESH, max_silence=constant.MAX_SILENCE, filename="voice.wav"):
    # Initialize pyaudio
    p = pyaudio.PyAudio()

    # Start the stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    # Parameters
    frame_count = 0
    frames = []
    is_recording = False

    print("Waiting for a noise to start recording...")

    while True:
        # Read a chunk from audio input
        chunk = stream.read(1024)

        # Check for voice
        rms = audioop.rms(chunk, 2)

        if rms > thresh:
            if not is_recording:
                print("Noise detected, starting recording!")
                is_recording = True
            print("Detected voice!")
            frame_count = 0
        else:
            if is_recording:
                print("No voice detected.")
                frame_count += 1

        # If recording, append the frames
        if is_recording:
            frames.append(chunk)

        # Check for maximum silence
        if frame_count > max_silence and is_recording:
            print("Max silence reached, stopping.")
            break

    # Close and terminate everything properly
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio to file
    if frames:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()


def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    audio = AudioSegment.from_file(audio_file_path, format="wav")
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text, len(text.split())
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio.", 4
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}", 4


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


def play_text_as_audio(text, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def get_loudness(file_path):
    data, sample_rate = sf.read(file_path)
    rms = (data**2).mean()**0.5
    loudness = 20 * np.log10(rms)
    duration = len(data) / sample_rate
    return loudness, duration


if __name__ == "__main__":
    while True:
        filename = "test"
        record_voice()

        audio_file_path = "voice.wav"
        loudness, duration = get_loudness(audio_file_path)
        print("Average Loudness:", loudness)
        print("Duration:", duration)
        text, length = audio_to_text(audio_file_path)
        print(f"Transcribed text: {text}, Length: {length}")
        emotion = textToEmotion(text)
        print(f"Emotion: {emotion}")
        play_text_as_audio(emotion)
