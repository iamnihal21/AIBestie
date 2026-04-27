"""
Bestie Voice AI — Local Voice Assistant
Run: python main.py
"""

import sys
import ollama
import signal
from core.assistant import BestieAssistant
from core.config import Config

def main():
    config = Config()
    assistant = BestieAssistant(config)

    def shutdown(sig, frame):
        print("\n\n👋 Bestie signing off. See ya!")
        assistant.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    print("=" * 50)
    print("  🎙️  Bestie Voice AI — Local & 100% Free")
    print("=" * 50)
    print(f"  Model  : {config.OLLAMA_MODEL}")
    print(f"  STT    : {config.WHISPER_MODEL} whisper")
    print(f"  TTS    : Piper ({config.PIPER_VOICE})")
    print(f"  Wake   : '{config.WAKE_WORD}'")
    print("=" * 50)
    print("  Say the wake word to start talking!")
    print("  Ctrl+C to exit\n")

    assistant.run()

if __name__ == "__main__":
    main()
