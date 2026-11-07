"""Approve -> schedule -> post (YouTube Shorts, TikTok, Instagram Reels) via Blotato.

Slots come from channels.json `post_times` (UTC, so they don't depend on where the Mac is). Each approved Short takes the next free
slot, so approving 4 at once spreads them across the day instead of dumping them together.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from . import ROOT, blotato

PLATFORMS = ["youtube", "tiktok", "instagram"]


def state_path(ch: dict) -> Path:
    return ROOT / "data" / ch["key"] / "posted.json"


def load_state(ch: dict) -> dict:
    f = state_path(ch)
    return json.loads(f.read_text()) if f.exists() else {}


def save_state(ch: dict, st: dict) -> None:
    f = state_path(ch)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(st, indent=2, ensure_ascii=False))


def next_slot(ch: dict, st: dict, now: dt.datetime | None = None) -> dt.datetime:
    """Next post_times slot (UTC) that's >=15 min away and not already used."""
    now = now or dt.datetime.now(dt.timezone.utc)
    used = {v.get("slot") for v in st.values() if v.get("slot")}
    times = ch.get("post_times_utc") or ["14:00", "16:45", "19:00"]
    for day in range(0, 30):
        d = (now + dt.timedelta(days=day)).date()
        for hm in times:
            h, m = map(int, hm.split(":"))
            slot = dt.datetime(d.year, d.month, d.day, h, m, tzinfo=dt.timezone.utc)
            if slot >= now + dt.timedelta(minutes=15) and slot.isoformat() not in used:
                return slot
    raise RuntimeError("no free slot in 30 days")


def caption(platform: str, title: str, post: dict, ch: dict) -> str:
    if platform == "youtube":
        return post.get("description") or f"{ch['credit']}\n{ch['hashtags']}"
    # TikTok / Instagram: the caption IS the title + credit + tags
    return f"{title}\n\n{ch['credit']}\n{ch['hashtags']}"


def approve(ch: dict, day_dir: Path, post: dict, title: str, platforms: list[str], when: str = "slot") -> dict:
    """when: 'slot' (next free slot) or 'now'."""
    st = load_state(ch)
    key = f"{day_dir.name}/{post['file']}"
    if st.get(key, {}).get("status") in ("scheduled", "posted"):
        return st[key]
    ids = ch.get("blotato", {})
    missing = [p for p in platforms if not ids.get(p)]
    if missing and not blotato.dry_run():
        raise ValueError(f"No Blotato account id for {missing} in channels.json → blotato. Run: python -m clipper accounts")
    slot = None if when == "now" else next_slot(ch, st)
    iso = slot.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if slot else None
    log: list = []
    media_url = blotato.upload(day_dir / post["file"], log)
    results = {}
    for p in platforms:
        try:
            results[p] = blotato.create_post(p, ids.get(p, "DRY"), caption(p, title, post, ch), media_url, title, iso, log)
        except Exception as e:  # one platform failing shouldn't lose the others
            results[p] = f"ERROR: {e}"
    entry = {"status": "scheduled" if iso else "posted", "slot": slot.isoformat() if slot else None,
             "utc": iso, "title": title, "platforms": results, "dry_run": blotato.dry_run()}
    st[key] = entry
    save_state(ch, st)
    if log:
        with open(ROOT / "data" / ch["key"] / "dryrun_posts.jsonl", "a") as f:
            for item in log:
                f.write(json.dumps({"file": key, **item}, ensure_ascii=False) + "\n")
    return entry


def skip(ch: dict, day_dir: Path, post: dict) -> dict:
    st = load_state(ch)
    key = f"{day_dir.name}/{post['file']}"
    st[key] = {"status": "skipped"}
    save_state(ch, st)
    return st[key]
