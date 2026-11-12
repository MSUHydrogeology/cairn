# SPDX-License-Identifier: MIT
"""Keep the small-fix rule and its capture pointer on the real install path.

Promises:
- A real install writes AGENTS.md as shipped, with only the project name filled in.
- A real install of the issue-capture module writes it byte for byte as shipped.
"""
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]


def test_small_fix_rule_and_capture_pointer_reach_install(tmp_path: Path) -> None:
    """The real install preserves the corresponding source guidance."""
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
    source_agents = (ROOT / "templates/core/AGENTS.md").read_bytes()
    installed_agents = (target / "AGENTS.md").read_bytes()
    rendered_agents = source_agents.replace(
        b"{{project_name}}", b"Stewardship-Test")
    assert installed_agents == rendered_agents
    assert (target / "dev/modules/issue-capture.md").read_bytes() == (
        ROOT / "templates/modules/team-gated/issue-capture.md").read_bytes()
