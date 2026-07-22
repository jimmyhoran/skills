#!/usr/bin/env python3
"""Negative fixtures for the workflow-security policy."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_checker(script_path: Path) -> ModuleType:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("repository_checker", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_workflow_copy(
    checker: ModuleType,
    repo_root: Path,
    workflow_name: str,
    mutate: Callable[[str], str],
) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="skills-workflow-policy-") as temporary:
        fixture_root = Path(temporary)
        fixture_workflows = fixture_root / ".github" / "workflows"
        shutil.copytree(repo_root / ".github" / "workflows", fixture_workflows)
        target = fixture_workflows / workflow_name
        original = target.read_text(encoding="utf-8")
        mutated = mutate(original)
        if mutated == original:
            raise AssertionError(f"fixture for {workflow_name} did not change its input")
        target.write_text(mutated, encoding="utf-8")
        errors: list[str] = []
        checker.validate_workflows(fixture_root, errors)
        return errors


def validate_extra_workflow(checker: ModuleType, repo_root: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="skills-workflow-policy-") as temporary:
        fixture_root = Path(temporary)
        fixture_workflows = fixture_root / ".github" / "workflows"
        shutil.copytree(repo_root / ".github" / "workflows", fixture_workflows)
        shutil.copy2(
            fixture_workflows / "external-links.yml",
            fixture_workflows / "unexpected.yml",
        )
        errors: list[str] = []
        checker.validate_workflows(fixture_root, errors)
        return errors


def require_rejection(label: str, errors: list[str], expected: str) -> None:
    if not errors:
        raise AssertionError(f"{label}: unsafe workflow unexpectedly passed")
    if not any(expected in error for error in errors):
        details = "\n".join(f"  - {error}" for error in errors)
        raise AssertionError(f"{label}: expected rejection containing {expected!r}\n{details}")


def replace_once(original: str, old: str, new: str) -> str:
    if original.count(old) != 1:
        raise AssertionError(f"fixture anchor must occur exactly once: {old!r}")
    return original.replace(old, new, 1)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    checker = load_checker(repo_root / "scripts" / "check-repository.py")

    baseline_errors: list[str] = []
    checker.validate_workflows(repo_root, baseline_errors)
    if baseline_errors:
        details = "\n".join(f"  - {error}" for error in baseline_errors)
        raise AssertionError(f"baseline workflows must pass before fixtures run\n{details}")

    fixtures: list[tuple[str, str, Callable[[str], str], str]] = [
        (
            "job-level contents write",
            "validate.yml",
            lambda text: replace_once(
                text,
                "    timeout-minutes: 15\n",
                "    timeout-minutes: 15\n    permissions:\n      contents: write\n",
            ),
            "job-level permission overrides are forbidden",
        ),
        (
            "write-all shorthand",
            "validate.yml",
            lambda text: replace_once(
                text,
                "permissions:\n  contents: read",
                "permissions: write-all",
            ),
            "write-all permissions are forbidden",
        ),
        (
            "JSON-style quoted job permissions",
            "validate.yml",
            lambda text: replace_once(
                text,
                "    timeout-minutes: 15\n",
                "    timeout-minutes: 15\n    \"permissions\": {\"contents\": write}\n",
            ),
            "job-level permission overrides are forbidden",
        ),
        (
            "bracket secret lookup",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        working-directory: candidate\n        run: ./scripts/validate.sh --skip-linker",
                "        working-directory: candidate\n        env:\n          LEAK: ${{ secrets['TOKEN'] }}\n        run: ./scripts/validate.sh --skip-linker",
            ),
            "workflows may not read secrets through any expression syntax",
        ),
        (
            "toJSON secrets lookup",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        working-directory: candidate\n        run: ./scripts/validate.sh --skip-linker",
                "        working-directory: candidate\n        env:\n          LEAK: ${{ toJSON(secrets) }}\n        run: ./scripts/validate.sh --skip-linker",
            ),
            "workflows may not read secrets through any expression syntax",
        ),
        (
            "bracket github token lookup",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        working-directory: candidate\n        run: ./scripts/validate.sh --skip-linker",
                "        working-directory: candidate\n        env:\n          LEAK: ${{ github['token'] }}\n        run: ./scripts/validate.sh --skip-linker",
            ),
            "workflows may not expose github.token",
        ),
        (
            "unquoted startup-hook key",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        working-directory: candidate\n        run: ./scripts/validate.sh --skip-linker",
                "        working-directory: candidate\n        env:\n          BASH_ENV: /tmp/untrusted-hook\n        run: ./scripts/validate.sh --skip-linker",
            ),
            "shell and runtime startup-hook environment variables are forbidden",
        ),
        (
            "quoted startup-hook key",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        working-directory: candidate\n        run: ./scripts/validate.sh --skip-linker",
                "        working-directory: candidate\n        env:\n          \"BASH_ENV\": /tmp/untrusted-hook\n        run: ./scripts/validate.sh --skip-linker",
            ),
            "shell and runtime startup-hook environment variables are forbidden",
        ),
        (
            "workflow PATH hijack",
            "validate.yml",
            lambda text: replace_once(
                text,
                "permissions:\n  contents: read\n",
                "env:\n  PATH: candidate/bin\n\npermissions:\n  contents: read\n",
            ),
            "shell and runtime startup-hook environment variables are forbidden",
        ),
        (
            "job continue-on-error",
            "validate.yml",
            lambda text: replace_once(
                text,
                "    timeout-minutes: 15\n",
                "    timeout-minutes: 15\n    continue-on-error: true\n",
            ),
            "continue-on-error is forbidden",
        ),
        (
            "step continue-on-error",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        run: ./scripts/validate.sh --skip-linker\n",
                "        run: ./scripts/validate.sh --skip-linker\n        continue-on-error: true\n",
            ),
            "continue-on-error is forbidden",
        ),
        (
            "aggregate dependency bypass",
            "validate.yml",
            lambda text: replace_once(
                text,
                "    needs: [validate]\n",
                "    needs: []\n",
            ),
            "aggregate wiring must be exactly needs: [validate]",
        ),
        (
            "aggregate result bypass",
            "validate.yml",
            lambda text: replace_once(
                text,
                "          VALIDATE_RESULT: ${{ needs.validate.result }}\n",
                "          VALIDATE_RESULT: success\n",
            ),
            "aggregate wiring must be exactly needs: [validate]",
        ),
        (
            "broadened bootstrap",
            "validate.yml",
            lambda text: replace_once(
                text,
                "github.event.pull_request.author_association == 'OWNER'",
                "github.event.pull_request.author_association == 'OWNER' || true",
            ),
            "bootstrap and normal PR conditions must retain their exact immutable trust scopes",
        ),
        (
            "mutable action tag",
            "validate.yml",
            lambda text: replace_once(
                text,
                "      - name: Check out candidate tree\n"
                "        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "      - name: Check out candidate tree\n"
                "        uses: actions/checkout@v7.0.1",
            ),
            "action must use an immutable full commit SHA",
        ),
        (
            "checkout repository override",
            "validate.yml",
            lambda text: replace_once(
                text,
                "        with:\n          path: candidate\n",
                "        with:\n          repository: attacker/repository\n          path: candidate\n",
            ),
            "checkout steps must retain their exact candidate/base refs",
        ),
        (
            "extra PR command",
            "validate.yml",
            lambda text: replace_once(
                text,
                "  aggregate:\n",
                "  unexpected:\n    runs-on: ubuntu-latest\n    timeout-minutes: 2\n    steps:\n      - run: ./candidate/scripts/untrusted.sh\n\n  aggregate:\n",
            ),
            "run commands must match the narrow bootstrap",
        ),
    ]

    for label, workflow_name, mutation, expected in fixtures:
        errors = validate_workflow_copy(checker, repo_root, workflow_name, mutation)
        require_rejection(label, errors, expected)
        print(f"[ok] rejected {label}")

    extra_workflow_errors = validate_extra_workflow(checker, repo_root)
    require_rejection(
        "unexpected workflow filename",
        extra_workflow_errors,
        "workflow filenames must match the exact allowlist",
    )
    print("[ok] rejected unexpected workflow filename")

    print(f"Workflow security rejected all {len(fixtures) + 1} unsafe fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
