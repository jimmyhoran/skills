# Contributing

This repository is Jimmy Horan's personally curated collection of agent skills. Focused fixes are welcome; submitting a change does not create an expectation that it will be accepted or supported indefinitely.

## Good contributions

Useful, bounded changes include:

- correcting a factual error or stale official reference;
- fixing a broken relative link or missing asset;
- making a workflow clearer, safer, or more honest about uncertainty;
- tightening an external-write boundary or prerequisite;
- adding a regression fixture for a demonstrated failure; and
- improving public documentation without inflating compatibility or usage claims.

For a new skill or a broad change in a skill's purpose, open an issue first and describe the user problem, intended output, required tools, and side effects. Please wait for maintainer direction before investing in a full implementation. This keeps the collection coherent and avoids turning it into a general-purpose registry.

Discuss changes to `.github/workflows/**` or the validation trust boundary before opening a pull request. Actions runs from external contributors stay paused until the maintainer has reviewed those security-sensitive diffs and explicitly approved the run.

There is no support or response-time SLA. Bug reports and improvement ideas are appreciated, but maintenance happens as availability and priorities allow.

## Before opening an issue or pull request

Security vulnerabilities do not belong in public issues or pull requests. Follow [SECURITY.md](./SECURITY.md) to report them privately.

For ordinary bugs, include the skill name, the prompt or scenario, what happened, what you expected, the agent and relevant tool versions, and any safe-to-share evidence. Remove tokens, private repository details, customer data, and other sensitive information.

## Local workflow

Validation requires Bash, `curl`, `tar`, Python 3.10 or newer, [ShellCheck](https://www.shellcheck.net/), network access, and a [GitHub CLI](https://cli.github.com/) build that provides `gh skill publish`. The entry point downloads checksummed copies of its pinned skill validator and actionlint releases when those exact versions are not already installed.

Clone the repository, make the smallest change that resolves the problem, and run the same deterministic validation used by CI:

```bash
git clone https://github.com/jimmyhoran/skills.git
cd skills
./scripts/validate.sh
```

The validator checks repository and skill structure; it cannot prove that an agent will reason correctly in every environment. If your change fixes a behavioral failure, include a reproducible example or deterministic fixture when practical.

Maintainers who want to exercise the checked-out skills in Claude Code or Codex can preview the link plan, then apply it:

```bash
./scripts/link-skills.sh
./scripts/link-skills.sh --apply
```

That linker is not the consumer installer. It targets both agents by default, supports selecting either one, and refuses collisions rather than moving or retargeting existing content. Review the dry-run output before applying it.

## Pull request checklist

- Keep the change focused and explain the concrete problem it solves.
- Run `./scripts/validate.sh` and report the result.
- Update the README catalog if a skill's promise, prerequisites, output, dependencies, write boundary, support status, slug, or path changed.
- Keep `name` aligned with the skill directory and use repository-standard author and license metadata.
- Add or retain attribution for material sources and methods.
- Do not include credentials, private data, generated audit artifacts, or internal planning notes.
- Call out any command or instruction that can write to an external system.

By contributing, you agree that your contribution is licensed under the repository's [MIT License](./LICENSE).
