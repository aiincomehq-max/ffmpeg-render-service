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

---

## 7. YouTube clipping account research (vidIQ, 7 Nov 2026)

Data source: vidIQ channel search (60 channels: 30 "breakout" generic clip channels plus 30 streamer-clip channels with 5M+ Shorts views in the last 30 days), then the top or most recent Shorts from 4 winners. Earnings figures are vidIQ *estimates*.

### 7.1 The single biggest finding
**Generic "viral clips" channels lose. Single-creator fan-edit channels win.**
- Generic "viral moments / funny clips / rankings" channels found by breakout search mostly average **1k–40k views** per Short.
- Channels that clip **one streamer or one friend group** dominate:

| Channel | Who they clip | Subs | Avg views/video | Shorts views (30d) | Est. $/mo | Notes |
|---|---|---|---|---|---|---|
| Nexxo Recaps | iShowSpeed only | 1.07M | 13.4M | 653M | ~$11.6k | Created **Jan 2026**. 148 Shorts total |
| OnShortz | Kai Cenat / Rakai / AMP | 225k | 3.8M | 68M | ~$2.3k | Created Apr 2025. 123 Shorts |
| core_fx | Core Boys (Lacy, Ron, Jason, Marlon) | 144k | 1.0M | 96M | ~$4.4k | 2–3 Shorts/day, faceless |
| LosPollosTv | own streams + clips | 137k | 1.0M | 103M | ~$3.0k | |
| Livestreams Memes | Twitch/Kick gaming streamers | 133k | 532k | 71M | ~$3.8k | Longer Shorts (~110s) |
| JoeShortz | iShowSpeed | 170k | 388k | 38M | ~$1.9k | Created Oct 2025 |
| trashclips | AMP / Kai / Rakai | 118k | 264k | 34M | ~$1.8k | |
| Fumous | Kai/Speed/AMP "cinematic" edits | 12k | 2.1M | 8M | ~$100 | Only **18 Shorts**: low volume, high effort |
| Burntpeanutclips | TheBurntPeanut (fan account) | 76k | 129k | 43M | ~$6.5k | 37 Shorts/week |
| StumbleRondale | StableRonaldo | 37k | 172k | 31M | ~$1.1k | |

New channels can still blow up in 2026: Nexxo hit 1M in about 10 months, and JoeShortz and Blue Cucumber both started in late 2025.

### 7.2 The format, reverse-engineered

**Length** (keep it short; longer is not better):
- Nexxo: 40–59s (story arc with a payoff "at the end")
- OnShortz / core_fx / Fumous: **10–30s** (one moment, one punchline)

**Title formulas that keep repeating:**
1. **Open loop to the end** (Nexxo, the top performer):
   `No way he [did X] at the end 😳 #ishowspeed` · `The picture at the end is UNBELIEVABLE ❤️‍🩹` · `Speed didn't even dare to try the last one 💀`
2. **[Name] + reaction verb + specific detail** (core_fx, OnShortz):
   `Lacy Got Hit With A $12,000 Restaurant Bill 😭💸` (12.4M) · `Jason Got Banned In QT Cinderella's Chat 😭💀` (4.3M) · `Rakai Accidentally Woke Up Rayquan 😭💀` (94M)
3. **Celebrity crossover** (Kevin Hart, MrBeast, Ronaldo, Druski) → `Kai Cenat gets COOKED by Kevin Hart 😭🥀` (9.2M)
- Always 1–2 emojis at the end, from 😭 💀 😳 ❤️‍🩹 🥀 🔥 💸. Specific numbers and money do well.
- Hashtags: 0–2, usually the creator's name (`#ishowspeed`, `#kaicenat`) plus optional `#shorts`.

**How often they post:**
- Volume model: core_fx 2–3/day, Burntpeanutclips ~5/day, Clips Edge ~6/day
- Quality model: Nexxo ~1/day, OnShortz ~4/week, Fumous ~2/month (and still averages 2M)

**Hit rate is a power law.** In core_fx's last ~50 Shorts, most got 30k–100k and about 8 went over 1M. The account lives on the outliers, so volume plus speed after a stream ends is the lever.

### 7.3 How they stay monetized (relevant to the Oct 2026 reused-content crackdown)
Nearly every winning channel's description says the same things:
- "Heavily edited / transformed": new pacing, **animated captions, zooms, custom SFX, music, restructuring**, sometimes voiceover or commentary
- "Not impersonating / not affiliated" disclaimer + contact email for takedowns
- A fair use (Section 107) statement

So the edit layer is what lets the channel monetize, not decoration. A raw cut + static captions (what `/render` does today) will be treated as reused content.

### 7.4 Implications for our build
1. **Niche choice:** one big streamer or crew with daily streams and a hungry fanbase (Speed, Kai/AMP, Core Boys, or a rising Kick streamer with fewer clippers). Check whether that creator runs a **paid clipping programme**, which gives us permission plus per-view pay on top of ad revenue.
2. **Speed matters:** clip within hours of the stream. The pipeline should ingest VODs/live archives automatically.
3. **The render service must produce the "transformed" edit, not a raw cut:**
   - [ ] segment cut with source audio kept
   - [ ] smart 9:16 reframe (face/subject tracking, or split facecam + gameplay)
   - [ ] word-by-word animated captions (ASS, highlight current word, bold, centred lower-third)
   - [ ] punch-in zooms on the key moment, SFX hits (whoosh/vine boom/bass), low music bed
   - [ ] optional hook text overlay in the first 1–2s
   - [ ] target 15–30s (one-moment format) or 40–59s ("at the end" story format)
4. **Selection prompt:** Claude ranks transcript moments by "payoff at the end", celebrity crossover, money or numbers, and emotional or wholesome beats. It also writes 3 titles per clip using the formulas in 7.2.
5. **Volume target:** start at 2–3 Shorts/day on one channel. Track which title formula and length wins, then double down.

### 7.5 Next research (cheap, when credits reset 11 Nov)
- Pull one niche's top Shorts across 5–10 competing clip channels (vidIQ `channel_videos`, 5 credits each) to measure how saturated that niche is
- Check which large streamers currently run paid clipping programmes
