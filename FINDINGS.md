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

# Why the input pipeline cannot produce a viral output

This is a separate question from the one above, and it has a clean answer.
Source: the scraped tables and config in `HUP_Content_Factory`.

## The input contains no failures

Config gates, read directly:

| Key | Value |
|---|---|
| `bootstrap_vpy_floor` | 50000 |
| `youtube_min_views` | 50000 |
| `min_views` | 1000 |
| `min_engagement_rate` | 0.02 |
| `top_n_per_run` | 20 |

The observed result in the TikTok scrape: the lowest view count in the entire
pool is 65,900, and the median is 297,450.

Every post that ever enters the system is already a winner. That makes the
central question unanswerable by construction. Whatever the winners have in
common, the flops may have in common too, and there are no flops in the data
to check against. The pipeline can describe what viral posts look like. It
cannot identify what made them travel, because it has never seen a post that
didn't.

This is the same survivorship error that makes hook-analysis accounts
unfalsifiable. The difference is that this version is industrialised.

## The winners' reach is not transferable

Creators in the TikTok pool hold between 48,300 and 952,000 followers, median
301,300. A large share of a 297,000-view median is the audience those accounts
already had.

Copying the structure of such a post transfers the form and none of the
distribution. An account posting to almost nobody lands at the platform floor
regardless of how well the structure was cloned, which is exactly what the
271-view median shows.

## The scoring rewards signals too small to read

| Weight | Value |
|---|---|
| `score_weight_views` | 1.0 |
| `score_weight_likes` | 2.0 |
| `score_weight_comments` | 3.0 |
| `score_weight_reposts` | 3.5 |
| `score_weight_shares` | 4.0 |
| `score_weight_saves` | 4.0 |

Views are weighted lowest and saves and shares highest. On a 300,000 follower
account those signals are stable and that weighting is defensible. On an
account producing 250 to 1,200 views with zero to three saves per post, they
are noise, and the ranking amplifies noise fourfold over the one metric that
had range.

## The fix is configuration, not construction

The infrastructure needed to answer the question already exists. What is
missing is variance in the outcome.

1. Drop the view floors and the top-N cut. Scrape full recent histories from
   the same tracked creators rather than their best posts.
2. Compare each creator's own best posts against their own worst. This holds
   follower count and audience constant, so the difference that remains is
   attributable to the post rather than the account.
3. Score by views alone until the account has the volume to make saves and
   shares stable.

That comparison is a real experiment, it is the first one this system would
have run, and it produces exactly the kind of checkable finding that is worth
publishing and selling.
