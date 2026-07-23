#!/usr/bin/env python3
"""Parse repository Python scripts as data without importing or executing them."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 10 * 1024 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile-only Python syntax validation.")
    parser.add_argument("scripts_root")
    return parser.parse_args()


def validate_python_tree(scripts_root: Path) -> list[str]:
    errors: list[str] = []
    if scripts_root.is_symlink() or not scripts_root.is_dir():
        return [f"{scripts_root}: must be a real directory"]

    total_bytes = 0
    python_files = sorted(scripts_root.rglob("*.py"))
    for path in python_files:
        if path.is_symlink() or not path.is_file():
            errors.append(f"{path}: must be a regular, non-symlink Python file")
            continue
        try:
            source = path.read_bytes()
        except OSError as exc:
            errors.append(f"{path}: unable to read: {exc}")
            continue
        file_bytes = len(source)
        total_bytes += file_bytes
        if file_bytes > MAX_FILE_BYTES:
            errors.append(f"{path}: exceeds the {MAX_FILE_BYTES}-byte per-file syntax limit")
            continue
        if total_bytes > MAX_TOTAL_BYTES:
            errors.append(
                f"{scripts_root}: exceeds the {MAX_TOTAL_BYTES}-byte total Python syntax limit"
            )
            break
        try:
            # ast.parse compiles syntax only. It does not import the module or
            # execute top-level statements, decorators, annotations, or hooks.
            ast.parse(source, filename=str(path), type_comments=True)
        except (SyntaxError, ValueError, UnicodeError) as exc:
            line = getattr(exc, "lineno", None)
            location = f":{line}" if line is not None else ""
            errors.append(f"{path}{location}: invalid Python syntax: {exc}")
    return errors


def main() -> int:
    args = parse_args()
    scripts_root = Path(args.scripts_root).expanduser()
    if not scripts_root.is_absolute():
        scripts_root = Path.cwd() / scripts_root
    errors = validate_python_tree(scripts_root)
    if errors:
        print("Python syntax validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = sum(1 for path in scripts_root.rglob("*.py") if path.is_file())
    print(f"Python syntax passed for {count} script files (compile-only; nothing imported).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
