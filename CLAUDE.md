# Repository guidance

This is Jimmy Horan's (`@jimmynhoran`) public, personally curated collection of practical agent playbooks for founder work in the space between product decisions, engineering operations, and distribution.

## Structure and catalog

- Skills live directly under `skills/`, one folder per skill, with `SKILL.md` as the entry point.
- Keep a skill's `name` aligned with its directory slug and retain the required frontmatter.
- Use Jimmy Horan as the author and MIT as the license for repository-owned skills. Repository release tags, not per-skill fields, are the version authority.
- Every published skill must have a stable link in `README.md` and be grouped by the job it helps with.
- Every README catalog entry must state the promise, an example invocation, expected output, prerequisites and tool or account needs, companion-skill dependencies when relevant, its external-write boundary, and a conservative installable-versus-tested support claim.
- Treat published slugs and paths as compatibility surfaces. Do not rename or remove one without a documented migration or deprecation path.

## Public writing bar

- Write for a first-time public reader. Do not assume access to Jimmy's private repositories, accounts, terminology, or prior conversations.
- Do not add secrets, private customer or company details, personal data, private URLs, or examples copied from confidential work.
- Keep claims testable and narrow. Do not describe a skill as behaviorally tested, cross-agent compatible, or production-safe unless current evidence proves that exact claim.
- Make side effects explicit. A skill that can push, merge, submit, publish, send, purchase, or modify an external system must state what user authorization is required.
- Preserve material provenance and source attribution. Prefer official, current sources for volatile product or platform instructions.
- Keep the collection curated. Focused fixes are welcome; new skill proposals should be discussed before implementation.

## Validation and local linking

Run the same deterministic validation used by CI before proposing a change:

```bash
./scripts/validate.sh
```

Treat `.github/workflows/**` and the validation scripts as a security boundary. GitHub Actions runs from every external contributor remain paused for maintainer approval; review the workflow and validator diff itself before approving a run, because pull-request workflow definitions are proposal-controlled.

`./scripts/link-skills.sh` is a maintainer-only convenience for previewing local links for Claude Code and Codex; `--apply` is required to write them. Do not present it as the normal user installer. It refuses every destination collision and never moves or retargets existing content.

Follow [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution policy and [SECURITY.md](./SECURITY.md) for confidential vulnerability reports.
