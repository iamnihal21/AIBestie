import mss
from PIL import Image
import os

class ScreenAnalyzer:

    def capture(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            path = "/tmp/screen.png"
            img.save(path)

            return path