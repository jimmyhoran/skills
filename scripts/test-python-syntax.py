#!/usr/bin/env python3
"""Negative fixture proving invalid candidate Python fails compile-only validation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    checker = Path(__file__).resolve().with_name("check-python-syntax.py")
    with tempfile.TemporaryDirectory(prefix="skills-python-syntax-") as temporary:
        candidate_scripts = Path(temporary) / "scripts"
        candidate_scripts.mkdir()
        invalid_script = candidate_scripts / "candidate-invalid.py"
        invalid_script.write_text("def invalid(:\n    pass\n", encoding="utf-8")

        completed = subprocess.run(
            [sys.executable, "-I", str(checker), str(candidate_scripts)],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            raise AssertionError("syntax-invalid candidate Python unexpectedly passed")
        if "invalid Python syntax" not in completed.stderr:
            raise AssertionError(
                "syntax fixture failed for the wrong reason:\n" + completed.stderr
            )

    print("[ok] rejected syntax-invalid candidate Python without importing it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
