from groq import Groq
from core.memory import get_memory, add_to_memory, get_user_profile
from core.config import Config
import base64

class Brain:
    def __init__(self, config: Config):
        self.config = config
        self.client = Groq(api_key=config.GROQ_API_KEY)

        print("    Groq connected ✅")

    # ==============================
    # 🧠 TEXT RESPONSE (MAIN BRAIN)
    # ==============================
    def respond(self, user_input: str) -> str:
        memory = get_memory()
        system = self.config.SYSTEM_PROMPT

        messages = [
            {"role": "system", "content": system},
            *memory,
            {"role": "user", "content": user_input}
        ]

        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",   # 🔥 BIG MODEL
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        reply = completion.choices[0].message.content

        add_to_memory("user", user_input)
        add_to_memory("assistant", reply)

        return reply

    # ==============================
    # 👁️ SCREEN ANALYSIS (VISION)
    # ==============================
    from groq import Groq
from core.memory import get_memory, add_to_memory, get_user_profile
from core.config import Config
import base64

class Brain:
    def __init__(self, config: Config):
        self.config = config
        self.client = Groq(api_key=config.GROQ_API_KEY)

        print("    Groq connected ✅")

    # ==============================
    # 🧠 TEXT RESPONSE (MAIN BRAIN)
    # ==============================
    def respond(self, user_input: str) -> str:
        memory = get_memory()
        system = self.config.SYSTEM_PROMPT

        messages = [
            {"role": "system", "content": system},
            *memory,
            {"role": "user", "content": user_input}
        ]

        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",   # 🔥 BIG MODEL
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        reply = completion.choices[0].message.content

        add_to_memory("user", user_input)
        add_to_memory("assistant", reply)

        return reply

    # ==============================
    # 👁️ SCREEN ANALYSIS (VISION)
    # ==============================
    def analyze_screen(self, image_path):
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        completion = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this screen in detail."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
            max_tokens=500,
        )

        return completion.choices[0].message.content