"""
text_mode.py — Chat with Bestie in text only (no mic/speaker needed).
Great for testing your Ollama setup before adding voice.

Run: python text_mode.py
"""

from core.config import Config
from core.brain import Brain
from core.utils import print_bestie, print_status

def main():
    config = Config()

    print("=" * 50)
    print("  💬  Bestie AI — Text Mode (no mic needed)")
    print("=" * 50)
    print("  Type your message and press Enter.")
    print("  Type 'clear' to reset memory.")
    print("  Type 'quit' or Ctrl+C to exit.\n")

    print_status("Connecting to Ollama...")
    brain = Brain(config)
    print()

    while True:
        try:
            user_input = input("  🧑 You    : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Bye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("\n👋 Bye!")
            break
        if user_input.lower() == "clear":
            brain.clear_memory()
            print("  🧹 Memory cleared!\n")
            continue

        print_status("Thinking...")
        response = brain.respond(user_input)
        print_bestie(response)
        print()

if __name__ == "__main__":
    main()
