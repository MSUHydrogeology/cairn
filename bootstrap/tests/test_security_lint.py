"""
Cairn-dev-only Bandit gate (P2 Chunk 4, finding I3 + plan-review P3.7).

Runs ``python -m bandit`` over the scaffold + Cairn's scripts and fails
on any HIGH/MEDIUM finding not in a small, rationale'd allowlist.  This
is a **Cairn development dependency only** -- it is never installed into,
or required of, an adopter's repository, so it does not collide with the
stdlib-only invariant the *shipped* scripts (claim_check.py /
lifecycle_metrics.py) hold.

Environment behavior (plan-review P3.7): a missing ``bandit`` **fails**
the test in CI (a skipped security gate in CI is a missing one) but
``pytest.skip``s with install guidance locally, so a contributor without
dev-deps is not blocked.  A scanner *error* (rc not in {0,1}) fails
closed, before any allowlist filtering.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

# Scan the executable surface: the scaffold + everything under scripts/
# (check_cairn.py now; content_scan.py once Phase 2 lands) + the two
# packaged reference scripts (shipped verbatim -- keep them clean too).
_SCAN_TARGETS = [
    "bootstrap/scaffold.py",
    "scripts/",
    "templates/modules/default-on/claim_check.py",
    "templates/modules/default-on/lifecycle_metrics.py",
]

_SEVERITY_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
_BLOCKING_RANK = _SEVERITY_RANK["MEDIUM"]

# Triaged-acceptable findings, keyed by (relative file, bandit test_id),
# each with a mandatory rationale.  Kept deliberately small; the
# executable surface is otherwise clean (the subprocess calls are all
# LOW severity -- fixed-arg, no shell -- and fall below the block
# threshold without an entry).
_ALLOWLIST: dict[tuple[str, str], str] = {
    ("scripts/check_cairn.py", "B310"): (
        "urllib.request.urlopen in _probe_external is the OPT-IN external "
        "link probe (off unless --check-external). The URL is a Markdown "
        "link target from Cairn's own tracked tree being verified, not "
        "untrusted runtime input; the call carries a noqa S310 and a HEAD "
        "request only. Not reachable in the default (offline) self-check."
    ),
}


def _in_ci() -> bool:
    return bool(os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))


def _run_bandit() -> tuple[int, str, str]:
    cmd = [
        sys.executable, "-m", "bandit", "-q", "-f", "json",
        *[str(CAIRN_ROOT / t) for t in _SCAN_TARGETS],
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(CAIRN_ROOT), check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _rel(filename: str) -> str:
    try:
        return str(Path(filename).resolve().relative_to(CAIRN_ROOT))
    except ValueError:
        return filename


def test_no_blocking_security_findings() -> None:
    try:
        rc, stdout, stderr = _run_bandit()
    except FileNotFoundError:
        rc, stdout, stderr = 127, "", "No module named bandit"

    bandit_absent = (
        rc == 127
        or "No module named bandit" in stderr
        or "No module named 'bandit'" in stderr
    )
    if bandit_absent:
        if _in_ci():
            pytest.fail(
                "bandit is not installed but this is CI -- a skipped "
                "security gate is a missing one. Install dev deps "
                "(e.g. pip install bandit)."
            )
        pytest.skip(
            "bandit not installed locally; install it to run the security "
            "gate (pip install bandit). Fails (not skips) in CI."
        )

    # Scanner-failure semantics: rc 0 (clean) / 1 (findings) are normal;
    # anything else is a scanner/config error -- fail closed, before any
    # allowlist filtering.
    if rc not in (0, 1):
        pytest.fail(
            f"bandit failed (rc={rc}); allowlist NOT applied.\n"
            f"--- stderr ---\n{stderr}\n--- stdout (head) ---\n{stdout[:1500]}"
        )

    try:
        report = json.loads(stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"bandit stdout not JSON (rc={rc}, {exc}):\n{stdout[:1500]}")

    blocking: list[str] = []
    for f in report.get("results", []) or []:
        if _SEVERITY_RANK.get(f.get("issue_severity", "LOW"), 0) < _BLOCKING_RANK:
            continue
        key = (_rel(f["filename"]), str(f["test_id"]))
        if key in _ALLOWLIST:
            continue
        blocking.append(
            f"  [{f['test_id']} {f['issue_severity']}] {key[0]}:"
            f"{f['line_number']}  {f['issue_text']}"
        )

    if blocking:
        pytest.fail(
            f"bandit found {len(blocking)} blocking finding(s) "
            f"(severity >= MEDIUM) not in the allowlist:\n"
            + "\n".join(blocking)
            + "\nFix the code or add a rationale'd _ALLOWLIST entry."
        )


def test_allowlist_entries_have_rationale() -> None:
    """Every allowlist entry carries a non-empty rationale -- a
    suppression without a reason is how the discipline rots."""
    for key, rationale in _ALLOWLIST.items():
        assert rationale.strip(), f"empty rationale for {key}"
