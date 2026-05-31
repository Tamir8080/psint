[README.md](https://github.com/user-attachments/files/28436519/README.md)
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

### Linux / macOS
```bash
git clone https://github.com/yourusername/psint.git
cd psint
pip install -r requirements.txt
chmod +x osint.py
python osint.py --help
```

### Windows
```cmd
git clone https://github.com/yourusername/psint.git
cd psint
pip install -r requirements.txt
osint.bat --help
```

---

## 💻 Usage

```
python osint.py [OPTIONS]
```

### Basic Examples

```bash
# Search a username across 40+ platforms
python osint.py --username johndoe

# Build intelligence profile from name + filters
python osint.py --name "John Doe" --country "UK" --city "London"

# Full profile search with all filters
python osint.py --username johndoe --name "John Doe" --sex male --country "US" --age 28

# Email intelligence
python osint.py --email john@example.com

# Phone intelligence
python osint.py --phone +12025551234

# Analyze image EXIF metadata
python osint.py --image /path/to/photo.jpg

# Run all modules and save HTML report
python osint.py --username johndoe --name "John Doe" --all --output report.html
```

### All Options

```
Target Input:
  --username USERNAME     Username to search across platforms
  --name FULL_NAME        Full name (e.g. "John Doe")
  --email EMAIL           Email address
  --phone PHONE           Phone number (E.164 format: +1234567890)
  --image IMAGE_PATH      Local image for EXIF analysis

Profile Filters:
  --sex {male,female,other}
  --country COUNTRY       Country (e.g. "US", "France")
  --city CITY             City
  --age AGE               Age or range (e.g. "25" or "20-30")
  --company COMPANY       Employer or company

Module Selection:
  --all, -a               Run all modules
  --social                Social media search only
  --profile               Profile build only
  --img                   Image search only

Output:
  --output FILE           Save to file (.json, .txt, .html)
  --verbose, -v           Show all platform results
  --no-color              Disable ANSI colors (for piping)
  --timeout SECONDS       Request timeout (default: 10)
```

---

## 📊 Sample Output

```
[10:42:01] [*] Starting username search across social platforms...

  [✓] GitHub               https://github.com/johndoe
  [✓] Twitter/X            https://twitter.com/johndoe
  [✓] Reddit               https://www.reddit.com/user/johndoe
  [✓] LinkedIn             https://www.linkedin.com/in/johndoe
  [✓] Instagram            https://www.instagram.com/johndoe/

  Found on 5 / 40 platforms
```

---

## 🗂️ Project Structure

```
psint/
├── osint.py              # Main entry point (CLI)
├── osint.bat             # Windows launcher
├── requirements.txt
├── README.md
└── modules/
    ├── banner.py         # ASCII banner
    ├── username_search.py # Platform username checker (40+ sites)
    ├── profile_builder.py # Name/email/phone intelligence
    ├── image_search.py   # EXIF analysis & reverse search
    ├── report.py         # JSON/HTML/TXT report generator
    └── utils.py          # Colors, helpers
```

---

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
