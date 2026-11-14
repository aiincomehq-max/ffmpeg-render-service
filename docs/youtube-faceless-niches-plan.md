# Faceless YouTube Channels: Plan

**Source:** vidIQ, "The Faceless Niches I'd Start Today (Before Everyone Else Does)". https://youtu.be/rStytOzzLwo, published 9 Nov 2026, about 63k views, outlier score 2.0
**Status:** Brainstorm from a phone session. Pick this up in a Claude Code terminal session on the Mac (vidIQ MCP connected).

---

## 1. What the video says (short version)

vidIQ filtered its data for faceless channels **under 6 months old with fewer than 50 videos** that are already breaking out. It found six niches:

| # | Niche | Example channel / proof | Format | Video's verdict |
|---|-------|-------------------------|--------|-----------------|
| 1 | **Horror survival plans** ("How I'd survive every *Final Destination*") | "Spooky", under 30 videos, 100k+ per video, top video 1.5M | VO + short commentary clips + stills + hand-drawn escape plan | Early. Only a few channels use the format |
| 2 | **Economic rise and fall docs** (products, businesses, places: "Why printer ink costs $6,200/L", "Is Dubai collapsing?") | "Groundbreak", 3 months, about 20 videos, 4 over 100k (20% hit rate) | Documentary VO, stock footage, data graphics | Good, but **every fact needs a source**. Generic AI finance docs are crowded |
| 3 | **Second-person POV finance stories** ("It's 7:41 on a Tuesday, you're microwaving oatmeal…") | "Ollie Finance", 5 months, 13 videos, 5k subs. A Russian copy reached 15k | Stick-figure animation, "you" narration, 20 min | Fresh "costume" on old lessons. Add a not-financial-advice disclaimer |
| 4 | **Historical autopsies** (forensic "case file" on famous deaths) | "Ancient Forensics", weekly uploads, several outliers | Calm narration, public-domain paintings and documents | A fresh slice of a huge niche (dark history, about 500k searches a month) |
| 5 | **"Living in [Country]"** | "Happy Travel 99", 3 months, Norway video at 3M | 4K stock footage, "a year in…" narration | ⚠️ **Too late.** 80+ channels and 150+ videos with the same title in 90 days |
| 6 | **Sci-fi/fantasy book lore deep dives** (Dune, Warhammer 40k) | "Understory" (Dune), about 2M on its top video. "Balter and Blade", 10k subs in 4 months, puts "human-made" in titles | 40 to 90 min deep dives, real reading, human narration | **The host's top pick.** Hard to automate, so it's protected from AI slop. New Dune film coming |

**Main lessons**
1. **First-mover advantage matters more than the niche itself.** Check how crowded a title format is *before* you make anything.
2. YouTube rewards **real research, real footage where you have it, and a real point of view**. Low-effort AI copies get filtered out or demonetized.
3. The work that's hard to automate (reading books, sourcing facts) is what protects the niche from copycats.
4. Copyright: film clips must be **short and actually commented on**, never re-uploads.

---

## 2. The "is it still early?" check (run this before choosing any niche)

Run this in a Claude Code terminal with the vidIQ MCP connected, once for each candidate niche:

```
Use vidIQ to check whether [NICHE] is still early:
1) Find faceless channels created in the last 6 months with under 50 videos that are breaking out.
2) Count how many different channels used the [TITLE FORMAT] in the last 90 days and when each channel started.
3) Give me a verdict on this title concept [TITLE FORMAT]. Am I still early, is it too crowded, am I too late?
```

**My go/no-go rule (a suggestion, tweak as you like):**
- Fewer than 10 channels using the format in 90 days → **GO**
- 10 to 40 → **GO only with a clear twist** (sub-niche, language, angle)
- More than 40 → **NO-GO** (the "Living in [Country]" trap)

---

## 2b. Niche check results (run 14 Nov 2026 via vidIQ)

Method: (a) vidIQ channel search for faceless channels created since 14 May 2026 with ≤50 videos; (b) YouTube search for the title format in the last 90 days (since 16 Aug 2026), up to 50 results, counting distinct channels.

| Niche | Distinct channels using format (90 d) | New breakout channels found | Verdict |
|-------|--------------------------------------|-----------------------------|---------|
| **#4 Historical autopsies** | **About 1** (a single 6-view Short matched "autopsy of historical figure") | **The DNA Casebook** (created June, 18 videos, 314k views, +38% views in 30 d), Candlelit History (sleep-history, 420k views) | 🟢 **WIDE OPEN. Best result.** |
| **#6 Book lore** | Many lore videos, but spread across many fandoms; most are big channels on games/comics | Bolter & Blade (10.5k subs, human-narrated 40k), SOTI More (40k, 15k avg views), Legends of Arrakis (Dune, 41 videos, 3-hour videos), **Echoes of Panem** (101 subs, 25k views on its *first* 2-hour Hunger Games video) | 🟢 **GO, if you pick an under-served fandom** |
| **#2 Economic rise and fall** | 44 channels / 47 videos, but it's a broad genre, not one title format. Big players (WSJ, RealLifeLore) mixed with small breakouts | Truth Vault (2.9k subs → 1.17M views, "Rise and Fall of Big Bazaar"), What Used to Be (5k subs → 163k), The Last Day (36k subs → 5.2M). New: Golden Age Lost, Forgotten Fortunes (AI-made, weak: about 700 avg views) | 🟡 **GO with a tight angle** (e.g. UK high-street brands). Generic AI versions are failing |
| **#1 Horror "How I'd Survive"** | **About 11 channels.** Spo0ky dominates (20+ videos, 1.9M top video). Copycats appeared in Sept/Oct: Crash Test Horror, The Real Horror, Bonsey, Reap (copied Spo0ky's description word for word), Survival Quests, gR!m, Dreggo, Dave's Survival Guide | Copycats under 400 subs still get 15 to 20k on early videos | 🟠 **Closing.** In the 10 to 40 band, so it needs a twist. Copyright risk with film clips |
| **#3 POV finance** | 🔴 **36 distinct channels in 90 days** (POV Finance, Money Life POV, Finance With Henry, Sean On Money, Maxwell Explains, Quiet Money Stories, Retired Life POV…) | Ollie Finance is still growing, but the format is flooded | 🔴 **NO-GO.** Already the "Living in [Country]" trap |

**Updated ranking:** 1) Historical autopsies → 2) Book lore (chosen fandom) → 3) Economic rise and fall (tight angle) → 4) Horror survival (only with a twist) → ✗ POV finance.

### On book lore and "can't AI just read the book?"
Yes, Claude can read a full book in chunks and pull out lore, timelines, and script drafts. But:
1. **Getting the text legally.** Claude can't fetch copyrighted novels. You'd provide your own purchased copy (no DRM-stripping). Or, the strongest option, **pick public-domain series**, where Claude can legally read the full text (Project Gutenberg): **Lovecraft's Cthulhu Mythos, Robert E. Howard's Conan, Burroughs' Barsoom/John Carter, Oz, Arthurian legend, Norse/Greek myth.** That's a fresh twist almost nobody uses, and you can quote the text directly with no copyright problem.
2. **Accuracy.** Lore fans catch every mistake. Working from memory, AI will invent details. Working from the actual text it's reliable, but you still fact-check.
3. **The moat changes, it doesn't vanish.** If AI does the reading, anyone can, so the edge becomes **your voice, taste and editing**. Channels winning here advertise "human-narrated, no AI" (Bolter & Blade) because AI-voiced lore gets called out in the comments. Best combination: Claude does the reading and drafting, **you narrate** (or at least edit hard).

---

## 3. Recommended shortlist

Since you're running several channels next to existing projects, choose by **how much effort each video takes against how well it's protected from copycats**:

| Priority | Niche | Why | Effort per video |
|----------|-------|-----|------------------|
| **A** | #2 Economic rise and fall | Endless topics, good RPM (finance/business), fits a script + stock + data-graphics pipeline | Medium (fact-checking is the work) |
| **A** | #4 Historical autopsies | Public-domain visuals mean no copyright risk. Calm VO suits AI voice or your own narration | Medium |
| **B** | #6 Book lore | Strongest protection and longest watch time, but you have to actually read the series. Choose a fandom you already know | High |
| **B** | #3 POV finance | Clever format, but stick-figure animation takes a lot of production | Medium-high |
| **C** | #1 Horror survival | Strong, but film clips carry copyright/Content ID risk | Medium |
| ✗ | #5 Living in [Country] | Already saturated. Skip it, or use only as a test of the check | None |

**Suggestion:** launch **one A-tier channel first**, get it to a repeatable weekly workflow, then add a second. Two half-run channels do worse than one done properly.

---

## 4. Phased plan

### Phase 0: Validate (terminal session, about 1 to 2 hours)
- [ ] Run the §2 check on niches #2, #4, #6 (and #3 if you're interested). Record the verdicts here.
- [ ] For each GO niche, have vidIQ list 20 video ideas (`vidiq_outliers`, `vidiq_keyword_research`) and score 5 titles (`vidiq_score_title`).
- [ ] Choose **Channel 1**. Note the reason and the competitors to track (`vidiq_update_competitors`).

### Phase 1: Set up the channel (about 1 day)
- [ ] Name, handle, banner, avatar (Higgsfield / vidIQ thumbnail tools for brand assets).
- [ ] Voice: choose one ElevenLabs voice and use it on every video for consistency (or record your own, which helps with the AI-slop defence).
- [ ] Templates: script outline, source-citation sheet (Google Sheets), thumbnail style.
- [ ] Description template that includes **sources** and, for finance, a **not-financial-advice disclaimer**.

### Phase 2: Production pipeline (terminal, in **this repo**)
This is where `ffmpeg-render-service` comes in. Right now it only renders **vertical 1080×1920 Shorts** (clips cut to 1.5 s, text overlays, VO). Long-form faceless docs need:
- [ ] A **16:9 1920×1080 long-form mode** (`/render` with `format: "landscape"`).
- [ ] **Variable clip/still durations** timed to the script, instead of a fixed 1.5 s.
- [ ] **Ken Burns pan/zoom on stills** (essential for #4 paintings and #6 book art).
- [ ] **Background music bed with ducking** under the VO.
- [ ] **Burned-in or sidecar captions** from the VO transcript.
- [ ] Optional **lower-thirds/data callouts** ("$6,200 per litre") for niche #2.
- [ ] Keep the Shorts mode: cut 3 to 5 Shorts from each long video to drive discovery.

Pipeline: **script (Claude) → fact sheet → VO (ElevenLabs) → visuals (stock/public domain/Higgsfield) → render (this service) → thumbnail + title (vidIQ score) → upload / schedule (vidIQ or Blotato) → Shorts cut-downs.**

### Phase 3: Launch and learn (weeks 1 to 8)
- [ ] Publish **1 long video a week + 3 Shorts a week** for 8 weeks.
- [ ] After each video at 48 h and 7 d: check CTR, retention, and outlier score with vidIQ (`vidiq_video_stats`, `vidiq_channel_analytics`).
- [ ] At week 4: double down on the best title format. Drop formats that are underperforming.
- [ ] At week 8: decide whether to **scale Channel 1, add Channel 2 (next A/B niche), or pivot**.

---

## 5. Risks and guardrails
- **Saturation:** run the §2 check again every month. Formats close fast.
- **Copyright:** short clips with real commentary only. Prefer public domain, licensed stock, or generated visuals.
- **Accuracy:** every number on screen needs a source in the citation sheet.
- **Demonetization ("inauthentic content"):** add a real point of view, real research, and consistent human editing decisions. Don't mass-produce templated AI videos.
- **Bandwidth:** one channel at a time until the workflow is repeatable.

---

## 6. Open decisions (for you to settle at the Mac)
1. Which niche(s) pass the check?
2. AI voice or your own narration?
3. For book lore: which series do you already know well?
4. How many hours a week can go to these channels next to existing projects?
5. Extend `ffmpeg-render-service` for long-form, or keep it Shorts-only and use a separate editor for long-form?
