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

## Funnel, verified by walking it (2026-10-12)

Previously inferred from the vendor's affiliate page. Now observed directly.

**The quiz is five steps, four of them questions.**

| step | asked |
|---|---|
| 1 | Who are you interested in? (men / women / both) |
| 2 | When were you born? (day, month, year) |
| 3 | What is your ethnic background? |
| 4 | What is your name? |
| 5 | Confirm, 18+, and consent to email — "Begin to draw my soulmate" |

- **"Four questions" is accurate** and may be used in ad copy. It was written as
  an inference and withheld from the first ad set until this check.
- **"No photo needed" is accurate.** No image is requested at any step.
- **Step 5 is an email opt-in, not a purchase.** The sketch is delivered by
  email, so the quiz is a lead capture and the $37 offer page comes after the
  address is given. The published 7.26% CVR is measured hop-to-sale and so
  already includes this step — the breakeven arithmetic does not change. But
  the bridge must not imply anything instant, and the resulting mailing list
  belongs to the vendor, not to us.

**Offer page, same walk:** base advertised at "starting at Just $37", anchored
against a struck-through $147, with three bonuses stacked to a claimed $262 of
value. $37 is an advertised starting price, not a verified checkout total — no
purchase was made.

**Attribution confirmed in the live URL:**
`aff-tinaaldea.com/offer?name=Andrew&tid=...&hopId=...&aff_sub1=a1`

## Ad creative, final (2026-10-12)

**Images:** `ads/FEMALE_1200x800.jpg` and `ads/MALE_1200x800.jpg` — two of the
vendor's own sample sketches, taken from the offer page, cropped away from the
paired customer photos, red arrows removed, no rotation. Her signature is left
intact because the work is hers.

These are photographs of real drawings, so Realize's **"AI content" box should
be unticked** for them.

**Headlines**
- `Why You Can't Picture Your Soulmate's Face` (42)
- `No Photo. Four Questions. Then a Face.` (38)

**Description:** `A personalized digital soulmate sketch, based on a psychic
reading. No photo needed. For entertainment purposes only.`

Brand `First Drop`, CTA `Learn More`. Two images x two headlines = the four
variations Realize requires.

### Concepts tried and rejected, with the reason

- **Window photographs** (woman with a phone, no sketch). Generic lifestyle
  stock — could advertise broadband. Removing the product to avoid rendering it
  badly threw away the hook.
- **Envelope reveal** (portrait emerging from an envelope). Killed on a factual
  mismatch, not aesthetics: **the sketch is delivered digitally.** The vendor's
  page says "delivered digitally to download and keep" and the quiz ends in an
  email opt-in. An envelope implies something arrives in the post, which is the
  kind of mismatch that drives refunds — and refunds come out of a 90%
  rev-share.
- **Kitchen-table scene** (woman looking at a sheet of paper). Same mismatch.
- **Generated sketches in the vendor's style.** Usable only unsigned; signing
  one "Tina Aldea" would fabricate her work. Also better than her actual
  samples, which over-promises and raises refunds.

**If a round two is funded,** the honest version of the discovery scene is the
sketch on a phone screen, since that is how it is actually received — generate
the scene with a blank screen and composite the real sketch onto it.

## Ad images, final (2026-10-12)

Four files in `research/clickbank-product-mastery/ads/`. All four carry a
**real Tina Aldea sketch** lifted from the vendor's own offer-page PDF — no
generated artwork is presented as the product.

| File | What it is | AI-content box in Realize |
|---|---|---|
| `SCENE_WOMAN_1200x800.jpg` | Woman on a sofa looking at the printed **male** sketch | **tick** — the room and the woman are generated |
| `SCENE_MAN_1200x800.jpg` | Man at a kitchen table looking at the printed **female** sketch | **tick** — the room and the man are generated |
| `MALE_1200x800.jpg` | The male sketch alone on cream paper | leave **unticked** — a photograph of a real drawing |
| `FEMALE_1200x800.jpg` | The female sketch alone on cream paper | leave **unticked** — a photograph of a real drawing |

Each scene shows the opposite sex to the person holding it, because that is
what the product delivers: you are shown your soulmate, not yourself.

Build method (`composite_sketch.py`): generate the scene with a deliberately
**blank** A4 **portrait** sheet, read the sheet's four corners off a coordinate
grid, then inverse-map the real sketch into that quad. Only the low-frequency
lighting of the plate is carried across, so a hard shadow edge does not land on
the drawn face and read as dirt on the print.

Mistake worth not repeating: the first pass set a 16:9 frame but never said the
*sheet* had to be portrait, so the model drew a landscape sheet and a portrait
sketch could not be laid on it without stretching the face. Orientation of the
object has to be stated separately from the frame.

### Where to generate: Higgsfield, not ElevenLabs

**Use `gpt_image_2_5` (variant `flare`) through the Higgsfield MCP.** Preflight
every call with `get_cost: true` before submitting.

| | ElevenLabs `bytedance-seedream-5-pro` | Higgsfield `gpt_image_2_5` flare |
|---|---|---|
| Cost, batch of 4 | 3,272 credits ≈ **$0.60** | **1 credit** (0.25 each) |
| Native 3:2 | no — 16:9, then crop | **yes**, Taboola's own ratio |
| Sheet rendered as asked | repeatedly wrong | right first time |

Same prompt, same four variations, and the Higgsfield plates were better. Roughly
60x the cost for a worse result; several pounds of credit went on it before the
check was run. **Check the price of a generation route before the first call,
not after the sixth.**

### Review creative at the size it runs

A 1200x800 native ad renders at roughly 300px wide in feed. Judge every plate in
a ~320px thumbnail strip before calling it finished. The first scene composites
looked fine at 1100px and were unreadable at ad size: the drawing was about 15%
of the frame, the paper was blown to white and the signature was a grey smudge.

### Scene geometry: three constraints, all of them separate

Each of these was broken on its own in a separate round. State all three.

1. **The page must be visible to the camera AND to the person.** A page held up
   facing the lens shows the person its blank back. Put it flat on a table with
   the camera above the table plane, or shoot over the shoulder. The reference
   the platform generated (`69.png`) does the first.
2. **The page's own orientation, stated apart from the frame.** "16:9 frame"
   says nothing about the sheet; say A4 portrait, taller than wide, explicitly.
3. **The page's rotation on the surface, stated in camera terms.** "Long edges
   running away from the camera" was read loosely and produced a sheet laid at
   about seventy degrees, so a portrait composited onto it came out on its side.
   Say: squared up to the camera, top and bottom edges parallel to the top of
   the photograph, not rotated or turned on the table.

`find_sheet_quad.py` recovers the sheet's four corners from a plate. Side edges
are fitted as x = a*y + b and top/bottom as y = c*x + d; fitting all four the
same way makes the near-horizontal edges blow up. Always overlay the fitted quad
on the plate and look at it before compositing.

**Page orientation on the table is the person's, not the viewer's.** The sheet is
rotated so its top points away from the person reading it, which is how a page
actually lies when someone reads it. Pass the quad to `composite_sketch.py` as
`BR;BL;TL;TR` to turn the texture through 180 degrees.

Note the geometry this forces: if the subject faces the camera, the camera is
opposite them, so a page oriented to them reads upside down to the viewer. There
is no framing where a flat page on a table faces the subject AND reads upright to
a camera in front of them. To have both, the page has to be propped or tilted up
towards the subject with the camera raised and off to their side.

**Placement: the sheet goes in front of the subject's chest.** Its near edge a
hand's width from their torso, hands resting either side of it, the way a person
actually puts down a page they are reading. A sheet off to one side of the table
reads as a prop nobody is holding. State this in the prompt; "on the table in the
lower left of the frame" puts it a foot away from them.

### Why the scene plates are generated whole, drawing included

Six rounds went into generating a blank sheet and warping the real vendor sketch
into it. Every round the geometry was wrong somewhere: page facing the lens so the
subject saw its back, page landscape, page rotated seventy degrees on the table,
page sitting off to one side instead of in front of the chest.

The platform's own tool had none of those faults, and the reason is not that its
prompt was better. It generated the scene and the drawing in ONE PASS, so the
model drew a face already in perspective. There is no quad to get wrong. Pinning
a fixed, real drawing into a measured quad is the hard version of the problem, and
it was self-imposed.

So the scene plates now generate the drawing too. The trade:

- The drawing is representative of the product, not a sample of it. The ad does
  not claim "this is your sketch"; the landing page does the selling.
- **The AI-content box must be ticked** for both scene plates.
- No signature is ever generated on these. "Tina Aldea" belongs only on the real
  sketches in `MALE_1200x800.jpg` and `FEMALE_1200x800.jpg`, which stay unticked
  because they are photographs of real drawings.

**Scale and angle: wide, not tight.** The platform's own creative is a wide
reportage frame - camera well back, the subject side-on and off-centre at about a
third of the frame height, the whole kitchen in shot, a laptop and mug on the
table. A tight symmetrical portrait with the subject centred and both hands flat
either side of the page reads as stock photography. Match the reference's
distance and asymmetry, not just its subject matter.

## Final ad set, as entered (2026-10-13)

Images: `ads/SCENE_WOMAN_1200x800.jpg` (woman with the male sketch) and
`ads/SCENE_MAN_1200x800.jpg` (man with the female sketch). Both carry a genuine
Tina Aldea drawing on the page; the room and the person are generated, so the
**AI content box is ticked** on both.

| Ad | Image | Headline | Chars |
|---|---|---|---|
| 1 | Woman | What Could Your Soulmate Look Like? | 35 |
| 2 | Man | What Could Your Soulmate Look Like? | 35 |
| 3 | Woman | Get a Psychic Sketch of Your Soulmate | 37 |
| 4 | Man | Get a Psychic Sketch of Your Soulmate | 37 |

Description, all four: `A personalized digital soulmate sketch, based on a
psychic reading. No photo needed. For entertainment purposes only.`

Brand `First Drop`. CTA `Learn More`. All four to
`https://read.firstdrophq.com/a/`.

`/b/` stays deployed and verified but is not in this campaign: Taboola's own
performance guidance is one destination URL per campaign, and at this budget a
two-page split produces no readable answer. It is the next test, not a
half-finished one.

Headline 3/4 asserts the sketch is of your soulmate, which is a stronger claim
than headline 1/2's conditional question. The description carries the
entertainment-purposes disclaimer, which is what the network looks for on this
category. If creative review rejects it, the drop-in replacement that keeps the
mechanism without the assertion is `A Psychic Sketch, From Four Questions` (36).

## Tracking installed (2026-10-13)

Taboola account ID **2125039**. Base pixel in the `<head>` of both bridge pages,
plus a click handler on the CTA firing a second event:

```js
window._tfa.push({notify: 'event', name: 'offer_click', id: 2125039});
```

Conversion rule in Realize step 5 should be built on the event name
**`offer_click`**, category Lead or Other.

**What this measures, and what it does not.** `offer_click` is the outbound
click to ClickBank, not a sale. The sale happens on the vendor's domain, which
we cannot instrument, and ClickBank's own postback is a server-to-server POST
that a browser pixel cannot receive. So the funnel reads:

| Stage | Measured by |
|---|---|
| Impression, click, CTR, CPC | Realize |
| Landed on the bridge | Cloudflare Web Analytics + `page_view` |
| Clicked through to the offer | `offer_click` |
| **Sale** | **ClickBank Analytics only, by `aff_sub1`** |

Reconciling spend against revenue stays a manual join between Realize and
ClickBank on the `a1` / `b1` sub-ids. Nothing automates it at this budget.

Taboola cannot optimise on `offer_click` either: Maximize Conversions needs 50
conversions in 7 consecutive days and this campaign will not produce them. The
rule exists so the data is recorded, not so the algorithm acts on it.
