"""Tests for the first-session-survivability plan's F3 (gate onboarding
seeds by the resolved roster).

* A rendered `dev/PLANNING.md` onboarding-tasks seed never references a
  module-specific surface -- tool *or* doc -- the resolved roster did not
  install (the broadened drift guard, plan-review R6).
* The two `agent_team` overrides gate *differently* (`concurrent-single-type`
  keeps `coordination-tiers` content, drops only `dual-review`/tour content;
  `single` drops both) -- asserted as two distinct sets, not one flat list
  (plan-review PR2), so the test cannot pass by over-stripping.
* The live (non-dry-run) install writes a clean lockfile for both override
  scenarios -- the regression plan-review PR1 found and this plan's Chunk B
  fixes (`write_install_lockfile`'s onboarding-overlay precompute must use
  the same roster-gated rendering `install_onboarding` does, or the
  lockfile's expected-clean-install `would` diverges from the actual
  stripped install and the fail-closed divergence guard refuses to write).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_onboarding_seed_roster.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402
from bootstrap._scaffold.lockfile import read_lockfile  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def _scaffold(target: Path, *, preset: str, agent_team: str | None = None) -> int:
    cfg = target / "profile.yml"
    lines = [
        "project_name: OnboardingRosterTest",
        "test_command: pytest",
        f"preset: {preset}",
    ]
    if agent_team is not None:
        lines.append(f"agent_team: {agent_team}")
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


def _seed_slot(target: Path) -> str:
    text = (target / "dev" / "PLANNING.md").read_text(encoding="utf-8")
    start = text.index("<!-- preset:")
    end = text.index("<!-- cairn:end onboarding-tasks -->")
    return text[start:end]


# --- (a) agent_team: single -- unstaffs both coordination-tiers + dual-review

def test_agent_team_single_drops_both_module_surfaces(tmp_path: Path) -> None:
    rc = _scaffold(tmp_path, preset="collaborative-team", agent_team="single")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    for surface in (
        "tools/intent.py",
        "doctrine/coordination.md",
        "dev/modules/dual-review.md",
        "agent-team-onboarding.md",
    ):
        assert surface not in slot, f"{surface} unexpectedly present under agent_team: single"


# --- (b) agent_team: concurrent-single-type -- unstaffs ONLY dual-review

def test_agent_team_concurrent_single_type_keeps_coordination_drops_dual_review(
    tmp_path: Path,
) -> None:
    rc = _scaffold(
        tmp_path, preset="collaborative-team", agent_team="concurrent-single-type",
    )
    assert rc == 0
    slot = _seed_slot(tmp_path)
    # Must-drop: dual-review is concurrent-multi-type only.
    assert "dev/modules/dual-review.md" not in slot
    assert "agent-team-onboarding.md" not in slot
    # Must-keep: coordination-tiers staffs both concurrent-* values -- an
    # over-eager strip that also dropped these would be just as wrong as
    # under-stripping (PR2's point).
    assert "tools/intent.py" in slot
    assert "doctrine/coordination.md" in slot


# --- (c) the unconditional case -- proves the gate is a real filter, not a
# silent no-op that would make (a)/(b) vacuously pass.

def test_unconditional_collaborative_team_renders_every_seed(tmp_path: Path) -> None:
    rc = _scaffold(tmp_path, preset="collaborative-team")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    for seed_id in (
        "read-coordination-doctrine",
        "install-work-intent-hooks",
        "read-dual-review-module",
        "agent-team-onboarding",
        "sign-collab-agreement-day-one",
    ):
        assert f"id: {seed_id}" in slot, f"expected seed {seed_id} at canonical axes"


# --- high-rigor-legacy: only one coordination seed, one tour seed --------

def test_high_rigor_legacy_agent_team_single_drops_its_two_gated_seeds(
    tmp_path: Path,
) -> None:
    rc = _scaffold(tmp_path, preset="high-rigor-legacy", agent_team="single")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    assert "tools/intent.py" not in slot
    assert "agent-team-onboarding.md" not in slot
    # Unconditional seeds must survive.
    assert "id: confirm-maintainer-authority" in slot
    assert "id: read-security-review-module" in slot


def test_solo_greenfield_is_a_no_op_it_carries_no_gated_seed(tmp_path: Path) -> None:
    """solo-greenfield carries none of the gated seed IDs -- gating must be
    a no-op there regardless of the agent_team override (edge case)."""
    rc = _scaffold(tmp_path, preset="solo-greenfield", agent_team="single")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    assert "id: try-session-start-skill" in slot


# --- PR1 regression: the live install must write a clean lockfile --------

def test_live_install_writes_a_clean_lockfile_under_agent_team_single(
    tmp_path: Path,
) -> None:
    """The regression plan-review PR1 found: write_install_lockfile's
    onboarding-overlay precompute must strip by the SAME axes
    install_onboarding used, or this diverges and the lockfile write
    refuses closed. A --dry-run smoke check cannot catch this (it exits
    before write_install_lockfile is ever reached)."""
    rc = _scaffold(tmp_path, preset="collaborative-team", agent_team="single")
    assert rc == 0
    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    assert lock_path.is_file(), (
        "cairn-lock.yml was not written -- the onboarding-overlay strip in "
        "write_install_lockfile has diverged from install_onboarding's"
    )
    lock = read_lockfile(tmp_path)
    assert lock is not None
    assert lock.get("files"), "lockfile has no files[] -- looks malformed"


def test_live_install_writes_a_clean_lockfile_under_concurrent_single_type(
    tmp_path: Path,
) -> None:
    rc = _scaffold(
        tmp_path, preset="collaborative-team", agent_team="concurrent-single-type",
    )
    assert rc == 0
    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    assert lock_path.is_file()
    assert read_lockfile(tmp_path) is not None
