# PHASE 1 — FILM/TV DEMAND MINE v0.1 — BUILD AND PROOF REPORT

**Prepared by:** Claude Code (Builder / Engineer)
**For:** The Chairman
**Date:** 31 August 2026
**Recommendation:** **REWORK** (see §12)

---

## 0. HEADLINE

The machine was built, physically executed, and it **failed its own proof test — for a reason worth knowing.**

The intersection scorer did not surface a commercial opportunity you would not have found unaided. What it produced instead was an artefact: every one of its top-ranked settings rested on **exactly one** evidence record. When a confidence gate was applied, **37 of 43 settings fell out** and the entire top of the ranking collapsed.

One finding did survive, and it is not an artefact and not in your brief: **on the format axis, vertical microdrama outscores returnable series despite having the weakest buyer demand of any format measured** — because it is the only format in the corpus that answers the actual binding constraint, which is deficit financing rather than commissioning appetite.

So: the world × engine model needs roughly ten times the evidence before it means anything. The format/structural axis is already producing signal. That is a specific, cheap, testable correction — which is why the recommendation is REWORK rather than STOP.

---

## 1. ARCHITECTURE ACTUALLY BUILT

Physical n8n implementation. Real nodes, real wiring, real state transitions, real file custody, executed from the n8n CLI against a real database.

| | |
|---|---|
| n8n version | **2.35.7**, self-hosted, npm install at `/home/user/n8n-host` |
| Database | **SQLite** — Docker daemon is unavailable in this environment, so the PostgreSQL instance recommended in Phase 0 §6.1 could not be provisioned. **Defect DEF-05.** |
| Execution mode | `n8n execute --id=<workflow>` (CLI), single instance, no queue mode |
| Licence position | Sustainable Use Licence, internal business use — permitted |
| File custody | `N8N_RESTRICT_FILE_ACCESS_TO` scoped to the phase1 directory |
| Node types used | `manualTrigger`, `readWriteFile`, `extractFromFile`, `code` (v2), `merge` (v3), `convertToFile` |
| Hashing | Real SHA-256 via `crypto` (`NODE_FUNCTION_ALLOW_BUILTIN=crypto`) |

**No Python control plane.** Python was used only to author and patch workflow JSON at build time and to read results out of n8n's own SQLite database for this report. It executes nothing at runtime. The runtime is n8n.

### Pipeline

```
raw_signals.json
  → WF-10  ingest, dedupe on SHA-256, normalise          → 01_normalised.json
  → WF-11  structured assertion extraction                → 02_assertions.json
  → WF-12  clustering + saturation + cost pressure        → 03_clusters.json
  → WF-13  intersection generation + scoring (V2)         → 04_opportunities.json
  → WF-14  legal screen + governance bands                → 05_screened.json
  → WF-15  dedupe, confidence gate, rank, digest          → 06_digest.json
                                                            + CHAIRMAN_DIGEST.md
```

Each stage reads one status and writes the next. Every stage is separately executable and separately re-runnable.

---

## 2. WORKFLOW IDS

| Workflow ID | Name | Executions |
|---|---|---|
| `SWFwf10Ingest0001` | WF-10 Signal Ingest and Normalise | 3 |
| `SWFwf11Assert0001` | WF-11 Structured Assertion Extraction | 1 |
| `SWFwf12Cluster001` | WF-12 Clustering and Saturation Analysis | 1 |
| `SWFwf13Score00001` | WF-13 Intersection Scoring and Opportunity Build | 2 |
| `SWFwf14Legal00001` | WF-14 Legal Screen and Governance Gate | 1 |
| `SWFwf15Digest0001` | WF-15 Rank and Chairman Digest | 2 |

**10 executions, 10 successes, 0 failures.** Full record with timestamps: `phase1/executions/execution_evidence.json`.

Multiple executions on WF-10, WF-13 and WF-15 are the repair cycles in §11 — first run, defect found, patched, re-run.

---

## 3. SOURCE INVENTORY

**A hard environmental constraint governs this entire phase.** The organisation's egress policy blocks outbound HTTPS to every journalism, government and data host. Verified at the proxy: `broadcastnow.co.uk`, `deadline.com`, `ofcom.org.uk`, `bfi.org.uk`, `feeds.bbci.co.uk`, `wikipedia.org`, `wikidata.org`, `themoviedb.org`, `caselaw.nationalarchives.gov.uk`, `company-information.service.gov.uk` — all `403` at CONNECT.

Reachable: `googleapis.com` (400/403 from Google itself, i.e. allowlisted), `api.github.com` (200), `api.anthropic.com` (401), package registries.

**Consequence: n8n cannot acquire a single demand signal in this environment.** The HTTP Request and RSS nodes have nowhere to go. Acquisition was performed by me through the WebSearch tool, which routes via Anthropic rather than the egress proxy, and staged as `evidence/raw_signals.json`.

This is reported, not routed around. The proxy documentation states policy denials must be reported rather than circumvented.

Sources represented in the corpus (37 distinct publishers/bodies), by class:

| Class | Examples |
|---|---|
| Buyer primary | Paramount/Channel 5 Mediahub, Sky Group, ITV Press Centre, Netflix Help Centre, Channel 4 Careers, BBC |
| Regulator / public body | Ofcom Media Nations 2026, BFI statistics, Screen Ireland, Northern Ireland Screen |
| Analyst | Ampere Analysis (via Variety, Cineuropa, C21, Broadband TV News), Deloitte TMT Predictions |
| Trade press | Deadline, Screen Daily, Broadcast, Televisual, Variety, Hollywood Reporter, Prolific North |
| Academic | Sage/AHRC "What's On?" class inequality research, White Rose |
| Reference | Wikipedia (title/date metadata) |

---

## 4. RAW SIGNAL COUNT

**102 signals** ingested, 0 duplicates dropped, all SHA-256 fingerprinted. Within the 100–250 target.

Distribution by signal type:

| Type | n | | Type | n |
|---|---|---|---|---|
| commissioning | 21 | | economics | 15 |
| renewal | 8 | | audience_data | 8 |
| genre_demand | 6 | | saturation | 6 |
| format_trend | 6 | | route | 8 |
| open_call | 3 | | industry_structure | 3 |
| production_activity | 4 | | funding | 3 |
| acquisition | 1 | | industry_event | 1 |
| other | 9 | | | |

---

## 5. ASSERTIONS

**236 structured assertions** extracted from 102 signals by WF-11.

```
supply            70     buyer_demand      36     genre_supply      57
economics         18     route             11     genre_demand       9
audience_demand    8     format_trend       8     saturation         6
structure          5     legal_flag         4     ip_provenance      4
```

Each assertion carries its originating `evidence_id`, `source_url` and an evidence weight (E1 = 1.0 official/primary, E2 = 0.7 trade press, E3 = 0.4 single secondary).

---

## 6. CLUSTERS

WF-12 produced eleven cluster maps. The load-bearing ones:

**Formats by demand:** limited_series 12.3 · returnable_series 9.1 · vertical_microdrama 5.2 · mixed 2.8

**Worlds by supply (top 8):** police 4.2 · criminal_justice 4.1 · intelligence_services 2.2 · hospitality 2.0 · aviation 1.4 · parliament 1.4 · suburban_family 1.1 · organised_crime 1.1

**Genres by demand:** crime 10.08 · thriller 9.08 · cosy_crime 4.10 · period_crime 2.80 · true_crime_drama 2.40 · procedural 2.10

**Routes (weighted, evidence-derived):** open_free **+2.7** · market +1.0 · open_competition +0.7 · open_paid +0.2 · closed **−1.7**

**Cost pressure index: 0.434** — derived from the proportion of economics evidence pointing negative. This is what makes cheap formats score.

---

## 7. TOP OPPORTUNITY THESES

### 7.1 What the machine ranked, ungated

| Rank | Intersection | Score | World evidence |
|---|---|---|---|
| 1 | food_hospitality × murder [limited series] | 77.19 | **1** |
| 2 | small_town × murder | 72.52 | **1** |
| 3 | small_town_america × murder | 72.52 | **1** |
| 4 | law × murder | 72.52 | **1** |
| 5 | medicine × betrayal | 69.56 | **1** |

Every one rests on a single evidence record, and the top four contain three near-identical ties. **This is the failure mode you named**: after processing 102 records it proposes murder in a restaurant, murder in a small town, murder in a law firm. That is "crime is popular" with extra steps.

### 7.2 What survived the confidence gate

Applying a minimum of two distinct evidence records per setting (DEF-03, §11), **only 6 of 43 settings qualify** — so there is no top ten, there is a top six:

| Rank | World × Engine | Format | Score | Evidence | Band |
|---|---|---|---|---|---|
| 1 | organised_crime × organised_crime | limited series | 63.47 | 2 | chairman_review |
| 2 | suburban_family × betrayal | limited series | 60.65 | 2 | chairman_review |
| 3 | intelligence_services × conspiracy | limited series | 59.15 | 4 | archive |
| 4 | aviation × conspiracy | limited series | 56.87 | 2 | archive |
| 5 | parliament × ambition | limited series | 55.71 | 2 | archive |
| 6 | hospitality × reinvention | limited series | 51.96 | 2 | archive |

**Not one reaches the 75 eligibility threshold.** Four of six fall in the archive band. Honest reading: *on the evidence actually gathered, the system has no world-level opportunity worth developing.*

### 7.3 The finding that did survive — format, not setting

| Format | Mean score | Buyer demand | Route access | Feasibility |
|---|---|---|---|---|
| limited series | 60.74 | **79%** | 70% | 73% |
| **vertical microdrama** | **56.51** | **44%** | 59% | **100%** |
| returnable series | 55.19 | 63% | 70% | 55% |

Vertical microdrama has the **weakest buyer demand of any format measured** — and still beats returnable series. It does so on production feasibility alone.

That is not a scoring quirk. It is the model correctly registering something the corpus says loudly:

- The UK constraint is **not** commissioning appetite. Ampere: Western European scripted commissions are only 2% below 2020, but take **40% longer to make** (EV070). Producers describe a UK greenlight as "effectively meaningless" because broadcasters fund about **one third** of budget (EV049). Co-production spend fell from £44.2m to £19.6m in a year (EV046). BFI H1 2026: inward TV investment down **23.5%** (EV043).
- Microdrama is the one format in the corpus that sidesteps all of it. Deloitte: in-app micro-series revenue **US$3.8bn in 2025 more than doubling to US$7.8bn in 2026** (EV090), and explicitly identifies **independent studios** as the beneficiaries (EV091). ReelShort ~$400m revenue (EV093); DramaBox 44m MAU (EV092). Peacock has licensed ten micro-dramas and Bravo is making originals (EV095). The UK market is only now forming: **KIN launched as the first UK vertical drama indie** (EV096) and the **RTS is convening on it** (EV097).
- It is the only format whose route to market does not run through a gatekeeper who is closed to us (Netflix agent-only, EV123) or through the aggregation layer that no longer exists (Coverfly shut 1 Aug 2025, EV124).

**This is outside your brief.** The mission named drama series, limited series, pilots, features, treatments, series bibles, pitch packages and screenplays. Vertical/short-form appears nowhere in it, nor in Phase 0.

---

## 8. SCORING EXPLANATION

`SCORING_MODEL_V2`, weights from Phase 0 §4.1, all dimensions computed from corpus counts — none hand-assigned per candidate.

| Dimension | Weight | Derivation |
|---|---|---|
| buyer_demand | 18 | 0.6 × format demand index + 0.4 × genre demand index |
| route_accessibility | 18 | Buyer-archetype openness derived from route assertions × format-archetype affinity |
| production_feasibility | 15 | Format base × (1 + cost_pressure × 0.5) |
| under_service | 12 | Rank-percentile of (world demand context ÷ (1 + world supply)) |
| audience_demand | 10 | Genre audience index |
| saturation_inverse | 10 | 1 − blend(world supply rank, genre supply index) |
| buyer_fit | 7 | Max buyer×genre affinity |
| international_potential | 5 | Territory breadth for the genre, capped at 3 |
| evidence_breadth | 5 | Rank-percentile of distinct evidence records per world |

**Archetype route openness, derived not assumed:** public_service **1.00** (the only archetype with evidenced open-access schemes — BBC Writers Open Call, C4 New Writers, 4Screenwriting) · niche_channel 0.45 · streamer **0.37** (dragged down by Netflix's explicit closed-door policy) · commercial_fta 0.35 · direct_app 0.59 (derived from the "independent studios empowered" language in format-trend evidence).

Changes from V1, both forced by observed defects: max-normalisation replaced with rank-percentile (V1 collapsed 47 of 53 worlds into a 0.7–0.9 band), and `originality_space` replaced with `under_service`.

---

## 9. EVIDENCE LINEAGE

Every scored candidate carries `evidence_support` — the evidence IDs that produced its score — traceable back through each stage to a source URL and retrieval date.

```
opportunity → evidence_support[] → assertion.evidence_id → evidence_id → source_url + SHA-256
```

Worked example, ranked #1 pre-gate: `food_hospitality__murder__limited_series` cites EV035 (A Taste for Murder, ITVX/BritBox, 7 Apr 2026), EV025 (The Good Ship Murder S4, Clapperboard/FIFTH SEASON), EV002/EV003 (ITV crime slate) and eleven more. The lineage is intact and checkable — which is precisely how the single-evidence defect was caught.

---

## 10. SPEND

| Item | Cost |
|---|---|
| LLM API calls | **£0.00** — no API key present; all analysis is deterministic JavaScript inside n8n Code nodes |
| n8n licence | £0.00 — Sustainable Use Licence, internal business use |
| Hosting | £0.00 — session container |
| Data/API subscriptions | £0.00 — none purchased; TMDB commercial licence correctly avoided |
| External accounts created | **none** |
| **Total** | **£0.00** |

---

## 11. DEFECTS AND LIMITATIONS

| ID | Defect | Status |
|---|---|---|
| **DEF-01** | Max-normalisation collapsed 47/53 worlds into a narrow band; only 9 distinct values across 360 candidates. | **Fixed** — rank-percentile normalisation (V2). Distinct scores rose 76→81, range widened 48.6–72.2 → 40.5–77.2. |
| **DEF-02** | **Candidate worlds are generated only from supply assertions, so every setting scored is already in commission. The system structurally cannot propose territory nobody is making.** | **Open — the most important defect in the build.** |
| **DEF-03** | `under_service` and `evidence_breadth` are anti-correlated by construction: a world seen once looks under-supplied when it is merely under-observed. Drove the entire pre-gate top ten. | **Mitigated** — confidence gate (≥2 records). Not cured; the cure is more evidence. |
| **DEF-04** | Corpus far too thin for world-level inference: 37 of 43 settings have exactly one evidence record. | **Open** — needs ~10× signal volume. |
| **DEF-05** | SQLite, not PostgreSQL as Phase 0 recommended — Docker daemon unavailable. Queue mode impossible. | **Open — environmental.** |
| **DEF-06** | n8n cannot acquire signals: all source hosts blocked by egress policy. Acquisition performed out-of-band. | **Open — environmental. Blocks automation of the whole ingest leg.** |
| **DEF-07** | No Sheets/Drive custody: no Google OAuth credentials available to n8n. State is local JSON. | **Open** |
| **DEF-08** | Production feasibility is driven almost entirely by format; world-level containment is not modelled. | **Open** |
| **DEF-09** | Two unresolved source conflicts logged in-corpus (*The Blame* cast/origin; *The Lady* buyer BBC vs ITV). | **Logged, not resolved** |
| **DEF-10** | All evidence is search-summary derived; no primary document was fetched. | **Open — same constraint as Phase 0.** |

**Legal screen performed as designed:** 63 of 360 candidates hard-blocked (real-case worlds, identifiable-individual flags, direct real-events engines). No score overrode a block.

---

## 12. RECOMMENDATION — **REWORK**

Not EXPAND: the proof question was answered "no" on the axis the pilot was built to test, and expanding a model with DEF-02 unfixed would scale an artefact.

Not STOP: the machine built cleanly, ran ten times without failure, caught its own defects through its own lineage, and produced one genuine finding on a different axis. That is a working instrument aimed at the wrong target.

**The four corrections, in order:**

1. **Fix DEF-02 — separate demand-worlds from supply-worlds.** Candidate settings must be generated from *demand-side* evidence (economics, audience, structural, policy) and cross-checked against supply, not extracted from lists of shows already made. Until this changes the system can only ever recommend what already exists. This is the single highest-value fix and it is a change to WF-13's candidate generator, not a rebuild.

2. **Raise signal volume ~10×** to roughly 1,000–1,500, targeting *settings and economics* rather than title announcements. The evidence gate then becomes meaningful instead of eliminating 86% of the field.

3. **Promote format and structure to first-class axes.** They are where the pilot actually produced signal. The next run should score format × route × financing-model explicitly, not treat format as an attribute of a setting.

4. **Resolve the environment.** Acquisition automation, Sheets/Drive custody and PostgreSQL are all blocked here (DEF-05/06/07). None is a design problem; all three need an environment with egress and Google credentials — which is a Mac-session or hosted-runner question, not an engineering one.

**On the proof question, stated plainly:**

> Did the system surface at least one credible commercial opportunity the Chairman/Orchestrator would not reasonably have identified unaided?

**On world × engine intersections: no.** It restated the obvious, and did so on a confound.

**On format: yes, once — vertical microdrama.** Weakest buyer demand of any format, still outranking returnable series, because it is the only format in the corpus that answers the financing constraint the same corpus proves is the real bottleneck. It is not in your brief. Whether it is *interesting* to you is a commercial judgement, not an engineering one — but the machine reached it from evidence, not from me, and I did not put it in the candidate set by hand.

**What I would not do yet:** write any drama. Nothing in this run identifies a premise worth developing, and the six settings that survived the evidence gate all sit in the archive or review bands. The correct next move is a corrected mine, not a script.

---

## 13. CONSTRAINTS OBSERVED

No production scripts. No screenplay generation. No music generation. No marketplace submissions. No publication. No schedules activated — every execution was manually invoked from the CLI. No external commercial accounts. No paid spend. No other project's files, infrastructure or credentials touched; the host repository's `app.py`, `Dockerfile` and `requirements.txt` remain unmodified.

---

## APPENDIX — ARTEFACTS

```
scriptwriter-factory/phase1/
  evidence/raw_signals.json          102 signals, 37 sources
  workflows/WF-10..WF-15 (6 files)   importable n8n workflow JSON
  state/01_normalised.json           102 records, SHA-256 fingerprinted
  state/02_assertions.json           236 assertions
  state/03_clusters.json             11 cluster maps + cost pressure index
  state/04_opportunities.json        360 scored candidates
  state/05_screened.json             legal screen + governance bands
  state/06_digest.json               ranked output + format findings
  output/CHAIRMAN_DIGEST.md          generated digest
  executions/execution_evidence.json 10 executions, all success
```

Re-run from a clean checkout:

```bash
source /home/user/n8n-host/env.sh
cd /home/user/n8n-host
for w in WF-10_ingest_normalise WF-11_extract_assertions WF-12_cluster_saturation \
         WF-13_score_opportunities WF-14_legal_screen WF-15_rank_digest; do
  ./node_modules/.bin/n8n import:workflow --input=.../phase1/workflows/$w.json
done
for id in SWFwf10Ingest0001 SWFwf11Assert0001 SWFwf12Cluster001 \
          SWFwf13Score00001 SWFwf14Legal00001 SWFwf15Digest0001; do
  ./node_modules/.bin/n8n execute --id=$id
done
```

*End of Phase 1 report.*
