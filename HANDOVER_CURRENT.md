# CLIPZ NETWORK — HANDOVER_CURRENT (8 clip channels, repo ~/ffmpeg-render-service)

Load this first. Also: memory `project_turboclipz_speed_clipper.md`, `SESSION_1_BUILD.md`, `channels.json`.
Branch `claude/tender-goodall-hg7yeu` (all commits pushed; head cbbc91c at time of writing).

---

## RESUME POINT — CLIPZ NETWORK (2026-11-11 22:30 UTC)

### Done this session (10–11 Nov)
- 10 Nov: all 8 channels published.
- 11 Nov: 7 of 8 channels posted (Kai skipped, no keeper).
- Commit f78e275: prompt caching on moments calls (`clipper/moments.py` system block `cache_control`), plus cache_w/cache_r logging in `clipper/__init__.py log_usage`. Saves about $1 a morning.
- Commit f17c4b1: caption/header prompts (`voice.label_qa`, `voice.context_line`) must never turn a question, doubt or irony into a claim.
- A/B model test via `channels.json moments_model`: Opus = gta, minecraft, kreek, osrs, speed; Sonnet = kai, fortnite, caylus.
- Commit cbbc91c: Speed (TurboClipz) is now countdown-only. `format: ranking`, `vo_mode: countdown`, `min_rank: 5`, yellow #FFE600 rank_style "SPEED'S CRAZIEST MOMENTS", voice Liam. Speed skips the day if there are not 5 keepers.
- Pulled the 12 Nov Speed post `084920_make-speed-laugh-win-an-iphone.mp4`: Blotato schedules 6782393/6782395/6782398/6782400 deleted (owner had called the gorilla Short "shit"). Marked cancelled in `data/speed/posted.json`. Nothing was deleted from YouTube.
- Speed heatmap scan of 5 older streams (Ohio State IRL, Revealing new iPhone, World Talent Show, Messi retired, Minecraft chat controls): timed out at 6000 s before rendering. The moments were banked, and those 5 ids were added to `data/speed/seen.json` (9 ids now).
- Rendered from the bank: `out/speed/2026-11-11/220224_ranking-speed.mp4` (37.5 s top 5). **REJECTED, not booked.** About 7 s per clip, so stories don't finish (cut-off caption "Unfortunately Jamal there's…"). #5 is from the iPhone call-in stream GfCnZ8cAYvQ, and #3/#4 are menu or chat screens. Moments 35/37/55/60 were set back to unused; 32 (call-in) was left used. Contact sheet: `handover/2026-11-11/qa_contact_sheets/speed_top5.jpg`.

### Status of every channel / 12 Nov slots (UTC; all verified "scheduled" on Blotato 11 Nov 22:20)
- GTA SnackClipz 12:37 `064100_ranking-gta.mp4` (schedule 6782384) — booked.
- OSRS Rare Drop Clipz 17:32 `064646_ranking-osrs.mp4` (6782386) — booked.
- KreekCraft RageClipz 19:46 `095919_ranking-kreekcraft.mp4` (6784216) — booked.
- Caylus CozyClipz 20:41 `080031_they-hid-the-killer-from-cops.mp4` (6782388) — booked.
- Speed TurboClipz 14:34 slot — EMPTY (countdown rejected; see next action).
- Minecraft GoofyClipz, Kai RowdyClipz, Fortnite StudioClipz — EMPTY for 12 Nov (no keepers yet).

### Views (last check 11 Nov)
- First Shorts got ~1.1–1.3k views on Fortnite, Minecraft, GTA, Caylus and OSRS.
- Speed got 11–12, Kreek 5, Kai 1 (YouTube). Speed IG got 157–163 views, 21–23 s average watch.
- The owner found no Studio notices on Turboclipz.

### STOPPED and why
- Speed countdown: rejected for quality (above). It is not booked.
- Drive `CLIPZ_SOURCE_CLIPS` eviction (~6.5 GB): waiting on the owner's yes. Manifest at `handover/2026-11-11/drive_evict_manifest_PENDING_2026-11-09.tsv`.

### Queued but NOT run
- `out/speed/2026-11-11/220224_ranking-speed.mp4` is rendered and rejected. Do not book it.

### Money
- Claude API today: $3.84 (kreek 2.03, speed 0.93, osrs 0.22, gta 0.22, caylus 0.17, minecraft 0.11, kai 0.10, fortnite 0.06).
- Claude API project total: $33.18 (all channels incl. trials) of the £200 allowance ("budget not target").
- ElevenLabs: 6,177 chars total logged (`data/elevenlabs_usage.jsonl`; there are no timestamps, so there is no per-day figure).
- Blotato: 6,695 credits left (subscription renewed 8 Nov; renewal decision early Dec).
- vidIQ: no paid use.

### Decisions waiting on the owner
1. Speed deadline ~15 Nov: drop TurboClipz if views don't improve (owner said Speed "will be the first to go").
2. Drive eviction of ~6.5 GB source clips: yes or no.
3. Silence in the Storm Instagram: reconnect in Blotato (owner's task, separate project).

### EXACT NEXT ACTION (12 Nov morning, before 14:34 UTC)
Fix the Speed countdown in the pipeline, not the video (Rule 55):
(a) Per-clip length in ranking comps: about 10–12 s, ending on the payoff, so each story finishes. Find the cap in `render_ranking` / `clipper/edl.py`.
(b) Exclude call-in / phone-giveaway streams from Speed's pool (GfCnZ8cAYvQ "make Speed laugh win an iPhone", and similar).
(c) Prefer IRL or large-face clips over menu/chat screens in the vision filter for Speed.
Then: `source .venv/bin/activate; RENDER_OBJECTIVE=voice-turboclipz-<tag>--h1-speed timeout 3000 python -m clipper --channel speed auto --mode heatmap --streams 0 --count 1`. `--streams 0` = render from the ~76 banked moments, no rescan.
QA the contact sheet. If good, book it in Speed's 14:34 slot with the book_today helper (`handover/2026-11-11/book_today_helper_2026-11-11.py` + picks json), verify with get_post_status, and append `data/coverage.jsonl`. If not good, Speed skips.
Then run the normal morning routine for all channels ("morning lets go to work please on todays posts" = approval to book).

### Gotchas hit
- Heatmap runs on Speed take ~20 min per stream (8 peaks): `--streams 5` needs a 6000 s timeout or more. Better: scan 2–3 streams per run.
- If a run times out, the moments are already banked in `data/<ch>/moments.db` but `seen.json` is NOT updated. Add the ids by hand or rescans cost money again.
- `rerender` takes a filename only, not a path.
- KreekCraft runs take more than 50 min (timeout 5400).
- The ranking pool includes fresh moments too, so old call-in moments can enter Speed comps.
- ElevenLabs commands need the prefix `RENDER_OBJECTIVE=voice-turboclipz-<x>--h1-<y>` (render guardrail; never route around it).

### Retirement debt
- `book_today.py` helper (copy in handover/) should become a CLI command (`python -m clipper book`). Then retire the helper.
- Fix vision to judge the rendered stacked/split layout.
- `data/cachetest/` test rows ($0.008) can go when the owner approves.

### Files saved this session
`handover/2026-11-11/` (14 files):
- book_today helper + picks json
- Drive evict/del manifests + keep_vods/moved_map (9 Nov)
- 8 QA contact sheets (qa_contact_sheets/)
