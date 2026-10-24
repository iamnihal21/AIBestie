"""
listener.py — Microphone input + wake word detection + conversation mode
"""

import numpy as np
import sounddevice as sd
import queue
import threading
from core.config import Config


class Listener:
    def __init__(self, config: Config):
        self.config = config
        self._stop_event = threading.Event()
        self._audio_queue = queue.Queue()

        # Test microphone on startup
        try:
            sd.query_devices(kind='input')
        except Exception as e:
            raise RuntimeError(f"No microphone found: {e}")

    # 🎙️ CORE RECORDING FUNCTION (UNCHANGED)
    def _record_audio(self, duration_seconds=None, stop_on_silence=True):
        """Record audio from mic, stop when silence detected or max duration hit."""
        frames = []
        silence_frames = 0
        max_silence = int(
            self.config.SILENCE_DURATION * self.config.SAMPLE_RATE / 512
        )
        max_frames = int(
            self.config.MAX_RECORD_SECONDS * self.config.SAMPLE_RATE / 512
        )

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy())
            rms = np.sqrt(np.mean(indata**2))
            nonlocal silence_frames
            if rms < self.config.SILENCE_THRESHOLD:
                silence_frames += 1
            else:
                silence_frames = 0

        with sd.InputStream(
            samplerate=self.config.SAMPLE_RATE,
            channels=self.config.CHANNELS,
            dtype='float32',
            blocksize=512,
            callback=callback
        ):
            while not self._stop_event.is_set():
                sd.sleep(30)

                if stop_on_silence and len(frames) > 5 and silence_frames >= max_silence:
                    break
                if len(frames) >= max_frames:
                    break

        if not frames:
            return None

        audio = np.concatenate(frames, axis=0).flatten()
        return audio

    # 🔥 NEW: Direct recording (no wake word)
    def record_direct(self):
        """
        Used in conversation mode.
        Directly records user's speech without waiting for wake word.
        """
        return self._record_audio(stop_on_silence=True)

    # 🧠 Wake word detection
    def wait_for_wake_word_then_record(self):
        """
        Listens in short chunks → detects wake word → records full command
        """
        import whisper as w
        import tempfile, soundfile as sf, os

        # Load tiny model for wake detection
        if not hasattr(self, '_wake_model'):
            self._wake_model = w.load_model("tiny.en")

        while not self._stop_event.is_set():
            # 🎧 Record short chunk
            chunk = self._record_chunk(seconds=3)
            if chunk is None:
                continue

            # 🔍 Transcribe chunk
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                sf.write(tmp.name, chunk, self.config.SAMPLE_RATE)
                result = self._wake_model.transcribe(
                    tmp.name,
                    language=self.config.WHISPER_LANGUAGE,
                    fp16=False
                )
                os.unlink(tmp.name)

            detected = result.get("text", "").lower().strip()
            wake = self.config.WAKE_WORD.lower()

            # 🔔 Wake word match (fuzzy)
            if any(w in detected for w in wake.split()):
                print(f"\n  🔔 Wake word detected! Switching to conversation mode...")
                return self._record_audio(stop_on_silence=True)

        return None

    # 🎧 Helper: fixed chunk recording
    def _record_chunk(self, seconds=3):
        """Record a fixed-length chunk."""
        frames = []
        total = int(seconds * self.config.SAMPLE_RATE / 512)

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy())

        with sd.InputStream(
            samplerate=self.config.SAMPLE_RATE,
            channels=self.config.CHANNELS,
            dtype='float32',
            blocksize=512,
            callback=callback
        ):
            count = 0
            while count < total and not self._stop_event.is_set():
                sd.sleep(30)
                count += 1

        if not frames:
            return None

        return np.concatenate(frames, axis=0).flatten()

    def stop(self):
        self._stop_event.set()