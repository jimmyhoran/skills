#!/usr/bin/env python3
"""Deterministic repository checks that treat skill and workflow files as data."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
MARKDOWN_INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_REFERENCE_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
FULL_SHA_ACTION_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")
REQUIRED_CHECK_NAME = "Public skills validation (required)"
BOOTSTRAP_BASE_SHA = "3c58d4c808b44e4eed04ed84d5ef5cc771c90dd9"
ALLOWED_WORKFLOW_DIGESTS = {
    "external-links.yml": "9c2e0e664ad3b87f0968b70e7fa026e11fe1b8a725d881c03482209ffe2b750a",
    "validate.yml": "47e431847f3dc03aa5c40be9bdd0294dc0b00cc5e718163aac04c58d381dd4f0",
}


class ValidationError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate catalog, relative references, manifests, and workflow security."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    return parser.parse_args()


def add_error(errors: list[str], path: Path | str, message: str) -> None:
    errors.append(f"{path}: {message}")


def parse_scalar(raw: str, line_number: int) -> Any:
    if raw == "true":
        return True
    if raw == "false":
        return False
    if not raw.startswith('"'):
        raise ValidationError(
            f"line {line_number}: strings must be double quoted and booleans must be true/false"
        )
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"line {line_number}: invalid quoted string: {exc.msg}") from exc
    if not isinstance(value, str):
        raise ValidationError(f"line {line_number}: only string and boolean scalars are allowed")
    return value


def split_mapping_entry(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise ValidationError(f"line {line_number}: expected a key/value mapping")
    key, raw_value = text.split(":", 1)
    if re.fullmatch(r"[a-z][a-z0-9_]*", key) is None:
        raise ValidationError(f"line {line_number}: invalid or quoted key {key!r}")
    return key, raw_value.strip()


def parse_yaml_subset(path: Path) -> dict[str, Any]:
    """Parse the small, deliberately allowlisted subset used by openai.yaml."""

    try:
        raw_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"unable to read UTF-8 YAML: {exc}") from exc

    tokens: list[tuple[int, str, int]] = []
    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        if "\t" in raw_line:
            raise ValidationError(f"line {line_number}: tabs are not allowed")
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2 != 0:
            raise ValidationError(f"line {line_number}: indentation must use two-space steps")
        text = raw_line[indent:]
        tokens.append((indent, text, line_number))

    if not tokens:
        raise ValidationError("manifest is empty")

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(tokens) or tokens[index][0] != indent:
            raise ValidationError("invalid indentation")
        if tokens[index][1].startswith("- "):
            result_list: list[Any] = []
            while index < len(tokens) and tokens[index][0] == indent:
                current_indent, text, line_number = tokens[index]
                del current_indent
                if not text.startswith("- "):
                    break
                item_text = text[2:].strip()
                if not item_text:
                    if index + 1 >= len(tokens) or tokens[index + 1][0] <= indent:
                        raise ValidationError(f"line {line_number}: empty list item")
                    item, index = parse_block(index + 1, tokens[index + 1][0])
                    result_list.append(item)
                    continue

                key, raw_value = split_mapping_entry(item_text, line_number)
                item_map: dict[str, Any] = {}
                if not raw_value:
                    if index + 1 >= len(tokens) or tokens[index + 1][0] <= indent:
                        raise ValidationError(f"line {line_number}: missing nested value")
                    value, index = parse_block(index + 1, tokens[index + 1][0])
                    item_map[key] = value
                else:
                    item_map[key] = parse_scalar(raw_value, line_number)
                    index += 1

                if index < len(tokens) and tokens[index][0] > indent:
                    continuation_indent = tokens[index][0]
                    continuation, index = parse_block(index, continuation_indent)
                    if not isinstance(continuation, dict):
                        raise ValidationError(
                            f"line {tokens[index - 1][2]}: list item continuation must be a mapping"
                        )
                    duplicate = set(item_map) & set(continuation)
                    if duplicate:
                        raise ValidationError(
                            f"line {line_number}: duplicate key {sorted(duplicate)[0]!r}"
                        )
                    item_map.update(continuation)
                result_list.append(item_map)
            return result_list, index

        result_map: dict[str, Any] = {}
        while index < len(tokens) and tokens[index][0] == indent:
            _, text, line_number = tokens[index]
            if text.startswith("- "):
                break
            key, raw_value = split_mapping_entry(text, line_number)
            if key in result_map:
                raise ValidationError(f"line {line_number}: duplicate key {key!r}")
            if raw_value:
                result_map[key] = parse_scalar(raw_value, line_number)
                index += 1
            else:
                if index + 1 >= len(tokens) or tokens[index + 1][0] <= indent:
                    raise ValidationError(f"line {line_number}: missing nested value for {key!r}")
                result_map[key], index = parse_block(index + 1, tokens[index + 1][0])
        return result_map, index

    parsed, final_index = parse_block(0, tokens[0][0])
    if tokens[0][0] != 0 or final_index != len(tokens) or not isinstance(parsed, dict):
        raise ValidationError("manifest must contain one top-level mapping")
    return parsed


def unknown_keys(
    value: dict[str, Any], allowed: set[str], label: str, path: Path, errors: list[str]
) -> None:
    for key in sorted(set(value) - allowed):
        add_error(errors, path, f"unknown {label} field {key!r}")


def require_string(
    value: dict[str, Any], key: str, label: str, path: Path, errors: list[str]
) -> str | None:
    field = value.get(key)
    if not isinstance(field, str) or not field.strip():
        add_error(errors, path, f"{label}.{key} must be a non-empty quoted string")
        return None
    return field


def validate_openai_manifest(
    skill_dir: Path, manifest_path: Path, repo_root: Path, errors: list[str]
) -> None:
    del repo_root
    try:
        payload = parse_yaml_subset(manifest_path)
    except ValidationError as exc:
        add_error(errors, manifest_path, str(exc))
        return

    unknown_keys(payload, {"interface", "policy", "dependencies"}, "top-level", manifest_path, errors)
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        add_error(errors, manifest_path, "interface must be a mapping")
        return
    unknown_keys(
        interface,
        {
            "display_name",
            "short_description",
            "icon_small",
            "icon_large",
            "brand_color",
            "default_prompt",
        },
        "interface",
        manifest_path,
        errors,
    )

    display_name = require_string(interface, "display_name", "interface", manifest_path, errors)
    if display_name is not None and len(display_name) > 64:
        add_error(errors, manifest_path, "interface.display_name must be at most 64 characters")

    short_description = require_string(
        interface, "short_description", "interface", manifest_path, errors
    )
    if short_description is not None and not (25 <= len(short_description) <= 64):
        add_error(
            errors,
            manifest_path,
            "interface.short_description must be 25-64 characters",
        )

    default_prompt = interface.get("default_prompt")
    if default_prompt is not None:
        if not isinstance(default_prompt, str) or not default_prompt.strip():
            add_error(errors, manifest_path, "interface.default_prompt must be a non-empty string")
        elif f"${skill_dir.name}" not in default_prompt:
            add_error(
                errors,
                manifest_path,
                f"interface.default_prompt must mention ${skill_dir.name}",
            )

    brand_color = interface.get("brand_color")
    if brand_color is not None and (
        not isinstance(brand_color, str) or HEX_COLOR_RE.fullmatch(brand_color) is None
    ):
        add_error(errors, manifest_path, "interface.brand_color must use #RRGGBB")

    for icon_field in ("icon_small", "icon_large"):
        icon_path = interface.get(icon_field)
        if icon_path is None:
            continue
        if not isinstance(icon_path, str) or not icon_path.startswith("./assets/"):
            add_error(
                errors,
                manifest_path,
                f"interface.{icon_field} must be a quoted ./assets/ relative path",
            )
            continue
        pure_path = PurePosixPath(icon_path)
        if ".." in pure_path.parts:
            add_error(errors, manifest_path, f"interface.{icon_field} may not traverse upward")
            continue
        resolved = (skill_dir / pure_path).resolve()
        try:
            resolved.relative_to(skill_dir.resolve())
        except ValueError:
            add_error(errors, manifest_path, f"interface.{icon_field} escapes the skill directory")
            continue
        if not resolved.is_file() or resolved.is_symlink():
            add_error(errors, manifest_path, f"interface.{icon_field} does not name a regular asset")

    policy = payload.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            add_error(errors, manifest_path, "policy must be a mapping")
        else:
            unknown_keys(
                policy, {"allow_implicit_invocation"}, "policy", manifest_path, errors
            )
            implicit = policy.get("allow_implicit_invocation")
            if implicit is not None and not isinstance(implicit, bool):
                add_error(
                    errors,
                    manifest_path,
                    "policy.allow_implicit_invocation must be true or false",
                )

    dependencies = payload.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            add_error(errors, manifest_path, "dependencies must be a mapping")
        else:
            unknown_keys(dependencies, {"tools"}, "dependencies", manifest_path, errors)
            tools = dependencies.get("tools")
            if not isinstance(tools, list) or not tools:
                add_error(errors, manifest_path, "dependencies.tools must be a non-empty list")
            else:
                for index, tool in enumerate(tools):
                    label = f"dependencies.tools[{index}]"
                    if not isinstance(tool, dict):
                        add_error(errors, manifest_path, f"{label} must be a mapping")
                        continue
                    unknown_keys(
                        tool,
                        {"type", "value", "description", "transport", "url"},
                        label,
                        manifest_path,
                        errors,
                    )
                    for field in ("type", "value", "description"):
                        require_string(tool, field, label, manifest_path, errors)
                    if tool.get("type") != "mcp":
                        add_error(errors, manifest_path, f"{label}.type currently supports only mcp")
                    for field in ("transport", "url"):
                        if field in tool and (
                            not isinstance(tool[field], str) or not tool[field].strip()
                        ):
                            add_error(errors, manifest_path, f"{label}.{field} must be a string")
                    if isinstance(tool.get("url"), str):
                        parsed_url = urlsplit(tool["url"])
                        if (
                            parsed_url.scheme != "https"
                            or not parsed_url.hostname
                            or parsed_url.username is not None
                            or parsed_url.password is not None
                        ):
                            add_error(errors, manifest_path, f"{label}.url must be a credential-free HTTPS URL")


def validate_skills(repo_root: Path, errors: list[str]) -> list[Path]:
    skills_root = repo_root / "skills"
    if not skills_root.is_dir() or skills_root.is_symlink():
        add_error(errors, "skills", "must be a real directory")
        return []

    skill_dirs: list[Path] = []
    for path in sorted(skills_root.rglob("*")):
        if path.is_symlink():
            add_error(
                errors,
                path.relative_to(repo_root),
                "symlinks are not allowed in published skill packages",
            )
    for entry in sorted(skills_root.iterdir()):
        relative = entry.relative_to(repo_root)
        if entry.is_symlink() or not entry.is_dir():
            add_error(errors, relative, "only real skill directories are allowed directly under skills/")
            continue
        if SKILL_NAME_RE.fullmatch(entry.name) is None:
            add_error(errors, relative, "directory name must be lowercase kebab-case")
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file() or skill_md.is_symlink():
            add_error(errors, relative, "must contain a regular SKILL.md")
            continue
        skill_dirs.append(entry)

        agents_dir = entry / "agents"
        if agents_dir.exists() or agents_dir.is_symlink():
            if agents_dir.is_symlink() or not agents_dir.is_dir():
                add_error(errors, agents_dir.relative_to(repo_root), "must be a real directory")
            else:
                contents = sorted(path.name for path in agents_dir.iterdir())
                if contents != ["openai.yaml"]:
                    add_error(
                        errors,
                        agents_dir.relative_to(repo_root),
                        "the intentional agents/ allowance permits only openai.yaml",
                    )
                manifest = agents_dir / "openai.yaml"
                if manifest.is_file() and not manifest.is_symlink():
                    validate_openai_manifest(entry, manifest, repo_root, errors)
                elif manifest.exists() or manifest.is_symlink():
                    add_error(errors, manifest.relative_to(repo_root), "must be a regular file")
    if not skill_dirs:
        add_error(errors, "skills", "must contain at least one skill")
    return skill_dirs


def validate_script_tree(repo_root: Path, errors: list[str]) -> None:
    scripts_root = repo_root / "scripts"
    if not scripts_root.is_dir() or scripts_root.is_symlink():
        add_error(errors, "scripts", "must be a real directory")
        return
    for path in sorted(scripts_root.rglob("*")):
        if path.is_symlink():
            add_error(errors, path.relative_to(repo_root), "script paths may not be symlinks")


def markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*.md"):
        relative = path.relative_to(repo_root)
        if ".git" in relative.parts:
            continue
        if path.is_file() and not path.is_symlink():
            files.append(path)
    return sorted(files)


def normalize_link_destination(raw: str) -> str:
    destination = raw.strip()
    if destination.startswith("<") and ">" in destination:
        destination = destination[1 : destination.index(">")]
    elif re.search(r"\s+[\"']", destination):
        destination = re.split(r"\s+[\"']", destination, maxsplit=1)[0]
    return destination


def validate_relative_references(repo_root: Path, errors: list[str]) -> None:
    resolved_root = repo_root.resolve()
    for markdown_path in markdown_files(repo_root):
        try:
            contents = markdown_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            add_error(errors, markdown_path.relative_to(repo_root), f"cannot read UTF-8 Markdown: {exc}")
            continue
        destinations = [match.group(1) for match in MARKDOWN_INLINE_LINK_RE.finditer(contents)]
        destinations.extend(match.group(1) for match in MARKDOWN_REFERENCE_RE.finditer(contents))
        for raw_destination in destinations:
            destination = normalize_link_destination(raw_destination)
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or destination.startswith("#"):
                continue
            path_part = unquote(parsed.path)
            if not path_part:
                continue
            if "\\" in path_part or path_part.startswith("/"):
                add_error(
                    errors,
                    markdown_path.relative_to(repo_root),
                    f"relative link must use a repository-local POSIX path: {destination}",
                )
                continue
            resolved = (markdown_path.parent / path_part).resolve()
            try:
                resolved.relative_to(resolved_root)
            except ValueError:
                add_error(
                    errors,
                    markdown_path.relative_to(repo_root),
                    f"relative link escapes the repository: {destination}",
                )
                continue
            if not resolved.exists():
                add_error(
                    errors,
                    markdown_path.relative_to(repo_root),
                    f"relative link target does not exist: {destination}",
                )


def validate_catalog(repo_root: Path, skill_dirs: list[Path], errors: list[str]) -> None:
    readme = repo_root / "README.md"
    try:
        contents = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add_error(errors, "README.md", f"unable to read catalog: {exc}")
        return
    catalog_slugs = re.findall(r"\]\((?:\./)?skills/([^/)]+)/SKILL\.md(?:#[^)]*)?\)", contents)
    expected_slugs = [path.name for path in skill_dirs]
    for slug in expected_slugs:
        count = catalog_slugs.count(slug)
        if count != 1:
            add_error(errors, "README.md", f"catalog must link to skills/{slug}/SKILL.md exactly once (found {count})")
    for slug in sorted(set(catalog_slugs) - set(expected_slugs)):
        add_error(errors, "README.md", f"catalog links to unknown skill {slug!r}")


def top_level_block(text: str, key: str) -> list[str] | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == f"{key}:":
            block: list[str] = []
            for following in lines[index + 1 :]:
                if following and not following.startswith(" ") and not following.startswith("#"):
                    break
                block.append(following)
            return block
    return None


def workflow_run_commands(text: str) -> list[str]:
    lines = text.splitlines()
    commands: list[str] = []
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"(\s*)(?:-\s+)?run:\s*(.*)", lines[index])
        if match is None:
            index += 1
            continue
        indent = len(match.group(1))
        raw_command = match.group(2)
        if raw_command not in {"|", ">", "|-", ">-"}:
            commands.append(raw_command)
            index += 1
            continue
        block_lines: list[str] = []
        index += 1
        while index < len(lines):
            line = lines[index]
            line_indent = len(line) - len(line.lstrip(" "))
            if line.strip() and line_indent <= indent:
                break
            if line.strip():
                block_lines.append(line[indent + 2 :])
            else:
                block_lines.append("")
            index += 1
        commands.append("\n".join(block_lines).strip())
    return commands


def normalized_named_step(text: str, name: str) -> str | None:
    marker = f"      - name: {name}"
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line == marker]
    if len(indexes) != 1:
        return None
    start = indexes[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("      - name:"):
            end = index
            break
    block = lines[start:end]
    while block and (not block[-1].strip() or block[-1].lstrip().startswith("#")):
        block.pop()
    normalized = "\n".join(block)
    return re.sub(
        r"actions/checkout@[0-9a-f]{40}(?:\s+# [^\n]+)?",
        "actions/checkout@<FULL_SHA>",
        normalized,
    )


def workflow_job_block(text: str, job_id: str) -> str | None:
    marker = f"  {job_id}:"
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line == marker]
    if len(indexes) != 1:
        return None
    start = indexes[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.fullmatch(r"  [a-zA-Z_][a-zA-Z0-9_-]*:", lines[index]):
            end = index
            break
    block = lines[start:end]
    while block and not block[-1].strip():
        block.pop()
    return "\n".join(block)


def normalized_workflow_digest(text: str) -> str:
    normalized = re.sub(
        r"actions/checkout@[0-9a-f]{40}(?:[ \t]+#[^\n]*)?",
        "actions/checkout@<FULL_SHA>",
        text,
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate_workflow_file(path: Path, repo_root: Path, errors: list[str]) -> None:
    relative = path.relative_to(repo_root)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add_error(errors, relative, f"unable to read UTF-8 workflow: {exc}")
        return

    permissions = top_level_block(text, "permissions")
    permission_lines = [line.strip() for line in permissions or [] if line.strip() and not line.lstrip().startswith("#")]
    if permission_lines != ["contents: read"]:
        add_error(errors, relative, "top-level permissions must be exactly contents: read")
    if top_level_block(text, "concurrency") is None:
        add_error(errors, relative, "must define top-level concurrency")

    forbidden_patterns = {
        r"(?m)^\s*pull_request_target\s*:": "pull_request_target is forbidden",
        r"(?m)^\s*paths(?:-ignore)?\s*:": "path filters are forbidden so required checks always emit",
        r"\$\{\{[^}]*\bsecrets\b": "workflows may not read secrets through any expression syntax",
        r"\$\{\{[^}]*\bgithub\s*(?:\.token\b|\[\s*['\"]token['\"]\s*\])": "workflows may not expose github.token to commands or inputs",
        r"\$\{\{[^}]*(?i:tojson)\s*\(\s*github\s*\)": "workflows may not serialize the token-bearing github context",
        r"(?m)^ {2,}['\"]?permissions['\"]?\s*:": "job-level permission overrides are forbidden",
        r"(?m)^\s+[A-Za-z-]+:\s*write\s*$": "write permissions are forbidden",
        r"(?m)^\s*permissions:\s*write-all\s*$": "write-all permissions are forbidden",
        r"(?i)runs-on:\s*.*self-hosted": "untrusted content may not reach self-hosted runners",
        r"actions/(?:cache|upload-artifact|download-artifact)@": "caches and artifacts are not allowed in validation workflows",
        r"\$\{\{\s*github\.event\.pull_request\.(?:title|body|head\.label)": "untrusted PR text may not be interpolated into commands",
        r"(?m)(?:^|[{,])\s*['\"]?(?:BASH_ENV|ENV|PATH|SHELLOPTS|LD_PRELOAD|PYTHONPATH|NODE_OPTIONS|RUBYOPT|PERL5OPT)['\"]?\s*:": "shell and runtime startup-hook environment variables are forbidden",
        r"(?m)^\s*(?:defaults|container|services|shell):\s*": "custom shells, defaults, containers, and services are forbidden",
    }
    for pattern, message in forbidden_patterns.items():
        if re.search(pattern, text):
            add_error(errors, relative, message)

    uses_values = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", text)
    for uses_value in uses_values:
        if FULL_SHA_ACTION_RE.fullmatch(uses_value) is None:
            add_error(errors, relative, f"action must use an immutable full commit SHA: {uses_value}")

    checkout_count = sum(value.startswith("actions/checkout@") for value in uses_values)
    persist_false_count = len(re.findall(r"(?m)^\s*persist-credentials:\s*false\s*$", text))
    if checkout_count != persist_false_count:
        add_error(errors, relative, "every checkout must set persist-credentials: false")

    jobs_block = top_level_block(text, "jobs")
    if jobs_block is None:
        add_error(errors, relative, "must define jobs")
        return
    job_ids = [
        match.group(1)
        for line in jobs_block
        if (match := re.fullmatch(r"  ([a-zA-Z_][a-zA-Z0-9_-]*):", line))
    ]
    for index, job_id in enumerate(job_ids):
        start_match = re.search(rf"(?m)^  {re.escape(job_id)}:\s*$", text)
        if start_match is None:
            continue
        remainder = text[start_match.end() :]
        next_job = re.search(r"(?m)^  [a-zA-Z_][a-zA-Z0-9_-]*:\s*$", remainder)
        job_text = remainder[: next_job.start()] if next_job else remainder
        if re.search(r"(?m)^    timeout-minutes:\s*[1-9][0-9]*\s*$", job_text) is None:
            add_error(errors, relative, f"job {job_id!r} must set a positive timeout-minutes")


def validate_workflows(repo_root: Path, errors: list[str]) -> None:
    workflows_root = repo_root / ".github" / "workflows"
    workflows = sorted(workflows_root.glob("*.yml")) + sorted(workflows_root.glob("*.yaml"))
    if not workflows:
        add_error(errors, ".github/workflows", "must contain validation workflows")
        return
    workflow_names = {workflow.name for workflow in workflows}
    expected_names = set(ALLOWED_WORKFLOW_DIGESTS)
    if workflow_names != expected_names:
        unexpected = sorted(workflow_names - expected_names)
        missing = sorted(expected_names - workflow_names)
        detail_parts = []
        if unexpected:
            detail_parts.append(f"unexpected: {', '.join(unexpected)}")
        if missing:
            detail_parts.append(f"missing: {', '.join(missing)}")
        add_error(
            errors,
            ".github/workflows",
            "workflow filenames must match the exact allowlist (" + "; ".join(detail_parts) + ")",
        )
    for workflow in workflows:
        if workflow.is_symlink() or not workflow.is_file():
            add_error(errors, workflow.relative_to(repo_root), "must be a regular file")
            continue
        validate_workflow_file(workflow, repo_root, errors)
        expected_digest = ALLOWED_WORKFLOW_DIGESTS.get(workflow.name)
        if expected_digest is not None:
            workflow_text = workflow.read_text(encoding="utf-8")
            if normalized_workflow_digest(workflow_text) != expected_digest:
                add_error(
                    errors,
                    workflow.relative_to(repo_root),
                    "workflow must match the complete security allowlist; only the checkout full SHA/comment may vary",
                )

    required_workflow = workflows_root / "validate.yml"
    if not required_workflow.is_file():
        add_error(errors, ".github/workflows/validate.yml", "required workflow is missing")
        return
    text = required_workflow.read_text(encoding="utf-8")
    if re.search(
        r"(?m)(?:^|[{,])\s*['\"]?continue-on-error['\"]?\s*:", text
    ):
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "continue-on-error is forbidden in required validation jobs and steps",
        )
    required_fragments = {
        "pull_request:": "must run for every pull request",
        "push:": "must run for default-branch pushes",
        "branches: [main]": "push and pull_request triggers must target main",
        f"name: {REQUIRED_CHECK_NAME}": "must expose the stable aggregate check name",
        "if: ${{ always() }}": "aggregate job must always be emitted",
        "github.event.pull_request.base.sha": "PR validation must check out trusted base scripts",
        "working-directory: trusted": "PR validation must execute from the trusted base checkout",
        "--repo-root \"$GITHUB_WORKSPACE/candidate\" --skip-linker": "PR validation must treat the candidate as data and skip linker execution",
        "working-directory: candidate": "trusted main validation must run the candidate entry point",
        f"github.event.pull_request.base.sha == '{BOOTSTRAP_BASE_SHA}'": "one-time bootstrap must be bound to the original base SHA",
        "github.event.pull_request.author_association == 'OWNER'": "one-time bootstrap must be restricted to the repository owner",
    }
    for fragment, message in required_fragments.items():
        if fragment not in text:
            add_error(errors, required_workflow.relative_to(repo_root), message)
    if text.count(f"name: {REQUIRED_CHECK_NAME}") != 1:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "aggregate check name must occur exactly once",
        )
    aggregate_block = workflow_job_block(text, "aggregate")
    aggregate_needs = (
        re.findall(r"(?m)^    ['\"]?needs['\"]?\s*:.*$", aggregate_block)
        if aggregate_block is not None
        else []
    )
    aggregate_result_sources = (
        re.findall(r"(?m)^          ['\"]?VALIDATE_RESULT['\"]?\s*:.*$", aggregate_block)
        if aggregate_block is not None
        else []
    )
    if aggregate_needs != ["    needs: [validate]"] or aggregate_result_sources != [
        "          VALIDATE_RESULT: ${{ needs.validate.result }}"
    ]:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "aggregate wiring must be exactly needs: [validate] with VALIDATE_RESULT from needs.validate.result",
        )

    bootstrap_scope = f"""if: >-
          github.event_name == 'pull_request' &&
          github.event.pull_request.base.sha == '{BOOTSTRAP_BASE_SHA}' &&
          github.event.pull_request.author_association == 'OWNER'
        working-directory: candidate"""
    normal_pr_scope = f"""if: >-
          github.event_name == 'pull_request' &&
          (github.event.pull_request.base.sha != '{BOOTSTRAP_BASE_SHA}' ||
          github.event.pull_request.author_association != 'OWNER')
        working-directory: trusted"""
    if text.count(bootstrap_scope) != 1 or text.count(normal_pr_scope) != 1:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "bootstrap and normal PR conditions must retain their exact immutable trust scopes",
        )
    if text.count("author_association") != 2 or text.count(BOOTSTRAP_BASE_SHA) != 2:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "bootstrap trust inputs may appear only in the two exact complementary conditions",
        )

    validate_uses = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", text)
    if len(validate_uses) != 2 or any(
        not value.startswith("actions/checkout@") for value in validate_uses
    ):
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "the PR workflow may invoke exactly two actions/checkout steps and no other actions",
        )
    expected_candidate_checkout = """      - name: Check out candidate tree
        uses: actions/checkout@<FULL_SHA>
        with:
          path: candidate
          persist-credentials: false"""
    expected_trusted_checkout = """      - name: Check out trusted validator from the PR base
        if: github.event_name == 'pull_request'
        uses: actions/checkout@<FULL_SHA>
        with:
          ref: ${{ github.event.pull_request.base.sha }}
          path: trusted
          persist-credentials: false"""
    if (
        normalized_named_step(text, "Check out candidate tree")
        != expected_candidate_checkout
        or normalized_named_step(text, "Check out trusted validator from the PR base")
        != expected_trusted_checkout
    ):
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "checkout steps must retain their exact candidate/base refs, paths, and credential settings",
        )
    expected_validate_commands = [
        "./scripts/validate.sh --skip-linker",
        './scripts/validate.sh --repo-root "$GITHUB_WORKSPACE/candidate" --skip-linker',
        "./scripts/validate.sh",
        'if [ "$VALIDATE_RESULT" != "success" ]; then\n'
        '  echo "Repository validation result: $VALIDATE_RESULT" >&2\n'
        "  exit 1\n"
        "fi\n"
        'echo "All required repository validation passed."',
    ]
    if workflow_run_commands(text) != expected_validate_commands:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "run commands must match the narrow bootstrap, data-validation, trusted-main, and aggregate allowlist",
        )
    if text.count("working-directory: trusted") != 1 or text.count(
        "working-directory: candidate"
    ) != 2:
        add_error(
            errors,
            required_workflow.relative_to(repo_root),
            "working-directory scopes must match the one-time bootstrap and trust split",
        )

    link_workflow = workflows_root / "external-links.yml"
    if not link_workflow.is_file():
        add_error(errors, ".github/workflows/external-links.yml", "scheduled trusted-main link check is missing")
    else:
        link_text = link_workflow.read_text(encoding="utf-8")
        for fragment, message in {
            "schedule:": "link check must be scheduled",
            "workflow_dispatch:": "link check must support manual runs",
            "github.ref == 'refs/heads/main'": "manual link checks must be restricted to main",
            "scripts/check-external-links.py": "link workflow must run the bounded SSRF-safe checker",
        }.items():
            if fragment not in link_text:
                add_error(errors, link_workflow.relative_to(repo_root), message)
        expected_link_commands = [
            "python3 scripts/check-external-links.py",
            """if [ "$LINK_RESULT" != "success" ]; then
  echo "::warning::One or more external links could not be verified."
else
  echo "External links passed the bounded health check."
fi""",
        ]
        if workflow_run_commands(link_text) != expected_link_commands:
            add_error(
                errors,
                link_workflow.relative_to(repo_root),
                "link workflow commands must match the trusted-main non-blocking allowlist",
            )
        link_uses = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", link_text)
        expected_link_checkout = """      - name: Check out trusted main
        uses: actions/checkout@<FULL_SHA>
        with:
          ref: refs/heads/main
          persist-credentials: false"""
        if (
            len(link_uses) != 1
            or not link_uses[0].startswith("actions/checkout@")
            or normalized_named_step(link_text, "Check out trusted main")
            != expected_link_checkout
        ):
            add_error(
                errors,
                link_workflow.relative_to(repo_root),
                "link workflow must use only the exact trusted-main checkout step",
            )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    errors: list[str] = []
    if not repo_root.is_dir():
        print(f"error: repository root is not a directory: {repo_root}", file=sys.stderr)
        return 2

    skill_dirs = validate_skills(repo_root, errors)
    validate_script_tree(repo_root, errors)
    validate_catalog(repo_root, skill_dirs, errors)
    validate_relative_references(repo_root, errors)
    validate_workflows(repo_root, errors)

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Catalog, relative references, OpenAI manifests, and workflow security passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
