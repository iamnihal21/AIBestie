"""
config.py — All settings in one place. Edit this to customize your assistant.
"""

import os

class Config:
    # ── Ollama (AI Brain) ─────────────────────────────────────────
    OLLAMA_HOST        = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL       = os.getenv("OLLAMA_MODEL", "llama3.2")   # or "mistral", "gemma2"
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.85"))
    OLLAMA_MAX_TOKENS  = int(os.getenv("OLLAMA_MAX_TOKENS", "300"))

    # ── Whisper (Speech → Text) ───────────────────────────────────
    # Sizes: tiny | base | small | medium | large
    # tiny=fastest, large=most accurate. Start with "base".
    WHISPER_MODEL      = os.getenv("WHISPER_MODEL", "tiny")
    WHISPER_LANGUAGE   = os.getenv("WHISPER_LANGUAGE", "en")   # "hi" for Hindi, None for auto

    # ── Piper (Text → Speech) ─────────────────────────────────────
    # Download voices from: https://huggingface.co/rhasspy/piper-voices
    PIPER_EXECUTABLE   = os.getenv("PIPER_PATH", "piper")      # full path if not in PATH
    PIPER_VOICE        = os.getenv("PIPER_VOICE", "en_US-amy-medium")
    PIPER_VOICE_PATH   = os.getenv("PIPER_VOICE_PATH", "voices/en_US-amy-medium.onnx")

    # ── Wake Word ─────────────────────────────────────────────────
    WAKE_WORD          = os.getenv("WAKE_WORD", "hey bestie")
    WAKE_SENSITIVITY   = float(os.getenv("WAKE_SENSITIVITY", "0.6"))   # 0.0–1.0

    # ── Audio ─────────────────────────────────────────────────────
    SAMPLE_RATE        = 16000
    CHANNELS           = 1
    SILENCE_THRESHOLD  = float(os.getenv("SILENCE_THRESHOLD", "0.01"))
    SILENCE_DURATION   = float(os.getenv("SILENCE_DURATION", "1.5"))   # seconds of silence = end of speech
    MAX_RECORD_SECONDS = int(os.getenv("MAX_RECORD_SECONDS", "30"))

    # ── Personality ───────────────────────────────────────────────
    USER_NAME          = os.getenv("USER_NAME", "friend")
    USER_CITY          = os.getenv("USER_CITY", "Ahmedabad")

    SYSTEM_PROMPT = f"""You are Bestie, a friendly AI assistant. Talk casually like a real friend. 
User is {USER_NAME} from {USER_CITY}, India. Keep replies under 2 sentences. No markdown."""
