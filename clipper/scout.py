"""Find WHERE to clip using signals viewers already gave us.

- YouTube streams: the "Most replayed" heatmap (yt-dlp `heatmap`), so we clip only the peaks.
- Twitch: the channel's most-viewed community clips (fans already cut the best moments).

This means we transcribe ~10-25 min of footage per stream instead of 3-4 hours, and the
moments we pick are ones the audience already proved it rewatches.
"""
from __future__ import annotations

import json
import subprocess

PEAKS_PER_STREAM = 8
MIN_GAP_S = 150          # peaks closer than this merge
PAD_BEFORE, PAD_AFTER = 45, 20


def _ytdlp_json(url: str, flat: bool = False) -> dict:
    cmd = ["yt-dlp", "--ignore-config", "-J", "--no-warnings"] + (["--flat-playlist"] if flat else []) + [url]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


def latest_streams(streams_url: str, n: int = 3) -> list[dict]:
    """streams_url e.g. https://www.youtube.com/@IShowSpeed/streams -> newest first."""
    j = _ytdlp_json(streams_url, flat=True)
    out = []
    for e in (j.get("entries") or [])[: n * 3]:
        if e.get("live_status") in ("is_live", "is_upcoming"):
            continue
        out.append({"id": e["id"], "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}", "title": e.get("title", "")})
        if len(out) >= n:
            break
    return out


def heatmap_sections(heatmap: list[dict], duration: float, n: int = PEAKS_PER_STREAM) -> list[tuple[float, float, float]]:
    """Return [(start, end, score)] windows around the top 'Most replayed' peaks, in time order."""
    if not heatmap:
        return []
    pts = sorted(heatmap, key=lambda h: h["start_time"])
    vals = [h["value"] for h in pts]
    # real spikes only: local maximum, rising above at least one neighbour, and in the top quarter of the
    # stream's replay values. Ignore the first 2% (stream intros always spike).
    body = sorted(v for h, v in zip(pts, vals) if h["start_time"] >= duration * 0.02) or sorted(vals)
    p75 = body[int(0.75 * (len(body) - 1))]
    cands = []
    for i, h in enumerate(pts):
        if h["start_time"] < duration * 0.02:
            continue
        left = vals[i - 1] if i > 0 else -1
        right = vals[i + 1] if i + 1 < len(vals) else -1
        if vals[i] >= left and vals[i] >= right and vals[i] > min(left, right) and vals[i] > p75:
            cands.append(h)
    cands.sort(key=lambda h: -h["value"])
    chosen: list[dict] = []
    for h in cands:
        mid = (h["start_time"] + h["end_time"]) / 2
        if all(abs(mid - (c["start_time"] + c["end_time"]) / 2) >= MIN_GAP_S for c in chosen):
            chosen.append(h)
        if len(chosen) >= n:
            break
    out = []
    for h in chosen:
        s = max(0.0, h["start_time"] - PAD_BEFORE)
        e = min(duration, h["end_time"] + PAD_AFTER)
        out.append((round(s, 1), round(e, 1), round(h["value"], 3)))
    return sorted(out)


def stream_peaks(url: str, n: int = PEAKS_PER_STREAM) -> tuple[dict, list[tuple[float, float, float]]]:
    j = _ytdlp_json(url)
    meta = {"id": j["id"], "title": j.get("title", ""), "upload_date": j.get("upload_date", ""), "url": url,
            "duration": j.get("duration") or 0}
    return meta, heatmap_sections(j.get("heatmap") or [], meta["duration"], n)


def fmt(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def twitch_top_clips(login: str, n: int = 10, range_: str = "7d") -> list[dict]:
    """Most-viewed clips of a Twitch channel in the last 24hr/7d/30d."""
    url = f"https://www.twitch.tv/{login}/clips?filter=clips&range={range_}"
    j = _ytdlp_json(url, flat=True)
    entries = j.get("entries") or []
    clips = [{"id": e.get("id"), "url": e.get("url"), "title": e.get("title", ""), "views": e.get("view_count") or 0}
             for e in entries if e.get("url")]
    clips.sort(key=lambda c: -c["views"])  # Twitch already lists by views; this keeps it explicit
    return clips[:n]
