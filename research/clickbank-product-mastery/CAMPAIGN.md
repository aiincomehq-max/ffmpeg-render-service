# Test #1 — campaign sheet

Offer: **Tina Aldea | Soulmate Sketch**, vendor `tinapsc`, 90% revshare,
$68.72 avg initial commission. Channel: **Taboola**, native, cold.

## Before launch

1. Replace `YOURNICKNAME` in both bridge pages with your ClickBank nickname.
   Two places: `bridge/a/index.html` and `bridge/b/index.html`.
2. Deploy `bridge/` to Cloudflare Pages on a **subdomain**:
   **`read.firstdrophq.com`**. Not humanupgradehq.com (health branding, wrong
   vertical) and not the firstdrophq.com root, which is a live site selling
   digital products — a psychic advertorial sitting inside it is incoherent to
   a reviewer, and the logo would lead somewhere unrelated. A subdomain leaves
   the main site untouched while inheriting the domain's age, which native
   reviewers weigh more kindly than a domain registered yesterday. The pages
   brand as "First Drop", so the subdomain reads as an editorial section.
   Pages go live at `read.firstdrophq.com/a/` and `/b/`.
3. Verify tracking at zero cost: open `/a/`, click through, confirm the hop
   appears in ClickBank Analytics under `aff_sub1=a1`. Repeat for `b1`. If a hop
   doesn't register, do not launch — the kill rule is unenforceable without it.
4. Saturation check (20 min): Meta Ad Library, TikTok Creative Center and a
   Google search for "soulmate sketch review". If native is already thick with
   the same offer, expect higher CPCs and say so before spending.

## Ads

Taboola wants a headline, a 1200x800 image and a branding line. Two headlines
per angle so there is something to rotate without changing the angle.

**Angle A — feeling first.** Tests whether the latent want is sharp enough to
act on. Lands on `/a/`.

- The Face You Keep Almost Remembering
- Most People Can Almost Picture Them. Not Quite.

**Angle B — mechanism first.** Tests whether the process itself is the hook,
independent of felt want. Lands on `/b/`.

- She Doesn't Ask For a Photo. Just Four Questions.
- Why a Soulmate Sketch Starts With You, Not a Picture

Branding line for both: `First Drop`

**Images.** Follow the vendor's own visual language — a framed or held sketch,
warm indoor light, nothing glossy or stock-looking. Native creative that reads
as editorial outperforms creative that reads as an advert. Do not use a photo of
an identifiable real person, and do not caption anything as hand-drawn: the
sketches are AI-generated and the vendor bans the claim "hand-drawn by Tina
personally".

## Settings

| | |
|---|---|
| Geo | United States |
| Device | Mobile + desktop, no split initially |
| Audience | All genders, 35+ (vendor's stated converting demographic) |
| Budget | £40/day, 4 days, £160 total |
| Bid | Start at the platform's suggested CPC, cap £0.50 |
| Structure | One campaign, two ad sets, one angle each, 50/50 |

US rather than UK because the vendor proved the funnel on US cold traffic with
$900k of their own spend. Running elsewhere adds a confound: a null result might
be the geo rather than the creative, and the creative is what we are testing.
Switch to UK/CA/AU only if US CPCs come back above £0.50.

## Links

```
https://hop.clickbank.net/?affiliate=NICKNAME&vendor=tinapsc&aff_sub1=a1
https://hop.clickbank.net/?affiliate=NICKNAME&vendor=tinapsc&aff_sub1=b1
```

`aff_sub1`, not `tid` — the vendor states this explicitly. Read results in
ClickBank → Reporting → Analytics, which breaks out hops, order-form
impressions and sales per tracking code.

## Rules, fixed in advance

- **Day-1 abort:** if realised CPC implies fewer than 300 landed clicks for the
  full £160, stop. Do not top up to reach the threshold.
- **Kill:** 300 qualified clicks across both angles, tracking verified, zero
  sales → the offer/channel pair is dead. No appeal, no extra creative.
  Qualified click = reached the bridge page per your own analytics, not
  Taboola's billed click count. Expect 10–25% loss between the two.
- **Continue:** any sale before 300 clicks → stop and recompute CPA against the
  $68.72 commission. A second tranche from the £50 reserve is a new decision.
- **Break-even:** this clears down to roughly 0.7% conversion at £0.25 clicks.
  Published CVR is 7.26%, so there is a ten-fold margin before it stops working.

## Compliance

Approved language only: "for entertainment purposes only", "psychic soulmate
sketch", "personalized digital sketch", "unique reading experience", "fun and
meaningful gift idea", "explore your love journey", "30-day money-back guarantee
via ClickBank".

Never: guarantees of any kind, "100% accurate", "hand-drawn by Tina personally",
"find your true love in 24 hours", "scientifically proven", invented
testimonials. No bidding on the vendor's brand terms. No direct linking to the
cart — that is a permanent-ban offence; the hoplink opens the quiz, which is
correct. FTC disclosure stays visible at the top of the bridge pages, not in the
footer.

Enforcement is three strikes: warning, commission hold, permanent ban with
commissions forfeited.
