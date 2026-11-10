"""Automated iShowSpeed-style Shorts clipper.

Pipeline: ingest (yt-dlp) -> transcribe (faster-whisper) -> moments (Claude API)
-> library (SQLite) -> EDL builder (format presets) -> render (ffmpeg).
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
STYLES = ROOT / "styles"


# Homebrew's plain `ffmpeg` (9.x) ships WITHOUT libass/freetype, so the `ass` caption filter is missing
# and every render fails. Prefer a libass-enabled build (Homebrew `ffmpeg-full`, keg-only) when present.
FFMPEG_DIRS = ("/opt/homebrew/opt/ffmpeg-full/bin", "/usr/local/opt/ffmpeg-full/bin")


def prefer_full_ffmpeg(dirs=FFMPEG_DIRS, env=os.environ):
    for d in dirs:
        if os.path.isfile(os.path.join(d, "ffmpeg")):
            parts = env.get("PATH", "").split(os.pathsep)
            if d not in parts:
                env["PATH"] = os.pathsep.join([d, *parts])
            return d
    return None


prefer_full_ffmpeg()


# $ per million tokens (input, output) - Anthropic list prices; used only for the spend log
PRICES = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-haiku-5-5": (0.10, 0.50)}


def log_usage(resp, what: str, channel: str = "speed") -> float:
    """Append one Claude call's tokens + $ to data/<channel>/api_usage.jsonl; returns the $ for that call."""
    import datetime as _dt
    import json as _json
    from pathlib import Path as _P
    try:
        u = resp.usage
        model = getattr(resp, "model", "") or ""
        pin, pout = next((v for k, v in PRICES.items() if model.startswith(k)), (4.0, 20.0))
        cw = getattr(u, "cache_creation_input_tokens", 0) or 0
        cr = getattr(u, "cache_read_input_tokens", 0) or 0
        read_x = 0.05 if model.startswith("claude-opus-5-5") else 0.1  # cache read price multiplier (Opus 5.5 = 0.05x)
        inp = (u.input_tokens or 0) + cw * 1.25 + cr * read_x
        usd = inp * pin / 1e6 + (u.output_tokens or 0) * pout / 1e6
        f = _P(__file__).resolve().parent.parent / "data" / channel / "api_usage.jsonl"
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(f, "a") as fh:
            fh.write(_json.dumps({"utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"), "what": what,
                                  "model": model, "in": u.input_tokens, "cache_w": cw, "cache_r": cr, "out": u.output_tokens, "usd": round(usd, 5)}) + "\n")
        return usd
    except Exception:
        return 0.0
