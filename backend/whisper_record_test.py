import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000

print("Speak for 5 seconds...")

audio = sd.rec(
    int(5 * fs),
    samplerate=fs,
    channels=1,
    dtype="int16"
)

sd.wait()

write("voice.wav", fs, audio)

print("Saved voice.wav")