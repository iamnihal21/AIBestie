"""
assistant.py — Orchestrates STT → LLM → TTS pipeline
"""

import time
from core.config import Config
from core.listener import Listener
from core.transcriber import Transcriber
from core.brain import Brain
from core.speaker import Speaker
from core.utils import print_status, print_user, print_bestie

class BestieAssistant:
    def __init__(self, config: Config):
        self.config = config
        self._running = False

        print_status("Loading speech-to-text (Whisper)...")
        self.transcriber = Transcriber(config)

        print_status("Connecting to Ollama AI brain...")
        self.brain = Brain(config)

        print_status("Setting up voice (Piper TTS)...")
        self.speaker = Speaker(config)

        print_status("Starting microphone listener...")
        self.listener = Listener(config)

        print_status("All systems ready! ✅\n")

    def run(self):
        self._running = True

        while self._running:
            # Step 1: Wait for wake word / just listen
            print(f"  👂 Listening... (say '{self.config.WAKE_WORD}')")
            audio_data = self.listener.wait_for_wake_word_then_record()

            if audio_data is None:
                continue

            # Step 2: Transcribe speech → text
            print_status("Transcribing...")
            user_text = self.transcriber.transcribe(audio_data)

            if not user_text or len(user_text.strip()) < 2:
                print("  (nothing detected, listening again...)\n")
                continue

            print_user(user_text)

            # Step 3: Get AI response
            print_status("Thinking...")
            response = self.brain.respond(user_text)

            if not response:
                response = "Sorry, I didn't get that. Try again?"

            print_bestie(response)

            # Step 4: Speak the response
            self.speaker.speak(response)
            print()

    def stop(self):
        self._running = False
        self.listener.stop()
