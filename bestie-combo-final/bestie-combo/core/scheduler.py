import threading
import time
from datetime import datetime
from core.reminder import get_pending, mark_done

class Scheduler:
    def __init__(self, speaker):
        self.speaker = speaker
        self._running = False

    def start(self):
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self._running:
            now = datetime.now().strftime("%H:%M")

            for r in get_pending():
                if r["time"] == now:
                    self.speaker.speak(f"Reminder: {r['text']}")
                    mark_done(r)

            time.sleep(30)

    def stop(self):
        self._running = False