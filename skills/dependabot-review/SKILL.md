---
name: dependabot-review
description: Review and merge a batch of open Dependabot dependency-update PRs one by one — reason about every dependency change, read the CI checks and the supply-chain/vulnerability scan reports (Socket) rather than trusting the green tick, triage and fix failing checks, then merge in a conflict-minimizing order while handling Dependabot's rebase/recreate behavior and any review-bot comments. Use when the user wants to work through their Dependabot PRs and says things like 'go through the dependabot PRs', 'review and merge the dependabot (or dependebot) PRs', 'clear the dependency update PRs', 'merge the dependency bumps', 'check the socket / vulnerability reports on the dep PRs', 'handle the weekly dependency updates', or 'are the dependabot PRs safe to merge'. Covers grouped and individual bumps across ecosystems (bun/npm, docker, github-actions, pulumi/infra) and any repo using the `gh` CLI.
metadata:
  author: Jimmy Horan
  version: "1.0"
---

# Dependabot Review & Merge

Work through open Dependabot PRs one at a time: **review → reason → verify → fix → merge**. Merging is the trivial part. The value is in reasoning about each dependency and each scan report *before* you trust it, handling the lockfile conflicts each merge creates, and leaving `main` green — or being precise about why it isn't.

## Core principle

**A green check is necessary, not sufficient — and a red check is not automatically your problem.** Two failure modes to avoid:

1. **Rubber-stamping.** Merging because CI is green without reading what changed or what the supply-chain scanner actually said. Grouped PRs bury a major transitive bump or a flagged package under 40 patch bumps. The vulnerability scanner's *check* can pass while its *comment* carries "Warn"-level alerts you never read.
2. **Misattribution.** Seeing red and assuming your merge caused it — or assuming a failure's cause without reading the failing job's log. Always determine whether a failure is **introduced** (new with this change) or **pre-existing** (already red on `main`) by checking the failure's history. Never assert a root cause you haven't read.

Everything below serves those two: reason about each change, verify every claim.

## 1 — Enumerate the batch

Find every open Dependabot PR. The author login is `app/dependabot`.

```bash
gh pr list --state open --limit 100 --json number,title,author,headRefName,createdAt \
  --jq '.[] | select(.author.login | test("dependabot")) | {number,title,headRefName}'
```

List them for the user, then process each. Note which touch a **shared lockfile** (they'll conflict with each other) versus which are **independent** (docker image tags, github-actions pins, a sub-project with its own lockfile like `infra/pulumi`). That split drives merge order (§7).

## 2 — Gather state per PR

For each PR pull, in parallel: CI checks, issue comments, review comments, changed files, the body, and the *direct-dependency* diff.

```bash
gh pr checks <n>                         # per-check pass/fail/pending/skipping
gh pr view <n> --json comments --jq '.comments[] | "[\(.author.login)] \(.body)"'
gh pr view <n> --json reviews  --jq '.reviews[]  | "[\(.author.login)] \(.state) \(.body)"'
gh pr view <n> --json files    --jq '.files[] | "\(.additions)+ \(.deletions)- \(.path)"'
gh pr view <n> --json body     --jq '.body'   # Dependabot's release-notes/compat summary
```

The signal is in the **package.json / manifest** lines, not the lockfile. Extract just the direct-dependency changes:

```bash
gh pr diff <n> --patch | awk '/^diff --git/{p=($0~/package\.json/)} p&&/^[+-]/&&!/^[+-][+-]/&&/"/{print}'
```

## 3 — Reason about the changes

For each bump, form a real opinion — don't just note the version delta:

- **Direct vs transitive.** A scary-looking major bump in the lockfile (e.g. OpenTelemetry 1.x→2.x) may be purely transitive. Grep the source for direct imports (`grep -rn "@scope/pkg" apps packages --include=*.ts`). Zero direct imports + a stable peer range + green typecheck = invisible to your code.
- **Semver reality.** Patch/minor within an existing major is low-risk. A major bump, or any `0.x` minor, can break — read the release notes in the PR body.
- **Known couplings** (project-specific — learn them). Some packages must move together or the build breaks: validation stacks (zod ↔ its hono/env adapters), SDK-pinned ecosystems (React pinned by the Expo SDK — bump the SDK first), tooling pinned to a runtime (a vendored ts-node needing an older TypeScript). If the PR bumps one side of a coupling without the other, that's a red flag even if checks pass. Confirm the coupled package is unchanged or co-bumped.
- **Is "checks pass" enough evidence?** For type/behavior breaks, typecheck + tests + build are strong evidence. For runtime-only behavior with no coverage, they aren't — say so.

## 4 — Read the supply-chain / vulnerability reports (don't skip this)

The scanner (Socket, login `socket-security`) posts **two things**, and they mean different things:

- **The checks** (`Socket Security: Project Report`, `Socket Security: Pull Request Alerts`) — passing means *nothing blocking*.
- **The comment** — a scorecard table **plus**, when anything is flagged, a `> [!WARNING]` block listing per-package alerts. **These "Warn" alerts are non-blocking, so the check still passes while real annotations sit in the comment.** Read the comment, not just the tick.

```bash
gh pr view <n> --json comments \
  --jq '.comments[] | select(.author.login=="socket-security") | .body' \
  | sed -E 's/<[^>]+>//g' \
  | grep -iE 'WARNING|Obfuscated|malware|install script|native code|typosquat|new author|protestware|CVE|GHSA|critical|Vulnerability'
```

Reason about each alert instead of reflexively accepting or blocking:

- **Vulnerability score.** `Vulnerability => 100` means no known CVEs. That's the number the user actually cares about. Low **Supply-Chain-Security** scores (60s–70s) on large packages (pulumi, expo, otel) are scorecards, not alerts.
- **"Obfuscated code" is usually a false positive.** Official/popular SDKs that ship **minified/bundled dist** (e.g. `@elevenlabs/elevenlabs-js`, `jiti`) trip the heuristic. Confirm it's a false positive by checking: is the package **already in the tree** (`grep '"pkg@' <lockfile>`)? Is it an approved/official publisher? Is only the version changing (so the trait predates this bump)? If yes to those → accept and note it.
- **Real blockers** — actual malware, protestware, a package that newly added an install script or network/shell access, a brand-new author on a package, a typosquat — do **not** merge. Escalate to the user.
- **No scanner comment** on a docker/github-actions PR is expected (it scans package deps, not image tags).

State your verdict per flagged package: *real vuln / real supply-chain risk / false positive because X*. This is the part the user asked for explicitly — show the reasoning.

## 5 — Check for review-bot comments

Beyond the scanner, look for code-review bots (Cursor "bugbot", CodeRabbit, etc.) in both the checks list and the comments. They may not be installed — **verify and say so** ("no bugbot configured on this repo") rather than silently skipping. If one left a comment, read it and address anything legitimate before merging.

## 6 — Triage and fix failing checks

For any failing check, read the **actual log** before acting:

```bash
gh run view --job=<jobId> --log-failed        # jobId from the check's URL
```

Separate **real regressions** from **tooling artifacts**. A classic artifact: a **linter/formatter version bump reformats untouched files** or invalidates a config `$schema`. Example — a `biome` bump fails `lint` with format diffs on files nobody touched plus a schema-version mismatch. That's not a real failure; it's the new tool version's output. The fix belongs on the PR branch (§8): reformat the affected files with the new version and bump the config's `$schema` to match. Confirm against the baseline (`run lint on main` — if it's clean there, the bump introduced it).

If it's a genuine regression the bump caused, that's decision-worthy: fix forward, or `@dependabot ignore` the offending version and tell the user.

## 7 — Merge order (minimize lockfile churn)

All PRs sharing one lockfile conflict with each other: merging one forces a rebase on every trailing one. You can't avoid the rebases, only sequence them well:

1. **Independent PRs first** — docker image tags, github-actions, sub-projects with their own lockfile. No shared-lockfile conflict; merge them freely, green.
2. **Shared-lockfile group PRs last.** Among these, merge the ones needing **no manual fix** earlier (let Dependabot rebase them), and the one you had to **hand-fix** dead last — so nothing re-clobbers your fix.

Merge with squash (matches most Dependabot histories):

```bash
gh pr merge <n> --squash --delete-branch
```

After each merge, re-check the trailing PRs' mergeability — they flip to `CONFLICTING`/`DIRTY`:

```bash
gh pr view <n> --json mergeable,mergeStateStatus
```

## 8 — Handle conflicts, rebases, and Dependabot's quirks

When a trailing PR conflicts (almost always **only in the lockfile**), you have three moves:

- **Let Dependabot rebase.** `gh pr comment <n> --body "@dependabot rebase"`. But know its quirks: it may instead **close the PR and open a brand-new one with a new number** (comment: *"these dependencies are updatable in another way, so this is no longer needed"*) — that new PR is the rebased equivalent; diff it against the old to confirm, then merge it. It can also be slow or silently decline. **Don't wait 15+ minutes** for an in-place rebase that may never come.
- **Resolve locally** (reliable, no force-push). Fetch the PR head, merge `main`, regenerate the lockfile, push:
  ```bash
  gh pr checkout <n>                 # or: git fetch origin refs/pull/<n>/head && git checkout -B fix FETCH_HEAD
  git merge origin/main --no-edit    # conflicts, typically just the lockfile
  git checkout origin/main -- bun.lock && <pkg-manager> install   # regenerate against merged manifests
  git add bun.lock && git commit --no-edit
  ```
  Verify the regenerated lockfile kept **both** sides (spot-check a dep from each PR), run `typecheck` locally, then push (non-force).
- **Fixing a PR + resolving in one go** (the linter-bump case). Prefer building on **Dependabot's latest rebased head** so its clean lockfile wins: `git checkout -B fix <dependabot-head>` then `git cherry-pick <your-fix-commit>`. Push non-force.

**Pushing to a Dependabot branch:** it's a normal (non-force) push if your local history has the remote head as an ancestor — a merge commit or a cherry-pick on top qualifies. A local **rebase** would need `--force` (avoid unless the user OKs it). Once you push a non-Dependabot commit, Dependabot stops managing that PR — fine, since you're about to merge it. **Watch for Dependabot racing you**: if your push is rejected as non-fast-forward, Dependabot re-pushed; re-fetch its new head and re-apply your fix on top.

**Pre-push gates:** repos may run a pre-push hook (typecheck/tests + an *interactive* review prompt). Interactive prompts can't be answered non-interactively — use the documented bypass for **only** the interactive step (e.g. `SKIP_REVIEW=1 git push`) so the real gates still run. Don't blanket-disable all hooks.

## 9 — Verify the end state honestly

After the last merge:

- Confirm **0 open Dependabot PRs** remain and `main`'s tip carries every expected bump (spot-check versions in the manifests).
- **Distinguish workflows.** "Is CI green?" often has two answers: the **`ci` gate** (lint/test/typecheck/build) may be fully green while a **separate `deploy` workflow** is red. Enumerate every workflow on `main`'s HEAD SHA and drill into jobs — don't report a single rolled-up status:
  ```bash
  gh run list --commit <sha> --json workflowName,conclusion
  gh run view <runId> --json jobs --jq '.jobs[] | "\(.conclusion // .status)\t\(.name)"'
  ```
- **Prove pre-existing vs introduced.** If a job is red, check its history on prior `main` commits (`gh run list --branch main --workflow deploy.yml`). If the **same job failed with the same signature before your batch**, it's pre-existing — say so, and cite the earlier commit. If it started with your merge, it's yours to fix.
- **Correct yourself.** If you asserted a cause and then read the log and found otherwise, say so plainly. "The deploy failure is the `deployerSa` step" → after reading, "the actual failing job is `e2e`; the deploy step is skipped behind it" is the honest update.

## Guardrails

- **Merging to `main` is significant and semi-irreversible.** Proceed on the user's explicit "merge them" (this workflow is that authorization), but don't invent scope — merge the dependency PRs, not unrelated open work.
- **Never `git push --force`** to a shared/Dependabot branch without explicit confirmation. Every technique above is non-force.
- **Merging often auto-deploys.** If merge-to-`main` triggers infra/image deploys, flag it — and note when a resulting deploy failure is a pre-existing/known-broken condition rather than something the bumps caused. Check that none of the PRs carry DB migrations before merging a batch unattended.
- **Record durable, non-obvious gotchas** you hit (a tool's schema-coupling, Dependabot's recreate behavior, a scanner false-positive pattern) to memory so the next sweep is faster.

## Output

While working, keep the user oriented with a compact per-PR table: **PR # · what · risk · CI · scanner verdict**. At the end, deliver: what merged (and in what order), the one or two issues you found and how you fixed them, the per-PR supply-chain reasoning (especially any flagged package and why it was safe or not), how conflicts were handled, and the honest final `main` state (which workflows/jobs are green, which are red and whether that's pre-existing). Lead with the correction if you revised an earlier claim.
