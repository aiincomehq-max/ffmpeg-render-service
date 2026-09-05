# First Drop HQ — The First Viral Month

**Playbook for 7 September to 6 October 2026.** Five videos a day, 150 posts, four platforms, one avatar, zero manual steps.

This document runs the five prompts from the "I gave my Instagram page to Claude" carousel against your actual niche (AI tools for AI-curious beginners and intermediates, no developers) and your actual pipeline (n8n 2.11.4 on Hetzner → Kling 2.5 avatar → two-pass ASS captions → Blotato). Every section ends with the thing you paste into a node. The prompts themselves live in `playbook/prompts/` and the day-by-day schedule in `playbook/calendar_30_day.csv`.

---

## 0. What the algorithms are actually rewarding right now

Before any content decision, here is the scoreboard the four platforms are keeping in September 2026, pulled from current creator research. The whole plan is reverse-engineered from these numbers.

| Platform | Primary ranking signal | Threshold that unlocks distribution | Length sweet spot |
|---|---|---|---|
| TikTok | Completion rate and rewatch/loop rate (loop rate now outranks follower count; "micro-loop tracking" added July 2026 rewards rewatched segments) | 70%+ completion to go viral, up from 50% in 2024 | 11 to 18 seconds for maximum loops; 15 to 60 for value-dense pieces |
| Instagram Reels | Total seconds watched including replays, then shares and DM sends, then saves. Likes barely matter for non-follower reach | Keep 60%+ of viewers past second 3. Reels that lose half the audience in 3 seconds "rarely recover" | A 15-second Reel watched 3 times outranks a 60-second Reel watched once |
| YouTube Shorts | "Viewed vs swiped away" ratio and average percentage viewed. Separate recommender from long-form | 70%+ viewed rate moves you to the next velocity gate. Swipe-away in the first 3 seconds must stay under 25% on Shorts under 30s | 30 to 45 seconds performs best; length only matters through completion |
| Facebook Reels | Same Meta engine as Instagram: watch time and shares | Same as Instagram | Same as Instagram |

Three consequences for First Drop HQ. First, one 20-second master edit is wrong for everything: TikTok and Instagram want 12 to 18 seconds with a loop, YouTube wants 30 to 40 seconds with more substance. The plan produces two cuts of every script, a short loop cut and a long value cut, and Blotato routes each to the right platforms. Second, the first two seconds are the entire game, so the hook line is spoken and shown on screen simultaneously, no intro, no logo, no "hey guys". Third, generic hooks ("wait for it", "you won't believe") are now read by viewers as a low-quality signal, so every hook in this playbook is specific: it names a tool, a number, or a mistake.

---

## 1. Niche and content validation (carousel prompt 1)

**Prompt executed:** search Reels, TikTok and Reddit for the top-performing AI-tools content of the last 30 days, find the recurring hooks and topics, cross-reference, return the five highest-demand angles optimised for AI-generated visuals.

### What is recurring across all three platforms

On Reddit, r/ChatGPT (4M+ members), r/ArtificialIntelligence (700K+) and r/Chatbots the recurring high-upvote posts are practical and un-sponsored: "what I actually use daily", the three-tool free stack (Claude for writing, ChatGPT for general tasks, Perplexity for research), and "I was using this wrong for a year" confessions. Reddit distrusts hype and rewards specificity, which is exactly the tone that also survives on Instagram in 2026.

On TikTok and Reels the formats that keep resurfacing in AI-tools content are the single-tool reveal ("this AI tool does X"), the correction ("stop using ChatGPT like this"), the free-versus-paid comparison, the 60-second micro-tutorial with a visible before/after, and the news translation ("AI just did what?"). The retention research is consistent: content that opens with immediate value beats content that opens with an intro by 30 to 40% in retention, and recurring characters (a consistent avatar) measurably lift repeat views and brand recall, which is your structural advantage with Kling.

The news feed this week is unusually good for a beginner channel: Grok Bot (a persistent tool-using agent) landed on iPad and Android at a consumer price, Claude gained background computer use, Google and Meta shipped rival "workhorse" models, OpenAI built automated shutdowns, Anthropic shipped Fable and Mythos 5.1 and opened a Model Hardware Standard for agents controlling physical devices. Every one of those is a "what does this mean for a normal person" video.

### The five highest-demand angles for First Drop HQ

**Angle 1 — The Daily Drop.** One tool or feature that launched or changed in the last 24 hours, explained in plain English in 15 seconds, ending with one thing the viewer can do with it today. This is the brand (the name is literally First Drop) and it is the angle your scraper already feeds. Primary trigger: novelty and FOMO. Platform fit: TikTok and Instagram loop cut. Visual: avatar plus one bold on-screen tool name, product screenshot cut-in if available.

**Angle 2 — You're Using It Wrong.** A common beginner mistake with ChatGPT, Claude, Gemini, Perplexity or Canva AI, shown as wrong-then-right. Highest comment and share rate of any AI format because it triggers ego ("I do that") and the viewer sends it to the friend who does it. Trigger: ego and surprise. Platform fit: all four, this is your Instagram share engine. Visual: split "before / after" text overlay.

**Angle 3 — The Free Stack.** "The free AI stack that replaces a £40-a-month subscription", tool comparisons, free tier limits, "which one for which job". Reddit's single favourite genre and the most saved format on Instagram. Trigger: desire and money. Platform fit: YouTube Shorts long cut (30 to 40s) and Instagram saves. Visual: stacked tool logos appearing one by one.

**Angle 4 — Do This in 60 Seconds.** One prompt or one two-step workflow with a visible result: turn a voice note into an email, make a meal plan from a fridge photo, summarise a 40-page PDF. Micro-tutorials are the rewatch engine; people replay to copy the prompt, and TikTok's micro-loop tracking rewards exactly that. Trigger: desire and "I can do that". Platform fit: TikTok and YouTube. Visual: the exact prompt on screen as an overlay for the whole payoff section.

**Angle 5 — AI Just Did What.** Agent and model news translated into consequences for a normal person: "Claude can now use your computer while you sleep, here's what that means for your job", "an AI now has a standard for controlling physical devices". Fear, awe and controversy generate comments, and comments plus shares are what Instagram and TikTok both weight this year. Trigger: fear and surprise. Platform fit: all four; strongest on TikTok and Facebook. Visual: avatar, dark background, single big stat overlay.

Angles 1 and 5 are fed by the news scraper. Angles 2, 3 and 4 are evergreen and fed by a topic bank, which means they never fail on a slow news day. That mix is the point: the news angles win reach, the evergreen angles win saves and followers.

---

## 2. Script architecture (carousel prompt 2)

**Prompt executed:** write a high-retention short-form script with a pattern interrupt in the first 2 seconds, emotional tension or curiosity immediately, a quick payoff, under 20 to 30 seconds, optimised for watch time, replay and shares, soft CTA at the end.

### The First Drop five-beat structure

Spoken English for an avatar runs at roughly 2.5 words per second. That gives a hard word budget: a 15-second loop cut is 36 to 40 words, a 20-second cut is about 50 words, a 35-second YouTube cut is about 85 words. Every script your pipeline generates should come with both a short and a long version from the same idea, and the generator prompt in `prompts/02_script_generator.md` enforces these budgets.

| Beat | Time (short / long) | Job | Rule |
|---|---|---|---|
| 1. Hook | 0 to 2s | Pattern interrupt. The spoken line is also the on-screen text | Name a tool, a number or a mistake. No greeting, no "in this video". |
| 2. Stake | 2 to 5s | Why it matters to *you* in one sentence | Use "you" or "your" in the sentence. |
| 3. Payoff | 5 to 12s / 5 to 28s | The actual thing: the tool, the fix, the prompt, the news translated | One concrete example, never two. Long cut adds a second example or a step-by-step. |
| 4. Loop line | last 2 to 3s | A line that lands back on the hook so the replay feels intentional | Reuse a word from the hook. TikTok and Instagram both count replays as watch time. |
| 5. Soft CTA | final 1 to 2s or caption only | Follow, save, or "send this to the person who…" | Never "like and subscribe". On Instagram, ask for a send or save; on YouTube, ask for a follow. |

The pattern interrupt has to be specific because vague ones are now penalised by viewers. Four interrupt shapes that work for this niche are the confident contradiction ("ChatGPT isn't your best free AI anymore"), the impossible-sounding number ("this replaces £40 a month of subscriptions for free"), the confession ("I used AI wrong for a year"), and the fresh-news jolt ("Claude started using computers on its own this week").

### Example script, Angle 1, short cut (15s, 38 words)

> **Hook (0–2s):** Grok Bot just landed on Android, and it runs errands for you.
> **Stake (2–5s):** That means the AI on your phone can now finish tasks, not just answer questions.
> **Payoff (5–12s):** Ask it to compare three flights and book the cheapest, and it does the clicking.
> **Loop (12–15s):** So which errand would you hand it first?

### Example script, Angle 2, long cut (35s, 84 words)

> **Hook:** You're using ChatGPT like a search engine, and that's why it gives you rubbish.
> **Stake:** One change and your answers get twice as useful.
> **Payoff:** Stop typing questions. Give it a role, a goal and a format. Instead of "what should I eat", say "you're a dietitian, plan me three high-protein dinners under ten minutes, as a table". Same tool, completely different result, because you told it who to be and what done looks like.
> **Loop:** Try it once and you'll never search it again.
> **CTA:** Send this to the friend who still types questions.

### What the generator has to output

Your render service takes a list of overlays with `text`, `start_s` and `end_s`. The script generator prompt therefore returns JSON, not prose: the two cuts, each with `spoken_text`, a `beats` array with timings, and an `overlays` array in exactly the shape the render endpoint expects, plus the caption and hashtags. That removes a parsing node and means the hook text is on screen the moment the avatar says it.

---

## 3. Hook and retention engineering (carousel prompt 3)

**Prompt executed:** analyse the top viral Reels in the niche, identify hook patterns, pacing and emotional triggers in the first 3 seconds, then create 5 new provocative, curiosity-driven, scroll-stopping variations focused on surprise, ego, fear or desire.

### What the top AI-tools hooks have in common

Across the research, the hooks that hold 80 to 90% of viewers through second 3 share four traits. They are addressed to one specific person, not "everyone". They contain a proper noun or a number, because specificity signals the creator knows something. They imply a gap between what the viewer believes and what is true. And they are said and shown at the same time, so a muted scroller still stops. Pacing in the winners is brisk: the first cut or on-screen text change happens inside the first second, and the payoff begins by second 5 at the latest.

### Six hook formulas, mapped to triggers

1. **The contradiction (ego):** "[Popular belief] is wrong, and it's costing you [outcome]." *"ChatGPT Plus isn't worth it anymore, and here's the free stack that beats it."*
2. **The impossible number (surprise):** "[Tool] just did [task] in [absurd time]." *"This free AI wrote my whole CV in 40 seconds."*
3. **The quiet threat (fear):** "[Thing you rely on] just changed and nobody told you." *"AI can now click around your computer by itself. Here's what that means for your job."*
4. **The confession (ego, relatable):** "I [did the wrong thing] for [long time]. Don't." *"I paid for three AI apps for a year. One free one does all of it."*
5. **The dare (desire):** "Do this one thing in [tool] today and [payoff]." *"Type these five words into Claude and it plans your whole week."*
6. **The fresh drop (novelty):** "[Tool] launched [feature] today." *"Grok Bot just landed on Android and it runs errands."*

### Twenty-five ready hooks, five per angle

**Angle 1 — Daily Drop:** "Claude started using computers on its own this week." · "Grok just became an app that does your errands." · "Google and Meta both dropped new models today, here's the one you should actually try." · "OpenAI gave its AI an off switch. Here's why that matters to you." · "A new AI standard means your robot vacuum could get a brain."

**Angle 2 — You're Using It Wrong:** "You're using ChatGPT like Google and that's why it's useless." · "Stop asking AI questions. Give it a job instead." · "The one word that ruins 90% of AI prompts." · "If your AI answers are generic, you're doing this." · "I watched my mum use ChatGPT and now I understand everything."

**Angle 3 — Free Stack:** "The free AI stack that replaces £40 a month." · "Claude vs ChatGPT vs Perplexity: which one for which job, in 20 seconds." · "You don't need ChatGPT Plus. You need these three free tabs." · "Perplexity is the AI you should be using for anything you'd Google." · "This is the only AI tool I'd pay for in 2026."

**Angle 4 — Do This in 60 Seconds:** "Type these five words into Claude and it plans your whole week." · "Take a photo of your fridge and let AI cook dinner." · "Turn a 40-page PDF into a one-line answer. Watch." · "Voice note in, polished email out, no typing." · "Make your CV in one prompt, honestly."

**Angle 5 — AI Just Did What:** "AI can now click around your computer while you sleep." · "An AI just got a standard for controlling physical machines. Read that again." · "A third of companies stopped buying software because AI built it for them." · "Your next customer service call will be an AI talking to an AI." · "The AI you use for free is now smarter than the one you paid for last year."

### The retention rules the caption pass should enforce

Because your ASS caption pass already runs twice, give the second pass three visual retention jobs: the hook overlay stays on screen for the full first 2 seconds in the largest font size, a new on-screen element (word emphasis, cut-in, colour change) appears at least every 3 seconds, and the loop line's overlay is styled identically to the hook so the replay reads as a seamless loop. In the daily A/B, each idea is rendered with two hooks (`hook_a`, `hook_b`) and the one that clears 60% 3-second retention on TikTok by hour 6 is the one that gets pushed to the other platforms.

---

## 4. Full automation via AI (carousel prompt 4, mapped to your n8n)

**Prompt executed:** create a fully automated content system that finds trending topics daily, generates high-retention scripts, creates consistent AI visuals, converts them to short-form video, generates captions and hashtags, structured as a repeatable workflow for multiple posts a day.

You already have most of this. What follows is the mapping of the five angles and the hook engine onto your existing nodes, with the new nodes named.

**Stage 1 — Sources.** Keep the daily news scrape for Angles 1 and 5. Add two sources so evergreen angles never starve: a Google Sheet (or n8n Data Table) called `topic_bank` with 60+ seed topics tagged by angle (2, 3, 4), and a weekly Reddit pull of the top posts from r/ChatGPT, r/ArtificialIntelligence and r/ClaudeAI sorted by top-of-week, which refills the bank with what people are actually confused about. The calendar CSV tells each day which angles need a news item and which need a bank item.

**Stage 2 — Scoring and angle assignment.** New node, one LLM call, prompt in `prompts/01_niche_scan.md`. It takes the day's scraped items plus five bank topics and returns exactly five slots for today, each with an angle, a topic, a one-line "why a beginner cares", a trigger (surprise/ego/fear/desire) and a source URL. It also rejects anything developer-only (SDKs, APIs, benchmarks) unless it can be reframed as a consumer consequence. This is the node that protects the audience promise.

**Stage 3 — Script generation.** Existing node, replace the prompt with `prompts/02_script_generator.md`. Input is one slot from Stage 2. Output is JSON with `short_cut` and `long_cut`, each holding spoken text, beats with timings, and an `overlays` array already in the render service's shape. Run it once per slot with a Split Out node, so a failure on one slot never kills the day.

**Stage 4 — Hook variants.** New node, prompt in `prompts/03_hook_engine.md`. Takes the script and returns `hook_a` and `hook_b` (two different formulas, two different triggers). Cheap call, big lift; this is the single highest-leverage addition to the pipeline.

**Stage 5 — Avatar video.** Kling 2.5 as now. Use the short cut's spoken text for the TikTok/Instagram render and the long cut for YouTube. Keep the same avatar, framing and outfit across every video for the whole month; recurring-character consistency is one of the few free retention levers left.

**Stage 6 — Captions and overlays.** Two-pass ASS as now, plus pass the `overlays` array from Stage 3 to the render service so the hook, the prompt text and the loop line are burned in at the right seconds.

**Stage 7 — Captions, hashtags and per-platform routing.** New prompt in `prompts/04_caption_hashtags.md`. One call returns four caption variants: TikTok (short, question-led, 3 to 5 tags), Instagram (save-or-send CTA, 5 to 8 tags, first line is the hook), YouTube (title under 60 chars with the tool name, description with the prompt written out), Facebook (one-sentence plain-English summary, no hashtags). Blotato posts the short cut to TikTok, Instagram and Facebook and the long cut to YouTube.

**Stage 8 — Weekly feedback loop.** New Sunday workflow, prompt in `prompts/05_weekly_feedback.md`. Pull the week's stats (views, completion, shares, saves per post) from Blotato or the platform APIs into a sheet, and have one LLM call return the top five performers with their angle and hook formula, the bottom five with a diagnosed reason, and an updated weighting for next week's calendar. Paste the top five hooks into the script generator as few-shot examples. This closes the loop: by week 3 the pipeline is writing in the voice that your specific audience already proved it likes.

### Posting cadence

Five slots a day, spread across the waking day of a UK and US audience. The calendar uses 07:30, 11:30, 15:00, 18:30 and 21:30 UK time. Slot 1 is always the Daily Drop, because the earliest post of the day sets the account's "first" promise. Slot 5 is always the strongest emotional hook of the day (Angle 5 or Angle 2), because evening scrolling is the highest-share window. Slots 2 to 4 rotate through the calendar.

---

## 5. The 30-day plan

The full 150-row schedule is in `calendar_30_day.csv` with date, slot, post time, angle, hook formula, trigger, topic source and the KPI to watch. This is the shape of the month.

**Week 1 (7 to 13 September) — Establish and measure.** All five angles get equal weight, 7 posts each across the week, each rendered with two hooks. The goal is not virality yet; it is 35 data points per angle. Watch 3-second retention and completion only.

**Week 2 (14 to 20 September) — Double down.** The Sunday feedback run reweights the calendar: the top two angles from week 1 take 3 of the 5 daily slots, the bottom angle drops to 3 posts for the week. Introduce the first recurring series title ("Drop of the Day #8", "Wrong Way Wednesday") so viewers recognise a format. Watch shares and saves.

**Week 3 (21 to 27 September) — Series and loops.** Every post is part of a numbered series, and every short cut ends on a loop line. Add one "reply to comment" video per day where the avatar answers the top comment from the previous day; comment-reply videos are the cheapest follower converter on TikTok and Instagram. Watch follows per 1,000 views.

**Week 4 (28 September to 4 October) — Compound.** Recap formats: "the five biggest AI drops this month", "the three mistakes you all admitted to in the comments", "my free stack after 30 days of testing". These get the highest save rate of the month and re-surface the earlier winners. Two catch-up days (5 and 6 October) carry the month-in-review and the "what's next" post.

**Daily minimum viable success.** By day 30 the realistic scoreboard for a brand-new faceless AI account posting 5 a day is one post over 100K views, a median post over 2K, and 3 to 5% of viewers on the best posts converting to follows. The 3.6M-in-a-week screenshot that started this is an outlier result from an established account; the plan above is built to find the one or two formats that can produce that outlier, then feed them.

---

## 6. Sources used for the validation pass

Current-month research that the numbers and formats above are drawn from:

- OpusClip, Short-form video trends reshaping creator marketing 2026 — https://www.opus.pro/blog/short-form-video-trends-reshaping-creator-marketing-2026
- Miraflow, How to go viral in 2026 and 10 AI Shorts formats that go viral — https://miraflow.ai/blog/how-to-go-viral-2026-what-actually-works-across-platforms and https://miraflow.ai/blog/ai-shorts-formats-that-go-viral-2026
- Virvid, TikTok algorithm 2026 and faceless Shorts strategy — https://virvid.ai/blog/tiktok-algorithm-2026-explained and https://virvid.ai/blog/faceless-shorts-dominance-strategy-2026
- Darkroom, TikTok algorithm 2026: how to win with rewatches — https://www.darkroomagency.com/observatory/how-tiktok%E2%80%99s-algorithm-works-in-2026-and-15-tactics-to-go-viral
- Stack Influence, Best TikTok video lengths 2026 — https://stackinfluence.com/blog/best-tiktok-video-lengths-for-creators-in-2026
- SocialPilot, Instagram Reels algorithm 2026 — https://www.socialpilot.co/blog/instagram-reels-algorithm
- Hootsuite, Instagram algorithm tips 2026 — https://blog.hootsuite.com/instagram-algorithm/
- Buffer, How the Instagram algorithm works 2026 — https://buffer.com/resources/instagram-algorithms/
- ReelRise, Viewed vs swiped away on YouTube Shorts — https://reelrise.app/guide/viewed-vs-swiped-away-the-only-youtube-shorts-metric-that-matters/
- Socialync, YouTube Shorts algorithm 2026 — https://www.socialync.io/blog/youtube-shorts-algorithm-2026
- Beginners in AI, Best AI tools 2026: what Reddit recommends — https://beginnersinai.org/best-ai-tools-reddit-2026/
- DEV Community, Reddit's most upvoted AI tools of 2026 — https://dev.to/b1fe7066aefjbingbong/reddits-most-upvoted-ai-tools-of-2026-ranked-3hhl
- Barchart, The 2026 faceless creator survival guide — https://www.barchart.com/story/news/1140548/the-2026-faceless-creator-survival-guide-how-to-build-a-10kyear-tiktok-account-using-ai-avatars
- The Neuron, Everything that happened in AI, 3 September 2026 — https://www.theneuron.ai/digest/everything-that-happened-in-ai-today-thursday-september-3-2026/
- AI Agent Store, AI agents news week of 5 September 2026 — https://aiagentstore.ai/ai-agent-news/this-week
- MEAN CEO, AI product launches September 2026 — https://blog.mean.ceo/ai-product-launches-news-september-2026/
