import os
import platform
import subprocess


class SystemControl:

    def __init__(self):
        self.os_name = platform.system()

    # 🚀 Open apps
    def open_app(self, app_name):
        app_name = app_name.lower()

        if "chrome" in app_name:
            return self._run("google-chrome")

        elif "code" in app_name or "vs code" in app_name:
            return self._run("code")

        elif "terminal" in app_name:
            return self._run("gnome-terminal")

        elif "files" in app_name or "file manager" in app_name:
            return self._run("nautilus")

        return "I don't know how to open that yet."

    # 🔊 Play music
    def play_music(self):
        return self._run("xdg-open ~/Music")

    # 📴 Shutdown
    def shutdown(self):
        return self._run("shutdown now")

    # 🔁 Restart
    def restart(self):
        return self._run("reboot")

    # 🧠 Core runner
    def _run(self, command):
        try:
            subprocess.Popen(command.split())
            return "Done."
        except Exception as e:
            return f"Error: {e}"