"""Vendor fan-out tests for the lifecycle skills (Chunk 6 of the executing plan
`2026-06-01-claude-cairn-vendor-neutral-skills`).

This module pins:

* per-tier fan-out -- alias (nothing), symlink (verified relative symlink to the
  canonical ``.agents/skills/``, only for an in-use vendor dir), manual
  (documented fallback, no write);
* copy-fallback where symlinks are unavailable -- gitignored generated copies +
  a divergence guard that **warns, never clobbers** an edited copy;
* containment -- a vendor row with an absolute / ``..`` / symlinked-parent
  path fails closed before any write.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_fanout.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "skills").exists(),
    reason="templates/skills not available",
)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A target with a canonical .agents/skills/ tree (as install would write)."""
    root = tmp_path.resolve()
    canon = root / ".agents" / "skills" / "session-start"
    canon.mkdir(parents=True)
    (canon / "SKILL.md").write_text("---\nname: session-start\n---\nbody\n",
                                    encoding="utf-8")
    return root


SYMLINK_ROW = {"target": "claude-code", "tier": "symlink", "path": ".claude/skills"}
ALIAS_ROW = {"target": "agents-native", "tier": "alias", "path": ".agents/skills"}
MANUAL_ROW = {"target": "cursor", "tier": "manual", "path": ".cursor/rules"}


def test_alias_and_manual_emit_nothing(repo):
    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[ALIAS_ROW, MANUAL_ROW])
    by = {name: (tier, status) for name, tier, status in res}
    assert by["agents-native"] == ("alias", "noop")
    assert by["cursor"][1] == "manual-fallback"
    assert not (repo / ".cursor").exists()


def test_symlink_emitted_only_when_vendor_dir_present(repo):
    # Vendor dir absent -> skipped (no littering a fresh repo).
    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW],
                           allow_symlinks=True)
    assert res[0][2] == "skipped-vendor-absent"
    assert not (repo / ".claude" / "skills").exists()

    # Vendor in use -> a relative symlink to the canonical dir.
    (repo / ".claude").mkdir()
    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW],
                           allow_symlinks=True)
    link = repo / ".claude" / "skills"
    assert res[0] == ("claude-code", "symlink", "linked")
    assert link.is_symlink()
    assert os.readlink(link) == os.path.join("..", ".agents", "skills")
    # Reaches the canonical SKILL.md through the link.
    assert (link / "session-start" / "SKILL.md").is_file()


def test_symlink_idempotent(repo):
    (repo / ".claude").mkdir()
    s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW], allow_symlinks=True)
    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW],
                           allow_symlinks=True)
    assert res[0][2] == "linked"  # no error on re-run


def test_copy_fallback_when_symlinks_unavailable(repo):
    (repo / ".claude").mkdir()
    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW],
                           allow_symlinks=False)
    copy = repo / ".claude" / "skills"
    assert res[0] == ("claude-code", "copy", "copied")
    assert not copy.is_symlink()
    assert (copy / "session-start" / "SKILL.md").is_file()  # generated copy
    # The copy dir is gitignored (a generated build artifact).
    assert ".claude/skills/" in (repo / ".gitignore").read_text(encoding="utf-8")


def test_copy_fallback_divergence_quarantines_and_regenerates(repo, capsys):
    # The generated copy is a vendor-read supply-chain artifact, not author-
    # owned: a diverged copy must not stay the active read-path.
    (repo / ".claude").mkdir()
    s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW], allow_symlinks=False)
    edited = repo / ".claude" / "skills" / "session-start" / "SKILL.md"
    canonical = (repo / ".agents" / "skills" / "session-start" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    edited.write_text("MALICIOUS / STALE COPY", encoding="utf-8")
    capsys.readouterr()

    res = s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[SYMLINK_ROW],
                           allow_symlinks=False)

    assert res[0][2] == "diverged-quarantined"
    # The active vendor-read path carries the safe canonical bytes again ...
    assert edited.read_text(encoding="utf-8") == canonical
    # ... and the stray bytes are preserved (not destroyed) in the quarantine.
    bak = edited.with_name("SKILL.md.diverged.bak")
    assert bak.read_text(encoding="utf-8") == "MALICIOUS / STALE COPY"
    assert "divergence" in capsys.readouterr().err


@pytest.mark.parametrize("bad_path", ["/etc/evil", "../escape", "a/../../b"])
def test_unsafe_fanout_path_fails_closed(repo, bad_path):
    row = {"target": "evil", "tier": "symlink", "path": bad_path}
    with pytest.raises(s.ScaffoldSecurityError):
        s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[row], allow_symlinks=True)


def test_symlinked_parent_fails_closed(repo, tmp_path):
    # A symlinked vendor parent dir must not be written through.
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside, repo / ".evil", target_is_directory=True)
    row = {"target": "x", "tier": "symlink", "path": ".evil/skills"}
    with pytest.raises(s.ScaffoldSecurityError):
        s.fan_out_skills(TEMPLATES_ROOT, repo, targets=[row], allow_symlinks=True)
