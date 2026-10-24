"""
transcriber.py — Converts audio to text using OpenAI Whisper (runs locally)
"""

import numpy as np
import tempfile
import os
import soundfile as sf
import whisper

from core.config import Config


class Transcriber:
    def __init__(self, config: Config):
        self.config = config
        print(f"    Loading Whisper '{config.WHISPER_MODEL}' model...")
        self.model = whisper.load_model(config.WHISPER_MODEL, device="cpu")
        print(f"    Whisper ready ✅")

    def transcribe(self, audio: np.ndarray) -> str:
        """
        Takes a float32 numpy audio array, returns transcribed text string.
        """
        if audio is None or len(audio) == 0:
            return ""

        # Whisper expects a .wav file or float32 numpy array
        # Writing to temp file is most reliable cross-platform
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio, self.config.SAMPLE_RATE)
            tmp_path = tmp.name

        try:
            result = self.model.transcribe(
                tmp_path,
                language=self.config.WHISPER_LANGUAGE,
                fp16=False,                   # fp16=True if you have NVIDIA GPU
                temperature=0.0,              # 0 = deterministic, best for commands
                condition_on_previous_text=False,
            )
            text = result.get("text", "").strip()

            # Remove common Whisper hallucinations on silence
            hallucinations = [
                "thank you", "thanks for watching", "you",
                "bye", ".", "", "the", "a"
            ]
            if text.lower() in hallucinations:
                return ""

            return text

        finally:
            os.unlink(tmp_path)
