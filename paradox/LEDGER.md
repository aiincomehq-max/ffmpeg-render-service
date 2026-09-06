# The Ledger

**What the Google Drive actually shows. Read on 6 September 2026.**

Every number below was read from a file in the Drive, and each one names the file it came from. Where a number can only come from the Mac (terminal recordings, invoices), it is marked as such rather than guessed. Snapshot view counts are what the analytics workflows recorded on the date shown; some posts appear in more than one snapshot, so the totals are "as logged", not de-duplicated.

## The headline, corrected

The story was not 60 days. It was longer and bigger.

| Measure | Value | Where it comes from |
|---|---|---|
| First AI content attempt | July 2025 (AIincomeHQ_Hybrid_Video_Starter folder) | Drive folder created 20 Jul 2025 |
| n8n experience at the start of this run | "8 months" | 30-day plan document, 19 Apr 2026 |
| The plan written on day zero | "From Builder to Business": interview 20 businesses, sell one £500 to £1,500 ops build by day 30. Explicitly: *"Content automation is a saturated, skeptical market... Keep FirstDropHQ running as your credibility engine. Sell ops builds privately."* | Two documents dated 19 Apr 2026 |
| What happened instead | First automated content account went live within 8 days of that plan (Silence in the Storm, 27 Apr). No client project appears anywhere in the Drive. | Folder timestamps |
| Days from that plan to today | 140 | 19 Apr to 6 Sep 2026 |
| Distinct project folders created since then | 30 named products (list below) | Root folder timestamps |
| Paid clients | 0 | No client artefact exists in the Drive |

## The projects, in order of birth

Silence in the Storm (18 to 27 Apr) · Lostbeyond.x (23 Apr) · AstroCosmos (27 Apr) · HumanUpgradeHQ carousels (28 Apr) · Brainsoup (15 May) · Kling driver videos and Dance Character (20 May) · Avatar_Pipeline (31 May) · DroneDreams (3 Jun) · **Project Control Relay (4 Jun)** · AI_Construction_Timelapse_Factory (6 Jun, five separate folders) · YTIF (6 Jun) · EAN Renders (11 Jun) · CTF Cabin (11 Jun) · FruitDrama (17 Jun) · FirstDropHQ canary and tool-topic tests (17 Jun) · FDHQ_Production (3 Jul) · Sneaker Watcher (6 Jul) · AIIncomeHQ Etsy scan (15 Jul) · OhChat Scarlett Vale (18 Jul) · BIG_BEAR (20 Jul) · HUP Content Factory (22 Jul) · CLOUD9 (2 Aug) · HUHQ Psychology Video Arm (6 Aug) · WARHOL_NOW (7 Aug) · ART_UNIVERSE (11 Aug) · AFF_DIRECT_EARNINGS (25 Aug) · AI_COMMERCE_DEMAND_MINE (28 Aug) · PostProtocol (5 Sep, yesterday).

That is a new product roughly every five days for 140 days.

## What the accounts actually did

| Account | Posts logged | Views as logged | Best single post | Followers (last recorded) | Source |
|---|---|---|---|---|---|
| Lostbeyond.x | 111 ranked (20 Apr to 9 Jun) plus 164 composites scheduled in July | 55,716 in the June ranking, 21,052 in the May snapshot | 1,300 | ~350 (3 Jun) | Lostbeyond.x sheet; PCR spec |
| AstroCosmos | 111 ranked (9 May to 18 Aug) plus 51 in the August snapshot | 68,633 in the August ranking, 8,581 for the last 51 posts | 1,856 | ~130 (3 Jun) | AstroCosmos sheet; PCR spec |
| Silence in the Storm | 3 accounts, 51 posts each in the August snapshots | 22,372 + 10,333 + 1,816 | 3,006 (a June post) | ~450 (3 Jun) | SilenceInTheStorm sheet; PCR spec |
| HumanUpgradeHQ | 45 in the August snapshot; 137 scripts written; 9 carousels | 16,330 | 1,258 | 757 recorded once in the accounts tab | HUP_Content_Factory sheet |
| FirstDropHQ | 50 carousels in June, 102 authored 24 Jul to 4 Sep, 125 on the grid | 141 profile views in the last 30 days; post views 0 to 3 | not recorded | 379 | FDHQ logs; Instagram profile |
| OhChat Scarlett Vale | 164 queued, 71 published, 50 scheduled, 36 held | not recorded | not recorded | not recorded | OhChat production log |

Everything together, as logged: roughly **600 published units** and about **210,000 views** across five months, with the best post of the whole estate at **3,006 views**, and a combined follower count in the region of **1,300**. The last 30 days on the flagship account produced 141 profile views.

## What the machine looked like

| Measure | Value | Source |
|---|---|---|
| Workflows in the n8n instance | 445 (paginated count, 8 Aug) | Warhol Now session handoff |
| Tabs in the FirstDropHQ production log | 107 | FDHQ_Production_Log |
| Tabs in the HumanUpgrade production log | 163 | HUP_Content_Factory |
| Workflows registered for HumanUpgrade alone | 38 (17 duplicated-inactive, 19 registered, 2 active) | HUP workflow register |
| Publish failures logged for FirstDropHQ | 205 events in one log tab, plus 8 failed and 8 partial in another | FDHQ_Production_Log |
| Configuration changes logged for FirstDropHQ | 109 change-log entries (18 Jul to 5 Sep) and 179 config-key updates | FDHQ_Production_Log |
| Competitor accounts catalogued for HumanUpgrade | 188 | HUP accounts tab |
| Competitor posts analysed for HumanUpgrade | 145, representing 265 million source views | HUP knowledge tab |
| Versions of one HumanUpgrade video | 18 (V16 rejected, V17 audited, V18 built) | HUHQ_PSY_V18_HANDOVER |
| Episodes of FruitDrama produced before naming an account | 14 | SESSION_END_2026-06-21 |
| Rejected topics vs used, FirstDropHQ June | 61 rejected, 50 used | Archived FDH Content Factory |

## What the management layer looked like

This is the part that matters for the account. The machine needed a machine to manage it, and then a human to manage that.

| Artefact | What it is | Source |
|---|---|---|
| Terminal recording of every Claude session | `script` wrapper started before every session; 191 recordings between 20 May and 25 Jun (36 days, about five sessions a day) | "Call Claude Code Session + Auto Save" doc; PCR recall note |
| Claude transcripts on disk | 170 JSONL files in the same period | PCR recall note |
| End-of-session ritual | A standard message demanding "LOSSLESS DURABLE STATE", read-back verification, "GOVERNED SHUTDOWN", and a resume message for the next session; a spreadsheet of 27 such handovers | "Claude End of Session Prompt Messages" sheet |
| Hash-verified checkpoints | Session checkpoints that re-hash 9 artefacts and a "CONSTITUTION RULE LIBRARY v1.1.7" before doing anything | C9_SESSION_2026-08-11_CHECKPOINT_A |
| Chairman approvals | 25 approval rows in one product's log, each item decided by "chairman"; "Claude = Builder. ChatGPT = independent auditor. [Owner] = final GO authority." | HUP approvals tab; HUHQ handover |
| Spend ceilings | $5.00 absolute ceiling per product; $2.00 per FirstDropHQ cycle; claim-before-spend gate written yesterday | Cost ledgers; fdhq_spend.py, 5 Sep |
| Project Control Relay | A four-layer control system (Claude workers, a relay, ChatGPT controller, human executive) to "remove me from the day-to-day management of multiple AI projects". Spec 3 Jun. Born 4 Jun. Declared "a complete failure" and deleted 25 Jun, with no git and no Time Machine. Post-mortem lists "M7 = deleting the history" as a mistake never to repeat. | PROJECT CONTROL MASTER SPECIFICATION V1; End of Session sheet |

## What the money looked like

The API money was tiny. The ledgers were kept to the cent.

| Item | Value | Source |
|---|---|---|
| Warhol Now, whole product life | $0.79 of a $5.00 ceiling | WARHOL_NOW_COST_LEDGER |
| HUHQ psychology video arm, spend ledger | $0.87 of $5.00 | WILSON_V260 spend ledger |
| HumanUpgrade cost ledger, 9 Aug to 4 Sep | about $16 estimated across 117 rows | HUP cost tab |
| FirstDropHQ gate and retry costs, 25 Jul to 4 Sep | $2.30 gate + $0.70 retry + $14.10 judge runs | FDHQ cost tabs |
| OhChat image and video generation | $23.40 across 303 jobs | OhChat cost tab |
| AstroCosmos, Silence, LostBeyond generation estimates | $0.64 + $1.45, $0.52, $0.54 | Project sheets |
| A January 2026 scrape run | $1.69 Apify + $0.26 OpenAI for 733 posts | "n8n Workflow Cost per Run" sheet |
| Subscriptions and total tokens | **Not in the Drive.** Claude, ChatGPT, Kling, ElevenLabs, Blotato, Hetzner invoices live in the billing consoles. | Fill from consoles |
| Hours | **Not in the Drive.** The 191 terminal recordings on the Mac carry start and end timestamps and can be summed. | Fill from `~/CodexProjects/claude-sessions/terminal-logs` |

## The sentences the Drive wrote itself

These are quotes from the logs, not paraphrases.

- *"The bottleneck is: not coding. Not model capability. Not token limits. The bottleneck is project coordination, context management, state management, decision tracking, review workflows, session orchestration."* (Project Control spec, 3 June)
- *"Claude Code sessions become workers. ChatGPT becomes controller. User becomes executive approval layer."* (same document)
- *"PCR v1 is DECOMMISSIONED and DELETED (2026-06-25, chairman: 'confirmed a complete failure').* DO NOT rebuild PCR."* (End of Session sheet)
- *"Visuals = solved. Continuity = solved. Rendering quality = solved. NONE is the bottleneck anymore. STORY QUALITY is the bottleneck."* (FruitDrama session end, 21 June)
- *"A gate that misses the case it was written for manufactures confidence."* (Warhol Now handoff, 8 August)
- *"Twenty-five well-formed frames can all be the same shot."* (HUHQ V18 handover, 14 August)
- *"Content automation is a saturated, skeptical market. Every agency on social sells it. Buyers have been burned."* (The 30-day plan, 19 April, day zero)

## The three numbers for the first Reel

**140 days. 30 products. 141 views.**

Or, if the Mac logs confirm the hours: **[hours] hours. 445 workflows. 141 views.**

## What this ledger cannot say

It cannot say how many hours were worked; only the terminal recordings can. It cannot say what the subscriptions and tokens cost; only the consoles can. It cannot de-duplicate views across snapshots, so the 210,000 is an upper bound as logged. It does not include anything that was deleted, and the Project Control Relay post-mortem says a great deal was.
