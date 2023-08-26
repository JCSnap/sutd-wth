import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

recording = False
myrecording = None

def start_stop_recording():
  global recording, myrecording
  if not recording:
    print("Recording started. Press Enter again to stop recording.")
   
    recording = True
    
    fs = 44100  
    duration = 5
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

  else:
    print("Recording stopped.")
    recording = False
    
    fs = 44100
    write("output.wav", fs, myrecording)
    wv.write("output.mp3", myrecording, fs, sampwidth=2)

print("Press Enter to start/stop recording")  
input()
start_stop_recording()
input()  
start_stop_recording()