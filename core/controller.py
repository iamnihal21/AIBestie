import pyautogui
import time

class Controller:

    def click(self, x, y):
        pyautogui.click(x, y)
        return f"Clicked at {x},{y}"

    def type_text(self, text):
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def press(self, key):
        pyautogui.press(key)
        return f"Pressed {key}"

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return f"Pressed {'+'.join(keys)}"