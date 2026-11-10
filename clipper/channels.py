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
    return with_window(cfg)


def with_window(cfg: dict, today=None) -> dict:
    """Dated overrides written in channels.json ("windows": [{"from", "to", "why", ...overrides}]), e.g. GTA 6
    launch week. Visible in the config, no hidden schedule: inside from..to (UTC dates, inclusive) the window's
    keys replace the channel's; rank_style is merged key by key."""
    import datetime as dt
    d = (today or dt.datetime.now(dt.timezone.utc).date()).isoformat()
    for w in cfg.get("windows", []):
        if w["from"] <= d <= w["to"]:
            for k, v in w.items():
                if k in ("from", "to", "why"):
                    continue
                cfg[k] = {**cfg.get(k, {}), **v} if k == "rank_style" else v
            cfg["active_window"] = w.get("why", f"{w['from']}..{w['to']}")
    return cfg
