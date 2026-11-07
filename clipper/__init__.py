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
