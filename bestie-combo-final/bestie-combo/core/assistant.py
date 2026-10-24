"""
assistant.py — STT → Intent → Tools → Agent → TTS
Updated: Oracle+Groq brain, screen vision injected, scheduler wired
"""

import datetime
import re
import json
import logging

from core.config import Config
from core.listener import Listener
from core.transcriber import Transcriber
from core.brain import Brain
from core.speaker import Speaker
from core.utils import print_status, print_user, print_bestie
from core.reminder import get_pending, add_reminder
from core.calender_service import CalendarService
from core.system_control import SystemControl
from core.browser import Browser
from core.screen import ScreenAnalyzer
from core.scheduler import Scheduler

logger = logging.getLogger(__name__)

STOP_COMMANDS = {
    "stop bestie", "sleep bestie",
    "exit bestie", "shutdown", "go to sleep"
}

INTENT_MAP = [
    ("reminder",     ["remind me", "set reminder", "reminder", "notify me"]),
    ("calendar",     ["schedule", "meeting", "appointment", "event",
                      "book", "set meeting", "add event", "plan meeting"]),
    ("get_calendar", ["my schedule", "today plan", "what's my plan",
                      "calendar", "events", "today's events"]),
    ("type",         ["write this"]),
    ("screen",       ["analyze screen", "what is on screen",
                      "read screen", "screen content"]),
    ("search",       ["search", "google", "look up", "find on internet"]),
]


class BestieAssistant:
    def __init__(self, config: Config):
        self.config = config
        self._running = False
        self._controller = None

        print_status("Loading Whisper (local)...")
        self.transcriber = Transcriber(config)

        print_status("Connecting to AI brain (Oracle VM + Groq)...")
        self.brain = Brain(config)

        print_status("Setting up TTS (local Piper)...")
        self.speaker = Speaker(config)

        print_status("Starting microphone listener...")
        self.listener = Listener(config)

        self.calendar = CalendarService()
        self.system = SystemControl()
        self.browser = Browser()

        # Screen analyzer — inject brain for Groq vision
        self.screen = ScreenAnalyzer()
        self.screen.set_brain(self.brain)

        # Wire up scheduler so reminders actually fire
        self.scheduler = Scheduler(self.speaker)
        self.scheduler.start()

        print_status("All systems ready! ✅\n")

    @property
    def controller(self):
        if self._controller is None:
            from core.controller import Controller
            self._controller = Controller()
        return self._controller

    # =====================================================
    # 🧠 DATETIME PARSER
    # =====================================================
    def extract_datetime(self, text: str):
        text = text.lower()
        date = datetime.date.today()

        if "tomorrow" in text or "next day" in text:
            date += datetime.timedelta(days=1)

        natural = {
            "morning":   (9,  0),
            "afternoon": (15, 0),
            "evening":   (18, 0),
            "night":     (21, 0),
        }
        for word, (h, m) in natural.items():
            if word in text:
                return datetime.datetime.combine(date, datetime.time(h, m))

        match_24 = re.search(r"\b(\d{3,4})\b", text)
        if match_24:
            val = match_24.group(1)
            hour = int(val[:-2]) if len(val) == 4 else int(val[0])
            mins = int(val[-2:])
            if 0 <= hour <= 23 and 0 <= mins <= 59:
                return datetime.datetime.combine(date, datetime.time(hour, mins))

        match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", text)
        if not match:
            return None

        hour = int(match.group(1))
        mins = int(match.group(2) or 0)
        ampm = match.group(3)

        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0

        if not (0 <= hour <= 23 and 0 <= mins <= 59):
            return None

        return datetime.datetime.combine(date, datetime.time(hour, mins))

    # =====================================================
    # 🎯 INTENT DETECTOR
    # =====================================================
    def detect_intent(self, text: str) -> str:
        lowered = text.lower()
        if lowered.startswith("type "):
            return "type"
        for intent, keywords in INTENT_MAP:
            if any(kw in lowered for kw in keywords):
                return intent
        return "agent"

    # =====================================================
    # 🤖 AGENT LOOP
    # =====================================================
    _AGENT_SYSTEM = """You control a PC. Given a task, return ONE JSON action:
{"action": "search_google"|"open_website"|"analyze_screen"|"click"|"type"|"respond", "input": "..."}
Return ONLY valid JSON. No explanation."""

    _VALID_ACTIONS = {
        "search_google", "open_website", "analyze_screen",
        "click", "type", "respond"
    }

    def agent_loop(self, task: str) -> str:
        context = task

        for step in range(3):
            result = "No action executed"
            raw = self.brain.respond(
                f"{self._AGENT_SYSTEM}\n\nTask: {context}"
            )

            try:
                clean = re.sub(r"```(?:json)?|```", "", raw).strip()
                step_data = json.loads(clean)
            except json.JSONDecodeError:
                return raw.strip()

            action = step_data.get("action", "")
            inp = step_data.get("input", "")

            if action not in self._VALID_ACTIONS:
                return "I'm not sure how to do that."

            try:
                if action == "search_google":
                    self.browser.search_google(inp)
                    result = f"Searched for '{inp}'"
                elif action == "open_website":
                    self.browser.open_url(inp)
                    result = f"Opened {inp}"
                elif action == "analyze_screen":
                    result = self.screen.analyze()
                elif action == "click":
                    x, y = (int(v) for v in inp.split())
                    self.controller.click(x, y)
                    result = f"Clicked ({x}, {y})"
                elif action == "type":
                    self.controller.type_text(inp)
                    result = f"Typed: {inp}"
                elif action == "respond":
                    return inp

            except ValueError:
                return "I couldn't parse those coordinates."
            except Exception as e:
                logger.error("Agent action '%s' failed: %s", action, e)
                if "not found" in str(e) or "404" in str(e):
                    return f"Required model not installed. Check your setup."
                result = f"Action failed: {e}"

            context = f"Last result: {result}. Original task: {task}. Continue."

        return "I tried but couldn't complete that fully. Check logs for details."

    # =====================================================
    # 🎯 INTENT HANDLERS
    # =====================================================
    def _handle_reminder(self, text: str) -> str:
        dt = self.extract_datetime(text)
        if not dt:
            return "Tell me the time clearly — like 'at 3pm' or 'at 1700'."
        match = re.search(r"remind me to (.+?)(?:\s+at\s+|$)", text)
        task = match.group(1).strip() if match else "something"
        add_reminder(task, dt.strftime("%H:%M"))
        return f"I'll remind you to {task} at {dt.strftime('%I:%M %p')}."

    def _handle_calendar_add(self, text: str) -> str:
        dt = self.extract_datetime(text)
        if not dt:
            return "Tell me the time clearly."
        match = re.search(
            r"(?:schedule|meeting|appointment|event)\s+(.+?)(?:\s+at\s+|$)", text)
        title = match.group(1).strip() if match else "Meeting"
        start = dt.isoformat()
        end = (dt + datetime.timedelta(hours=1)).isoformat()
        self.calendar.add_event(title, start, end)
        return f"Scheduled '{title}' at {dt.strftime('%I:%M %p')}."

    def _handle_calendar_get(self) -> str:
        events = self.calendar.get_today_events()
        if not events:
            return "You have nothing scheduled today."
        titles = ", ".join(e["summary"] for e in events)
        return f"Your events today: {titles}."

    def _handle_type(self, text: str) -> str:
        content = re.sub(r"^(type|write this)\s*",
                         "", text, flags=re.I).strip()
        if not content:
            return "What should I type?"
        self.controller.type_text(content)
        print(f"⌨️  Typed: {content}")
        return f"Typing: {content}."

    def _handle_screen(self) -> str:
        result = self.screen.analyze()
        print_bestie(result)
        return result

    def _handle_search(self, text: str) -> str:
        match = re.search(
            r"(?:search|google|look up)(?:\s+for)?\s+(.+)", text, re.I)
        if not match:
            return "What should I search for?"
        query = match.group(1).strip()
        self.browser.search_google(query)
        return f"Searching for '{query}'."

    # =====================================================
    # 🚀 MAIN LOOP
    # =====================================================
    def run(self):
        self._running = True
        active_mode = False

        while self._running:
            if not active_mode:
                print(f"\n👂  Say '{self.config.WAKE_WORD}' to wake me up.")
                audio = self.listener.wait_for_wake_word_then_record()
                if audio is None:
                    continue
                active_mode = True
                self.speaker.speak("Yes, I'm listening.")
            else:
                print("🎙️  Listening...")
                audio = self.listener.record_direct()
                if audio is None:
                    continue

            print_status("Transcribing...")
            user_text = self.transcriber.transcribe(audio)

            if not user_text or len(user_text.strip()) < 2:
                continue

            print_user(user_text)
            lowered = user_text.lower().strip()

            if any(cmd in lowered for cmd in STOP_COMMANDS):
                active_mode = False
                self.speaker.speak("Okay, I'll wait.")
                continue

            intent = self.detect_intent(lowered)

            try:
                if intent == "reminder":
                    response = self._handle_reminder(lowered)
                elif intent == "calendar":
                    response = self._handle_calendar_add(lowered)
                elif intent == "get_calendar":
                    response = self._handle_calendar_get()
                elif intent == "type":
                    response = self._handle_type(lowered)
                elif intent == "screen":
                    response = self._handle_screen()
                elif intent == "search":
                    response = self._handle_search(lowered)
                else:
                    print_status("Thinking (Agent)...")
                    response = self.agent_loop(user_text)

            except Exception as e:
                logger.error("Handler '%s' raised: %s", intent, e)
                response = "Something went wrong. Try again?"

            print_bestie(response)
            self.speaker.speak(response)
            print()

    def stop(self):
        self._running = False
        self.listener.stop()
