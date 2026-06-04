"""Install-path tests for the lifecycle-routine skills (Chunk 4 of the
executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

A real scaffold of a scratch adopter repo must:

* install both ``SKILL.md`` sources to ``.agents/skills/<name>/`` and the CLI to
  ``tools/lifecycle.py`` -- unconditionally, with no module selected (Decision
  5: skills install like core);
* record each canonical skill artifact in ``dev/.cairn/cairn-lock.yml`` -- the two
  ``SKILL.md`` files non-verbatim (with a ``base_cache`` + ``base_hash`` -> the
  3-way-merge upgrade path) and ``tools/lifecycle.py`` verbatim (hash-only, no
  base cache) (Decision 4 / EP3);
* write ``dev/.cairn/base/...`` cache entries for the non-verbatim skills;
* write the untracked ``dev/.cairn/local-env.json`` interpreter binding and seed
  it (plus the handoff lock) into ``.gitignore`` (Decision 6 / R3);
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
CLI = "tools/lifecycle.py"


@pytest.fixture()
def scaffolded(tmp_path: Path) -> Path:
    target = tmp_path.resolve()
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
    for rel in (SKILL_START, SKILL_END, CLI):
        assert (scaffolded / rel).is_file(), f"missing installed artifact: {rel}"


def test_lockfile_records_skills_with_correct_cache_policy(scaffolded: Path):
    lock = read_lockfile(scaffolded)
    assert lock is not None, "lockfile was not written on a clean install"
    by_dst = {rec["dst"]: rec for rec in lock["files"]}

    # The CLI is verbatim: hash-only, no base cache (a script is merged by the
    # hash policy, not a 3-way merge).
    cli = by_dst[CLI]
    assert cli["verbatim"] is True
    assert "hash" in cli and "base_cache" not in cli

    # The SKILL.md sources are substituted: base cache + base hash -> they ride
    # the same 3-way-merge upgrade path as core docs.
    for rel in (SKILL_START, SKILL_END):
        rec = by_dst[rel]
        assert rec["verbatim"] is False
        assert "base_cache" in rec and "base_hash" in rec
        assert (scaffolded / rec["base_cache"]).is_file()


def test_local_env_binding_written_and_gitignored(scaffolded: Path):
    cfg = scaffolded / "dev" / ".cairn" / "local-env.json"
    assert cfg.is_file()
    data = json.loads(cfg.read_text(encoding="utf-8"))
    assert set(data) == {"interpreter"}
    assert Path(data["interpreter"]).is_absolute()

    gitignore = (scaffolded / ".gitignore").read_text(encoding="utf-8")
    assert "dev/.cairn/local-env.json" in gitignore
    assert "dev/.cairn/handoff.lock" in gitignore


def test_failed_fanout_leaves_local_env_gitignored_and_exits_nonzero(tmp_path):
    # Codex P1#2: a containment failure during fan-out (a symlinked vendor
    # parent) must not leave an UNIGNORED local-env.json carrying a local
    # absolute path -- the ignore entry is seeded before the file is written,
    # and main() returns a crisp non-zero, not a traceback.
    import os
    target = tmp_path.resolve()
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
    env = target / "dev" / ".cairn" / "local-env.json"
    assert env.is_file()
    assert "dev/.cairn/local-env.json" in (
        target / ".gitignore"
    ).read_text(encoding="utf-8")


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
