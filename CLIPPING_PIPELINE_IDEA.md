# Clipping Pipeline: Idea Brief

> Status: **brainstorm / not started**. Written from a phone session. Open this in a Claude Code terminal session on the Mac to plan and build.
>
> Starter prompt for the terminal: *"Read CLIPPING_PIPELINE_IDEA.md and help me plan phase 1."*

## 1. Where the idea came from

Reference reel: https://www.instagram.com/reel/DfadbZ-TdRE/ (46s)

| Time | Beat | What happens |
|---|---|---|
| 0–15s | **Urgency hook** | Talking head with *GTA 6* art overlaid. Text: "You have 12 days to learn this skill". Claim: GTA 6 will be the most clipped game ever, so learn clipping now. |
| 15–41s | **Screen-recorded demo** | YouTube → copy the link to a viral MrBeast video → paste it into the everygen.ai "Wizard" → it picks the viral moments, cuts vertical clips and auto-captions them → download and post. |
| 41–46s | **Comment-keyword CTA** | "Comment 'creator' and I'll send you a FREE guide". A comment-to-DM lead funnel. |

Two takeaways:
1. **Product:** build our own version of "long video in, captioned vertical clips out" on top of this repo, instead of paying for Everygen/Opus Clip-style tools.
2. **Content format:** the hook → demo → comment-keyword structure is a good template for our own posts. We could even use it to market the pipeline.

## 2. What this repo already does

`app.py` is a FastAPI service with `POST /render`:
- downloads N clip URLs
- normalises each to **1.5s, 1080x1920, 30fps** (scale + centre crop)
- concatenates them
- burns in timed `drawtext` overlays
- optionally muxes a voiceover

Gaps that matter for clipping:
- clips are hard-trimmed to the **first 1.5s**, with no `start`/`end` per clip
- source audio is dropped (`-an`)
- no word-level / animated captions (only static overlays)
- centre crop only (no face/speaker tracking)
- the response returns `job_id` but **no way to fetch the output file** (no download endpoint or upload to storage)
- synchronous request, so long renders will time out on most hosts

## 3. Proposed pipeline

```
source video (own long-form / licensed / clipping-campaign footage)
  │
  ├─► 1. Ingest       download/upload source, store it
  ├─► 2. Transcribe   word-level timestamps (ElevenLabs transcription, or Whisper locally)
  ├─► 3. Select       Claude reads the transcript and returns N moments
  │                   {start, end, hook_title, why_viral, score}
  ├─► 4. Render       ffmpeg (THIS REPO): cut start→end, 9:16 reframe,
  │                   keep source audio, burn word-by-word captions (ASS subs), hook title
  ├─► 5. Review       human approves/rejects (optional: vidIQ virality / title scoring)
  └─► 6. Publish      Blotato (multi-platform scheduling) or vidIQ IG Reel publish
                      + Blotato IG DM automation for "comment KEYWORD" funnels
```

## 4. Suggested phases

**Phase 1: make the render service clip-capable (this repo only)**
- [ ] New endpoint e.g. `POST /clip`: `{source_url, segments:[{start,end}], captions?, title?}`
- [ ] Per-segment trim with `-ss`/`-to`, **keep audio**
- [ ] Caption burn-in from word timestamps via an `.ass` subtitle file (bold, centred, highlighted word)
- [ ] Output storage + retrieval (`GET /jobs/{id}/file` or upload to S3/R2/Drive and return a URL)
- [ ] Async jobs (background task + status endpoint) for long sources

**Phase 2: auto-selection**
- [ ] Transcription step
- [ ] Claude prompt that returns ranked clip candidates as JSON
- [ ] Glue script/service: URL in → N rendered clips out

**Phase 3: distribution + funnel**
- [ ] Publish via Blotato
- [ ] Comment-keyword DM automation via Blotato
- [ ] Track performance (Blotato / vidIQ analytics) and feed winners back into selection prompts

**Later / nice-to-have**
- Face/speaker-tracked reframing instead of centre crop
- Gaming mode: split-screen facecam + gameplay layout (relevant to the GTA 6 angle)
- B-roll / emoji / zoom-punch effects

## 5. Rights and risk (decide before building)

- Clipping **other creators' content without permission** risks copyright strikes and account bans.
- Safe inputs: **our own** long-form content, licensed footage, or official **paid clipping campaigns** where creators pay clippers per view.
- Decide which of these the pipeline is for. It changes priorities: own content → brand polish; clipping campaigns → volume and speed.

## 6. Open questions

1. Is the goal (a) a clipping service for our own channels, (b) earning from clipping campaigns, (c) a product to sell, or (d) content about clipping?
2. Where are the outputs stored and how are they delivered (S3/R2, Google Drive, direct to Blotato)?
3. Where is this service deployed today, and what are its request timeout limits?
4. Captions: Everygen-style word highlight, or simpler sentence captions first?
5. Budget per clip for transcription + Claude selection?
