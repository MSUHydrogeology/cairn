"""Install-path tests for the lifecycle-routine skills (Chunk 4 of the
executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

A real scaffold of a scratch adopter repo must:

* install both ``SKILL.md`` sources to ``.agents/skills/<name>/`` and the CLI to
  ``tools/session.py`` -- unconditionally, with no module selected (Decision
  5: skills install like core);
* record each canonical skill artifact in ``dev/.cairn/cairn-lock.yml`` -- the two
  ``SKILL.md`` files non-verbatim (with a ``base_cache`` + ``base_hash`` -> the
  3-way-merge upgrade path) and ``tools/session.py`` verbatim (hash-only, no
  base cache);
* write ``dev/.cairn/base/...`` cache entries for the non-verbatim skills;
* write the per-worktree Git-administration interpreter binding and retain the
  legacy ``dev/.cairn/local-env.json`` ignore entry;
* leave an installed, runnable CLI: ``session-start`` runs read-only.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_install.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import main, read_lockfile  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "skills").exists(),
    reason="templates/skills not available",
)

SKILL_START = ".agents/skills/session-start/SKILL.md"
SKILL_END = ".agents/skills/session-end/SKILL.md"
CLI = "tools/session.py"
METER = "tools/meter.py"
GIT_READ = "tools/git_read.py"


@pytest.fixture()
def scaffolded(tmp_path: Path) -> Path:
    target = tmp_path.resolve()
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: SkillsTest\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    rc = main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])
    assert rc == 0
    return target


def test_skills_install_to_canonical_paths(scaffolded: Path):
    for rel in (SKILL_START, SKILL_END, CLI, METER, GIT_READ):
        assert (scaffolded / rel).is_file(), f"missing installed artifact: {rel}"
    assert (scaffolded / METER).read_bytes() == (
        TEMPLATES_ROOT / "skills/_lib/meter.py").read_bytes()
    assert (scaffolded / GIT_READ).read_bytes() == (
        TEMPLATES_ROOT / "skills/_lib/git_read.py").read_bytes()


def test_lockfile_records_skills_with_correct_cache_policy(scaffolded: Path):
    lock = read_lockfile(scaffolded)
    assert lock is not None, "lockfile was not written on a clean install"
    by_dst = {rec["dst"]: rec for rec in lock["files"]}

    # The CLI is verbatim: hash-only, no base cache (a script is merged by the
    # hash policy, not a 3-way merge).
    cli = by_dst[CLI]
    assert cli["verbatim"] is True
    assert "hash" in cli and "base_cache" not in cli

    git_read = by_dst[GIT_READ]
    assert git_read["verbatim"] is True
    assert "hash" in git_read and "base_cache" not in git_read

    # The SKILL.md sources are substituted: base cache + base hash -> they ride
    # the same 3-way-merge upgrade path as core docs.
    for rel in (SKILL_START, SKILL_END):
        rec = by_dst[rel]
        assert rec["verbatim"] is False
        assert "base_cache" in rec and "base_hash" in rec
        assert (scaffolded / rec["base_cache"]).is_file()


def test_git_admin_binding_written_and_legacy_path_stays_ignored(scaffolded: Path):
    git_dir = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=scaffolded,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    cfg = Path(git_dir) / "cairn" / "local-env.json"
    assert cfg.is_file()
    data = json.loads(cfg.read_text(encoding="utf-8"))
    assert set(data) == {"interpreter"}
    assert Path(data["interpreter"]).is_absolute()

    gitignore = (scaffolded / ".gitignore").read_text(encoding="utf-8")
    assert "dev/.cairn/local-env.json" in gitignore
    assert "dev/.cairn/handoff.lock" in gitignore
    assert "dev/measurement/meter.json" in gitignore


def test_install_does_not_create_meter_consent_or_ledger(scaffolded: Path):
    assert not (scaffolded / ".cairn" / "meter.json").exists()
    assert not (scaffolded / ".cairn" / "meter" / "ledger.json").exists()
    assert not (scaffolded / "dev" / ".cairn" / "meter.json").exists()


def test_failed_fanout_keeps_binding_in_git_admin_and_exits_nonzero(tmp_path):
    # A containment failure during fan-out must not put machine state in
    # checkout content, and main() returns a crisp non-zero, not a traceback.
    import os
    target = tmp_path.resolve()
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: FailTest\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    outside = target.parent / (target.name + "-outside")
    outside.mkdir()
    os.symlink(outside, target / ".claude", target_is_directory=True)

    rc = main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])

    assert rc != 0  # crisp non-zero, not a traceback
    git_dir = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=target,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    env = Path(git_dir) / "cairn" / "local-env.json"
    assert env.is_file()
    assert not (target / "dev" / ".cairn" / "local-env.json").exists()


def test_installed_cli_runs_read_only(scaffolded: Path):
    # session-start needs a git repo to gather state.
    subprocess.run(["git", "init", "-q"], cwd=scaffolded, check=True)
    subprocess.run(["git", "add", "-A"], cwd=scaffolded, check=True,
                   capture_output=True)
    subprocess.run(
        ["git", "-c", "user.email=t@e.com", "-c", "user.name=T",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", "init"],
        cwd=scaffolded, check=True, capture_output=True,
    )
    proc = subprocess.run(
        [sys.executable, str(scaffolded / CLI), "session-start"],
        cwd=scaffolded, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "session-start gather complete" in proc.stdout
