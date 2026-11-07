import json
from functools import lru_cache

from . import STYLES

EMOJI_FILES = {
    "💀": "skull", "🤯": "mindblown", "😭": "sob", "😂": "joy", "🥶": "cold",
    "❤️‍🩹": "mending_heart", "💖": "sparkle_heart", "🔥": "fire", "😳": "shocked",
}


@lru_cache(maxsize=None)
def load(name: str = "speed_v2") -> dict:
    return json.loads((STYLES / f"{name}.json").read_text())


def color(style: dict, key_or_hex: str) -> str:
    """Resolve a palette name ('yellow') or hex ('#FFD700') to hex."""
    if key_or_hex.startswith("#"):
        return key_or_hex
    return style["global"]["palette"][key_or_hex]


def emoji_name(e: str) -> str:
    return EMOJI_FILES.get(e, e)
