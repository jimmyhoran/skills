---
name: feeling-first-design
description: Design or critique a consumer-product moment by forming an evidence-backed emotional state-shift hypothesis, choosing the smallest intervention that could create it, and defining a behavioral test, user-reported measure, guardrail, and stop condition. Use when a user is designing, redesigning, or reviewing a consumer-facing flow; investigating weak adoption, trust, motivation, or retention; or asking for emotional design, behavioral design, a stickier experience, a less anxious flow, or an ethical product nudge.
license: MIT
metadata:
  author: Jimmy Horan
---

# Feeling-First Design

Treat the feeling around a product task as a hypothesis to test, not a mood to decorate onto the interface. Start with evidence about a specific user moment, define one useful emotional shift, make the smallest change that could cause it, and measure both behavior and experience.

## Operating rules

- Start from an observed moment, not a generic aspiration such as “make it delightful.”
- Choose one primary emotional shift. Add another only when the evidence requires it.
- Fix basic usability, reliability, or value problems before applying behavioral mechanisms.
- Prefer the smallest intervention that can isolate the hypothesis.
- Pair a behavioral metric with a direct user-reported measure. Behavior alone does not reveal how the user felt.
- Preserve informed choice. Never manufacture urgency, progress, scarcity, social proof, or consequences.

## 1. Frame the moment

Write down:

- **Actor:** the specific user or segment.
- **Goal:** what they are trying to accomplish in their own terms.
- **Moment:** the exact decision, action, or transition under review.
- **Evidence:** observed behavior, research, support signals, or product data.
- **Stakes:** what could be lost through error, delay, disclosure, payment, or commitment.

Separate observations from interpretations. “42% leave on the connection screen” is an observation; “they do not trust us” is a hypothesis. If evidence is missing, label the assumptions and recommend the cheapest way to investigate them.

## 2. Form a state-shift hypothesis

Describe one transition:

> At **[moment]**, the user may feel **[current state]** because **[evidence-backed cause]**. Help them feel **[desired state]** so they can **[user-benefiting behavior]**.

Make the states concrete and moment-specific. Prefer “uncertain about what will be shared → informed and in control” over “worried → delighted.” The desired state should help the user pursue their goal, not merely make the product more persuasive.

Assign **low**, **medium**, or **high** confidence and name the evidence behind that rating. Do not present an inferred emotion as a user fact.

## 3. Diagnose what could create the shift

Choose one working mechanism from the signal in front of you. These are hypotheses, not universal laws.

| Signal in the moment | Working mechanism | Candidate treatment |
| --- | --- | --- |
| The outcome, status, or consequence is unclear | Reduce uncertainty | Explain what happens next, show system status, or preview the consequence before commitment |
| The task looks larger or harder than it is | Support competence | Create a smaller first success, clarify the next action, or show only real progress |
| The path feels imposed | Preserve agency | Offer a meaningful choice, explain the default, or make the action easy to undo |
| Valuable work happens out of sight | Make real effort visible | Briefly explain actual processing or show useful intermediate results |
| A relevant answer is missing | Create useful curiosity | Preview the specific question and ensure the reveal consistently delivers value |
| The user has already made genuine progress | Recognize earned progress | Carry completed work forward and show the remaining distance honestly |

If none fits, do not force a psychological explanation. The stronger recommendation may be clearer value, fewer steps, better performance, or a product defect fix.

## 4. Design the smallest intervention

Turn the mechanism into one concrete product change. Specify:

- what changes in the interface, interaction, timing, or copy;
- why that change could produce the state shift;
- what stays unchanged so the test remains interpretable; and
- how the treatment could backfire.

For example, consider a first-run budgeting flow with a sharp drop before account connection. Do not assume users need more motivation. A testable treatment might explain the exact data requested, offer a read-only preview, and show how to disconnect later. The hypothesis is “uncertain and exposed → informed and in control,” not “add reassurance.”

## 5. Define the test before recommending launch

Write the hypothesis in this form:

> For **[segment]** at **[moment]**, **[intervention]** will help shift **[current state]** toward **[desired state]**, increasing **[behavioral outcome]**, because **[working mechanism]**.

Define all of the following:

- **Primary behavior:** the one observable action expected to change.
- **Experience measure:** a short, neutral question that checks the proposed state, such as confidence or perceived control.
- **Guardrail:** a measure that would reveal harm elsewhere, such as regret, reversal, complaints, accidental consent, or downstream abandonment.
- **Stop condition:** the result that should end or roll back the test even if the primary behavior improves.
- **Method and window:** an A/B test where volume and risk permit it; otherwise a prototype study, usability session, or staged release with a defined observation period.

Avoid metric bundles that make any result look successful. Choose the primary measure before seeing the outcome.

## 6. Run the agency review

Reject or revise the intervention if any answer is no:

1. **Truthful:** Are every claim, status, consequence, and progress indicator real?
2. **Understandable:** Can the user tell what is happening and why?
3. **Voluntary:** Can they decline without a hidden penalty or misleading obstruction?
4. **Reversible:** Can they recover when the stakes justify an undo or confirmation?
5. **Proportionate:** Does the emotional intensity match the importance of the action?
6. **Safe:** Have risks to vulnerable or high-stakes users been considered explicitly?

Do not use a survey score to excuse coercive behavior. A treatment must pass the agency review as well as the experiment.

## Output format

> **Moment and evidence:** [actor, goal, exact moment, observations, stakes]
>
> **State-shift hypothesis:** [current state → desired state → user-benefiting behavior]
>
> **Confidence:** [low / medium / high, with evidence and assumptions]
>
> **Working mechanism:** [one mechanism and why it fits]
>
> **Smallest intervention:** [concrete change, what remains fixed, possible backfire]
>
> **Test:** [hypothesis, method, segment, and window]
>
> **Measures:** [primary behavior, experience measure, guardrail, stop condition]
>
> **Agency review:** [truth, understanding, choice, reversibility, proportionality, safety]
>
> **Open questions:** [evidence still needed]

Scale the response to the ask. For a narrow critique, identify the weakest assumption and one test. For a full flow, repeat the method only for the moments that materially affect the user's goal.

## Common failure modes

- **Inventing the emotion.** Treating an analytics drop as proof of anxiety, distrust, or boredom without research.
- **Choosing a brand feeling.** Optimizing for “premium” or “exciting” when the user first needs clarity, safety, or competence.
- **Stacking interventions.** Changing copy, layout, incentives, and timing together, then learning nothing about causality.
- **Measuring behavior only.** Calling a conversion lift successful while regret, confusion, or accidental consent rises.
- **Adding psychology to a product defect.** Using persuasion to compensate for weak value, broken reliability, or needless friction.
- **Confusing honesty with softness.** Clear consequences and protective friction can be the most respectful design at a high-stakes moment.

## Research basis

The workflow is independently organized around evidence, a state-shift hypothesis, a minimal intervention, a test, and an agency review. Individual candidate mechanisms are informed by public research, including Buell and Norton's [operational-transparency research](https://doi.org/10.1287/mnsc.1110.1376), Fogg's [behavior model](https://doi.org/10.1145/1541948.1541999), Loewenstein's [information-gap account of curiosity](https://doi.org/10.1037/0033-2909.116.1.75), and Nunes and Drèze's [endowed-progress research](https://doi.org/10.1086/500480). These sources support mechanism selection; they do not prove that a particular treatment will work for a particular product or user.
