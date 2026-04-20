import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

# charger modèle
model = Model("model")
rec = KaldiRecognizer(model, 16000)

print("🎤 Test Vosk actif (parle...)")

with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):
    while True:
        data = q.get()

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            print("🟢 reconnu :", text)