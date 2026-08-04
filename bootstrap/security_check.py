#!/usr/bin/env python3
"""Cairn release security check -- fail-closed (never skips).

The dev-time Bandit gate (``bootstrap/tests/test_security_lint.py``)
*skips* when Bandit is absent locally, so a contributor without dev-deps
is not blocked. That is the wrong posture for a **release**: "the security
gate may have skipped on the machine that cut the release" is not
acceptable evidence. This command is the release-facing counterpart -- it
**fails closed**. A missing Bandit, a scanner error, a requested file the
scanner could not open, or any unallowlisted MEDIUM+ finding is a non-zero
exit.

Run from the Cairn repo root, before cutting a release (and record its
output in the release notes / checklist):

    python bootstrap/security_check.py

It scans the same **derived** executable surface as the dev gate -- every
file the scaffold ships **byte-for-byte** as Python, derived from the
published install manifest (``install_manifest``, the same enumeration
behind ``scaffold.py --manifest``), plus Cairn's own dev scripts and the
scaffold engine -- and runs the Markdown self-check
(``scripts/check_cairn.py``). Exit 0 only if both pass. This module is the
single source of the scan-target set and the Bandit allowlist; the dev
gate imports them (no second drift-prone copy).

Security-hardening Chunk 7 / R1; manifest derivation per the
``scan-coverage`` plan.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.config import (  # noqa: E402  (trust anchor: narrowest owner, plan 0B.3 / Stage 4)
    _ALWAYS_ON_MAPPINGS,
    _MODULE_MAPPINGS,
)
from bootstrap._scaffold.install import install_manifest  # noqa: E402

_BLOCKING_SEVERITIES = {"MEDIUM", "HIGH"}

#: Triaged-acceptable Bandit findings, keyed by (repo-relative file,
#: test_id), each with a mandatory rationale. The single source of truth
#: for both this release command and the dev gate.
ALLOWLIST: dict[tuple[str, str], str] = {
    ("templates/modules/team-gated/link_check.py", "B310"): (
        "urllib.request.urlopen in link_check._probe_external is the OPT-IN "
        "external-link probe (off unless --check-external) and is SSRF-guarded: "
        "http(s)-only, manual redirects with per-hop host validation (is_global "
        "allowlist; non-public IPs refused), and no proxy/auth/netrc handlers. "
        "Cairn's own check_cairn composes this shipped tool, so the finding "
        "lives here."
    ),
}


def scan_targets() -> list[str]:
    """The executable surface to scan, derived from Cairn's source of truth:
    every **verbatim** (byte-for-byte, un-substituted) ``.py`` in the
    published install manifest -- the artifacts an adopter runs as code --
    plus Cairn's own dev executables (``scripts/*.py`` + the top-level
    ``bootstrap/`` tools) and the whole scaffold engine package, as explicit
    files. A newly-shipped script is covered automatically; there is no
    hand-maintained list to drift.

    The two registry loops below (``_MODULE_MAPPINGS``, ``_ALWAYS_ON_MAPPINGS``)
    are strictly redundant once the manifest union lands -- measured, their
    42 entries are a subset of the manifest's 44 -- and are **retained on
    purpose**: they are ``set.add`` calls into the same accumulator, so
    "this change cannot shrink the scanned surface" is true by inspection
    rather than by measurement. They are defence in depth, not a second
    guard: what actually catches a shipped ``.py`` falling out of this set is
    the on-disk oracle in ``bootstrap/tests/test_security_lint.py``, whose
    input this function never reads."""
    targets: set[str] = set()
    for specs in _MODULE_MAPPINGS.values():
        for spec in specs:
            if spec.verbatim and spec.src.endswith(".py"):
                targets.add(f"templates/modules/{spec.src}")
    # Always-on EXECUTABLE helpers (onboarding launcher + _onboarding/ engine):
    # the same shipped-verbatim-.py class as a module script, but delivered
    # unconditionally OUTSIDE _MODULE_MAPPINGS (install._ALWAYS_ON_MAPPINGS). They
    # were release-unscanned while side-door-delivered; including them here closes
    # that PRE-EXISTING Bandit blind spot, not just a new one (R1 / side-door
    # parity). Same `templates/modules/{src}` join as the module loop above.
    for spec in _ALWAYS_ON_MAPPINGS:
        if spec.verbatim and spec.src.endswith(".py"):
            targets.add(f"templates/modules/{spec.src}")
    # Cairn's own dev executables: scripts/*.py + the top-level bootstrap/
    # tools (scaffold, security_check, verify_integrity). Non-recursive, so
    # bootstrap/tests/ -- which carry intentional attack fixtures -- are not
    # scanned.
    for sub in ("scripts", "bootstrap"):
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in (CAIRN_ROOT / sub).glob("*.py")
        )
    # The scaffold engine package (post-split; plan 2026-06-05-scaffold-split,
    # RR3/S4): RECURSE it -- every module under bootstrap/_scaffold/ is
    # privileged implementation, equal in authority to the old monolith, so the
    # non-recursive bootstrap/*.py glob above would leave the engine's guts
    # unscanned after the split. bootstrap/tests/ (intentional attack fixtures)
    # stays excluded. A no-op until the package exists (Stage 0B), so the Bandit
    # surface is unchanged today.
    engine_pkg = CAIRN_ROOT / "bootstrap" / "_scaffold"
    if engine_pkg.is_dir():
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in engine_pkg.rglob("*.py")
        )
    # Every verbatim .py the scaffold ACTUALLY installs, from the published
    # install manifest -- the same enumeration adopters depend on through
    # `scaffold.py --manifest`. Two facts here are load-bearing:
    #   * `modules=None` means the FULL published catalog. A module subset
    #     would silently shrink the scanned surface, and nothing downstream
    #     would say so.
    #   * This is a UNION WITH the two registry loops above, never a
    #     replacement for them. That framing is what makes "coverage cannot
    #     shrink" checkable by inspection instead of by measurement.
    # It closes a real, 63-day-old miss: `_SKILLS_MAPPINGS` ships the two
    # session-lifecycle tools unconditionally to every adoption and no loop
    # above reaches them (scan-coverage plan, Chunk B / proposal items 1-2).
    for src, _dst, verbatim in install_manifest(modules=None):
        if verbatim and src.endswith(".py"):
            targets.add(f"templates/{src}")
    return sorted(targets)


def _rel(filename: str) -> str:
    try:
        return str(Path(filename).resolve().relative_to(CAIRN_ROOT))
    except ValueError:
        return filename


def run_bandit() -> int:
    """Run Bandit over the derived surface; fail closed on absence/error."""
    # `install_manifest` REFUSES a malformed mapping (duplicate destinations)
    # by raising ValueError. This wrapper is legibility, not new safety:
    # main() wraps run_bandit() in no handler, so an uncaught ValueError
    # already exits non-zero -- it buys a security message instead of a
    # traceback (scan-coverage plan, Chunk B / proposal item 2).
    try:
        scanned = scan_targets()
    except ValueError as exc:
        print("security_check: cannot enumerate the shipped surface "
              f"({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    targets = [str(CAIRN_ROOT / t) for t in scanned]
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "bandit", "-q", "-f", "json", *targets],
            capture_output=True, text=True, check=False, cwd=str(CAIRN_ROOT),
        )
    except OSError as exc:
        print(f"security_check: cannot run bandit ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1
    if (proc.returncode == 127
            or "No module named bandit" in proc.stderr
            or "No module named 'bandit'" in proc.stderr):
        print("security_check: bandit is NOT installed -- FAIL CLOSED. A "
              "release security gate must not be skippable; install bandit "
              "(pip install bandit) and re-run.", file=sys.stderr)
        return 1
    if proc.returncode not in (0, 1):
        print(f"security_check: bandit error (rc={proc.returncode}) -- fail "
              f"closed.\n{proc.stderr[:800]}", file=sys.stderr)
        return 1
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("security_check: bandit output was not JSON -- fail closed.",
              file=sys.stderr)
        return 1
    # A file Bandit could not READ is not a file Bandit found clean. Bandit
    # records such a failure (missing file, unparseable source) in the JSON
    # `errors` array, scans the rest, and exits 0 -- so the rc branch above
    # never fires and the run reports clean over a file it never opened.
    # Fail closed here, BEFORE allowlist filtering, matching the scanner-error
    # posture above (scan-coverage plan, Chunk A / [I1]).
    errors = report.get("errors") or []
    if errors:
        detail = "\n".join(
            f"  {_rel(str(e.get('filename', '?')))}: {e.get('reason', '?')}"
            for e in errors
        )
        print("security_check: bandit could not scan "
              f"{len(errors)} requested file(s) -- fail closed. A file the "
              "scanner never opened is not a file it found clean.\n" + detail,
              file=sys.stderr)
        return 1
    blocking = [
        f"  [{f['test_id']} {f['issue_severity']}] {_rel(f['filename'])}:"
        f"{f['line_number']}  {f['issue_text']}"
        for f in (report.get("results") or [])
        if f.get("issue_severity") in _BLOCKING_SEVERITIES
        and (_rel(f["filename"]), str(f["test_id"])) not in ALLOWLIST
    ]
    if blocking:
        print("security_check: unallowlisted MEDIUM+ Bandit finding(s):\n"
              + "\n".join(blocking), file=sys.stderr)
        return 1
    print(f"security_check: Bandit clean over {len(targets)} shipped file(s).")
    return 0


def run_check_cairn() -> int:
    """Run the Markdown self-check (link / claim / content integrity)."""
    script = CAIRN_ROOT / "scripts" / "check_cairn.py"
    if not script.is_file():
        print(f"security_check: {script} missing -- fail closed.",
              file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(script)],
                          cwd=str(CAIRN_ROOT), check=False).returncode


def main() -> int:
    rc = run_bandit() | run_check_cairn()
    if rc == 0:
        print("security_check: PASS -- release security gate clean.")
    else:
        print("security_check: FAIL -- resolve the above before release.",
              file=sys.stderr)
    return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
