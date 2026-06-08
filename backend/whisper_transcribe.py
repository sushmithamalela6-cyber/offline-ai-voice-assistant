from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    "voice.wav"
)

print("\nTranscription:")

for segment in segments:
    print(segment.text)