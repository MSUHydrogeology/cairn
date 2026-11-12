"""
The #54 adoption->canonical drift surfacing (cairn-loop-fidelity-verification).

``upgrade --plan`` compares the Cairn commit the adopter's lockfile records
(the installed ref) with the canonical source's commit and prints a one-line
surfacing message. Informational, never blocks.

Promises:
- ``upgrade --plan`` reports how many commits an installed Cairn version trails the canonical one.
- ``upgrade --plan`` reports the drift as current when the installed and canonical versions match.
- ``upgrade --plan`` says the drift is unavailable, rather than failing, when a version is unknown or missing.
- ``upgrade --plan`` says the drift is unavailable, rather than failing, when the Cairn source is not a git repository.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import scaffold  # noqa: E402


def _git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent


def _install(target: Path, cairn_root: Path) -> None:
    target.mkdir(parents=True)
    profile = target / "profile.yml"
    profile.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    assert scaffold.main(["--config", str(profile), "--target", str(target),
                          "--cairn-root", str(cairn_root), "--allow-dev"]) == 0


def _set_installed_version(target: Path, commit: str) -> None:
    """Rewrite the Cairn commit the lockfile says is installed."""
    lock = target / "dev" / ".cairn" / "cairn-lock.yml"
    text = lock.read_text(encoding="utf-8")
    edited = re.sub(r'("cairn_commit": ")[^"]*(")',
                    lambda m: m.group(1) + commit + m.group(2), text)
    assert edited != text
    lock.write_text(edited, encoding="utf-8")


def _cairn_without_git(tmp_path: Path) -> Path:
    """A copy of what an install reads from the Cairn source, with no git history."""
    root = tmp_path / "cairn-without-git"
    shutil.copytree(CAIRN_ROOT / "templates", root / "templates")
    (root / "bootstrap" / "_scaffold").mkdir(parents=True)
    for name in ("config.py", "install.py"):
        shutil.copy2(CAIRN_ROOT / "bootstrap" / "_scaffold" / name,
                     root / "bootstrap" / "_scaffold" / name)
    if (CAIRN_ROOT / "CITATION.cff").exists():
        shutil.copy2(CAIRN_ROOT / "CITATION.cff", root / "CITATION.cff")
    return root


@pytest.mark.parametrize("case", [
    "behind", "current", "version-unknown", "version-git-does-not-know", "source-not-a-git-repo",
])
def test_upgrade_plan_reports_the_drift_from_canonical_and_never_fails(
    tmp_path, capsys, case
):
    """The plan says how many commits the installed version trails the source, that
    it is current, or that the comparison is unavailable (an unknown version, one
    git cannot resolve, a source with no git history); it exits 0 each time."""
    target = tmp_path / "project"
    if case == "source-not-a-git-repo":
        source = _cairn_without_git(tmp_path)
        expected = "unavailable"
    else:
        source = CAIRN_ROOT
        try:
            head = _git(source, "rev-parse", "--short", "HEAD")
            old = _git(source, "rev-parse", "--short", "HEAD~2")
        except (OSError, subprocess.CalledProcessError):
            pytest.skip("the Cairn source has no git history here")
        expected = {"behind": f"behind canonical by {_git(source, 'rev-list', '--count', old + '..' + head)} ",
                    "current": "current with canonical",
                    "version-unknown": "unavailable",
                    "version-git-does-not-know": "unavailable"}[case]
    _install(target, source)
    if case == "behind":
        _set_installed_version(target, old)
    elif case == "version-unknown":
        _set_installed_version(target, "unknown")
    elif case == "version-git-does-not-know":
        _set_installed_version(target, "0" * 40)
    capsys.readouterr()
    assert scaffold.main(["upgrade", "--target", str(target), "--plan",
                          "--cairn-root", str(source)]) == 0
    out = capsys.readouterr()
    drift = [line for line in (out.out + out.err).splitlines() if "adoption drift" in line]
    assert len(drift) == 1 and expected in drift[0], drift
