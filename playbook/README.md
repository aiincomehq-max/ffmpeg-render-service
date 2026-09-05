# First Drop HQ — First Viral Month kit

Everything in this folder is the output of running the five "I gave my Instagram page to Claude" prompts against First Drop HQ's real niche and pipeline.

| File | What it is | Where it goes |
|---|---|---|
| `FIRST_VIRAL_MONTH.md` | The playbook: algorithm scoreboard, five validated angles, script architecture, hook bank, automation mapping, 30-day plan, sources | Read once, keep for reference |
| `prompts/01_niche_scan.md` | Daily topic scoring and slot assignment | New LLM node after the news scrape |
| `prompts/02_script_generator.md` | Two-cut script generator; emits overlays in this render service's `RenderRequest` shape | Replaces the existing script node prompt |
| `prompts/03_hook_engine.md` | Hook A/B variants | New LLM node after the script node |
| `prompts/04_caption_hashtags.md` | Per-platform captions, titles, hashtags | New LLM node before Blotato |
| `prompts/05_weekly_feedback.md` | Sunday analytics pass that reweights next week | New weekly workflow |
| `calendar_30_day.csv` | 150 rows: date, slot, time, angle, series title, hook formula, trigger, source, KPI | Import to Google Sheets or an n8n Data Table; Prompt 01 reads today's rows |
| `topic_bank_seed.csv` | 54 evergreen topics tagged by angle | Import as the `topic_bank` table; the weekly Reddit pull tops it up |

Build order, one node at a time: import the two CSVs, add Prompt 01, swap Prompt 02 in, add Prompt 03, add Prompt 04, run one full day manually, then schedule. Prompt 05 can wait until the first Sunday.
