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

**Promise:** Turn evidence about a consumer-product moment into an ethical, testable intervention for one useful emotional state shift.

- **Try:** `Use feeling-first-design to make our first-run budgeting flow feel safer and more motivating.`
- **Expected output:** The moment and evidence, one state-shift hypothesis with confidence, the smallest fitting intervention, a behavioral and user-reported test, guardrails, a stop condition, and an agency review.
- **Needs:** A product or flow, its audience, and the behavior or outcome being considered. Existing research or metrics help but are not required; no account or companion skill is required.
- **External writes:** None by default. It recommends experiments; it does not change the product or launch a test.
- **Support:** Installable; repository checks validate its package, but there is no automated behavioral certification across agents.

#### [backlog-triage](./skills/backlog-triage/SKILL.md)

**Promise:** Read your whole backlog in whatever tracker you use, then get the 10 issues to act on now and the 10 to close, merge, revise, split, or delete, with evidence for each. Built to run daily or weekly.

- **Try:** `Use backlog-triage on our Linear backlog for this week. We're focused on onboarding.`
- **Expected output:** Coverage and backlog-health lines, a ranked act-now table (why now, next action, effort, owner), a prune table (action, evidence, confidence), and a numbered list of proposed tracker changes. A list comes back shorter only when fewer issues qualify, and the report says why.
- **Needs:** Read access to the tracker through a connected MCP server (preferred), its CLI, or its API: for example [fp](https://fp.dev/), an authenticated [`gh`](https://cli.github.com/) session for GitHub Issues, or the official Linear or Trello MCP server. Other trackers work through their own MCP server, CLI, API, or an export you provide. `jq` helps with large backlogs. A structured question tool such as Claude Code's AskUserQuestion is preferred for approval; otherwise it asks in plain text. No companion skill is required.
- **External writes:** None until you approve. It then applies only the changes you chose: priority, order, labels, status, comments, closing or merging duplicates, and revising or splitting issues. Deletion needs a separate confirmation naming each item. A request that already says to apply the changes covers everything except deletion, and unattended runs only report.
- **Support:** Installable; repository checks validate its package. Its fp and GitHub CLI commands were checked against fp 0.24 and gh 2.95 in November 2026, and its Linear, Trello, and Jira access notes against their official documentation; no automated end-to-end test covers a real backlog.

### Run engineering operations

#### [dependabot-review](./skills/dependabot-review/SKILL.md)

**Promise:** Work through a batch of Dependabot PRs with dependency reasoning, CI and supply-chain evidence, conflict-aware ordering, and an honest final state.

- **Try:** `Review and merge the open Dependabot PRs. Read the Socket reports, fix legitimate failures, and keep main green.`
- **Expected output:** A per-PR table covering change, risk, CI, and scanner verdict, followed by merge order, fixes, conflict handling, and the final status of each relevant workflow.
- **Needs:** A local Git checkout; an authenticated [`gh`](https://cli.github.com/) session with access to the repository, pull requests, and Actions logs; and the repository's package manager and test toolchain. Socket or review-bot evidence is used only when that integration exists. No companion skill is required.
- **External writes:** This is an execution workflow. When the user explicitly asks it to merge, it may comment on PRs, push non-force fixes, merge and delete branches, and thereby trigger deployments. Review-only requests do not authorize those writes.
- **Support:** Installable; repository checks validate its package, but its authenticated, repository-specific behavior is not covered by an automated end-to-end test.

#### [worktree-cleanup](./skills/worktree-cleanup/SKILL.md)

**Promise:** Close out a finished worktree: confirm its work is merged and nothing is left undone, update the issues tied to it, stop what it is still running, and remove it. It asks before doing anything that could lose work.

- **Try:** `Use worktree-cleanup. The PR merged, so close everything out and tear down this worktree.`
- **Expected output:** An audit of merge state, unfinished work, and tracker state; one question per unresolved item with a recommended option; then the tracker updates and shell cleanup it performed, and a final report written before the worktree is removed.
- **Needs:** A local Git worktree and `git`, plus an authenticated [`gh`](https://cli.github.com/) session for pull-request and issue state. Orca-managed worktrees use the [Orca](https://onorca.dev/) CLI; other worktrees fall back to `git worktree`. [fp](https://fp.dev/), Linear (through Orca or a Linear MCP server), and GitHub Issues are checked only when the project already uses them. A structured question tool such as Claude Code's AskUserQuestion is preferred; otherwise it asks in plain text. No companion skill is required.
- **External writes:** Invoking it authorizes three things: updating or closing tracker items whose work it verified as merged, stopping shells and dev servers the worktree owns, and removing the worktree once nothing is unresolved (running the repository's Orca archive hook when Orca manages it). It commits, pushes, merges, closes a PR, discards changes, deletes an unmerged branch, creates follow-up issues, or stops another agent only when the user picks that option.
- **Support:** Installable; repository checks validate its package. Its command syntax was checked against the Orca 1.4 and fp 0.24 CLI references in November 2026, but no automated end-to-end test covers a real teardown.

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
