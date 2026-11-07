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
| `track.py` | Face-tracked 9:16 crop (YuNet): follows the streamer like a camera operator, centre-crop fallback | ✅ on a moving-face test |
| `scout.py` | WHERE to clip: YouTube "Most replayed" heatmap peaks (Speed) + most-viewed Twitch clips (Kai, Core) | ✅ peak logic; ⚠️ live fetch untested |
| `vision.py` | Visual QA gate: Claude checks 8 frames per moment, drops ones that are boring to watch, fixes payoff timing | ⚠️ untested (no API key), fails open |
| wholesome format | `type: wholesome` moments get soft emotional music, gold captions, ❤️‍🩹, no flash/thud (deagzzz style, the biggest category) | ✅ |
| `tools/setup_mac.sh` / `tools/schedule.sh` | One-command setup (.env for the key) · daily launchd autopilot + macOS notification | ⚠️ syntax-checked only (needs a Mac) |
| auto-posting | `review` = approve page on localhost:8765: pick/edit title, tick YouTube/TikTok/Instagram, Approve → uploaded + scheduled via Blotato into the next free slot (`post_times_utc` in channels.json, default 14:00/16:45/19:00 UTC from the winners' upload-time analysis) | ✅ dry-run end to end; ⚠️ live Blotato API untested (docs/API host blocked in cloud session; verify endpoint paths in `clipper/blotato.py` against help.blotato.com/api on first real post) |
| `performance.py` | Learning loop: 48h + 7d after posting, reads views (yt-dlp, via the live URL from Blotato), writes `data/<channel>/learnings.md` (top/flop Shorts, best types/formats/lengths, virality-score calibration), which is automatically added to Claude's moment-picking instructions. `python -m clipper --channel speed stats` | ✅ simulated end to end |
| `tests/test_clipper.py` | 15 fast checks (edit logic, scheduling, scouting, tracking, prompts, learning loop) + optional real render: `python -m unittest discover -s tests` | ✅ all pass |
| review page | `out/<channel>/<date>/review.html`: watch every Short + its 3 titles, post the best | ✅ |
| `assets/` | Montserrat Black (OFL), Twemoji PNGs (CC-BY), SFX + placeholder phonk loops (generated from scratch, royalty-free) | ✅ |

## Mac setup (~5 min, one command)
```bash
git clone https://github.com/aiincomehq-max/ffmpeg-render-service && cd ffmpeg-render-service   # or cd into your existing copy
git checkout claude/tender-goodall-hg7yeu && git pull
bash tools/setup_mac.sh        # installs everything, asks for API key + channel handle, runs the demo
bash tools/schedule.sh speed 10:00          # autopilot DAY run (Mac local time; done before the 14:00 UTC first slot)
# later, for the Twitch channels: day run + 1am NIGHT run (auto-posts the single strongest fresh Short, rest wait for approval)
bash tools/schedule.sh kai 10:00 && bash tools/schedule.sh kai 01:00 night
bash tools/schedule.sh core 10:00 && bash tools/schedule.sh core 01:00 night: runs daily, pops a notification when Shorts are ready
```

## Channels (one streamer each, so viewers who subscribe for that person keep getting that person)
| key | Streamer | Streams on | Launch order |
|---|---|---|---|
| `speed` | iShowSpeed | YouTube | 1st |
| `kai` | Kai Cenat + crew | Twitch | 2nd |
| `core` | Lacy, StableRonaldo + Core boys | Twitch / Kick | 3rd (once 1–2 are running) |
Add more by copying an entry in `channels.json`. Each channel has its own moment library (`data/<key>/`) and output folder (`out/<key>/`).

### Channel names (brand names, never the streamer's name: avoids impersonation takedowns, like the winners Nexxo Recaps / deagzzzshorts / Drayzshorts)
Try them in order. If a handle is taken, double a letter (`@blitzzrecaps`) or add `hq` (`@blitzrecapshq`). Grab the same handle on TikTok and Instagram.
Once created, put the real handle into `channels.json` (replace `@CHANGE_ME_...`); it becomes the watermark.

| Channel | Theme | Names to try (@handle) |
|---|---|---|
| `speed`: create NOW | fast / speed | **Blitz Recaps** (@blitzrecaps) · Dash Recaps (@dashrecaps) · Turbo Clipz (@turboclipz) · Zippo Edits (@zippoedits) · Velo Recaps (@velorecaps) · Brixo Shorts (@brixoshorts) |
| `kai`: create once Speed posts daily | loud / chaos / hype | **Hype Recaps** (@hyperecaps) · Chaos Clipz (@chaosclipz) · Rumble Edits (@rumbleedits) · Loudr Shorts (@loudrshorts) |
| `core`: create third | friend group / squad | **Crew Cuts** (@crewcutsclips) · Squad Recaps (@squadrecaps) · Lobby Clipz (@lobbyclipz) · Gang Edits (@gangedits) |

**Setup for every channel:**
- Profile picture: a simple logo, never the streamer's face.
- Audience: **"No, it's not made for kids"**.
- Description: "Daily {streamer} fan edits 🔥 Not affiliated with or impersonating {streamer}. All credit to the original creator."

## Go live: THE DAILY COMMAND
```bash
python -m clipper --channel speed auto     # newest streams → "Most replayed" peaks → moments → visual QA → 4 Shorts → review.html
python -m clipper --channel kai auto       # top Twitch clips this week → same
python -m clipper --channel speed review     # approve page → Approve = scheduled on YouTube/TikTok/IG via Blotato
# (with tools/schedule.sh the approve page opens by itself after the daily run)
```

Manual mode (a specific stream/section) is still there:
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
1. [ ] Run setup, then `python -m clipper demo` and `python -m unittest discover -s tests`. Both must pass.
2. [ ] Run `--channel speed auto` (then `run` on one stream if auto has issues). Fix any scout/ingest/transcribe/moments/vision errors (untested against live services).
3. [ ] Watch every output and tune:
   - payoff timing (`payoff_t` accuracy). If it's often late or early, add a vision check: send 6 frames around payoff_t to Claude to confirm.
   - crop: face tracking is on (`CLIPPER_TRACK=0` disables). Check it follows Speed; tune `DEADZONE`/`EASE` in `track.py`.
   - caption size and position, tag wording, music level.
4. [ ] Connect the new YouTube (+ TikTok/IG) account in Blotato, run `python -m clipper --channel speed accounts`, put the ids into channels.json → blotato.
5. [ ] First real post: approve ONE Short with "Post now" to YouTube only, and check it appears correctly. If the Blotato call fails, fix the endpoint paths/body in `clipper/blotato.py` using help.blotato.com/api. Until BLOTATO_API_KEY is set everything is a dry run (logged to data/<channel>/dryrun_posts.jsonl).
6. [ ] Commit fixes to `claude/tender-goodall-hg7yeu`.

## Next sessions (not session 1)
`escalation_levels` / `timeline_progression` / `wholesome_fan` presets (style in `styles/speed_v2.json`) · auto-watch Speed's channel for new streams (cron/launchd + `yt-dlp --dateafter`) · auto-upload (YouTube Data API or Blotato) · analytics feedback into the selection prompt.

## Knobs
`CLIPPER_MODEL` (default `claude-opus-5-5`) · `CLIPPER_WHISPER` (default `small.en`; `medium.en` = better, slower) · `CLIPPER_VISION=0` skips the visual QA · `CLIPPER_TRACK=0` = plain centre crop · `CLIPPER_FALLBACKS=0` to turn off the server-side refusal fallback · drop licensed tracks into `assets/music/phonk/` and `assets/music/emotional/` (your files are preferred over the placeholders automatically).
