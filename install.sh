#!/bin/bash

echo "=================================="
echo "   PSINT - Auto Installer"
echo "=================================="

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv

# Activate it
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[*] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[+] Installation complete!"
echo "[+] Run the tool with:"
echo "    source venv/bin/activate"
echo "    python3 osint.py --help"
echo ""
