"""
brain.py — Fixed: system prompt injection, NameError, bare except, dead import
"""

import requests
import ollama
from collections import deque

from core.news import get_latest_news
from core.memory import get_memory, add_to_memory, get_user_profile
from core.config import Config


class Brain:
    def __init__(self, config: Config):
        self.config = config
        self._check_ollama()
        # Don't add system prompt to memory — pass it separately to ollama

    def _check_ollama(self):
        try:
            r = requests.get(f"{self.config.OLLAMA_HOST}/api/tags", timeout=5)
            r.raise_for_status()
            models = [m["name"] for m in r.json().get("models", [])]
            model_base = self.config.OLLAMA_MODEL.split(":")[0]
            if not any(model_base in m for m in models):
                print(f"\n⚠️  Model '{self.config.OLLAMA_MODEL}' not found.")
                print(f"    Run: ollama pull {self.config.OLLAMA_MODEL}\n")
            else:
                print(f"    Ollama connected, model '{self.config.OLLAMA_MODEL}' ready ✅")
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Ollama not reachable: {e}")
            print("    Start it with: ollama serve\n")
            raise SystemExit(1)

    def analyze_screen(self, image_path: str) -> str:
        response = ollama.chat(
            model="llava",
            messages=[{
                "role": "user",
                "content": "Explain what is on this screen in simple terms.",
                "images": [image_path]
            }]
        )
        return response["message"]["content"]

    def respond(self, user_input: str) -> str:
        memory  = get_memory()
        profile = get_user_profile()

        # Start from base system prompt
        system = self.config.SYSTEM_PROMPT

        # Inject news if relevant
        if "news" in user_input.lower():
            try:
                news = get_latest_news()
                system += f"\n\nLatest News:\n{news}"
            except Exception:
                pass  # news fetch optional — don't crash

        # Debate mode
        if "debate" in user_input.lower():
            system += "\n\nDEBATE MODE: Challenge strongly, use logic, don't agree easily."

        messages = [
            {"role": "system", "content": system},
            *memory,
            {"role": "user", "content": user_input}
        ]

        response = ollama.chat(
            model=self.config.OLLAMA_MODEL,
            messages=messages,
            options={
                "temperature": self.config.OLLAMA_TEMPERATURE,
                "num_predict": self.config.OLLAMA_MAX_TOKENS,
            }
        )

        reply = response["message"]["content"]

        add_to_memory("user", user_input)
        add_to_memory("assistant", reply)

        return reply
