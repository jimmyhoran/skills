---
name: funnel-teardown
description: Tear down a competitor's (or your own) complete offer — funnel, landing page, lead magnet, upsell path, pricing strategy, emails, and CTAs — then connect the dots into four answers, why people buy, where people drop off, what's missing, and where money is being left on the table. Use when the user wants to analyze a competitor's funnel or offer, shares a competitor's landing page, pricing page, or email sequence and asks what's working, or says things like 'tear down this funnel', 'funnel audit', 'offer teardown', 'why do people buy from them', 'where are they leaving money on the table', 'what can I steal from their funnel', or 'find the gaps in this offer'.
license: MIT
compatibility: Requires network and web-browser access to inspect live funnels. Gated steps may require user-provided screenshots or emails, or authorized account access supplied by the user.
metadata:
  author: Jimmy Horan
---

# Funnel Teardown

Investigate a complete offer end-to-end, then synthesize. The inventory is not the deliverable. The four answers at the end are.

## Core principle

Every offer is a system: traffic → landing page → lead capture → nurture → core offer → upsell → retention. Most funnel analysis fails in one of two ways: it reviews a single asset in isolation (a landing page critique that ignores what the emails promised), or it produces an inventory with no synthesis (a list of what exists, no view on what it means). A teardown does neither. It maps every component, walks the path as the target buyer, and answers:

1. **Why people buy** — the psychological engine of the offer.
2. **Where people drop off** — the specific leaks, with reasoning.
3. **What's missing** — gaps versus a complete funnel.
4. **Where money is left on the table** — absent monetization mechanisms.

Works on a competitor's funnel (find opportunities to exploit) or the user's own (find leaks to fix). Ask which framing applies if unclear — it changes the final recommendations, not the investigation.

## Gathering the assets

Collect before analyzing. Evidence beats inference: a fetched page beats a screenshot beats memory of the brand. Label anything you could not verify as inference.

- **Public assets** — fetch them yourself when URLs are available (web fetch or browser tools): landing pages, pricing page, blog/SEO entry points, ad library pages (Meta Ad Library, Google Ads Transparency Center).
- **Gated assets** — ask the user to provide them rather than inventing them: email sequences (suggest they opt in with a throwaway address), checkout screens, upsell/OTO pages, in-app paywalls, cancellation flows.
- **Entry point matters** — a funnel from a Meta ad often differs from the SEO funnel. Note which entry point you analyzed; don't present one path as the whole system.

If key assets are unavailable, proceed with what exists, and list the missing assets in the report — an unverifiable component is itself a finding, not a gap to paper over.

## The investigation

Work through each component with these questions. Skip nothing; if a component doesn't exist, that goes in "what's missing".

**Funnel map.** Entry points (ads, SEO, social, referral). Number of steps from first touch to first dollar. Free-to-paid path (trial, freemium, lead magnet → pitch, demo/sales call). Is there an ascension ladder (cheap entry offer → core → premium) or one product at one price? What does the post-purchase path look like?

**Landing page.** What does the headline promise — an outcome, a mechanism, or a feature? Pass the above-the-fold test: could a stranger say what this is, who it's for, and why it's different in five seconds? Awareness level targeted (problem-aware vs solution-aware vs product-aware) — does the page match how cold its traffic is? Proof stack: testimonials, numbers, logos, and whether they're specific or decorative. Risk reversal: guarantee, free trial, "cancel anytime". Urgency/scarcity, and whether it's real or manufactured. Friction: form length, number of competing links and asks.

**Lead magnet.** What it promises and how specific the promise is. Time-to-value: consumed in five minutes or shelved forever? The critical question: does consuming it make the reader *more likely to need the paid product* (it advances them toward the sale) or is it unrelated goodwill? What contact data is captured, and what does that imply about how they sell?

**Upsell path.** Order bump at checkout? One-time offer after purchase? Downsell when declined? Timing — before payment, immediately after, or later by email? Price relative to the core offer. Logic: does the upsell complete the job the core offer started, or is it a random second product?

**Pricing strategy.** Tiers, names, and what each name signals. Anchoring: is an expensive tier there to sell the middle one? Monthly/annual toggle and the discount for annual. What's held back to force upgrades (seats, limits, features)? Guarantee terms. Free trial vs money-back vs neither. What the structure implies about their unit economics and who their best customer is.

**Email.** Welcome sequence: length, cadence, and the mix of value emails vs pitch emails. Angle: story-driven, feature-driven, discount-driven? Is there a deadline mechanism (closing cart, expiring offer)? Signals of segmentation or behavioral triggers (abandoned cart, browse, trial expiry)? What does each email ask the reader to do?

**Calls to action.** Is there one consistent ask per page, or scattered competing asks? Verb + outcome ("Start closing more deals") or generic ("Learn more", "Submit")? Do CTAs escalate sensibly across the funnel (low-commitment early, purchase later), and does the ad's CTA match the landing page it lands on?

## Connecting the dots

This is the deliverable. Each answer must cite evidence from the investigation — a synthesis that could have been written without the assets is a failed teardown.

**Why people buy.** Name the dominant buying trigger (pain relief, fear, status, identity, ROI) and the offer's mechanism of belief — the specific thing that makes a skeptic think "this will work for me": a demo, a guarantee, a founder story, overwhelming proof, a free result delivered before payment. Identify which asset does the heaviest lifting. For B2B offers, separate the champion from the signer — the answer may differ per role, and the funnel has to sell to both.

**Where people drop off.** Walk the funnel as a skeptical member of the target audience. Drop-off happens where demanded effort or trust exceeds the motivation built so far — a 14-field form after a vague headline, a $2,000 price with no proof, a credit-card wall on a "free" trial. Name the top two or three leaks, each with the friction-vs-motivation reasoning. Never just point at a step and say "people might leave here".

**What's missing.** Compare against the complete system: retargeting, risk reversal, proof near the CTA, downsell, annual option, abandoned-cart sequence, win-back, referral loop, post-purchase ascension. Only list absences that matter for *this* business model — a missing order bump is irrelevant to enterprise sales-led SaaS.

**Money on the table.** Concrete absent mechanisms with a revenue story: no order bump at checkout, no annual toggle (cash-flow and churn), no cart-abandonment sequence, no expansion path after the core purchase, no win-back for churned customers, one-price offer with no premium tier for whales. For each, state what adding it would plausibly capture and why it fits their model.

**Then turn it into moves.** For a competitor teardown, end with three lists: *steal* (validated mechanics worth adapting), *exploit* (their gaps you can win on), *avoid* (their visible mistakes). For a self-teardown, end with fixes ranked by expected impact over effort.

## Output format

> **Offer:** [what's being sold, price, business model]
> **Entry point analyzed:** [which path, what evidence was available, what was missing]
>
> **Component findings:** [per component: 2-4 lines of the sharpest observations — not everything you noticed]
>
> **Why people buy:** [trigger + mechanism of belief + heaviest-lifting asset]
> **Where people drop off:** [top 2-3 leaks with reasoning]
> **What's missing:** [gaps that matter for this model]
> **Money on the table:** [absent mechanisms + revenue story]
>
> **Moves:** [steal / exploit / avoid — or ranked fixes for a self-teardown]

Scale depth to evidence. A full teardown with pages, pricing, and emails in hand earns the full format; a single landing page with nothing else earns component findings for that page and clearly-labeled inference for the rest.

## Common failure modes

- **Inventory without synthesis.** Describing every asset and stopping. The four questions are the product; the checklists only exist to feed them.
- **Guessing dressed as observation.** If you didn't see the emails, say so and reason from what the opt-in promises. Mark every inference as inference.
- **Cargo-cult swiping.** A big competitor's funnel is not a validated funnel — they may be testing, wrong, or winning despite it (brand, sales team, capital). Recommend stealing mechanics only when you can articulate *why* they work.
- **Judging by your own taste.** You are not the buyer. A page that feels hypey to you may convert cold traffic at problem-level awareness. Critique against the target buyer and traffic temperature, not personal aesthetics.
- **Snapshot blindness.** Funnels vary by traffic source, geography, and device, and change weekly. State what you analyzed and when; don't generalize one path into "their strategy".
- **Invisible-funnel fallacy.** The public funnel may not be the real funnel — sales teams, communities, DMs, partnerships, and retargeting are mostly invisible from outside. Flag when the visible economics don't add up; that usually means a hidden channel is doing the selling.
