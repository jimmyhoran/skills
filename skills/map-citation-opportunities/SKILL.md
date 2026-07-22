---
name: map-citation-opportunities
description: Discover, verify, and rank legitimate third-party listing, review, editorial, community, integration, and owned-content opportunities by auditing live sources and brand recommendations for buyer-intent queries across AI search engines. Use when the user asks which Perplexity, ChatGPT, or Google AI citations to target, why competitors appear in "best" or comparison answers, where citation evidence suggests earning backlinks or brand mentions, or for a repeatable off-site AI-visibility map. Works for consumer, B2B, developer, local, marketplace, and mixed products. Do not use merely to execute an already-chosen directory list or optimize owned pages without a source audit; use directory-submissions or ai-seo for those tasks.
---

# Map Citation Opportunities

Turn a sample of live AI-search answers into an evidence-backed opportunity backlog. Map where buyers and engines currently obtain information, then identify legitimate ways for the product to become present there.

Do not treat a citation panel as a submission list. A source can be cited without mentioning the brand, and a brand can be mentioned without being recommended.

## Set the scope

Read project context before asking questions. Check, in order:

1. `.agents/product-marketing.md`
2. `.claude/product-marketing.md`
3. `product-marketing-context.md`
4. Repository documentation and the live public site

Resolve or ask only for missing essentials:

- Product URL and canonical brand name
- Offering type: consumer, B2B, developer, local, marketplace, or mixed
- Category and plain-language problem solved
- Primary buyer, use cases, market, and language
- Main competitors and substitutes
- Objective: baseline, opportunity map, competitive diagnosis, or recurring monitor

State assumptions when the category or audience remains ambiguous. A consumer product must not inherit a SaaS-heavy source plan merely because software directories are easy to find.

## Check citation-surface access

Before choosing the audit depth, inventory the answer surfaces actually available. A citation audit requires both a generated answer and a visible source or citation interface that can be inspected.

- **One or more citation surfaces available:** run the audit at the appropriate depth and report the exact coverage.
- **No citation surfaces available:** label the result `partial — citation surfaces unavailable`. Do not simulate answers, calculate visibility-ladder rates, or assign recurrence above 0. Ordinary search may be used only as separately labeled reconnaissance to test prompts and discover candidate source types. Return the proposed prompt set, a low-confidence candidate backlog, and the access needed to complete the baseline.

A browser, API, or search tool that returns ordinary ranked links is not by itself an AI citation surface.
Treat login walls, regional restrictions, bot challenges, and CAPTCHAs as unavailable access unless the user provides a legitimate interactive route. Do not bypass them.

## Choose the audit depth

Match the sample to the decision and available access:

- **Quick scan:** 5-8 prompts on one or two available search-enabled engines. Label it a directional snapshot.
- **Standard map:** 8-12 prompts across at least two available engines, with the 2-3 highest-value prompts repeated in fresh sessions.
- **Monitoring baseline:** Preserve the standard prompt set, engine or surface, locale, and observation settings for later reruns.

Use only engines and account surfaces actually available. Never simulate unavailable answers or merge ordinary web results into an AI-citation dataset without labeling them separately. Do not incur paid API usage or change an account plan without authorization.

Read [references/methodology.md](references/methodology.md) when designing a new prompt set, changing the scoring method, explaining confidence, or resolving a citation-versus-recommendation ambiguity.

## Build buyer-intent prompts

Select natural prompts from the families that match the product:

| Family | Pattern | Purpose |
| --- | --- | --- |
| Category discovery | `best [category]` | Identify default shortlists and category authorities |
| Use case | `best [category] for [job/context]` | Reveal fit-specific sources and recommendations |
| Audience | `[category] for [persona/company type]` | Separate consumer, B2B, developer, and vertical sources |
| Alternatives | `alternatives to [competitor] for [constraint]` | Find comparison and switching surfaces |
| Comparison | `[brand A] vs [brand B] for [job]` | Expose evaluation criteria and evidence gaps |
| Trust | `[category] reviews`, `is [brand] good for [job]` | Find review, community, analyst, and reputation sources |
| Geography | `best [category] in/for [market]` | Capture local availability and regional authorities |

Prefer queries a real buyer would ask. Do not add instructions such as "use these sources" or "cite directories" to a baseline prompt; that changes the source mix being measured. Enable the product's normal search mode when one exists.

Run repeated prompts in fresh sessions so prior conversational context does not contaminate the comparison. Record material settings rather than pretending results are universal.

## Capture observations

For every answer, record:

- Exact prompt
- Engine, product surface, and mode or model when visible
- Evidence surface type: AI answer, deep research, ordinary search, official policy, or live source page
- Locale or market, language, and observation timestamp
- Answer or share URL when available
- Every cited page URL, not only its root domain
- Whether the answer cites an owned brand page, names the brand, recommends it, hedges it, or recommends against it
- Whether each cited third-party page contains the brand and in what context
- Which claim the source supports: category definition, evaluation criteria, product fact, social proof, comparison, or recommendation
- Other brands recommended and their position or framing

Inspect the cited page. Do not infer that a cited domain contains the target brand. Separate these rungs:

1. **Retrieved:** the engine may have read the page, but this is usually not observable.
2. **Cited:** the page appears in the visible source set.
3. **Mentioned:** the answer names the brand.
4. **Recommended:** the answer puts the brand on the buyer's shortlist.
5. **Recommended against:** the answer explicitly rules the brand out or attaches a material warning.

Treat citation frequency as the count of distinct prompt-engine observations, not the number of links displayed in one answer.

## Convert sources into opportunities

Normalize cited URLs while preserving the exact source page. Classify each opportunity by the legitimate action available:

| Type | Legitimate path |
| --- | --- |
| Claimable profile or directory | Claim, create, or correct an eligible listing |
| Review platform or app store | Establish the profile and invite genuine users under current platform rules |
| Editorial, analyst, newsletter, or listicle | Pitch a relevant inclusion, correction, data point, or expert contribution |
| Community or forum | Participate helpfully where the product is genuinely relevant; do not manufacture mentions |
| Integration or partner marketplace | Build or document a real integration before applying |
| Dataset, registry, or knowledge source | Submit accurate structured facts through its official process |
| Owned content | Publish or improve the source page that answers the observed evidence gap |
| Unattainable or inappropriate | Record competitors, closed publications, and conflict-of-interest surfaces without inventing a route |

One domain can produce multiple opportunities. A review page, category page, and editorial guide on the same site have different requirements and recommendation leverage.

## Verify attainability live

Before ranking a source as actionable, verify current information from official documentation or the live interface:

1. Confirm that the product type, maturity, geography, and language are eligible.
2. Find the official submission, claim, correction, partnership, or editorial-contact route.
3. Record free, paid, reciprocal-link, review-count, and moderation requirements.
4. Check whether representative pages are public, indexable, current, and relevant to real buyers.
5. Inspect a representative outbound link in rendered HTML when link status matters. Keep the target product's link status as `unknown` until its own listing is live.
6. Distinguish editorial inclusion from sponsored placement. Paid or reciprocal links must not be pursued to pass ranking credit.
7. Date every volatile fact and retain the official evidence URL.

Do not rank opportunities by root-domain DR. Domain Rating and similar metrics may be included as optional context, but are not search-engine scores and do not establish page relevance, indexability, referral value, or AI recommendation influence.

## Score without false precision

Score every verified candidate from 0-3 on these dimensions and retain the component scores:

- **Buyer fit:** relevance to the target audience and query
- **Recurrence:** appearances across distinct prompts, engines, or snapshots
- **Attainability:** clarity and realism of the legitimate path
- **Recommendation leverage:** likelihood that presence could affect shortlist inclusion rather than only supply a background fact
- **Audience value:** credible direct discovery or referral potential
- **Effort:** time, assets, customer participation, and monetary cost
- **Risk:** spam, conflict-of-interest, reputational, legal, or platform-policy risk

Use this only as a sorting aid:

`priority = 2*buyer_fit + 2*recurrence + 2*attainability + recommendation_leverage + audience_value - effort - risk`

Do not hide judgment behind the total. A lower-scoring high-trust editorial opportunity can be more valuable than several easy directory listings. Reject an opportunity when the only path is deceptive or policy-violating, regardless of score.

Assign confidence separately:

- **Low:** one observation, unclear source role, or unverified route
- **Medium:** repeated within one engine or prompt family and the route is verified
- **High:** recurring across at least two prompt families and across two engines or observation dates, with both the source role and route verified

Candidates found only through ordinary search reconnaissance have recurrence 0 and low observation confidence, even when their action route is well verified.

## Produce the opportunity map

Return:

1. **Scope and coverage** — product type, market, engines, prompts, repeats, date, and limitations
2. **Visibility ladder baseline** — cited, mentioned, recommended, and recommended-against rates by prompt family
3. **Source pattern summary** — recurring domains, exact pages, source types, and which claims they support
4. **Ranked backlog** — source, evidence, opportunity type, fit, legitimate route, cost, component scores, confidence, next action, and owner or dependency
5. **Now / next / later queue** — a bounded action sequence, not an indiscriminate submission dump
6. **Content and consensus gaps** — what the brand itself must publish versus what the broader web must corroborate
7. **Measurement plan** — preserved prompt set, recheck date, and success signal

In degraded mode, omit the visibility ladder and source recurrence claims. Replace them with an explicit access limitation, the unrun prompt plan, and a search-layer reconnaissance section labeled `not AI-citation evidence`.

Use [assets/opportunity-tracker.csv](assets/opportunity-tracker.csv) when the user asks for a persistent tracker. Copy it into the user's chosen project location; do not modify the template in place. Do not create project artifacts for a read-only audit unless requested.

Report these states separately: `identified`, `verified`, `drafted`, `submitted`, `accepted`, `live`, `indexed`, `brand mentioned`, and `brand recommended`. Never report submission as acceptance or citation as recommendation.

## Respect the execution boundary

Mapping and verification are read-only by default. Do not submit forms, create profiles, request reviews, publish content, send pitches, or modify production systems unless the user asks for that action.

For execution, use these related skills when they are available:

- Use `directory-submissions` for eligible directory and launch-platform work.
- Use `ai-seo` for owned-page citation and recommendation gaps.
- Use `search-discovery` after new or materially changed owned URLs are published.
- Use the appropriate outreach, community, PR, or review workflow for earned mentions.

Preserve the map as the evidence layer even when another workflow executes the action.

## Guardrails

- Never buy, automate, or exchange links for ranking manipulation.
- Never fabricate reviews, testimonials, community discussions, editorial independence, or customer experience.
- Never condition a review incentive on positive sentiment. Check the platform's rules and applicable jurisdiction before offering any incentive, and disclose it when required.
- Never directly promote through a conflict-of-interest knowledge surface when its rules require independent coverage or disclosure.
- Never scrape or automate a site where its terms or access controls prohibit it.
- Never promise indexing, citation, ranking, referral traffic, or recommendation.
- Prefer accurate corrections, genuine customer evidence, useful contributions, real partnerships, and editorially earned coverage.
