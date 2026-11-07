"""CLI.

  python -m clipper run <vod_url> [--section 01:00:00-01:45:00] [--count 3] [--handle @x]
  python -m clipper comp [--skill reflexes]
  python -m clipper skills
  python -m clipper demo           # offline end-to-end test on synthetic footage
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import sys
from pathlib import Path

from . import ASSETS, ROOT
from . import edl as E
from . import library
from .render import render
from .style import load

OUT = ROOT / "out"
CREDIT = "Credit: iShowSpeed (youtube.com/@IShowSpeed). Fan edit, not affiliated."


def pick_music() -> str | None:
    tracks = [p for p in (ASSETS / "music").glob("*") if p.suffix.lower() in {".wav", ".mp3", ".m4a"}]
    real = [p for p in tracks if not p.name.startswith("placeholder")]
    pool = real or tracks
    return str(random.choice(pool)) if pool else None


def ensure_assets() -> None:
    if not (ASSETS / "sfx" / "bass_thud.wav").exists() or not list((ASSETS / "music").glob("*")):
        sys.path.insert(0, str(ROOT / "tools"))
        import make_audio_assets
        make_audio_assets.main()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "clip"


def day_dir() -> Path:
    d = OUT / dt.date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_post(d: Path, entry: dict) -> None:
    f = d / "posts.json"
    posts = json.loads(f.read_text()) if f.exists() else []
    posts.append(entry)
    f.write_text(json.dumps(posts, indent=2, ensure_ascii=False))


def render_single(m: dict, handle: str, d: Path) -> Path:
    style = load()
    edl = E.single_moment(m, style, handle, pick_music())
    name = f"{dt.datetime.now():%H%M%S}_{slug(m.get('hook_tag', 'moment'))}.mp4"
    out = render(edl, style, d / name)
    write_post(d, {"file": out.name, "format": "single_moment", "titles": m.get("titles", []),
                   "description": f"{m.get('hook_tag', '').title()}\n\n{CREDIT}\n#ishowspeed #speed #shorts",
                   "virality": m.get("virality"), "why": m.get("why")})
    return out


def cmd_run(a) -> None:
    from .ingest import download
    from .moments import find_moments
    from .transcribe import transcribe

    ensure_assets()
    print("1/4 downloading...")
    src, meta = download(a.url, a.section)
    print("2/4 transcribing...")
    tr = transcribe(src, meta["vod_key"])
    print(f"3/4 finding moments ({len(tr['segments'])} segments)...")
    ms = find_moments(tr, f"{meta['title']} ({meta['upload_date']})")
    library.add(meta["vod_key"], src, ms)
    print(f"   {len(ms)} moments stored; virality: {sorted([m['virality'] for m in ms], reverse=True)}")
    best = library.top(meta["vod_key"], a.count, a.min_virality)
    print(f"4/4 rendering {len(best)} Shorts...")
    d = day_dir()
    for m in best:
        print("   ->", render_single(m, a.handle, d))
    library.mark_used([m["_id"] for m in best])
    print(f"done: {d}/  (titles in posts.json)")


def cmd_comp(a) -> None:
    ensure_assets()
    style = load()
    counts = library.skill_counts()
    skill = a.skill
    if not skill:
        ok = [s for s, f, sc in counts if (f or 0) >= 1 and (sc or 0) >= 5]
        if not ok:
            print("Not enough moments yet for a comp (need 1 fail + 5 successes of one skill). Have:")
            for s, f, sc in counts:
                print(f"  {s:15s} fail={f} success={sc}")
            return
        skill = ok[0]
    fails, wins = library.by_skill(skill, "fail"), library.by_skill(skill, "success")
    if not fails or len(wins) < 5:
        print(f"{skill}: need 1 fail + 5 successes, have {len(fails)} + {len(wins)}")
        return
    claim = {"reflexes": "has slow reflexes", "strength": "isnt strong", "aura": "has no aura"}.get(skill, f"cant {skill}")
    edl = E.subversion_comp(claim, fails[0], wins[:5], style, a.handle, pick_music())
    d = day_dir()
    out = render(edl, style, d / f"{dt.datetime.now():%H%M%S}_comp-{slug(skill)}.mp4")
    write_post(d, {"file": out.name, "format": "subversion_comp", "titles": [edl["title"]],
                   "description": f"{CREDIT}\n#ishowspeed #speed #shorts"})
    library.mark_used([fails[0]["_id"]] + [w["_id"] for w in wins[:5]])
    print("->", out)


def cmd_skills(a) -> None:
    for s, f, sc in library.skill_counts():
        print(f"{s:15s} fail={f} success={sc}")


def cmd_demo(a) -> None:
    """Offline: synthetic VOD + fake moments -> library -> single + comp renders."""
    import subprocess
    ensure_assets()
    src = ROOT / "data" / "vods" / "demo.mp4"
    src.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30:duration=150",
                        "-f", "lavfi", "-i", "sine=frequency=220:duration=150", "-c:v", "libx264", "-preset", "ultrafast",
                        "-c:a", "aac", "-shortest", str(src)], check=True)
    rng = random.Random(2)
    words = []
    t = 5.0
    while t < 145:
        words.append({"w": rng.choice("bro no way chat look speed is crazy watch this".split()), "s": round(t, 2), "e": round(t + 0.28, 2)})
        t += 0.35 + (rng.uniform(0.8, 2) if rng.random() < 0.05 else 0)
    ms = [{"start": 5, "end": 35, "payoff_t": 31, "impact_ts": [], "type": "funny", "skill": "none", "outcome": "na",
           "people": ["Speed"], "hook_tag": "DEMO HOOK TAG", "action_tags": [{"t": 20, "text": "WAIT FOR IT"}], "emoji": "😂",
           "comedic": True, "virality": 9, "titles": ["Demo title 😭💀"], "why": "demo", "words": [w for w in words if 5 <= w["s"] < 35]}]
    ms.append({"start": 40, "end": 46, "payoff_t": 43, "impact_ts": [43], "type": "skill", "skill": "reflexes", "outcome": "fail",
               "people": [], "hook_tag": "", "action_tags": [], "emoji": "💀", "comedic": False, "virality": 6, "titles": [], "why": "", "words": []})
    for i in range(5):
        s = 50 + i * 15
        ms.append({"start": s, "end": s + 8, "payoff_t": s + 4, "impact_ts": [s + 4], "type": "skill", "skill": "reflexes",
                   "outcome": "success", "people": [], "hook_tag": "", "action_tags": [], "emoji": "🤯", "comedic": False,
                   "virality": 6, "titles": [], "why": "", "words": []})
    library.add("demo", src, ms)
    a.count, a.min_virality = 1, 7
    d = day_dir()
    for m in library.top("demo", 1, 7):
        print("single ->", render_single(m, a.handle, d))
    a.skill = "reflexes"
    cmd_comp(a)


def main() -> None:
    ap = argparse.ArgumentParser(prog="clipper")
    ap.add_argument("--handle", default=os.environ.get("CLIPPER_HANDLE", "@yourhandle"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("url")
    r.add_argument("--section", help="HH:MM:SS-HH:MM:SS (download only this part)")
    r.add_argument("--count", type=int, default=3)
    r.add_argument("--min-virality", type=int, default=7)
    c = sub.add_parser("comp")
    c.add_argument("--skill")
    sub.add_parser("skills")
    sub.add_parser("demo")
    a = ap.parse_args()
    {"run": cmd_run, "comp": cmd_comp, "skills": cmd_skills, "demo": cmd_demo}[a.cmd](a)


if __name__ == "__main__":
    main()
