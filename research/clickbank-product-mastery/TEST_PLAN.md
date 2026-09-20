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
