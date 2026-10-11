# Product Mastery, Reverse Engineered

Reconstruction of the likely methodology behind ClickBank's $27 "Product Mastery"
guide, converted into criteria we can actually run, plus an audit of why our own
screening has produced zero tests.

Date: 2026-09-20
Status: framework only. No product approved. No spend authorised.

Sources used: the sales page copy supplied by the user, ClickBank's own public
blog claims (via search index), and our prior evidence files. The paid product
was NOT purchased or obtained. Nothing here is copied from it.

---

## 0. What the product almost certainly is

Two things, sold together:

1. A filter (the "5 step checklist") — reconstructable, low value, below.
2. A list of offers that currently pass the filter — NOT reconstructable without
   marketplace time-series data.

Item 2 is the whole product. The FAQ confirms it: "The Product Mastery PDF guide
along with a list of the current offers that fit the criteria." The guide sells
the list.

Their defensible claim — "years of marketplace data and affiliate research that
ONLY we have access to" — decodes to one specific thing: **they can see how each
offer's metrics moved over time.** We only ever see today's snapshot. That is the
real asymmetry, and it is the single missing input in every screen we have run.

---

## 1. The inferred 5-step checklist

Read straight off the sales page's own claims and negations.

| # | Step | The sales page tell |
|---|------|---------------------|
| 1 | **Proof of life** — other affiliates are already being paid on it | "products that had no chance of ever converting" |
| 2 | **Momentum, not peak** — metrics rising, before the crowd arrives | "BEFORE they scale to $10,000+/day"; "circumventing overly saturated products" |
| 3 | **Unit economics** — payout × conversion must beat traffic cost | "waste thousands on ads and have no sales to show for it" |
| 4 | **Funnel & trust quality** — page converts cold, refunds don't eat it | "low converting products" |
| 5 | **Competitive room** — a beginner can win a slice | "affiliates 100x their size would CRUSH them" |

Nothing exotic. The value is entirely in step 2, which needs data we don't have.

---

## 2. Measurable criteria

Notation: `G` = Gravity, `C` = initial commission per sale, `R` = expected return
(refund) rate, `CVR` = click→sale conversion rate, `CPC` = cost per click on the
chosen channel.

`Net commission  N = C × (1 − R)`
`Expected EPC    E = CVR × N`
`Breakeven CPC   = E`.  **Required margin: E ≥ 1.5 × CPC.**

### Gate 1 — Proof of life (snapshot data, we have this)
- `8 ≤ G ≤ 60`. Below 8: too few independent affiliates earning to call it proven.
  Above 60: that is the crowded end the product explicitly tells you to avoid.
- Avg $/sale > 0 and consistent with stated commission.
- **PASS/FAIL. Hard.**

### Gate 2 — Momentum (time-series, we do NOT have this)
- `G` rising across ≥4 weekly snapshots, or `G_now ≥ 1.25 × G_4wk_ago`.
- Offer age: first appeared in the marketplace within the last ~6 months, or
  re-launched (payout or funnel changed) within 8 weeks.
- **This is the gate that separates "early" from "dying". Both look like G≈10 in
  a snapshot.** Rocket (G 9.3) and AMP (G 10.7) may have been either. We had no
  way to tell, and we never admitted that.
- **Cannot be evaluated today.** Fix: start weekly snapshots now (cost: £0, 4
  weeks of calendar), or buy the $27 list.

### Gate 3 — Unit economics (computable, channel-dependent)
- Compute `E = CVR × C × (1 − R)` using marketplace CVR.
- Require `E ≥ 1.5 × CPC_channel`.
- Channel CPC planning bands (assumptions, label them as such):
  native (Taboola/Outbrain/NewsBreak) £0.05–£0.40; TikTok £0.30–£0.80;
  Meta £0.40–£1.20; Google Search non-brand £0.80–£3.00.
- **Note what this replaces: there is no payout floor.** A $50 offer at 3% CVR on
  £0.20 native clicks beats a $235 offer at 1.2% CVR on £0.90 Meta clicks.

### Gate 4 — Funnel & trust
- `R < 15%`, and the basis must be **30 Day or 90 Day**. If the basis is
  "Category Average", the vendor has no history — treat R as unknown and drop the
  offer a tier, don't reject it.
- Vendor entity identifiable (company name, address, contact on the order page).
- Affiliate resources page exists (swipe, creatives, terms). Absence = the vendor
  isn't running an affiliate programme seriously.
- Paid-social compliance: does the vendor permit the channel we intend to use.
- **Trust evidence must come from the vendor's own assets, not affiliate-built
  review pages.** Affiliate pages are written by strangers with a commission
  motive; their inconsistencies are evidence about *them*, not the vendor.

### Gate 5 — Competitive room
Four public checks, each scored 0–2 (0 = wide open, 2 = saturated):
- Meta Ad Library: count of active ads naming the product.
- TikTok: count of distinct creatives / accounts pushing it.
- Google: how many of page 1 for `"<product> review"` are affiliate pages.
- Reddit / forums: is the product being discussed organically at all (0 mentions
  is a demand warning, not a win).
- **Total ≤ 5 of 8 to proceed.** 0 across the board means no proven demand, which
  is a fail, not a green light.

### Verdict rule
- **Reject** — fails Gate 1, Gate 3, or Gate 4 hard.
- **Watch** — passes 1, 3, 4 but Gate 2 is unknown → enters the weekly snapshot
  list and is re-scored in 4 weeks.
- **Test** — passes all five, and one creative angle can be stated in a sentence.

---

## 3. Re-audit of our previous filters

### Signals we pointed at that were wrong

**The $100 payout floor.** The most damaging filter we ever set. Our own screen
proved it: 109 offers at payout ≥$80 and G ≥5, of which 92 were Health &
Fitness. We concluded "supplement dominance is structural to the marketplace."
Wrong conclusion — it is structural *to the band our filter selected*. The filter
manufactured the finding, then we treated the finding as marketplace truth.
Payout is an input to EPC, never a threshold in itself.

**High payout treated as opportunity.** Already disproven by us: Crypto Code
$1,716 / G 1.8 / EPC $0.14. Correctly abandoned. Worth keeping as the standing
counter-example.

**Static screening.** Every screen we ran was a single snapshot. A snapshot
cannot distinguish an offer on the way up from one on the way down. This is not a
detail — it is the entire mechanism the $27 product sells, and we never even
recorded that we were missing it.

**Prior verdicts treated as settled.** Soulmate Sketch carries
`CUSTOMER_QUALITY=NEGATIVE` from a pipeline whose category assumptions, refund
assumptions and EPC field interpretation were all subsequently found wrong. A
verdict from a broken screen is not evidence. Re-screen it or delete the verdict;
leaving it as "unresolved" costs us the option for free.

### Where we were too strict

**The diligence bar.** AMP Joint 10 was killed on: inconsistent review counts on
third-party affiliate pages, no Trustpilot footprint, no Supplement Facts panel.
Every one of those is true of essentially every direct-response supplement on
ClickBank. A rule that rejects 100% of the category the marketplace is made of is
not a filter — it is a decision to leave the category. If that is the decision,
make it explicitly and stop screening supplements. Don't re-derive it offer by
offer over several days.

**"Why wouldn't they just use the free alternative?"** Correct and decisive for
commodity information products (Rocket vs ChatGPT; InstaDoodle vs any AI tool).
Wrongly generalised into a universal test. Direct-response buyers are not
rational comparison shoppers — that is the premise of the entire industry.
Applied universally, this question rejects everything, which is roughly what
happened.

**Confidence set at "would I defend this in public?"** The actual question for a
£210 test is narrower: will a cold click convert, and will the sale survive the
refund window? We were running a brand-safety review and calling it commercial
diligence.

### What was missing entirely

**We never tested ourselves.** Every offer was judged; our own ability to make an
ad that converts was never put on trial. In a £210 test the offer is maybe 40% of
the outcome and the creative is the rest. Nine months of offer screening has
produced zero evidence about the variable that matters most.

**No kill rule.** There is still no written stop-loss. Without "£X spent or Y
clicks with zero sales → dead," any test will drift into the same open-ended
analysis loop as the screening did.

### The correction you proposed is right

"Find a decent early product, create strong angles, test fast, kill cleanly" is a
better machine than "find the best product." I'd add one thing: the reason the
old machine never terminated is that "best" has no stopping condition and
"decent" does. Write the decent-threshold down (Gates 1/3/4 above) and the search
ends the moment something clears it.

---

## 4. Candidates — what I can and cannot give you

**I am not going to hand you ten products with Gravity and EPC numbers.** This
environment's network policy blocks `accounts.clickbank.com`, `cbengine.com` and
`cbsnooper.com` at the proxy (verified: 403 on CONNECT). Any table of metrics I
produced here would be invented or recalled from stale training data, and this
project has already been damaged twice by numbers that turned out to mean
something other than we thought (`average_epc`, `expectedReturnRate`). Fabricated
precision is the specific failure mode to avoid.

What I can give:

### 4a. One structural lead worth more than a product list

**Performance e-commerce.** ClickBank states publicly that this category began
appearing on the marketplace in early 2026, and gives indicative economics of
**$50–$100 commission at 2–3%+ CVR**, promoted mainly on native (Taboola,
Outbrain, NewsBreak) and TikTok. Named examples in their own material include
Water Freedom System, Air Fountain, Joseph's Well, Dark Reset.

Run the arithmetic on their own claimed numbers:

```
E = 0.025 × $75 = $1.88 EPC   (≈ £1.45)
Native CPC ≈ £0.05–£0.40  →  margin 3.6×–29×
TikTok CPC ≈ £0.30–£0.80  →  margin 1.8×–4.8×
```

This is the first structure in this project whose economics clear ex ante rather
than after optimistic assumptions. Caveats, stated plainly: [Likely, not Certain]
— these are the marketplace operator's own promotional figures about its own
marketplace, so biased upward; and a new category means thin refund history
(Gate 4 will read "Category Average" for many of these).

It also fits your constraints better than anything we've looked at: physical
product (survives the free-substitute question), mid payout (doesn't force the
$100-floor supplement trap), visual (suits faceless UGC), native-friendly (cheap
clicks, so £210 buys a real test rather than 200 clicks).

Note one thing: **Water Freedom System already crossed our desk** and we rejected
it as "digital plans / free-information substitution." ClickBank classifies it as
performance e-com. Worth re-reading which it actually is before re-rejecting.

### 4b. The screener that produces the ten

`screen.py` in this directory implements Gates 1, 3 and 4 against a ClickBank
marketplace export and ranks the survivors. It takes CSV or the REST API JSON,
normalises the field-name variants, and prints Reject/Watch/Test with the reason.
Getting you a real ranked ten is then a ~20 minute job on your side:

1. Log into ClickBank → Marketplace. Filter **Category = E-Commerce**, language
   English. Also pull Health & Fitness for comparison.
2. Export or copy the results (site, title, category, initial $/sale, avg $/sale,
   gravity, CVR, return rate, return rate basis).
3. `python3 screen.py marketplace.csv --cpc 0.25 --channel native`
4. Paste the output back here and I'll do Gate 5 (saturation) on the top ~10 and
   write the angles.

**Start the weekly snapshot on the same pull.** `screen.py --snapshot` writes a
dated copy. Four of those and Gate 2 comes online permanently, and we stop being
dependent on anyone's proprietary list.

---

## 5. Recommendation

**Buy the $27 guide. Not for the method — the method is above — for the list.**

The list is a momentum-filtered shortlist, and momentum is the one input we
cannot produce for another four weeks. $27 to skip four weeks of calendar is
good value even at a 50% chance the list is stale or padded. Treat it as a
candidate generator, not as truth: every name on it still goes through Gates 1,
3, 4 and 5 above, and if their list and our screener disagree, our screener wins
on anything we can measure.

**Do not buy Spark.** The $27 product's entire commercial purpose is to sell you
the upsell. The FAQ tells you so.

**Concrete next actions, in order:**

1. Pull the marketplace export (20 min, your login) — E-Commerce + Health.
2. Run `screen.py`, post the output here.
3. Buy the $27 guide, post its shortlist here.
4. I score both lists on Gate 5 and return **one** offer with a stated creative
   angle and a stated kill rule.
5. Test budget: **£15/day × 4 days on native, not £30/day × 7 on TikTok.** Native
   CPCs make £60 buy a statistically meaningful number of clicks on a $50–100
   offer, where the same £60 on Meta buys noise. Kill rule fixed in advance:
   **zero sales by 300 clicks → dead, no appeal.**

The thing that ends this project's nine-month loop is step 5, not steps 1–4.
Everything above is only worth writing because it terminates in a test.

---

## 6. What the purchased product actually changed (2026-10-11)

Product Mastery was bought ($27) and fully extracted: the 14-page PDF plus all
eleven course video transcripts. The advertised "list of current top offers" does
not exist in it — refund requested separately. What it did deliver:

### Corrections to the gates above

| | before | after | source |
|---|---|---|---|
| Gravity, paid/cold | 8–60 | **100–250** | "a paid media buyer will want to see a higher gravity score of 100 plus" (*The Numbers*) |
| Gravity, free/warm | 8–60 | **10–100** | free-traffic affiliates told to "avoid the affiliate products with the highest gravity scores of 100 plus" (same) |
| Payout, paid/cold | no floor | **$100+ expected** | "you're gonna want to see products in the triple digits... in order to profitably back out" (same) |

Section 3 above called the $100 payout floor "the most damaging filter we ever
set." That holds for the band we were screening in, but is wrong as a general
rule: for cold paid traffic their own guidance restores it. The resolution is
that payout is still not a gate — EPC vs CPC decides — but at Gravity 100+ on
cold traffic, offers under $100 rarely clear the margin anyway.

### New, and operationally useful

- **Take CPA over rev-share where offered.** "CPA... eliminates the risk for
  refunds for you. You get paid a flat fee for every sale that you drive and you
  get to keep the commissions no matter what happens after the sale." This makes
  Gate 4's refund threshold irrelevant on a CPA deal, and would have saved AMP
  Joint 10 from rejection on a 15.4% return rate.
- **"Requires Approval" offers are an advantage, not friction.** Vendors gate
  them "to ensure that their products don't hit saturation and they can better
  control the quality of affiliates promoting them." Direct answer to the
  beginner-versus-whale problem.
- **Affiliate support pages publish EPC and conversion rate**, linked under
  "average payout" on the marketplace listing. Section 2 said this data was hard
  to get; often it is sitting on the vendor's own page. Their caveat: treat it as
  optimistic, since it is usually measured on warm or hand-picked traffic.
- **Those same pages carry demographic data, ad creative, pre-written copy and a
  hoplink generator offering several sales-page variants.** Free creative raw
  material, and a second variable to test besides the ad.
- **Day-0 profitability**: "measuring your earnings per click versus your cost
  per click for your campaigns in real time." Identical to Gate 3 and the kill
  rule in TEST_PLAN.md.

### The method that replaces the missing list

"Niching down": take the top 3 offers in each of ClickBank's top 10 niches — 30
offers — then filter to Gravity 100+ with CPA available. That is a finite,
self-built shortlist, and it is the closest thing to the product's unfulfilled
promise. It costs about thirty minutes in the marketplace.

**Not useful for us:** the "past champions" method (offers whose Gravity has
declined from a peak — contradicts the 100+ paid floor; it is a free-traffic
play) and the "handshake deal" method (networking and events; long-term).
