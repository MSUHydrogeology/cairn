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
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import _MODULE_MAPPINGS  # noqa: E402
# The derived scan-target set and the Bandit allowlist are single-sourced in
# the release command (bootstrap/security_check.py); the dev gate imports
# them so the two never drift (security-hardening Chunk 2 / R2 + Chunk 7).
from bootstrap.security_check import (  # noqa: E402
    ALLOWLIST as _ALLOWLIST,
    scan_targets as _scan_targets,
)

_SEVERITY_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
_BLOCKING_RANK = _SEVERITY_RANK["MEDIUM"]


def _in_ci() -> bool:
    return bool(os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))


def _run_bandit() -> tuple[int, str, str]:
    cmd = [
        sys.executable, "-m", "bandit", "-q", "-f", "json",
        *[str(CAIRN_ROOT / t) for t in _scan_targets()],
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


def test_scan_targets_cover_all_shipped_scripts() -> None:
    """Coverage is derived from the source of truth, not a hand list: every
    verbatim .py shipped via _MODULE_MAPPINGS is in the scanned set (so a
    9th reference script is auto-covered), and Cairn's dev executables are
    covered too. This is the anti-drift assertion (R2) -- the previous miss
    was a stale inventory + a non-recursing directory target."""
    targets = set(_scan_targets())
    shipped = {
        f"templates/modules/{spec.src}"
        for specs in _MODULE_MAPPINGS.values()
        for spec in specs
        if spec.verbatim and spec.src.endswith(".py")
    }
    assert shipped, "expected at least one verbatim .py reference script"
    missing = shipped - targets
    assert not missing, f"shipped scripts not scanned: {sorted(missing)}"
    for dev in ("bootstrap/scaffold.py", "scripts/check_cairn.py",
                # content_scan moved to the content-security module (single
                # source); it is now covered via the verbatim derivation.
                "templates/modules/team-gated/content_scan.py"):
        assert dev in targets, dev
    # No bare directory target (the no-`-r` footgun) -- every target is a file.
    for t in _scan_targets():
        assert t.endswith(".py"), f"non-file scan target: {t}"


def test_scan_targets_recurses_the_scaffold_engine_package(tmp_path, monkeypatch) -> None:
    """RR3/S4 (scaffold-split 0A.1): when the post-split engine package exists,
    EVERY .py under bootstrap/_scaffold/ is scanned recursively (the engine's
    guts can't fall out of the release Bandit gate), while bootstrap/tests/
    (intentional attack fixtures) stays excluded. A no-op until Stage 0B creates
    the package; this exercises the capability now against a throwaway tree."""
    import bootstrap.security_check as sc

    (tmp_path / "scripts").mkdir()
    (tmp_path / "bootstrap" / "_scaffold" / "sub").mkdir(parents=True)
    (tmp_path / "bootstrap" / "scaffold.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "_scaffold" / "engine.py").write_text("y = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "_scaffold" / "sub" / "deep.py").write_text("z = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "tests").mkdir()
    (tmp_path / "bootstrap" / "tests" / "attack_fixture.py").write_text("evil = 1\n", encoding="utf-8")
    monkeypatch.setattr(sc, "CAIRN_ROOT", tmp_path)

    targets = set(sc.scan_targets())
    assert "bootstrap/_scaffold/engine.py" in targets
    assert "bootstrap/_scaffold/sub/deep.py" in targets, "recursion must reach nested modules"
    assert "bootstrap/scaffold.py" in targets
    assert "bootstrap/tests/attack_fixture.py" not in targets, "attack fixtures must stay excluded"
