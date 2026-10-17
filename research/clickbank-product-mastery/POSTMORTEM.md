# Soulmate Sketch campaign - what happened

Account: Taboola/Realize 2125039 (andrew@firstdrophq.com)
Campaign: 50647792, "Soulmate Sketch | US | bridge-a | Oct15 | £160"
Offer: ClickBank vendor `tinapsc`, affiliate `digitdog`, `aff_sub1=a1`
Ran: 16 October 2026. Paused and ended the same day.
Spend: £33.

## Result

| Metric | Value |
|---|---|
| Realize spend | **£33** |
| Realize impressions | **78,900** |
| Realize clicks | **321** |
| Realize CTR | **0.41%** |
| Realize CPC | **£0.103** |
| ClickBank total hops | 89 |
| ClickBank unique hops | 83 |
| **Clicks that reached the offer** | **28%** |
| **Cost per visitor delivered** | **£0.40** |
| Initial Order Form Impressions | **0** |
| Initial Sales | **0** |
| Gross earnings | **£0** |

Figures from Realize's own 24-hour performance email of 17 October. Earlier
working numbers in this session (135 clicks, ~£28) were read mid-run from a
report whose date range excluded part of the spend. They understated both the
click count and the size of the delivery gap.

Two failures, one on each side of the link.

## Failure 1 - the vendor's funnel (the one that mattered)

83 unique visitors reached the vendor's page. Not one reached a page
showing a price.

The vendor's front end is a four-question quiz followed by an email
capture. The ClickBank order form sits behind it. At 83 arrivals, a pass
rate of even one in ten would have produced about eight order form
impressions. Zero were recorded, which puts the real pass rate below
roughly one in thirty.

Break-even on this budget needed about one sale per 113 clicks. If fewer
than one in thirty even see a price, more than one in four of those who do
would have to buy. That does not happen.

**This offer's front end does not pass cold affiliate traffic through to a
checkout.** No amount of traffic quality or budget would have changed it.
That is the finding the £28 bought, and it is a real one.

## Failure 2 - Taboola's broken conversion setup

Conversion tracking could never be configured on the account:

- The **Choose conversion category** dropdown renders empty. The field is
  required, so the New Conversion form cannot be completed.
- Taboola support (Case #01250920, Sourav Kumar) said the options were
  visible on their side and suggested reducing browser zoom with Cmd+Minus.
  That made no difference.
- The alternative route the interface itself advertises - the banner reading
  "hover over it and select 'Set as conversion'" - does not open a
  configuration form. It redirects into the Abby AI chat.

The pixel itself was fine. It was installed on both bridge pages, verified
firing by curl, and confirmed receiving by Taboola's own team. `offer_click`
appeared in Active Events and reached 22 recorded hits.

**Why that cost money.** The campaign ran on **Maximize Conversions**
bidding. That strategy cannot function with no conversion defined, because
there is no signal to optimise toward. The bidder falls back to buying the
cheapest available clicks, which in Taboola's inventory means app and arcade
placements where clicks are largely accidental.

The symptom shows in the gap between what was billed and what arrived:
**321 clicks charged, 89 hops recorded at the destination. 72% of billed
clicks never reached the page they were paying for.** At £33 spend, roughly
£24 bought clicks that went nowhere.

A CTR of 0.41% across 78,900 impressions is weak for native placement and is
consistent with delivery into low-intent inventory.

[Likely, not proven] The causal link to the bid strategy fits the numbers but
cannot be demonstrated without placement-level data. The size of the gap,
however, is measured, not inferred.

**Taboola flagged this themselves, twice, and it was dismissed.** The Realize
dashboard carried a "Missing Conversion Setup" alert, and an automated account
health check emailed on 17 October said: "define at least one conversion goal
using our codeless conversions tool. This is a critical step that will allow
our algorithm to optimize your campaign." Both were read in session as generic
upsell prompts. They were not. They named the live defect.

## What this does and does not justify

It does **not** explain the zero sales. Perfect traffic would have hit the
same wall at the vendor's quiz. Doubling the arrivals doubles the number of
people who never see a price.

It does justify a refund request on the narrower ground that a required
platform feature was unusable, and the campaign was billed while running a
bid strategy that depended on that feature. Realistic outcome is an account
credit rather than cash.

## The process failure

The user stated plainly, before launch, that the campaign would not start
until Taboola answered the support ticket.

The plan written into CAMPAIGN.md said the opposite: that the bid strategy
should not be changed pre-emptively, that "the tell is spend", and that if
the campaign spent normally the concern was unfounded. That is advice to
launch with the fault open and watch what happens. The campaign launched on
that basis.

It was also described as "cosmetic" and as affecting only a reporting
column. That was wrong in one specific way that was foreseeable: a reporting
object that a bid strategy depends on is not cosmetic.

**The correct call was to switch the campaign to fixed CPC before launch, or
not to launch until the conversion rule existed.** Fixed CPC was proposed in
session and withdrawn as over-reaction. It was not an over-reaction.

## What to carry forward

1. **Check the vendor's funnel before buying traffic for it.** Walk the full
   path from hoplink to price page as a cold visitor. If there is a quiz,
   an email gate, or a survey before the price, assume cold paid traffic will
   not survive it. This is a five-minute check that would have saved the
   entire budget.
2. **Never run conversion-optimised bidding without a working conversion.**
   If the conversion cannot be created, use fixed CPC.
3. **Compare platform clicks to destination arrivals early.** A gap above
   roughly 20% means the traffic source is selling junk placements, and the
   fix is site blocking, not more budget.
4. **A stated precondition from the user is a hard gate.** "It won't start
   until I get a response" is not a preference to be reasoned around.

## Money

- Spent: £33
- Remaining of the £160: £127, unspent and still available
- Taboola will bill the £33 on 1 November, or sooner at a £100 threshold
  that will now not be reached
- Refund request filed against Case #01250920
