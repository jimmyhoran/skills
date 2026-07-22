# Security policy

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/jimmyhoran/skills/security/advisories/new) for suspected security issues. Do not disclose the issue in a public GitHub issue, pull request, discussion, or social post before it has been assessed and, where appropriate, fixed.

A useful report includes:

- the affected skill, script, workflow, or file;
- the security impact and the conditions required to trigger it;
- minimal reproduction steps or a proof of concept that does not expose real secrets;
- the agent, operating system, and relevant tool versions; and
- any mitigation or proposed fix you have identified.

Never include live credentials, customer data, or private repository content in the report. If GitHub's private reporting form is unavailable, do not fall back to a public issue with vulnerability details.

## What belongs here

Examples of security-relevant reports include:

- instructions that can cause unexpected destructive actions or external writes outside the user's stated authorization;
- command, prompt, path, or workflow injection that can execute untrusted content;
- secret exposure through repository content, logs, examples, Actions, or generated artifacts;
- unsafe handling of authenticated accounts, tokens, pull requests, or third-party content; and
- a vulnerability in a repository-maintained script or CI workflow.

Ordinary factual corrections, broken links, output-quality disagreements, and feature requests can use public issues as long as they contain no sensitive information.

## Scope and expectations

Security fixes target the default branch and, when a release exists, the latest release. Older tags may not receive backports.

This is a personal open-source project with no security bounty, guaranteed response time, or support SLA. Reports will be assessed as maintainer availability allows. Please allow time for investigation before public disclosure.

Agent skills are instructions, not a security boundary. Review a skill before use, grant agents the minimum tools and account permissions needed, and confirm external writes before execution. The repository is provided under the terms of the [MIT License](./LICENSE), including its warranty disclaimer.
