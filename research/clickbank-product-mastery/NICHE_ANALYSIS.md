# What actually performs in this niche

Pulled 2026-10-12: sixteen Instagram and TikTok posts that substantially
outperformed their own creator's median, in the soulmate / psychic / manifestation
space. Structural patterns only — no content lifted.

## The finding that matters most: small accounts break out here

This niche does not gate reach behind follower count.

| account | followers | views | vs own median |
|---|---|---|---|
| @visions_with_liv | 2,600 | 769,400 | **593×** |
| @ezreal018 | 702 | 762,900 | 8.2× |
| @averkhaya | 8,900 | 1,100,000 | 77× |
| @astrologerfreya | 11,000 | 2,700,000 | **1,960×** |
| @chinglung._.p | 4,700 | 1,000,000 | 10.5× |

A 702-follower account did three quarters of a million views. That is the direct
answer to the worry about dreamreach.x being new, and it is better news than I
gave: **the constraint is the content, not the account age.**

## Six patterns across the outliers

**1. Second person, diagnostic, about the viewer.**
Not "most people feel X" but "you are currently in X". The hooks read as
verdicts on the viewer's own life: *"You are currently in a confusing situation
with your person."* *"Person that you have had strong feelings for lately."*
*"If you have a fear of being seen, you have a powerful psychic gift."*

**2. A prop in the first three seconds that doesn't make sense yet.**
Red underwear being tucked into a pillowcase. Coffee grounds poured onto a white
plate. A kangaroo figurine pressed into pink salt. A line of leaves set on fire
in a hallway. The viewer stays to find out what the object is for. Atmosphere is
not a substitute for this — the object has to be concrete and slightly absurd.

**3. The "check yourself" mechanic is the strongest single format.**
The same premise — a mark on the palm indicating psychic ability — appears twice
in the top sixteen, from unrelated creators:

- @anterra.eve, 93K followers: **2.4M views, 408× median**
- @stevenaitchisonbooks, 31K followers: **2.3M views, 900× median**

Two creators, one premise, both enormous. It works because the viewer physically
gets up, looks at their own hand, and then comments what they found. It converts
watching into doing, and doing into commenting.

**4. Production value is irrelevant, but a human is not.** *(corrected 2026-10-12
 — see "The error in pattern 4" below.)*
Almost every entry is logged as "within an hour", static camera, low visual
change. Nobody is winning on craft. But "static camera" means the camera does
not move while **a person sits in front of it talking**. It does not mean a
still image.

**5. Explicit engagement instructions, crudely stated.**
"Click here to activate this blessing." "Save this to lock it in." "Comment to
seal it." Inelegant, and it is doing the work — this is how these posts get the
comment velocity that compounds distribution.

**6. Length is not a constraint.**
Winners run from 15 seconds to 823 seconds. A 9-minute tarot reading pulled 1.5M.
Short-form discipline is not what is being rewarded; holding attention is.

## Useful compliance note

@alexandra_mclash1 opens her caption with **"FOR ENTERTAINMENT PURPOSES ONLY"**
and the post did 1.4M views. The disclaimer the vendor's terms require does not
appear to cost reach in this niche — it is normal here.

## Where this leaves VIDEOS.md

The five scripts already written are wrong, in a specific and fixable way. They
are third-person, reflective, atmospheric, propless, and they ask a question
rather than hand the viewer a verdict. Against this data they would be quiet.

What they need:

- **Second person throughout.** Tell the viewer something about themselves.
- **A concrete object on screen in the first second.** Not an empty chair.
- **At least one script built on the "check yourself" mechanic**, pointed at the
  face premise rather than at palmistry — the thing a viewer can test on
  themselves and report back.
- **A blunt engagement instruction**, not a literary closing question.

What they keep:

- No link, no product, no affiliate mention while the account is new.
- The five-different-formats structure, so the test identifies a shape and not
  just a topic.
- The kill rule: five videos, none clearing 10,000 views, stop.


---

## The error in pattern 4 (found 2026-10-12, after five videos were built wrong)

I read two metadata fields wrong and built the five videos in `VIDEOS.md` to a
format that does not appear anywhere in this data.

- `visual_changes: Low (static camera)` — I read as "static image". It means the
  camera is locked off while a person performs in front of it.
- `style: Faceless text-on-screen` — I read as "no human present". On the one
  in-niche post carrying that label, a person is still partially in frame.

I never watched a single one of these videos. `vidiq_watch_shortform_content`
was available the whole time. **Do not log a format claim in this file again
without having watched the post.**

### Second pull, run deliberately biased toward faceless formats

Query: *"no person on camera — text on screen, objects, hands only, voiceover
over b-roll"*, format embedding, 100K+ views. Seven of the eight Instagram
results have a person on camera anyway.

| format | in this niche? | needs a human? | evidence |
|---|---|---|---|
| Talking head holding a real prop | yes, dominant | **yes, face** | @floralspirittarot 1.2M on 7.3K followers (276×); @_austinbecker_ 846K on 4.7K (458×); @rashitarot, @luna_starseed, @kiki.kennedy |
| Hands-only with a real prop, locked-off phone | yes | **hands, no face** | @juliannfrostt 1.3M — hook is a close-up of hands pouring pink salt; @iivymooon 923K (206×) — hook is hands pouring powder on a car floor |
| Static background + long cold-read text block + a recognisable song, **no voiceover** | yes, one case | no | @chinglung._.p — 1M views on 4.7K followers, 10.5× median, *Fast Car* by Tracy Chapman |
| Ambient b-roll + one line of text + trending song, 6–10s | **no** — relationship quotes, different niche | no | @thingsineversaid94 724K; @vanessadarling777_ 1.1M |

### What this kills

The five videos in `build/`. A 26–33 second AI-generated still with a calm
voiceover and two text cards matches nothing in either pull. The one faceless
in-niche winner has **no voiceover at all** — it is read, not listened to, and
the song does the emotional work.

### What it leaves

1. **Hands-only with real objects, filmed on a phone.** Matches the second row
   above, which includes two of the biggest numbers in the sample. Requires
   someone to physically film; requires no face. The existing voiceovers can sit
   over it. Cheapest real option.
2. **The text-block format.** Fully buildable with no filming and no camera, and
   it has a 1M-view data point on a 4.7K-follower account. Drop the voiceovers,
   drop the hook/end cards, write a long cold-read text block, use a recognisable
   song from Instagram's in-app library.
3. **AI talking head / avatar.** Structurally matches the dominant format without
   filming. **No evidence either way** — no AI-avatar account appears anywhere in
   either pull. Untested, and logged here as untested rather than recommended.
