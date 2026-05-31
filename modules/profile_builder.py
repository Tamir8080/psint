"""
Profile builder — aggregates publicly available information
from open data sources (no private API keys required for basic mode).
"""
import re
import requests
from .utils import Colors, print_status, separator

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

class ProfileBuilder:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    # ------------------------------------------------------------------ #
    # Public profile build from name + optional filters                   #
    # ------------------------------------------------------------------ #
    def build(self, target: dict) -> dict:
        name = target.get("name", "")
        country = target.get("country", "")
        city = target.get("city", "")
        company = target.get("company", "")
        sex = target.get("sex", "")
        age = target.get("age", "")

        print(f"\n{Colors.BOLD}[~] Building intelligence profile for: {Colors.CYAN}{name}{Colors.RESET}")
        separator()

        profile = {
            "input": target,
            "search_queries": [],
            "data_sources": [],
            "inferred": {},
        }

        # Build targeted Google dork queries
        dorks = self._generate_dorks(name, country, city, company)
        profile["search_queries"] = dorks

        print(f"  {Colors.YELLOW}[*]{Colors.RESET} Generated {len(dorks)} OSINT search queries")
        print(f"\n  {Colors.BOLD}Google Dork Queries (use in browser):{Colors.RESET}")
        for i, dork in enumerate(dorks[:6], 1):
            print(f"  {Colors.DIM}{i}.{Colors.RESET} {dork}")

        # Infer additional info
        inferred = {}
        if sex:
            inferred["likely_pronouns"] = "he/him" if sex == "male" else ("she/her" if sex == "female" else "they/them")
        if country:
            inferred["country_code"] = self._country_to_code(country)
            inferred["common_platforms"] = self._country_platforms(country)
        if age:
            inferred["birth_year_estimate"] = self._estimate_birth_year(age)

        profile["inferred"] = inferred

        # Wikidata public person lookup
        wiki = self._wikidata_lookup(name)
        if wiki:
            profile["wikidata"] = wiki
            print_status(f"Wikidata entity found: {wiki.get('label', name)}", "found")

        print(f"\n  {Colors.GREEN}[+]{Colors.RESET} Profile build complete")
        return profile

    # ------------------------------------------------------------------ #
    # Email intelligence (public breach checks via HaveIBeenPwned API)   #
    # ------------------------------------------------------------------ #
    def email_lookup(self, email: str) -> dict:
        print(f"\n{Colors.BOLD}[~] Email intelligence: {Colors.CYAN}{email}{Colors.RESET}")
        separator()

        result = {"email": email, "sources": [], "gravatar": None, "format_valid": False}

        # Validate format
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            result["format_valid"] = True
            print_status("Email format: valid", "found")
        else:
            print_status("Email format: invalid", "error")
            return result

        domain = email.split("@")[1]
        result["domain"] = domain

        # Domain MX lookup hint
        print_status(f"Email domain: {domain}", "info")

        # Gravatar hash (MD5 of lowercase email — public standard)
        import hashlib
        gh = hashlib.md5(email.strip().lower().encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{gh}?d=404"
        result["gravatar_hash"] = gh
        result["gravatar_check_url"] = gravatar_url
        try:
            r = requests.get(gravatar_url, timeout=8)
            if r.status_code == 200:
                result["gravatar"] = f"https://www.gravatar.com/{gh}"
                print_status(f"Gravatar profile found: {result['gravatar']}", "found")
            else:
                print_status("No Gravatar profile found", "notfound")
        except Exception:
            pass

        # HaveIBeenPwned (public API — no key for basic check)
        hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        print_status("Checking HaveIBeenPwned (manual):", "info")
        print(f"    → {Colors.CYAN}https://haveibeenpwned.com/account/{email}{Colors.RESET}")
        result["hibp_manual_url"] = f"https://haveibeenpwned.com/account/{email}"

        # EmailRep.io public lookup
        emailrep_url = f"https://emailrep.io/{email}"
        try:
            r = requests.get(emailrep_url, headers={"User-Agent": "psint/1.0"}, timeout=8)
            if r.status_code == 200:
                data = r.json()
                result["emailrep"] = {
                    "reputation": data.get("reputation"),
                    "suspicious": data.get("suspicious"),
                    "references": data.get("references"),
                    "profiles": data.get("details", {}).get("profiles", []),
                    "first_seen": data.get("details", {}).get("first_seen"),
                    "last_seen": data.get("details", {}).get("last_seen"),
                    "domain_exists": data.get("details", {}).get("domain_exists"),
                }
                rep = data.get("reputation", "unknown")
                color = Colors.GREEN if rep == "high" else (Colors.YELLOW if rep == "medium" else Colors.RED)
                print_status(f"EmailRep reputation: {color}{rep}{Colors.RESET}", "info")
                profiles = data.get("details", {}).get("profiles", [])
                if profiles:
                    print_status(f"Associated profiles: {', '.join(profiles)}", "found")
        except Exception as ex:
            if self.verbose:
                print_status(f"EmailRep lookup failed: {ex}", "warning")

        return result

    # ------------------------------------------------------------------ #
    # Phone intelligence                                                   #
    # ------------------------------------------------------------------ #
    def phone_lookup(self, phone: str) -> dict:
        print(f"\n{Colors.BOLD}[~] Phone intelligence: {Colors.CYAN}{phone}{Colors.RESET}")
        separator()

        result = {"phone": phone}

        # Basic E.164 format check
        clean = re.sub(r"[\s\-\(\)]", "", phone)
        result["cleaned"] = clean

        if clean.startswith("+"):
            # Country code inference
            cc_map = {
                "+1": "USA/Canada", "+44": "UK", "+33": "France",
                "+49": "Germany", "+61": "Australia", "+91": "India",
                "+86": "China", "+81": "Japan", "+55": "Brazil",
                "+7": "Russia", "+34": "Spain", "+39": "Italy",
                "+31": "Netherlands", "+46": "Sweden", "+47": "Norway",
                "+45": "Denmark", "+41": "Switzerland", "+32": "Belgium",
                "+351": "Portugal", "+48": "Poland", "+27": "South Africa",
                "+234": "Nigeria", "+20": "Egypt", "+966": "Saudi Arabia",
            }
            for prefix, country in cc_map.items():
                if clean.startswith(prefix):
                    result["country"] = country
                    result["country_code"] = prefix
                    print_status(f"Country code: {prefix} → {country}", "found")
                    break

        # Search reference links
        search_links = [
            f"https://www.truecaller.com/search/us/{clean.lstrip('+')}",
            f"https://www.whitepages.com/phone/{clean}",
            f"https://sync.me/search/?number={clean}",
        ]
        result["manual_lookup_urls"] = search_links
        print_status("Manual lookup URLs:", "info")
        for url in search_links:
            print(f"    → {Colors.CYAN}{url}{Colors.RESET}")

        return result

    # ------------------------------------------------------------------ #
    # Helpers                                                             #
    # ------------------------------------------------------------------ #
    def _generate_dorks(self, name, country="", city="", company="") -> list:
        dorks = []
        q = f'"{name}"'
        loc = f'"{city}"' if city else (f'"{country}"' if country else "")
        org = f'"{company}"' if company else ""

        dorks.append(f'site:linkedin.com {q} {loc} {org}'.strip())
        dorks.append(f'site:twitter.com OR site:x.com {q}')
        dorks.append(f'site:facebook.com {q} {loc}'.strip())
        dorks.append(f'site:instagram.com {q}')
        dorks.append(f'{q} {loc} {org} email OR contact OR profile'.strip())
        dorks.append(f'{q} site:github.com')
        dorks.append(f'"{name}" filetype:pdf resume OR cv {loc}'.strip())
        dorks.append(f'inurl:about {q} {loc}'.strip())
        dorks.append(f'{q} {org} site:crunchbase.com OR site:angel.co'.strip())
        dorks.append(f'"{name}" phone OR email OR address {loc}'.strip())
        return [d for d in dorks if d.strip()]

    def _country_to_code(self, country: str) -> str:
        mapping = {
            "us": "US", "usa": "US", "united states": "US",
            "uk": "GB", "united kingdom": "GB", "england": "GB",
            "france": "FR", "germany": "DE", "spain": "ES",
            "italy": "IT", "canada": "CA", "australia": "AU",
            "india": "IN", "china": "CN", "japan": "JP",
            "brazil": "BR", "russia": "RU",
        }
        return mapping.get(country.lower(), country.upper()[:2])

    def _country_platforms(self, country: str) -> list:
        regional = {
            "CN": ["Weibo", "WeChat", "Douyin", "Baidu Tieba"],
            "RU": ["VKontakte", "OK.ru", "Telegram"],
            "KR": ["KakaoTalk", "Naver Blog", "Band"],
            "JP": ["Line", "Mixi", "Nico Nico"],
            "IN": ["ShareChat", "Josh", "Koo"],
        }
        code = self._country_to_code(country)
        return regional.get(code, ["Instagram", "Facebook", "Twitter", "LinkedIn"])

    def _estimate_birth_year(self, age: str) -> str:
        import datetime
        current_year = datetime.datetime.now().year
        if "-" in age:
            lo, hi = age.split("-")
            return f"{current_year - int(hi.strip())}–{current_year - int(lo.strip())}"
        try:
            return str(current_year - int(age))
        except ValueError:
            return "unknown"

    def _wikidata_lookup(self, name: str) -> dict:
        try:
            url = "https://www.wikidata.org/w/api.php"
            params = {
                "action": "wbsearchentities",
                "search": name,
                "language": "en",
                "format": "json",
                "limit": 1,
                "type": "item",
            }
            r = requests.get(url, params=params, timeout=8, headers=HEADERS)
            data = r.json()
            results = data.get("search", [])
            if results:
                entity = results[0]
                return {
                    "id": entity.get("id"),
                    "label": entity.get("label"),
                    "description": entity.get("description"),
                    "url": entity.get("url"),
                    "concepturi": entity.get("concepturi"),
                }
        except Exception:
            pass
        return {}
