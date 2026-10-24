"""
config.py — Updated for Oracle VM + Groq API combo setup
"""
import os

class Config:
    # ── Ollama (runs on Oracle VM) ────────────────────────────────
    # Change OLLAMA_HOST to your Oracle VM's public IP after setup
    # OLLAMA_HOST        = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # OLLAMA_MODEL       = os.getenv("OLLAMA_MODEL", "llama3:8b")
    # OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.85"))
    # OLLAMA_MAX_TOKENS  = int(os.getenv("OLLAMA_MAX_TOKENS", "300"))
    OLLAMA_HOST = "REMOVED"

    # ── Groq API (cloud, biggest models + vision) ─────────────────
    GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
    GROQ_MODEL         = os.getenv("GROQ_MODEL")
    GROQ_VISION_MODEL  = os.getenv("GROQ_VISION_MODEL")

    # ── Brain mode ────────────────────────────────────────────────
    # "ollama" = always use Oracle VM
    # "groq"   = always use Groq API
    # "auto"   = try Oracle first, fallback to Groq if unreachable
    BRAIN_MODE         = os.getenv("BRAIN_MODE", "auto")

    # ── News API (newsapi.org — free tier) ────────────────────────
    NEWS_API_KEY       = os.getenv("NEWS_API_KEY", "")

    # ── Whisper (Speech → Text, runs locally on your PC) ─────────
    WHISPER_MODEL      = os.getenv("WHISPER_MODEL", "tiny")
    WHISPER_LANGUAGE   = os.getenv("WHISPER_LANGUAGE", "en")

    # ── Piper (Text → Speech, runs locally on your PC) ───────────
    PIPER_EXECUTABLE   = os.getenv("PIPER_PATH", "piper")
    PIPER_VOICE        = os.getenv("PIPER_VOICE", "en_US-lessac-medium")
    PIPER_VOICE_PATH   = os.getenv("PIPER_VOICE_PATH", "voices/en_US-lessac-medium.onnx")

    # ── Wake Word ─────────────────────────────────────────────────
    WAKE_WORD          = os.getenv("WAKE_WORD", "hey bestie")
    WAKE_SENSITIVITY   = float(os.getenv("WAKE_SENSITIVITY", "0.6"))

    # ── Audio ─────────────────────────────────────────────────────
    SAMPLE_RATE        = 16000
    CHANNELS           = 1
    SILENCE_THRESHOLD  = float(os.getenv("SILENCE_THRESHOLD", "0.01"))
    SILENCE_DURATION   = float(os.getenv("SILENCE_DURATION", "1.5"))
    MAX_RECORD_SECONDS = int(os.getenv("MAX_RECORD_SECONDS", "30"))

    # ── User Profile ──────────────────────────────────────────────
    USER_NAME = os.getenv("USER_NAME", "Nihal")
    USER_CITY = os.getenv("USER_CITY", "Ahmedabad")

    SYSTEM_PROMPT = """
You are "Bestie", a smart, proactive, and slightly witty AI assistant designed to help Nihal (a computer engineering student) manage life, productivity, and learning.

USER CONTEXT:
- Name: Nihal | CE student 3rd year | from Ahmedabad
- Interests: AI, automation, system design, building real-world projects
- Style: Likes direct answers, practical advice, no fluff

BEHAVIOR:
- Be concise but helpful
- Prefer actionable answers over theory
- Think like a smart teammate
- Slightly witty when appropriate
- Never over-explain unless asked

STRICT RULES:
- Never hallucinate fake capabilities
- If unsure, ask a short clarification question

Be useful, sharp, and real. Not robotic. Not generic.
"""
