#!/usr/bin/env python3
"""Cairn install-integrity check -- on-disk files vs. the lockfile (R10).

A Cairn install records every written file's SHA-256 in
``dev/.cairn/cairn-lock.yml`` (the module-upgrade arc owns that schema). This
command **verifies** an installed tree against it: it recomputes each
recorded file's hash and reports any **mismatch** (a file modified after
install -- e.g. a tampered shipped script) or **missing** file. It is a
**lockfile-backed preflight**, not an in-file self-verifier: the check lives
*outside* the files it verifies, so there is no bootstrapping problem (a
backdoored script cannot vouch for itself).

It **fails closed**: a missing / unparseable lockfile, a lockfile that
records no files, or any hash mismatch / missing file is a non-zero exit.

Run against an installed target before trusting its scripts:

    python bootstrap/verify_integrity.py --target <repo>

Standard-library only. Reuses the lockfile reader from ``scaffold.py`` so
the schema is single-sourced (this command never writes the lockfile;
``cairn-module-upgrade-3way-merge`` owns its schema + version).

Exit codes: ``0`` every recorded file matches; ``1`` an integrity violation
or a fail-closed condition; ``2`` usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import _LOCKFILE_REL, read_lockfile  # noqa: E402


def verify(target: Path) -> int:
    lock = read_lockfile(target)
    if lock is None:
        print(f"verify_integrity: no/unparseable {_LOCKFILE_REL} under "
              f"{target} -- FAIL CLOSED (cannot attest integrity without a "
              f"lockfile).", file=sys.stderr)
        return 1
    files = lock.get("files") or []
    if not files:
        print(f"verify_integrity: {_LOCKFILE_REL} records no files -- FAIL "
              f"CLOSED.", file=sys.stderr)
        return 1

    violations: list[str] = []
    target_resolved = target.resolve()
    for rec in files:
        dst_rel = rec.get("dst")
        recorded = rec.get("hash", "")
        # The lockfile is itself a tamper target, so fail closed on a
        # malformed record *before* reading anything: a record must name a
        # contained, repo-relative dst with a well-formed sha256 hash.
        # Without this, a `dst: ../outside` could make the check "attest" a
        # file outside the installed tree and still print OK.
        if not isinstance(dst_rel, str) or not dst_rel:
            violations.append(f"  malformed record (no dst): {rec!r}")
            continue
        rel = Path(dst_rel)
        if rel.is_absolute() or ".." in rel.parts:
            violations.append(f"  unsafe dst (absolute / .. escape): {dst_rel}")
            continue
        if not (isinstance(recorded, str) and recorded.startswith("sha256:")):
            violations.append(f"  malformed hash for {dst_rel}: {recorded!r}")
            continue
        dst = (target / rel).resolve()
        if dst != target_resolved and target_resolved not in dst.parents:
            violations.append(f"  dst escapes the target tree: {dst_rel}")
            continue
        if not dst.is_file():
            violations.append(f"  missing: {dst_rel}")
            continue
        actual = "sha256:" + hashlib.sha256(dst.read_bytes()).hexdigest()
        if actual != recorded:
            violations.append(f"  modified (hash mismatch): {dst_rel}")

    if violations:
        print(f"verify_integrity: {len(violations)} integrity violation(s) "
              f"vs. {_LOCKFILE_REL}:\n" + "\n".join(violations)
              + "\nThe on-disk tree no longer matches its recorded install. "
              "Do not trust the shipped scripts until this is resolved.",
              file=sys.stderr)
        return 1
    print(f"verify_integrity: OK -- {len(files)} recorded file(s) match "
          f"{_LOCKFILE_REL}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify_integrity",
        description="Verify an installed Cairn tree against its lockfile "
                    "(fail-closed SHA-256 integrity check).")
    parser.add_argument("--target", type=Path, required=True,
                        help="The installed repository to verify.")
    args = parser.parse_args(argv)
    target = args.target.resolve()
    if not target.is_dir():
        print(f"verify_integrity: target is not a directory: {target}",
              file=sys.stderr)
        return 2
    return verify(target)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
