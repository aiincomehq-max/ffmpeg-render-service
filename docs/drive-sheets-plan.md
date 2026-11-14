# DreamReach: Google Drive + Sheets production tracker (plan)
_14 Nov 2026 · runs from this cloud session (Drive and Sheets connectors) or a Claude Code terminal session that has them_

> **Terminal handoff:** `claude "Read docs/drive-sheets-plan.md and CLAUDE.md, then build the Drive folders and tracker sheet"`

## 1. Drive folder structure
```
DreamReach/
├── 00 Tracker/                      ← "DreamReach Production Tracker" (Google Sheet)
├── 01 References/                   ← product photos, logos, character sheets
├── 02 Brands/
│   ├── Wenzels/   ├── Stills/  ├── Clips/  └── Finals/
│   ├── Dior-Unboxing/   (same three subfolders)
│   └── Hermes-Chypre/   (same)
├── 03 Artists/
│   ├── BEMZ-DND/        (same)
│   └── Rimzee-Hometown/ (same)
├── 04 Series/
│   ├── LA-MALLE/        (Day-00 … Day-24, each with Stills/Clips/Finals)
│   └── Dre-and-Mia/     (Characters/, Video-01 … Video-10)
└── 99 Archive/                      ← rejected versions (kept, not deleted)
```
**Sharing:** everything stays **private to you** by default. Only finals get "anyone with the link" when you want to send one to a brand or artist.

## 2. The tracker sheet: 5 tabs
**Videos** (one row per finished video)
| ID | Project | Title | Status | Length | Final (Drive URL) | Caption | Tags | AI label | Posted to | Post URLs | Credits | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
Status values: `Planned → Stills → Stills approved → Animating → QC → Final → Posted`

**Shots** (one row per shot: the complete record behind every video)
| Video ID | Shot | Description | Image prompt | Motion prompt | Model | Image job ID | Image URL | End-frame ID | Clip job ID | Clip URL | QC result | Fix applied | Credits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
**QC result** = pass/fail plus the reason, e.g. *"bottle taller than drawer"*. **Fix applied** = trim / zoom / reverse / regenerated.

**Rejected** (what failed and why: the record that stops the same mistake twice)
| Date | Video | Shot | Problem | Caught at (prompt / still / clip / final) | Credits wasted |

**Credits** (the spend log)
| Date | What | Credits | Balance after |

**References**
| Asset | Source | Drive URL | Higgsfield media ID | Notes (e.g. scale: 100ml bottle ≈ ⅔ of the hand) |

## 3. Where URLs come from
- **Images and clips:** Higgsfield already hosts every render at a permanent link (`d8j0ntlcm91z4.cloudfront.net/...`). The sheet stores those links, so there's **no upload needed** for the ~150 images and ~70 clips made so far.
- **Finals (12 videos so far):** uploaded to `Finals/` in Drive, with the Drive link in the **Videos** tab. Each upload needs **your tap to approve** (the Drive connector requires it per file). Faster alternative on the Mac: drag the repo's `deliverables/` folder into Drive, then I fill in the links.
- **References:** the Dior photo, sandal photo, Wenzel's logo and the Dre & Mia sheets get uploaded to `01 References/` (4–6 approvals).

## 4. Back-filling everything made so far
All the data already exists in the repo: `prompts/*.md` (prompts, image IDs, rejections) and `jobs/*.json` (clip lists and trims).
I turn that into rows: **about 12 videos, ~120 shots, ~25 rejections**, plus the credits history.

## 5. From now on (added to CLAUDE.md)
For every new video:
1. **Plan** → add a row to **Videos** with status `Planned`, and the shot rows to **Shots** with their prompts.
2. **Images made** → add the image IDs and URLs, set the status to `Stills`.
3. **You approve** → `Stills approved`.
4. **Clips made** → add the clip IDs and URLs, plus the QC result for each shot.
5. **Final rendered** → upload it to `Finals/`, add the Drive URL, set the status to `Final`, and log the credits.
6. **Posted** → you tell me the post links and I add them, set to `Posted`.

## 6. Cost and effort
- **Credits:** none. This is all Drive and Sheets.
- **Your approvals:** about 12 for the finals and about 6 for references (or one drag-and-drop on the Mac instead).
- **Time:** about 20–30 minutes of tool calls to build and back-fill.

## Decisions
1. **Finals:** upload from here (about 12 taps) or drag `deliverables/` into Drive on the Mac?
2. **Top-level folder name:** "DreamReach" OK?
3. **Go:** reply **"go drive"** to build it.
