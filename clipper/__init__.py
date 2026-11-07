"""Automated iShowSpeed-style Shorts clipper.

Pipeline: ingest (yt-dlp) -> transcribe (faster-whisper) -> moments (Claude API)
-> library (SQLite) -> EDL builder (format presets) -> render (ffmpeg).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
STYLES = ROOT / "styles"
