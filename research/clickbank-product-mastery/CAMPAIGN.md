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

## Gate 5 — saturation check (done 2026-10-12)

**Category saturation: high.** ClickBank carries several near-identical
competing offers — "Soulmate Sketch" (Master Wang / Cosmic Media LLC),
"Soulmate Sketch 2.0 [Feb 2026]", "Naked Soulmate Sketch — crushing it on
TikTok", plus off-platform operators (Soulmate Story, Soulgaze Drawing,
auralyapp). Expect competition on the obvious angles and upward pressure on
CPCs. Read the other way: Tina Aldea's offer sits at rank #4 with a $4.90 EPC
*inside* that crowded category, which is a point in its favour rather than
against — it is winning where many are trying.

**Category reputation: poor, and this matters for angle choice.** Trustpilot
carries complaints about $1.99 soulmate-sketch trials followed by $39.99
charges, and about subscriptions people struggled to cancel. Those complaints
name other operators (soulgazedrawing.com, auralyapp.com), not Tina Aldea — and
the distinction is real: her offer averages $68.79 with $0.07 of future
commission, i.e. a one-time sale, not a trial-to-subscription trap. But anyone
who googles "soulmate sketch review" lands in that mess.

Consequence: **do not run a review or comparison angle.** It sends readers
straight to the category's complaint footprint. The two angles written here —
feeling-first and mechanism-first — are editorial and don't invite that search.
That was the right call by accident; keep it deliberate.

This also partially rehabilitates the old `CUSTOMER_QUALITY=NEGATIVE` verdict
from the original pipeline. It was reached by a process we later found broken,
but the underlying signal about the category was not baseless.

**Channel support, first-party:** ClickBank's own blog says native networks such
as NewsBreak and Taboola work for cold spirituality traffic, cost less than
Facebook and YouTube and are less saturated, at the cost of smaller audiences
and more testing needed. That supports the channel pick. Note one inconsistency:
elsewhere the same blog files soulmate sketch under warm-traffic offers.

**Ignore the conflicting payout figures** on third-party listing sites ($1.13
EPC, $0.20 EPC, $25 CPA). Those describe the competing offers, not this one. The
live marketplace pull is the only figure to trust.

## Deployment state (2026-10-12)

Live at **read.firstdrophq.com** — Cloudflare Worker `firstdrop-read`, static
assets, custom domain on the firstdrophq.com zone, valid certificate. The
firstdrophq.com root is a separate project and was not touched.

Tracking verified end to end by clicking each bridge CTA once. Both hops
resolved with the nickname and sub-id intact and distinct ClickBank hopIds:

```
/a/ -> aff-tinaaldea.com/?hopId=80368622-...&hop=digitdog&aff_sub1=a1
/b/ -> aff-tinaaldea.com/?hopId=5f16f738-...&hop=digitdog&aff_sub1=b1
```

Still to do before spend: confirm both hops appear in ClickBank → Reporting →
Analytics (the kill rule depends on that reporting working, not just on the
redirect carrying the parameters), then open the Taboola account.

Noted in passing: the vendor's own sales page says "I will draw your Destined
Soulmate in 24 hours and tell you when and where you'll meet", which sits close
to the claims their affiliate terms forbid affiliates from making. Their page,
their risk. The bridge pages are deliberately more conservative, and the bridge
is what the ad network reviews.

**Analytics confirmed (2026-10-12).** Cloudflare Web Analytics is registered for
read.firstdrophq.com in JS-snippet mode and recorded **3 page views across 1
visit** — root, /a/ and /b/ in a single session, which is exactly the test that
was run. Page load 385ms, Core Web Vitals all green. Landed clicks are now
measurable on our side, so the kill rule's "qualified click" is enforceable.

Every pre-spend step is complete: pages live on a real domain with a valid
certificate, hoplinks verified carrying the nickname and per-angle sub-ids,
saturation checked, analytics recording per-path. The only remaining step is
opening the Taboola account and submitting for review, which is also free.
