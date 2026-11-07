# Session 1: go live (most of the build is ALREADY DONE)

> Paste into Claude Code on the Mac: **"Read SESSION_1_BUILD.md and get the clipper running on a real Speed VOD. Fix whatever breaks."**

## What already exists (built and tested in the phone session, 7 Nov 2026)
`clipper/` is a Python CLI. One command does all of this: VOD URL → download → transcribe → Claude finds moments → moment library → styled Shorts + titles.

| Module | Does | Tested? |
|---|---|---|
| `render.py` | EDL → 1080x1920 Short: crop, speed ramps/slow-mo, punch-in, shake, flashes, ASS captions with word highlight, `*TAGS*`, headers, emoji pops, watermark, phonk bed (muffled until the drop, ducked under speech), SFX, loudness −14 LUFS | ✅ on synthetic footage |
| `edl.py` | Format presets `single_moment` (cuts silences, payoff punch-in, hook tag) and `subversion_comp` (Drayz "Speed cant X" format, 20–22s) | ✅ |
| `library.py` | SQLite moment library (skill / outcome / virality / used) | ✅ |
| `__main__.py` | CLI: `run`, `comp`, `skills`, `demo` | ✅ (`demo`) |
| `ingest.py` | yt-dlp download, optional `--section` | ⚠️ untested (YouTube blocked in the cloud session) |
| `transcribe.py` | faster-whisper word timestamps, cached | ⚠️ untested (model download blocked) |
| `moments.py` | Claude API (`claude-opus-5-5`, structured JSON output, server-side refusal fallback) → ranked moments + 3 titles each | ⚠️ untested (no API key in the cloud session) |
| `assets/` | Montserrat Black (OFL), Twemoji PNGs (CC-BY), SFX + placeholder phonk loops (generated from scratch, royalty-free) | ✅ |

## Mac setup (~10 min)
```bash
brew install ffmpeg yt-dlp python@3.12
cd ffmpeg-render-service && git checkout claude/tender-goodall-hg7yeu && git pull
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-clipper.txt
export ANTHROPIC_API_KEY=sk-ant-...          # console.anthropic.com
# put your real channel handles into channels.json (replace the @CHANGE_ME_... values)
python -m clipper demo                        # offline sanity check → out/<date>/
```

## Channels (one streamer each, so viewers who subscribe for that person keep getting that person)
| key | Streamer | Streams on | Launch order |
|---|---|---|---|
| `speed` | iShowSpeed | YouTube | 1st |
| `kai` | Kai Cenat + crew | Twitch | 2nd |
| `core` | Lacy, StableRonaldo + Core boys | Twitch / Kick | 3rd (once 1–2 are running) |
Add more by copying an entry in `channels.json`. Each channel has its own moment library (`data/<key>/`) and output folder (`out/<key>/`).

## Go live
```bash
# Grab a 45-min chunk of a recent Speed stream (much faster than a full 4h VOD)
# ONE STREAMER PER CHANNEL. --channel picks which (speed / kai / core, see channels.json)
python -m clipper --channel speed run "https://www.youtube.com/watch?v=<SPEED_STREAM_ID>" --section 00:30:00-01:15:00 --count 3
python -m clipper --channel kai   run "https://www.twitch.tv/videos/<KAI_VOD_ID>"         --section 01:00:00-01:45:00 --count 3
# → out/<channel>/<date>/*.mp4 + posts.json (3 title options each). Watch them, upload the best to THAT channel.

# After 2–3 streams per channel are in its library:
python -m clipper --channel speed skills      # what the library has per skill
python -m clipper --channel speed comp        # "Speed cant X" comp (Kai: "Kai cant X")
```

## Session 1 checklist for Claude Code
1. [ ] Run setup, then `python -m clipper demo`. It must pass.
2. [ ] Run `run` on a real Speed stream section. Fix any ingest/transcribe/moments errors (these 3 modules are untested).
3. [ ] Watch every output and tune:
   - payoff timing (`payoff_t` accuracy). If it's often late or early, add a vision check: send 6 frames around payoff_t to Claude to confirm.
   - crop: centre crop cuts Speed off when he's off-centre. Next upgrade: face-tracked crop (mediapipe/opencv) in `render_piece`.
   - caption size and position, tag wording, music level.
4. [ ] Upload the 3 best manually in YouTube Studio (title from posts.json, description already includes the credit).
5. [ ] Commit fixes to `claude/tender-goodall-hg7yeu`.

## Next sessions (not session 1)
Face-tracked crop · `escalation_levels` / `timeline_progression` / `wholesome_fan` presets (style in `styles/speed_v2.json`) · auto-watch Speed's channel for new streams (cron/launchd + `yt-dlp --dateafter`) · auto-upload (YouTube Data API or Blotato) · analytics feedback into the selection prompt.

## Knobs
`CLIPPER_MODEL` (default `claude-opus-5-5`) · `CLIPPER_WHISPER` (default `small.en`; `medium.en` = better, slower) · `CLIPPER_FALLBACKS=0` to turn off the server-side refusal fallback · drop licensed tracks into `assets/music/` (non-placeholder files are preferred automatically).
