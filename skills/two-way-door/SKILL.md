---
name: two-way-door
description: Evaluate a decision using Jeff Bezos's two-way door framework, score its reversibility from 1 to 5, explain the binding cost or blast-radius constraint, and recommend proportionate deliberation. Use when someone is weighing options or approaching a consequential product, architecture, hiring, public brand, regulatory, or contractual commitment. Score distinct decisions separately when the context contains more than one choice.
license: MIT
metadata:
  author: Jimmy Horan
---

# Two-Way Door

A reversibility analyser. When the user is making a decision, score how reversible it is so they know how much deliberation it warrants.

## Core principle

From Bezos's [2015 shareholder letter](https://ir.aboutamazon.com/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF): most decisions are two-way doors. You can walk through, see what's on the other side, and walk back if you don't like it. These should be made fast, by small teams or individuals. One-way doors are decisions you can't reverse, or can only reverse at huge cost. These deserve slow, careful analysis.

The 1-5 scale below is this skill's operational extension of Bezos's binary framework; it does not appear in the source letter.

The two most common decision-making mistakes:

1. Treating two-way doors as one-way doors (overthinking, gathering more data, delaying).
2. Treating one-way doors as two-way doors (moving fast on something that can't be undone).

The point of this skill is to make the user's deliberation budget match the actual reversibility of the decision in front of them.

## When to apply

Trigger when the user is:

- Weighing a decision ("should I", "thinking about", "considering")
- Comparing options ("X vs Y", "picking between", "deciding between")
- About to commit ("going with", "leaning toward", "ready to ship", "about to send")
- Asking for input on a choice
- Drafting something that locks in a position (public posts, pricing, hires, contracts)

If the conversation surfaces multiple distinct decisions, score each separately. Do not collapse them into one rating. Common case: a product spec contains three architectural choices, each with different reversibility profiles.

If the user has not explicitly asked for an analysis but is clearly mid-decision and the reversibility would change their approach, surface the rating proactively. Be brief about it.

## The rubric

Assess the decision across these dimensions before assigning a rating:

1. **Reversibility cost.** How expensive (time, money, effort) is it to undo?
2. **Blast radius.** Who and what does it affect? Internal only? Users? Public? Regulators?
3. **Commitment signal.** Does reversing damage trust, credibility, or relationships?
4. **State irreversibility.** Does it destroy or permanently alter data, code, or position?

The final rating reflects the dominant constraint, not the average. A decision that is technically easy to reverse but signals weakness if reversed (e.g. pricing) is bounded by the signal cost.

## The 1-5 scale

**1. Two-way door (free).** Easily reversed within hours, internal only, no signal cost.
Examples: drafting a tweet, picking a font, naming a Slack channel, choosing folder structure, internal tool selection.

**2. Mostly two-way.** Reversible within days to a week, low signal cost.
Examples: feature behind a flag, adopting a new internal tool, choosing a JS library for a non-core module, internal process changes.

**3. Mixed.** Reversible with real effort and some signal cost.
Examples: public product launch, hiring a contractor, vendor selection with a 3-month contract, non-breaking schema additions, choosing a domain you haven't promoted yet.

**4. Mostly one-way.** Reversing is expensive, public, or damaging.
Examples: full-time hire, raising a priced round, destructive DB migration, public pricing change, partnership announcement, choosing a primary tech stack post-traction.

**5. One-way door.** Effectively irreversible.
Examples: layoffs, selling the company, changing the company name post-traction, IPO, deleting production data, signing a multi-year exclusive, public co-founder split, regulated licensing commitments.

## Output format

For a single decision:

> **Decision:** [one-line summary of what's being decided]
> **Rating:** [N/5, label from the scale]
> **Why:** [1-2 lines on the dominant reversibility factor]
> **Deliberation:** [recommended depth, see below]

For multiple decisions in context, repeat the block per decision, in the order they appear.

Keep the block tight. The user wants a rating and the reasoning behind it, not an essay.

## Deliberation guidance by rating

- **1-2.** Decide and move. Don't gather more input unless something specific is genuinely unknown. Minutes to a couple of hours of thought, maximum.
- **3.** Sleep on it. One round of input from someone trusted. Half a day of analysis at most.
- **4.** Real analysis. Pre-mortem (what would make you regret this in 6 months?), 2-3 advisors, written rationale. Days, not hours.
- **5.** Maximum scrutiny. Written argument, multiple advisors, specialist input (lawyer, accountant, etc.) if relevant, deliberate time delay before final commit. Resist time pressure unless it's a genuine forcing function.

## Common failure modes

- **Reversibility theatre.** Treating something as "easily reversible" when the *signal* cost of reversing is high. Pricing changes are technically a config update. Reversing one within a month damages trust badly.
- **Sunk cost trap.** Confusing "already invested heavily" with "irreversible". Money already spent is irrelevant. Only future cost to undo matters.
- **Component fallacy.** A reversible feature inside an irreversible architecture is bounded by the architecture's reversibility. Score the binding constraint, not the local one.
- **Domain blindness.** In regulated industries (fintech, health, legal), decisions that look like two-way doors often have one-way regulatory or compliance footprints (data retention, audit trails, license terms, KYC records). Default the rating higher when in doubt.
- **Public commitment creep.** A blog post, podcast appearance, or LinkedIn announcement turns a 2 into a 4 by adding signal cost. Note this in the rating if the user is about to make the decision visible.
- **Reversible-now, irreversible-soon.** A decision can be a 2 today and a 4 in 12 months as the system grows or audience expands. Score for current state, but flag if the rating is likely to shift.

## Calibration notes

- Default to lower ratings when genuinely ambiguous. Most decisions really are two-way doors. The cost of mis-scoring upward is wasted deliberation. The cost of mis-scoring downward can be unrecoverable damage. So when the difference between two ratings matters and the user is about to act, err high.
- Brand and naming decisions are often underrated. A name is a 2 before launch and a 4 after any traction.
- Hiring decisions are usually 4, not 5. Firing is hard but possible. Treat as a 5 only when the hire is a co-founder, executive with equity, or someone whose departure would be public.
- Architectural decisions compound. A 3 today that locks in 6 months of further work becomes a 4. Look at what the decision *enables* and *forecloses*, not just the decision itself.
- For drafts of public content (tweets, posts, emails to investors), the *unsent* draft is a 1. The *sent* version is whatever the audience and content make it (often a 3 for visible founder posts, higher for investor or regulator comms).
