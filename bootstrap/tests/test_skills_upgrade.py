"""Upgrade round-trip for the lifecycle-routine skills (Chunk 4.5 of the
executing plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

The canonical skill artifacts participate in the shipped
upgrade machinery exactly like a ``core/`` file --

* a substituted ``SKILL.md`` an adopter customized **rides the token-/slot-aware
  3-way merge** (an upstream advance folds in while the adopter's edit is
  preserved -- never a silent clobber);
* the verbatim CLI (``tools/lifecycle.py``) follows the **hash policy**: a local
  edit is surfaced for review, not 3-way-merged.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_upgrade.py
"""
from __future__ import annotations

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

SKILL_START = ".agents/skills/session-start/SKILL.md"
CLI = "tools/lifecycle.py"


def _install(target: Path) -> None:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    assert s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0


def test_skill_md_rides_3way_merge(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)

    # Model "old install + adopter customization, upstream since advanced":
    # base cache + ours both carry an OLD header; ours adds a local marker; the
    # live upstream template still carries the new header.
    base = target / "dev" / ".cairn" / "base" / SKILL_START
    ours = target / SKILL_START
    old = "# Session-start (good-morning)"
    base.write_text(base.read_text().replace(old, "# OLD", 1), encoding="utf-8")
    ours.write_text(
        ours.read_text().replace(old, "# OLD", 1) + "\n<!-- adopter note -->\n",
        encoding="utf-8",
    )

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
    )
    plan = next(p for p in plans if p.dst == SKILL_START)

    # Rides the merge like a core doc: advancing, and the upstream advance
    # folded in while the adopter's marker survived (no silent clobber).
    assert plan.kind in s._ADVANCING_KINDS, f"got kind {plan.kind!r}"
    assert plan.applied is not None
    assert "<!-- adopter note -->" in plan.applied   # adopter edit preserved
    assert old in plan.applied                        # upstream advance folded in


def test_verbatim_cli_local_edit_is_surfaced_not_merged(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)

    # Adopter edits the verbatim CLI.
    cli = target / CLI
    cli.write_text(
        cli.read_text() + "\n# adopter local change\n", encoding="utf-8"
    )

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
    )
    plan = next(p for p in plans if p.dst == CLI)

    # A verbatim script is not 3-way-merged: a local edit is surfaced
    # (review-only / locally-modified), never silently advanced.
    assert plan.kind not in s._ADVANCING_KINDS, f"got kind {plan.kind!r}"
    assert "modified" in plan.kind or "review" in plan.kind, plan.kind


# ---------------------------------------------------------------------------
# Fold-back #47: a pre-skills adopter (lockfile predates the skills) acquires
# the skills on upgrade -- detected as `new-core`, brought in, fanned out, and
# RECORDED in the lockfile. Fold-back #48: a verbatim file hand-synced to
# exactly the new upstream is `up-to-date`, not a fork, and its stale lock hash
# heals on apply.
# ---------------------------------------------------------------------------

SKILL_END = ".agents/skills/session-end/SKILL.md"
LIFECYCLE = "tools/lifecycle.py"
_SKILL_DSTS = {SKILL_START, SKILL_END, LIFECYCLE}


def _make_pre_skills(target: Path) -> None:
    """Mutate a freshly-installed tree to look like a **pre-skills adopter**:
    drop the skills entries from the lockfile and delete the on-disk skill
    files + their base caches, so the lockfile no longer knows the skills exist
    (the state an adopter who bootstrapped before skills lands in)."""
    import shutil

    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] not in _SKILL_DSTS]
    (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        s._emit_lock_yaml(lock), encoding="utf-8")
    for rel in (".agents", LIFECYCLE, "dev/.cairn/base/.agents"):
        p = target / rel
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()


def test_pre_skills_compute_surfaces_skills_as_new_core(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_skills(target)

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
    )
    new_core = {p.dst: p for p in plans if p.kind == "new-core"}

    assert set(new_core) == _SKILL_DSTS, f"got {set(new_core)}"
    assert all(p.kind in s._ADVANCING_KINDS for p in new_core.values())
    # The verbatim CLI is hash-tracked; the SKILL.md files are mergeable.
    assert new_core[LIFECYCLE].verbatim is True
    assert new_core[LIFECYCLE].src == "skills/_lib/lifecycle.py"
    assert new_core[SKILL_START].verbatim is False
    assert new_core[SKILL_START].base_cache  # mergeable -> base cache seeds


def test_pre_skills_apply_records_skills_in_lockfile_and_fans_out(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_skills(target)
    # A vendor read-path present -> the symlink fan-out emits (the guard only
    # writes a vendor dir when its parent already exists).
    (target / ".claude").mkdir(exist_ok=True)

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0

    # On disk + fanned out to the claude-code read-path.
    assert (target / SKILL_START).exists()
    assert (target / LIFECYCLE).exists()
    assert (target / ".claude" / "skills").exists()  # symlink (or copy fallback)
    # Recorded in the lockfile (the whole point of #47).
    lock = s.read_lockfile(target)
    dsts = {r["dst"] for r in lock["files"]}
    assert _SKILL_DSTS <= dsts, f"missing from lock: {_SKILL_DSTS - dsts}"
    # Mergeable SKILL.md re-seeded its base cache; verbatim CLI did not.
    assert (target / "dev/.cairn/base" / SKILL_START).exists()
    cli_rec = next(r for r in lock["files"] if r["dst"] == LIFECYCLE)
    assert cli_rec["verbatim"] is True and "base_cache" not in cli_rec


def test_stage_metadata_new_entries_are_refs_only(tmp_path: Path):
    """Plan-review rec 4b: stage-metadata carries only references for new-core
    files (src / verbatim / base_cache), never file bodies."""
    import json

    target = tmp_path.resolve()
    _install(target)
    _make_pre_skills(target)
    assert s.main([
        "upgrade", "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--stage",
    ]) == 0

    meta = json.loads(
        (target / "dev/.cairn-upgrade/stage-metadata.json").read_text())
    new_entries = meta["new_entries"]
    assert _SKILL_DSTS <= set(new_entries)
    for info in new_entries.values():
        assert set(info) <= {"src", "verbatim", "base_cache"}, info


def test_skills_gitignore_seeded_idempotently_on_apply(tmp_path: Path):
    """Plan-review rec 4a: skills .gitignore seeding routes through the
    idempotent seed_gitignore -- the entry the install already seeded is not
    duplicated when --apply re-seeds it."""
    target = tmp_path.resolve()
    _install(target)            # the install seeds the skills .gitignore entries
    _make_pre_skills(target)
    pre = s._SKILLS_GITIGNORE[0]
    gi = target / ".gitignore"
    assert gi.read_text().splitlines().count(pre) == 1, "install should seed once"

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    # --apply re-seeds via the idempotent seed_gitignore -> still exactly one.
    assert gi.read_text().splitlines().count(pre) == 1


def test_verbatim_hand_synced_to_upstream_is_up_to_date():
    """#48 unit: ours == theirs is up-to-date even with a stale lock hash;
    a genuine fork (ours != theirs, hash != lock) is still flagged."""
    content = b"x = 1\n"
    assert s.classify_verbatim(content, "sha256:STALEHASH", content) == "up-to-date"
    assert s.classify_verbatim(b"forked\n", "sha256:STALEHASH", b"theirs\n") \
        == "locally-modified"


def test_verbatim_stale_hash_heals_on_apply(tmp_path: Path):
    """#48 end-to-end: a verbatim file on-disk == upstream but with a stale
    lockfile hash heals to the on-disk hash on apply (no content swap)."""
    target = tmp_path.resolve()
    _install(target)
    stale = "sha256:" + "0" * 64
    lock = s.read_lockfile(target)
    for r in lock["files"]:
        if r["dst"] == LIFECYCLE:
            r["hash"] = stale
    (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        s._emit_lock_yaml(lock), encoding="utf-8")

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0

    healed = s.read_lockfile(target)
    rec = next(r for r in healed["files"] if r["dst"] == LIFECYCLE)
    on_disk = "sha256:" + s._sha256_hex((target / LIFECYCLE).read_bytes())
    assert rec["hash"] == on_disk
    assert rec["hash"] != stale
