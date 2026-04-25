#!/bin/bash
set -e

echo "============================================"
echo "  Bestie Voice AI — Linux/Mac Setup"
echo "============================================"
echo

# Python check
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 not found. Install with:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Mac: brew install python3"
    exit 1
fi
echo "[OK] Python: $(python3 --version)"

# pip
pip3 install -r requirements.txt
echo "[OK] Python packages installed"

# System audio libs (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing system audio libraries..."
    sudo apt-get install -y portaudio19-dev libsndfile1 ffmpeg 2>/dev/null || \
    sudo dnf install -y portaudio-devel libsndfile ffmpeg 2>/dev/null || \
    echo "[WARN] Could not auto-install audio libs. Install portaudio manually."
fi

# Ollama
if ! command -v ollama &>/dev/null; then
    echo
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi
echo "[OK] Ollama: $(ollama --version)"

echo "Pulling llama3.2 model (may take a few minutes on first run)..."
ollama pull llama3.2

# Piper
if ! command -v piper &>/dev/null; then
    echo
    echo "[WARN] Piper TTS not found."
    echo "       Download from: https://github.com/rhasspy/piper/releases"
    echo "       Extract and add to PATH, then re-run this script."
    echo "       Voice models: https://huggingface.co/rhasspy/piper-voices"
    echo "       Place .onnx files in the voices/ folder"
else
    echo "[OK] Piper found"
fi

echo
echo "============================================"
echo "  Setup complete!"
echo
echo "  QUICK START:"
echo "  1. Start Ollama: ollama serve   (new terminal)"
echo "  2. Test text:    python3 text_mode.py"
echo "  3. Full voice:   python3 main.py"
echo "============================================"
