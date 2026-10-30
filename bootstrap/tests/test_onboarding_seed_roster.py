"""Tests for the onboarding seeds gated by the resolved roster.

* A rendered `dev/PLANNING.md` onboarding-tasks seed never references a
  module-specific surface -- tool *or* doc -- the resolved roster did not
  install (the broadened drift guard).
* The two `agent_team` overrides gate *differently* (`concurrent-single-type`
  keeps `coordination-tiers` content, drops only `dual-review`/tour content;
  `single` drops both) -- asserted as two distinct sets, not one flat list
  so the test cannot pass by over-stripping.
* The live (non-dry-run) install writes a clean lockfile for both override
  scenarios -- the regression below and this plan's Chunk B
  fixes (`write_install_lockfile`'s onboarding-overlay precompute must use
  the same roster-gated rendering `install_onboarding` does, or the
  lockfile's expected-clean-install `would` diverges from the actual
  stripped install and the fail-closed divergence guard refuses to write).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_onboarding_seed_roster.py
"""
from __future__ import annotations

import sys
import subprocess
import hashlib
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402
from bootstrap._scaffold.config import _MODULE_DISCOVERY, _MODULE_MAPPINGS  # noqa: E402
from bootstrap._scaffold.lockfile import read_lockfile  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def _scaffold(
    target: Path, *, preset: str, agent_team: str | None = None,
    complexity: str | None = None, remove_model_selection: bool = False,
) -> int:
    cfg = target / "profile.yml"
    lines = [
        "project_name: OnboardingRosterTest",
        "test_command: pytest",
        f"preset: {preset}",
    ]
    if agent_team is not None:
        lines.append(f"agent_team: {agent_team}")
    if complexity is not None:
        lines.append(f"complexity: {complexity}")
    if remove_model_selection:
        lines.extend(("modules_remove:", "  - model-selection"))
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


def _seed_slot(target: Path) -> str:
    text = (target / "dev" / "PLANNING.md").read_text(encoding="utf-8")
    slot = text.index("<!-- cairn:slot onboarding-tasks -->")
    start = text.find("<!-- preset:", slot)
    if start < 0:
        start = slot
    end = text.index("<!-- cairn:end onboarding-tasks -->")
    return text[start:end]


def test_selected_modules_have_usable_tasks(tmp_path: Path) -> None:
    """Exact selection controls task and inventory rows, including empty."""
    selected = list(_MODULE_MAPPINGS)
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: ModuleDiscoveryTest\ntest_command: pytest\n"
        "python_package: src\nmodules:\n"
        + "".join(f"  - {name}\n" for name in selected), encoding="utf-8")
    assert main(["--config", str(cfg), "--target", str(tmp_path),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    slot = _seed_slot(tmp_path)
    inventory = (tmp_path / "dev/modules/README.md").read_text(encoding="utf-8")
    for name, (_purpose, entry, action, result) in _MODULE_DISCOVERY.items():
        assert f"module-task id={name}" in slot
        assert f"{name}**" in slot
        assert f"`{entry}`" in slot
        assert action in slot and result in slot
        assert f"module id={name}" in inventory
    lock = read_lockfile(tmp_path)
    assert lock is not None
    assert (tmp_path / "dev/PLANNING.md").read_text(encoding="utf-8")
    inventory_record = next(
        record for record in lock["files"]
        if record["dst"] == "dev/modules/README.md"
    )
    assert inventory_record["hash"] == "sha256:" + hashlib.sha256(
        (tmp_path / "dev/modules/README.md").read_bytes()
    ).hexdigest()
    cached_baseline = tmp_path / inventory_record["base_cache"]
    assert inventory_record["base_hash"] == "sha256:" + hashlib.sha256(
        cached_baseline.read_bytes()
    ).hexdigest()


def test_empty_selection_has_no_module_tasks(tmp_path: Path) -> None:
    cfg = tmp_path / "profile.yml"
    cfg.write_text("project_name: EmptyRoster\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    assert main(["--config", str(cfg), "--target", str(tmp_path),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    assert "module-task id=" not in _seed_slot(tmp_path)
    assert "module id=" not in (tmp_path / "dev/modules/README.md").read_text()


def test_unselected_modules_have_no_tasks_or_inventory_rows(tmp_path: Path) -> None:
    """The explicit roster, rather than the available catalog, drives output."""
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: NarrowRoster\ntest_command: pytest\nmodules:\n"
        "  - reflections\n", encoding="utf-8")
    assert main(["--config", str(cfg), "--target", str(tmp_path),
                 "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    slot = _seed_slot(tmp_path)
    inventory = (tmp_path / "dev/modules/README.md").read_text(encoding="utf-8")
    assert "module-task id=reflections" in slot
    assert "module id=reflections" in inventory
    assert "module-task id=dual-review" not in slot
    assert "module id=dual-review" not in inventory


def test_reinstall_preserves_completion_and_refuses_loss(tmp_path: Path) -> None:
    """Repeated install keeps completed work and refuses its removal."""
    cfg = tmp_path / "profile.yml"

    def install(modules: list[str]) -> int:
        cfg.write_text(
            "project_name: PreserveModuleTask\ntest_command: pytest\nmodules:\n"
            + "".join(f"  - {name}\n" for name in modules),
            encoding="utf-8")
        return main(["--config", str(cfg), "--target", str(tmp_path),
                     "--cairn-root", str(CAIRN_ROOT), "--allow-dev"])

    assert install(["reflections"]) == 0
    planning = tmp_path / "dev/PLANNING.md"
    planning.write_text(planning.read_text().replace(
        "* [ ] **reflections**", "* [x] **reflections**"), encoding="utf-8")
    inventory_path = tmp_path / "dev/modules/README.md"
    inventory_path.write_text(inventory_path.read_text().replace(
        "A local reflection in dev/reflections/.",
        "A local reflection in dev/reflections/.\n  Adopter note retained."),
        encoding="utf-8")
    assert install(["reflections"]) == 0
    assert "Adopter note retained." in inventory_path.read_text(encoding="utf-8")
    before_planning = planning.read_bytes()
    before_inventory = (tmp_path / "dev/modules/README.md").read_bytes()
    before_lock = (tmp_path / "dev/.cairn/cairn-lock.yml").read_bytes()
    assert install([]) == 2
    assert planning.read_bytes() == before_planning
    assert (tmp_path / "dev/modules/README.md").read_bytes() == before_inventory
    assert (tmp_path / "dev/.cairn/cairn-lock.yml").read_bytes() == before_lock


@pytest.mark.parametrize("surface,damage", [
    ("task", "malformed-opener"),
    ("task", "missing-closer"),
    ("task", "duplicate-entry"),
    ("task", "nested-entry"),
    ("task", "crossed-entry"),
    ("task", "duplicate-region"),
    ("task", "reversed-region"),
    ("inventory", "malformed-closer"),
])
def test_empty_roster_refuses_ambiguous_markers_without_writes(
    tmp_path: Path, surface: str, damage: str, capsys: pytest.CaptureFixture[str],
) -> None:
    """Empty selection still validates marked state before changing any artifact."""
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: MarkerAmbiguity\ntest_command: pytest\nmodules:\n"
        "  - reflections\n  - dual-review\n", encoding="utf-8")
    args = ["--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    assert main(args) == 0
    planning = tmp_path / "dev/PLANNING.md"
    inventory = tmp_path / "dev/modules/README.md"
    lock = tmp_path / "dev/.cairn/cairn-lock.yml"
    path = planning if surface == "task" else inventory
    text = path.read_text(encoding="utf-8")
    if surface == "task":
        opener = "<!-- cairn:module-task id=reflections -->"
        closer = "<!-- cairn:module-task-end id=reflections -->"
        region_open = "<!-- cairn:slot onboarding-tasks -->"
        region_close = "<!-- cairn:end onboarding-tasks -->"
    else:
        opener = "<!-- cairn:module id=reflections -->"
        closer = "<!-- cairn:module-end id=reflections -->"
        region_open = "<!-- cairn:generated-modules:start -->"
        region_close = "<!-- cairn:generated-modules:end -->"
    if damage == "malformed-opener":
        text = text.replace(opener, opener.replace(" id=", "  id="), 1)
    elif damage == "malformed-closer":
        text = text.replace(closer, closer + " ", 1)
    elif damage == "missing-closer":
        text = text.replace(closer + "\n", "", 1)
    elif damage == "duplicate-entry":
        start = text.index(opener)
        end = text.index(closer, start) + len(closer)
        block = text[start:end]
        text = text[:end] + "\n" + block + text[end:]
    elif damage == "nested-entry":
        text = text.replace(opener, opener + "\n" + opener, 1)
    elif damage == "crossed-entry":
        second_opener = "<!-- cairn:module-task id=dual-review -->"
        second_closer = "<!-- cairn:module-task-end id=dual-review -->"
        first_start = text.index(opener)
        first_end = text.index(closer, first_start) + len(closer)
        second_start = text.index(second_opener, first_end)
        second_end = text.index(second_closer, second_start) + len(second_closer)
        first_body = text[first_start + len(opener):
                           text.index(closer, first_start)].strip("\n")
        second_body = text[second_start + len(second_opener):
                            text.index(second_closer, second_start)].strip("\n")
        crossed = "\n".join((opener, first_body, second_opener, second_body,
                               closer, second_closer))
        text = text[:first_start] + crossed + text[second_end:]
    elif damage == "duplicate-region":
        text = text.replace(region_close, region_close + "\n" + region_close, 1)
    elif damage == "reversed-region":
        text = text.replace(region_open, "__CAIRN_REGION_OPEN__", 1)
        text = text.replace(region_close, region_open, 1)
        text = text.replace("__CAIRN_REGION_OPEN__", region_close, 1)
    path.write_text(text, encoding="utf-8")
    before = tuple(p.read_bytes() for p in (planning, inventory, lock))

    cfg.write_text("project_name: MarkerAmbiguity\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    assert main(args) == 2
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "manually" in output or "malformed" in output
    assert tuple(p.read_bytes() for p in (planning, inventory, lock)) == before


def test_marker_mentions_outside_column_zero_entries_survive_empty_roster(
    tmp_path: Path,
) -> None:
    """Inline, indented, and blockquoted mentions remain ordinary prose."""
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: MarkerMentions\ntest_command: pytest\nmodules:\n"
        "  - reflections\n", encoding="utf-8")
    args = ["--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    assert main(args) == 0
    planning = tmp_path / "dev/PLANNING.md"
    inventory = tmp_path / "dev/modules/README.md"
    mentions = (
        "Inline mention <!-- cairn:module-task id=example -->\n"
        "  <!-- cairn:module-task id=indented -->\n"
        "> <!-- cairn:module-task id=quoted -->\n"
    )
    text = planning.read_text(encoding="utf-8")
    text = text.replace("<!-- cairn:end onboarding-tasks -->",
                        mentions + "<!-- cairn:end onboarding-tasks -->")
    planning.write_text(text, encoding="utf-8")
    inventory_mentions = (
        "Inline <!-- cairn:module id=example -->\n"
        "  <!-- cairn:module id=indented -->\n"
        "> <!-- cairn:module id=quoted -->\n"
    )
    text = inventory.read_text(encoding="utf-8")
    text = text.replace("<!-- cairn:generated-modules:end -->",
                        inventory_mentions + "<!-- cairn:generated-modules:end -->")
    inventory.write_text(text, encoding="utf-8")
    cfg.write_text("project_name: MarkerMentions\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    assert main(args) == 0
    assert mentions in planning.read_text(encoding="utf-8")
    assert inventory_mentions in inventory.read_text(encoding="utf-8")
    assert "module-task id=reflections" not in planning.read_text(encoding="utf-8")
    assert "module id=reflections" not in inventory.read_text(encoding="utf-8")


def test_reinstall_preserves_work_beside_empty_placeholder(tmp_path: Path) -> None:
    """A populated placeholder slot retains unrelated completed work."""
    cfg = tmp_path / "profile.yml"
    cfg.write_text("project_name: PreserveWork\ntest_command: pytest\nmodules: []\n",
                   encoding="utf-8")
    args = ["--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    assert main(args) == 0
    planning = tmp_path / "dev/PLANNING.md"
    marker = "<!-- cairn:end onboarding-tasks -->"
    task = "* [x] Preserve my completed research task\n"
    planning.write_text(planning.read_text(encoding="utf-8").replace(
        marker, task + marker), encoding="utf-8")
    paths = (planning, tmp_path / "dev/modules/README.md",
             tmp_path / "dev/.cairn/cairn-lock.yml")
    before = tuple(path.read_bytes() for path in paths)
    cfg.write_text("project_name: PreserveWork\ntest_command: pytest\n"
                   "modules:\n  - dual-review\n", encoding="utf-8")
    assert main(args) == 2
    assert tuple(path.read_bytes() for path in paths) == before


class TestModelMappingWaitingSeed:
    @pytest.mark.parametrize("preset", ("collaborative-team", "high-rigor-legacy"))
    def test_seed_renders_and_board_lists_it(self, tmp_path: Path, preset: str) -> None:
        assert _scaffold(tmp_path, preset=preset) == 0
        slot = _seed_slot(tmp_path)
        assert "id: fill-model-selection-mapping" in slot
        assert "**Waiting on Maintainer**: fill the model mapping" in slot
        normalized = " ".join(slot.split())
        assert "add rows for additional families assigned to a tier" in normalized
        assert "This is an assignment, not a benchmark claim" in normalized
        assert read_lockfile(tmp_path) is not None
        board = subprocess.run(
            [sys.executable, str(CAIRN_ROOT / "tools/board.py"),
             "--maintainer", "--root", str(tmp_path)],
            capture_output=True, text=True, check=False,
        )
        assert board.returncode == 0, board.stderr
        assert "fill the model mapping" in board.stdout

    @pytest.mark.parametrize("preset", ("collaborative-team", "high-rigor-legacy"))
    def test_simple_profile_strips_seed(self, tmp_path: Path, preset: str) -> None:
        assert _scaffold(tmp_path, preset=preset, complexity="simple") == 0
        assert "fill-model-selection-mapping" not in _seed_slot(tmp_path)

    def test_solo_preset_has_no_seed(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, preset="solo-greenfield") == 0
        assert "fill-model-selection-mapping" not in _seed_slot(tmp_path)

    def test_explicit_module_removal_keeps_guarded_reminder(self, tmp_path: Path) -> None:
        assert _scaffold(
            tmp_path, preset="collaborative-team", remove_model_selection=True
        ) == 0
        assert "fill-model-selection-mapping" in _seed_slot(tmp_path)
        assert not (tmp_path / "dev/.cairn/model-selection-mapping.yml").exists()


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
    # under-stripping.
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
        "fill-team-roster-day-one",
    ):
        assert f"id: {seed_id}" in slot, f"expected seed {seed_id} at canonical axes"
    assert "module-task id=dual-review" not in slot
    assert "module-task id=coordination-tiers" not in slot


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


# --- Regression: the live install must write a clean lockfile -----------

def test_live_install_writes_a_clean_lockfile_under_agent_team_single(
    tmp_path: Path,
) -> None:
    """write_install_lockfile's
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
