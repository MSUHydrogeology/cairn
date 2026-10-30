#!/usr/bin/env python3
"""Run the interpreter-binding Windows evidence checks on native Windows.

Run from a clean committed checkout using Python 3.13 with pytest and Git
installed: python scripts/run_windows_interpreter_binding.py. Preserve the
output and commit ID in the plan's verification record. Any failed or skipped
required case remains open; this runner does not certify the whole tree.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    if os.name != "nt":
        print("Native Windows is required; no Windows evidence was collected.", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    print(f"Interpreter: {sys.executable} ({sys.version})", flush=True)
    subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True)
    subprocess.run(["git", "status", "--short"], cwd=root, check=True)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-ra", "bootstrap/tests/test_git_interpreter_binding_portable.py"],
        cwd=root,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
