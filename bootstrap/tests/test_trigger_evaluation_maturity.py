"""No onboarding trigger classifies a tree by adoption level.

Cairn does not publish adoption levels: an adopter reads the doctrine or
installs it with a profile, and the profile sizes the install.  So no
trigger may fire on a guess about which level a tree is at.  The four
level triggers this replaced keyed on states that carry no such meaning --
``dev/.cairn/cairn-lock.yml`` is written by every install, and archive counts
measure activity, not a level -- and one of them told every new adopter to
"graduate" at their first goodnight.

Each fixture below is a state on which one of those triggers would fire, so
restoring any one of them turns this file red:

* a fresh ``solo-greenfield`` install (lockfile, nothing archived);
* a lockfile with 5 archived proposals and 3 archived plans;
* no lockfile, at 5 and 3;
* a lockfile at 15 and 10.

The counts are literals, not imported constants, because the thresholds
they once matched no longer exist.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_trigger_evaluation_maturity.py
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
HELPER_SRC = (
    CAIRN_ROOT
    / "templates"
    / "modules"
    / "default-on"
    / "onboarding_activate.py"
)
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
SOLO_GREENFIELD = CAIRN_ROOT / "bootstrap" / "profiles" / "solo-greenfield.yml"

pytestmark = pytest.mark.skipif(
    not HELPER_SRC.exists(), reason="onboarding_activate.py source missing",
)


def _load_helper() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "_onboarding_activate_under_test_no_levels", HELPER_SRC,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_onboarding_activate_under_test_no_levels"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


def _git(*args: str, cwd: Path) -> None:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
    }
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                   capture_output=True)


def _fresh_install(target: Path) -> Path:
    """Install the smallest shipped profile, exactly as an adopter would."""
    target.mkdir(parents=True, exist_ok=True)
    _git("init", "-q", cwd=target)
    result = subprocess.run(
        [sys.executable, str(SCAFFOLD), "--config", str(SOLO_GREENFIELD),
         "--target", str(target), "--allow-dev"],
        cwd=CAIRN_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (target / "dev" / ".cairn" / "cairn-lock.yml").is_file(), (
        "the fixture must carry the lockfile every install writes"
    )
    return target


def _tree(target: Path, *, lockfile: bool, proposals: int, plans: int) -> Path:
    for family, count in (("proposals", proposals), ("plans", plans)):
        archive = target / "dev" / family / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            (archive / f"2026-05-{i:02d}-author-slug.md").write_text("# x\n")
    if lockfile:
        (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text("schema: 1\n")
    return target


def _level_ids(fired: set[str]) -> set[str]:
    return {trigger for trigger in fired if trigger.startswith("level-")}


class TestNoTriggerClassifiesAnAdoptionLevel:
    def test_fresh_install(self, helper: ModuleType, tmp_path: Path) -> None:
        tree = _fresh_install(tmp_path / "repo")
        assert _level_ids(helper.evaluate_triggers(tree)) == set()

    @pytest.mark.parametrize(
        ("lockfile", "proposals", "plans"),
        [(True, 5, 3), (False, 5, 3), (True, 15, 10)],
        ids=["lockfile-5-3", "no-lockfile-5-3", "lockfile-15-10"],
    )
    def test_activity_states(
        self, helper: ModuleType, tmp_path: Path,
        lockfile: bool, proposals: int, plans: int,
    ) -> None:
        tree = _tree(tmp_path, lockfile=lockfile, proposals=proposals,
                     plans=plans)
        assert _level_ids(helper.evaluate_triggers(tree)) == set()
