"""Lightweight "build" step for this sample project.

This repository is an app-style FastAPI project (not a packaged library).
So "build" here means:
- bytecode/syntax compilation check across the repo
- import checks for main entrypoints

Usage:
  python run_build.py
"""

from __future__ import annotations

import compileall
import importlib
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent

    ok = compileall.compile_dir(
        str(repo_root),
        quiet=1,
        force=False,
    )
    if not ok:
        print("compileall failed")
        return 1

    # Import checks (fail fast if dependencies/import graph is broken)
    importlib.import_module("main")
    importlib.import_module("secure_main")

    print("build ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
