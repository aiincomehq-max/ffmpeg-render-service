# Receipts vs Claims

**The series format. A viral "AI made me money" post, taken apart on screen, then held against 140 days of real logs.**

The mechanic is borrowed from the breakdown accounts (a viral video, paused and annotated, "here's why this works", comment for the list). The subject is different: not how viral videos work, but how viral *money claims* work, and what the same experiment produced when someone actually ran it with receipts. The audience is the burnt. The credential on every video is one line: **self-hosted n8n on Hetzner, 600+ workflows, a couple of hundred built by hand, £0 earned.**

## Why this beats the paper cards

The paper-card Reel says "here is my number". This format says "here is their number, here is how it was built to make you comment, and here is my number". It borrows the reach of the post it dissects (people who saw the original recognise it instantly), it carries a built-in villain without naming one, and every episode ends on a receipt that can be checked. It also produces its own lead magnet: every hook pattern identified in an episode goes into the list the comment keyword delivers.

## The four-beat structure (25 to 40 seconds)

| Beat | Time | On screen | Spoken |
|---|---|---|---|
| 1. The claim | 0–3s | The original post, paused on the money line. Handle blurred or cropped. | Read the claim verbatim. "3.6 million views in one week and $7,526." Nothing else. |
| 2. The mechanism | 3–15s | Same frame, annotated: arrows and labels on the paper, the number, the comment CTA. | Two or three sentences on what each element is doing. Paper = trust. Specific-but-unverifiable number = bait. "Comment X" = a DM bot and a lead list. |
| 3. The receipt | 15–30s | Cut to your ledger card, or a screen recording of the actual log. | "I ran the same experiment. Here's mine." One number, one screenshot, one sentence. |
| 4. The turn | last 3–5s | Card: the one question the viewer should ask next time. | The loop line, then "Comment RECEIPTS and I'll send you the 50 hooks these posts use on you. Free. No course." |

The turn is what stops it being bitter. Every episode ends by giving the viewer a tool, not a grievance.

## Production

Screen-record the original on your phone, import to CapCut, freeze on the claim, draw the annotations by hand (finger on the screen reads more honest than motion graphics). Voice-over in your own voice, straight to phone mic. The receipt card is a screenshot of the real sheet or dashboard with the number circled. No avatar, no Kling, no render service. Twenty minutes per episode once the script exists.

Half of the script can come from the pipeline. The Apify scrapers in the HumanUpgrade project already pull TikTok, Instagram and YouTube posts with view counts and creator followers, and the January workflow already transcribes and OCRs posts. Point them at AI-money content, run the analyser prompt in `prompts/claim_anatomy.md` over each post, and the mechanism beat writes itself. The receipt beat is a lookup into `../ledger.csv`.

## The rules that keep it safe and keep it credible

These matter more here than in any other format, because the whole account's authority is that its own claims can be checked.

Never say a claim is fake. Say it is unverifiable, and show the blank column. You cannot know their number; you can know that nobody can check it, and that yours can be checked. Never name the creator in the spoken track or caption; blur the handle in the frame. The subject is the claim structure, which thousands of accounts share, not the person. Comment on the post, not the poster. "This number is doing a job" is criticism of a technique. "This person is a scammer" is a defamation claim you would have to defend in a UK court, where the burden is on you. Use the original only as much as the commentary needs: a frozen frame or a few seconds, annotated, is commentary; reposting the whole thing is not. Give the viewer something on every episode. The lead magnet is the anger converted into a tool.

## What the comment keyword delivers

**RECEIPTS** → the DM sends `lead_magnet/50_hooks_they_use_on_you.md` as a page, free, no email required to read it. The email field on the page is optional and offers the full Ledger. The product ladder behind it is unchanged from `../funnel/FUNNEL.md`: the actual build for £29, the post-mortem for £97, the one-hour "don't spend 140 days" call for £249.

The 50 hooks list is the one that grows. Each episode identifies one or two hook patterns; they are appended to the list with the episode number, so the lead magnet is always slightly bigger than the version the last person got, which is a reason to comment again.

## Cadence and the first ten

One episode a day. Episodes 1 to 5 are scripted in `episodes/`. Episode 1 is the carousel that started this. Episodes 2 to 5 are the four archetypes that cover most of what the algorithm serves to someone who has ever watched an AI-money video, so any real post that comes through the scraper maps to one of them. Episodes 6 to 10 come from the scraper, whichever claims are getting the most reach that week.

## The numbers to watch

Comments per 1,000 views on the RECEIPTS keyword is the measure of the turn. Shares per view is the measure of the mechanism beat, because the mechanism is what people send to the friend who fell for it. Follows per 1,000 views is the measure of the credential line. If comments are high and follows are low, the receipt beat is too weak: put the actual sheet on screen, not a card.
