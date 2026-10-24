"""
screen.py — GNOME Wayland safe capture + Groq Vision + OCR fallback
"""

import os
import time
from PIL import Image
import pytesseract


class ScreenAnalyzer:

    def __init__(self):
        self._brain = None  # injected from assistant

    def set_brain(self, brain):
        self._brain = brain

    # =====================================================
    # 📸 GNOME WAYLAND SCREEN CAPTURE
    # =====================================================
    def capture(self) -> str:
        """
        Capture screen using gnome-screenshot (Wayland-safe)
        """
        path = "/tmp/bestie_screen.png"

        try:
            # Take screenshot
            exit_code = os.system(f"gnome-screenshot -f {path}")

            if exit_code != 0:
                raise RuntimeError("gnome-screenshot command failed")

            # Ensure file is written
            time.sleep(0.4)

            if not os.path.exists(path) or os.path.getsize(path) == 0:
                raise RuntimeError("Screenshot failed or empty")

            # ✅ Optimize image (important for Groq)
            self._optimize_image(path)

            return path

        except Exception as e:
            raise RuntimeError(f"Screen capture failed: {str(e)}")

    # =====================================================
    # 🧠 ANALYSIS PIPELINE
    # =====================================================
    def analyze(self) -> str:
        """
        Capture → Groq Vision → fallback OCR
        """
        try:
            path = self.capture()
        except Exception as e:
            return str(e)

        # 🥇 Groq Vision
        if self._brain:
            try:
                result = self._brain.analyze_screen(path)

                if result and not self._is_bad_result(result):
                    return result

            except Exception as e:
                print("⚠️ Vision failed:", e)

        # 🥈 OCR fallback
        return self._ocr_fallback(path)

    # =====================================================
    # ⚡ IMAGE OPTIMIZATION
    # =====================================================
    def _optimize_image(self, path: str):
        """
        Resize image for faster + better AI processing
        """
        try:
            img = Image.open(path)

            # Resize to reasonable size
            img.thumbnail((1280, 720))

            img.save(path, quality=85)

        except Exception:
            pass  # don't break if optimization fails

    # =====================================================
    # 🚫 FILTER BAD AI OUTPUT
    # =====================================================
    def _is_bad_result(self, text: str) -> bool:
        text = text.lower()

        bad_patterns = [
            "black rectangle",
            "blank screen",
            "no visible content",
            "solid black",
        ]

        return any(p in text for p in bad_patterns)

    # =====================================================
    # 🔍 OCR FALLBACK
    # =====================================================
    def _ocr_fallback(self, path: str) -> str:
        try:
            img = Image.open(path)

            # Improve OCR accuracy
            img = img.convert("L")

            text = pytesseract.image_to_string(img)

            if not text.strip():
                return "I couldn't detect any readable text on the screen."

            return f"📄 Screen text:\n{text.strip()}"

        except Exception as e:
            return f"OCR failed: {str(e)}"