# 🔍 PSINT — Passive OSINT Intelligence Gatherer

> A cross-platform passive OSINT framework for authorized security research and cybersecurity education.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Education](https://img.shields.io/badge/Purpose-Educational-orange)

---

## ⚠️ Legal Disclaimer

**This tool is for educational purposes and authorized security research ONLY.**  
Using this tool against individuals or systems without explicit written permission may violate computer crime laws including CFAA (USA), Computer Misuse Act (UK), GDPR (EU), and equivalent laws in your jurisdiction.  
**The author assumes no liability for unauthorized use.**

---

## 📋 Features

| Module | Description |
|--------|-------------|
| 🌐 Username Search | Check 40+ platforms (Twitter, Instagram, GitHub, TikTok, Steam, etc.) |
| 👤 Profile Builder | Generate OSINT dork queries, infer metadata, Wikidata lookup |
| 📧 Email Intel | Gravatar check, EmailRep.io reputation, HIBP reference |
| 📱 Phone Intel | Country code detection, manual lookup references |
| 🖼️ Image Analysis | EXIF extraction (GPS, device, timestamps), reverse search links |
| 📄 Report Export | JSON, HTML, and TXT report generation |

---

## 🚀 Installation

### Requirements
- Python 3.8+
- pip

---

### 🐧 Kali Linux / Ubuntu / Debian

```bash
# Step 1 — Clone the repo
git clone https://github.com/Tamir8080/psint.git
cd psint

# Step 2 — Install venv (Kali requires this)
sudo apt update
sudo apt install python3-venv -y

# Step 3 — Create virtual environment
python3 -m venv venv

# Step 4 — Activate it
source venv/bin/activate

# Step 5 — Install dependencies
pip install -r requirements.txt

# Step 6 — Run the tool
python3 osint.py --help
```

### 🍎 macOS

```bash
git clone https://github.com/Tamir8080/psint.git
cd psint
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 osint.py --help
```

### 🪟 Windows (PowerShell)

```powershell
git clone https://github.com/Tamir8080/psint.git
cd psint
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python osint.py --help
```

---

## ⚡ Easy Install (One Script)

### Kali / Linux / macOS
```bash
git clone https://github.com/Tamir8080/psint.git
cd psint
bash install.sh
```

### Windows
```cmd
git clone https://github.com/Tamir8080/psint.git
cd psint
install.bat
```

---

## 🔄 Every time you want to use it

### Kali / Linux / macOS
```bash
cd psint
source venv/bin/activate
python3 osint.py --help
```

### Windows
```cmd
cd psint
venv\Scripts\activate
python osint.py --help
```

---

## 💻 Usage Examples

```bash
# Search username across 40+ platforms
python3 osint.py --username johndoe

# Build profile from name
python3 osint.py --name "John Doe" --country "US" --city "New York"

# Email intelligence
python3 osint.py --email target@example.com

# Phone lookup
python3 osint.py --phone +1234567890

# Analyze image EXIF metadata
python3 osint.py --image photo.jpg

# Run all modules
python3 osint.py --username johndoe --name "John Doe" --all

# Save report
python3 osint.py --username johndoe --output report.html
```

---

## 🛠️ Troubleshooting

| Error | Fix |
|-------|-----|
| `pip not found` | Run `sudo apt install python3-pip -y` |
| `externally-managed-environment` | Use virtual environment — follow steps above |
| `python3-venv not found` | Run `sudo apt install python3-venv -y` |
| `No module named requests` | Run `pip install -r requirements.txt` inside venv |
| `git not found` (Windows) | Download Git from https://git-scm.com |
| `python not found` | Download Python from https://python.org |
| `destination path already exists` | Skip clone — just `cd psint` and continue |

---

## 🔁 If something breaks — full reset

```bash
cd ~/psint
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 osint.py --help
```


## 🛡️ Ethical Use

This tool only uses:
- **Passive HTTP probing** of publicly accessible profile URLs
- **Public APIs** (Wikidata, EmailRep.io — no authentication)
- **EXIF metadata** from locally provided images
- **No scraping** of private data or login-required pages
- **No data storage** — results only exist in your terminal/report

---

## 📚 Educational Context

PSINT demonstrates core OSINT concepts taught in:
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- CompTIA Security+
- University cybersecurity courses

---

## 🤝 Contributing

Pull requests welcome. Please ensure:
1. No scraping of private/authenticated data
2. New platform targets use only public, unauthenticated URLs
3. Code follows the passive-only philosophy

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Built for cybersecurity education. Use responsibly.
