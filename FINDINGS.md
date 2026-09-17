# What the humanupgradehq data says

Source: `HUP_Content_Factory`, read 2026-09-17. 139 own-post performance
snapshots covering 134 distinct posts published 2026-07-12 to 2026-08-15.
Every row was marked `analysis_status: pending`. Nobody had read them.

Parsed in full for structure and metrics. Caption text was read for the top
and bottom performing posts only.

## The month in numbers

| Platform | Posts | Total views | Likes | Comments | Shares | Saves |
|---|---|---|---|---|---|---|
| TikTok | 45 | 16,330 | 344 | 7 | 6 | 42 |
| Instagram | 44 | 77 | 31 | 0 | 0 | 0 |
| Third platform | 50 | 1 | 0 | 0 | 0 | 0 |

TikTok median is 271 views, which is roughly the floor the platform gives any
post. Best post reached 1,258. Six shares across 45 posts is a share rate of
0.04%, and likes outnumber shares 57 to 1.

## What separates the winners

Comparing the top and bottom twelve TikTok posts.

| | Top 12 | Bottom 12 |
|---|---|---|
| Median views | 382 | 250 |
| Median caption length | 440 chars | 1,870 chars |
| Contains a question | 9 of 12 | 4 of 12 |
| Median uses of "you" | 5 | 2 |
| Posting hours | identical | identical |

**Specific beats abstract, by four to five times.** Every top post opens with
a concrete second-person situation: "You keep repeating the same relationship
or career mistakes", "You tense up when someone comes home". Every bottom post
opens with an abstract third-person generality about progress or change:
"Most progress doesn't grab headlines".

**Short beats long.** The losing captions are four times longer.

**Timing is not a factor.** Both groups posted at the same hours. Any theory
about posting time is dead.

**The generator is producing near-duplicates.** Seven of the bottom twelve are
the same vague statement about quiet progress, rewritten. They reliably land
in the 240 to 260 floor. This is the single clearest defect in the pipeline.

## Why the ranking never showed any of this

The setup scores every metric and combines them into `weighted_score`. That
composite is the reason a month of data looked like noise.

It barely tracks reach. Rank correlation against views is +0.25. Against saves
it is +0.76 and against likes +0.75. The composite is mostly measuring likes
and saves while ignoring how far a post travelled.

The clearest case in the data:

| Views | Likes | Saves | Composite score |
|---|---|---|---|
| 944 | 1 | 0 | 1 |
| 299 | 4 | 3 | 19 |

The composite ranked the 299-view post nineteen times higher than the
944-view post. Only four of the top ten posts by views appear in the top ten
by score. Anyone steering content by that number would have been pushed
towards the weaker posts and away from the stronger ones.

It also cannot rank. There are 20 distinct score values across 45 posts, and
38 of those posts share a score with another post.

The cause is scale. Views ranged from 240 to 1,258, a fivefold spread with
real signal in it. Likes ranged from 0 to 14 and shares from 0 to about 2. At
that volume the engagement counts are noise, and a composite built on them
inherits the noise while drowning out the one metric that had range.

**At this stage, rank by views alone.** Composites are for when every input
has enough volume to be stable. Blending five metrics into one number destroys
the ability to attribute a result to any cause, which is precisely the
complaint that the results were unexplainable.

## Two things that need checking

Instagram reports zero views on 43 of 44 posts while still recording likes.
That is more likely a metrics capture gap for the post type than a publishing
failure, but it has not been verified and it means Instagram is currently
unmeasurable.

The third platform recorded one view across 50 posts. Either publishing is
failing silently or the metrics are not being captured at all.

## What this changes

The pipeline works. It published 134 posts in a month and recorded what
happened. The content strategy is what failed, which is the cheaper of the two
problems to have.

The niche is the deeper issue. General-audience pop psychology is the
low-intent category: high competition, no purchase intent, nothing to sell at
the end of it. Six shares in a month is the market answering clearly. Fixing
caption length inside this niche optimises toward a ceiling that is still
too low to matter.

Carry the two findings that transfer, concrete second-person openers and short
captions, into the automation niche. Both already match the caption structure
built into the renderer.

And read the snapshots this time. The loop exists. It has never been closed.
