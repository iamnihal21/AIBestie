"""
speaker.py — Fixed: safe stream wait, no RuntimeError on fast audio
"""

import subprocess
import tempfile
import os
import re
import threading
import sounddevice as sd
import soundfile as sf

from core.config import Config


class Speaker:
    def __init__(self, config: Config):
        self.config       = config
        self._speech_thread = None
        self._stop_flag   = threading.Event()
        self._check_piper()

    def _check_piper(self):
        try:
            subprocess.run(
                [self.config.PIPER_EXECUTABLE, "--version"],
                capture_output=True, timeout=5
            )
            print("    Piper TTS ready ✅")
        except Exception:
            print("⚠️  Piper not found — voice output disabled.")

    def speak(self, text: str, emotion: str = "neutral"):
        if not text or not text.strip():
            return
        self.stop()                         # cancel any ongoing speech
        clean = self._clean_text(text)
        self._stop_flag.clear()
        self._speech_thread = threading.Thread(
            target=self._speak_piper,
            args=(clean, emotion),
            daemon=True
        )
        self._speech_thread.start()

    def wait(self):
        """Block until current speech finishes (call before next listen cycle)."""
        if self._speech_thread and self._speech_thread.is_alive():
            self._speech_thread.join()

    def stop(self):
        self._stop_flag.set()
        sd.stop()
        if self._speech_thread and self._speech_thread.is_alive():
            self._speech_thread.join(timeout=1)

    def _speak_piper(self, text: str, emotion: str):
        length_scale = {"excited": "0.85", "calm": "1.1", "serious": "0.95"}.get(emotion, "1.0")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            out_path = f.name

        try:
            cmd = [
                self.config.PIPER_EXECUTABLE,
                "--model",        self.config.PIPER_VOICE_PATH,
                "--output_file",  out_path,
                "--length_scale", length_scale,
            ]
            proc = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True)
            if proc.returncode != 0 or self._stop_flag.is_set():
                return

            audio, sr = sf.read(out_path)
            if self._stop_flag.is_set():
                return

            sd.play(audio, sr)

            # Safe wait: poll stop flag instead of checking stream.active
            while sd.get_stream().active if self._is_stream_active() else False:
                if self._stop_flag.wait(timeout=0.05):
                    sd.stop()
                    break

            sd.wait()   # final drain

        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            if os.path.exists(out_path):
                os.unlink(out_path)

    def _is_stream_active(self) -> bool:
        try:
            return sd.get_stream().active
        except Exception:
            return False

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`[^`]*`', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        return re.sub(r'\s+', ' ', text).strip()
