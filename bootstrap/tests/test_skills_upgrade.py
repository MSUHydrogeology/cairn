"""Upgrade round-trip for the lifecycle-routine skills (Chunk 4.5 of the
executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

Decision 4 / EP3: the canonical skill artifacts participate in the shipped
upgrade machinery exactly like a ``core/`` file --

* a substituted ``SKILL.md`` an adopter customized **rides the token-/slot-aware
  3-way merge** (an upstream advance folds in while the adopter's edit is
  preserved -- never a silent clobber);
* the verbatim CLI (``tools/lifecycle.py``) follows the **hash policy**: a local
  edit is surfaced for review, not 3-way-merged.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_upgrade.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "skills").exists(),
    reason="templates/skills not available",
)

SKILL_START = ".agents/skills/session-start/SKILL.md"
CLI = "tools/lifecycle.py"


def _install(target: Path) -> None:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    assert s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0


def test_skill_md_rides_3way_merge(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)

    # Model "old install + adopter customization, upstream since advanced":
    # base cache + ours both carry an OLD header; ours adds a local marker; the
    # live upstream template still carries the new header.
    base = target / "dev" / ".cairn" / "base" / SKILL_START
    ours = target / SKILL_START
    old = "# Session-start (good-morning)"
    base.write_text(base.read_text().replace(old, "# OLD", 1), encoding="utf-8")
    ours.write_text(
        ours.read_text().replace(old, "# OLD", 1) + "\n<!-- adopter note -->\n",
        encoding="utf-8",
    )

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
    )
    plan = next(p for p in plans if p.dst == SKILL_START)

    # Rides the merge like a core doc: advancing, and the upstream advance
    # folded in while the adopter's marker survived (no silent clobber).
    assert plan.kind in s._ADVANCING_KINDS, f"got kind {plan.kind!r}"
    assert plan.applied is not None
    assert "<!-- adopter note -->" in plan.applied   # adopter edit preserved
    assert old in plan.applied                        # upstream advance folded in


def test_verbatim_cli_local_edit_is_surfaced_not_merged(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)

    # Adopter edits the verbatim CLI.
    cli = target / CLI
    cli.write_text(
        cli.read_text() + "\n# adopter local change\n", encoding="utf-8"
    )

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
    )
    plan = next(p for p in plans if p.dst == CLI)

    # A verbatim script is not 3-way-merged: a local edit is surfaced
    # (review-only / locally-modified), never silently advanced.
    assert plan.kind not in s._ADVANCING_KINDS, f"got kind {plan.kind!r}"
    assert "modified" in plan.kind or "review" in plan.kind, plan.kind
