"""
memory.py — Fixed: O(1) deque, thread-safe, auto-eviction
"""

import threading
from collections import deque

_lock        = threading.Lock()
_memory      = deque(maxlen=20)   # auto-evicts oldest, O(1) append/pop

user_profile = {
    "name":      "Nihal",
    "goals":     ["learn AI", "build projects"],
    "habits":    ["walking daily"],
    "interests": ["technology", "AI"]
}

def add_to_memory(role: str, content: str):
    with _lock:
        _memory.append({"role": role, "content": content})

def get_memory() -> list:
    with _lock:
        return list(_memory)

def get_user_profile() -> dict:
    return user_profile

def clear_memory():
    with _lock:
        _memory.clear()
