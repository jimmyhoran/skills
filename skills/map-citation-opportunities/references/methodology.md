# Citation Opportunity Mapping Method

Use this reference to design a defensible audit, explain its limits, or revise the scoring model. Keep live platform facts in the opportunity tracker with an observation date rather than hard-coding a directory catalog here.

## Evidence behind the method

- [Perplexity's product documentation](https://www.perplexity.ai/help-center/en/articles/10352895-how-does-perplexity-work) says it searches the web in real time and exposes citations. Treat those citations as observable evidence, not as a stable ranking report.
- [OpenAI's ChatGPT Search documentation](https://help.openai.com/en/articles/9237897) explains that a prompt may be rewritten into one or more targeted searches and that general location can affect results. Record prompt, surface, and locale; do not assume the visible wording is the only retrieval query.
- [Google's generative AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) says normal technical eligibility and useful, people-first content remain the foundation, and warns against manufacturing many query variants to manipulate AI answers.
- The KDD 2024 paper [GEO: Generative Engine Optimization](https://doi.org/10.1145/3637528.3671900) established that source presentation can affect generative-engine visibility. It does not justify assuming that a citation automatically creates a brand recommendation.
- The audit study [Generative AI Search Engines as Arbiters of Public Knowledge](https://arxiv.org/abs/2405.14034) sampled multiple systems over multiple days. This supports using repeated, cross-surface observations rather than presenting a single answer as stable truth.
- [Ahrefs' own guidance](https://help.ahrefs.com/en/articles/907673-do-search-engines-use-domain-authority-domain-rating-as-a-ranking-factor) states that Domain Rating is not known to be a search-engine ranking factor. Use it only as optional third-party context.

## Sampling rules

1. Build prompts from actual buyer decisions, not from phrases chosen only because they produce convenient citations.
2. Keep the baseline prompt neutral. Do not ask the engine to prefer directories, reviews, Reddit, recent sources, or a named domain unless that preference is itself the experiment.
3. Use fresh sessions for repeats. Record whether the user was logged in, search was enabled, a model or mode was selected, and location or language could affect the answer.
4. Keep ordinary search results, AI answer citations, and deep-research outputs as separate surfaces.
5. Preserve negative results. An answer with no citations, no recommendation, or an explicit warning is evidence.
6. Re-run the same baseline for trend measurement. Changing the prompts and engines destroys comparability.

If no generated-answer surface with inspectable citations is available, stop the citation baseline and label the run partial. Ordinary search can inform the prompt plan and candidate-source reconnaissance, but every such candidate receives recurrence 0 and low observation confidence until it appears in a sampled AI answer.

## Observation definitions

- **Citation observation:** a visible source page attached to an answer.
- **Brand citation:** the brand's own page is cited; this does not mean the brand is named or endorsed.
- **Third-party mention:** an independent source names the brand, whether or not that page is cited in the current answer.
- **Recommendation:** the answer affirmatively includes the brand in a shortlist or says it fits the requested job.
- **Recommended against:** the answer says not to choose the brand, excludes it for a stated requirement, or attaches a material warning.
- **Source recurrence:** the source appears across distinct prompt-engine-snapshot observations.

Inspect the answer and the cited page before assigning these labels. A citation can support a category definition while the answer recommends entirely different brands.

## Interpreting opportunity types

The action must match the source's governance:

- **Open or claimable:** submit accurate facts through the official route.
- **Customer-governed:** invite genuine eligible customers without controlling sentiment.
- **Editorially governed:** offer verifiable relevance, expertise, data, or a correction; the publisher decides.
- **Community-governed:** contribute as a participant and disclose material connections where required.
- **Partner-governed:** qualify through a real integration, certification, or commercial relationship.
- **Conflict governed:** do not directly insert promotional material; use the surface's disclosed request or discussion process, if any.

An attainable backlink is not automatically an attainable recommendation. Record what the source actually influences.

## Scoring anchors

Apply the 0-3 dimensions consistently:

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Buyer fit | Unrelated | Adjacent audience or job | Relevant | Exact buyer, job, and market |
| Recurrence | Found only outside the sampled answers | One prompt-engine observation | Repeats within an engine or prompt family | Repeats across engines, prompt families, or dates |
| Attainability | Ineligible, closed, or no legitimate route | Unclear or exceptional route | Verified but conditional route | Direct, verified, eligible route |
| Recommendation leverage | Background fact only | Shapes category language or criteria | Can feature, compare, or review the product | Recurrently informs buyer shortlists |
| Audience value | No credible discovery value | Unknown or weak audience | Relevant audience | Verified high-intent audience or referrals |
| Effort | Trivial correction or claim | Low preparation | Material assets, outreach, or customer coordination | Sustained program, integration, or high cost |
| Risk | No material concern | Manageable disclosure or moderation risk | Significant policy or reputation sensitivity | Deceptive, prohibited, or legally unsafe path |

Reject risk-3 opportunities rather than allowing other scores to offset them. Keep every component visible so the total remains auditable.

## Link and review safeguards

- [Google's spam policies](https://developers.google.com/search/docs/essentials/spam-policies) define links created primarily to manipulate search rankings, including automated, paid, and required reciprocal links, as link spam. Sponsored or reciprocal exposure can still have audience value, but it must not be framed as a way to pass ranking credit.
- [FTC review guidance](https://www.ftc.gov/business-guidance/resources/soliciting-paying-online-reviews-guide-marketers) says to check platform rules, use genuine users, avoid sentiment-conditioned incentives, and disclose incentives where applicable.
- [ACCC guidance](https://www.accc.gov.au/consumers/advertising-and-promotions/online-reviews-for-product-and-services) says fake or misleading reviews are unlawful in Australia and that incentives must apply regardless of sentiment and be clearly disclosed.

Verify the user's jurisdiction and the target platform's current policy. Apply the stricter rule when the platform and local law differ.

## Confidence and change over time

Confidence combines two different questions:

1. **Observation stability:** does the source recur across prompts, engines, or dates?
2. **Actionability confidence:** is there a verified, legitimate route suitable for this product?

Do not upgrade confidence merely because a high-authority domain appeared once. Date the audit and recommend a recheck:

- 30 days for active campaigns or volatile launch categories
- 60-90 days for ordinary category monitoring
- Immediately after a major product repositioning, market expansion, or engine change
