# BIG BEAR — MANUAL CREATIVE PRODUCTION SOP

**Version:** v3.1 · 2026-10-08 · Chairman-issued (supersedes v3.0 and all earlier versions)
**v3.1 change (ROLE MODEL REPLACED):** Production ownership moved from the Claude app / Cowork to **ChatGPT**
(creative lead + production controller). **Claude Code** returns as custodian / ledger / QA / scheduling support
only. The Claude app / Cowork is removed from the active Big Bear production chain unless the Chairman explicitly
reintroduces it for a bounded task. §2 replaced in full; actor names in §3–§21 reassigned to match. No production
rule changed. Two open items are listed in §20.
**v3.0 change (SUPERSEDED by v3.1):** ChatGPT removed from every role; the Claude app did every job in the lane.
**v2.6 change:** new §21 MODEL PROMPT-ENGINEERING REFERENCE (Nano Banana Pro · GPT Image 2.5 · Seedance), read before
writing / approving any paid prompt; pointer added in §8; §15 pre-spend report confirms the §21 check.
**v2.5 change:** new §7A MODEL-FACING PROMPT LANGUAGE (self-contained image / video prompts; no names or memory references).
**v2.4 change:** §6 adds the standing DEFAULT BIG BEAR VOICE (ElevenLabs Big Bear2 / v3) and PAUSE HANDLING.
**v2.3 change:** §18 adds the mandatory CapCut clean step (true 9:16 conform + "Ai" mark mask) for every export.
**v2.2 change:** §20 `BB_MANUAL_001` reconciliation item marked COMPLETE. No production rule changed.
**v2.1 change:** §7 default reference-image model corrected to Nano Banana Pro at 2K (was GPT Image 2.5);
§20 open item clarified (rows written by Cowork/App; read-back procedure). No other production rule changed.
**Canonical (AUTHORITATIVE):** `My Drive/BIG_BEAR/00_GOVERNANCE/BIG_BEAR_MANUAL_CREATIVE_SOP.md`
**Local working mirror (Claude Code):** `terminal-logs/BIG_BEAR_MANUAL_CREATIVE_SOP.md`

The Google Drive version is the source of truth. If the two ever differ, the Drive version wins and the
mirror is re-synced from it. There is exactly one Big Bear manual-production SOP; do not create another.

### Change log

- **v3.1 — 2026-10-08.** Reassigned Big Bear manual production ownership from Claude app/cowork to ChatGPT.
  Claude Code remains custody / ledger / scheduling support only. Claude app/cowork removed from default
  production path.

---

## 1. PURPOSE / GOVERNING PRINCIPLE

Big Bear is produced manually, with a human in the loop at every creative decision.

    MAKE ONE GOOD VIDEO
    → FINALISE IT
    → BANK OR PUBLISH IT
    → MEASURE
    → LEARN
    → MAKE THE NEXT ONE BETTER.

No automation before creative proof. No n8n, watchers, schedulers or new infrastructure for this lane
unless the Chairman separately authorises it.

---

## 2. ROLE OWNERSHIP

### 2.1 CHAIRMAN / USER

Final decision-maker.

Responsibilities:
- approve / reject concepts
- approve / reject scripts
- approve / reject spend
- inspect stills, renders and edits
- decide rerender / rescue / abandon
- perform CapCut finishing where desired
- approve the final master before publication

No repeated paid generations without approval.

### 2.2 CHATGPT — CREATIVE LEAD + PRODUCTION CONTROLLER

ChatGPT is the primary operating partner for Big Bear manual production.

Responsibilities:
- select and develop concepts from the pool
- decide the story mechanic, emotional turn and payoff
- write the script
- write the full prompt pack
- choose tool / model (within the standing defaults in §6, §7 and §21.3; any deviation needs Chairman approval)
- specify still-generation prompts
- specify video-generation prompts
- specify timing plan from measured VO length
- specify sound design / ambience requirements
- review outputs with the Chairman
- diagnose failures
- plan the next correction
- control generation strategy end-to-end

For Big Bear, ChatGPT must preserve the Big Bear doctrine and not import unrelated project aesthetics.

ChatGPT owns:
- script
- image prompts
- video prompts
- timing structure
- render strategy
- creative iteration logic

### 2.3 HIGGSFIELD

Higgsfield is a generation tool only.

Use cases:
- still generation
- image-to-video
- text-to-video where appropriate
- continuation / correction renders
- targeted fixes

Important:
- do not spend credits casually
- one approved generation at a time
- every render must have a clear purpose
- before spend, provide model, duration, settings, prompt and expected credit cost
- after render, record actual credits used

### 2.4 ELEVENLABS

ElevenLabs is the voice tool.

Default Big Bear voice unless explicitly overridden (full specification in §6):
- Voice: Big Bear2
- Model: v3
- Delivery: warm, low-key, conversational, with natural drawl accepted as part of character

Rules:
- script comes first
- then voice generation
- then measure exact VO duration
- then build timing around that actual duration
- do not let punctuation create exaggerated pauses without approval
- deterministic trimming of excessive silence is allowed
- do not rewrite wording without approval

### 2.5 CAPCUT

CapCut is the Chairman's finishing tool.

Typical use:
- final timing trim
- text / captions / hook
- font choice
- music / SFX / ambience finishing
- minor polish
- export of final master

### 2.6 CLAUDE CODE TERMINAL

Claude Code is custodian / ledger / scheduling support only, not the creative lead.

Responsibilities:
- create Drive folders when needed
- maintain sheet rows / ledger / provenance
- preserve assets
- run technical QA on the final approved export (§18, including the mandatory clean step)
- store prompts, IDs, credits, lineage and captions
- schedule in Blotato if requested
- verify publication state if requested

Claude Code does not own:
- concept
- script
- prompts
- video direction
- generation strategy

It acts only after direction from the Chairman and / or ChatGPT.

### 2.7 CLAUDE APP / COWORK

Claude app / Cowork is not part of the default Big Bear production chain.

It is excluded unless the Chairman explicitly assigns it a bounded task.

It must not:
- take over prompting by default
- control creative direction
- initiate generations for Big Bear without explicit assignment

### 2.8 BIG BEAR MANUAL WORKFLOW

Default loop:

    idea selection
    → ChatGPT + Chairman develop concept
    → ChatGPT writes script
    → ChatGPT writes still prompt
    → Chairman approves spend
    → still generated
    → Chairman + ChatGPT inspect
    → ChatGPT writes video prompt
    → Chairman approves spend
    → render generated
    → Chairman + ChatGPT inspect
    → targeted correction if justified
    → CapCut finishing by Chairman if desired
    → final master approved
    → Claude Code handles QA / custody / ledger / scheduling

### 2.9 SPECIAL BIG BEAR RULES

- Do not use character names in model-facing prompts. Describe them visually (§7A).
- Build video duration from measured VO length (§6, §9).
- Default image generation model for Big Bear stills: Nano Banana Pro (at 2K, §7) unless explicitly changed.
- Default video rule: use the approved still as the starting image when doing image-to-video.
- Prompts must include atmospheric sound intent when relevant (§12).
- Avoid wording that induces slow-motion walking unless explicitly desired (§10).
- Keep Blade silent; his contribution is visual reaction only (§5, §10).
- Still framing must not box the video model into an unusably tight start frame (§7).
- Show the exact prompt before spend (§15).

### 2.10 OPERATING PRINCIPLE

Keep the process manual, controlled and quality-first.

Do not build more machinery before the creative works.

---

## 3. START OF EACH VIDEO (ChatGPT + Chairman select; Claude Code sets up on direction)

1. ChatGPT and the Chairman select the concept; Claude Code creates the next `BB_MANUAL_00X` ID.
2. Claude Code creates the Drive folder `BIG_BEAR/04_EPISODES/BB_MANUAL_00X/`.
3. Claude Code creates / updates the video's `MANUAL_CREATIVE` row in `BIG_BEAR_PRODUCTION` (never `EPISODE_QUEUE`).
4. Claude Code retrieves, from the source tables, and hands to ChatGPT:
   - source master ID
   - exact original transcript
   - source URL
   - source metrics
   - creator / account details
   - relevant lineage

---

## 4. SOURCE ANALYSIS / CREATIVE THESIS (ChatGPT + Chairman)

Define:
- why the original worked;
- what emotional / mechanical truth transfers;
- what must NOT be copied;
- the Big Bear-specific adaptation thesis.

---

## 5. BIG BEAR SCRIPT LAW

The default script is THREE BEATS:

1. specific observation / setup
2. concrete turn / human detail
3. emotional payoff

- No generic motivational-quote writing.
- Bear speaks naturally to Blade.
- Blade NEVER speaks.
- Blade responds through restrained looks and body language.

---

## 6. VOICEOVER GOVERNANCE

CRITICAL ORDER:

    SCRIPT LOCK
    → GENERATE FINAL VO
    → MEASURE EXACT VO
    → DESIGN VIDEO TIMING
    → CHOOSE VIDEO DURATION
    → GENERATE VIDEO

**Video length is governed by the VO.** Do not choose a render duration first and stretch the VO to fit.

The Prompt Pack must specify:
- exact script
- voice
- voice model / version
- delivery
- pace
- emotional tone

The VO is measured and reported (who measures: see §20 open item v3.1-A):
- exact VO duration
- speech start
- speech end
- meaningful internal pauses

ChatGPT builds the timing plan (§9) from those measurements.

### DEFAULT BIG BEAR VOICE

| field | standing default |
|---|---|
| Provider | ElevenLabs |
| Voice | Big Bear2 |
| ElevenLabs Voice ID | `TZfV6mWOAvPylRYbxCfh` |
| Default model | ElevenLabs v3 |
| Default delivery | warm, low-key, conversational, with natural drawl accepted as part of character |

Character direction:
- Big Bear speaks naturally to Blade, not to camera.
- Low-key and grounded.
- Warm without becoming sentimental.
- Reflective without sounding motivational.
- Normal real-world conversational pace.
- No theatrical delivery.
- No exaggerated emotional reactions.
- No unnecessarily long dramatic pauses.

The Prompt Pack still owns the exact script and may specify a different delivery where the scene genuinely
requires it.

The Chairman may explicitly approve a different ElevenLabs model, voice or delivery for a specific video.
Absent such an explicit override, the standing Big Bear default is:

    Big Bear2 · TZfV6mWOAvPylRYbxCfh · ElevenLabs v3 · warm / low-key / conversational / natural drawl accepted

ChatGPT must NOT ask which Big Bear voice / model to use on every video when this default applies.
ChatGPT raises the voice / model in its pre-spend review (§14) only if there is a specific technical or
creative reason to deviate from the standing default.

### PAUSE HANDLING

Punctuation in the script must not be allowed to create obviously exaggerated artificial pauses.

Where an otherwise-approved ElevenLabs take contains an excessive silence caused by punctuation, ChatGPT may
propose a deterministic trim in its pre-spend review (§14). Deterministic trimming of excessive silence is
allowed; it never changes the words.

Nobody changes an approved script without the Chairman's approval.

---

## 7. REFERENCE IMAGE — MANDATORY STEP

The reference still is FRAME ZERO of the video and must be designed for motion.

**Default reference-image model: Nano Banana Pro at 2K.**

Use Nano Banana Pro at 2K for Big Bear reference-image generation unless the Chairman explicitly approves a
different image model for a specific shot.

GPT Image 2.5 may be used as an alternative where there is a clear creative or technical reason, but it is
NOT the default.

Every Prompt Pack MUST include a separate REFERENCE IMAGE PROMPT.

Reference-image rules:
- 9:16
- normally WIDER than the final desired video framing
- camera far enough back to give the video model room
- Bear and Blade both clearly readable
- walking scenes preferably full-body or comfortably knee-up
- enough space ahead of the direction of travel
- enough lateral / depth room for camera tracking
- the emotional / background subject remains visible
- avoid tight portrait framing
- avoid cropping Blade
- avoid forcing the video model to invent missing limbs / bodies
- preserve the environment the story needs
- design pose and staging with the later video movement in mind

The reference image MUST be inspected and approved before any video-generation spend.
If the framing is bad, fix the still first. Do not ask the video model to rescue a poor starting composition.

---

## 7A. MODEL-FACING PROMPT LANGUAGE

Production notes, Prompt Packs and internal coordination may use project names and character names for
clarity.

However, the ACTUAL text sent to an image or video generation model must be self-contained and describe only
what the model can directly see, hear or perform.

Do NOT rely on:
- character names alone;
- project names;
- "the previous attempt";
- "same as last time";
- "keep the approved look";
- "don't crop him again";
- "use the previous framing";
- any other instruction that assumes the generation model has memory of earlier prompts or renders.

Instead, model-facing prompts must explicitly describe:
- visible character type / species;
- clothing;
- position in frame;
- relative position to other subjects;
- body scale / proportions where relevant;
- camera distance;
- direction of travel;
- action;
- timing;
- environment;
- lighting;
- sound;
- exact framing / composition.

Example:

| internal production note | model-facing instruction |
|---|---|
| "Keep Blade nearest camera." | "The black panther walks on the side nearest the camera, slightly ahead of the large anthropomorphic brown bear, remaining fully visible throughout the shot." |
| "Don't repeat the tight framing from the last attempt." | "Use a medium-wide full-body composition with generous space around both foreground subjects and visible environment ahead of their direction of travel." |

### REFERENCE IMAGE RULE

The reference-image prompt must be fully self-contained even when reference images are supplied.

Reference assets provide identity / appearance conditioning. The text prompt still defines:
- scene;
- staging;
- camera;
- composition;
- action-ready pose;
- environment;
- lighting;
- spatial relationships.

### VIDEO PROMPT RULE

The video prompt must also be fully self-contained. It must describe:
- what each visible subject is;
- where each subject is positioned;
- exactly what each subject does;
- camera movement;
- timing;
- sound;
- end-state composition.

Do not assume the video model understands production names or remembers prior iterations.

---

## 8. SEEDANCE PROMPT-ENGINEERING RULE (MANDATORY)

Before ChatGPT writes EVERY Seedance prompt, it must refer to the latest available Seedance
prompt-engineering documentation / project notes, and check current guidance for:

- reference-image conditioning
- subject motion
- camera motion
- natural gait
- multi-subject stability
- dialogue / audio
- lipsync behaviour
- duration constraints
- timing behaviour
- negative instructions
- continuity
- current model limitations

Do not blindly reuse an old Seedance prompt.
If the latest documentation is unavailable, that must be stated BEFORE spend.

**The project's prompt-engineering reference for every paid model — Nano Banana Pro, GPT Image 2.5 and
Seedance — is §21 of this SOP.** ChatGPT reads the relevant §21 subsection before WRITING any image or video
prompt, and checks the prompt against it again before asking the Chairman to APPROVE any spend.

---

## 9. TIMING GOVERNANCE

The measured VO determines final timing:

    opening visual beat
    + exact VO duration
    + closing visual beat
    = desired video duration

Seedance currently supports whole-second duration choices only.
**Any surplus duration MUST be explicitly choreographed.** Do not leave spare seconds for the model to fill.

Unplanned surplus can cause:
- stretched speech
- slow-motion gait
- floating / low-gravity walking
- dead time
- unwanted camera movement
- loss of the closing beat

---

## 10. BIG BEAR VIDEO PROMPT RULES

The prompt must explicitly define:

**BEAR**
- natural conversational performance
- speaks to Blade
- no direct-to-camera presentation unless intentional
- restrained, natural movement

**BLADE**
- never speaks
- remains visible
- subtle / lazy / knowing acknowledgement where appropriate
- no exaggerated animal performance

**WALKING**
- normal, relaxed, real-world pace
- natural stride
- believable body weight
- no slow motion unless deliberately requested
- no floating
- no skipped / looped step behaviour
- dialogue timing must not slow the gait

**BACKGROUND**
- keeps moving naturally
- does not freeze while Bear talks
- remains part of the story

**CAMERA**
- exact starting framing
- exact tracking / pan / push behaviour
- speed
- framing relationship
- Bear and Blade both preserved where required
- the emotional background subject preserved where required
- exact closing composition

Do not use vague instructions such as "cinematic", "slow", "calm" or "push in" without physical detail.

---

## 11. CLOSING BEAT

Every video should deliberately reserve a final visual payoff where appropriate.
Typical target: ~1–2 seconds after the final spoken phrase.

Possible actions:
- Blade gives a knowing look;
- Bear / Blade glance back;
- the camera returns attention to the human moment;
- background action continues after the speech.

The closing beat must be budgeted BEFORE generation.

---

## 12. SOUND DESIGN

Every Prompt Pack must state:
- environmental ambience;
- footsteps;
- traffic / birds / wind / room tone / etc.;
- relevant diegetic sound;
- whether music should be generated in-scene, or whether the Chairman will add music later in CapCut.

Silence happens only intentionally.

---

## 13. COMPLETE PROMPT PACK

Before any paid generation, ChatGPT provides (A–E supplied by Claude Code from the source tables, §3):

- A. Manual ID
- B. source master ID
- C. source URL
- D. source metrics
- E. original viral transcript
- F. why the original worked
- G. Big Bear adaptation thesis
- H. final three-beat script
- I. voice specification
- J. reference-image prompt
- K. reference-image approval checkpoint
- L. final VO
- M. exact VO measurements
- N. timing block
- O. final video prompt
- P. provider / model / settings
- Q. quoted credit cost
- R. expected output
- S. primary medium-length platform caption
- T. five SEO-woven caption variants where required
- U. five SEO tags / hashtags

No paid generation runs until the Chairman approves the Prompt Pack.

---

## 14. PRE-SPEND REVIEW

Before asking for spend approval, ChatGPT reviews its own Prompt Pack once against §7, §7A and §21, and states
plainly any concern or recommended change, with:
- the proposed change
- why it helps
- the cost / timing implication where relevant

The Chairman then decides: **ACCEPT / REJECT / AMEND.**
No silent implementation.

---

## 15. GENERATION RULE

ONE paid generation at a time unless the Chairman explicitly approves more.

Before spend, ChatGPT reports:
- provider
- model
- duration
- resolution / settings
- exact prompt
- exact quoted credits
- confirmation that the prompt was checked against the relevant §21 model reference (state which subsection)

Then waits for **GO**.

After generation, the following are reported (who executes and reports: see §20 open item v3.1-B) and passed to
Claude Code for the ledger:
- provider / model
- job / generation ID
- actual credits charged
- technical result

Then STOPS for inspection by the Chairman and ChatGPT.

---

## 16. FAILURE REVIEW (ChatGPT + Chairman)

Before rerendering, diagnose:
- reference still
- framing
- script
- VO timing
- surplus duration
- gait
- camera
- Blade behaviour
- background motion
- sound
- lipsync
- model limitations

Do not default to another paid render.

---

## 17. CAPCUT / FINAL MASTER (Chairman)

The Chairman finishes in CapCut where useful:
- trims
- timing
- sound effects
- music
- ambience
- text
- colour / filter
- final audio
- final inspection

The final export goes to `BIG_BEAR/04_EPISODES/BB_MANUAL_00X/` under a governed final filename.
The Chairman then states: **FINAL MASTER APPROVED**.

Claude Code does not register intermediate or rejected generations.

---

## 18. FINAL MASTER CUSTODY (Claude Code)

After FINAL MASTER APPROVED, Claude Code:

1. locates the final master;
2. performs technical QA (filename, duration, resolution, fps / frames, audio present, no black bars,
   no watermark, no corruption);
3. preserves the original master unchanged;
4. **cleans EVERY export before it can be READY (mandatory, Chairman standing rule):**
   - conform to a TRUE 9:16 1080×1920 publish file — CapCut exports a 1080×2038 letterboxed canvas, which
     is NOT 9:16; remove the black bands without cutting picture (prove every dropped row is black,
     uniform scale, no stretch);
   - mask the top-left Seedance / CapCut "Ai" mark if present, with the minimum clean treatment (exact
     9:16 crop clearing the mark, scaled back; no blur box or visible patch);
   - audio stream-copied and verified identical; frame count unchanged; frames inspected by eye;
   - method = the estate's proven `conform` + `mask_watermark` treatment (reference implementation:
     `products/huhq-psy-video-arm/source/publish_video.py`), or an equivalent that meets every check above;
     the cleaned file is uploaded beside the original as `<FINAL_NAME>_CLEAN_1080x1920.mp4` and is the file
     that publishes;
5. updates `MANUAL_CREATIVE` and the ledgers (`ASSET_LIBRARY`, `RENDER_LEDGER`), then reads every written row
   back to confirm it;
6. reconciles assets / credits / provenance;
7. records:
   - source
   - script
   - reference-image prompt
   - video prompt
   - VO spec
   - timing
   - provider / model
   - job IDs
   - credits
   - final filename
   - Drive URL
   - duration / resolution / audio
   - captions (as written by ChatGPT in the Prompt Pack, §13 S–U, or as finalised by the Chairman)
   - tags
8. schedules via Blotato if distribution is authorised — verifying account, platform, time and media, checking
   every submission's status, and recording submission IDs and URLs;
9. otherwise marks the master **READY / UNSCHEDULED**, keeps its Drive URL, and never invents a destination.

---

## 19. DISTRIBUTION

Big Bear does not currently require a dedicated platform home.
Multiple completed videos may be banked before choosing where they publish.
Do not block creative production waiting for account allocation.

---

## 20. RECORD-KEEPING

Do not create duplicate or competing SOPs.

- **Canonical SOP:** `My Drive/BIG_BEAR/00_GOVERNANCE/BIG_BEAR_MANUAL_CREATIVE_SOP.md`
- **Local terminal mirror:** `terminal-logs/BIG_BEAR_MANUAL_CREATIVE_SOP.md`
- **The Drive version is authoritative.** Any change is made to the Drive copy first, then mirrored locally.
- Claude Code is the owner of all Big Bear Sheet writes from v3.1. Read rows back after every write.

### Open items (v3.1)

- **v3.1-A — VO measurement owner.** The v3.1 amendment requires the VO to be measured before timing is built,
  but does not assign who measures it. Until the Chairman decides, the Chairman generates the take and either
  measures it or directs Claude Code to measure it deterministically (duration, speech start / end, internal
  pauses) and hand the numbers to ChatGPT.
- **v3.1-B — Generation / VO executor.** The v3.1 amendment gives ChatGPT control of generation strategy and
  makes Higgsfield / ElevenLabs tools only, but does not name who presses GO in Higgsfield and ElevenLabs.
  Claude Code does not own generation (§2.6) and the Claude app / Cowork is excluded (§2.7). Until the Chairman
  decides, the Chairman executes approved generations and reports job ID and actual credits to Claude Code for
  the ledger.

### Estate references

| item | location / ID |
|---|---|
| `BIG_BEAR` root folder | `1lrOOPhQRMKwlTPGEZ-ESJD914hQmK3eK` |
| `00_GOVERNANCE` folder | `1gEIdGJrdU_0V4EU4LLKcLme3-ckCikNN` |
| `04_EPISODES` folder | `1NRFYAYl7fTtHxsEFhYLh05Jvt6VVJdFR` |
| `BIG_BEAR_PRODUCTION` sheet (`MANUAL_CREATIVE` tab) | `1owQYkUdTlUg2zydh2mx48Lku6E3avrmvsR5wQSWvb1Q` |

### BB_MANUAL_001 reconciliation — COMPLETE (2026-10-07, accepted by the Chairman)
The `BB_MANUAL_001` rows MANUAL_CREATIVE r2, ASSET_LIBRARY r76 and RENDER_LEDGER r58 were written by
Cowork/App through the Google Sheets connector, before the current role boundary was locked.

Claude Code read all three back (read-only) and verified them against the known `BB_MANUAL_001` state:
all values match, with no conflict and no duplicate record. The factual read-back is kept in
`terminal-logs/BIG_BEAR_MANUAL_001_CHECKPOINT_2026-10-07.md`. (Historical: Sheet ownership passed to
Claude Code, then to the Claude app in v3.0, and back to Claude Code in v3.1.)

Three observations were reviewed. By Chairman decision, no Sheet edit is made for any of them:
1. MANUAL_CREATIVE still status — left unchanged. Still v1 is being superseded by a new, wider reference
   still; the status is not updated before the replacement exists.
2. ASSET_LIBRARY reference-ID format (Drive file IDs) — left unchanged. The references are unambiguous and
   the asset IDs are preserved in notes. No schema or historical-format repair is authorised.
3. RENDER_LEDGER `credits_consumed` blank — left unchanged. The 2 Higgsfield credits are recorded in
   MANUAL_CREATIVE and the row notes. The historically Kie-oriented column is not repurposed.

---

## 21. MODEL PROMPT-ENGINEERING REFERENCE (read before writing or approving any paid prompt)

**MANDATORY.** ChatGPT reads the relevant subsection below before writing any image or video prompt, checks the
prompt against it again before asking for spend approval, and states which subsection was checked in its pre-spend
report (§15). The Chairman may check it too before approving. §7A (self-contained model-facing language) applies
to every model.

Each subsection separates **VENDOR GUIDANCE** (from the provider's own documentation, with its date) from **PROJECT
LESSONS** (what our own paid generations have proven). If a provider's documentation has changed since the date
shown, the newer official guidance wins and this section is updated (Drive first).

### 21.1 Nano Banana Pro (Google Gemini 3 Pro Image) — DEFAULT reference-image model (§7)

VENDOR GUIDANCE — Google, "7 tips to get the most out of Nano Banana Pro" (published 2025-11-20):
- Build the prompt from five parts: **Subject** (specific, e.g. species, clothing, distinguishing features) ·
  **Composition** (shot size and angle: wide, full-body, low angle) · **Action** (what is happening) ·
  **Location** (the scene) · **Style** (e.g. "photorealistic cinematic film still").
- Define the canvas in words as well as settings, e.g. "9:16 vertical".
- Direct it like a cinematographer: lens / depth of field, camera height and angle, colour grade, light direction
  and quality (e.g. "warm porch light, soft blue dusk sky").
- Write in full sentences, not comma-separated keyword lists. Put the most important detail first: earlier words
  carry more weight.
- When supplying reference images, **state the role of each one** (identity, pose, style or background).
- Resolution options are 1K / 2K / 4K; the Big Bear default is 2K (§7).
- Known limitations (vendor-stated): small text and fine detail can be imperfect; complex blending can create
  artefacts; **character consistency across edits may vary**, so inspect identity on every output.
- Source: https://blog.google/products/gemini/prompting-tips-nano-banana-pro/

PROJECT LESSONS:
- **A reference image anchors POSE as well as identity.** 2026-08-08: two front-facing character sheets made the
  model render the bear square to camera, twice, despite a capitalised three-quarter-walk instruction later in the
  prompt. What worked: put the pose / framing directive FIRST and scope the references explicitly — "the reference
  images govern identity and appearance only, never pose or framing".
- **Write the prompt against what each reference image actually shows**, not what it was meant to show. Open
  every reference before citing it.
- **Text cannot carry continuity between separate generations.** "The exact same room" / "same as before"
  produced different locations every time. Continuity must come from an image reference (see §7A).
- **Inspect the output for staging before wardrobe**: who is facing whom, who is speaking to whom, what is in front
  of whom, and whether there is room for the planned motion (§7). Then check clothing and props.
- BB_MANUAL_001 still v1 (Higgsfield `nano_banana_2`, 2K, 1536×2752): identity held, but the composition was
  too tight for the video model. Frame wider than the final video framing.

### 21.2 GPT Image 2.5 — ALTERNATIVE reference-image model (only with a clear reason, §7)

VENDOR GUIDANCE — OpenAI, "Image prompting" developer guide (read 2026-10-08):
- Define the result first: subject, intended use, composition, aspect ratio and placement constraints.
- Describe visible details: materials, lighting, colours, medium. Ask explicitly for "photorealistic" or "a real
  photograph". Describe framing and texture rather than relying on mood words alone.
- **People and action**: state body framing, relative scale, gaze and object interaction, e.g. "full body
  visible, feet included".
- Photorealism levers: named light ("soft dusk light"), lens ("50mm lens"), depth of field, film grain,
  "honest and unposed". Avoid heavy-retouching language.
- **Reference images: give each input a number and a role** (subject, style, clothing, background).
- **Restate the critical constraints in every prompt.** Phrases like "same style as before" drift (§7A).
- Preserve identity explicitly, e.g. "do not change his face, facial features, body shape or identity";
  "do not redesign the character".
- For edits, separate the change from the constraints: "change only X; keep A, B, C". Make one change per turn,
  repeat what must be preserved, and compare before adding more instructions.
- Model tiers: **GPT Image 2.5 Sunburst** (base, highest quality) and **GPT Image 2.5 Flare** (small, faster,
  roughly GPT Image 2 quality). Quality settings run auto / low / medium / high / xhigh / max. Choose an explicit
  setting; do not assume the same label means the same result across models; use xhigh / max only when they
  solve an unmet requirement. Portrait size 1024×1536; outputs above 3,686,400 total pixels are experimental.
- Pre-use checks (vendor checklist): identity and reference details intact, only the requested elements
  changed, no unwanted text.
- Source: https://developers.openai.com/api/docs/guides/image-prompting

PROJECT LESSONS: none yet. No Big Bear generation has used GPT Image 2.5. Record the first one's result here.

### 21.3 Seedance 2.0 (via Higgsfield) — video model

VENDOR GUIDANCE (ByteDance launch material and the official host docs, compiled in the project's Seedance research
`terminal-logs/SEEDANCE_ARCHITECTURE_RESEARCH_2026-07-20.md`; do not re-research — update this section instead):
- **There are no camera parameters.** All camera direction lives in the prompt, in film grammar the model
  understands: dolly in / out, pan, tilt, tracking, crane, rack focus, push-in, orbit, handheld, static lock-off.
- Camera, motion stability and natural human motion are stated model strengths. Lean on descriptive camera
  language rather than over-constraining.
- Reference images supply the LOOK (identity, wardrobe, composition, lighting, colour). The prompt supplies the
  MOTION. In image-to-video the start image is frame zero (§7), so it must already contain the room for the planned
  motion.
- Multi-reference mode accepts up to 9 images, bound to shots with the host's in-prompt token (on fal:
  `@Image1`, `@Image2`…). Array order is not a documented control.
- Duration is 4–15 s in whole seconds (§9). Longer films are made by video extension, not by one long render.

PRACTITIONER CONSENSUS (secondary; treat as hypothesis, not vendor guidance):
- The first ~20–30 words carry the most weight: lead with the subjects and the core action.
- Structure the prompt as an ordered shot list; each beat = camera move → subject action → framing.
- **Hard per-second timestamps are reported to make timing unstable.** Prefer ordered beats. If timing must be
  pinned, say so in the Prompt Pack and inspect the result against the VO (§6, §9).
- 4–6 well-chosen references are reported to outperform using all 9.

PROJECT LESSONS:
- **Resolution: Constitution Rule 58 makes 480p the default paid video resolution.** A higher tier (e.g. 720p) needs
  explicit Chairman authorisation for that render, recorded before spend. Quality problems are fixed through the
  prompt, the still, framing or post-processing, never by inferring a higher tier.
- BB_MANUAL_001 v1 (Higgsfield `seedance_2_0` mode fast, 720p, 10 s, start image = still v1, VO supplied as audio
  input, generate_audio on): **the generated speech changed the supplied line** ("something that lasts" became
  "something they've lost"). After every generation, transcribe the spoken words and compare them with the locked
  script before accepting the take.
- The same render's prompt used hard timestamps (0–1.5 s / 1.5–8.5 s / 8.5–10 s), and the timing needed rescue in
  CapCut (1.2× speed). This is consistent with the timestamp caution above but does not prove it caused the problem.
- generate_audio / audio-input settings are a per-video Prompt Pack decision for Big Bear. Other lanes' audio
  locks do not apply here.
