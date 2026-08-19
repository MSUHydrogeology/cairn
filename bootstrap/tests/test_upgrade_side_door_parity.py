"""Scaffold upgrade: install.py side-door executable parity (plan
`2026-06-10-claude-cairn-upgrade-install-side-door-parity`).

`install_onboarding` historically fanned the progressive-onboarding launcher
(`scripts/onboarding_activate.py`) + its `_onboarding/` engine package out
UNCONDITIONALLY but OUTSIDE the manifest/lockfile -- a side door: `upgrade`
could not enumerate/refresh/attest them and the release Bandit scan never
covered them. This pins the parity fix:

* **one scanned shipped-executable authority: every verbatim always-on
  `.py` is a `scan_targets()` entry; a fresh install tracks the launcher+engine
  and `verify_integrity` attests them.
* **a surfaced verbatim launcher fork** records `base_hash = upstream`
  (shared `_record_fork_entry`), so it survives two upstream versions as
  `locally-modified`, never `update`.
* **the existing-adopter migration** composes with the sibling
  `--adopt-collisions` (keep-mine) + remove-and-re-stage (accept-upstream); no
  new backfill command.
* **the launcher + engine are a required completeness group**: install,
  lockfile write, and upgrade advancement fail closed on a partial group.
* **the new-core enumeration** mirrors the new-module occupied-destination
  split: present-unlocked (adoptable), absent-but-locked (not a collision), and
  present-and-locked-under-another-source (a distinct, non-adoptable conflict).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_side_door_parity.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap import verify_integrity  # noqa: E402
from bootstrap._scaffold import install_onboarding  # noqa: E402
from bootstrap._scaffold.config import _ALWAYS_ON_MAPPINGS  # noqa: E402
from bootstrap._scaffold.security import ScaffoldSecurityError  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "modules" / "default-on" / "_onboarding").exists(),
    reason="the onboarding launcher+engine split is not in templates",
)

# The always-on executable completeness group: the launcher + its engine package.
_LAUNCHER = "scripts/onboarding_activate.py"
_ENGINE_NAMES = ("__init__", "activation", "cli", "prompts", "security",
                 "shared", "slotparse", "triggers")
_ENGINE_DSTS = [f"scripts/_onboarding/{n}.py" for n in _ENGINE_NAMES]
_ALWAYS_ON_DSTS = [_LAUNCHER] + _ENGINE_DSTS


def _src_for(dst: str) -> str:
    """The canonical lockfile source key for an always-on dst -- install records
    `f"modules/{spec.src}"` (the `modules/` namespace install_manifest +
    scan_targets share)."""
    name = dst.rsplit("/", 1)[1]
    if dst == _LAUNCHER:
        return "modules/default-on/onboarding_activate.py"
    return "modules/default-on/_onboarding/" + name


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


def _make_pre_parity(target: Path, *, keep_on_disk: tuple[str, ...] = ()) -> None:
    """Mutate a freshly-installed tree to look like a **pre-side-door-parity
    adopter**: drop the always-on launcher+engine entries from the lockfile and
    delete the on-disk files, so the lockfile no longer tracks them (the state an
    adopter who bootstrapped before parity lands in -- the files were
    side-door-delivered but never recorded). `keep_on_disk` leaves named dsts on
    disk (un-tracked) to model an occupied-destination collision."""
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] not in _ALWAYS_ON_DSTS]
    _write_lock(target, lock)
    for dst in _ALWAYS_ON_DSTS:
        if dst in keep_on_disk:
            continue
        p = target / dst
        if p.exists():
            p.unlink()


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


def _doctored_templates(tmp_path: Path, drop: str) -> Path:
    """A copy of `templates/` with one always-on source removed -- models a
    corrupted checkout / a misregistered spec for the completeness-group guard."""
    tpl2 = tmp_path / "doctored-templates"
    shutil.copytree(TEMPLATES_ROOT, tpl2)
    (tpl2 / drop).unlink()
    return tpl2


# ===========================================================================
# One scanned shipped-executable authority
# ===========================================================================

def test_fresh_install_tracks_launcher_and_engine(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)

    lock = s.read_lockfile(target)
    tracked = {r["dst"] for r in lock["files"]}
    for dst in _ALWAYS_ON_DSTS:
        assert dst in tracked, f"{dst} not tracked in the lockfile"
        rec = next(r for r in lock["files"] if r["dst"] == dst)
        assert rec["src"] == _src_for(dst)        # canonical modules/ namespace
        assert rec["verbatim"] is True            # byte-for-byte executables
        assert (target / dst).is_file()           # actually installed

    # Attestation closure: verify_integrity passes over the installed tree
    # (it attests exactly the lockfile-tracked set, now incl. launcher+engine).
    assert verify_integrity.main(["--target", str(target)]) == 0


def test_always_on_executables_are_release_scan_targets():
    # Every verbatim always-on .py enters the release Bandit scan -- closing
    # the pre-existing blind spot (they shipped outside _MODULE_MAPPINGS).
    from bootstrap.security_check import scan_targets  # noqa: PLC0415
    targets = set(scan_targets())
    scanned = 0
    for spec in _ALWAYS_ON_MAPPINGS:
        if spec.verbatim and spec.src.endswith(".py"):
            assert f"templates/modules/{spec.src}" in targets, spec.src
            scanned += 1
    assert scanned == 9, f"expected launcher + 8 engine members, got {scanned}"


# ===========================================================================
# New-core occupied-destination collision split
# ===========================================================================

def test_present_unlocked_launcher_is_an_adoptable_new_core_collision(tmp_path: Path):
    # Present on disk + UNLOCKED -> new-core-blocked, adoptable (carries src), and
    # --apply fails closed unconditionally until reconciled (no silent overwrite).
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# my customized launcher\n", encoding="utf-8")

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    fp = plans[_LAUNCHER]
    assert fp.kind == "new-core-blocked"
    assert fp.kind not in s._ADVANCING_KINDS
    assert fp.src == _src_for(_LAUNCHER)          # adoptable -> carries canonical src
    assert fp.theirs_raw is not None              # the upstream merge base

    base = _base(target)
    assert s.main(base + ["--stage"]) == 0
    # the occupied launcher hard-blocks --apply (neither override bypasses it)
    assert s.main(base + ["--apply"]) != 0
    assert s.main(base + ["--apply", "--ack-review-only"]) != 0
    assert s.main(base + ["--apply", "--force"]) != 0
    # the adopter's bytes are untouched by the blocked upgrade
    assert (target / _LAUNCHER).read_text(encoding="utf-8") \
        == "# my customized launcher\n"


def test_absent_but_locked_launcher_is_not_a_new_core_collision(tmp_path: Path):
    # Tracked (locked) but missing on disk -> NOT a new-core collision (its src is
    # in lock_srcs, so the new-core loop skips it); handled by the tracked-file
    # path, never surfaced as new-core-blocked/lockconflict.
    target = tmp_path.resolve()
    _install(target)
    (target / _LAUNCHER).unlink()                 # tracked entry stays in lockfile

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    launcher = plans.get(_LAUNCHER)
    assert launcher is None or launcher.kind not in (
        "new-core-blocked", "new-core-lockconflict")


def test_present_and_locked_under_another_source_is_a_distinct_conflict(tmp_path: Path):
    # Dst tracked under ANOTHER lockfile source -> new-core-lockconflict, a
    # provenance conflict adoption never clears (never adoptable).
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# adopter fork\n", encoding="utf-8")
    lock = s.read_lockfile(target)
    lock["files"].append({"src": "modules/bogus/elsewhere.py", "dst": _LAUNCHER,
                          "verbatim": True,
                          "hash": "sha256:" + s._sha256_hex(b"x")})
    _write_lock(target, lock)

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    assert plans[_LAUNCHER].kind == "new-core-lockconflict"
    assert plans[_LAUNCHER].kind not in s._ADVANCING_KINDS

    # Authorizing it refuses (it is not in the live adoptable set).
    obs = s._sha256_hex((target / _LAUNCHER).read_bytes())
    assert s.main(_base(target)
                  + ["--adopt-collisions", f"{_LAUNCHER}@{obs}@" + "0" * 64]) != 0


# ===========================================================================
# Keep-mine via --adopt-collisions; accept-upstream via remove-and-re-stage
# ===========================================================================

def test_keep_mine_launcher_fork_via_adopt_collisions(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# my customized launcher\n", encoding="utf-8")
    fork = (target / _LAUNCHER).read_bytes()
    base = _base(target)
    assert s.main(base + ["--stage"]) == 0

    # Adopt: records the on-disk fork; never writes the dst.
    assert s.main(base + ["--adopt-collisions"] + _adopt_args(target, _LAUNCHER)) == 0
    assert (target / _LAUNCHER).read_bytes() == fork

    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == _LAUNCHER)
    assert rec["src"] == _src_for(_LAUNCHER)
    assert rec["verbatim"] is True
    assert rec["hash"] == "sha256:" + s._sha256_hex(fork)      # integrity
    assert rec.get("base_hash") and rec["base_hash"] != rec["hash"]  # upstream base

    # Re-stage -> the launcher is a kept verbatim-locally-modified fork, the engine
    # adds clean, the hard block is gone -> --apply completes directly.
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / _LAUNCHER).read_bytes() == fork
    for dst in _ENGINE_DSTS:
        assert (target / dst).is_file()
    after = {r["dst"] for r in s.read_lockfile(target)["files"]}
    for dst in _ALWAYS_ON_DSTS:
        assert dst in after


def test_launcher_fork_survives_two_upstream_versions(tmp_path: Path):
    # A verbatim launcher fork must record base_hash=upstream, NOT only its own
    # hash, or a later upstream change classifies `update` and overwrites the fork.
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# my launcher\n", encoding="utf-8")
    base = _base(target)
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--adopt-collisions"] + _adopt_args(target, _LAUNCHER)) == 0

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    fork = (target / _LAUNCHER).read_bytes()
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == _LAUNCHER)
    later_upstream = b"# a brand-new thin launcher v2\n"
    assert UP.classify_verbatim(
        fork, rec["base_hash"], later_upstream) == "locally-modified"
    # Proof of the closed bug: with only `hash` (=the fork) it would be `update`.
    assert UP.classify_verbatim(
        fork, rec["hash"], later_upstream) == "update"


def test_accept_upstream_via_remove_and_restage(tmp_path: Path):
    # The stock-monolith (LHM) path: a stale launcher blocks; remove it + re-stage
    # to accept upstream -> the thin launcher + complete engine, all tracked.
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# stale monolith launcher\n", encoding="utf-8")
    base = _base(target)

    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) != 0        # the stale launcher blocks

    (target / _LAUNCHER).unlink()                 # accept upstream
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0

    upstream = (TEMPLATES_ROOT
                / "modules/default-on/onboarding_activate.py").read_bytes()
    assert (target / _LAUNCHER).read_bytes() == upstream   # the thin launcher
    after = {r["dst"] for r in s.read_lockfile(target)["files"]}
    for dst in _ALWAYS_ON_DSTS:
        assert (target / dst).is_file()
        assert dst in after


# ===========================================================================
# The launcher + engine are a required completeness group
# ===========================================================================

def test_install_onboarding_fails_closed_on_missing_launcher(tmp_path: Path):
    tpl2 = _doctored_templates(tmp_path, "modules/default-on/onboarding_activate.py")
    target = tmp_path / "adopter"
    target.mkdir()
    with pytest.raises(ScaffoldSecurityError):
        install_onboarding(tpl2, target, None)
    # fail-closed BEFORE any write: no facade, no engine on disk
    assert not (target / _LAUNCHER).exists()
    assert not (target / "scripts" / "_onboarding").exists()


def test_install_onboarding_fails_closed_on_missing_engine_member(tmp_path: Path):
    tpl2 = _doctored_templates(tmp_path, "modules/default-on/_onboarding/cli.py")
    target = tmp_path / "adopter"
    target.mkdir()
    with pytest.raises(ScaffoldSecurityError):
        install_onboarding(tpl2, target, None)
    assert not (target / _LAUNCHER).exists()      # a facade never ships without
    assert not (target / "scripts" / "_onboarding").exists()  # its engine


def test_write_install_lockfile_refuses_partial_group(tmp_path: Path):
    from bootstrap._scaffold import write_install_lockfile  # noqa: PLC0415
    tpl2 = _doctored_templates(tmp_path, "modules/default-on/_onboarding/triggers.py")
    target = tmp_path / "adopter"
    target.mkdir()
    result = write_install_lockfile(
        target, CAIRN_ROOT, tpl2,
        tokens={}, modules=[], optional=[], profile={"axes": {}})
    assert result is None                         # refuse-signal, no partial lock
    assert not (target / s._LOCKFILE_REL).exists()


def test_upgrade_fails_closed_when_a_group_source_is_missing(tmp_path: Path):
    # The upgrade-advancement guard: a missing engine source makes the group
    # incomplete, so NO member advances -- a facade never advances over an absent
    # engine member. Modelled with a doctored templates_root (one member dropped).
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target)                      # launcher+engine untracked + gone
    tpl2 = _doctored_templates(tmp_path, "modules/default-on/_onboarding/triggers.py")

    lock = s.read_lockfile(target)
    plans = s._compute_upgrade(target, CAIRN_ROOT, tpl2, lock, to_ref=None)[0]
    kinds = {fp.dst: fp.kind for fp in plans}

    incomplete = [fp.dst for fp in plans
                  if fp.kind == "new-core-incomplete-group"]
    assert incomplete, "expected the completeness group to fail closed on upgrade"
    # the present launcher is blocked, not advanced over the missing engine member
    assert _LAUNCHER in incomplete
    assert "new-core" not in {kinds[d] for d in _ALWAYS_ON_DSTS if d in kinds}
    # the incomplete-group block is a hard block (non-advancing)
    assert "new-core-incomplete-group" not in s._ADVANCING_KINDS


def test_adopt_collisions_refuses_a_partial_group(tmp_path: Path):
    # An occupied-unlocked launcher must NOT be
    # adoptable while an engine source is missing -- adopting it would advance the
    # lockfile authority for a partial group. The post-pass converts the occupied
    # launcher to the incomplete-group hard block (no longer adoptable), so
    # `_cmd_adopt_collisions` records nothing and the lockfile is unchanged.
    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    target = tmp_path.resolve()
    _install(target)
    _make_pre_parity(target, keep_on_disk=(_LAUNCHER,))
    (target / _LAUNCHER).write_text("# my launcher fork\n", encoding="utf-8")
    tpl2 = _doctored_templates(tmp_path, "modules/default-on/_onboarding/triggers.py")

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, tpl2, lock, to_ref=None)[0]}
    # the occupied launcher is the incomplete-group hard block, NOT adoptable
    assert plans[_LAUNCHER].kind == "new-core-incomplete-group"

    before = (target / s._LOCKFILE_REL).read_bytes()
    obs = s._sha256_hex((target / _LAUNCHER).read_bytes())
    rc = UP._cmd_adopt_collisions(
        target, CAIRN_ROOT, tpl2, lock, [f"{_LAUNCHER}@{obs}@" + "0" * 64])
    assert rc != 0                                           # adoption refused
    assert (target / s._LOCKFILE_REL).read_bytes() == before  # lock UNCHANGED
    assert not any(r["dst"] == _LAUNCHER
                   for r in s.read_lockfile(target)["files"])


def test_install_onboarding_refuses_a_duplicate_destination(tmp_path: Path, monkeypatch):
    # Two always-on specs claiming one destination
    # must fail closed BEFORE any write -- otherwise `--force` writes both in
    # sequence and silently shadows the launcher. Destination ownership is checked
    # alongside source completeness in `assert_always_on_complete`.
    import bootstrap._scaffold.install as inst  # noqa: PLC0415
    from bootstrap._scaffold.config import InstallSpec  # noqa: PLC0415
    target = tmp_path / "adopter"
    (target / "scripts").mkdir(parents=True)
    (target / _LAUNCHER).write_text("# the original launcher\n", encoding="utf-8")
    dup = inst._ALWAYS_ON_MAPPINGS + (
        InstallSpec("default-on/_onboarding/triggers.py", _LAUNCHER, True),)
    monkeypatch.setattr(inst, "_ALWAYS_ON_MAPPINGS", dup)

    with pytest.raises(ScaffoldSecurityError):
        inst.install_onboarding(TEMPLATES_ROOT, target, None, force=True)
    # refused before any write -> the original launcher is untouched
    assert (target / _LAUNCHER).read_text(encoding="utf-8") \
        == "# the original launcher\n"


def test_install_manifest_refuses_a_duplicate_destination(monkeypatch):
    # The published manifest -- and the lockfile
    # derived from it -- must refuse two rows for one destination.
    import bootstrap._scaffold.install as inst  # noqa: PLC0415
    from bootstrap._scaffold.config import InstallSpec  # noqa: PLC0415
    dup = inst._ALWAYS_ON_MAPPINGS + (
        InstallSpec("default-on/_onboarding/triggers.py", _LAUNCHER, True),)
    monkeypatch.setattr(inst, "_ALWAYS_ON_MAPPINGS", dup)
    with pytest.raises(ValueError, match="destination-ownership conflict"):
        inst.install_manifest()
