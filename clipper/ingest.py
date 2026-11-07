"""Download a VOD (or a section of it) with yt-dlp."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from . import ROOT

VODS = ROOT / "data" / "vods"


def _section_tag(section: str | None) -> str:
    return "" if not section else "_" + re.sub(r"[^0-9]", "", section)


def info(url: str) -> dict:
    out = subprocess.run(["yt-dlp", "--ignore-config", "-J", "--no-warnings", url], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    return {"id": j["id"], "title": j.get("title", ""), "upload_date": j.get("upload_date", ""),
            "duration": j.get("duration"), "channel": j.get("channel", ""), "url": url}


def download(url: str, section: str | None = None, meta: dict | None = None) -> tuple[Path, dict]:
    """section: 'HH:MM:SS-HH:MM:SS' to grab only part of a long stream (much faster)."""
    meta = dict(meta) if meta else info(url)
    VODS.mkdir(parents=True, exist_ok=True)
    out = VODS / f"{meta['id']}{_section_tag(section)}.mp4"
    meta["section"] = section
    meta["vod_key"] = out.stem
    if out.exists():
        return out, meta
    cmd = ["yt-dlp", "--ignore-config", "--no-warnings", "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b",
           "--merge-output-format", "mp4", "-o", str(out), url]
    if section:
        cmd[1:1] = ["--download-sections", f"*{section}", "--force-keyframes-at-cuts"]
    subprocess.run(cmd, check=True)
    return out, meta
