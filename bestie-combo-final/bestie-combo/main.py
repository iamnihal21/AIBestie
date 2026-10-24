"""
main.py — Bestie Voice AI
Loads .env automatically, boots full Oracle+Groq pipeline
"""

import sys
import signal
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

from core.assistant import BestieAssistant
from core.config import Config


def main():
    config    = Config()
    assistant = BestieAssistant(config)

    def shutdown(sig, frame):
        print("\n\n👋 Bestie signing off. See ya!")
        assistant.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    print("=" * 52)
    print("  🎙️  Bestie Voice AI — Oracle + Groq Edition")
    print("=" * 52)
    print(f"  Brain mode : {config.BRAIN_MODE}")
    # print(f"  Brain  : {config.G}")
    print(f"  Groq model : {config.GROQ_MODEL}")
    print(f"  STT        : Whisper {config.WHISPER_MODEL} (local)")
    print(f"  TTS        : Piper {config.PIPER_VOICE} (local)")
    print(f"  Wake word  : '{config.WAKE_WORD}'")
    print("=" * 52)
    print("  Say the wake word to start!\n")

    assistant.run()


if __name__ == "__main__":
    main()
