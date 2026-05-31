@echo off
echo ==================================
echo    PSINT - Auto Installer
echo ==================================

echo [*] Creating virtual environment...
python -m venv venv

echo [*] Activating virtual environment...
call venv\Scripts\activate

echo [*] Installing dependencies...
pip install -r requirements.txt

echo.
echo [+] Installation complete!
echo [+] Run the tool with:
echo     venv\Scripts\activate
echo     python osint.py --help
echo.
pause
