"""Utility helpers for PSINT."""
import sys
import datetime

class Colors:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

    @classmethod
    def disable(cls):
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ""
        cls.MAGENTA = cls.CYAN = cls.WHITE = ""
        cls.BOLD = cls.DIM = cls.RESET = ""

_STATUS_ICONS = {
    "info":    ("*", Colors.BLUE),
    "success": ("+", Colors.GREEN),
    "warning": ("!", Colors.YELLOW),
    "error":   ("-", Colors.RED),
    "found":   ("✓", Colors.GREEN),
    "notfound":("✗", Colors.RED),
}

def print_status(message: str, level: str = "info"):
    icon, color = _STATUS_ICONS.get(level, ("*", Colors.BLUE))
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{ts}]{Colors.RESET} {color}[{icon}]{Colors.RESET} {message}")

def separator(char="─", width=65, color=Colors.DIM):
    print(f"{color}{char * width}{Colors.RESET}")
