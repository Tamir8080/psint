"""
Image intelligence module.
- Extracts EXIF metadata from local images (GPS, device, timestamp).
- Provides reverse image search links (Google, Bing, TinEye, Yandex).
- Searches for public profile pictures by username.
"""
import os
import struct
from .utils import Colors, print_status, separator

class ImageSearcher:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    # ------------------------------------------------------------------ #
    # Local image analysis — EXIF extraction                              #
    # ------------------------------------------------------------------ #
    def analyze_local(self, image_path: str) -> dict:
        print(f"\n{Colors.BOLD}[~] Analyzing image: {Colors.CYAN}{image_path}{Colors.RESET}")
        separator()

        result = {"path": image_path, "exif": {}, "reverse_search_urls": []}

        if not os.path.exists(image_path):
            print_status(f"File not found: {image_path}", "error")
            return result

        file_size = os.path.getsize(image_path)
        result["file_size_bytes"] = file_size
        print_status(f"File size: {file_size / 1024:.1f} KB", "info")

        # Try Pillow for EXIF
        exif_data = self._extract_exif_pillow(image_path)
        if exif_data:
            result["exif"] = exif_data

        # GPS coordinates
        if "gps_latitude" in result["exif"] and "gps_longitude" in result["exif"]:
            lat = result["exif"]["gps_latitude"]
            lon = result["exif"]["gps_longitude"]
            print_status(f"GPS coordinates found: {lat}, {lon}", "found")
            result["exif"]["google_maps_url"] = f"https://maps.google.com/?q={lat},{lon}"
            print(f"    → {Colors.CYAN}{result['exif']['google_maps_url']}{Colors.RESET}")
        else:
            print_status("No GPS data found in image", "notfound")

        # Show key EXIF fields
        important = ["Make", "Model", "DateTime", "Software", "Artist", "Copyright"]
        for field in important:
            if field in result["exif"]:
                print_status(f"EXIF {field}: {result['exif'][field]}", "found")

        # Reverse image search URLs (user opens these in browser)
        result["reverse_search_urls"] = self._reverse_search_links(image_path)
        print(f"\n  {Colors.BOLD}Reverse Image Search Links:{Colors.RESET}")
        for engine, url in result["reverse_search_urls"].items():
            print(f"  {Colors.DIM}•{Colors.RESET} {engine:<12} {Colors.CYAN}{url}{Colors.RESET}")

        return result

    def _extract_exif_pillow(self, image_path: str) -> dict:
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS
            img = Image.open(image_path)
            raw_exif = img._getexif()
            if not raw_exif:
                return {}
            exif = {}
            for tag_id, value in raw_exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    gps = {}
                    for gps_id, gps_val in value.items():
                        gps_tag = GPSTAGS.get(gps_id, gps_id)
                        gps[gps_tag] = gps_val
                    # Convert to decimal degrees
                    if "GPSLatitude" in gps and "GPSLongitude" in gps:
                        lat = self._dms_to_decimal(gps["GPSLatitude"], gps.get("GPSLatitudeRef", "N"))
                        lon = self._dms_to_decimal(gps["GPSLongitude"], gps.get("GPSLongitudeRef", "E"))
                        exif["gps_latitude"] = round(lat, 6)
                        exif["gps_longitude"] = round(lon, 6)
                    exif["GPSInfo"] = {k: str(v) for k, v in gps.items()}
                else:
                    exif[str(tag)] = str(value)
            return exif
        except ImportError:
            print_status("Pillow not installed. Install with: pip install Pillow", "warning")
            return {}
        except Exception as ex:
            if self.verbose:
                print_status(f"EXIF extraction error: {ex}", "warning")
            return {}

    def _dms_to_decimal(self, dms, ref) -> float:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        decimal = degrees + minutes / 60 + seconds / 3600
        if ref in ["S", "W"]:
            decimal = -decimal
        return decimal

    def _reverse_search_links(self, image_path: str) -> dict:
        # For local files, point user to upload pages
        return {
            "Google":  "https://images.google.com/  (use 'Search by image' → upload)",
            "TinEye":  "https://tineye.com/  (drag & drop your image)",
            "Yandex":  "https://yandex.com/images/  (camera icon → upload)",
            "Bing":    "https://www.bing.com/visualsearch  (upload image)",
        }

    # ------------------------------------------------------------------ #
    # Search for profile images by username                               #
    # ------------------------------------------------------------------ #
    def search_by_username(self, username: str) -> dict:
        print(f"\n{Colors.BOLD}[~] Profile image lookup for: {Colors.CYAN}{username}{Colors.RESET}")
        separator()

        # Public avatar endpoints (no auth required)
        endpoints = {
            "GitHub":     f"https://github.com/{username}.png",
            "Gravatar":   self._gravatar_url(username),
            "Reddit":     f"https://www.reddit.com/user/{username}/about.json",
        }

        result = {"username": username, "image_urls": {}}
        import requests
        for platform, url in endpoints.items():
            try:
                r = requests.head(url, timeout=8, allow_redirects=True,
                                  headers={"User-Agent": "psint/1.0"})
                if r.status_code == 200:
                    result["image_urls"][platform] = url
                    print_status(f"Profile image on {platform}: {url}", "found")
                else:
                    if self.verbose:
                        print_status(f"No image on {platform}", "notfound")
            except Exception:
                pass

        return result

    def _gravatar_url(self, username: str) -> str:
        import hashlib
        h = hashlib.md5(username.lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{h}?d=404"
