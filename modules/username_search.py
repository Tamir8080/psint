"""
Username search module — checks username existence across social platforms
by probing public profile URLs (no API keys required, fully passive).
"""
import requests
import concurrent.futures
from .utils import Colors, print_status, separator

# All platforms use passive HTTP HEAD/GET probes on public URLs only.
PLATFORMS = {
    # --- Social Networks ---
    "Twitter/X":        "https://twitter.com/{u}",
    "Instagram":        "https://www.instagram.com/{u}/",
    "TikTok":           "https://www.tiktok.com/@{u}",
    "Facebook":         "https://www.facebook.com/{u}",
    "Snapchat":         "https://www.snapchat.com/add/{u}",
    "Pinterest":        "https://www.pinterest.com/{u}/",
    "Tumblr":           "https://{u}.tumblr.com",
    "Reddit":           "https://www.reddit.com/user/{u}",
    "LinkedIn":         "https://www.linkedin.com/in/{u}",
    "Mastodon":         "https://mastodon.social/@{u}",
    "Bluesky":          "https://bsky.app/profile/{u}.bsky.social",
    # --- Developer / Tech ---
    "GitHub":           "https://github.com/{u}",
    "GitLab":           "https://gitlab.com/{u}",
    "HackerNews":       "https://news.ycombinator.com/user?id={u}",
    "Stack Overflow":   "https://stackoverflow.com/users/{u}",
    "Codepen":          "https://codepen.io/{u}",
    "Replit":           "https://replit.com/@{u}",
    "Dev.to":           "https://dev.to/{u}",
    "Kaggle":           "https://www.kaggle.com/{u}",
    "HuggingFace":      "https://huggingface.co/{u}",
    # --- Gaming ---
    "Steam":            "https://steamcommunity.com/id/{u}",
    "Twitch":           "https://www.twitch.tv/{u}",
    "Roblox":           "https://www.roblox.com/user.aspx?username={u}",
    "Chess.com":        "https://www.chess.com/member/{u}",
    # --- Content / Creative ---
    "YouTube":          "https://www.youtube.com/@{u}",
    "Medium":           "https://medium.com/@{u}",
    "Substack":         "https://{u}.substack.com",
    "Flickr":           "https://www.flickr.com/people/{u}",
    "Behance":          "https://www.behance.net/{u}",
    "Dribbble":         "https://dribbble.com/{u}",
    "Vimeo":            "https://vimeo.com/{u}",
    "SoundCloud":       "https://soundcloud.com/{u}",
    "Spotify":          "https://open.spotify.com/user/{u}",
    "Last.fm":          "https://www.last.fm/user/{u}",
    # --- Forums / Communities ---
    "Keybase":          "https://keybase.io/{u}",
    "ProductHunt":      "https://www.producthunt.com/@{u}",
    "AngelList":        "https://angel.co/{u}",
    "Patreon":          "https://www.patreon.com/{u}",
    "Ko-fi":            "https://ko-fi.com/{u}",
}

# Platforms that return 200 even for non-existent users — need body check
BODY_CHECK_PLATFORMS = {
    "Reddit":        "Sorry, nobody on Reddit goes by that name",
    "HackerNews":    "No such user",
    "Chess.com":     "404",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

class UsernameSearcher:
    def __init__(self, timeout: int = 10, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose
        self.found = []
        self.not_found = []
        self.errors = []

    def _check_platform(self, platform: str, url_template: str, username: str) -> dict:
        url = url_template.replace("{u}", username)
        result = {"platform": platform, "url": url, "found": False, "status": None}
        try:
            resp = requests.get(url, headers=HEADERS, timeout=self.timeout,
                                allow_redirects=True)
            result["status"] = resp.status_code

            if resp.status_code == 200:
                # Extra body-check for platforms that 200 on missing users
                if platform in BODY_CHECK_PLATFORMS:
                    needle = BODY_CHECK_PLATFORMS[platform].lower()
                    if needle in resp.text.lower():
                        result["found"] = False
                        return result
                result["found"] = True
            elif resp.status_code == 404:
                result["found"] = False
            else:
                result["found"] = False

        except requests.exceptions.Timeout:
            result["status"] = "timeout"
        except requests.exceptions.ConnectionError:
            result["status"] = "connection_error"
        except Exception as ex:
            result["status"] = f"error: {ex}"
        return result

    def search(self, username: str) -> dict:
        print(f"\n{Colors.BOLD}[~] Searching username: {Colors.CYAN}{username}{Colors.RESET}")
        separator()

        results_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(self._check_platform, platform, url_tpl, username): platform
                for platform, url_tpl in PLATFORMS.items()
            }
            for future in concurrent.futures.as_completed(futures):
                r = future.result()
                results_list.append(r)
                if r["found"]:
                    print(f"  {Colors.GREEN}[✓]{Colors.RESET} {r['platform']:<20} {Colors.CYAN}{r['url']}{Colors.RESET}")
                    self.found.append(r)
                else:
                    if self.verbose:
                        print(f"  {Colors.RED}[✗]{Colors.RESET} {r['platform']:<20} {Colors.DIM}({r['status']}){Colors.RESET}")
                    self.not_found.append(r)

        separator()
        print(f"\n  {Colors.GREEN}Found on {len(self.found)}{Colors.RESET} / {len(PLATFORMS)} platforms")
        return {
            "username": username,
            "found": self.found,
            "not_found": self.not_found,
            "total_platforms": len(PLATFORMS),
            "found_count": len(self.found),
        }
