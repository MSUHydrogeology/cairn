"""Scaffold upgrade: occupied-destination and ownership refusals for a file
added to the core or skills mappings.

A file that a later Cairn version adds to the core or skills mappings can meet
a project that already has something at its destination. `upgrade` must never
overwrite it silently. This pins the refusals, using one tracked skills file
(`tools/board.py`) as the occupied destination:

* **an occupied, unlocked destination is an adoptable collision** that blocks
  `--apply` until the operator keeps it as a tracked fork
  (`--adopt-collisions`) or removes it and re-stages (accept upstream);
* **a verbatim fork** records `base_hash = upstream` (shared
  `_record_fork_entry`), so it survives two upstream versions as
  `locally-modified`, never `update`;
* **the new-core enumeration** splits occupied destinations three ways:
  present-unlocked (adoptable), absent-but-locked (not a collision), and
  present-and-locked-under-another-source (a distinct, non-adoptable conflict);
* **the published manifest** refuses two rows for one destination.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_side_door_parity.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

# The occupied destination: a verbatim file the skills mapping installs.
_TARGET = "tools/board.py"
_TARGET_SRC = "skills/_lib/board.py"


def _install(target: Path) -> None:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    assert s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0


def _write_lock(target: Path, lock: dict) -> None:
    (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
    (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
        s._emit_lock_yaml(lock), encoding="utf-8")


def _make_untracked(target: Path, *, keep_on_disk: bool = False) -> None:
    """Mutate a freshly-installed tree so the lockfile no longer tracks the
    target file: drop its lockfile entry and, unless `keep_on_disk`, delete the
    file. Kept on disk it models an occupied-destination collision."""
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] != _TARGET]
    _write_lock(target, lock)
    path = target / _TARGET
    if not keep_on_disk and path.exists():
        path.unlink()


def _base(target: Path) -> list[str]:
    return ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]


def _adopt_args(target: Path, *collides: str) -> list[str]:
    """The operator-supplied `dst@observed@upstream` triples for the given
    adoptable new-core collisions -- exactly what `upgrade --plan` prints."""
    lock = s.read_lockfile(target)
    plans, _ = s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, None)
    by_dst = {fp.dst: fp for fp in plans
              if fp.kind in ("new-core-blocked", "new-module-blocked") and fp.src}
    out = []
    for c in collides:
        fp = by_dst[c]
        obs = s._sha256_hex((target / c).read_bytes())
        up = s._sha256_hex((fp.theirs_raw or "").encode("utf-8"))
        out.append(f"{c}@{obs}@{up}")
    return out


# ===========================================================================
# New-core occupied-destination collision split
# ===========================================================================

def test_present_unlocked_file_is_an_adoptable_new_core_collision(tmp_path: Path):
    # Present on disk + UNLOCKED -> new-core-blocked, adoptable (carries src), and
    # --apply fails closed unconditionally until reconciled (no silent overwrite).
    target = tmp_path.resolve()
    _install(target)
    _make_untracked(target, keep_on_disk=True)
    (target / _TARGET).write_text("# my customized file\n", encoding="utf-8")

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    fp = plans[_TARGET]
    assert fp.kind == "new-core-blocked"
    assert fp.kind not in s._ADVANCING_KINDS
    assert fp.src == _TARGET_SRC                  # adoptable -> carries canonical src
    assert fp.theirs_raw is not None              # the upstream merge base

    base = _base(target)
    assert s.main(base + ["--stage"]) == 0
    # the occupied file hard-blocks --apply (neither override bypasses it)
    assert s.main(base + ["--apply"]) != 0
    assert s.main(base + ["--apply", "--ack-review-only"]) != 0
    assert s.main(base + ["--apply", "--force"]) != 0
    # the adopter's bytes are untouched by the blocked upgrade
    assert (target / _TARGET).read_text(encoding="utf-8") \
        == "# my customized file\n"


def test_absent_but_locked_file_is_not_a_new_core_collision(tmp_path: Path):
    # Tracked (locked) but missing on disk -> NOT a new-core collision (its src is
    # in lock_srcs, so the new-core loop skips it); handled by the tracked-file
    # path, never surfaced as new-core-blocked/lockconflict.
    target = tmp_path.resolve()
    _install(target)
    (target / _TARGET).unlink()                   # tracked entry stays in lockfile

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    entry = plans.get(_TARGET)
    assert entry is None or entry.kind not in (
        "new-core-blocked", "new-core-lockconflict")


def test_present_and_locked_under_another_source_is_a_distinct_conflict(tmp_path: Path):
    # Dst tracked under ANOTHER lockfile source -> new-core-lockconflict, a
    # provenance conflict adoption never clears (never adoptable).
    target = tmp_path.resolve()
    _install(target)
    _make_untracked(target, keep_on_disk=True)
    (target / _TARGET).write_text("# adopter fork\n", encoding="utf-8")
    lock = s.read_lockfile(target)
    lock["files"].append({"src": "modules/bogus/elsewhere.py", "dst": _TARGET,
                          "verbatim": True,
                          "hash": "sha256:" + s._sha256_hex(b"x")})
    _write_lock(target, lock)

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    assert plans[_TARGET].kind == "new-core-lockconflict"
    assert plans[_TARGET].kind not in s._ADVANCING_KINDS

    # Authorizing it refuses (it is not in the live adoptable set).
    obs = s._sha256_hex((target / _TARGET).read_bytes())
    assert s.main(_base(target)
                  + ["--adopt-collisions", f"{_TARGET}@{obs}@" + "0" * 64]) != 0


# ===========================================================================
# Keep-mine via --adopt-collisions; accept-upstream via remove-and-re-stage
# ===========================================================================

def test_keep_mine_fork_via_adopt_collisions(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_untracked(target, keep_on_disk=True)
    (target / _TARGET).write_text("# my customized file\n", encoding="utf-8")
    fork = (target / _TARGET).read_bytes()
    base = _base(target)
    assert s.main(base + ["--stage"]) == 0

    # Adopt: records the on-disk fork; never writes the dst.
    assert s.main(base + ["--adopt-collisions"] + _adopt_args(target, _TARGET)) == 0
    assert (target / _TARGET).read_bytes() == fork

    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == _TARGET)
    assert rec["src"] == _TARGET_SRC
    assert rec["verbatim"] is True
    assert rec["hash"] == "sha256:" + s._sha256_hex(fork)      # integrity
    assert rec.get("base_hash") and rec["base_hash"] != rec["hash"]  # upstream base

    # Re-stage -> the file is a kept verbatim-locally-modified fork, the hard
    # block is gone -> --apply completes directly.
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / _TARGET).read_bytes() == fork
    after = {r["dst"] for r in s.read_lockfile(target)["files"]}
    assert _TARGET in after


def test_fork_survives_two_upstream_versions(tmp_path: Path):
    # A verbatim fork must record base_hash=upstream, NOT only its own
    # hash, or a later upstream change classifies `update` and overwrites the fork.
    target = tmp_path.resolve()
    _install(target)
    _make_untracked(target, keep_on_disk=True)
    (target / _TARGET).write_text("# my file\n", encoding="utf-8")
    base = _base(target)
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--adopt-collisions"] + _adopt_args(target, _TARGET)) == 0

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    fork = (target / _TARGET).read_bytes()
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == _TARGET)
    later_upstream = b"# a brand-new version 2\n"
    assert UP.classify_verbatim(
        fork, rec["base_hash"], later_upstream) == "locally-modified"
    # Proof of the closed bug: with only `hash` (=the fork) it would be `update`.
    assert UP.classify_verbatim(
        fork, rec["hash"], later_upstream) == "update"


def test_accept_upstream_via_remove_and_restage(tmp_path: Path):
    # A stale file at the destination blocks; remove it + re-stage to accept
    # upstream -> the current file, tracked.
    target = tmp_path.resolve()
    _install(target)
    _make_untracked(target, keep_on_disk=True)
    (target / _TARGET).write_text("# stale copy\n", encoding="utf-8")
    base = _base(target)

    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) != 0        # the stale file blocks

    (target / _TARGET).unlink()                   # accept upstream
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0

    upstream = (TEMPLATES_ROOT / _TARGET_SRC).read_bytes()
    assert (target / _TARGET).read_bytes() == upstream
    after = {r["dst"] for r in s.read_lockfile(target)["files"]}
    assert (target / _TARGET).is_file()
    assert _TARGET in after


# ===========================================================================
# Destination ownership
# ===========================================================================

def test_install_manifest_refuses_a_duplicate_destination(monkeypatch):
    # The published manifest -- and the lockfile
    # derived from it -- must refuse two rows for one destination.
    import bootstrap._scaffold.install as inst  # noqa: PLC0415
    dup = inst._SKILLS_MAPPINGS + (
        ("skills/_lib/session.py", _TARGET, True),)
    monkeypatch.setattr(inst, "_SKILLS_MAPPINGS", dup)
    with pytest.raises(ValueError, match="destination-ownership conflict"):
        inst.install_manifest()
