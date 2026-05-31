# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

---

## Reporting a Vulnerability

If you discover a security vulnerability in PSINT, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

Send a private report to:
- **Email:** your@email.com
- **GitHub:** Use [Private Security Advisory](https://github.com/Tamir8080/psint/security/advisories/new)

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within **48 hours** and aim to patch within **7 days**.

---

## Scope

### In Scope
- Code vulnerabilities in the tool itself
- Dependencies with known CVEs
- Logic flaws that could cause unintended behavior

### Out of Scope
- Vulnerabilities in third-party platforms being searched
- Issues caused by misuse of the tool
- Social engineering attacks

---

## Ethical Use Policy

PSINT is built for **authorized security research and education only**.

### ✅ Acceptable Use
- Penetration testing with written permission
- Security research on your own accounts
- Academic assignments and CTF challenges
- Bug bounty programs within their defined scope

### ❌ Unacceptable Use
- Investigating individuals without their consent
- Stalking, harassment, or doxxing
- Any illegal surveillance or data collection
- Violating platform terms of service

---

## Legal Disclaimer

Misuse of this tool may violate:
- Computer Fraud and Abuse Act (CFAA) — USA
- Computer Misuse Act — UK
- General Data Protection Regulation (GDPR) — EU
- And equivalent laws in your country

The author holds **no responsibility** for unauthorized or illegal use.

---

## Dependencies

PSINT uses the following dependencies — keep them updated:

| Package  | Purpose              | Check vulnerabilities |
| -------- | -------------------- | --------------------- |
| requests | HTTP requests        | [PyPI](https://pypi.org/project/requests/) |
| Pillow   | Image EXIF analysis  | [PyPI](https://pypi.org/project/Pillow/) |

To check for vulnerable dependencies:
```bash
pip install safety
safety check -r requirements.txt
```

---

## Security Best Practices for Users

- Always run PSINT in a **virtual environment**
- Keep dependencies updated: `pip install -r requirements.txt --upgrade`
- Never run as root/administrator unless necessary
- Review output reports before sharing — they may contain sensitive data
- Delete report files after use

---

## Acknowledgements

We thank all responsible security researchers who help improve PSINT.
Responsible disclosures will be credited in release notes.

---

Last updated: May 2026
Maintainer: Tamir8080
