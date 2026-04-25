"""
speaker.py — Converts text to speech using Piper TTS (runs locally, offline)
"""

import subprocess
import tempfile
import os
import sounddevice as sd
import soundfile as sf
import numpy as np

from core.config import Config


class Speaker:
    def __init__(self, config: Config):
        self.config = config
        self._check_piper()

    def _check_piper(self):
        """Check Piper executable and voice model exist."""
        try:
            result = subprocess.run(
                [self.config.PIPER_EXECUTABLE, "--version"],
                capture_output=True, text=True, timeout=5
            )
            print(f"    Piper TTS ready ✅")
        except FileNotFoundError:
            print(f"\n  ⚠️  Piper not found at '{self.config.PIPER_EXECUTABLE}'")
            print("     Download from: https://github.com/rhasspy/piper/releases")
            print("     Set PIPER_PATH env var or put piper in your system PATH\n")

        if not os.path.exists(self.config.PIPER_VOICE_PATH):
            print(f"\n  ⚠️  Voice model not found: {self.config.PIPER_VOICE_PATH}")
            print(f"     Download from: https://huggingface.co/rhasspy/piper-voices")
            print(f"     Place the .onnx and .onnx.json files in the voices/ folder\n")

    def speak(self, text: str):
        """
        Convert text to speech using Piper and play it through speakers.
        Falls back to printing if Piper is not available.
        """
        if not text or not text.strip():
            return

        # Clean text for TTS — remove markdown artifacts
        clean = self._clean_text(text)

        # Try Piper first
        success = self._speak_piper(clean)

        # Fallback: print only (no audio)
        if not success:
            print(f"  [TTS fallback — install Piper to hear audio]")

    def _speak_piper(self, text: str) -> bool:
        """Run Piper TTS and play audio output."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as out_file:
            out_path = out_file.name

        try:
            cmd = [
                self.config.PIPER_EXECUTABLE,
                "--model", self.config.PIPER_VOICE_PATH,
                "--output_file", out_path,
            ]

            proc = subprocess.run(
                cmd,
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=30
            )

            if proc.returncode != 0:
                return False

            # Play the generated audio
            audio, sample_rate = sf.read(out_path)
            sd.play(audio, sample_rate)
            sd.wait()
            return True

        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"  TTS error: {e}")
            return False
        finally:
            if os.path.exists(out_path):
                os.unlink(out_path)

    def _clean_text(self, text: str) -> str:
        """Remove markdown and clean text for natural TTS output."""
        import re
        text = re.sub(r'\*+', '', text)          # remove bold/italic
        text = re.sub(r'#+\s*', '', text)         # remove headers
        text = re.sub(r'`[^`]*`', '', text)       # remove code blocks
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # links → text
        text = re.sub(r'\s+', ' ', text).strip()
        return text
