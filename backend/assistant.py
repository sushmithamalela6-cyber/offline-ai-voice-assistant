import queue
import tempfile
import sounddevice as sd
import pyttsx3
import threading

from ollama import chat
from faster_whisper import WhisperModel
from scipy.io.wavfile import write

speech_lock = threading.Lock()
# =========================
# LOAD WHISPER MODEL
# =========================

print("Loading Whisper...")

whisper_model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper Loaded Successfully")

# =========================
# AUDIO QUEUE
# =========================

q = queue.Queue()

# =========================
# TTS ENGINE
# =========================


# =========================
# SPEECH TO TEXT
# =========================

def get_voice_input():

    try:

        fs = 16000

        print("\n🎤 Speak now (5 seconds)...")

        audio = sd.rec(
            int(5 * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        write(
            temp_file.name,
            fs,
            audio
        )

        segments, info = whisper_model.transcribe(
            temp_file.name
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        print("You Said:", text)

        return text.lower()

    except Exception as e:

        print("Speech Recognition Error:", e)

        return ""

# =========================
# OLLAMA AI RESPONSE
# =========================

def generate_reply(text):

    try:

        print("\nUsing Model: phi3:mini")

        response = chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an offline AI voice assistant. "
                    "Give short and direct answers in 2-3 sentences."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        reply = response["message"]["content"]

        reply = reply.replace("\n\n", "\n")
        reply = " ".join(reply.split())

        print("\nAI Reply:", reply)

        return reply

    except Exception as e:

        print("Ollama Error:", e)

        return "Sorry, I could not generate a response."

# =========================
# TEXT TO SPEECH
# =========================

def speak_text(text):

    try:

        engine = pyttsx3.init("sapi5")

        voices = engine.getProperty("voices")

        engine.setProperty("voice", voices[1].id)

        engine.setProperty("rate", 150)

        engine.setProperty("volume", 1.0)

        print("🔊 Speaking...")

        engine.say(text)

        engine.runAndWait()

        engine.stop()

        print("✅ Speech Completed")

    except Exception as e:

        print("Speech Error:", e)
# =========================
# STOP VOICE
# =========================

def stop_voice():

    print("⛔ Voice Stopped")