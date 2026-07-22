# Jimmy Horan's agent skills

Practical agent playbooks by [Jimmy Horan](https://x.com/jimmynhoran) (`@jimmynhoran`) for founder work in the space between product decisions, engineering operations, and distribution.

These skills turn recurring work into explicit workflows: what evidence to gather, how to reason about it, what to return, and where the agent must stop before making an external change. They are deliberately opinionated and personally curated rather than a general-purpose skill registry.

## Before you install

An agent skill is an instruction package, not a sandbox. Read the linked `SKILL.md` before using a skill, especially when it can merge code, change a website, submit a URL, or use an authenticated account. Your agent's permissions and confirmation rules still apply.

The skills use the standard `skills/<name>/SKILL.md` layout and are installable by compatible skill managers. Repository validation checks structure and packaging; it does not certify an agent's judgment or guarantee identical behavior across clients. Each catalog entry below calls out its prerequisites and external-write boundary.

## Install with skills.sh

The primary install path is the open [skills.sh CLI](https://skills.sh/docs/cli) ([source](https://github.com/vercel-labs/skills)). It requires Node.js and can run through `npx` without a global CLI install.

Start with one skill:

```bash
npx skills add jimmyhoran/skills --skill two-way-door
```

The interactive flow lets you choose the agent or agents that should receive it. To make the destination explicit, install into the current project:

```bash
npx skills add jimmyhoran/skills \
  --skill two-way-door \
  --agent claude-code \
  --agent codex
```

Project scope is the default. Use `--global` (`-g`) only when you want the skill available across all projects for the selected agent:

```bash
npx skills add jimmyhoran/skills \
  --skill two-way-door \
  --agent claude-code \
  --global
```

You can repeat `--skill` to install a small set, or use `--skill '*'` to install the whole collection. Selective installation is recommended: install the workflows you expect the agent to use.

### Verify, update, and remove

List project and global installs separately:

```bash
npx skills list
npx skills list --global
```

Update this example skill in project or global scope:

```bash
npx skills update --project two-way-door
npx skills update --global two-way-door
```

Remove it from the current project or from global scope:

```bash
npx skills remove two-way-door
npx skills remove --global two-way-door
```

The `skills` CLI collects anonymous install telemetry by default. Set `DISABLE_TELEMETRY=1` if you prefer to opt out; see the CLI's documentation for the current behavior.

## GitHub CLI preview

GitHub CLI also has preview support for agent skills. It is a useful secondary path, particularly for inspecting a skill before installation, but its interface is explicitly subject to change.

```bash
# Read the skill without installing it.
gh skill preview jimmyhoran/skills two-way-door

# Install at project scope for one agent.
gh skill install jimmyhoran/skills two-way-door \
  --agent codex \
  --scope project

# Or install at user scope.
gh skill install jimmyhoran/skills two-way-door \
  --agent claude-code \
  --scope user

# Inspect and update installs managed by GitHub CLI.
gh skill list
gh skill update --dry-run
gh skill update two-way-door
```

See the current [`gh skill` manual](https://cli.github.com/manual/gh_skill) before scripting this preview interface.

## Choose a skill by the job

### Make product decisions

#### [two-way-door](./skills/two-way-door/SKILL.md)

**Promise:** Match the amount of deliberation to the real cost of reversing a decision, using a calibrated 1-5 reversibility score.

- **Try:** `Use two-way-door on whether we should announce this pricing change next week.`
- **Expected output:** A compact decision statement, reversibility rating, dominant reason, and recommended deliberation depth. Multiple decisions are scored separately.
- **Needs:** The decision, its constraints, and any known blast radius. No special tools, accounts, or companion skills.
- **External writes:** None. It is an advisory workflow and does not make the decision or act on it.
- **Support:** Installable; repository checks validate its package, but there is no automated behavioral certification across agents.

#### [feeling-first-design](./skills/feeling-first-design/SKILL.md)

**Promise:** Turn a consumer-product moment into an ethical, testable design treatment built around the feelings that should drive adoption.

- **Try:** `Use feeling-first-design to make our first-run budgeting flow feel safer and more motivating.`
- **Expected output:** The moment and journey stage, three target feelings, selected behavioral levers, a concrete product move, an experiment and metric, and a dark-pattern check.
- **Needs:** A product or flow, its audience, and the behavior or outcome being considered. Existing research or metrics help but are not required; no account or companion skill is required.
- **External writes:** None by default. It recommends experiments; it does not change the product or launch a test.
- **Support:** Installable; repository checks validate its package, but there is no automated behavioral certification across agents.

### Run engineering operations

#### [dependabot-review](./skills/dependabot-review/SKILL.md)

**Promise:** Work through a batch of Dependabot PRs with dependency reasoning, CI and supply-chain evidence, conflict-aware ordering, and an honest final state.

- **Try:** `Review and merge the open Dependabot PRs. Read the Socket reports, fix legitimate failures, and keep main green.`
- **Expected output:** A per-PR table covering change, risk, CI, and scanner verdict, followed by merge order, fixes, conflict handling, and the final status of each relevant workflow.
- **Needs:** A local Git checkout; an authenticated [`gh`](https://cli.github.com/) session with access to the repository, pull requests, and Actions logs; and the repository's package manager and test toolchain. Socket or review-bot evidence is used only when that integration exists. No companion skill is required.
- **External writes:** This is an execution workflow. When the user explicitly asks it to merge, it may comment on PRs, push non-force fixes, merge and delete branches, and thereby trigger deployments. Review-only requests do not authorize those writes.
- **Support:** Installable; repository checks validate its package, but its authenticated, repository-specific behavior is not covered by an automated end-to-end test.

### Understand and grow distribution

#### [funnel-teardown](./skills/funnel-teardown/SKILL.md)

**Promise:** Connect the visible parts of an offer into four useful answers: why people buy, where they drop off, what is missing, and where revenue is being left behind.

- **Try:** `Tear down the funnel at https://example.com from the point of view of a skeptical first-time buyer.`
- **Expected output:** Evidence coverage, sharp component findings, the four-part synthesis, and either steal/exploit/avoid moves for a competitor or impact-versus-effort fixes for your own funnel.
- **Needs:** Public URLs and browser or web access. The user must supply gated assets such as emails, checkout screens, or in-app paywalls; otherwise the gaps stay explicitly unverified. No account or companion skill is required for the base teardown.
- **External writes:** None by default. It investigates and reports; it does not sign up, purchase, publish, or change the funnel.
- **Support:** Installable; repository checks validate its package, but live-site coverage and behavior vary with the evidence and tools available.

#### [map-citation-opportunities](./skills/map-citation-opportunities/SKILL.md)

**Promise:** Turn observed AI-search citations and recommendations into a verified, ranked backlog of legitimate visibility opportunities rather than a directory-submission dump.

- **Try:** `Map citation opportunities for our product across buyer-intent prompts in ChatGPT and Perplexity.`
- **Expected output:** Audit scope, a citation/mention/recommendation baseline when observable, recurring source patterns, a scored backlog, a now/next/later queue, content gaps, and a measurement plan.
- **Needs:** Product, buyer, market, and competitor context; browser or web access; and at least one AI answer surface with inspectable citations for a full audit. Without that surface it returns a clearly labeled partial reconnaissance. Optional execution companions include `search-discovery` from this repo and separate directory, AI SEO, outreach, or PR skills when available.
- **External writes:** Read-only mapping and verification by default. It does not create profiles, submit forms, request reviews, publish content, send pitches, or change production without separate authorization.
- **Support:** Installable; repository checks validate its package, but there is no automated behavioral test and full results depend on live citation-surface access.

#### [search-discovery](./skills/search-discovery/SKILL.md)

**Promise:** Diagnose indexability first, keep sitemaps truthful, and follow each search engine's current discovery or submission guidance without presenting a request as guaranteed indexing.

- **Try:** `Use search-discovery for the pages in this launch and tell me what is ready to submit.`
- **Expected output:** For each URL: change type, sitemap state, request or notification state, evidence, and the next check, with incomplete account prerequisites separated from completed actions.
- **Needs:** Production URLs and live web access. Authenticated Google Search Console or Bing Webmaster Tools access and verified site ownership are needed for their protected submission flows; sitemap or IndexNow changes also require access to the site's code or publishing system. No companion skill is required.
- **External writes:** Diagnosis is read-only. Updating sitemaps or `robots.txt`, configuring IndexNow, and submitting authenticated discovery requests happen only when the user authorizes them.
- **Support:** Installable; repository checks validate its package, but live submission flows are not automated and must be rechecked against current official guidance.

## Maintainer setup

Contributors and maintainers working from a clone can preview local development links with `./scripts/link-skills.sh`, then apply the reviewed plan with `./scripts/link-skills.sh --apply`. This is a maintainer convenience, not the public installation path. It targets Claude Code and Codex by default, supports selecting either agent, and refuses destination collisions instead of moving or retargeting existing content.

See [CONTRIBUTING.md](./CONTRIBUTING.md) before proposing a change and [SECURITY.md](./SECURITY.md) for confidential vulnerability reporting. The collection is available under the [MIT License](./LICENSE).
