"""
brain.py — Talks to Ollama local LLM. Keeps conversation history (memory).
"""

import requests
import json
from core.config import Config


class Brain:
    def __init__(self, config: Config):
        self.config = config
        self.history = []   # conversation memory
        self._check_ollama()

    def _check_ollama(self):
        """Verify Ollama is running and the model is available."""
        try:
            r = requests.get(f"{self.config.OLLAMA_HOST}/api/tags", timeout=5)
            models = [m["name"] for m in r.json().get("models", [])]
            model_base = self.config.OLLAMA_MODEL.split(":")[0]
            available = any(model_base in m for m in models)

            if not available:
                print(f"\n  ⚠️  Model '{self.config.OLLAMA_MODEL}' not found in Ollama.")
                print(f"     Run: ollama pull {self.config.OLLAMA_MODEL}")
                print(f"     Available models: {models}\n")
            else:
                print(f"    Ollama connected, model '{self.config.OLLAMA_MODEL}' ready ✅")

        except requests.exceptions.ConnectionError:
            print("\n  ❌ Ollama not running! Start it with: ollama serve")
            print("     Then re-run this script.\n")
            raise SystemExit(1)

    def respond(self, user_message: str) -> str:
        """
        Send message to Ollama, get response. Maintains conversation history.
        """
        self.history.append({"role": "user", "content": user_message})

        # Keep last 20 messages to avoid context overflow
        recent_history = self.history[-6:]

        payload = {
            "model": self.config.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": self.config.SYSTEM_PROMPT},
                *recent_history
            ],
            "stream": False,
            "options": {
                "temperature": self.config.OLLAMA_TEMPERATURE,
                "num_predict": self.config.OLLAMA_MAX_TOKENS,
            }
        }

        try:
            response = requests.post(
                f"{self.config.OLLAMA_HOST}/api/chat",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            reply = data.get("message", {}).get("content", "").strip()

            if reply:
                self.history.append({"role": "assistant", "content": reply})

            return reply

        except requests.exceptions.Timeout:
            return "Hmm, I'm thinking too hard. Ask me again?"
        except Exception as e:
            return f"Got an error talking to my brain: {str(e)[:80]}"

    def clear_memory(self):
        """Reset conversation history."""
        self.history = []
        return "Memory cleared! Fresh start."
