import speech_recognition as sr
import threading

class VoiceControl:
    def __init__(self):
        self.command = None
        self.recognizer = sr.Recognizer()
        self.running = True

        thread = threading.Thread(target=self.listen_loop)
        thread.daemon = True
        thread.start()

    def listen_loop(self):
        try:
            mic = sr.Microphone()
        except:
            print("⚠️ Micro non détecté")
            return

        while self.running:
            try:
                with mic as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=2)

                text = self.recognizer.recognize_google(audio).lower()
                print("🎤", text)
                self.command = text

            except:
                self.command = None