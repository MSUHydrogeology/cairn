# SPDX-License-Identifier: MIT
"""Keep the small-fix rule and its capture pointer on the real install path."""
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def test_small_fix_rule_and_capture_pointer_reach_install(tmp_path: Path) -> None:
    """Installed guidance must carry the promise and cost bar, not capture-first advice."""
    config = tmp_path / "profile.yml"
    config.write_text(
        "project_name: Stewardship-Test\ntest_command: pytest\n"
        "modules:\n  - issue-capture\n",
        encoding="utf-8",
    )
    target = tmp_path / "project"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, str(ROOT / "bootstrap/scaffold.py"),
         "--config", str(config), "--target", str(target),
         "--cairn-root", str(ROOT), "--allow-dev"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    agents = " ".join((target / "AGENTS.md").read_text(encoding="utf-8").split())
    capture = " ".join(
        (target / "dev/modules/issue-capture.md").read_text(encoding="utf-8").split()
    )
    lifecycle = " ".join(
        (ROOT / "doctrine/lifecycle.md").read_text(encoding="utf-8").split()
    )
    assert "needs a Maintainer decision" in lifecycle
    assert "belongs to work already in motion" in lifecycle
    assert "over the cost bar" in lifecycle
    assert "A defect breaks a promise already in the file" in agents
    assert "Count person-steps, not machine time" in agents
    assert "Fixing an easy problem you meet" in capture
    assert "`AGENTS.md`" in capture
    assert "defer-OK" not in (ROOT / "doctrine/plans.md").read_text(encoding="utf-8")
