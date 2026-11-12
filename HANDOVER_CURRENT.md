# CLIPZ NETWORK — HANDOVER_CURRENT (8 clip channels, repo ~/ffmpeg-render-service)

Load this first. Also: memory `project_turboclipz_speed_clipper.md`, `SESSION_1_BUILD.md`, `channels.json`.
Branch `claude/tender-goodall-hg7yeu` (all commits pushed; head cbbc91c at time of writing).

---

## RESUME POINT — CLIPZ NETWORK (2026-11-12 21:35 UTC) — supersedes 21:25

### Owner 12 Nov: "you choose — let the original data and the learning data from views choose"
- **YouTube views (live 12 Nov 21:20Z):** countdowns 1,018–1,454 each (gta/fortnite/minecraft/osrs/kreek/caylus, 10–11 Nov); singles 1–19 (Fortnite 8, Kai 3, Speed 12/19/1); Caylus single 242 (hours old). **Speed had never posted a countdown.**
- Decision from that data: Speed gets ONE countdown test before the ~15 Nov keep/drop call. Commit: Speed `min_rank` 3 and `allow_single` false (no more Speed singles). `auto` cleanup is now REPORT ONLY (dry run); delete only with `cleanup --yes` after the owner says yes.
- Rebuilt top 3 `out/speed/2026-11-12/211519_ranking-speed.mp4` (36 s; clips 12.0/11.1/13.0 s; moments 56, 64, 60). QA: all three stories end on a full sentence, all IRL, no call-in. Weak points: Speed is barely in frame in #3 (the fan raps) and #1 (the Apple presenter fills it); a stream chat column is beside his cam in #2.
- **BOOKED 13 Nov 12:55Z** "Only Speed would drink Ochocinco's coffee 💀". YT b251c032 · TT 2b33699f · IG 5b25d60e · FB 8423e194 — all verified `scheduled`.

### EXACT NEXT ACTION
1. ~14–15 Nov: read the views on this Speed countdown vs the game countdowns (~1k). Clearly below → recommend dropping TurboClipz (owner decides). Near → scan 2–3 older IRL streams for top-5 supply.
2. Normal morning routine for all channels.
3. Learning gap: posted.json does not store the format (countdown/single), so `performance.learnings` cannot compare formats. Add it when next touching publish.

---

## RESUME POINT — CLIPZ NETWORK (2026-11-12 21:25 UTC)

### Done 12 Nov (evening session)
- 12 Nov posts all PUBLISHED (Blotato get_post_status): GTA youtu.be/ig1X_z54LUA · OSRS olrmrB6Yaik · Kreek klTCLwXB4pg · Caylus 7_7ZWbTVqH8. Speed, Minecraft, Kai, Fortnite: no post.
- Commit 26b14a6 (pushed). Speed countdown pipeline fixed (Rule 55, fix the generator):
  - `edl.story_window`: each clip ENDS on the first clean sentence end 1.5–5 s after the payoff and STARTS on a sentence start, 10–12 s (channels.json `rank_style.clip_s`). No clean end/start = the moment is not used (gate, no fixed-cut fallback). Speed only; other channels still use the old 5 s + 2.5 s cut.
  - Vision now judges exactly that window, and it is pinned as `clip_win` so the render = what was judged. (The old check sampled the whole 40 s moment, which is how menu/chat screens passed.)
  - Call-ins: `skip_streams_re` in channels.json (JOIN THIS STREAM / WIN AN IPHONE / call-in / FaceTime), applied at scan time and in the pool. Moments now carry `stream_title` (93 Speed moments backfilled). Excluded: GfCnZ8cAYvQ "JOIN THIS STREAM, WIN AN IPHONE 18!" and glOhY5hiOwI "JOIN THIS STREM MESSI RETIRED" (frames confirm random video-call: Next/Stop buttons).
  - Speed `vision_extra` (no phone/chat/call/menu screens) and `min_visual` 7.
- Rebuild `auto --mode heatmap --streams 0`: 10 checked, 3 KEEP (60 iPhone Duo 8, 64 Ochocinco coffee 7, 56 Ohio freestyle 7). Speed needs 5 (min_rank 5), so **no comp and nothing booked**. 7 drops are marked used. Only 2 untested story-complete candidates are left in the bank (75 KSI, 39 John Bobby v5), so the bank cannot make a top 5.
- ⚠️ The run's built-in cleanup (approved 9 Nov) deleted 155 local cache files (1.32 GB): stream clips no unused moment needs, plus renders >7 days. Drive was untouched. The owner now wants a yes before ANY deletion, so make `auto`'s cleanup a dry run unless he says otherwise (decision pending).

### Decisions waiting on the owner
1. Speed: (a) scan 2–3 more OLDER IRL streams (~$0.3–0.5 Claude each, ~20 min each), (b) allow a top 3 (min_rank 3) from the 3 keepers, or (c) drop TurboClipz (deadline ~15 Nov).
2. Should `auto` keep its automatic cleanup, or report only?
3. Drive eviction (~6.5 GB) still pending.

### EXACT NEXT ACTION
Owner's Speed answer. If (a): `RENDER_OBJECTIVE=voice-turboclipz-<tag>--h1-speed timeout 6000 python -m clipper --channel speed auto --mode heatmap --streams 3 --count 1` → QA contact sheet + each clip's transcript vs label → book in the 13 Nov day_plan slot only if it passes. Then the normal morning routine for all channels.

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
