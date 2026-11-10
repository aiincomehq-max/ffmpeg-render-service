"""Learn from results: collect views of posted Shorts, then feed winners/losers back into moment picking.

  python -m clipper --channel speed stats     # also runs automatically at the start of every `auto`

How it works:
1. For every posted Short, ask Blotato for the live URL of each platform post (once).
2. After 48h (and again after 7 days), read views/likes/comments with yt-dlp (no API key needed).
3. Write data/<channel>/learnings.md: what won, what flopped, which formats/types/lengths do best,
   and how well the virality score predicted reality. moments.py adds it to Claude's instructions,
   so the channel's own results steer what gets clipped next.
"""
from __future__ import annotations

import datetime as dt
import json
import statistics
import subprocess
from collections import defaultdict

from . import ROOT, blotato, publish

CHECKPOINTS_H = [48, 168]  # measure at 2 days and 7 days
MIN_FOR_LEARNINGS = 4


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def fetch_stats(url: str) -> dict | None:
    """views/likes/comments for a public YouTube/TikTok/Instagram URL via yt-dlp."""
    try:
        out = subprocess.run(["yt-dlp", "--ignore-config", "-J", "--no-warnings", "--skip-download", url],
                             capture_output=True, text=True, timeout=120, check=True).stdout
        j = json.loads(out)
        return {"views": j.get("view_count") or 0, "likes": j.get("like_count") or 0,
                "comments": j.get("comment_count") or 0}
    except Exception:
        return None


def collect(ch: dict, fetch=fetch_stats, status=blotato.status, now: dt.datetime | None = None) -> int:
    """Update posted.json with live URLs + stats at each checkpoint. Returns number of new measurements."""
    now = now or _now()
    st = publish.load_state(ch)
    n = 0
    for key, e in st.items():
        if e.get("status") not in ("posted", "scheduled") or not e.get("utc"):
            continue
        t0 = dt.datetime.fromisoformat(e["utc"].replace("Z", "+00:00"))
        age_h = (now - t0).total_seconds() / 3600
        if age_h < CHECKPOINTS_H[0]:
            continue
        urls = e.setdefault("urls", {})
        stats = e.setdefault("stats", {})
        for plat, pid in (e.get("platforms") or {}).items():
            if not isinstance(pid, str) or pid.startswith(("ERROR", "dry-")):
                continue
            if plat not in urls:
                s = status(pid) or {}
                if s.get("publicUrl"):
                    urls[plat] = s["publicUrl"]
            if plat not in urls:
                continue
            due = [c for c in CHECKPOINTS_H if age_h >= c and f"{c}h" not in stats.get(plat, {})]
            if not due:
                continue
            got = fetch(urls[plat])
            if got:
                stats.setdefault(plat, {})[f"{max(due)}h"] = {**got, "at": now.isoformat(timespec="minutes")}
                n += 1
    publish.save_state(ch, st)
    return n


def _views(e: dict, plat: str = "youtube") -> int | None:
    s = e.get("stats", {}).get(plat, {})
    for k in ("168h", "48h"):
        if k in s:
            return s[k]["views"]
    return None


def learnings(ch: dict) -> str:
    """Markdown summary of what works on THIS channel. Empty if too little data."""
    st = publish.load_state(ch)
    rows = []
    for key, e in st.items():
        v = _views(e)
        if v is None:
            continue
        m = e.get("meta") or {}
        rows.append({"title": e.get("title", ""), "views": v, "format": m.get("format") or "?",
                     "type": m.get("type") or "?", "virality": m.get("virality"), "duration": m.get("duration"),
                     "hook": m.get("hook_tag") or "", "why": m.get("why") or "",
                     "origin": m.get("origin") or "?",
                     "clip_views": ("?" if not m.get("clip_views") else "<1k" if m["clip_views"] < 1000
                                    else "1k-5k" if m["clip_views"] < 5000 else "5k+")})
    if len(rows) < MIN_FOR_LEARNINGS:
        return ""
    rows.sort(key=lambda r: -r["views"])
    med = statistics.median(r["views"] for r in rows)
    lines = [f"YOUR CHANNEL'S OWN RESULTS ({len(rows)} Shorts measured, median {med:,.0f} views). Weight these heavily:",
             "Top performers (do MORE like these):"]
    for r in rows[:5]:
        lines.append(f'  {r["views"]:>10,} views | {r["format"]}/{r["type"]} | {r["duration"]}s | "{r["title"]}" | hook: {r["hook"]}')
    lines.append("Flops (do LESS like these):")
    for r in rows[-5:][::-1]:
        lines.append(f'  {r["views"]:>10,} views | {r["format"]}/{r["type"]} | {r["duration"]}s | "{r["title"]}" | hook: {r["hook"]}')

    def group(field):
        g = defaultdict(list)
        for r in rows:
            g[r[field]].append(r["views"])
        return sorted(((k, statistics.median(v), len(v)) for k, v in g.items()), key=lambda x: -x[1])

    # 10 Nov (Andrew): test new-stream estimates vs older 'Most replayed' streams vs Twitch clips, and whether the
    # source clip's own view count predicts the Short's views (decides the min_clip_views floor)
    for field, label in (("type", "Moment type"), ("format", "Format"), ("origin", "Source"),
                         ("clip_views", "Source clip views")):
        lines.append(f"{label} by median views: " + "; ".join(f"{k} {m:,.0f} (n={n})" for k, m, n in group(field)))
    lens = [(r["duration"], r["views"]) for r in rows if r["duration"]]
    if len(lens) >= MIN_FOR_LEARNINGS:
        short = [v for d, v in lens if d <= 30]
        long_ = [v for d, v in lens if d > 30]
        if short and long_:
            lines.append(f"Length: <=30s median {statistics.median(short):,.0f} vs >30s median {statistics.median(long_):,.0f}")
    pred = [(r["virality"], r["views"]) for r in rows if r["virality"] is not None]
    if len(pred) >= MIN_FOR_LEARNINGS:
        hi = [v for p, v in pred if p >= 8]
        lo = [v for p, v in pred if p < 8]
        if hi and lo:
            lines.append(f"Calibration: your virality>=8 picks median {statistics.median(hi):,.0f} vs <8 median "
                         f"{statistics.median(lo):,.0f}. Adjust your scoring if these are close or reversed.")
    return "\n".join(lines)


def write_learnings(ch: dict) -> str:
    txt = learnings(ch)
    f = ROOT / "data" / ch["key"] / "learnings.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    if txt:
        f.write_text(txt + "\n", encoding="utf-8")
    return txt


def load_learnings(ch: dict) -> str:
    f = ROOT / "data" / ch["key"] / "learnings.md"
    return f.read_text(encoding="utf-8") if f.exists() else ""
