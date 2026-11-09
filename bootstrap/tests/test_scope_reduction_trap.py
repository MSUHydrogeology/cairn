# SPDX-License-Identifier: MIT
"""Keep both-profile installation of the shipped plan template intact."""
import subprocess
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def test_scope_reduction_plan_template_installs_from_source(tmp_path: Path) -> None:
    """Both profiles install the shipped plan template without drift."""
    profiles = ("solo-greenfield.yml", "high-rigor-legacy.yml")
    source = (CAIRN_ROOT / "templates/core/dev/plans/_template.md").read_bytes()
    for profile_name in profiles:
        target = tmp_path / profile_name.removesuffix(".yml")
        target.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(CAIRN_ROOT / "bootstrap/scaffold.py"),
                "--config", str(CAIRN_ROOT / "bootstrap/profiles" / profile_name),
                "--target", str(target),
                "--cairn-root", str(CAIRN_ROOT),
                "--non-interactive", "--allow-dev",
            ],
            cwd=CAIRN_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        installed = (target / "dev/plans/_template.md").read_bytes()
        assert installed == source, (
            f"{profile_name} installed a plan template that differs from its source"
        )
