"""Tests for the adopter-licensing-compliance plan (P1 + P2).

* P2 (this file's initial cut): every shipped ``templates/**/*.py`` manifest
  source carries the SPDX/copyright header within its first 3 lines (after
  any shebang, per plan-review R10); every self-hosted twin under
  ``scripts/``/``tools/`` carries the identical header AND stays byte-identical
  to its ``templates/`` source (the parity check plan-review R3 flagged as
  missing).
* P1 (extended once Chunk C lands): the notice installs to a scratch target,
  is recorded in the lockfile ``files[]``, and appears in ``--manifest``.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_notice_install.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import install_manifest  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

_HEADER_TOKEN = "SPDX-License-Identifier: MIT"

# Cairn's own non-shipped dev tooling under scripts/ (own-repo MIT hygiene,
# not adopter self-propagation -- plan-review R3).
_OWN_ONLY_SCRIPTS = (
    "scripts/check_cairn.py",
    "scripts/measurements.py",
    "scripts/quality_gate.py",
    "scripts/quality_gate_unused_def_whitelist.py",
    "scripts/token_budget.py",
    "scripts/verify_counts.py",
)


def _manifest_py_sources() -> list[str]:
    """Every ``templates/**/*.py`` manifest source, as a repo-relative path."""
    rows = install_manifest(modules=None)
    return sorted(
        f"templates/{src}" for src, _dst, _verbatim in rows if src.endswith(".py")
    )


def _self_hosted_twins() -> list[tuple[str, str]]:
    """``(destination, templates_source)`` pairs for every ``scripts/``/
    ``tools/`` file this repo's own self-hosted tree carries that mirrors a
    manifest source byte-for-byte."""
    rows = install_manifest(modules=None)
    by_dest = {dst: src for src, dst, _verbatim in rows if src.endswith(".py")}
    twins = []
    for prefix in ("scripts/", "tools/"):
        for path in (CAIRN_ROOT / prefix.rstrip("/")).rglob("*.py"):
            dst = str(path.relative_to(CAIRN_ROOT))
            src = by_dest.get(dst)
            if src is not None and (CAIRN_ROOT / "templates" / src).is_file():
                twins.append((dst, f"templates/{src}"))
    return sorted(twins)


def _has_header(path: Path) -> bool:
    with path.open(encoding="utf-8") as fh:
        head = [next(fh, "") for _ in range(4)]
    return any(_HEADER_TOKEN in line for line in head)


def test_manifest_has_the_expected_py_source_count():
    sources = _manifest_py_sources()
    assert len(sources) == 44, (
        f"expected 44 templates/**/*.py manifest sources, found "
        f"{len(sources)} -- if this moved intentionally, update this test"
    )


def test_every_template_py_source_carries_spdx_header():
    missing = [
        src for src in _manifest_py_sources()
        if not _has_header(CAIRN_ROOT / src)
    ]
    assert not missing, "missing SPDX header:\n" + "\n".join(missing)


def test_every_self_hosted_twin_carries_spdx_header():
    twins = _self_hosted_twins()
    assert twins, "expected at least one self-hosted scripts/tools/ twin"
    missing = [
        dst for dst, _src in twins if not _has_header(CAIRN_ROOT / dst)
    ]
    assert not missing, "missing SPDX header:\n" + "\n".join(missing)


def test_every_self_hosted_twin_stays_byte_identical_to_its_source():
    """The parity check plan-review R3 flagged as absent: a header applied
    to one side of a twin pair but not the other (or applied differently)
    would silently diverge Cairn's own self-hosted tree from what
    ``install.py``'s divergence/base-hash check expects."""
    mismatches = []
    for dst, src in _self_hosted_twins():
        dst_bytes = (CAIRN_ROOT / dst).read_bytes()
        src_bytes = (CAIRN_ROOT / src).read_bytes()
        if dst_bytes != src_bytes:
            mismatches.append(f"{dst} != {src}")
    assert not mismatches, "twin parity broken:\n" + "\n".join(mismatches)


def test_own_only_dev_scripts_carry_spdx_header():
    """Cairn's own non-shipped dev tooling -- own-repo MIT hygiene, not
    adopter self-propagation (plan-review R3's second population)."""
    missing = [
        rel for rel in _OWN_ONLY_SCRIPTS
        if not _has_header(CAIRN_ROOT / rel)
    ]
    assert not missing, "missing SPDX header:\n" + "\n".join(missing)


def test_own_only_dev_scripts_are_not_shipped():
    """Sanity guard on the P2 population split (plan-review, independently
    re-derived): these files must have zero manifest rows, or they aren't
    actually 'own-only' and belong in the propagating-set tests above."""
    rows = install_manifest(modules=None)
    shipped_dsts = {dst for _src, dst, _verbatim in rows}
    shipped = [rel for rel in _OWN_ONLY_SCRIPTS if rel in shipped_dsts]
    assert not shipped, f"expected these to be unshipped, but found in manifest: {shipped}"
