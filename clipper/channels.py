"""Per-channel config: one streamer (or crew) per YouTube channel. Edit channels.json to add more."""
import json

from . import ROOT


def load_all() -> dict:
    return json.loads((ROOT / "channels.json").read_text())


def get(name: str) -> dict:
    all_ = load_all()
    if name not in all_:
        raise SystemExit(f"Unknown channel '{name}'. Options: {', '.join(all_)} (edit channels.json to add one)")
    cfg = dict(all_[name])
    cfg["key"] = name
    return cfg
