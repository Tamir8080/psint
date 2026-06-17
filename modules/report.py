"""
Report generator — outputs findings as terminal summary, JSON, TXT, or HTML.
"""
import json
import datetime
from .utils import Colors, separator

class ReportGenerator:
    def __init__(self, target: dict, results: dict):
        self.target = target
        self.results = results
        self.timestamp = datetime.datetime.now().isoformat()

    def print_summary(self):
        print(f"\n{Colors.BOLD}{'═'*65}")
        print(f"  PSINT REPORT SUMMARY")
        print(f"{'═'*65}{Colors.RESET}")
        print(f"  Generated : {Colors.DIM}{self.timestamp}{Colors.RESET}")
        print(f"  Target    : {Colors.CYAN}{self._target_str()}{Colors.RESET}")
        separator()

        # Social accounts summary
        if "social_accounts" in self.results:
            sa = self.results["social_accounts"]
            found = sa.get("found", [])
            print(f"\n  {Colors.BOLD}Social Media Accounts{Colors.RESET} ({Colors.GREEN}{len(found)} found{Colors.RESET})")
            for acc in found:
                print(f"    {Colors.GREEN}✓{Colors.RESET}  {acc['platform']:<20} {acc['url']}")

        # Profile summary
        if "profile" in self.results:
            prof = self.results["profile"]
            print(f"\n  {Colors.BOLD}Intelligence Profile{Colors.RESET}")
            inferred = prof.get("inferred", {})
            for k, v in inferred.items():
                if isinstance(v, list):
                    v = ", ".join(v)
                print(f"    {Colors.DIM}•{Colors.RESET}  {k.replace('_',' ').title():<30} {v}")
            if "wikidata" in prof and prof["wikidata"]:
                wd = prof["wikidata"]
                print(f"    {Colors.DIM}•{Colors.RESET}  Wikidata{' '*22} {wd.get('label')} — {wd.get('description', '')}")
            print(f"\n  {Colors.BOLD}OSINT Search Queries{Colors.RESET}")
            for i, q in enumerate(prof.get("search_queries", [])[:5], 1):
                print(f"    {Colors.DIM}{i}.{Colors.RESET} {q}")

        # Email summary
        if "email_info" in self.results:
            ei = self.results["email_info"]
            print(f"\n  {Colors.BOLD}Email Intelligence{Colors.RESET}")
            print(f"    {Colors.DIM}•{Colors.RESET}  Valid format      : {'Yes' if ei.get('format_valid') else 'No'}")
            if "emailrep" in ei:
                er = ei["emailrep"]
                print(f"    {Colors.DIM}•{Colors.RESET}  Reputation        : {er.get('reputation', 'N/A')}")
                print(f"    {Colors.DIM}•{Colors.RESET}  Suspicious        : {er.get('suspicious', 'N/A')}")
                profs = er.get("profiles", [])
                if profs:
                    print(f"    {Colors.DIM}•{Colors.RESET}  Associated        : {', '.join(profs)}")
            if ei.get("gravatar"):
                print(f"    {Colors.DIM}•{Colors.RESET}  Gravatar          : {ei['gravatar']}")

        # Phone summary
        if "phone_info" in self.results:
            pi = self.results["phone_info"]
            print(f"\n  {Colors.BOLD}Phone Intelligence{Colors.RESET}")
            if "country" in pi:
                print(f"    {Colors.DIM}•{Colors.RESET}  Country           : {pi['country']}")

        # Image summary
        if "image_analysis" in self.results:
            ia = self.results["image_analysis"]
            exif = ia.get("exif", {})
            print(f"\n  {Colors.BOLD}Image Analysis{Colors.RESET}")
            if "gps_latitude" in exif:
                print(f"    {Colors.DIM}•{Colors.RESET}  GPS               : {exif['gps_latitude']}, {exif['gps_longitude']}")
                print(f"    {Colors.DIM}•{Colors.RESET}  Maps URL          : {exif.get('google_maps_url', '')}")
            for field in ["Make", "Model", "DateTime", "Software"]:
                if field in exif:
                    print(f"    {Colors.DIM}•{Colors.RESET}  {field:<18} : {exif[field]}")

        print(f"\n{Colors.BOLD}{'═'*65}{Colors.RESET}\n")

    def save(self, path: str):
        ext = path.lower().split(".")[-1]
        if ext == "json":
            self._save_json(path)
        elif ext == "html":
            self._save_html(path)
        else:
            self._save_txt(path)

    def _target_str(self) -> str:
        # Minimize sensitive data exposure in report headers/metadata.
        # Keep only non-sensitive identifiers for display.
        parts = [v for v in [self.target.get("username"), self.target.get("name")] if v]
        return " | ".join(parts) if parts else "Unknown"

    def _save_json(self, path: str):
        payload = {
            "tool": "PSINT v1.0",
            "timestamp": self.timestamp,
            "target": self.target,
            "results": self._json_safe(self.results),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def _save_txt(self, path: str):
        lines = [
            "=" * 65,
            "PSINT - Passive OSINT Intelligence Report",
            "=" * 65,
            f"Generated : {self.timestamp}",
            f"Target    : {self._target_str()}",
            "",
        ]
        if "social_accounts" in self.results:
            found = self.results["social_accounts"].get("found", [])
            lines.append(f"Social Accounts ({len(found)} found):")
            for acc in found:
                lines.append(f"  [+] {acc['platform']}: {acc['url']}")
            lines.append("")
        if "profile" in self.results:
            lines.append("OSINT Queries:")
            for q in self.results["profile"].get("search_queries", []):
                lines.append(f"  {q}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _save_html(self, path: str):
        found_accounts = ""
        if "social_accounts" in self.results:
            for acc in self.results["social_accounts"].get("found", []):
                found_accounts += f'<li><strong>{acc["platform"]}</strong>: <a href="{acc["url"]}" target="_blank">{acc["url"]}</a></li>'

        queries_html = ""
        if "profile" in self.results:
            for q in self.results["profile"].get("search_queries", []):
                queries_html += f"<li><code>{q}</code></li>"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PSINT Report — {self._target_str()}</title>
<style>
  body {{ font-family: 'Courier New', monospace; background: #0d1117; color: #c9d1d9; margin: 2rem; }}
  h1 {{ color: #58a6ff; }} h2 {{ color: #3fb950; border-bottom: 1px solid #30363d; padding-bottom:.4rem; }}
  a {{ color: #58a6ff; }} code {{ background:#161b22; padding:2px 6px; border-radius:4px; }}
  .meta {{ color:#8b949e; font-size:.85rem; }} ul {{ line-height:2; }}
  .container {{ max-width:900px; margin:auto; }}
  .badge {{ background:#1f6feb; color:#fff; padding:2px 8px; border-radius:12px; font-size:.75rem; }}
</style>
</head>
<body>
<div class="container">
  <h1>&#128270; PSINT Intelligence Report</h1>
  <p class="meta">Generated: {self.timestamp} &nbsp;|&nbsp; Target: <strong>{self._target_str()}</strong></p>
  <h2>Social Media Accounts <span class="badge">{len(self.results.get("social_accounts",{}).get("found",[]))} found</span></h2>
  <ul>{found_accounts or "<li>No accounts found</li>"}</ul>
  <h2>OSINT Search Queries</h2>
  <ul>{queries_html or "<li>No queries generated</li>"}</ul>
  <hr style="border-color:#30363d">
  <p class="meta">&#9888;&#65039; For authorized security research only. PSINT v1.0</p>
</div>
</body>
</html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def _json_safe(self, obj):
        if isinstance(obj, dict):
            return {k: self._json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._json_safe(i) for i in obj]
        else:
            return str(obj) if not isinstance(obj, (str, int, float, bool, type(None))) else obj
