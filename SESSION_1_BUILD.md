# Session 1 build brief: Speed clipping pipeline MVP

> Paste into Claude Code on the Mac: **"Read SESSION_1_BUILD.md and execute it end to end. Don't stop to ask unless blocked."**
> Background: `CLIPPING_PIPELINE_IDEA.md` (sections 7–8), style: `styles/speed_v2.json`.

## Goal for this ONE session
By the end of the session: **one command turns a Speed stream VOD URL into finished, styled 9:16 Shorts plus titles**, and the first Shorts are uploaded.

```
python -m clipper run "<speed VOD url>" --formats single_moment,subversion_comp --count 3
→ out/<date>/*.mp4 + out/<date>/posts.json (title, description, hashtags per clip)
```

## Scope: in (session 1)
1. **CLI tool on the Mac.** It runs locally: no server, no deploy. `app.py` (FastAPI) stays as is and is out of scope.
2. **Ingest:** `yt-dlp` downloads the VOD (or a time range of it) in ≤1080p.
3. **Transcribe:** word timestamps with `faster-whisper` locally (model `small.en`; use `medium.en` if quality is poor). Cache the result to disk.
4. **Moment finder:** send the transcript chunks to the Claude API and get back JSON moments `{start, end, type, people, emotion, skill, success, payoff_t, hook_tag, action_tags[], emoji, titles[3]}`. Use the title formulas from section 7.2/8 of the idea doc and the `formats` in `speed_v2.json`.
5. **Moment library:** SQLite `moments.db` stores every moment with its tags and source, so later formats can query across VODs.
6. **Renderer** (ffmpeg, driven by `speed_v2.json`). Build these in this order:
   - `single_moment`: crop 9:16 (centre crop is fine for v1), cut pauses >0.4s, ASS captions (ALL CAPS, white with green/yellow active word, black stroke, y=50%), `*ACTION TAGS*`, hook tag 0–2s, 1.15x punch-in + white flash + bass thud at `payoff_t`, emoji pop at the payoff, phonk bed at −16dB with the drop at the first impact, watermark, hard cut.
   - `subversion_comp`: query the library for 6 moments sharing one `skill` (1 fail + 5 successes), header "SPEED {CLAIM}" at y=8% for clips 1–2, "ARE YOU SURE?" at clip 3, 0.35x slow-mo + punch-in + 💀 pop on each impact, hard cuts, no captions, 20–22s total.
7. **Output:** mp4s + `posts.json`. Then **upload**: either manually to YouTube Studio for session 1, or through Blotato if its MCP/API is connected in the terminal.

## Scope: out (later sessions; don't start these)
Face-tracked crop, the `escalation_levels` / `timeline_progression` / `wholesome_fan` renderers, an auto VOD watcher, auto-scheduling, analytics loop.

## Acceptance test (the session is done only when this passes)
- [ ] `python -m clipper run <real Speed VOD url> --count 3` produces **3 single_moment Shorts**, each 15–58s, 1080x1920, with audio and readable captions
- [ ] After 2–3 VODs are in the library, `python -m clipper comp --skill <x>` produces **1 subversion_comp** of 20–22s
- [ ] Each Short has 3 title options in `posts.json`
- [ ] Watch every output once yourself before uploading, then upload the 3 best

## Prerequisites (do these before starting; ~15 min)
- [ ] `brew install ffmpeg yt-dlp python@3.12`
- [ ] `ANTHROPIC_API_KEY` exported in the shell (console.anthropic.com)
- [ ] Font: **Montserrat Black**, from Google Fonts, installed on the Mac
- [ ] `assets/music/`: 3–5 **royalty-free/licensed** phonk tracks (no copyrighted phonk, because Content ID will claim it)
- [ ] `assets/sfx/`: bass_thud, whoosh, ding, vine_boom (royalty-free packs)
- [ ] `assets/emoji/`: PNGs for 💀 🤯 😭 😂 🥶 ❤️‍🩹 (e.g. Twemoji, CC-BY), since ffmpeg can't render colour emoji fonts reliably
- [ ] A new YouTube channel created, with handle chosen (used for the watermark)
- [ ] 1–3 recent iShowSpeed stream VOD URLs ready

## Suggested repo layout
```
clipper/
  __main__.py      # CLI: run, comp, render
  ingest.py        # yt-dlp
  transcribe.py    # faster-whisper → words.json
  moments.py       # Claude API → moments JSON, SQLite library
  edl.py           # moment(s) + style preset → edit decision list
  render.py        # EDL → ffmpeg filtergraph (ASS captions, zoompan, overlays, amix)
  ass.py           # caption/tag/header .ass generator
styles/speed_v2.json
assets/{music,sfx,emoji,fonts}/
out/
```

## Hard rules
- Style values come only from `styles/speed_v2.json`; don't hard-code them
- Test each stage on a 5-minute slice of the VOD before running the full VOD
- No copyrighted music. Keep source audio.
