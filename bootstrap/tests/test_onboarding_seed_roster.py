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
    end = text.index("<!-- cairn:end onboarding-tasks -->")
    return text[slot:end]


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
    assert set(_MODULE_DISCOVERY) == set(_MODULE_MAPPINGS)
    for name, (_purpose, entry, action, result) in _MODULE_DISCOVERY.items():
        assert f"* [ ] **{name}**" in slot
        assert f"{name}**" in slot
        assert f"`{entry}`" in slot
        assert action in slot and result in slot
        assert f"module id={name}" in inventory
    assert "module-task" not in slot
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
    assert "**reflections**" not in _seed_slot(tmp_path)
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
    assert "**reflections**" in slot
    assert "module id=reflections" in inventory
    assert "**dual-review**" not in slot
    assert "module id=dual-review" not in inventory


def test_reinstall_never_reconciles_board_and_updates_inventory(tmp_path: Path) -> None:
    """Board completion/deletion persists while inventory follows selection."""
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
    completed = planning.read_bytes()
    assert install(["reflections"]) == 0
    assert planning.read_bytes() == completed
    text = planning.read_text(encoding="utf-8")
    start = text.index("* [x] **reflections**")
    end = text.index("\n\n", start) + 2
    planning.write_text(text[:start] + text[end:], encoding="utf-8")
    deleted = planning.read_bytes()
    assert install(["reflections"]) == 0
    assert planning.read_bytes() == deleted
    assert install([]) == 0
    assert planning.read_bytes() == deleted
    inventory = (tmp_path / "dev/modules/README.md").read_text(encoding="utf-8")
    assert "module id=reflections" not in inventory


@pytest.mark.parametrize("damage", [
    "malformed-opener", "malformed-closer", "missing-closer",
    "duplicate-entry", "nested-entry", "crossed-entry", "duplicate-region",
    "reversed-region", "missing-region-open", "missing-region-close",
])
def test_refuses_ambiguous_markers_without_writes(
    tmp_path: Path, damage: str, capsys: pytest.CaptureFixture[str],
) -> None:
    """Ambiguous inventory boundaries refuse before inventory or lock writes."""
    cfg = tmp_path / "profile.yml"
    module_lines = "  - reflections\n"
    if damage == "crossed-entry":
        module_lines += "  - dual-review\n"
    cfg.write_text(
        "project_name: MarkerAmbiguity\ntest_command: pytest\nmodules:\n"
        + module_lines, encoding="utf-8")
    args = ["--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    assert main(args) == 0
    planning = tmp_path / "dev/PLANNING.md"
    inventory = tmp_path / "dev/modules/README.md"
    lock = tmp_path / "dev/.cairn/cairn-lock.yml"
    path = inventory
    text = path.read_text(encoding="utf-8")
    entry, end_entry = "module", "module-end"
    region_open = "<!-- cairn:generated-modules:start -->"
    region_close = "<!-- cairn:generated-modules:end -->"
    opener = f"<!-- cairn:{entry} id=reflections -->"
    closer = f"<!-- cairn:{end_entry} id=reflections -->"
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
        second_opener = f"<!-- cairn:{entry} id=dual-review -->"
        second_closer = f"<!-- cairn:{end_entry} id=dual-review -->"
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
    elif damage == "missing-region-open":
        text = text.replace(region_open, "__CAIRN_REGION_OPEN__", 1)
    elif damage == "missing-region-close":
        text = text.replace(region_close, "__CAIRN_REGION_CLOSE__", 1)
    path.write_text(text, encoding="utf-8")
    before = tuple(p.read_bytes() for p in (planning, inventory, lock))

    if damage != "crossed-entry":
        cfg.write_text(
            "project_name: MarkerAmbiguity\ntest_command: pytest\nmodules: []\n",
            encoding="utf-8")
    # The crossed identity case keeps both entries selected: independent
    # closer searches can then accept the damaged pair instead of rejecting
    # it merely because removing the edited block would lose work.
    assert main(args) == 2
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "manually" in output
    if damage in {"duplicate-region", "reversed-region",
                  "missing-region-open", "missing-region-close"}:
        assert "save" in output and "reconcile" in output
    assert tuple(p.read_bytes() for p in (planning, inventory, lock)) == before


def test_board_text_stays_project_owned_while_inventory_reconciles(
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
    assert "**reflections**" in planning.read_text(encoding="utf-8")
    assert "module id=reflections" not in inventory.read_text(encoding="utf-8")


def test_reinstall_does_not_seed_over_project_owned_board_text(tmp_path: Path) -> None:
    """New selections do not mutate a board installed by an earlier run."""
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
    before_planning = planning.read_bytes()
    cfg.write_text("project_name: PreserveWork\ntest_command: pytest\n"
                   "modules:\n  - dual-review\n", encoding="utf-8")
    assert main(args) == 0
    assert planning.read_bytes() == before_planning
    assert "module id=dual-review" in (
        tmp_path / "dev/modules/README.md").read_text(encoding="utf-8")


class TestModelMappingWaitingSeed:
    @pytest.mark.parametrize("preset", ("collaborative-team", "high-rigor-legacy"))
    def test_seed_renders_and_board_lists_it(self, tmp_path: Path, preset: str) -> None:
        assert _scaffold(tmp_path, preset=preset) == 0
        slot = _seed_slot(tmp_path)
        assert "id: fill-model-selection-mapping" not in slot
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
        assert "**Waiting on Maintainer**: fill the model mapping" not in _seed_slot(tmp_path)

    def test_solo_preset_has_no_seed(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, preset="solo-greenfield") == 0
        assert "**Waiting on Maintainer**: fill the model mapping" not in _seed_slot(tmp_path)

    def test_explicit_module_removal_keeps_guarded_reminder(self, tmp_path: Path) -> None:
        assert _scaffold(
            tmp_path, preset="collaborative-team", remove_model_selection=True
        ) == 0
        assert "**Waiting on Maintainer**: fill the model mapping" in _seed_slot(tmp_path)
        assert not (tmp_path / "dev/.cairn/model-selection-mapping.yml").exists()


# --- (a) agent_team: single -- unstaffs both coordination-tiers + dual-review

def test_agent_team_single_drops_both_module_surfaces(tmp_path: Path) -> None:
    rc = _scaffold(tmp_path, preset="collaborative-team", agent_team="single")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    for surface in (
        "tools/intent.py",
        "docs/methodology/coordination.md",
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
    assert "docs/methodology/coordination.md" in slot


# --- (c) the unconditional case -- proves the gate is a real filter, not a
# silent no-op that would make (a)/(b) vacuously pass.

def test_unconditional_collaborative_team_renders_every_seed(tmp_path: Path) -> None:
    rc = _scaffold(tmp_path, preset="collaborative-team")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    for task_text in (
        "Read `docs/methodology/coordination.md`",
        "Install the work-intent git hooks",
        "Read `dev/modules/dual-review.md`",
        "Walk `dev/modules/onboarding/agent-team-onboarding.md`",
        "Convene the team + agents in your first session",
    ):
        assert task_text in slot, f"expected task text {task_text!r} at canonical axes"
    assert "**dual-review**" not in slot
    assert "**coordination-tiers**" not in slot


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
    assert "Confirm the existing project maintainer's authority" in slot
    assert "Read `dev/modules/security-review.md`" in slot


def test_solo_greenfield_is_a_no_op_it_carries_no_gated_seed(tmp_path: Path) -> None:
    """solo-greenfield carries none of the gated seed IDs -- gating must be
    a no-op there regardless of the agent_team override (edge case)."""
    rc = _scaffold(tmp_path, preset="solo-greenfield", agent_team="single")
    assert rc == 0
    slot = _seed_slot(tmp_path)
    assert "Try the `session-start` skill" in slot


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


def test_diverged_planning_board_does_not_become_clean_lock_baseline(
    tmp_path: Path,
) -> None:
    assert _scaffold(tmp_path, preset="solo-greenfield") == 0
    planning = tmp_path / "dev/PLANNING.md"
    changed = planning.read_bytes() + b"\nHuman changes after install\n"
    planning.write_bytes(changed)
    lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
    assert lock_path.is_file()
    lock_path.unlink()
    assert _scaffold(tmp_path, preset="solo-greenfield") == 0
    assert planning.read_bytes() == changed
    assert not lock_path.exists()


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
