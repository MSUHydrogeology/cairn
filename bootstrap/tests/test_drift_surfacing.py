"""
The #54 adoption->canonical drift surfacing (cairn-loop-fidelity-verification).

``scaffold._behind_by_n`` turns the stage-metadata refs -- ``lock_commit``
(the adopter's installed Cairn ref) vs ``new_commit`` (canonical target) --
into a one-line surfacing message for ``upgrade --plan``. Informational, never
blocks.

Promises:
- ``upgrade --plan`` reports how many commits an installed Cairn version trails the canonical one.
- ``upgrade --plan`` reports the drift as current when the installed and canonical versions match.
- ``upgrade --plan`` says the drift is unavailable, rather than failing, when a version is unknown or missing.
- ``upgrade --plan`` says the drift is unavailable, rather than failing, when the Cairn source is not a git repository.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

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


@pytest.fixture
def git_repo(tmp_path: Path):
    """A throwaway git repo with three commits; returns (repo_path, [shas])."""
    repo = tmp_path / "cairn"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    shas = []
    for n in range(3):
        (repo / "f.txt").write_text(f"v{n}\n")
        _git(repo, "add", "f.txt")
        _git(repo, "commit", "-q", "-m", f"c{n}")
        shas.append(_git(repo, "rev-parse", "--short", "HEAD"))
    return repo, shas


class TestBehindByN:
    # ---- graceful degradation -------------------------------------
    @pytest.mark.parametrize("lock,new", [
        ("unknown", "abc1234"),
        ("abc1234", "unknown"),
        (None, "abc1234"),
        ("abc1234", None),
    ])
    def test_unknown_or_missing_ref_is_unavailable(self, tmp_path, lock, new):
        msg = scaffold._behind_by_n(tmp_path, lock, new)
        assert "unavailable" in msg and "git metadata missing" in msg

    def test_non_git_source_does_not_crash(self, tmp_path):
        """Real-looking shas but the cairn_root is not a git repo."""
        msg = scaffold._behind_by_n(tmp_path, "aaaaaaa", "bbbbbbb")
        assert "unavailable" in msg  # git error / not comparable, never raises

    # ---- the adopter-behind fixture surfaces the message ----------
    def test_behind_by_n_reports_count(self, git_repo):
        repo, shas = git_repo
        first, _, head = shas  # behind head by 2
        msg = scaffold._behind_by_n(repo, first, head)
        assert "behind canonical by 2 commit(s)" in msg, msg

    def test_current_when_equal(self, git_repo):
        repo, shas = git_repo
        msg = scaffold._behind_by_n(repo, shas[-1], shas[-1])
        assert "current with canonical" in msg
