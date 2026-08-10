"""Tests for the adopter-licensing-compliance plan (P1 + P2).

* P2: every shipped ``templates/**/*.py`` manifest source carries the
  SPDX/copyright header within its first 3 lines (after any shebang, per
  plan-review R10); every self-hosted twin under ``scripts/``/``tools/``
  carries the identical header AND stays byte-identical to its
  ``templates/`` source (the parity check plan-review R3 flagged as
  missing).
* P1: the notice installs to a scratch target, is recorded in the lockfile
  ``files[]``, and appears in ``--manifest``.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_notice_install.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import install_manifest, main  # noqa: E402
from bootstrap._scaffold.lockfile import read_lockfile  # noqa: E402

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
    assert len(sources) == 56, (
        f"expected 56 templates/**/*.py manifest sources, found "
        f"{len(sources)} -- if this moved intentionally, update this test. "
        f"Moved 44 -> 45 by portable-security-sweeps Chunk A, which registers "
        f"templates/modules/team-gated/run_portable_security_sweeps.py; "
        f"moved 45 -> 46 by security-verification-activation Chunk A, which "
        f"registers templates/modules/default-on/run_security_verification.py; "
        f"moved 46 -> 56 by api-web-security-modules, which registers two "
        f"facades plus ONE four-member _security_net/ engine tree under TWO "
        f"destination trees (_api_access_security/ and _web_hosting_security/). "
        f"NOTE: this returns a LIST, so a source installed to two destinations "
        f"counts TWICE -- 6 distinct new files produce 10 new entries here. "
        f"Its sibling pin in bootstrap/tests/test_security_lint.py "
        f"(test_templates_py_count_is_pinned) counts DISTINCT files on disk and "
        f"therefore no longer agrees with this one: 52 there, 56 here. The two "
        f"still move in the same commit; they no longer move to the same number"
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


@pytest.mark.parametrize(
    ("destination", "source"),
    [
        (
            "scripts/content_scan.py",
            "templates/modules/team-gated/content_scan.py",
        ),
        (
            "scripts/content_scan_runner.py",
            "templates/modules/team-gated/content_scan_runner.py",
        ),
    ],
    ids=("scanner", "runner"),
)
def test_content_scan_twin_is_present_and_byte_identical(
    destination: str,
    source: str,
):
    """Pin required twins independently of the presence-derived sweep."""
    pair = (destination, source)
    assert pair in _self_hosted_twins(), f"required self-hosted twin missing: {pair}"
    assert (CAIRN_ROOT / destination).read_bytes() == (CAIRN_ROOT / source).read_bytes()


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


# --- P1: the NOTICE.md install path ------------------------------------------


def test_notice_is_a_core_mapping():
    """NOTICE.md installs unconditionally, like AGENTS.md -- no module
    selection should be able to skip it."""
    rows = install_manifest(modules=None)
    notice_rows = [row for row in rows if row[1] == "NOTICE.md"]
    assert notice_rows == [("core/NOTICE.md", "NOTICE.md", False)]


def test_notice_appears_in_manifest_data_row_count():
    rows = install_manifest(modules=None)
    assert len(rows) == 114, (
        f"expected 114 manifest rows (94 + NOTICE.md + portable-security-"
        f"sweeps' three + security-verification's two + api-web-security-"
        f"modules' fourteen), found {len(rows)} "
        f"-- if this moved intentionally, update this test. Moved 95 -> 98 "
        f"by portable-security-sweeps Chunk A: the module registers its "
        f"doctrine, its runner and its policy as one group, and the install "
        f"contract grew by exactly three additive rows. Moved 98 -> 100 by "
        f"security-verification-activation Chunk A: the module registers "
        f"its doctrine + its verbatim dispatcher as one group, two "
        f"additive rows."
    )


@pytest.fixture
def _scratch_install(tmp_path: Path) -> Path:
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: NoticeTest\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    rc = main([
        "--config", str(cfg), "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])
    assert rc == 0
    return tmp_path


def test_notice_installs_to_a_scratch_target(_scratch_install: Path):
    installed = _scratch_install / "NOTICE.md"
    assert installed.is_file()
    assert installed.read_text(encoding="utf-8") == (
        (CAIRN_ROOT / "templates" / "core" / "NOTICE.md").read_text(encoding="utf-8")
    )


def test_notice_is_recorded_in_the_lockfile(_scratch_install: Path):
    lock = read_lockfile(_scratch_install)
    assert lock is not None
    notice_recs = [rec for rec in lock["files"] if rec["dst"] == "NOTICE.md"]
    assert len(notice_recs) == 1, "expected exactly one NOTICE.md lockfile record"
    assert notice_recs[0]["src"] == "core/NOTICE.md"
    assert notice_recs[0]["hash"].startswith("sha256:")
