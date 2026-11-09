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


MUSIC_LOG = ROOT / "data" / "music_used.jsonl"


def pick_music(kind: str = "phonk") -> str | None:
    """'phonk' = the hype bed: assets/music/hiphop (YouTube Audio Library, no attribution) + the phonk loops.
    9 Nov: a track is never reused by the same channel within 14 days, nor by ANY channel within 3 days;
    if everything is blocked, the least recently used track wins. Every pick is logged to data/music_used.jsonl."""
    dirs = ["hiphop", "phonk"] if kind == "phonk" else [kind]
    pool = [p for d in dirs for p in (ASSETS / "music" / d).glob("*") if p.suffix.lower() in {".wav", ".mp3", ".m4a"}]
    if not pool:
        return None
    now = dt.datetime.now()
    last_any, last_mine = {}, {}
    if MUSIC_LOG.exists():
        for line in MUSIC_LOG.read_text().splitlines():
            try:
                r = json.loads(line); t = dt.datetime.fromisoformat(r["at"])
            except Exception:
                continue
            last_any[r["track"]] = max(last_any.get(r["track"], t), t)
            if r.get("channel") == CH.get("key"):
                last_mine[r["track"]] = max(last_mine.get(r["track"], t), t)
    ok = [p for p in pool if (now - last_mine.get(p.name, dt.datetime.min)).days >= 14
          and (now - last_any.get(p.name, dt.datetime.min)).days >= 3]
    pick = random.choice(ok) if ok else min(pool, key=lambda p: last_any.get(p.name, dt.datetime.min))
    MUSIC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(MUSIC_LOG, "a") as f:
        f.write(json.dumps({"at": now.isoformat(timespec="seconds"), "channel": CH.get("key"), "track": pick.name}) + "\n")
    return str(pick)


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


MIN_VISUAL = 6  # 8 Nov: a 5/10 'KEEP' was 43 s of a still anime image with Speed tiny in the corner


def vision_filter(cands: list[dict], want: int) -> list[dict]:
    """Visual QA: drop moments that are boring to watch, fix payoff timing. CLIPPER_VISION=0 to skip."""
    if os.environ.get("CLIPPER_VISION", "1") != "1":
        return cands[:want]
    from .vision import check
    kept = []
    for m in cands:
        r = check(m, CH)
        if r["keep"] and r.get("visual_score") is not None and r["visual_score"] < CH.get("min_visual", MIN_VISUAL):
            r["keep"] = False
        print(f"  vision: {'KEEP' if r['keep'] else 'DROP'} ({r.get('visual_score')}) {r['reason'][:90]}")
        if r["keep"]:
            if r.get("payoff_t") is not None:
                m["payoff_t"] = r["payoff_t"]
            m["visual_score"] = r.get("visual_score")
            m["burned_captions"] = bool(r.get("burned_captions"))
            if "_id" in m:
                library.update(m["_id"], payoff_t=m.get("payoff_t"), visual_score=m["visual_score"],
                               burned_captions=m["burned_captions"])
            kept.append(m)
        else:
            library.mark_used([m["_id"]])  # don't offer it again
        if len(kept) >= want:
            break
    return kept


def add_voice(edl: dict, lines_fn) -> None:
    """Our commentary (reused-content rule). Fails open: a Short without VO beats no Short."""
    from . import voice
    if not voice.enabled() or not edl.get("vo_slots"):
        return
    try:
        lines = lines_fn()[:len(edl["vo_slots"])]
        spoken = voice.speak(lines, voice=CH.get("vo_voice"), speed=CH.get("vo_speed"), el_voice=CH.get("el_voice"))  # own narrator per channel
        edl["voice"] = [{"t": t, "file": f, "text": l} for t, (f, _), l in zip(edl["vo_slots"], spoken, lines)]
        print("  voice:", " / ".join(lines))
    except Exception as e:
        print(f"  voice skipped ({type(e).__name__}: {str(e)[:80]})")


def render_single(m: dict, handle: str, d: Path) -> Path:
    style = load()
    wholesome = m.get("type") == "wholesome"
    edl = E.single_moment(m, style, handle, pick_music("emotional" if wholesome else "phonk"))
    from . import voice
    if CH.get("vo_mode", "full") != "none":  # 9 Nov: winners' single-clip Shorts have no narrator
        add_voice(edl, lambda: voice.single_lines(m, CH["key"]))
    else:  # ...so the situation is explained on screen instead, top of frame, whole Short
        try:
            line = voice.context_line(m, CH["key"])
            dur = sum((p["end"] - p["start"]) / p.get("speed", 1) for p in edl["pieces"])
            edl["texts"].insert(0, {"text": E.hook_text(line, 46), "start": 0.0, "end": round(dur, 3),
                                    "kind": "header", "color": "white", "y_pct": 9})
            print("  context:", line)
        except Exception as e:
            print(f"  context skipped ({type(e).__name__}: {str(e)[:80]})")
    name = f"{dt.datetime.now():%H%M%S}_{slug(m.get('hook_tag', 'moment'))}.mp4"
    out = render(edl, style, d / name)
    write_post(d, {"file": out.name, "format": edl["format"], "titles": m.get("titles", []),
                   "description": f"{CH['credit']}\n{CH['hashtags']}",  # (title-casing the hook turned KFC into "Kfc")
                   "virality": m.get("virality"), "why": m.get("why"), "source": m.get("source", ""),
                   "source_kind": m.get("source_kind", "heatmap"),
                   "type": m.get("type"), "hook_tag": m.get("hook_tag"), "people": m.get("people", []),
                   "moment_ids": [m["_id"]] if "_id" in m else [],
                   "duration": round(sum((p["end"] - p["start"]) / p.get("speed", 1) for p in edl["pieces"]), 1)})
    return out


RANK_N = 5


def render_ranking(group: list[dict], handle: str, d: Path) -> Path:
    """group sorted weakest -> strongest; the strongest plays last as #1."""
    style = load()
    game = CH.get("short", "gaming")
    look = CH.get("rank_style", {})
    edl = E.ranking_comp(group, game, handle, pick_music("phonk"), look)
    from . import voice
    if CH.get("vo_mode", "full") == "countdown":  # 9 Nov: rank calls only, the streamer's audio carries the clip
        add_voice(edl, lambda: voice.countdown_calls(len(group), look))
    elif CH.get("vo_mode", "full") != "none":
        add_voice(edl, lambda: voice.ranking_lines(group, game, CH["key"], look.get("vo_opener", "Number {n}.")))
    out = render(edl, style, d / f"{dt.datetime.now():%H%M%S}_ranking-{slug(game)}.mp4")
    write_post(d, {"file": out.name, "format": "ranking_comp",
                   "titles": [t.format(game=game) for t in look.get("titles", [])] or [edl["title"], f"Top 5 {game} moments that made me cry laughing 💀", f"{game} players will understand 😭"],
                   "description": f"{CH['credit']}\n{CH['hashtags']}", "virality": max(m.get("virality", 0) for m in group),
                   "why": " | ".join(f"#{5 - i} {m.get('hook_tag', '')}" for i, m in enumerate(group)),
                   "source": " ".join(m.get("source", "") for m in group), "source_kind": "heatmap", "type": "ranking",
                   "hook_tag": edl["title"], "people": [], "moment_ids": [m["_id"] for m in group if "_id" in m],
                   "duration": round(sum((p["end"] - p["start"]) / p.get("speed", 1) for p in edl["pieces"]), 1)})
    return out


def write_review(d: Path) -> Path:
    """Simple approval page: every rendered Short with its titles, score and why."""
    import html

    from . import publish
    f = d / "posts.json"
    posts = json.loads(f.read_text()) if f.exists() else []
    cards = []
    for p in posts:
        titles = "".join(f"<li>{html.escape(t)}</li>" for t in p.get("titles", []))
        cards.append(f"""<div class=c><video src="{html.escape(p['file'])}" controls preload=metadata></video>
<div class=m><b>{publish.batch_label(p)}</b> · {html.escape(p.get('format', ''))} · score {p.get('virality', '-')}<br><small>{html.escape(p.get('why') or '')}</small>
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


def process_file(src: Path, meta: dict, hint: str = "", kind: str = "manual", offset: float = 0.0) -> list[dict]:
    """kind: 'fresh' | 'heatmap' | 'manual'. offset = where src starts inside the original stream (sections)."""
    from .moments import find_moments
    from .transcribe import transcribe
    tr = transcribe(src, meta["vod_key"])
    ctx = f"{meta.get('title', '')} ({meta.get('upload_date', '')}){' | ' + hint if hint else ''}"
    kept = []
    for m in find_moments(tr, ctx, CH):
        m["source"] = f"{meta.get('url', '')} {meta.get('section') or ''}".strip()
        m["source_kind"], m["video_id"] = kind, meta.get("id")
        m["abs_start"] = round(offset + m["start"], 1)
        if m["video_id"] and library.exists_near(m["video_id"], m["abs_start"]):
            print(f"  (already in library: {m.get('hook_tag')})")
            continue
        kept.append(m)
    library.add(meta["vod_key"], src, kept)
    return kept


def seen_path(mode: str = "heatmap") -> Path:
    # separate per batch: a stream scanned FRESH today must still get its 'Most replayed' batch weeks later
    return ROOT / "data" / CH["key"] / ("seen.json" if mode == "heatmap" else f"seen_{mode}.json")


def seen(mode: str = "heatmap") -> set:
    f = seen_path(mode)
    return set(json.loads(f.read_text())) if f.exists() else set()


def mark_seen(ids: set, mode: str = "heatmap") -> None:
    f = seen_path(mode)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(sorted(seen(mode) | ids)))


SAME_SCENE_S = 600  # moments this close in the same stream are the same scene (e.g. one KFC shift)


def diversify(pool: list[dict], used: list[tuple[str, float]], per_stream: int = 2) -> list[dict]:
    """Drop moments from a scene already posted (or already picked this run), cap picks per stream,
    and skip moments made before the current hook rules (no source_kind)."""
    out: list[dict] = []
    taken: list[tuple[str, float]] = []
    for m in pool:
        if not m.get("source_kind"):
            continue
        sid, t = library.stream_pos(m.get("_vod", ""), m["start"])
        if any(p[0] == sid and abs(p[1] - t) < SAME_SCENE_S for p in used + taken):
            continue
        if sum(1 for p in taken if p[0] == sid) >= per_stream:
            continue
        out.append(m)
        taken.append((sid, t))
    return out


def fresh_windows(ms: list[dict], duration: float, n: int) -> list[tuple[float, float]]:
    """Top-n coarse moments -> padded sections (merged when they overlap), in time order."""
    from .scout import PAD_AFTER, PAD_BEFORE
    best = sorted(ms, key=lambda m: -m["virality"])[:n]
    wins = sorted((max(0.0, m["start"] - PAD_BEFORE), min(duration or 1e9, m["end"] + PAD_AFTER)) for m in best)
    out: list[list[float]] = []
    for a0, a1 in wins:
        if out and a0 <= out[-1][1]:
            out[-1][1] = max(out[-1][1], a1)
        else:
            out.append([a0, a1])
    return [(round(a, 1), round(b, 1)) for a, b in out]


def scan_fresh(st: dict, a) -> bool:
    """FRESH batch: Claude estimates the viral moments of a brand-new stream (no 'Most replayed' yet).
    Audio-only download + fast transcript to find candidates, then only those sections go through the
    normal download -> transcribe -> moments path. Returns False if the stream is too old/unsuitable."""
    from . import scout
    from .ingest import download, download_audio, info
    from .moments import find_moments
    from .transcribe import transcribe
    meta = info(st["url"])
    age = (dt.date.today() - dt.datetime.strptime(meta["upload_date"], "%Y%m%d").date()).days if meta.get("upload_date") else 99
    if age > a.fresh_days:
        return False
    print(f"  fresh scan ({age}d old, {int((meta.get('duration') or 0) / 60)} min): audio + {os.environ.get('CLIPPER_SCAN_WHISPER', 'base.en')} transcript")
    audio = download_audio(st["url"], meta)
    tr = transcribe(audio, f"{meta['id']}_scan", os.environ.get("CLIPPER_SCAN_WHISPER", "base.en"), words=False)
    tr.setdefault("words", [])
    coarse = find_moments(tr, f"{meta['title']} ({meta.get('upload_date', '')}) | coarse scan of the whole stream", CH)
    for f in (audio, audio.with_suffix(".16k.wav")):
        f.unlink(missing_ok=True)  # the full-stream audio is only needed for the scan
    for s0, s1 in fresh_windows(coarse, meta.get("duration") or 0, a.fresh_windows):
        sec = f"{scout.fmt(s0)}-{scout.fmt(s1)}"
        print(f"  window {sec}")
        f, m = download(st["url"], sec, meta)
        process_file(f, m, kind="fresh", offset=s0,
                     hint="Claude-estimated viral window from a FRESH stream (no audience data yet) - the best moment should be inside it")
    return True


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
    """Daily one-liner. Two batches per channel:
    - fresh:   newest streams (< --fresh-days old), moments estimated by Claude from the transcript -> post NOW
    - heatmap: older streams with YouTube 'Most replayed' data (proven peaks) -> banked for later posts
    Rendering takes fresh moments first and fills up with heatmap ones (--mode heatmap = heatmap only)."""
    from . import scout
    from .ingest import download
    ensure_assets()
    learn_from_results()
    src_cfg = CH.get("sources", {})
    modes = ["fresh", "heatmap"] if a.mode == "both" else [a.mode]
    if src_cfg.get("youtube_streams"):
        streams = scout.latest_streams(src_cfg["youtube_streams"], a.lookback)
        if "fresh" in modes:
            done, used, new_ids = seen("fresh"), 0, set()
            for st in streams:
                if used >= a.streams:
                    break
                if st["id"] in done:
                    continue
                print(f"stream (fresh): {st['title'][:70]}")
                if scan_fresh(st, a):
                    used += 1
                    new_ids.add(st["id"])
                else:
                    break  # newest first: once one is too old, the rest are too
            mark_seen(new_ids, "fresh")
        if "heatmap" in modes:
            # YouTube only shows "Most replayed" some weeks after a stream airs: look further back and clip the
            # newest unseen streams that HAVE it; too-new streams stay unseen and are picked up on a later day.
            done, used, new_ids = seen("heatmap"), 0, set()
            for st in streams:
                if used >= a.streams:
                    break
                if st["id"] in done:
                    continue
                print(f"stream (most replayed): {st['title'][:70]}")
                meta, peaks = scout.stream_peaks(st["url"], a.peaks)
                if not peaks:
                    print("  no 'Most replayed' data yet (too new?) -> skipping for now")
                    continue
                used += 1
                for s0, s1, v in peaks:
                    sec = f"{scout.fmt(s0)}-{scout.fmt(s1)}"
                    print(f"  peak {sec} (replay score {v})")
                    try:
                        f, m = download(st["url"], sec, meta)
                        process_file(f, m, kind="heatmap", offset=s0,
                                     hint=f"this window is a 'Most replayed' peak (score {v}) - the best moment is inside it")
                    except Exception as e:  # one failed section download must not kill the whole run
                        print(f"\n  skipped peak ({type(e).__name__}: {str(e)[:80]})")
                new_ids.add(st["id"])
            mark_seen(new_ids, "heatmap")
    new_ids = set()
    done = seen("heatmap")
    clips = [c for login in src_cfg.get("twitch_clips", []) for c in scout.twitch_top_clips(login, a.clips, a.range)]
    clips += [c for game in src_cfg.get("twitch_game_clips", []) for c in scout.twitch_game_clips(game, a.clips, a.range)]
    clips = [c for c in clips if c["views"] >= CH.get("min_clip_views", 0)]  # unproven clips cost the same to scan
    if True:
        for clip in clips:
            if clip["id"] in done:
                continue
            print(f"clip: {clip['title'][:60]} ({clip['views']} views)")
            try:
                f, m = download(clip["url"])
                process_file(f, m, kind="heatmap",
                             hint=f"fan-made Twitch clip with {clip['views']} views - a proven moment; tighten it to the payoff")
            except Exception as e:  # one bad clip (e.g. whisper alignment crash on near-silent audio) must not kill the run
                print(f"\n  skipped clip ({type(e).__name__}: {str(e)[:80]})")
            mark_seen({clip["id"]}, "heatmap")  # per clip, so a crash later never re-pays for clips already done
    # fresh first (recency is the lever), heatmap fills the rest; leftover heatmap moments wait for later posts
    pool = [] if a.mode == "heatmap" else library.top(None, a.count * 5, a.min_virality, kind="fresh")
    if a.mode != "fresh":
        pool += [m for m in library.top(None, a.count * 5, a.min_virality) if m.get("source_kind", "heatmap") != "fresh"]
    pool = diversify(pool, library.used_positions())
    d = day_dir()
    rendered = []
    if CH.get("format") == "ranking":
        # countdown comps: each clip only needs one strong payoff, so the bar is one lower and no minimum length
        rpool = diversify(library.top(None, a.count * RANK_N * 4, a.min_virality - 1), library.used_positions())
        best = vision_filter(rpool, a.count * RANK_N)
        print(f"rendering {len(best) // RANK_N} ranking comps from {len(best)} clips...")
        for i in range(len(best) // RANK_N):
            group = sorted(best[i * RANK_N:(i + 1) * RANK_N], key=lambda m: (m.get("virality", 0), m.get("visual_score") or 0))
            out = render_ranking(group, a.handle, d)
            print("  ->", out)
            rendered.append((group[-1], out))
            library.mark_used([m["_id"] for m in group])
        best = [m for m, _ in rendered]
    else:
        pool = [m for m in pool if E.kept_len(m) >= E.MIN_LEN]  # too short once silences are cut
        best = vision_filter(pool, a.count)
        print(f"rendering {len(best)} Shorts...")
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
    try:  # daily housekeeping so the Mac disk doesn't fill again (9 Nov)
        cleanup(apply=True)
    except Exception as e:
        print(f"  cleanup skipped ({type(e).__name__}: {str(e)[:80]})")
    if a.serve and best:
        from .review_server import serve
        serve(CH, d, 8765, open_browser=True, timeout_h=12)


def cleanup(apply: bool, render_days: int = 7, previews: bool = False, vod_hours: float = 24) -> None:
    """9 Nov (chairman-approved): the Mac disk filled with downloaded stream clips. Deletes the pipeline's OWN cache:
    - data/vods files no unused moment on a LIVE channel (one with a Blotato account) still needs, >24 h old;
    - rendered Shorts in out/<channel>/ older than render_days (posted ones live on YouTube);
    - with previews=True, out/voice_previews/* except the latest folder.
    Clips still needed live in Drive (My Drive/CLIPZ_SOURCE_CLIPS) and are never touched here."""
    import sqlite3
    import time
    cfg = json.loads((ROOT / "channels.json").read_text())
    live = {k for k, v in cfg.items() if isinstance(v, dict) and v.get("blotato")}
    need = set()
    for k in live:
        db = ROOT / "data" / k / "moments.db"
        if db.exists():
            need |= {str(Path(s).resolve()) for (s,) in sqlite3.connect(db).execute("select src from moments where used=0")}
    now = time.time()
    # 9 Nov bug: "used" != finished. Cancelled/unposted renders still need their sources to be re-rendered,
    # so keep the source of every moment behind any Short rendered within render_days.
    for k in cfg:
        db = ROOT / "data" / k / "moments.db"
        if not db.exists():
            continue
        ids = set()
        for pj in (ROOT / "out" / k).glob("*/posts.json"):
            if now - pj.stat().st_mtime > max(render_days, 7) * 86400:
                continue
            try:
                for post in json.loads(pj.read_text()):
                    ids |= set(post.get("moment_ids", []))
            except Exception:
                continue
        if ids:
            q = ",".join("?" * len(ids))
            need |= {str(Path(s).resolve()) for (s,) in sqlite3.connect(db).execute(f"select src from moments where id in ({q})", list(ids))}
    doomed = [p for p in (ROOT / "data" / "vods").glob("*")
              if p.is_file() and str(p.resolve()) not in need and now - p.stat().st_mtime > vod_hours * 3600]
    for k in cfg:
        od = ROOT / "out" / k
        if od.is_dir():
            doomed += [p for p in od.rglob("*") if p.is_file() and p.suffix in {".mp4", ".wav", ".mp3", ".jpg"}
                       and now - p.stat().st_mtime > render_days * 86400]
    if previews and (ROOT / "out" / "voice_previews").is_dir():
        vp = sorted((ROOT / "out" / "voice_previews").iterdir(), key=lambda p: p.stat().st_mtime)
        latest = max((p for p in vp if p.is_dir()), key=lambda p: p.stat().st_mtime, default=None)
        for p in vp:
            if p == latest:
                continue
            doomed += [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()]
    size = sum(p.stat().st_size for p in doomed)
    print(f"cleanup: {len(doomed)} files, {size / 1024**3:.2f} GB" + ("" if apply else " (dry run, add --yes to delete)"))
    if apply:
        for p in doomed:
            p.unlink()
        with open(ROOT / "data" / "cleanup_log.jsonl", "a") as f:
            f.write(json.dumps({"at": dt.datetime.now().isoformat(timespec="seconds"), "files": len(doomed), "bytes": size}) + "\n")


def cmd_cleanup(a) -> None:
    cleanup(a.yes, a.render_days, a.previews, a.vod_hours)


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


def cmd_rerender(a) -> None:
    """Rebuild a rendered Short from its stored moments with the CURRENT pipeline (fixes reach old Shorts too);
    the old file is marked skipped so it can never be posted."""
    from . import publish
    f = next((OUT / CH["key"]).glob(f"*/{a.file}"), None)
    if not f:
        print(f"{a.file} not found under out/{CH['key']}/")
        return
    d = f.parent
    post = next(p for p in json.loads((d / "posts.json").read_text()) if p["file"] == a.file)
    rows = {r["_id"]: r for r in library._rows("select id, used, vod_key, data from moments")}
    ids = post.get("moment_ids") or []
    if not ids:  # Shorts made before ids were stored: match by hook text
        tags = [t.split(" ", 1)[1] for t in post.get("why", "").split(" | ")] if post.get("format") == "ranking_comp" \
            else [post.get("hook_tag")]
        by_tag = {r.get("hook_tag"): i for i, r in rows.items()}
        ids = [by_tag[t] for t in tags if t in by_tag]
    ms = [rows[i] for i in ids if i in rows]
    if post.get("format") == "ranking_comp":
        out = render_ranking(ms, a.handle, d)
    else:
        out = render_single(ms[0], a.handle, d)
    publish.skip(CH, d, post)
    write_review(d)
    print("->", out, "(old one skipped)")


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
    au.add_argument("--mode", default="both", choices=["both", "fresh", "heatmap"],
                    help="fresh = Claude-estimated moments from new streams; heatmap = 'Most replayed' peaks (later posts)")
    au.add_argument("--fresh-days", type=int, default=3, help="fresh: only streams newer than this")
    au.add_argument("--fresh-windows", type=int, default=6, help="fresh: candidate sections to download per stream")
    au.add_argument("--streams", type=int, default=2, help="YouTube: streams per batch (fresh / heatmap)")
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
    rr = sub.add_parser("rerender", help="rebuild one rendered Short with the current pipeline")
    rr.add_argument("file", help="the .mp4 file name in out/<channel>/<date>/")
    sub.add_parser("skills")
    sub.add_parser("demo")
    cl = sub.add_parser("cleanup", help="delete the pipeline's own used stream clips + old renders (dry run unless --yes)")
    cl.add_argument("--yes", action="store_true")
    cl.add_argument("--render-days", type=int, default=7)
    cl.add_argument("--previews", action="store_true")
    cl.add_argument("--vod-hours", type=float, default=24, help="only delete clips downloaded more than N hours ago")
    load_env()
    a = ap.parse_args()
    CH.update(channels.get(a.channel))
    a.handle = a.handle or CH["handle"]
    library.CHANNEL = a.channel
    if a.cmd == "demo":
        library.CHANNEL = CH["key"] = "demo"
    {"run": cmd_run, "auto": cmd_auto, "review": cmd_review, "rerender": cmd_rerender, "accounts": cmd_accounts, "stats": cmd_stats, "comp": cmd_comp, "skills": cmd_skills, "demo": cmd_demo, "cleanup": cmd_cleanup}[a.cmd](a)


if __name__ == "__main__":
    main()
