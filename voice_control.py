import queue
import json
import threading
import pyaudio
from vosk import Model, KaldiRecognizer

class VoiceControl:
    def __init__(self):
        self.command = None
        self.q = queue.Queue()

        # modèle Vosk
        self.model = Model("model")
        self.rec = KaldiRecognizer(self.model, 16000)

        # PyAudio
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )

        self.stream.start_stream()

        # thread écoute
        self.running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def listen(self):
        while self.running:
            data = self.stream.read(4000, exception_on_overflow=False)

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text", "").lower()

                print("🎤 VOICE:", text)

                if "boost" in text:
                    self.command = "boost"
                elif "speed" in text:
                    self.command = "speed"
                elif "restart" in text:
                    self.command = "restart"
                elif "quit" in text:
                    self.command = "quit"