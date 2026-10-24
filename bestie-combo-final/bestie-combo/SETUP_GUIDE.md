# 🎙️ Bestie AI — Complete Setup Guide
## Oracle VM + Groq API + Local Voice (Zero Cost)

---

## 🗺️ Architecture Overview

```
Your PC (mic + speaker)
    ├── Whisper STT     → runs locally (CPU)
    ├── Piper TTS       → runs locally (CPU)
    └── brain.py
            ├── PRIMARY   → Oracle Cloud VM (Ollama llama3:8b, 24GB RAM)
            └── FALLBACK  → Groq API (llama3-70b, free cloud)

Screen Analysis:
    └── Groq Vision API → no local GPU needed
```

---

## PART 1 — Groq API Setup (15 minutes)

### Step 1 — Sign up for Groq

1. Go to **https://console.groq.com**
2. Click **"Sign Up"** → use Google or email
3. Verify your email

### Step 2 — Generate API key

1. After login, click **"API Keys"** in left sidebar
2. Click **"Create API Key"**
3. Give it a name: `bestie-ai`
4. Copy the key — it starts with `gsk_...`
5. Paste it in your `.env` file:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

### Step 3 — Check free limits

Groq free tier gives you:
- `llama3-70b-8192` — 6,000 tokens/min
- `llama3-8b-8192`  — 30,000 tokens/min
- Vision models     — included free

This is more than enough for a voice assistant.

---

## PART 2 — Oracle Cloud VM Setup (45 minutes)

### Step 1 — Sign up for Oracle Cloud

1. Go to **https://cloud.oracle.com** → click **"Start for free"**
2. Fill in your details:
   - Use your real name and email
   - **Home Region**: Choose **"US East (Ashburn)"** — most capacity
   - (India region often has no ARM capacity)
3. **Credit card**: Required for verification only — NOT charged
   - If Indian debit card is rejected, try a **Visa credit card**
   - If still rejected: upgrade to Pay-As-You-Go after signup (still free)
4. Complete phone verification
5. Wait for welcome email (~5 min)

### Step 2 — Create the Ampere A1 VM (free forever)

1. Login to **cloud.oracle.com**
2. Go to: **Compute → Instances → Create Instance**
3. Configure:
   ```
   Name:  bestie-ai-vm
   Image: Ubuntu 22.04 (Always Free eligible)
   Shape: Click "Change Shape"
           → Ampere → VM.Standard.A1.Flex
           → OCPUs: 4
           → Memory: 24 GB
   ```
4. **SSH Keys**: Click "Generate a key pair"
   - Download both private and public keys
   - Save private key as `oracle_key.pem` on your PC
5. Click **"Create"**

> If you see "Out of host capacity" → wait 10 min and retry, or try a different Availability Domain (AD-2, AD-3).

### Step 3 — Connect to your VM

```bash
# On your local PC:
chmod 400 oracle_key.pem

# SSH into VM (replace with your VM's public IP from Oracle console)
ssh -i oracle_key.pem ubuntu@YOUR_ORACLE_VM_IP
```

### Step 4 — Install Ollama on the VM

```bash
# Inside the Oracle VM:

# Update system
sudo apt update && sudo apt upgrade -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama (runs in background)
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull the model (llama3:8b fits in 24GB RAM perfectly)
ollama pull llama3:8b

# Test it works
ollama run llama3:8b
# Type "hello" — you should get a response
# Press Ctrl+D to exit
```

### Step 5 — Expose Ollama on a public port

```bash
# Edit Ollama service to listen on all interfaces
sudo nano /etc/systemd/system/ollama.service
```

Find the `[Service]` section and add:
```
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Save (Ctrl+O, Enter, Ctrl+X), then restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verify it's listening
ss -tlnp | grep 11434
```

### Step 6 — Open port 11434 in Oracle firewall

**In Oracle Cloud Console:**
1. Go to: **Networking → Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. Click **"Add Ingress Rules"**:
   ```
   Source CIDR:  0.0.0.0/0
   Protocol:     TCP
   Dest Port:    11434
   Description:  Ollama API
   ```
4. Click **"Add Ingress Rules"**

**Also open in Ubuntu firewall:**
```bash
sudo iptables -I INPUT -p tcp --dport 11434 -j ACCEPT
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
```

### Step 7 — Test from your local PC

```bash
# Replace with your Oracle VM's public IP
curl http://YOUR_ORACLE_VM_IP:11434/api/tags
```

You should see JSON with your models listed. ✅

---

## PART 3 — News API Setup (5 minutes)

### Step 1 — Sign up for NewsAPI

1. Go to **https://newsapi.org**
2. Click **"Get API Key"** → sign up with email
3. Copy your API key from the dashboard
4. Add to `.env`:
   ```
   NEWS_API_KEY=your_newsapi_key_here
   ```

Free tier: 100 requests/day — plenty for a voice assistant.

---

## PART 4 — Local PC Setup

### Step 1 — Clone/copy your project

```bash
cd ~/Projects
# If using the zip:
unzip bestie-combo.zip
cd bestie-combo
```

### Step 2 — Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# Windows: venv\Scripts\activate
```

### Step 3 — Install system dependencies (Linux)

```bash
sudo apt install -y \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg \
    tesseract-ocr \
    python3-dev \
    build-essential
```

### Step 4 — Install Python packages

```bash
pip install -r requirements.txt
```

If `pyaudio` fails:
```bash
sudo apt install python3-pyaudio
pip install pyaudio
```

### Step 5 — Install Piper TTS

```bash
# Download Piper
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz

# Move to system path
sudo mv piper /usr/local/bin/piper-tts
echo 'export PATH="/usr/local/bin/piper-tts:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Download voice model
mkdir -p voices
wget -O voices/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx

wget -O voices/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Test Piper
echo "Hello from Bestie AI!" | piper --model voices/en_US-lessac-medium.onnx --output_file test.wav
aplay test.wav
```

### Step 6 — Configure .env

```bash
cp .env.example .env
nano .env
```

Fill in:
```
OLLAMA_HOST=http://YOUR_ORACLE_VM_IP:11434
GROQ_API_KEY=gsk_your_key_here
NEWS_API_KEY=your_newsapi_key_here
BRAIN_MODE=auto
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

### Step 7 — Test each component

```bash
# Test 1: Groq API
python3 -c "
from dotenv import load_dotenv; load_dotenv()
from groq import Groq; import os
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
r = client.chat.completions.create(model='llama3-70b-8192', messages=[{'role':'user','content':'say hello'}], max_tokens=20)
print('Groq OK:', r.choices[0].message.content)
"

# Test 2: Oracle VM
python3 -c "
from dotenv import load_dotenv; load_dotenv()
import requests, os
r = requests.get(os.getenv('OLLAMA_HOST') + '/api/tags', timeout=5)
print('Oracle VM OK:', [m['name'] for m in r.json().get('models',[])])
"

# Test 3: Full text mode
python3 text_mode.py
```

### Step 8 — Run Bestie!

```bash
python3 main.py
```

Say **"hey bestie"** and start talking! 🎙️

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Oracle card rejected | Use Visa credit card, or try Pay-As-You-Go signup |
| Out of host capacity | Wait and retry, or try AD-2/AD-3 in same region |
| Ollama not reachable | Check port 11434 in Oracle Security List + iptables |
| Groq 401 error | API key wrong — regenerate at console.groq.com |
| pip install fails | Use `pip install --break-system-packages` or venv |
| Piper not found | Add `/usr/local/bin/piper-tts` to PATH |
| No mic found | Check: `python3 -c "import sounddevice; print(sounddevice.query_devices())"` |

---

## 💰 Total Monthly Cost: ₹0

| Component | Platform | Cost |
|---|---|---|
| AI brain (text) | Oracle VM (24GB ARM) | Always free |
| AI brain (big) | Groq API (70b model) | Free tier |
| Screen vision | Groq Vision API | Free tier |
| Speech to text | Whisper (your PC) | Free |
| Voice output | Piper TTS (your PC) | Free |
| News | NewsAPI free tier | Free |
