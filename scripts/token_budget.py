#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Always-on token budget — measure the prefix every turn pays for.

The token-efficiency doctrine's governing rule (principle 6): you cannot hold a
token gain you do not measure. This is the sibling of ``check_cairn`` /
``claim_check`` for that rule — it measures the **always-on load manifest** (the
files an agent's harness auto-loads on *every* turn) and flags growth against a
soft cap.

What counts is the *manifest*, not two hard-coded filenames: an explicit list of
auto-loaded files. Pass them, or let the tool auto-detect the common adopter
shape in the CWD (the vendor wrapper + ``AGENTS.md`` + ``RULES.md``). A file that
is *invoked on demand* (a skill body) is NOT always-on and must not be listed —
that is the loophole this measure closes.

Token denomination: a real tokenizer (``tiktoken``, ``cl100k_base``) when
importable; otherwise an explicitly-labelled ``chars / 4`` proxy. The estimator
in use is always printed, so a proxy figure is never mistaken for a true count.

Soft-cap by default (warn, never block): exit 0 even over cap. ``--strict``
makes an over-cap run exit 1 (for a CI gate the adopter opts into).

Usage:
    python scripts/token_budget.py [FILE ...] [--cap N] [--strict] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Vendor-wrapper names an adopter might auto-load (renamed from VENDOR.md).
_WRAPPER_NAMES = ("CLAUDE.md", "GEMINI.md", "VENDOR.md", "AGENTS.local.md")
# The always-on core an adopter loads on every turn.
_CORE_NAMES = ("AGENTS.md", "RULES.md")


def _detect_manifest(root: Path) -> list[Path]:
    """The common adopter always-on shape, in cache-stable order (stable first)."""
    found: list[Path] = []
    for name in _WRAPPER_NAMES + _CORE_NAMES:
        p = root / name
        if p.is_file() and p not in found:
            found.append(p)
    return found


def _counter():
    """Return (count_fn, label). Prefer a real tokenizer; else a labelled proxy."""
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")
        return (lambda s: len(enc.encode(s)), "tiktoken/cl100k_base")
    except Exception:
        # Honest proxy — labelled so it is never read as a true token count.
        return (lambda s: round(len(s) / 4), "chars/4 proxy (estimate)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="always-on manifest files (auto-detect if omitted)")
    ap.add_argument("--cap", type=int, default=None, help="soft cap on total tokens")
    ap.add_argument("--strict", action="store_true", help="exit 1 when over cap (default: warn only)")
    ap.add_argument("--json", action="store_true", help="emit a JSON report")
    args = ap.parse_args(argv)

    root = Path.cwd()
    paths = [Path(f) for f in args.files] if args.files else _detect_manifest(root)
    if not paths:
        print("token_budget: no manifest files given and none auto-detected "
              f"(looked for {', '.join(_WRAPPER_NAMES + _CORE_NAMES)}).", file=sys.stderr)
        return 2

    count, label = _counter()
    rows, total_tok, total_bytes, missing = [], 0, 0, []
    for p in paths:
        if not p.is_file():
            missing.append(str(p))
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        tok = count(text)
        nbytes = len(text.encode("utf-8"))
        rows.append({"file": str(p), "tokens": tok, "bytes": nbytes})
        total_tok += tok
        total_bytes += nbytes

    over = args.cap is not None and total_tok > args.cap
    report = {"estimator": label, "files": rows, "missing": missing,
              "total_tokens": total_tok, "total_bytes": total_bytes,
              "cap": args.cap, "over_cap": over}

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"token_budget: always-on manifest ({label})")
        for r in rows:
            print(f"  {r['tokens']:>7,} tok  {r['bytes']:>7,} B  {r['file']}")
        if missing:
            print(f"  (missing, skipped: {', '.join(missing)})")
        cap_note = f" / cap {args.cap:,}" if args.cap is not None else ""
        print(f"  {'-' * 30}")
        print(f"  {total_tok:>7,} tok  {total_bytes:>7,} B  TOTAL{cap_note}")
        if over:
            print(f"token_budget: WARNING — over cap by {total_tok - args.cap:,} tokens.")
        elif args.cap is not None:
            print(f"token_budget: OK — {args.cap - total_tok:,} tokens under cap.")

    if missing and not args.files:
        # auto-detect missing is informational; explicit-missing is an error
        pass
    elif missing:
        return 2
    return 1 if (over and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
