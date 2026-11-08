"""CLI.

  python -m clipper --channel speed auto          # DAILY: scout new streams/clips, clip, render, review.html
  python -m clipper --channel speed review        # approve + schedule posts (YouTube/TikTok/IG via Blotato)
  python -m clipper --channel speed run <vod_url> [--section 01:00:00-01:45:00] [--count 3]
  python -m clipper --channel kai   comp [--skill reflexes]
  python -m clipper --channel core  skills
  python -m clipper demo           # offline end-to-end test on synthetic footage

One YouTube channel per streamer: see channels.json (handle, hashtags, credit per channel).
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
from . import channels, library
from .render import render
from .style import load

OUT = ROOT / "out"
CH: dict = {}


def load_env() -> None:
    """Read KEY=VALUE lines from .env (created by tools/setup_mac.sh) without overriding the shell."""
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def notify(msg: str) -> None:
    """macOS notification (no-op elsewhere)."""
    if sys.platform == "darwin":
        import subprocess
        subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "Clipper"'], check=False)


def pick_music(kind: str = "phonk") -> str | None:
    """assets/music/<kind>/: your own licensed tracks are preferred over the placeholder loops."""
    tracks = [p for p in (ASSETS / "music" / kind).glob("*") if p.suffix.lower() in {".wav", ".mp3", ".m4a"}]
    real = [p for p in tracks if not p.name.startswith("placeholder")]
    pool = real or tracks
    return str(random.choice(pool)) if pool else None


def ensure_assets() -> None:
    if not (ASSETS / "sfx" / "bass_thud.wav").exists() or not list((ASSETS / "music" / "emotional").glob("*")):
        sys.path.insert(0, str(ROOT / "tools"))
        import make_audio_assets
        make_audio_assets.main()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "clip"


def day_dir() -> Path:
    d = OUT / CH["key"] / dt.date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_post(d: Path, entry: dict) -> None:
    f = d / "posts.json"
    posts = json.loads(f.read_text()) if f.exists() else []
    posts.append(entry)
    f.write_text(json.dumps(posts, indent=2, ensure_ascii=False))


def vision_filter(cands: list[dict], want: int) -> list[dict]:
    """Visual QA: drop moments that are boring to watch, fix payoff timing. CLIPPER_VISION=0 to skip."""
    if os.environ.get("CLIPPER_VISION", "1") != "1":
        return cands[:want]
    from .vision import check
    kept = []
    for m in cands:
        r = check(m, CH)
        print(f"  vision: {'KEEP' if r['keep'] else 'DROP'} ({r.get('visual_score')}) {r['reason'][:90]}")
        if r["keep"]:
            if r.get("payoff_t") is not None:
                m["payoff_t"] = r["payoff_t"]
            m["visual_score"] = r.get("visual_score")
            kept.append(m)
        else:
            library.mark_used([m["_id"]])  # don't offer it again
        if len(kept) >= want:
            break
    return kept


def render_single(m: dict, handle: str, d: Path) -> Path:
    style = load()
    wholesome = m.get("type") == "wholesome"
    edl = E.single_moment(m, style, handle, pick_music("emotional" if wholesome else "phonk"))
    name = f"{dt.datetime.now():%H%M%S}_{slug(m.get('hook_tag', 'moment'))}.mp4"
    out = render(edl, style, d / name)
    write_post(d, {"file": out.name, "format": edl["format"], "titles": m.get("titles", []),
                   "description": f"{CH['credit']}\n{CH['hashtags']}",  # (title-casing the hook turned KFC into "Kfc")
                   "virality": m.get("virality"), "why": m.get("why"), "source": m.get("source", ""),
                   "type": m.get("type"), "hook_tag": m.get("hook_tag"), "people": m.get("people", []),
                   "duration": round(sum((p["end"] - p["start"]) / p.get("speed", 1) for p in edl["pieces"]), 1)})
    return out


def write_review(d: Path) -> Path:
    """Simple approval page: every rendered Short with its titles, score and why."""
    import html
    f = d / "posts.json"
    posts = json.loads(f.read_text()) if f.exists() else []
    cards = []
    for p in posts:
        titles = "".join(f"<li>{html.escape(t)}</li>" for t in p.get("titles", []))
        cards.append(f"""<div class=c><video src="{html.escape(p['file'])}" controls preload=metadata></video>
<div class=m><b>{html.escape(p.get('format', ''))}</b> · score {p.get('virality', '-')}<br><small>{html.escape(p.get('why') or '')}</small>
<ol>{titles}</ol><small>{html.escape(p.get('source', ''))}</small></div></div>""")
    page = f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Review {CH.get('key')} {d.name}</title>
<style>body{{font-family:system-ui;background:#111;color:#eee;margin:16px}}.g{{display:flex;flex-wrap:wrap;gap:16px}}
.c{{width:300px;background:#1c1c1c;border-radius:10px;overflow:hidden}}video{{width:300px;aspect-ratio:9/16;background:#000}}
.m{{padding:10px;font-size:14px}}ol{{padding-left:18px}}</style>
<h2>{CH.get('key')} · {d.name} · {len(posts)} Shorts. Post the best, delete the rest.</h2><div class=g>{''.join(cards)}</div>"""
    out = d / "review.html"
    out.write_text(page, encoding="utf-8")
    return out


def process_file(src: Path, meta: dict, hint: str = "") -> list[dict]:
    from .moments import find_moments
    from .transcribe import transcribe
    tr = transcribe(src, meta["vod_key"])
    ctx = f"{meta.get('title', '')} ({meta.get('upload_date', '')}){' | ' + hint if hint else ''}"
    ms = find_moments(tr, ctx, CH)
    for m in ms:
        m["source"] = f"{meta.get('url', '')} {meta.get('section') or ''}".strip()
    library.add(meta["vod_key"], src, ms)
    return ms


def seen_path() -> Path:
    return ROOT / "data" / CH["key"] / "seen.json"


def seen() -> set:
    f = seen_path()
    return set(json.loads(f.read_text())) if f.exists() else set()


def mark_seen(ids: set) -> None:
    f = seen_path()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(sorted(seen() | ids)))


def autopost(d: Path, rendered: list, n: int, min_virality: int) -> int:
    """Night mode: post the strongest N immediately (no human awake). Only very strong moments
    that also passed the visual check qualify; everything else waits for morning approval."""
    from . import publish
    posts = {p["file"]: p for p in json.loads((d / "posts.json").read_text())}
    platforms = [p for p, acc in CH.get("blotato", {}).items() if acc] or ["youtube"]
    ranked = sorted(rendered, key=lambda r: (r[0].get("virality", 0), r[0].get("visual_score") or 0), reverse=True)
    done = 0
    for m, out in ranked:
        if done >= n:
            break
        vs = m.get("visual_score")
        if m.get("virality", 0) < min_virality or (vs is not None and vs < 7):
            continue
        post = posts.get(out.name)
        if not post or not post.get("titles"):
            continue
        try:
            res = publish.approve(CH, d, post, post["titles"][0], platforms, when="now")
            print(f"  AUTO-POSTED {out.name} → {res['platforms']}{' (dry run)' if res.get('dry_run') else ''}")
            done += 1
        except Exception as e:
            print(f"  autopost failed for {out.name}: {e}")
    return done


def cmd_auto(a) -> None:
    """Daily one-liner: scout new streams/clips for this channel, find moments, render the best, write review.html."""
    from . import scout
    from .ingest import download
    ensure_assets()
    learn_from_results()
    src_cfg = CH.get("sources", {})
    done, new_ids = seen(), set()
    if src_cfg.get("youtube_streams"):
        # YouTube only shows "Most replayed" on a stream some weeks after it airs, so the newest streams
        # usually have no heatmap. Look further back and clip the newest unseen streams that HAVE one;
        # too-new streams stay unseen and are picked up on a later day.
        used = 0
        for st in scout.latest_streams(src_cfg["youtube_streams"], a.lookback):
            if used >= a.streams:
                break
            if st["id"] in done:
                continue
            print(f"stream: {st['title'][:70]}")
            meta, peaks = scout.stream_peaks(st["url"], a.peaks)
            if not peaks:
                print("  no 'Most replayed' data yet (too new?) -> skipping for now")
                continue
            used += 1
            for s0, s1, v in peaks:
                sec = f"{scout.fmt(s0)}-{scout.fmt(s1)}"
                print(f"  peak {sec} (replay score {v})")
                f, m = download(st["url"], sec, meta)
                process_file(f, m, hint=f"this window is a 'Most replayed' peak (score {v}) - the best moment is inside it")
            new_ids.add(st["id"])
    for login in src_cfg.get("twitch_clips", []):
        for clip in scout.twitch_top_clips(login, a.clips, a.range):
            if clip["id"] in done:
                continue
            print(f"clip: {clip['title'][:60]} ({clip['views']} views)")
            f, m = download(clip["url"])
            process_file(f, m, hint=f"fan-made Twitch clip with {clip['views']} views - a proven moment; tighten it to the payoff")
            new_ids.add(clip["id"])
    mark_seen(new_ids)
    best = vision_filter(library.top(None, a.count * 2, a.min_virality), a.count)
    d = day_dir()
    print(f"rendering {len(best)} Shorts...")
    rendered = []
    for m in best:
        out = render_single(m, a.handle, d)
        print("  ->", out)
        rendered.append((m, out))
    library.mark_used([m["_id"] for m in best])
    review = write_review(d)
    print(f"REVIEW: open {review}")
    posted = autopost(d, rendered, a.autopost, a.autopost_min) if a.autopost else 0
    waiting = len(best) - posted
    msg = f"{CH['key']}: {posted} posted automatically, " if posted else f"{CH['key']}: "
    notify(msg + f"{waiting} Shorts waiting for approval (localhost:8765)")
    if a.serve and best:
        from .review_server import serve
        serve(CH, d, 8765, open_browser=True, timeout_h=12)


def cmd_run(a) -> None:
    from .ingest import download

    ensure_assets()
    print("1/4 downloading...")
    src, meta = download(a.url, a.section)
    print("2-3/4 transcribing + finding moments...")
    ms = process_file(src, meta)
    print(f"   {len(ms)} moments stored; virality: {sorted([m['virality'] for m in ms], reverse=True)}")
    best = vision_filter(library.top(meta["vod_key"], a.count * 2, a.min_virality), a.count)
    print(f"4/4 rendering {len(best)} Shorts...")
    d = day_dir()
    for m in best:
        print("   ->", render_single(m, a.handle, d))
    library.mark_used([m["_id"] for m in best])
    print(f"REVIEW: open {write_review(d)}")


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
    edl = E.subversion_comp(claim, fails[0], wins[:5], style, a.handle, pick_music(), name=CH["short"])
    d = day_dir()
    out = render(edl, style, d / f"{dt.datetime.now():%H%M%S}_comp-{slug(skill)}.mp4")
    write_post(d, {"file": out.name, "format": "subversion_comp", "titles": [edl["title"]],
                   "description": f"{CH['credit']}\n{CH['hashtags']}", "type": "skill", "hook_tag": claim,
                   "duration": round(sum((p["end"] - p["start"]) / p.get("speed", 1) for p in edl["pieces"]), 1)})
    library.mark_used([fails[0]["_id"]] + [w["_id"] for w in wins[:5]])
    print("->", out)


def cmd_review(a) -> None:
    from .review_server import latest_day, serve
    base = OUT / CH["key"]
    day = base / a.date if a.date else latest_day(base)
    if not day or not (day / "posts.json").exists():
        print(f"Nothing to review in {base}. Run: python -m clipper --channel {CH['key']} auto")
        return
    serve(CH, day, a.port, open_browser=not a.no_browser, timeout_h=a.hours)


def cmd_accounts(a) -> None:
    from . import blotato
    if blotato.dry_run():
        print("Set BLOTATO_API_KEY in .env first (Blotato > Settings > API).")
        return
    for acc in blotato.accounts():
        print(json.dumps(acc, ensure_ascii=False))
    print(f"\nCopy the ids for this channel's YouTube / TikTok / Instagram into channels.json → {CH['key']} → blotato.")


def learn_from_results() -> None:
    """Measure posted Shorts (48h / 7d) and refresh learnings.md that steers moment picking."""
    from . import performance
    try:
        n = performance.collect(CH)
        txt = performance.write_learnings(CH)
        if n or txt:
            print(f"learning: {n} new measurements; {'learnings updated' if txt else 'not enough data yet'}")
    except Exception as e:  # never block the daily run
        print(f"learning skipped: {e}")


def cmd_stats(a) -> None:
    from . import performance, publish
    learn_from_results()
    st = publish.load_state(CH)
    rows = []
    for k, e in st.items():
        if e.get("status") in ("posted", "scheduled"):
            v = {p: (s.get("168h") or s.get("48h") or {}).get("views") for p, s in e.get("stats", {}).items()}
            rows.append((e.get("utc", "")[:16], e.get("title", "")[:50], v))
    for when, title, v in sorted(rows):
        print(f"{when}  {title:50s}  " + "  ".join(f"{p}:{n:,}" for p, n in v.items() if n is not None))
    txt = performance.load_learnings(CH)
    print("\n" + (txt or f"Need {performance.MIN_FOR_LEARNINGS}+ measured Shorts (48h after posting) before learnings kick in."))


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
    print("REVIEW:", write_review(d))


def main() -> None:
    ap = argparse.ArgumentParser(prog="clipper")
    ap.add_argument("--channel", default=os.environ.get("CLIPPER_CHANNEL", "speed"), help="key in channels.json")
    ap.add_argument("--handle", help="override the channel's watermark handle")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("url")
    r.add_argument("--section", help="HH:MM:SS-HH:MM:SS (download only this part)")
    r.add_argument("--count", type=int, default=3)
    r.add_argument("--min-virality", type=int, default=7)
    c = sub.add_parser("comp")
    c.add_argument("--skill")
    au = sub.add_parser("auto", help="scout + clip + render + review page (run daily)")
    au.add_argument("--count", type=int, default=4)
    au.add_argument("--min-virality", type=int, default=7)
    au.add_argument("--streams", type=int, default=2, help="YouTube: clip the newest N streams that have 'Most replayed' data")
    au.add_argument("--lookback", type=int, default=12, help="YouTube: how many recent streams to search for those")
    au.add_argument("--peaks", type=int, default=8, help="YouTube: 'Most replayed' peaks per stream")
    au.add_argument("--clips", type=int, default=10, help="Twitch: top N clips per streamer")
    au.add_argument("--range", default="7d", choices=["24hr", "7d", "30d"])
    au.add_argument("--serve", action="store_true", help="after rendering, keep the approve page up for 12h")
    au.add_argument("--autopost", type=int, default=0, help="night mode: post the best N immediately, no approval")
    au.add_argument("--autopost-min", type=int, default=8, help="minimum virality score to auto-post")
    rv = sub.add_parser("review", help="approve-and-post page on http://localhost:8765")
    rv.add_argument("--date", help="YYYY-MM-DD (default: latest)")
    rv.add_argument("--port", type=int, default=8765)
    rv.add_argument("--hours", type=float, default=0, help="auto-stop after N hours (0 = until Ctrl+C)")
    rv.add_argument("--no-browser", action="store_true")
    sub.add_parser("accounts", help="list Blotato accounts (to fill channels.json → blotato)")
    sub.add_parser("stats", help="views of posted Shorts + what the channel has learned")
    sub.add_parser("skills")
    sub.add_parser("demo")
    load_env()
    a = ap.parse_args()
    CH.update(channels.get(a.channel))
    a.handle = a.handle or CH["handle"]
    library.CHANNEL = a.channel
    if a.cmd == "demo":
        library.CHANNEL = CH["key"] = "demo"
    {"run": cmd_run, "auto": cmd_auto, "review": cmd_review, "accounts": cmd_accounts, "stats": cmd_stats, "comp": cmd_comp, "skills": cmd_skills, "demo": cmd_demo}[a.cmd](a)


if __name__ == "__main__":
    main()
