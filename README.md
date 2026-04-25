# 🎙️ Bestie Voice AI
**A 100% free, fully local AI voice assistant. No cloud. No subscriptions. No data leaving your PC.**

---

## 📁 Folder Structure

```
bestie-voice-ai/
│
├── main.py              ← Run this for full voice mode
├── text_mode.py         ← Run this to test without mic/speaker
├── requirements.txt     ← Python packages
├── .env.example         ← Copy to .env and customize
│
├── core/
│   ├── config.py        ← All settings (model, voice, wake word)
│   ├── assistant.py     ← Main pipeline orchestrator
│   ├── listener.py      ← Microphone + wake word detection
│   ├── transcriber.py   ← Whisper speech-to-text
│   ├── brain.py         ← Ollama LLM (the AI)
│   ├── speaker.py       ← Piper text-to-speech
│   └── utils.py         ← Terminal output helpers
│
├── models/              ← (auto-managed by Ollama)
├── voices/              ← Put Piper .onnx voice files here
├── logs/                ← Conversation logs (optional)
└── scripts/
    ├── setup_windows.bat
    └── setup_linux_mac.sh
```

---

## ⚡ Quick Start

### Step 1 — Install prerequisites

**Windows:**
```bat
scripts\setup_windows.bat
```

**Linux / Mac:**
```bash
chmod +x scripts/setup_linux_mac.sh
./scripts/setup_linux_mac.sh
```

### Step 2 — Install Ollama + pull a model
```bash
# Download Ollama from https://ollama.com
# Then pull a model (choose one):
ollama pull llama3.2       # recommended — fast, good quality (~2 GB)
ollama pull mistral        # great alternative (~4 GB)
ollama pull gemma2:2b      # tiny, very fast (~1.5 GB)
```

### Step 3 — Install Piper TTS + voice model
1. Download Piper from: https://github.com/rhasspy/piper/releases
2. Extract and add to your PATH (or set `PIPER_PATH` in `.env`)
3. Download a voice from: https://huggingface.co/rhasspy/piper-voices
4. Place the `.onnx` and `.onnx.json` files in the `voices/` folder

Popular English voices:
- `en_US-amy-medium` — friendly female voice
- `en_US-ryan-high` — natural male voice
- `en_GB-alan-medium` — British accent

### Step 4 — Configure (optional)
```bash
cp .env.example .env
# Edit .env to set your name, city, wake word, model etc.
```

### Step 5 — Run!
```bash
# Test text-only first (no mic needed):
python text_mode.py

# Full voice mode:
python main.py
```

---

## 🗣️ How to Use

1. Run `python main.py`
2. Say **"hey bestie"** (or your custom wake word)
3. Wait for the 🔔 notification
4. Ask your question or say anything
5. Bestie responds in voice!

---

## 🔧 Customization

Edit `core/config.py` or `.env` to change:

| Setting | Default | Options |
|---|---|---|
| AI model | `llama3.2` | mistral, gemma2, qwen2.5 |
| Whisper size | `base` | tiny, small, medium, large |
| Wake word | `hey bestie` | anything you want |
| Voice | `en_US-amy-medium` | any Piper voice |
| Language | `en` | hi, en, auto |

---

## 💻 Hardware Requirements

| Spec | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Storage | 5 GB free | 10 GB |
| GPU | Not needed | NVIDIA (much faster) |
| Python | 3.9+ | 3.11+ |

---

## 🐛 Troubleshooting

**"Ollama not running"**
```bash
ollama serve   # run in a separate terminal
```

**"No microphone found"**
- Check Windows: Settings → Privacy → Microphone → allow apps
- Check your default recording device in Sound settings

**"Piper not found"**
- Make sure piper.exe is in your PATH, or set `PIPER_PATH` in `.env`
- Windows: add the Piper folder to System Environment Variables → Path

**"Model too slow"**
- Switch to a smaller model: `OLLAMA_MODEL=gemma2:2b`
- Switch to faster Whisper: `WHISPER_MODEL=tiny`

**Voice sounds robotic / no voice at all**
- Confirm `.onnx` file exists in `voices/` folder
- Try running Piper directly: `piper --model voices/en_US-amy-medium.onnx --output_file test.wav` then type text + Enter

---

## 📦 Tech Stack (all free & open source)

| Component | Tool | License |
|---|---|---|
| AI Brain | Ollama + Llama/Mistral | MIT / Apache 2 |
| Speech → Text | OpenAI Whisper | MIT |
| Text → Speech | Piper TTS | MIT |
| Audio I/O | SoundDevice | MIT |

**Total monthly cost: ₹0**
