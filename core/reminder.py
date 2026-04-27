"""
reminder.py — Fixed: thread-safe file access with Lock
"""

import json
import os
import threading
from datetime import datetime

REMINDER_FILE = "data/reminders.json"
_lock = threading.Lock()

def _load() -> list:
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, "r") as f:
        return json.load(f)

def _save(data: list):
    os.makedirs("data", exist_ok=True)
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_reminder(text: str, time_str: str):
    with _lock:
        reminders = _load()
        reminders.append({"text": text, "time": time_str, "done": False})
        _save(reminders)

def get_pending() -> list:
    with _lock:
        return [r for r in _load() if not r["done"]]

def mark_done(reminder: dict):
    with _lock:
        reminders = _load()
        for r in reminders:
            if r["text"] == reminder["text"] and r["time"] == reminder["time"]:
                r["done"] = True
        _save(reminders)
