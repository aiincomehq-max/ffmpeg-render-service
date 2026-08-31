# SCRIPTWRITER FACTORY — PHASE 0: DISCOVERY AND ARCHITECTURE

**Project:** Scriptwriter Factory (isolated lane)
**Phase:** 0 — Commercial + Technical Discovery
**Prepared by:** Claude Code (Builder / Engineer)
**For:** The Chairman
**Date:** 31 August 2026
**Status:** Discovery complete. No production built. No spend incurred. No external accounts created. No content published.

---

## 0. HOW TO READ THIS DOCUMENT

Every substantive claim is tagged:

| Tag | Meaning |
|---|---|
| **[FACT]** | A statement reported by a cited source. See the evidence-integrity caveat below. |
| **[INFERENCE]** | My reasoning from one or more facts. Could be wrong. Reasoning is shown. |
| **[PROPOSAL]** | A design or commercial recommendation. Not evidence. Requires Chairman decision. |
| **[UNKNOWN]** | An open question I could not resolve in Phase 0. Named, not hidden. |

### 0.1 Evidence-integrity caveat — READ THIS FIRST

**[FACT]** This session's execution environment blocked all direct outbound HTTP fetches. Every attempt to retrieve a primary source returned `403` at the network egress proxy (verified against `developers.google.com`, `themoviedb.org`, `docs.n8n.io`, `prsformusic.com`, `variety.com`).

**Consequence:** *All* evidence below was obtained through a search tool that returns search-engine result summaries. I read **no primary document in full**. I therefore grade evidence:

| Grade | Meaning |
|---|---|
| **E1** | Statement attributed to an official/primary body (regulator, PRO, platform ToS, government) and reported consistently. High confidence, still unverified against the primary text. |
| **E2** | Reported by established trade press or a specialist outlet. Moderate confidence. |
| **E3** | Reported by a single commercial/SEO-driven secondary source. **Low confidence — treat as a lead, not a fact.** Prices and platform policies in this grade are especially prone to being stale or wrong. |

**No commercial decision, and no spend, should rest on an E3 item without primary verification.** Primary-source verification of every E1/E2/E3 item in the Decision Register (§14) is a mandatory Phase 1 gate. I have not fabricated any figure, source or URL; where I could not find evidence I have written **[UNKNOWN]**.

---

## 1. EXECUTIVE CONCLUSION

**The single most important finding of Phase 0 is that the Factory's founding assumption is inverted by the evidence.**

The mission assumes the hard part is *production* — that if we can generate screenplays and music at scale, commercialisation follows. The evidence says the opposite:

**[INFERENCE]** **Production cost has collapsed to approximately zero. The binding constraints are (a) rights defensibility and (b) channel access — and the evidence shows both tightening specifically and deliberately against automated output during 2025–2026.**

The supporting arithmetic is stark. A complete television pilot package — research dossier, treatment, series architecture, six episode outlines, a 60-page pilot screenplay, three critique passes — costs roughly **$11–30 in model tokens** (§11). A creator-music track costs roughly **$0.05–0.25** to generate (§11). At those prices, "generate 10,000 assets" is trivially affordable and therefore **worthless as a competitive position**. Everyone can do it. Many already are: Deezer reported identifying **~75,000 fully AI-generated tracks per day by April 2026, approximately 44% of all daily uploads** [E2, §6.3].

Meanwhile, the three gates that actually matter have closed or narrowed:

1. **Copyright.** The US Copyright Office concluded that prompting alone — "even using complex and multiple prompts" — does not confer copyright in the output [E1, §7.1]. The UK Government's March 2026 report proposed **removing** s9(3) CDPA, the provision that currently protects computer-generated works with no human author [E1, §7.2]. **An unsupervised machine-generated property may be an asset we do not own and cannot stop others from copying.**

2. **Contract.** The 2023 WGA Minimum Basic Agreement provides that generative AI is not a writer and that nothing it produces constitutes literary material [E2, §8.1]. PRS for Music policy states that AI-generated works **cannot be registered**; only *AI-assisted* works with substantial human contribution may be [E1, §7.3].

3. **Channel.** Netflix accepts submissions only via licensed literary agents or pre-existing industry relationships [E1/E2, §8.1]. Coverfly — the largest screenplay aggregator — **shut down in August 2025** [E2, §8.1]. Epidemic Sound, the dominant creator-music platform, **does not accept AI-generated music from contributors and states it has no plans to change** [E2, §8.3]. Envato/AudioJungle prohibits AI-generated content as the main component of a submission [E3, §8.3].

**These three gates all point in the same direction, and it is a constructive direction.** Every one of them is passable by the same key: **substantial, documented, human authorship.** The Chairman's creative contribution is not a nice-to-have in this system — under USCO guidance, PRS policy, and every commercially relevant contract, it is *the thing that makes the property an asset at all*. The provenance infrastructure specified in §7 of the mission is therefore not "foundational infrastructure, not an afterthought" — it is the **product**. The evidence record proving human authorship may be worth more than the draft it attaches to.

### 1.1 Recommendation

**[PROPOSAL]** Build **Phase 1 as the Demand Intelligence Engine only.** No creative generation. No distribution. No submissions. Rationale:

- It is the one component whose value is **not** commoditised by cheap generation. Knowing *which* opportunity to pursue is scarce; producing the asset is not.
- It is lawful, low-cost (~£40–70/month, §11), reversible, and creates no rights exposure.
- It produces something immediately useful to the Chairman **whether or not** the Factory ever generates a line of script — a live, evidenced map of where demand actually is.
- It defers every unresolved legal and commercial question (§14) until we have evidence with which to answer them.

**[PROPOSAL]** **Do not build an autonomous IP production factory.** Build a **governed development instrument for a human principal** — one that finds opportunities, assembles research, drafts against explicit human creative direction, and records provenance to an evidential standard. This is a narrower claim than the mission's, and I flag the divergence explicitly for the Chairman's decision (§14, D-01). Everything in §§3–10 is designed so that either reading can be built from the same foundation; the difference is where the human sits, not what the pipes look like.

### 1.2 Arm viability at a glance

| Arm | Verdict | Confidence | Binding constraint |
|---|---|---|---|
| **A — Film & TV** | Viable **only** as human-authored development support. Not viable as autonomous production. | High | Channel access requires representation; WGA MBA excludes AI-authored literary material |
| **B — Songs / Artist Material** | **Lowest priority. Recommend deferral.** | High | Cuts come via relationships, not cold pitch; PRS will not register AI-generated works |
| **C — Creator Music** | Viable **only** via direct/own-channel licensing with explicit AI disclosure. Established libraries largely closed. | Medium | Contributor bans + severe commodity glut (~44% of daily uploads AI) |

---

## 2. COMMERCIAL FEASIBILITY BY ARM

### 2.1 ARM A — FILM & TELEVISION

#### Market conditions

**[FACT, E2]** Scripted commissioning has contracted roughly **25% since the ~2022 peak of TV**. ([Variety, MIP London takeaways](https://variety.com/2026/tv/global/5-takeaways-from-the-ampere-analysis-at-mip-london-broadcasters-more-important-than-ever-youtube-as-a-growing-destination-for-factual-sports-boost-1236670993/))

**[FACT, E2]** Ampere Analysis (presented by research manager Olivia Deane at Series Mania, March 2026) found there were only **2% fewer Western European scripted commissions announced in 2025 than in 2020**, but they now take on average **40% longer to make**. Ampere's framing: the bottleneck is production *speed*, not commissioning volume. ([Variety](https://variety.com/2026/global/spotlight/post-peak-tv-supply-chain-crunch-ampere-analysis-1236696837/))

**[FACT, E2]** In the same research: asked to name their favourite genre globally, consumers put **crime and thriller top at 11%**; romance came last at 6%. Yet romance was the only genre with positive acquisition growth 2024→2025, up 18%. ([Variety](https://variety.com/2026/global/spotlight/post-peak-tv-supply-chain-crunch-ampere-analysis-1236696837/))

**[FACT, E2]** Scripted titles accounted for **83% of first-run romance commissions in H1 2026**; first-run book adaptations rose **73%** between the 12-month periods covering late 2023–early 2024 and late 2025–early 2026. ([Broadband TV News](https://www.broadbandtvnews.com/2026/06/29/streamers-shift-towards-scripted-romance-as-reality-dating-shows-decline/))

**[FACT, E2]** UK-specific (Ampere, 2023 data, published March 2024): the BBC greenlit **129 of 256** UK scripted shows; UK scripted commissions fell **18%**; within BBC commissions, **crime and thriller titles were up 16%** while comedy fell 27%. ([Deadline](https://deadline.com/2024/03/bbc-scripted-research-ampere-analysis-1235867117/), [Televisual](https://www.televisual.com/news/bbc-orders-half-of-all-uk-2023-scripted-commissions-says-report/))

**[FACT, E2]** True crime: Ampere reports true crime was **16% of all documentary commissions worldwide in 2025** (up from 15%), **632 new crime documentary commissions** across 22 markets — but trade reporting notes the commissioning frenzy "has matured," with one production executive describing a fall from 9-of-12 to 3-of-8 simultaneous true-crime productions. UK and US remain dominant; BBC and Channel 5 the top UK commissioners. ([C21Media](https://www.c21media.net/marketplace/truecrimeandinvestigation26/))

**[FACT, E1/E2]** Ofcom *Media Nations 2026* (published 29 July 2026): Netflix is first choice for **26%** of UK viewers vs BBC **25%**; SVOD household penetration **70% in Q1 2026** — only 2pp above 2021, i.e. plateaued; SVOD revenues **£5.17bn in 2025**, up 18% YoY. ([Ofcom](https://www.ofcom.org.uk/media-use-and-attitudes/media-habits-adults/media-nations-2026), [Broadband TV News](https://www.broadbandtvnews.com/2026/07/29/netflix-overtakes-bbc-as-uk-viewers-first-choice-says-ofcom/))

#### [INFERENCE] What this means for the Factory

The Chairman's instinct toward crime/thriller territory is **evidentially supported on the audience side** (top genre at 11%) but **is the most competed space on the supply side**. That is the classic trap the scoring model in §4 exists to detect: high audience demand and high saturation are different axes, and a naive "crime is popular" heuristic scores the *worst* opportunities highest.

The Ampere supply-crunch finding is the more actionable signal. If commissions are roughly flat but take 40% longer to produce, the scarce resource is **production-ready material** — projects that are de-risked, clearly budgeted, and fast to make. **[INFERENCE]** This favours *contained, feasible, low-cast-count* propositions over sprawling ones, and it means "production feasibility" deserves far more weight in the scoring model than a demand-first model would naturally give it. I have weighted it accordingly in §4.

**[INFERENCE]** The romance/adaptation growth figures are a live counter-example to the Chairman's genre assumption and exactly the kind of finding the mission asked the system to surface rather than suppress. I surface it without recommending we chase it: single-year acquisition growth in one genre is weak evidence for a multi-year development bet.

#### Route to market — the binding constraint

**[FACT, E1]** Netflix accepts submissions **only** through a licensed literary agent, or from a producer, attorney, manager or executive with a pre-existing relationship. Anything else is an unsolicited submission and will not be accepted. ([Netflix Help Centre](https://help.netflix.com/en/node/100386))

**[FACT, E2]** **Coverfly shut down on 1 August 2025**, along with sibling platforms The Tracking Board, ScreenCraft, The Script Lab and WeScreenplay. This removed the largest free aggregation/discovery layer between unrepresented writers and the industry. ([IndieWire](https://www.indiewire.com/features/commentary/coverfly-shutting-down-screenplay-industrial-complex-1235120359/), [No Film School](https://nofilmschool.com/coverfly-is-shutting-down))

**[FACT, E3]** The Black List website: **$30/month hosting**, **$100 per feature evaluation**; a "real run" (six months' hosting plus two evaluations) ≈ **$380 per script**. A score of 8+ promotes the script and triggers an industry email. ([storynotes.app](https://www.storynotes.app/blog/black-list-2026-pricing-explained))

**[FACT, E3]** InkTip: **InkTip Pro $32.50/month**; additional listings $12.50/month; standalone listing $19.99/month. Free for qualified filmmakers to search. ([InkTip](https://www.inktip.com/sa_services_products.php))

**[FACT, E3]** Virtual Pitch Fest: tiered, ~**$6.52–7.86 per pitch** ($55/7, $90/12, $189/29). Stage 32 pitch sessions ~**$30 per pitch**. ([Virtual Pitch Fest](https://www.virtualpitchfest.com/), [Stage 32](https://www.stage32.com/happy-writers/pitch-sessions))

**[FACT, E2]** BBC Writersroom operates time-boxed Open Call windows (~5 weeks) for unsolicited scripts rather than continuous submission. ([London Playwrights](https://londonplaywrightsblog.com/bbc-writersroom-script-room-10-now-open-for-drama-submissions/))

**[FACT, E2]** Academy Nicholl Fellowships: up to five **$35,000** fellowships annually; as of the 2024 contest **24 winning scripts had later been produced**. 2025–2026 recipients announced March 2026. ([Academy Press Office](https://press.oscars.org/news/academy-announces-2025-2026-nicholl-fellowships-screenwriting), [Deadline](https://deadline.com/2026/03/movie-academy-2025-2026-nicholl-fellowships-winners-1236763373/))

**[FACT, E3]** Option economics: option fees are commonly ~**10% of the agreed purchase price**, for a 12–24 month exclusive period, offset against the purchase price on exercise; extension fees typically not offset. ([filmandink](https://filmandink.com/2025/08/27/a-beginners-guide-to-option-purchase-agreements-in-film-and-tv/), [Practical Law](https://uk.practicallaw.thomsonreuters.com/1-504-5111))

**[FACT, E2]** For scale: BBC agreement minimums have been reported at **£12,900 per 60 minutes** for series, £9,360 for dramatisations, £5,760 for adaptations. **[UNKNOWN]** Current PACT/WGGB minimum rates for 2026 — I could not source them and will not estimate. ([Deadline](https://deadline.com/2024/03/bbc-show-writers-pay-rise-residuals-1235842854/))

#### The disqualifying finding

**[FACT, E2]** The 2023 WGA Minimum Basic Agreement provides that **AI cannot write or rewrite literary material**, and per the WGA's own summary, **generative AI is not a writer, so nothing it produces counts as literary material**. Companies cannot require writers to use AI tools and must disclose AI-generated material given to a writer. A tentative four-year deal reached **4 April 2026** adds compensation where studios train AI on member scripts. ([Bloomberg Law](https://news.bloomberglaw.com/ip-law/writers-guild-ai-deal-pushes-studios-down-new-copyright-path), [Variety](https://variety.com/2026/film/news/wga-ai-training-amptp-talks-1236684012/), [Collider](https://collider.com/wga-ai-written-movies/))

**[INFERENCE]** Combine the four findings — no unsolicited route without representation; the aggregation layer gone; the guild framework excluding AI-authored literary material; and (§7) no copyright in prompt-only output — and the conclusion is not marginal. **An autonomous screenplay-generation factory has no lawful, contractually-permitted, commercially-accessible route to a professional buyer.** Paid marketplaces (Black List, InkTip, pitch fests) remain open and would take our money, but they are a **cost centre priced per script**, which means the strategy's economics get *worse* with volume, not better — the exact inverse of a factory. At Black List rates, 100 scripts is ~£30,000 of hosting and evaluation fees with no evidenced conversion mechanism.

**[PROPOSAL]** Arm A proceeds as **demand intelligence + human-authored development**, targeting UK independent producers and open-call routes (BBC Writersroom, Nicholl, 4Screenwriting) where the Chairman is the credited author with documented authorship. Volume is explicitly *not* the strategy: one strong, genuinely human-authored, well-evidenced property beats one hundred machine drafts, because only the former can be submitted, registered, or defended.

---

### 2.2 ARM B — SONGS / ARTIST MATERIAL

**[FACT, E1]** PRS for Music policy (v1, October 2025): **AI-generated works cannot be registered with PRS for Music.** Works meeting the definition of *AI-assisted* may be registered; the creator must ensure eligibility and, where appropriate, **evidence the extent and influence of their contribution**. ([PRS for Music AI Policy PDF](https://www.prsformusic.com/-/media/files/prs-for-music/works/prs-for-music-and-artificial-intelligence-policy.pdf))

**[FACT, E2/E3]** Route reality: most songs that get cut come through **publisher relationships and co-writing sessions, not cold pitches**. Publishers circulate briefs specifying tempo, vibe, lyrical theme and reference tracks; brief aggregators include Music Gateway, TAXI and Songtradr. Paid pitch routes exist (e.g. Discover Sooner "Monthly Pitch" reported at $17/month rising to $21/month from 1 August 2026; SongU Fast-Track/Street Pitch). ([Orphiq](https://orphiq.com/resources/songwriter-pitching-guide), [Discover Sooner](https://www.discoversooner.com/monthly-pitch), [SongU](https://www.songu.com/pitchingOpps.aspx))

**[FACT, E3]** Songtradr operates freemium: free account retains **60%** of a sync fee; top paid tier (~**$49/year**) retains **80%**. ([Music Industry How To](https://www.musicindustryhowto.com/songtradr-review/))

**[FACT, E2/E3]** Identifiers: **ISWCs are free** from PROs; ISRCs are issued free by most distributors, with PPL the UK national ISRC agency for direct registrants. ([Davincii](https://davincii.co/guides/iswc), [Buzzsonic](https://buzzsonic.com/resource/ppl-uk-isrc-registration/))

**[INFERENCE]** Arm B is the **weakest** of the three and I recommend deferring it. Its value chain depends almost entirely on relationship capital — A&R trust, co-writing rooms, publisher briefs — which is precisely the input an automated factory cannot manufacture and the mission's doctrine (§8: "do not treat vanity exposure as evidence of commercial value") correctly refuses to fake. Layer on the PRS registration bar and a paid-pitch layer whose conversion rate is undocumented, and Arm B consumes governance attention disproportionate to its evidenced opportunity.

**[PROPOSAL]** **Defer Arm B entirely** until Arm A or C has produced at least one evidenced commercial outcome. Reassess then. If the Chairman wishes to keep a foothold, the minimum viable version is *demand intelligence only* — harvesting public publisher briefs into the same Sheets/Drive spine — at near-zero marginal cost, with no generation and no submission.

---

### 2.3 ARM C — CREATOR MUSIC

#### Market

**[FACT, E3]** Royalty-free music licensing market valued at **~USD 1.5bn in 2025**, projected to **USD 3.2bn by 2034** (CAGR ~9.2%). ([Verified Market Reports](https://www.verifiedmarketreports.com/product/royalty-free-music-licensing-market/)) **[INFERENCE]** Third-party market-sizing reports of this type are marketing collateral; treat the *direction* as informative and the *figures* as unreliable.

**[FACT, E2]** Epidemic Sound pays artists a fixed fee of **USD $2,000–$8,000 per track** (Q1 2026), paid before the track is made available and **not recouped**; splits streaming royalties 50/50; and operates a yearly Soundtrack Bonus (~**$4.2m in 2026**). ([Epidemic Sound](https://corporate.epidemicsound.com/about-us/how-we-work-with-artists/))

**[INFERENCE]** That per-track fee range is the clearest evidence in this document of what a *human-composed, platform-accepted* creator-music track is worth to the dominant buyer. It is also the number our arm cannot access — see below.

#### The two blocking findings

**[FACT, E2/E3]** **Epidemic Sound does not accept AI-generated music from contributors and has stated it has no plans to change** — an explicitly "human-first" catalogue policy, with AI confined to its own tools (Adapt, Voices) for which it pays contributing humans from dedicated pools. ([Epidemic Sound commitments](https://www.epidemicsound.com/blog/our-commitments-to-artists-and-content-creators-in-the-ai-paradigm/), [Dynamoi](https://dynamoi.com/learn/ai-music-distribution/does-epidemic-sound-accept-ai-music))

**[FACT, E3]** **Envato/AudioJungle prohibits AI-generated content as the main component of a submission.** Artlist is reported to exclude AI contributions through its contributor requirements while itself shipping an AI music generator. Pond5 is reported to require **mandatory AI disclosure** rather than imposing a ban, treating undisclosed AI uploads and models trained on unlicensed copyrighted data as high copyright-risk. **Sources materially conflict on all three platforms.** ([Dynamoi](https://dynamoi.com/learn/ai-music-distribution/stock-music-sites-that-accept-ai-generated-music), [Last Play Distro](https://lastplaydistro.com/blog/pond5-ai-generated-music-policy-2025-complete-guide-for-creators))

**[FACT, E2]** **Deezer** deployed AI detection (rolled out 24 January 2025) and by **April 2026 was identifying ~75,000 fully AI-generated tracks per day — approximately 44% of all daily uploads**; flagged tracks are tagged and kept out of algorithmic recommendations and editorial playlists. **Spotify** updated policy in September 2025, adopting DDEX AI disclosure in credits, stating it does **not** down-rank music for being AI-assisted, and reporting removal of **more than 75 million spam tracks** in the prior year via a filter targeting mass uploads, duplicated titles and ultra-short filler. ([aimusicpreneur](https://www.aimusicpreneur.com/ai-music-news/spotify-no-ai-music-filter-deezer-toggle-2026/), [TechCrunch](https://techcrunch.com/2025/09/25/spotify-updates-ai-policy-to-label-tracks-cut-down-on-spam/))

**[INFERENCE]** The 44% figure is the most commercially significant number in this document. It says the *exact strategy* Arm C would naturally adopt — generate large volumes of instrumental beds and push them into catalogues — is already being executed at industrial scale by thousands of others, and platforms have built detection and demotion machinery in direct response. **We would be a late entrant into a commodity glut, competing on the one axis (volume) where we have no advantage.** Spotify's "we don't down-rank AI-assisted music" is not the reassurance it appears to be: it sits beside a 75-million-track spam purge, and the operative distinction is between *disclosed, non-spammy, AI-assisted* output and *bulk automated* output. A factory optimising for volume lands on the wrong side of that line by construction.

#### The open routes

**[FACT, E2/E3]** **TikTok Commercial Music Library**: a pre-cleared catalogue of 1m+ tracks for brands, free to any TikTok Business Account, cleared for organic brand posts and paid TikTok ads. Artists request CML opt-in through a participating distributor (DistroKid, Believe, Vydia) or SoundOn. **The licence covers TikTok placements only.** TikTok does not publish a universal artist payout rate. ([TikTok Ads Help](https://ads.tiktok.com/help/article/how-to-use-the-commercial-music-library), [Velveteen](https://www.velveteen.fm/guides/tiktok-for-musicians/tiktok-commercial-music-library-explained))

**[INFERENCE]** This directly validates the Chairman's stated caution. Uploading a sound to TikTok confers **no multi-platform commercial rights on third parties** — the mission's instruction not to assume otherwise is correct, and the CML is a *TikTok-scoped* licence, not a general one. Any social presence we build is a **marketing funnel to a licence we issue ourselves**, never the licence itself.

**[FACT, E1/E2]** **DDEX** is now the industry-standard channel for AI declarations, carried in release metadata; distributors have added an AI checkbox that embeds the declaration in the delivery to platforms. ([Undetectr](https://undetectr.com/blog/ddex-ai-disclosure-standard-explained))

**[PROPOSAL]** Arm C, if pursued at all, proceeds on a **narrow, disclosed, direct-licensing** basis:
- **Disclose AI involvement everywhere, by default and without exception** — DDEX flags, catalogue metadata, our own licence terms. This is both the EU AI Act direction of travel (§7.4) and the only posture that survives platform enforcement.
- **Do not** attempt Epidemic Sound or Envato — their terms exclude us.
- **Do** treat Pond5 (disclosure-based) as a candidate route **only after** primary verification of its current contributor terms.
- **Prefer our own direct-licensing channel**, where we set licence scope, territory and term explicitly, and where no third party's contributor policy can close the route overnight.
- Compete on **curation, coherence and licence clarity** — a small, deliberately-designed, cleanly-documented catalogue — not on volume. Volume is the commodity; provenance is not.

---

## 3. DEMAND-SOURCE INVENTORY

Legality note: everything below is public or officially-provisioned. **[PROPOSAL]** Standing rules for the Factory: obey `robots.txt`; use official APIs and RSS wherever they exist; identify our agent honestly; rate-limit conservatively; store **source URL + retrieval timestamp + verbatim excerpt** for every claim; never ingest copyrighted creative works (screenplays, lyrics, compositions) for the purpose of paraphrase or derivation.

### 3.1 Film & TV

| Source | Type | Access | Grade | Notes |
|---|---|---|---|---|
| Broadcast, Televisual, Deadline, Variety, C21Media, Screen Daily | Trade press | RSS / public pages | E2 | Primary commissioning-announcement signal. Several are paywalled — headline/RSS only. |
| Ampere Analysis press page | Analyst | Public releases | E2 | Free press releases carry usable aggregate figures; full data is paid. **[UNKNOWN]** licence cost. |
| Ofcom *Media Nations* | Regulator | Free PDF, annual | **E1** | Authoritative UK audience/market data. |
| BFI Research & Statistics | Public body | Free | **E1** | UK production volume, spend, genre. |
| BBC Writersroom / Channel 4 / ITV commissioning pages | Buyer | Public pages | **E1** | Open-call windows and commissioning briefs — direct buyer-intent signal. |
| TMDB | Metadata | API | E1 | **Commercial use requires a paid written agreement — see §3.4.** |
| Wikidata / Wikipedia | Metadata | API, CC licence | E1 | Free, licence-clean fallback for title/company/date metadata. |
| Find Case Law (The National Archives) | Court judgments | **Public API**, Open Justice Licence | **E1** | Reality anchors. Explicitly designed for reuse and republication. |
| Companies House | Registry | Free API | E1 | Production-company activity, filings, directors. |
| Regulator/inquiry publications (FCA, HSE, ICO, CQC, Ofsted, public inquiries) | Government | Free | E1 | Strong world/reality anchors — see §3.5. |

**[FACT, E2]** **Find Case Law** (The National Archives) provides a public API for court judgments and tribunal decisions, under a bespoke **Open Justice Licence** permitting copying, publication, distribution and transmission. The Ministry of Justice ended its arrangement with BAILII; from April 2022 judgments from the High Court, Court of Appeal, Crown Court, House of Lords, Supreme Court, Privy Council and other courts are public records held by TNA. BAILII itself has historically refused bulk download/scraping, granting bulk access only in specific research arrangements. ([TNA Find Case Law API](https://nationalarchives.github.io/ds-find-caselaw-docs/public), [Law Gazette](https://www.lawgazette.co.uk/law/official-court-judgments-database-goes-live/5112223.article))

**[PROPOSAL]** Use **Find Case Law**, not BAILII. It is the official source, has an API, and has an explicit reuse licence. Scraping BAILII against its stated position would be both a legal and a reputational error.

### 3.2 Music & creator music

| Source | Type | Access | Grade | Notes |
|---|---|---|---|---|
| TikTok Creative Center | Trend data | Public web UI, **no public API** | E2 | Trending sounds/hashtags, ~24–48h refresh, ~6-month window; reliable for last 30–90 days. |
| TikTok Research API | Official API | **Academic institutions only; commercial use prohibited** | E1 | **Closed to us.** |
| YouTube Data API | Official API | Free, 10,000 units/day | **E1** | See §3.4. |
| Spotify Web API | Official API | Free tier, **restricted** | **E1** | See §3.4 — likely unusable for us. |
| Google Trends | Trend data | Public; no official API | E2 | Useful directional signal; unofficial libraries are fragile and ToS-ambiguous. |
| Music Gateway / TAXI / Songtradr briefs | Buyer briefs | Public/member pages | E2 | Direct demand signal for Arm B if revived. |
| Library catalogue pages (Epidemic, Artlist, Soundstripe, Pond5, Uppbeat) | Supply/taxonomy | Public pages | E2 | **Use for taxonomy and saturation analysis only** — what moods/durations/use-cases exist and how crowded each is. Never for audio ingestion. |

**[FACT, E2]** TikTok Creative Center has **no public API**. TikTok's official Research API is restricted to qualifying academic institutions, takes ~4 weeks to approve, caps at 1,000 requests/day, and **explicitly prohibits commercial use**. The Creative Center web UI is free and accessible without login; trend data refreshes every 24–48h over a ~6-month window. ([ScrapeBadger](https://scrapebadger.com/blog/tiktok-scraping-apis-in-2026-the-complete-deep-guide), [Creatify](https://creatify.ai/blog/tiktok-creative-center))

**[INFERENCE]** The most important creator-music demand signal on the market is therefore available to us **only through manual human observation**. **[PROPOSAL]** Treat this as a *human-in-the-loop weekly task* — a person records the top rising sounds by category into a Sheet — not an automated scrape. Scraping the Creative Center to work around the absence of an API, having been told the Research API forbids commercial use, would be circumventing a clearly-expressed restriction. That is not a route I will design in.

### 3.3 Cross-arm

**[PROPOSAL]** Public RSS/Atom feeds are the backbone: cheap, explicitly published for consumption, stable, and requiring no credentials. n8n has native RSS and HTTP nodes. Build the Factory RSS-first and add APIs only where a feed cannot answer the question.

### 3.4 API constraints that materially change the design

**[FACT, E1]** **TMDB**: free licence is **non-commercial only**, with attribution. Commercial use requires a **written agreement**. Reported commercial rate ~**$149/month** for companies under $1m annual revenue [E3]. ([TMDB API Terms](https://www.themoviedb.org/api-terms-of-use), [TMDB API for Business](https://www.themoviedb.org/api-for-business))

**[INFERENCE]** The Scriptwriter Factory is a commercial venture by definition. **We therefore cannot use TMDB's free tier.** This is a hard gate, not a grey area. Either budget for the commercial licence or use Wikidata (CC-licensed) instead. **[PROPOSAL]** Start with Wikidata; add TMDB only if a specific, evidenced need justifies the licence.

**[FACT, E1]** **Spotify**: developer terms prohibit using the Spotify Platform or Spotify Content **to train a machine learning or AI model, or to ingest Spotify Content into an ML/AI model**. In February 2026 Spotify narrowed Development Mode to non-commercial use by individual developers. ([Spotify Developer Terms](https://developer.spotify.com/terms), [Spotify Developer Blog, 6 Feb 2026](https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security))

**[INFERENCE]** **Assume Spotify is unavailable to this project.** Both restrictions bite: we are commercial, and the Factory's purpose is to feed evidence into model-driven analysis. **[PROPOSAL]** Design with no Spotify dependency. Do not apply for extended access on the theory that our use is "analysis, not training" — that is exactly the argument the revised terms exist to foreclose, and the downside (a public terms breach by an IP company whose entire pitch is clean provenance) is asymmetric.

**[FACT, E1/E2]** **YouTube Data API**: free, no per-request billing, **10,000 quota units/day**; a single *search* request costs **100 units** → ~100 searches/day. Quota **cannot be purchased**; the only routes to more are an extension request (no guarantee) or using less. Developer policies restrict long-term storage beyond permitted windows, multiplying quota across projects, and building competing datasets. ([Google YouTube API Developer Policies](https://developers.google.com/youtube/terms/developer-policies), [Phyllo](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota))

**[INFERENCE]** 100 searches/day is a real design constraint. **[PROPOSAL]** Never let a workflow call `search.list` in a loop. Resolve channels/playlists once, cache IDs in Sheets, and poll cheap endpoints thereafter. Budget quota explicitly as a governed resource with its own Sheet tab.

**[FACT, E1/E3]** **Google Sheets API**: **60 read and 60 write requests per minute per user; 300 per minute per project**; no daily cap within those limits. Overages are **planned to become billable later in 2026**. ([Google Sheets API Limits](https://developers.google.com/workspace/sheets/api/limits))

**[INFERENCE]** This is the sharpest technical constraint on the whole architecture, because the estate doctrine puts Sheets on the critical path as operational state. A naive n8n design writing one row per item will hit 60 writes/minute almost immediately. **[PROPOSAL]** Mandate **batch writes** (`values.batchUpdate`) — accumulate in the workflow, write once per batch. Treat "one Sheets write per record" as a design defect. The forthcoming billing change makes this a cost issue as well as a reliability one, and should be re-checked before Phase 1 ships.

### 3.5 Reality anchoring — a governance boundary, not a feature

**[FACT, E2]** *When They See Us*: Linda Fairstein sued Netflix for defamation in 2020 over her portrayal; settled 2024, with Netflix adding a disclaimer and donating $1m to the Innocence Project. *Inventing Anna*: Rachel Williams sued Netflix for defamation and false light. UK practitioners identify the twin risks as defamation (inaccurate/misleading portrayal capable of causing serious harm) and misuse of private information. ([Gateley](https://gateleyplc.com/insight/article/fictionalising-true-stories-the-legal-risks/), [Brooklyn Sports & Ent. Law](https://sports-entertainment.brooklaw.edu/film-tv/documentaries-drama-and-defamation-creators-in-court-for-real-life-portrayals/))

**[INFERENCE]** Both cited actions were brought by **real, identifiable, living people portrayed unflatteringly in dramatisations** — the precise output an automated "reality anchor" pipeline would produce if left unsupervised. An automated system that reads a court judgment and drafts a drama around its participants is a defamation generator with extra steps. The risk is not theoretical and it is not cheap.

**[PROPOSAL]** Hard-code these as **non-negotiable system constraints**, enforced in workflow logic and not merely in a prompt:
1. Facts may inspire **fictional** stories. Real cases are **never** dramatised as themselves.
2. **Automatic block** on any property whose research dossier references a living identifiable individual, an unresolved criminal matter, or active proceedings. Block, not warn.
3. Names, distinguishing characteristics and case-specific detail must be **changed by human decision**, recorded in provenance.
4. **Mandatory human legal review** before any external submission touching real events. No automation gate substitutes for this.
5. Prefer **structural** anchoring — how a regulated industry actually works, what a real process looks like, what the economics are — over **incident** anchoring. This captures most of the authenticity value with a fraction of the risk, and is the stronger creative choice anyway.

---

## 4. PROPOSED SCORING MODELS

**[PROPOSAL]** All weights below are **priors to be beaten by our own evidence** (§9), not truths. The mission asked me not to implement the candidate dimensions blindly; the changes I have made are justified against evidence, and the *revision mechanism* matters more than the opening numbers.

### 4.1 Film/TV Opportunity Score (0–100)

| # | Dimension | Weight | Source | Why this weight |
|---|---|---|---|---|
| 1 | Buyer/commissioner demand | 18 | Commissioning announcements, buyer briefs, open calls | Direct purchase intent — the strongest single signal |
| 2 | **Route-to-buyer accessibility** | **18** | Submission-policy register (§5) | **Raised sharply.** §2.1 shows access, not quality, is the binding constraint. An unreachable buyer scores zero regardless of demand |
| 3 | **Production feasibility** | **15** | Cast size, locations, VFX, period, budget band | **Raised.** Ampere: commissions ~flat but 40% slower — production-ready material is the scarce good |
| 4 | Originality space | 12 | Saturation analysis of comparable titles | Guards against the crime-saturation trap |
| 5 | Audience demand | 10 | Ofcom, BFI, public audience research | Necessary but weakly discriminating: everyone can see it |
| 6 | Saturation (inverse) | 10 | Count of comparable recent commissions | Explicit counterweight to dimension 5 |
| 7 | Buyer fit | 7 | Specific named buyer's recent slate | Precision of targeting |
| 8 | International potential | 5 | Format travel, co-pro viability | Real but secondary at our stage |
| 9 | Reality-anchor strength | 5 | Depth of lawful factual grounding | Value only when §3.5 constraints are satisfied |

**Removed from the candidate list, with reasons:**
- **Pitchability** — **[INFERENCE]** unmeasurable without a buyer response; it is a *property of the eventual pitch document*, not of the opportunity. Scoring it pre-development invites the model to reward its own fluency, which is circular. Moved to the QA gate (§6.4).
- **Marketplace accessibility** — merged into dimension 2; they were measuring the same thing.
- **Budget practicality** — merged into dimension 3 for the same reason.
- **Episodic/series potential** — **[PROPOSAL]** demote to a *categorical attribute* (feature / limited / returnable) rather than a score. It changes which buyer we approach; it is not a quality axis.

**[PROPOSAL]** Governance gates:
- **Score < 60** → archive. No development spend.
- **60–74** → Chairman review required before development.
- **≥ 75** → eligible for development, still subject to the §3.5 legal block and an explicit Chairman go.
- **Any legal block** → hard stop regardless of score. A score cannot override a block.

### 4.2 Creator-Music Opportunity Score (0–100)

| # | Dimension | Weight | Rationale |
|---|---|---|---|
| 1 | **Licence-route clarity** | **25** | **[INFERENCE]** Highest weight, deliberately. §2.3: contributor bans and platform enforcement mean a track with no lawful, open, disclosed route to a paying licensee has zero value however good it is |
| 2 | Evidenced creator/brand demand | 20 | Observed use-case demand (TikTok Creative Center, brand briefs) |
| 3 | Saturation (inverse) | 20 | With ~44% of daily uploads AI-generated, crowding is the default state and must be scored heavily |
| 4 | Use-case specificity | 15 | Narrow, well-defined briefs beat generic "background music" |
| 5 | Production feasibility & QC pass rate | 10 | Can we actually make it to standard, repeatably |
| 6 | Differentiation | 10 | Curation/coherence — the one axis where volume does not win |

**[PROPOSAL]** Arm B scoring is **not specified** in Phase 0, consistent with the recommendation to defer (§2.2). Specifying a model for an arm we are not building is waste.

### 4.3 How the model learns (§9 mission requirement)

**[PROPOSAL]** Every scored opportunity writes a frozen **score vector** at decision time. Every outcome (§9.2) writes back against that vector. After ≥ 30 outcomes per arm, run a **quarterly calibration review**: which dimensions actually predicted outcomes? Re-weight by evidence and **version the model** (`SCORING_MODEL_V1`, `V2`…), recording the version on every scored row so historic decisions remain interpretable. **[INFERENCE]** 30 is a judgement call — enough to see gross mis-weighting, far too few for statistical confidence. Until we have hundreds of outcomes, calibration is *directional correction by human judgement informed by data*, not model fitting, and should be labelled as such so nobody mistakes it for rigour it does not have.

---

## 5. PROPOSED DATA SCHEMA

**[PROPOSAL]** Canonical entities. `snake_case`; every table carries `created_at`, `updated_at`, `updated_by` (workflow ID or human), `schema_version`.

### 5.1 Core

**`evidence`** — the atomic unit. Everything else references it.
```
evidence_id (ULID, PK)
arm                  A | B | C | CROSS
source_name
source_url
source_type          rss | api | public_page | manual | document
retrieved_at         ISO-8601 UTC
publisher
published_at
title
excerpt              verbatim, bounded length
claim_summary        model-generated, clearly marked as derived
evidence_grade       E1 | E2 | E3
signal_type          commissioning | acquisition | renewal | cancellation |
                     development | exec_statement | open_call | brief |
                     audience_data | trend | economics | other
entities_json        companies, titles, genres, territories (no living individuals)
content_hash         SHA-256 of excerpt — dedupe + tamper-evidence
drive_file_id        snapshot custody
model_used / prompt_hash / token_cost_usd
status               new | classified | scored | archived | rejected
```

**`opportunity`**
```
opportunity_id (ULID, PK)
arm
title_working
thesis                 the demand argument in prose
world_id / engine_id    (Arm A)
use_case_id             (Arm C)
evidence_ids_json       array of evidence_id — the audit trail
score_total
score_vector_json       per-dimension scores
scoring_model_version
legal_flags_json        living_individual | active_proceedings | unresolved_case | none
legal_block             TRUE | FALSE     ← hard gate
status                  candidate | chairman_review | approved | in_development |
                        parked | archived | rejected
chairman_decision / chairman_decision_at / chairman_note
```

**`property`** — a developed creative asset.
```
property_id (ULID, PK)
opportunity_id (FK)
arm
type                 series_bible | pilot | feature | treatment | pitch_pack |
                     song | track | pack
title
current_stage        see §6 pipeline stages
current_version
drive_folder_id
rights_record_id (FK)
status               in_development | qa | packaged | submitted | licensed |
                     optioned | sold | shelved
```

**`property_version`** — append-only. Never updated in place.
```
version_id (ULID, PK)
property_id (FK)
version_number
stage
authored_by          chairman | chatgpt | claude | human_other
human_input_text     ← Chairman/adviser creative contribution, verbatim
model_provider / model_id / prompt_hash / prompt_drive_file_id
output_drive_file_id / output_hash (SHA-256)
token_cost_usd
critique_summary
created_at
```

**[INFERENCE]** `property_version` is the single most important table in the schema. Under USCO guidance (§7.1) and PRS policy (§7.3), the asset's legal status turns on demonstrable human authorship. An append-only, hash-anchored chain showing *what the human contributed, when, and what changed as a result* is the evidence that claim rests on. Storing it as a mutable "latest draft" field would destroy the thing we are actually building.

**`rights_record`** — one per property. Chain of title.
```
rights_record_id (ULID, PK)
property_id (FK)
creation_timestamp
chairman_concept_text
contributors_json          role, name, contribution, date
ai_involvement             none | assisted | generated
ai_disclosure_text         the text we publish (DDEX / licence / submission)
human_authorship_evidence_json    version_ids evidencing human contribution
composition_owner / lyric_owner / master_owner / publishing_owner
performer_voice_info
samples_json / third_party_assets_json
licences_json              licensee, scope, territory, term, exclusivity, fee
submissions_json           channel, date, outcome, response
transaction_history_json
final_hash_sha256
drive_custody_folder_id
legal_review_by / legal_review_at    ← required before any external submission
```

### 5.2 Arm A libraries

**`world`** — `world_id`, `name`, `sector`, `research_depth`, `saturation_score`, `evidence_ids_json`, `notes`
**`dramatic_engine`** — `engine_id`, `name`, `category`, `saturation_score`, `notes`
**`intersection`** — `intersection_id`, `world_id`, `engine_id`, `intersection_score`, `originality_score`, `rationale`, `evidence_ids_json`, `status`

**[INFERENCE]** The mission is right that the system must *discover and score* intersections rather than randomly combine words. The combinatorial space (say 40 worlds × 30 engines = 1,200 pairs) is small enough to enumerate exhaustively and score cheaply — but scoring must be **evidence-gated**: an intersection scores only where `evidence_ids_json` is non-empty. **[PROPOSAL]** An intersection with no supporting evidence is not a low-scoring opportunity; it is **unscored**, and must be excluded from ranking entirely. Otherwise the model's fluency silently becomes the evidence, which is the failure mode the whole doctrine exists to prevent.

### 5.3 Arm C

**`use_case`** — `use_case_id`, `name`, `platform`, `mood`, `genre`, `duration_band`, `bpm_band`, `evidence_ids_json`, `saturation_score`
**`track`** — `track_id`, `property_id`, `use_case_id`, `isrc`, `iswc`, `duration_s`, `bpm`, `key`, `lufs`, `true_peak_db`, `qc_status`, `qc_notes`, `master_drive_file_id`, `preview_drive_file_id`, `ai_disclosure_flag`, `licence_terms_id`

### 5.4 Outcomes

**`outcome`** — `outcome_id`, `property_id`, `channel`, `channel_type`, `event_type` (view | download | request | shortlist | response | rejection | licence | option | sale), `event_at`, `revenue_gbp`, `buyer_type`, `time_to_outcome_days`, `notes`, `evidence_url`

---

## 6. PROPOSED SHEETS, DRIVE AND WORKFLOW ARCHITECTURE

### 6.1 Doctrine compliance

**[PROPOSAL]** The architecture below is designed to the stated estate doctrine: physical n8n workflows, modular not monolithic, queue/status-driven, Sheets for visible operational state, Drive for durable custody, explicit status transitions, idempotency, retries, cost telemetry, lineage, hashes, configurable providers, budget ceilings, human gates only where genuinely useful, automation-first, **no production Python control plane**.

**[UNKNOWN]** **I do not have the text of Rule 53 or the wider constitutional engineering rules.** They are not present in this repository and I could not retrieve them. I have designed to the doctrine as stated in the mission brief, but **I cannot certify compliance with a rule I have not read.** *Requested from the Chairman: the text of Rule 53 and any related constitutional rules, before Phase 1 build.* I would rather state this plainly than assert a compliance I cannot support.

**[FACT, E1/E2]** n8n's **Sustainable Use License** permits free self-hosted use for **internal business purposes**; the restriction bites where you sell a product or service whose value derives entirely or substantially from n8n functionality, host n8n as a service for customers, or build a competing platform. ([n8n Docs](https://docs.n8n.io/sustainable-use-license/))

**[INFERENCE]** The Factory uses n8n to run its own internal operations and sells *screenplays and music*, not automation. That is internal business use and appears clearly permitted. **[PROPOSAL]** Flag one boundary for legal review: if the Factory ever productises the Demand Intelligence Engine itself as a service to third parties, that changes the analysis. Note it in the Decision Register (D-09) now, while it is cheap to note.

**[FACT, E1/E2]** n8n **queue mode** separates main (UI/API), worker and webhook processes, using Redis as broker and PostgreSQL for persistence; SQLite is unsupported for distributed operation. ([n8n Docs — queue mode](https://docs.n8n.io/hosting/scaling/queue-mode/))

**[PROPOSAL]** Phase 1 does **not** need queue mode — volumes are far too low. Deploy single-instance with PostgreSQL (not SQLite) so that queue mode is a configuration change later rather than a migration. Choosing PostgreSQL on day one is the whole of the forward-compatibility cost.

### 6.2 Google Sheets — operational control plane

One spreadsheet, `SCRIPTWRITER_FACTORY_CONTROL`:

| Tab | Purpose | Written by |
|---|---|---|
| `00_CONFIG` | Providers, model IDs, budget ceilings, feature flags, scoring model version | Human |
| `01_SOURCES` | Feed/API registry: URL, arm, cadence, enabled, last_run, last_status, error_count | Human + workflows |
| `02_EVIDENCE` | `evidence` rows | Workflows |
| `03_WORLDS` / `04_ENGINES` / `05_INTERSECTIONS` | Arm A libraries | Workflows + human |
| `06_USE_CASES` | Arm C library | Workflows + human |
| `07_OPPORTUNITIES` | Scored opportunities + Chairman decision columns | Workflows + Chairman |
| `08_PROPERTIES` / `09_VERSIONS` | Development state and provenance chain | Workflows + human |
| `10_RIGHTS` | Chain-of-title summary (Drive holds the full record) | Workflows + human |
| `11_SUBMISSIONS` / `12_OUTCOMES` | Route activity and results | Human + workflows |
| `13_COST_LEDGER` | Per-execution token/API cost | Workflows |
| `14_ERRORS` | Failed executions, payload ref, retry count | Workflows |
| `15_QUOTA` | YouTube units, Sheets writes, per-provider spend vs ceiling | Workflows |
| `16_DECISIONS` | Chairman decision log — the governance record | Chairman |

**[PROPOSAL]** Hard rules, given §3.4:
- **Batch every write.** No per-record writes. This is the single most important operational rule in the architecture.
- Sheets is the **control surface**, not the database of record. Drive holds artefacts; Sheets holds pointers and state.
- Every row carries `evidence_id` or `source_url` — **no unsourced rows, ever**.
- When a tab exceeds ~50,000 rows, roll to an archive spreadsheet and keep a pointer. Do not let the control plane degrade into a data lake.

### 6.3 Google Drive — durable custody

```
/SCRIPTWRITER_FACTORY/
  /00_GOVERNANCE/          constitution, Rule 53, decision log exports, legal reviews
  /01_EVIDENCE/            /YYYY/MM/{evidence_id}/  snapshot + metadata.json
  /02_RESEARCH/            /{opportunity_id}/       dossiers, source PDFs
  /03_PROPERTIES/
      /{property_id}/
          /00_RIGHTS/      rights_record.json, disclosures, licences, hashes
          /01_INPUTS/      Chairman + adviser creative input, verbatim, timestamped
          /02_PROMPTS/     prompt snapshots by version
          /03_DRAFTS/      /v001/, /v002/ … append-only
          /04_CRITIQUE/
          /05_PACKAGE/     final deliverables
          /06_SUBMISSIONS/
  /04_CATALOGUE/           Arm C masters, previews, metadata
  /05_TELEMETRY/           cost exports, run logs
```

**[PROPOSAL]** Every file written to Drive is SHA-256 hashed, with the hash recorded in Sheets at write time. Draft folders are **append-only** — a new version is a new folder, never an edit. This is what makes the provenance record evidential rather than decorative: a record that can be silently rewritten proves nothing.

### 6.4 n8n workflow map

**[PROPOSAL]** Modular, single-responsibility, status-driven. Each workflow reads rows in one status and writes rows in the next.

**Foundation**
| ID | Workflow | Trigger | Responsibility |
|---|---|---|---|
| `WF-00` | Config Loader | Sub-workflow | Reads `00_CONFIG`; returns providers/ceilings. Every workflow calls it first |
| `WF-01` | Sheets Batch Writer | Sub-workflow | **Only** component permitted to write to Sheets. Enforces batching + retry |
| `WF-02` | Drive Custody | Sub-workflow | Writes file, computes SHA-256, returns `drive_file_id` + hash |
| `WF-03` | Cost Ledger | Sub-workflow | Appends to `13_COST_LEDGER`; **halts the caller when a ceiling is breached** |
| `WF-04` | Error Handler | n8n error trigger | Writes `14_ERRORS`; exponential backoff; dead-letters after N |

**[INFERENCE]** Routing all Sheets writes through a single sub-workflow (`WF-01`) is the highest-value structural decision in this map. It is the only way to enforce the 60-writes/minute limit globally rather than hoping every future workflow author remembers.

**Demand Intelligence (Phase 1 scope)**
| ID | Workflow | Trigger | Responsibility |
|---|---|---|---|
| `WF-10` | Source Poller | Schedule | Reads `01_SOURCES`; fetches RSS/API; dedupes on `content_hash`; writes `status=new` |
| `WF-11` | Evidence Classifier | Status `new` | LLM extraction → `signal_type`, entities, `claim_summary`, `evidence_grade`. Writes `status=classified` |
| `WF-12` | Saturation Analyser | Schedule | Aggregates classified evidence into genre/world/use-case saturation counts |
| `WF-13` | Intersection Scorer | Schedule | Scores evidence-backed intersections only (§5.2) |
| `WF-14` | Opportunity Builder | Status `scored` | Assembles thesis + evidence chain → `07_OPPORTUNITIES` as `candidate` |
| `WF-15` | Legal Screen | Status `candidate` | Applies §3.5 rules. Sets `legal_block`. **Hard stop** |
| `WF-16` | Chairman Digest | Weekly | Ranked opportunities + evidence links to the Chairman. **The Phase 1 deliverable** |

**Development (Phase 2+, gated)**
`WF-20` Research Dossier → `WF-21` Premise/Logline → `WF-22` Character & World → `WF-23` Story Architecture → `WF-24` Treatment → `WF-25` Episode Outlines → `WF-26` Screenplay Draft → `WF-27` Critique/Coverage → `WF-28` Revision → `WF-29` Originality & Rights Check → `WF-30` Package Assembly.

**[PROPOSAL]** Every one of `WF-20`…`WF-30` **must** write a `property_version` row capturing human input, prompt hash, output hash and cost. A stage that cannot evidence its human contribution does not advance. This is enforced in workflow logic, not left to discipline.

**Arm C (Phase 3+, gated)**
`WF-40` Use-Case Demand → `WF-41` Composition Brief → `WF-42` Generation → `WF-43` QC (LUFS/true-peak/duration/duplicate detection) → `WF-44` Mastering/Normalisation → `WF-45` Rights & Disclosure → `WF-46` Catalogue Metadata → `WF-47` Preview Assets → `WF-48` Outcome Telemetry.

**Feedback**
`WF-60` Outcome Ingest → `WF-61` Score Calibration (quarterly, **human-reviewed**, versioned) → `WF-62` Model Version Publisher.

**[PROPOSAL]** Idempotency everywhere: every workflow computes a deterministic key (`content_hash` for evidence; `property_id + stage + version` for development) and no-ops on a key it has already processed. Given that n8n retries and most sources are at-least-once, this is not optional.

---

## 7. RIGHTS, PROVENANCE AND CHAIN OF TITLE

**Not legal advice.** These are research findings for the Chairman's legal advisers. I have deliberately not drawn legal conclusions beyond what the cited sources state.

### 7.1 United States — copyrightability

**[FACT, E1]** US Copyright Office, *Copyright and Artificial Intelligence, Part 2: Copyrightability* (**29 January 2025**): based on current generally-available technology, **prompts alone do not provide sufficient control for the resulting work to be human-authored**; prompting alone, "even using complex and multiple prompts," does not confer copyright in the output. Human authors retain copyright in human-authored material perceptible in AI outputs, in creative **selection, coordination or arrangement**, and in **creative modifications** of outputs. Sufficiency is assessed **case by case**. The Office concluded existing law is adequate. ([Copyright Alliance](https://copyrightalliance.org/ai-report-part-2-copyrightability/), [Skadden](https://www.skadden.com/insights/publications/2025/02/copyright-office-publishes-report), [Jones Day](https://www.jonesday.com/en/insights/2025/02/copyrightability-of-ai-outputs-us-copyright-office-analyzes-human-authorship-requirement))

### 7.2 United Kingdom

**[FACT, E1/E2]** s9(3) CDPA 1988 currently protects computer-generated literary, dramatic, musical or artistic works with no human author for **50 years from creation**. The UK Government's report of **18 March 2026** concluded that s9(3) protection **should be removed**, while continuing to monitor. Most consultation respondents considered works created solely by AI should not be protected, while supporting continued protection for **AI-assisted** works. No consensus emerged on broader AI/copyright questions; the one area of broad support was **transparency** in the use of copyright material in AI training and deployment. **No legislation has been introduced; the report is non-binding.** ([HSF Kramer](https://www.hsfkramer.com/notes/ip/2026-03/uk-government-report-on-copyright-and-ai-concludes-more-evidence-is-needed-although-s9-3-cdpa-could-go), [Bird & Bird](https://www.twobirds.com/en/insights/2026/uk/copyright-,-a-,-aiin-the-uk-the-debate-rolls-on), [GOV.UK consultation](https://www.gov.uk/government/consultations/copyright-and-artificial-intelligence/copyright-and-artificial-intelligence))

**[INFERENCE]** The UK and US positions are converging on the same rule from opposite directions: **AI-assisted works with substantial human authorship are protectable; purely AI-generated works are not (US now, UK proposed).** For the Factory this is unambiguous strategic direction — the human contribution is not a compliance overhead, it is the mechanism by which an output becomes an asset. Note also that s9(3), while it still stands, is *not* a safe harbour to design around: the Government has proposed removing it, so any strategy depending on it is depending on a provision with a published expiry intent.

### 7.3 Collective management — music

**[FACT, E1]** PRS for Music AI policy (**v1, October 2025**): AI-generated lyrics and compositions with no human author or insufficient human intervention are not protected under UK law, and **AI-generated works cannot be registered with PRS for Music**. *AI-assisted* works may be registrable; a relevant test is whether the **human contribution alone would be substantial**. It is for the creator to ensure eligibility and, where appropriate, **to evidence the extent and influence of their contribution**. ([PRS for Music AI Policy](https://www.prsformusic.com/-/media/files/prs-for-music/works/prs-for-music-and-artificial-intelligence-policy.pdf))

**[INFERENCE]** "Evidence the extent and influence of their contribution" is, almost verbatim, a specification for the `property_version` table (§5.1). A PRO has told us in writing what record it expects. Build to that specification and the same artefact serves registration, copyright assertion, and buyer due diligence simultaneously.

### 7.4 Disclosure obligations

**[FACT, E1/E2]** **EU AI Act Article 50**: providers must ensure generative AI outputs are marked with **effective, reliable, robust and interoperable machine-readable marks** enabling detection as AI-generated or manipulated. Obligations apply from **2 August 2026**; under the AI Omnibus provisional agreement of May 2026, generative AI systems already on the market before that date have until **2 December 2026** to meet the Art. 50(2) machine-readable marking requirement. The Commission published finalised guidelines on **20 July 2026** alongside a Code of Practice on Transparency of AI-Generated Content, including three publicly-available EU icons for Art. 50(4)/(5) disclosure. Purely personal, non-professional use is exempt. ([Orrick](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50), [European Commission](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), [artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/50/))

**[INFERENCE]** These obligations fall primarily on *providers and deployers of AI systems*. Whether a UK company publishing AI-assisted creative works into EU markets is a "deployer" with Art. 50(4) disclosure duties is **[UNKNOWN]** and a question for counsel. **[PROPOSAL]** Do not wait for the answer. **Disclose by default in every arm.** The commercial cost of disclosure is low (Spotify states it does not down-rank AI-assisted music); the cost of an undisclosed-AI finding against an IP company whose entire proposition is clean provenance would be severe and probably terminal. Disclosure is also simply the honest position, which is the better reason.

**[FACT, E1/E2]** **DDEX** is the standard channel for AI declarations in release metadata; distributors embed the declaration in deliveries to platforms. ([Undetectr](https://undetectr.com/blog/ddex-ai-disclosure-standard-explained))

### 7.5 Provenance record — what "durable" must mean

**[PROPOSAL]** Every property carries a `rights_record` (§5.1) satisfying the mission's §7 list, with these additions justified by the evidence above:
- **`ai_involvement`** as a controlled value (`none` | `assisted` | `generated`) — because PRS registration and platform disclosure both turn on exactly this distinction.
- **`human_authorship_evidence_json`** — pointers to `property_version` rows evidencing the Chairman's contribution. This is the PRS "evidence the extent and influence" artefact.
- **`legal_review_by` / `legal_review_at`** — mandatory before any external submission.
- **SHA-256 at every stage**, with hashes in Sheets and files in Drive, append-only.

**[UNKNOWN]** Whether third-party timestamping/notarisation is warranted for high-value properties. Cheap to add later; do not gold-plate in Phase 1.

---

## 8. ROUTE-TO-MARKET INVENTORY

### 8.1 Film & TV

| Route | Access | Cost | Grade | Assessment |
|---|---|---|---|---|
| Netflix / major streamers | **Agent or existing relationship only** | — | E1 | **Closed** without representation |
| BBC Writersroom Open Call | Open, ~5-week windows | Free | E2 | **Open.** Highest-value free route. Human-authored only |
| Nicholl Fellowships | Open competition | Entry fee | E2 | 5 × $35,000; 24 winning scripts produced as of 2024 |
| The Black List | Open, paid | ~$380/script per "real run" | E3 | Open but **cost scales linearly with volume** — anti-factory economics |
| InkTip | Open, paid | ~$32.50/mo Pro | E3 | Open; free to filmmakers; conversion evidence **[UNKNOWN]** |
| Virtual Pitch Fest / Stage 32 | Open, paid | ~$6.50–30/pitch | E3 | Open; conversion evidence **[UNKNOWN]** |
| UK independent producers | Direct approach | Free | E2 | **[INFERENCE]** Most realistic paid-outcome route. Ampere's supply-crunch finding says they need feasible material |
| Coverfly | **Shut down Aug 2025** | — | E2 | **Gone** |
| Agents / managers | Referral, track record | Free | E2 | Gateway to everything closed above |

**[INFERENCE]** The routes that are *open* are open to **human-authored** work; the routes that are *paid* charge per script and provide no evidenced conversion rate. I could find **no published conversion data** for any paid pitch platform — that absence is itself a finding, and the mission's warning against treating vanity exposure as commercial evidence applies with full force here. **[PROPOSAL]** Any Arm A route spend must be treated as a measured experiment with a pre-declared budget cap and a pre-declared success criterion, logged in `11_SUBMISSIONS` and `12_OUTCOMES`.

### 8.2 Songs

| Route | Access | Grade | Assessment |
|---|---|---|---|
| Publishers direct | Relationship / limited open submission | E2/E3 | Largely relationship-gated |
| Songtradr | Open, freemium (60%/80% split) | E3 | Open; outcomes **[UNKNOWN]** |
| Music Gateway / TAXI briefs | Membership | E2 | Brief aggregation — genuine demand signal |
| Paid pitch (Discover Sooner, SongU) | Open, paid | E3 | Conversion **[UNKNOWN]** |
| Sync libraries | Varies | E2 | Overlaps Arm C |
| **PRS registration** | **AI-generated: refused** | **E1** | **Gate on the whole arm** |

### 8.3 Creator music

| Route | Access | Grade | Assessment |
|---|---|---|---|
| Epidemic Sound | **Refuses AI-generated contributions** | E2 | **Closed** |
| Envato / AudioJungle | **Prohibits AI as main component** | E3 | **Closed** (verify) |
| Artlist | Reported to exclude AI contributions | E3 | **Probably closed** (verify) |
| Pond5 | Mandatory AI disclosure, not a ban | E3 | **Possibly open** — highest-priority verification |
| TikTok CML | Via distributor / SoundOn opt-in | E2 | **Open**, but TikTok-scoped licence only; payout rate unpublished |
| DSPs (Spotify, etc.) via distributor | Open with DDEX AI disclosure | E2 | Open; economics poor at commodity scale |
| **Direct creator/brand licensing (own channel)** | **We control it** | — | **[PROPOSAL] Primary route.** No third-party policy can close it |
| Own social presence | Open | — | **Funnel only.** Never mistake reach for a licence |

---

## 9. FEEDBACK LOOP

**[PROPOSAL]** `RESEARCH → SCORE → SELECT → CREATE → QA → PACKAGE → DISTRIBUTE → MEASURE → LEARN → RESEARCH`, with the loop closed through `12_OUTCOMES` (§5.4) and calibration through `WF-61` (§4.3).

Recorded per the mission: views, downloads, requests, shortlists, responses, rejections, submission outcomes, licences, options, sales, revenue, buyer type, genre/use case, time-to-outcome.

**[INFERENCE]** Two honest cautions about the loop:
1. **Rejections are the dominant signal and will be mostly silent.** Most submissions receive no response at all. **[PROPOSAL]** Record `no_response` explicitly after a defined window; treating silence as missing data will bias the model toward whatever happens to generate replies.
2. **Volume will be far too low for statistical learning for a long time.** A handful of outcomes per quarter cannot fit a nine-dimension model. **[PROPOSAL]** Label `WF-61` output as *human-reviewed directional correction*, and forbid automatic re-weighting without Chairman sign-off. A system that claims to learn from six data points is worse than one that admits it cannot.

---

## 10. MUSIC TOOLING COMPARISON

All rows **E3 unless marked** — vendor pricing and licence terms change frequently and none of this was verified against primary documentation. **Do not select a provider on this table alone.**

| Provider | API | Commercial rights | Training-data position | Indicative cost | Assessment |
|---|---|---|---|---|---|
| **ElevenLabs Music** | **Yes** | Commercial use from **Starter $6/mo**; **film/TV/Studio Games require Enterprise** | **States "trained on licensed data only"**, citing deals with Merlin Network (indie labels) and Kobalt (publishing) | Starter $6 → Creator $22 → Pro $99 → Scale $299 → Business $990; shared credits; recent cuts up to 50% API / 40% self-serve | **[INFERENCE] Strongest provenance story of any candidate.** v2 announced 11 June 2026 |
| **Suno** | **No public self-serve API** as of mid-2026; partner exploration announced 1 July | Pro $10/mo and Premier $30/mo give full commercial rights; free tier non-commercial | Contested / **[UNKNOWN]** | ~$0.03–0.04/song raw at Premier | **Third-party "Suno API" services are unofficial.** [INFERENCE] Unsuitable — no official API, unclear training provenance |
| **Stable Audio 2.5** | Yes | Commercial-oriented | Licensed-data positioning | **~$0.20/track** | Transparent pricing; credible for instrumental beds |
| **Loudly** | **Yes — public developer portal, REST docs, free allowance** | Enterprise licensing **with indemnification** | Copyright-safe positioning | Quote-driven (startup/SME/corporate) | **[INFERENCE] Indemnification is commercially significant** — it is the only candidate reported to transfer risk to the vendor |
| **Mubert** | Yes | Royalty-free background/adaptive | **[UNKNOWN]** | **[UNKNOWN]** | Suited to adaptive/generative streaming, not fixed catalogue |
| **Beatoven** | Yes | Commercial rights | **[UNKNOWN]** | ~$2.50/mo entry | Cheapest paid option reported |

Sources: [Apiframe](https://apiframe.ai/blog/best-ai-music-generation-apis), [aimusicapi](https://aimusicapi.ai/en/blog/ai-music-generation-api-comparison), [BIGVU](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/), [invideo](https://invideo.io/blog/elevenlabs-music-ai-generator/), [gptproto](https://gptproto.com/blog/suno-api), [musicmake.ai](https://musicmake.ai/blog/suno-ai-pricing-plans-2026)

**[PROPOSAL]** If Arm C proceeds, shortlist **ElevenLabs Music** (licensed-training provenance) and **Loudly** (indemnification). Both align with the §7 conclusion that defensible provenance is the actual asset. **Reject Suno** for production use: no official API and unclear training provenance are exactly the two properties we cannot accept in a chain of title. Selection requires primary verification of terms — including, specifically, whether the licence permits **sub-licensing to third parties**, which is what a creator-music catalogue business actually requires and which none of the sources above addressed.

**[UNKNOWN]** Whether any of these providers permits sub-licensing of generated output to third-party licensees. **This is the single most important unresolved question for Arm C** — a licence that permits our own commercial use but not sub-licensing would invalidate the entire catalogue model. Verify before any further Arm C work.

---

## 11. COST MODEL

### 11.1 Model pricing (current, from the Claude API reference)

| Model | Input $/1M | Output $/1M |
|---|---|---|
| Claude Opus 5 (`claude-opus-5`) | $5.00 | $25.00 |
| Claude Sonnet 5 (`claude-sonnet-5`) | $2.00 | $10.00 |
| Claude Haiku 4.5 (`claude-haiku-4-5`) | $1.00 | $5.00 |

### 11.2 Demand Intelligence Engine — Phase 1 (recommended scope)

| Item | Assumption | Monthly |
|---|---|---|
| Evidence classification | 200 items/day × (2k in / 500 out) on Haiku 4.5 | **~$27** |
| Weekly synthesis + digest | 4 × (150k in / 20k out) on Opus 5 | **~$5** |
| n8n hosting (self-hosted VPS + PostgreSQL) | Small instance | **~$25** |
| Google Workspace | Existing estate | £0 |
| TMDB | **Excluded** — commercial licence not justified (§3.4) | $0 |
| **Total** | | **≈ $57/month (~£45)** |

**[INFERENCE]** Prompt caching should materially reduce the classification line, since the classifier's system prompt and taxonomy are stable across every call. I have **not** modelled the saving — it depends on cache-hit behaviour we cannot predict pre-build. Treat ~$57 as an unoptimised ceiling.

### 11.3 Development — per property, if authorised

| Stage | Assumption (Opus 5) | Cost |
|---|---|---|
| Research dossier | 50k in / 15k out | $0.63 |
| Treatment | 30k in / 12k out | $0.45 |
| Series architecture + 6 outlines | 6 × (40k in / 15k out) | $3.45 |
| Pilot screenplay, 5 passes | 5 × (60k in / 25k out) | $4.63 |
| Critique / coverage, 3 passes | 3 × (80k in / 8k out) | $1.80 |
| **Raw total** | | **≈ $11** |
| **With retries and revisions** | | **≈ $15–30** |

### 11.4 Creator music — per track

| Item | Cost |
|---|---|
| Generation (Stable Audio ~$0.20 / Suno ~$0.04 / ElevenLabs credit-based) | $0.05–0.25 |
| QC + metadata (Haiku) | ~$0.01 |
| **Per track** | **≈ $0.06–0.26** |
| **1,000 tracks** | **≈ $60–260** |

### 11.5 The finding that matters

**[INFERENCE]** **Production cost is not a meaningful constraint on this business at any scale we would plausibly operate.** A complete pilot package costs less than a paperback. A thousand-track catalogue costs less than a single Black List "real run" on three scripts.

The real costs sit entirely elsewhere:
- **Route access**: ~$380 per script per Black List run; ~$32.50/month InkTip; ~$6.50–30 per pitch — all **per-asset and volume-scaling**
- **Legal review**: **[UNKNOWN]**, and mandatory before any reality-anchored submission
- **Human creative time**: the Chairman's, which is the genuinely scarce input
- **Human authorship**: which the evidence says is what makes the output an asset at all

**[INFERENCE]** This inverts the factory metaphor completely. The mission's model — cheap mass production feeding a distribution funnel — describes a cost structure that does not exist here. Cheap generation is not a moat; it is the commodity floor everyone already stands on (see: 44% of Deezer's daily uploads). **[PROPOSAL]** Spend the budget on **evidence, selection, human authorship and legal defensibility**, not on generation volume. Those are the scarce inputs, and they are the ones the §7 gates actually reward.

---

## 12. RISKS

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | **Purely AI-generated properties are not copyrightable** (USCO; UK s9(3) proposed for removal) | **High** | **Severe** — no defensible asset | Mandatory substantial human authorship; `property_version` evidence chain; no property advances without it |
| R-02 | **No route to professional Film/TV buyers without representation** | **High** | **Severe** — no revenue path | Target UK independents + open calls; treat paid routes as capped experiments |
| R-03 | **Creator-music glut** (~44% of daily uploads AI) | **High** | High | Compete on curation and licence clarity, not volume; own-channel direct licensing |
| R-04 | **Library contributor bans** (Epidemic, Envato, probably Artlist) | **High** | High | Verify each; prioritise direct licensing where no third party can close the route |
| R-05 | **Defamation / privacy** from reality anchoring | Medium | **Severe** | §3.5 hard blocks; no living individuals; mandatory legal review |
| R-06 | **Platform policy shifts** invalidate a route overnight | High | Medium | Never single-route; quarterly route re-verification |
| R-07 | Sheets API rate limits break the control plane | **High if unmitigated** | Medium | Mandatory batching via `WF-01`; quota tab; forthcoming billing change monitored |
| R-08 | **Terms-of-service breach** (Spotify ML clause, TMDB commercial, TikTok Research API) | Medium | **Severe** — reputational for a provenance business | Excluded by design; §3.4 is a compliance boundary, not guidance |
| R-09 | Scoring model overfits to tiny outcome samples | High | Medium | Human-reviewed calibration only; versioned models; no auto re-weighting |
| R-10 | **Evidence quality** — this document rests on search summaries, not primary sources | **Certain** | High | Primary verification is a Phase 1 gate (§0.1, §14) |
| R-11 | Cost creep from unbounded generation | Medium | Low–Medium | Budget ceilings in `00_CONFIG`; `WF-03` halts on breach |
| R-12 | Sunk-cost drift into mass production despite §11 | Medium | High | Phase gates require explicit Chairman authority; volume is not a KPI in any tab |
| R-13 | **Rule 53 / constitutional compliance unverified** | **Certain** | Unknown | Chairman to supply text before Phase 1 build |
| R-14 | Music provider licence may not permit **sub-licensing** | **[UNKNOWN]** | **Severe for Arm C** | Verify before any Arm C work (§10) |

---

## 13. UNRESOLVED DECISIONS — FOR THE CHAIRMAN

| ID | Decision | Why it matters | My recommendation |
|---|---|---|---|
| **D-01** | **Autonomous IP factory, or governed development instrument for a human principal?** | Determines whether outputs are ownable and submittable at all | **Governed instrument.** Every gate in §7 and §8 rewards human authorship |
| **D-02** | Proceed with Arm B? | Weakest evidenced opportunity; consumes governance attention | **Defer** until Arm A or C shows one real outcome |
| **D-03** | Arm C: pursue at all, and on what route? | Contributor bans + glut close most routes | **Direct licensing only, fully disclosed**, or not at all |
| **D-04** | Volume ambition | §11 shows volume is not a moat and scales route costs linearly | **Explicitly reject volume as a goal** |
| **D-05** | Legal budget and adviser | Reality anchoring and rights need counsel | Engage before any submission; budget **[UNKNOWN]** |
| **D-06** | Music provider selection | Provenance is the asset | **ElevenLabs Music** and/or **Loudly**; **not Suno**. Verify sub-licensing first (D-13) |
| **D-07** | TMDB commercial licence (~$149/mo)? | Free tier is non-commercial only | **No** — use Wikidata |
| **D-08** | Paid route experiments, and at what cap? | No published conversion data anywhere | Cap tightly; pre-declare success criteria |
| **D-09** | Will the DIE ever be sold as a service? | Would change n8n licence analysis | Note now; decide later |
| **D-10** | **Supply Rule 53 and constitutional rules** | I cannot certify compliance with unread rules | **Required before Phase 1 build** |
| **D-11** | Who performs primary-source verification? | This document is search-summary-based | **Independent Auditor (Codex)** is well-suited |
| **D-12** | Chairman's weekly time commitment | Human authorship and review are the binding inputs | Realistic estimate needed before Phase 2 |
| **D-13** | **Does any music provider permit sub-licensing?** | Invalidates the Arm C catalogue model if not | **Verify before any Arm C work** |

---

## 14. RECOMMENDED PHASE 1 — BOUNDED PILOT

**[PROPOSAL]** **Scope: Demand Intelligence Engine only. No creative generation. No submissions. No publication. No paid accounts beyond hosting.**

### Objective
Prove that lawful, automated, evidence-grade demand intelligence can be produced continuously at low cost — and that its output changes what the Chairman would otherwise have chosen to develop. If it does not change a decision, it is not intelligence, and we should stop.

### Deliverables
1. `WF-00`…`WF-04` foundation workflows (config, batched Sheets writer, Drive custody, cost ledger, error handler)
2. `WF-10`…`WF-16` demand intelligence pipeline
3. `SCRIPTWRITER_FACTORY_CONTROL` spreadsheet with all tabs (§6.2)
4. Drive structure (§6.3)
5. 20–30 verified sources in `01_SOURCES` (RSS-first; Find Case Law; Ofcom; BFI; Companies House; buyer commissioning pages)
6. Populated `03_WORLDS` / `04_ENGINES`, seeded by human judgement, scored only where evidence exists
7. **Weekly Chairman Digest** — ranked, evidenced opportunities with full source chains
8. **Primary-source verification report** closing out every E3 item in §14's register

### Explicitly out of scope
Screenplay/treatment/song/track generation. Any submission or publication. Any paid marketplace account. Any external commercial account. Any schedule that incurs material spend. Arm B entirely.

### Success criteria (pre-declared, measured at 8 weeks)
| # | Criterion | Threshold |
|---|---|---|
| 1 | Evidence captured, all with source URL + timestamp + hash | ≥ 1,000 items |
| 2 | Classification precision on a human-audited 100-item sample | ≥ 85% |
| 3 | Evidence-backed opportunities surfaced | ≥ 20 |
| 4 | Opportunities the Chairman rates "worth developing" | ≥ 3 |
| 5 | **Opportunities the Chairman would not have found unaided** | **≥ 1** |
| 6 | Total run cost | ≤ £70/month |
| 7 | Unhandled workflow failures | 0 |
| 8 | Sheets rate-limit breaches | 0 |
| 9 | Terms-of-service breaches | **0 — non-negotiable** |
| 10 | E3 items verified against primary sources | 100% |

**[INFERENCE]** Criterion 5 is the real test. Criteria 1–4 can be satisfied by a system that efficiently rediscovers what the Chairman already believed — which would be an expensive mirror, not an intelligence engine. If after eight weeks the Factory has not surfaced a single opportunity the Chairman would not have reached alone, the honest conclusion is that the engine is not earning its place, and I would recommend stopping rather than proceeding to Phase 2.

### Gate to Phase 2
Phase 2 (development engine) proceeds **only** on: criteria 1–10 met; D-01, D-10, D-11, D-12 resolved; legal adviser engaged; and explicit Chairman authority.

---

## 15. WHAT I DID NOT DO

Stated for the record, per the Phase 0 constraints:

- No schedules activated
- No material paid spend incurred
- No external commercial accounts created
- No creative properties generated or submitted
- No content published
- No irreversible external changes
- **No other project's infrastructure, files, Sheets, Drive assets, credentials or memory touched.** The host repository (`ffmpeg-render-service`) was read to establish context and **not modified**; all Phase 0 output is confined to `scriptwriter-factory/`
- No production Python control plane written — and none proposed
- No fabricated market evidence, sources, figures or URLs. Where evidence was unavailable, **[UNKNOWN]** is recorded

---

## APPENDIX A — SOURCES

**Film & TV market**
- [Variety — Post-Peak TV Crunch: Slow Production Is Choking Scripted Supply](https://variety.com/2026/global/spotlight/post-peak-tv-supply-chain-crunch-ampere-analysis-1236696837/)
- [Variety — 5 Takeaways From Ampere Analysis at MIP London](https://variety.com/2026/tv/global/5-takeaways-from-the-ampere-analysis-at-mip-london-broadcasters-more-important-than-ever-youtube-as-a-growing-destination-for-factual-sports-boost-1236670993/)
- [Broadband TV News — Streamers shift towards scripted romance](https://www.broadbandtvnews.com/2026/06/29/streamers-shift-towards-scripted-romance-as-reality-dating-shows-decline/)
- [Deadline — BBC Commissioned Half Of All UK TV Scripted Shows](https://deadline.com/2024/03/bbc-scripted-research-ampere-analysis-1235867117/)
- [Televisual — BBC orders half of all UK 2023 scripted commissions](https://www.televisual.com/news/bbc-orders-half-of-all-uk-2023-scripted-commissions-says-report/)
- [C21Media — True Crime & Investigation 2026](https://www.c21media.net/marketplace/truecrimeandinvestigation26/)
- [Ofcom — Media Nations 2026](https://www.ofcom.org.uk/media-use-and-attitudes/media-habits-adults/media-nations-2026)
- [Broadband TV News — Netflix overtakes BBC as UK viewers' first choice](https://www.broadbandtvnews.com/2026/07/29/netflix-overtakes-bbc-as-uk-viewers-first-choice-says-ofcom/)

**Film & TV routes**
- [Netflix Help Centre — How ideas are pitched to Netflix](https://help.netflix.com/en/node/100386)
- [IndieWire — Coverfly Is Shutting Down](https://www.indiewire.com/features/commentary/coverfly-shutting-down-screenplay-industrial-complex-1235120359/)
- [No Film School — Coverfly Is Shutting Down](https://nofilmschool.com/coverfly-is-shutting-down)
- [storynotes.app — Black List Evaluation Cost in 2026](https://www.storynotes.app/blog/black-list-2026-pricing-explained)
- [InkTip — Screenwriter Services](https://www.inktip.com/sa_services_products.php)
- [Virtual Pitch Fest](https://www.virtualpitchfest.com/) · [Stage 32 Pitch Sessions](https://www.stage32.com/happy-writers/pitch-sessions)
- [London Playwrights — BBC Writersroom Script Room](https://londonplaywrightsblog.com/bbc-writersroom-script-room-10-now-open-for-drama-submissions/)
- [Academy Press Office — 2025-2026 Nicholl Fellowships](https://press.oscars.org/news/academy-announces-2025-2026-nicholl-fellowships-screenwriting) · [Deadline](https://deadline.com/2026/03/movie-academy-2025-2026-nicholl-fellowships-winners-1236763373/)
- [filmandink — Option Purchase Agreements](https://filmandink.com/2025/08/27/a-beginners-guide-to-option-purchase-agreements-in-film-and-tv/) · [Practical Law — Film option agreement](https://uk.practicallaw.thomsonreuters.com/1-504-5111)
- [Deadline — BBC writers pay rise, residuals](https://deadline.com/2024/03/bbc-show-writers-pay-rise-residuals-1235842854/)

**Guild / AI in screenwriting**
- [Bloomberg Law — Writers Guild AI Deal Pushes Studios Down New Copyright Path](https://news.bloomberglaw.com/ip-law/writers-guild-ai-deal-pushes-studios-down-new-copyright-path)
- [Variety — WGA to Seek Payment for AI Training on Scripts](https://variety.com/2026/film/news/wga-ai-training-amptp-talks-1236684012/)
- [Collider — WGA Takes Steps to Ban AI Generated Content](https://collider.com/wga-ai-written-movies/)

**Music — market, platforms, policy**
- [Epidemic Sound — How we work with artists](https://corporate.epidemicsound.com/about-us/how-we-work-with-artists/) · [Commitments to creators in the AI paradigm](https://www.epidemicsound.com/blog/our-commitments-to-artists-and-content-creators-in-the-ai-paradigm/)
- [Dynamoi — Does Epidemic Sound accept AI music](https://dynamoi.com/learn/ai-music-distribution/does-epidemic-sound-accept-ai-music) · [Stock music sites that accept AI music](https://dynamoi.com/learn/ai-music-distribution/stock-music-sites-that-accept-ai-generated-music)
- [Last Play Distro — Pond5 AI-Generated Music Policy](https://lastplaydistro.com/blog/pond5-ai-generated-music-policy-2025-complete-guide-for-creators)
- [aimusicpreneur — Spotify has no AI music filter while Deezer does](https://www.aimusicpreneur.com/ai-music-news/spotify-no-ai-music-filter-deezer-toggle-2026/)
- [TechCrunch — Spotify updates AI policy to label tracks, cut down on spam](https://techcrunch.com/2025/09/25/spotify-updates-ai-policy-to-label-tracks-cut-down-on-spam/)
- [Undetectr — DDEX AI Disclosure Standard](https://undetectr.com/blog/ddex-ai-disclosure-standard-explained)
- [TikTok Ads — How to use the Commercial Music Library](https://ads.tiktok.com/help/article/how-to-use-the-commercial-music-library) · [Velveteen — TikTok CML: How Artists Get In](https://www.velveteen.fm/guides/tiktok-for-musicians/tiktok-commercial-music-library-explained)
- [Orphiq — Songwriter Pitching Guide](https://orphiq.com/resources/songwriter-pitching-guide) · [Discover Sooner Monthly Pitch](https://www.discoversooner.com/monthly-pitch) · [SongU Pitching Opportunities](https://www.songu.com/pitchingOpps.aspx)
- [Music Industry How To — Songtradr Review](https://www.musicindustryhowto.com/songtradr-review/)
- [Davincii — ISWC Codes Explained](https://davincii.co/guides/iswc) · [Buzzsonic — PPL UK ISRC Registration](https://buzzsonic.com/resource/ppl-uk-isrc-registration/)
- [Verified Market Reports — Royalty Free Music Licensing Market](https://www.verifiedmarketreports.com/product/royalty-free-music-licensing-market/)

**Music generation tooling**
- [Apiframe — Best AI Music Generation APIs](https://apiframe.ai/blog/best-ai-music-generation-apis) · [aimusicapi — API Comparison](https://aimusicapi.ai/en/blog/ai-music-generation-api-comparison)
- [BIGVU — ElevenLabs Pricing 2026](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) · [invideo — ElevenLabs Music v1 to v2](https://invideo.io/blog/elevenlabs-music-ai-generator/)
- [gptproto — Suno API Guide 2026](https://gptproto.com/blog/suno-api) · [musicmake.ai — Suno Pricing Plans 2026](https://musicmake.ai/blog/suno-ai-pricing-plans-2026)

**Copyright / AI law**
- [Copyright Alliance — USCO AI Report Part 2](https://copyrightalliance.org/ai-report-part-2-copyrightability/) · [Skadden](https://www.skadden.com/insights/publications/2025/02/copyright-office-publishes-report) · [Jones Day](https://www.jonesday.com/en/insights/2025/02/copyrightability-of-ai-outputs-us-copyright-office-analyzes-human-authorship-requirement)
- [HSF Kramer — UK Government Report on Copyright and AI](https://www.hsfkramer.com/notes/ip/2026-03/uk-government-report-on-copyright-and-ai-concludes-more-evidence-is-needed-although-s9-3-cdpa-could-go) · [Bird & Bird](https://www.twobirds.com/en/insights/2026/uk/copyright-,-a-,-aiin-the-uk-the-debate-rolls-on) · [GOV.UK consultation](https://www.gov.uk/government/consultations/copyright-and-artificial-intelligence/copyright-and-artificial-intelligence)
- [PRS for Music — AI Policy (v1, Oct 2025)](https://www.prsformusic.com/-/media/files/prs-for-music/works/prs-for-music-and-artificial-intelligence-policy.pdf)
- [Orrick — EU AI Act Article 50](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50) · [European Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act) · [artificialintelligenceact.eu — Article 50](https://artificialintelligenceact.eu/article/50/)
- [Gateley — Fictionalising true stories: the legal risks](https://gateleyplc.com/insight/article/fictionalising-true-stories-the-legal-risks/) · [Brooklyn Sports & Entertainment Law](https://sports-entertainment.brooklaw.edu/film-tv/documentaries-drama-and-defamation-creators-in-court-for-real-life-portrayals/)

**Data sources / APIs / infrastructure**
- [TMDB API Terms of Use](https://www.themoviedb.org/api-terms-of-use) · [TMDB API for Business](https://www.themoviedb.org/api-for-business)
- [Spotify Developer Terms](https://developer.spotify.com/terms) · [Spotify Developer Blog, 6 Feb 2026](https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security)
- [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies) · [Phyllo — YouTube API quota limits](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota)
- [Google Sheets API — Usage limits](https://developers.google.com/workspace/sheets/api/limits)
- [The National Archives — Find Case Law public API](https://nationalarchives.github.io/ds-find-caselaw-docs/public) · [Law Gazette — Official court judgments database goes live](https://www.lawgazette.co.uk/law/official-court-judgments-database-goes-live/5112223.article)
- [ScrapeBadger — TikTok Scraping APIs 2026](https://scrapebadger.com/blog/tiktok-scraping-apis-in-2026-the-complete-deep-guide) · [Creatify — TikTok Creative Center](https://creatify.ai/blog/tiktok-creative-center)
- [n8n Docs — Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) · [n8n Docs — Queue mode](https://docs.n8n.io/hosting/scaling/queue-mode/)

---

*End of Phase 0 deliverable.*
