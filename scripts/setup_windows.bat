@echo off
echo ============================================
echo   Bestie Voice AI — Windows Setup Script
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Download from https://python.org
    pause & exit /b 1
)
echo [OK] Python found

:: Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found. Reinstall Python with pip included.
    pause & exit /b 1
)

:: Install Python packages
echo.
echo Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed. Check your internet connection.
    pause & exit /b 1
)
echo [OK] Python packages installed

:: Check Ollama
echo.
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Ollama not found.
    echo        Download from: https://ollama.com
    echo        After installing, run: ollama pull llama3.2
) else (
    echo [OK] Ollama found
    echo Pulling llama3.2 model (this may take a few minutes)...
    ollama pull llama3.2
)

:: Check Piper
echo.
piper --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Piper TTS not found.
    echo        Download from: https://github.com/rhasspy/piper/releases
    echo        Extract and add to PATH, or set PIPER_PATH in .env
    echo        Voice models: https://huggingface.co/rhasspy/piper-voices
    echo        Place .onnx files in the voices/ folder
) else (
    echo [OK] Piper found
)

echo.
echo ============================================
echo   Setup complete!
echo.
echo   QUICK START:
echo   1. Make sure Ollama is running: ollama serve
echo   2. Test text mode first: python text_mode.py
echo   3. Then run full voice: python main.py
echo ============================================
pause
