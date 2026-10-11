# Test #1 — execution plan

The channel, budget, tracking, bridge and kill rules are fixed here. The offer
and its angles are the only open items, and they are blocked on one input only.

Date: 2026-09-20. Supersedes the £15/day suggestion in the previous reply.
Budget ceiling: £210, not authorised until the offer is chosen.

---

## 1. Channel: native. Decided by arithmetic, not preference.

Kill threshold is 300 qualified clicks. Budget ceiling is £210. So the maximum
CPC at which this test can reach a verdict at all is:

```
£210 / 300 clicks = £0.70 per click — absolute ceiling
```

Against realistic planning CPCs:

| Channel | Planning CPC | Clicks for £160 | Reaches 300? |
|---|---|---|---|
| Native (Taboola/Outbrain/NewsBreak) | £0.15–£0.40 | 400–1,060 | **yes, with margin** |
| TikTok | £0.30–£0.80 | 200–530 | marginal |
| Meta | £0.40–£1.20 | 130–400 | mostly no |
| Google Search non-brand | £0.80–£3.00 | 50–200 | no |

Meta and Google are out on budget arithmetic before any offer is named. TikTok
can only reach a verdict at the cheap end of its band, which you cannot assume
in advance. Native is the only channel where £210 reliably buys a decision.

This is not "native is better." It is "native is the only one that fits the
budget and the kill rule you wrote."

**Network: Taboola first.** No minimum deposit, self-serve entry, lowest
friction for a first account. Outbrain's $20/day floor is fine but it asks a
$500 deposit from serious buyers. NewsBreak is the fallback if Taboola rejects
the account.

### What this decision costs you

Native de-prioritises Soulmate Sketch. Psychic/soulmate-drawing offers draw
heavy native compliance rejection, and it is also the one offer carrying an
unresolved customer-quality flag. It belongs in a different lane (Meta/TikTok),
where the click math above does not clear £210. **Recommendation: do not spend
time re-screening Soulmate for test #1.** It is not rejected — it is out of
scope for this channel. Revisit it only if a native test succeeds and funds a
second lane.

---

## 2. Spend plan

```
£40/day × 4 days = £160        one network, one campaign, two ad sets (one per angle)
£50 held in reserve            not spent without a new decision
```

Why £40/day and not £15: $50/day is Taboola's own stated signal threshold, and
£40 ≈ $50. Below that the algorithm never leaves the learning phase and you pay
for noise. £40/day also clears Outbrain's $20/day floor 2.5× if you switch.

At £0.25 CPC this buys ~640 clicks — over twice the kill threshold, so a real
verdict survives a CPC overrun.

**Day-1 abort:** if realised CPC after day 1 implies fewer than 300 clicks for
the full £160, stop the campaign and report it. Do not top up to chase the
threshold. That is a channel/offer mismatch, not a budget problem.

---

## 3. Bridge page — required, not optional

Taboola and Outbrain do not accept direct affiliate links. You need a page on a
domain you control. **Prerequisite: confirm you have a domain and somewhere to
host a static page. If not, this blocks everything below.**

Structure (advertorial, ~600–900 words, mobile-first):

1. Headline continuing the ad's promise. Do not restate the offer's headline —
   the click already happened; this page's job is to qualify, not re-sell.
2. Three to five paragraphs on the problem, in the reader's language.
3. The mechanism — why this approach works — without making the claim the
   vendor's page makes. Your page must not out-claim theirs.
4. Single CTA to the hoplink. One link, repeated two or three times, same target.
5. Footer: who you are, affiliate disclosure, contact, privacy link. Native
   compliance reviewers check for this; its absence is a common rejection.

No email capture on test #1. It adds a variable and delays the read.

---

## 4. Tracking — verified before a pound is spent

Four-stage funnel, no infrastructure to build:

```
native click  →  bridge page  →  hoplink hop  →  order form  →  sale
 (platform)      (your page)     (ClickBank Analytics, by TID)
```

Setup:

- Bridge URL carries the network's click macros, e.g.
  `https://yourdomain/report?cid={click_id}&site={site}&ad={ad_id}`
  Confirm the exact macro names in the Taboola campaign UI — they change.
- Bridge CTA appends a TID to the hoplink encoding angle + placement:
  `https://AFFILIATE.VENDOR.hop.clickbank.net/?tid=a1site<id>`
  Keep it short and strictly alphanumeric; ClickBank rejects special characters
  and caps the length. Check the HopLinks guide for the current limit.
- ClickBank's newer affiliate tracking parameters (June 2024+) supplement TID
  and are the recommended way to pass unique click identifiers. Use them
  alongside TID, not instead of it, for this first test.
- Read results in ClickBank → Reporting → Analytics, which reports hops, order
  form impressions and sales **by TID**. That gives per-angle conversion without
  any third-party tracker.

**Verification step, before launch, costs £0:** load the bridge directly with a
fake `cid`, click through to the hoplink, and confirm the hop appears in
ClickBank Analytics under the expected TID. If it does not appear, tracking is
not verified and the kill rule cannot be applied. Do not launch.

---

## 5. Creative angles — what "materially different" has to mean

Two angles that are variations of the same idea invalidate the test: a null
result then tells you nothing about the offer. The two must differ on the axis
below, not on headline wording or image choice.

- **Angle A — problem-first.** Opens on the reader's symptom/frustration. Tests
  whether the pain is sharp enough to buy against.
- **Angle B — mechanism/curiosity-first.** Opens on the unusual thing about how
  it works. Tests whether the offer has a hook independent of felt pain.

If both produce clicks and neither produces a sale, the offer is dead on this
channel. If A works and B doesn't (or vice versa), you have a direction, not a
failure. Optional third angle only if the offer has an obvious social proof or
price/comparison hook.

Concrete copy for both arrives with the offer — it cannot be written before it.

---

## 6. Kill / continue rules

**Kill the offer/channel combination when:** 300 qualified clicks delivered,
across at least two materially different angles, tracking verified, zero sales.
No appeal, no rescue attempt, no "one more creative."

Qualified click = a click that reached the bridge page, per your own page
analytics — not the network's billed click count. Expect 10–25% loss between
billed clicks and landed sessions; budget for it.

**Continue when:** one or more sales land before 300 clicks. Then the question
becomes CPA vs net commission, and a second tranche from the £50 reserve is a
new decision, not an automatic one.

**Abort early (not a kill) when:** day-1 CPC implies missing 300 clicks on
budget; or tracking breaks mid-flight; or the network disapproves the creative
and the campaign never delivers. These are execution failures. They say nothing
about the offer, and the offer goes back in the queue unjudged.

---

## 7. The one open item

Offer and angles are blocked on a single input, either of:

- a ClickBank marketplace export (log in → Marketplace → Category = E-Commerce,
  English → export), run through `screen.py`; or
- the $27 Product Mastery shortlist, scored against the same gates.

Either one, pasted back, returns: one offer, two angles with copy, bridge
headline and body, and the campaign settings — in a single pass. Nothing else in
this document changes when the offer arrives.

---

## 8. Offer selected: Tina Aldea | Soulmate Sketch (2026-10-11)

Vendor ID `tinapsc`. CB rank #4, Gravity 61.9, avg $/conv $68.79, CVR 7.26%,
EPC $4.90. Screens at **15.7x** expected EPC over a £0.25 native CPC, and still
clears at 4.7x if the published EPC is discounted 70% for cold traffic. Nothing
else in the 31-offer pull survives that discount with room.

### Corrections to sections 4 and 5 above, from the vendor's affiliate page

- **Tracking parameter is `aff_sub1`, not `tid`.** The vendor states this
  explicitly: "Please use `aff_sub1`, not `tid`." Section 4 is wrong. Link form:
  `https://hop.clickbank.net/?affiliate=NICKNAME&vendor=tinapsc&aff_sub1=<code>`
- **The destination is a quiz page, not a VSL.** "There is no VSL page. Don't
  look for one. The simple quiz page your link opens is THE page to advertise...
  we tested it with over $900,000 of our own ad spend." So the bridge page in
  section 3 should not try to sell. Its only jobs are native compliance, the FTC
  disclosure, and qualifying the click. Keep it short; the quiz converts.
- **Direct linking to the cart or order form is banned** and results in a
  permanent ban. Linking to the hoplink (which opens the quiz) is what they
  instruct. A bridge page in front of the hoplink is fine.

### Terms that bind the creative

Commission is **90% on the whole funnel** — front end, order bumps, every
upsell, same rate for every affiliate. It is **rev-share, not CPA**, so the CPA
refund-immunity noted in FRAMEWORK.md section 6 does **not** apply here.

Prohibited in ads and on the bridge: "guaranteed to find your soulmate", "100%
accurate", "hand-drawn by Tina personally", "find your true love in 24 hours",
"scientifically proven", any health/medical/relationship guarantee.

Approved: "for entertainment purposes only", "psychic soulmate sketch",
"personalized digital sketch", "unique reading experience", "fun and meaningful
gift idea", "explore your love journey", "30-day money-back guarantee via
ClickBank".

Also binding: no PPC bidding on brand terms; no "scam"/"fraud" in copy; no
claiming to be the creator; no spy-tool copying of other affiliates' campaigns.
FTC disclosure must be clearly visible, never buried in a footer. Enforcement is
three strikes: warning, commission hold, permanent ban with commissions
forfeited.

Vendor demographic guidance: all genders, 35+.

### Open items before spend

1. **Return rate is not published** anywhere on the listing or the affiliate
   page. On a 90% rev-share deal refunds come straight out of the commission, so
   this is the live risk on this offer, not compliance. Check the marketplace
   listing for `expectedReturnRate` and its basis.
2. **Network acceptance is unverified.** Taboola's published prohibited and
   restricted lists do not appear to name psychics, astrology or tarot (Microsoft
   Advertising does ban the category, but that is a different network). This
   resolves itself for free: account creation and campaign review cost nothing,
   and nothing is charged until delivery starts. Submit and find out.
3. Creative supplied by the vendor is **email swipes only** — no ad images, no
   video, no demographic breakdown. Everything for native is written from
   scratch.
