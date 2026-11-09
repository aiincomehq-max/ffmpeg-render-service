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
    if section and _audio_short(out):  # 9 Nov: YouTube section + m4a audio sometimes stops early (75 s of 112 s)
        cmd[cmd.index("-f") + 1] = "bv*[height<=1080]+ba[ext=webm]/bv*[height<=1080]+ba"
        subprocess.run(cmd[:1] + ["--force-overwrites"] + cmd[1:], check=True)
    return out, meta


def _audio_short(path: Path) -> bool:
    """True when the audio track is clearly shorter than the video track."""
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True).stdout
        d = {l.split(",")[0]: float(l.split(",")[1]) for l in r.splitlines() if "," in l and l.split(",")[1] not in ("", "N/A")}
        return "audio" in d and "video" in d and d["audio"] < 0.95 * d["video"]
    except Exception:
        return False


def download_audio(url: str, meta: dict) -> Path:
    """Audio only (~175MB for a 3h stream vs ~7GB of 1080p video): used to SCAN a fresh stream for moments."""
    VODS.mkdir(parents=True, exist_ok=True)
    out = VODS / f"{meta['id']}_audio.m4a"
    if not out.exists():
        subprocess.run(["yt-dlp", "--ignore-config", "--no-warnings", "-f", "ba[ext=m4a]/ba", "-o", str(out), url],
                       check=True)
    return out


def restore(url: str, section: str | None, dest: Path) -> Path:
    """9 Nov: re-download a source clip the cleanup removed, to the exact path the moment records."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["yt-dlp", "--ignore-config", "--no-warnings", "-q", "--force-overwrites", "-f",
           "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b",
           "--merge-output-format", "mp4", "-o", str(dest), url]
    if section:
        cmd[1:1] = ["--download-sections", f"*{section}", "--force-keyframes-at-cuts"]
    subprocess.run(cmd, check=True)
    if section and _audio_short(dest):
        cmd[cmd.index("-f") + 1] = "bv*[height<=1080]+ba[ext=webm]/bv*[height<=1080]+ba"
        subprocess.run(cmd, check=True)
    return dest
