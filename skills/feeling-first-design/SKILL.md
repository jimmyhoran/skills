---
name: feeling-first-design
description: Design or critique a consumer-app feature so users adopt it because of how it makes them feel, not just what it does. Runs an emotional-design lens (name the three target feelings), pulls the right behavioral-psychology levers for that moment in the journey, turns each into a testable experiment with a metric, and screens for the dark-pattern trap. Use when the user is designing, redesigning, or reviewing a consumer-facing flow — onboarding, activation, retention, engagement, habit, growth/viral, monetization, conversion, trust, or premium positioning — or says things like 'make this feature stickier', 'why won't users adopt this', 'design the onboarding', 'this flow feels flat', 'add a growth loop', 'behavioral design', 'emotional design', or 'what psychological lever fits here'.
metadata:
  author: Jimmy Horan
  version: "1.0"
---

# Feeling-First Design

A behavioral-design method for consumer apps. Function is table stakes; the apps that get adopted instantly engineer a *feeling* at each step. This skill takes a moment in the product and produces a treatment: the target emotion, the psychological lever that triggers it, the experiment that tests it, the metric that proves it, and the trap that would make it a dark pattern.

## Core principle

Good products solve the task. The best products shape the feeling around it. Users return to Duolingo to feel *disciplined*, to Strava to feel *athletic*, to Airbnb to feel *adventurous* — the function is the excuse, the feeling is the reason. So design backwards from emotion: decide what a flow should make the user *feel*, then choose the mechanic that produces it. Designing from named psychological principles beats guessing, and beats copying a competitor's surface without knowing why it works.

This is a lens and a lever set, not a checklist to run top-to-bottom. Pull the one or two levers that fit the moment; most of them interlink, so the leverage is in the pairings.

## Step 1 — Run the Emotional Design Lens

Before any mechanic, name the **three feelings** the flow should leave the user with. Write them first. If you can't name them, you're designing function, not experience — stop and find them.

The format is *mundane function → emotional payoff*:

- "Duolingo teaches Spanish." → *Productive · Disciplined · Intelligent*
- "Strava tracks runs." → *Accomplished · Admired · Athletic*
- "Airbnb finds places to stay." → *Adventurous · Spontaneous · Freedom*

Then sanity-check against the user's real emotional state at that moment. A high-anxiety step (handing over money, granting access, first use) needs *calm / safe / in-control* before anything clever. Match the feeling to the stakes.

## Step 2 — Locate the moment in the journey (the 12 stacks)

A feature usually lives in one stack but pairs across several. Locate it, because the right lever depends on where in the arc the user is.

1. **Onboarding** — first value, least friction, right first feeling
2. **Activation** — reach the "aha", the moment core value lands
3. **Retention** — earn the next session
4. **Engagement** — depth and quality within a session
5. **Habit Formation** — make returning automatic, not deliberate
6. **Growth & Viral** — users bring users as a byproduct of getting value
7. **Monetisation** — capture revenue in proportion to value delivered
8. **Conversion** — move people across a threshold (signup, free→paid)
9. **Trust Building** — earn the right to handle their data/money
10. **Intent Shaping** — guide what the user does next
11. **Experience Refinement** — polish, delight, perceived performance
12. **Premium Positioning** — feel high-end, worth paying for, worth talking about

## Step 3 — Pull the lever

Each lever is a named, public behavioral principle and the moment it fits. Pick by the feeling you named in Step 1. Pairings (→) are where the leverage compounds.

**Onboarding & Activation**
- **Labor Illusion** (Norton & Buell) — narrate the invisible work ("scanning 1,243 items…") so the result feels earned, not cheap. → Credibility Borrow
- **Progressive Disclosure** (Sweller, cognitive load) — reveal complexity only as the user is ready; default the smart choice; one concept per screen.
- **Micro-Commitment Ladder** (Cialdini, commitment & consistency) — chain tiny escalating yeses instead of one big ask; bank each visibly. → Goal Mirror
- **Aha Shortcut** (time-to-value) — find your magic-moment threshold (Facebook's *7 friends in 10 days*), then delete everything between signup and it.
- **Reciprocity Primer** (Cialdini/Gouldner) — give one real, free insight *before* the costly ask; the gift earns the ask. → Curiosity Gap
- **Goal Mirror** (self-reference + commitment) — ask the user's goal in their words, reflect it back across the next screens.

**Retention, Engagement & Habit**
- **Variable Reward** (Skinner, variable-ratio; Eyal) — vary the *magnitude/form* of a genuine payoff; dopamine spikes on anticipation. Never vary facts, only insights.
- **Return Trigger** (Eyal, trigger→action) — fire the external nudge on the user's *internal* state (a routine, an event, a threshold), so it lands as help, not noise.
- **Zeigarnik Open Loop** — leave something genuinely, visibly incomplete ("2 of 3 done") so the mind wants to close it. → Return Trigger, Endowed Progress
- **Curiosity Gap** (Loewenstein, information gap) — lead with the question, not the answer; make the reveal worth the tap *every time*.
- **Endowed Progress** (Nunes & Drèze) — start the bar with real credit already earned; "finishing" beats "starting".
- **Goal Gradient** (Hull; Kivetz) — emphasize how *little* is left; accelerate visible progress near the finish.
- **Streak** (loss aversion) — reward a visible chain the user won't break; make it forgiving; aim it at healthy regularity, not compulsion.
- **Habit Stacking** (Gollwitzer; Clear) — anchor the behavior to an existing routine ("after I do X, I do Y"); let the user pick the anchor.
- **Cue-Routine-Reward** (Duhigg; Fogg B=MAP) — design the whole loop: a reliable cue, an action made trivially easy, a reward that closes it. Lower the ability barrier before raising motivation.
- **Personalization Loop** (IKEA effect / data network effect) — make the product visibly better the more the user puts in, and show that it did.

**Growth & Viral**
- **Collaborative Invite** — build value that *increases when the inviter pulls someone in*; invite as a feature, not a favor. → Embedded Invite
- **Status Share** (Berger, social currency) — auto-generate a beautiful, brag-worthy, privacy-safe artifact at genuine achievement peaks.
- **Embedded Invite** (classic viral loop) — every user-generated output carries a tasteful soft invitation; distribution as a byproduct of normal use.

**Monetisation, Conversion & Premium**
- **Value-Metric Alignment** (value-based pricing) — price on the axis that scales with value received; never price on the behavior you want to encourage.
- **Earned Upgrade Moment** (contextual paywall) — surface the upgrade at the instant the user hits the value ceiling, showing the specific thing they'll unlock.
- **Reverse Trial** (endowment + loss aversion) — give full premium up front, then let them keep it; downgrading feels like a loss.
- **Anchor & Decoy** (Tversky/Kahneman; Ariely) — high anchor first, target plan as the obvious value; keep anchors honest.
- **Loss-Framed Nudge** (prospect theory) — frame the *real* cost of inaction; losses loom ~2× gains. Only for losses that genuinely exist.
- **Friction Audit** (Hick's Law) — cut every non-essential field/step from a conversion flow; defer, default, pre-fill.
- **Identity Upgrade** (self-signaling) — sell the *person the user becomes*, backed by features — not a feature checklist.
- **Exclusivity Frame** (scarcity) — give premium a genuine membership feel; real selectivity, never fabricated countdowns.
- **Premium Aesthetic Signal** (aesthetic-usability / halo) — use visible craft and restraint as a proxy for quality and safety, especially where trust is being judged.

**Trust, Intent & Experience**
- **Transparency Default** (reduces reactance; Langer's "because") — explain the *why* behind every data request and automated action, before the user asks.
- **Calm Confirmation** — for irreversible/high-stakes actions, confirm with clarity and a clear way out; *good* friction that signals care.
- **Credibility Borrow** (authority + social proof) — surface true authority/social-proof signals exactly where doubt peaks (the sensitive step, the first commitment).
- **Default Path** (Thaler & Sunstein) — set the smart default so the path of least resistance serves the user; make changing it trivial.
- **Single Next Best Action** (Hick's Law; paradox of choice) — reduce any moment to one obvious, high-value next step; demote the rest.
- **Peak-End Rule** (Kahneman & Redelmeier) — deliberately design the emotional peak and the ending; spend the delight budget there, never end on an upsell.
- **Delightful Detail** (aesthetic-usability; Norman) — craft at key beats signals quality; match tone to stakes; delight that slows the user is friction.
- **Perceived Performance** (optimistic UI) — respond to input instantly, skeletons not spinners; never fake the state of something that must be correct.

*In crowded, feature-parity categories (e.g. the wave of AI-wrapper apps), craft and feeling are often the only remaining wedge — differentiation is a growth lever, not a finishing polish.*

## Step 4 — Turn it into an experiment

Each lever becomes a testable change. Write it as: **the moment** → **the feeling** → **the lever** → **the concrete move** → **the metric that moves if it worked** → **the trap to avoid**. That's a ready A/B test, not a vibe.

Instrument the stack's core metric *before* shipping:

| Stack | Core metric | Definition |
| --- | --- | --- |
| Onboarding | Time-to-value, completion % | signup → first-value time; % completing setup |
| Activation | Activation rate | users reaching the aha ÷ signups |
| Retention | D1/D7/D30, resurrection | % active N days after signup; % dormant returning |
| Engagement | Stickiness, depth | DAU÷MAU; actions per session |
| Habit Formation | Habit rate | % users with ≥N qualifying sessions/week; streak survival |
| Growth & Viral | K-factor, cycle time | invites/user × invite→join rate; time per loop |
| Monetisation | ARPU/ARPPU, expansion | revenue ÷ users; per paying user; expansion rev |
| Conversion | Funnel CVR, trial→paid | completions ÷ entries per step; paid ÷ trials |
| Trust Building | Grant rate, trust signal | permission/link grant %; trust survey/NPS |
| Intent Shaping | Next-action take rate | % taking the recommended action; default-acceptance % |
| Experience Refinement | NPS/CSAT, perceived speed | post-flow survey; interaction→feedback latency |
| Premium Positioning | WTP, premium CVR | willingness-to-pay; conversion on premium surfaces |

## Output format

> **Moment:** [the flow/feature and its stack]
> **Target feelings:** [three, from the lens]
> **Lever(s):** [1–3 named levers + why they fit this feeling]
> **The move:** [concrete design change, in the product's own terms]
> **Experiment:** [what you'd A/B test]
> **Metric:** [the stack metric that should move]
> **Dark-pattern check:** [the specific trap and how this stays honest]

Scale depth to the ask. A single "make this stickier" earns one lever and its trap; a full flow design earns the lens, two or three paired levers, and the experiment set.

## Common failure modes

- **Designing function, not feeling.** Shipping a flow without naming the three target emotions. The lens is Step 1 for a reason — skip it and every later choice is a guess.
- **Cargo-culting a competitor's surface.** Copying Duolingo's streak without asking whether the behavior *should* be daily. Recommend a lever only when you can name the principle and the feeling it produces here.
- **Varying facts, not insights.** Variable reward belongs on what an insight *found*, never on balances, statuses, or anything that must be deterministic. Surprising a user with the state of their own data destroys trust.
- **Friction blindness.** Stripping *protective* friction (a confirm on an irreversible action) in the name of conversion. Distinguish friction from safety before cutting it.
- **Manufactured everything.** Fake progress bars, fake scarcity ("3 left!" that resets), fear-bait curiosity gaps, anxiety-driven streaks. Manufactured mechanics read as manipulation the moment they're noticed and cost more trust than they buy.
- **The dark-pattern line.** Every lever here is a persuasion mechanic; the same lever builds a genuine habit or a compulsion depending on intent. The test: *would the user thank you for this if they fully understood it?* If yes, ship it. If no, it's a dark pattern — cut it. The ethical move and the effective move are usually the same one, because users adopt what makes them feel capable and in control, and abandon what makes them feel used.

## Provenance

The *system* here — the emotional-design lens, the 12-stack journey, the card/lever method, and the metrics-and-diagnosis layers — is modelled on the structure of Bartek Marzec's paid "Product Design Playbook" ([consumerapp.studio](https://www.consumerapp.studio/)). The lever bodies are original and grounded in named, public behavioral research (Cialdini, Kahneman & Tversky, Eyal, Fogg, Duhigg, Clear, Berger, Thaler & Sunstein, Ariely, Loewenstein, Nunes & Drèze, Norton & Buell, Norman/Tractinsky); nothing is copied from the paywalled product. The "craft as the wedge in crowded categories" note reflects a complementary design-differentiation thesis (Satya / Kree8, [@heysatya_](https://x.com/heysatya_)).
