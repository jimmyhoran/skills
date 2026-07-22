# Skills

My personal collection of agent skills (slash commands and behaviors) loaded by Claude Code. Layout adapted from [mattpocock/skills](https://github.com/mattpocock/skills).

## Install

Symlink everything in this repo into `~/.claude/skills`:

```bash
./scripts/link-skills.sh
```

The script symlinks each `skills/<name>/` folder into `~/.claude/skills`, where Claude Code discovers them. If a same-named entry already exists there, a real directory is moved aside to `<name>.bak` and an existing symlink is retargeted, each with a warning.

## Skills

- **[dependabot-review](./skills/dependabot-review/SKILL.md)** — Review and merge a batch of open Dependabot PRs one by one: reason about each dependency, read the CI checks and Socket supply-chain/vulnerability reports (not just the green tick), fix failing checks, and merge in a conflict-minimizing order while handling Dependabot's rebase/recreate quirks.
- **[feeling-first-design](./skills/feeling-first-design/SKILL.md)** — Design or critique a consumer-app feature so users adopt it because of how it makes them *feel*: run an emotional-design lens, pull the right behavioral-psychology lever for that moment in the journey, turn it into a testable experiment with a metric, and screen for the dark-pattern trap.
- **[funnel-teardown](./skills/funnel-teardown/SKILL.md)** — Tear down a complete offer (funnel, landing page, lead magnet, upsell, pricing, emails, CTAs) and connect the dots: why people buy, where they drop off, what's missing, and where money is left on the table.
- **[search-discovery](./skills/search-discovery/SKILL.md)** — Prepare new, changed, moved, or deleted URLs for search discovery: verify indexability, keep sitemaps accurate, submit through the appropriate current engine route, and report requests without overstating indexing guarantees.
- **[two-way-door](./skills/two-way-door/SKILL.md)** — Score a decision 1–5 on Bezos's two-way-door reversibility scale so deliberation depth matches the actual cost of reversing.
