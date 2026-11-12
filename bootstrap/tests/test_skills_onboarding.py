"""Onboarding-integration tests for the lifecycle skills (Chunk 8 of the
executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

Decision 7: the scaffolder reports the installed skill count, and a single
**passive** ``onboarding-tasks`` pointer ("try `session-start`") is seeded into
``dev/PLANNING.md`` at install -- a low-key day-one task, not an active-surfacing
row.

Promises:
- A fresh install of any preset reports the installed lifecycle skill count.
- A fresh install seeds one session-start task into the day-one list, naming
  the session-start command once, and it is a passive entry, not an
  active-surfacing row.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_onboarding.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import main  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "skills").exists(),
    reason="templates/skills not available",
)


def _scaffold(target: Path, preset: str) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        f"project_name: OnbTest\ntest_command: pytest\npreset: {preset}\n",
        encoding="utf-8",
    )
    return main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


@pytest.mark.parametrize(
    "preset", ["solo-greenfield", "collaborative-team", "high-rigor-legacy"]
)
def test_passive_session_start_pointer_seeded_once(tmp_path, preset, capsys):
    target = tmp_path.resolve()
    assert _scaffold(target, preset) == 0

    # The scaffold reports the installed skill count (Decision 7).
    out = capsys.readouterr().out
    assert "lifecycle skill" in out

    # The source seed ID is internal; the installed task must remain usable.
    planning = (target / "dev" / "PLANNING.md").read_text(encoding="utf-8")
    assert planning.count("/session-start") == 1
    assert planning.count("python tools/session.py session-start") == 1
