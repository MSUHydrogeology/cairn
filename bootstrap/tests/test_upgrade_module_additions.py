"""Upgrade carries module-internal file additions to already-adopted modules
(plan `2026-06-10-claude-cairn-scaffold-upgrade-module-additions`).

The classifier auto-adds new core/skills files but, before this change, never
new files belonging to a module the adopter has ALREADY adopted -- so a module
that split a single tool into a facade + a sibling package upstream (the
`lifecycle_metrics.py` -> `_lifecycle_metrics/` case) could not be consumed via
`scaffold.py upgrade`. This pins the `new-module` add path and the Codex-review
hardening (R1 canonical source-key namespace, R2 expected-absence through apply,
R3 occupied-destination collision + duplicate-destination ownership, R5 `--to`
registry contract, and the UTF-8-text-only constraint).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_module_additions.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold.config import InstallSpec  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "modules" / "default-on" / "_lifecycle_metrics").exists(),
    reason="the _lifecycle_metrics split package is not in templates",
)

# The lifecycle-metrics module (default-on, always adopted) ships its engine as a
# facade + a sibling `_lifecycle_metrics/` package -- the canonical split case.
_FACADE = "tools/lifecycle_metrics.py"
_PKG_NAMES = ("__init__", "config", "parse", "gitmeta", "report",
              "subsystems", "extract", "snapshot", "cli")
_PKG_DSTS = [f"tools/_lifecycle_metrics/{n}.py" for n in _PKG_NAMES]


def _src_for(dst: str) -> str:
    """The canonical lockfile source key for a `_lifecycle_metrics/` dst --
    install records `f"modules/{spec.src}"` (the namespace R1 is about)."""
    return "modules/default-on/_lifecycle_metrics/" + dst.rsplit("/", 1)[1]


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


def _make_pre_split(target: Path, *, keep_on_disk: tuple[str, ...] = ()) -> None:
    """Mutate a freshly-installed tree to look like a **pre-split adopter**: drop
    the `_lifecycle_metrics/*` package entries from the lockfile and delete the
    on-disk package files, so the lockfile no longer knows the package exists
    (the state an adopter who bootstrapped before the split lands in). The facade
    stays tracked. `keep_on_disk` leaves named dsts on disk (un-tracked) to model
    an occupied-destination collision."""
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] not in _PKG_DSTS]
    _write_lock(target, lock)
    for dst in _PKG_DSTS:
        if dst in keep_on_disk:
            continue
        p = target / dst
        if p.exists():
            p.unlink()


# ---------------------------------------------------------------------------
# R1 -- canonical source-key namespace + positive add
# ---------------------------------------------------------------------------

def test_pre_split_compute_surfaces_package_as_new_module(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    lock = s.read_lockfile(target)
    plans, _structural = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)
    new_module = {p.dst: p for p in plans if p.kind == "new-module"}

    # Every dropped package file is detected as a new-module add (proves the
    # canonical `modules/<spec.src>` namespace -- a raw-src comparison would
    # match nothing here, since the dropped srcs ARE module-relative).
    assert set(new_module) == set(_PKG_DSTS), f"got {sorted(new_module)}"
    for dst, p in new_module.items():
        assert p.kind in s._ADVANCING_KINDS
        assert p.verbatim is True          # package .py files are verbatim code
        assert p.src == _src_for(dst)      # canonical lockfile namespace (R1)


def test_pre_split_apply_records_package_in_lockfile(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0

    # On disk and recorded in the lockfile under the canonical src.
    lock = s.read_lockfile(target)
    by_dst = {r["dst"]: r for r in lock["files"]}
    for dst in _PKG_DSTS:
        assert (target / dst).exists(), f"missing on disk: {dst}"
        assert dst in by_dst, f"missing from lockfile: {dst}"
        assert by_dst[dst]["src"] == _src_for(dst)
        assert by_dst[dst]["verbatim"] is True


# ---------------------------------------------------------------------------
# R1 -- new-upstream only: a deliberately-deleted tracked file stays deleted
# ---------------------------------------------------------------------------

def test_deleted_tracked_module_file_is_not_re_added(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    # Delete the on-disk package files but KEEP their lockfile entries -- the
    # adopter deliberately removed them. The canonical src stays in lock_srcs,
    # so they must NOT be classified new-module.
    for dst in _PKG_DSTS:
        p = target / dst
        if p.exists():
            p.unlink()

    lock = s.read_lockfile(target)
    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)
    new_module = {p.dst for p in plans if p.kind == "new-module"}
    assert new_module == set(), f"re-added a deleted tracked file: {new_module}"


# ---------------------------------------------------------------------------
# R3 -- occupied-destination collision is a non-advancing review-only block
# ---------------------------------------------------------------------------

def test_occupied_destination_is_hard_blocked_not_ack_bypassable(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    # Drop the package from the lockfile but leave ONE package file on disk
    # (unlocked) with adopter-local content -> a genuine new-upstream spec whose
    # destination already exists outside the lockfile.
    collide = _PKG_DSTS[1]   # tools/_lifecycle_metrics/config.py
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_text("# adopter-local content\n", encoding="utf-8")

    lock = s.read_lockfile(target)
    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)
    by_dst = {p.dst: p for p in plans}

    # The collision is a DISTINCT hard-blocking kind (NOT ordinary review-only),
    # so generic --ack-review-only cannot bypass it; the rest add as new-module.
    assert by_dst[collide].kind == "new-module-blocked"
    assert by_dst[collide].kind not in s._ADVANCING_KINDS
    assert all(by_dst[d].kind == "new-module" for d in _PKG_DSTS if d != collide)

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    # Neither plain --apply, NOR --ack-review-only, NOR --force may advance.
    assert s.main(base + ["--apply"]) != 0
    assert s.main(base + ["--apply", "--ack-review-only"]) != 0
    assert s.main(base + ["--apply", "--ack-review-only", "--force"]) != 0
    # The adopter-local content is untouched; the lock did NOT advance to record
    # the collided file (it must never be left importable-but-unattested); and
    # the sibling adds did not land either (the whole apply failed closed).
    assert (target / collide).read_text() == "# adopter-local content\n"
    lock_after = s.read_lockfile(target)
    assert not any(r["dst"] == collide for r in lock_after["files"])
    assert not (target / _PKG_DSTS[0]).exists()


# ---------------------------------------------------------------------------
# R2 -- expected-absence protected through apply (data-loss guard); --force
#       does NOT override it
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("force", [False, True])
def test_destination_appearing_after_stage_blocks_apply(tmp_path: Path, force: bool):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0

    # Another process creates one staged (expected-absent) destination AFTER
    # --stage, with its own content.
    appeared = target / _PKG_DSTS[2]
    appeared.parent.mkdir(parents=True, exist_ok=True)
    appeared.write_text("# created after stage\n", encoding="utf-8")

    apply = base + ["--apply"] + (["--force"] if force else [])
    assert s.main(apply) != 0, "apply must fail closed on a reappeared dst"
    # The content created since --stage is NOT overwritten.
    assert appeared.read_text() == "# created after stage\n"


def test_symlinked_destination_after_stage_blocks_apply(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0

    # A symlink appears at a staged destination -> fail closed (broken symlinks
    # do not satisfy exists(), so the guard checks is_symlink() too).
    link = target / _PKG_DSTS[3]
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target / "nonexistent-target")
    assert s.main(base + ["--apply"]) != 0


# ---------------------------------------------------------------------------
# Opt-in preserved: a module the adopter has NOT adopted never auto-adds
# ---------------------------------------------------------------------------

def test_not_adopted_module_files_are_not_auto_added(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)   # modules: [] -> only default-on; team-gated NOT adopted

    lock = s.read_lockfile(target)
    adopted = set(lock.get("modules", []))
    # Find a team-gated module that is NOT adopted and whose specs exist.
    from bootstrap._scaffold.config import _MODULE_MAPPINGS  # noqa: PLC0415
    not_adopted = [m for m in _MODULE_MAPPINGS if m not in adopted]
    assert not_adopted, "expected at least one un-adopted module"
    not_adopted_dsts = {
        spec.dst for m in not_adopted for spec in _MODULE_MAPPINGS[m]}

    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)
    added = {p.dst for p in plans if p.kind == "new-module"}
    assert not (added & not_adopted_dsts), \
        f"auto-added un-adopted module files: {added & not_adopted_dsts}"


# ---------------------------------------------------------------------------
# R5 -- structural module additions are skipped under an explicit --to <ref>
# ---------------------------------------------------------------------------

def test_module_additions_under_explicit_to_are_hard_blocked(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    lock = s.read_lockfile(target)
    # Under an explicit --to, structural additions are enumerated from the
    # running registry (which need not match the ref) -> NOT silently skipped,
    # but a hard block, so a facade cannot advance without its package.
    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref="HEAD")
    assert [p for p in plans if p.kind == "new-module"] == []   # no silent add
    blocked = [p for p in plans if p.kind == "new-module-blocked"]
    assert len(blocked) == len(_PKG_DSTS), f"expected all blocked, got {len(blocked)}"
    assert all(p.kind not in s._ADVANCING_KINDS for p in blocked)

    # Public path: a --to upgrade with pending additions fails closed at apply
    # (nothing advances), proving the facade cannot move without its package.
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT),
            "--to", "HEAD"]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) != 0
    assert s.main(base + ["--apply", "--ack-review-only", "--force"]) != 0


# ---------------------------------------------------------------------------
# R3 -- duplicate destination ownership across mappings is refused, not deduped
# ---------------------------------------------------------------------------

def test_duplicate_destination_ownership_is_refused(tmp_path: Path, monkeypatch):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    lock = s.read_lockfile(target)
    # Inject a second adopted-module spec that claims an already-claimed NEW
    # destination (the first package file) -> a mapping-ownership conflict.
    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    dup = _PKG_DSTS[0]
    patched = dict(UP._MODULE_MAPPINGS)
    # Append a colliding spec to an adopted module's mapping list.
    adopted = next(m for m in lock.get("modules", []) if m in patched)
    patched[adopted] = list(patched[adopted]) + [
        InstallSpec("default-on/_lifecycle_metrics/__init__.py", dup, verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/__init__.py", dup, verbatim=True),
    ]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)

    with pytest.raises(ValueError, match="mapping ownership conflict"):
        s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)


# ---------------------------------------------------------------------------
# Text-only contract: a non-UTF-8 module InstallSpec fails crisply
# ---------------------------------------------------------------------------

def test_non_text_module_addition_fails_crisply(tmp_path: Path, monkeypatch):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    lock = s.read_lockfile(target)
    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    bin_dst = "tools/_lifecycle_metrics/asset.bin"
    bin_src_rel = "default-on/_lifecycle_metrics/asset.bin"
    patched = dict(UP._MODULE_MAPPINGS)
    adopted = next(m for m in lock.get("modules", []) if m in patched)
    patched[adopted] = list(patched[adopted]) + [
        InstallSpec(bin_src_rel, bin_dst, verbatim=True)]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)
    # Make the (canonical) template resolve to non-UTF-8 bytes.
    real_theirs = UP._theirs_bytes

    def fake_theirs(cairn_root, templates_root, src_rel, to_ref):
        if src_rel == f"modules/{bin_src_rel}":
            return b"\xff\xfe\x00\x01binary"
        return real_theirs(cairn_root, templates_root, src_rel, to_ref)

    monkeypatch.setattr(UP, "_theirs_bytes", fake_theirs)

    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)
    by_dst = {p.dst: p for p in plans}
    assert by_dst[bin_dst].kind == "error"
    assert "UTF-8" in by_dst[bin_dst].detail
    assert by_dst[bin_dst].kind not in s._ADVANCING_KINDS


# ---------------------------------------------------------------------------
# F1 -- a malformed (traversing) destination is refused before any stage write
# ---------------------------------------------------------------------------

def test_malformed_module_destination_is_refused_at_stage(tmp_path: Path, monkeypatch):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)
    escaped = tmp_path / "escaped.txt"   # OUTSIDE the adopter target
    assert not escaped.exists()

    # Inject a hypothetical malformed hard-coded InstallSpec.dst with traversal
    # (a real src so the template resolves; the dst escapes the target).
    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    lock = s.read_lockfile(target)
    patched = dict(UP._MODULE_MAPPINGS)
    adopted = next(m for m in lock.get("modules", []) if m in patched)
    patched[adopted] = list(patched[adopted]) + [
        InstallSpec("default-on/_lifecycle_metrics/__init__.py",
                    "../../../../escaped.txt", verbatim=True)]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)

    # --stage fails closed (ScaffoldSecurityError -> CLI exit 2) and writes
    # NOTHING outside the target.
    rc = s.main(["upgrade", "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--stage"])
    assert rc != 0
    assert not escaped.exists()


def test_symlinked_dev_parent_does_not_escape_at_stage(tmp_path: Path):
    # F1 round 2: the stage ROOT mutation (rmtree/mkdir) must be containment-
    # guarded BEFORE it runs -- a symlinked ``target/dev`` parent must not let
    # --stage delete/recreate an EXTERNAL directory.
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)
    # Move dev/ outside the target, symlink target/dev -> it, and seed an
    # external staging dir with a sentinel that must survive.
    external_dev = tmp_path / "external_dev"
    (target / "dev").rename(external_dev)
    (target / "dev").symlink_to(external_dev, target_is_directory=True)
    ext_stage = external_dev / ".cairn-upgrade"
    ext_stage.mkdir(parents=True, exist_ok=True)
    sentinel = ext_stage / "sentinel.txt"
    sentinel.write_text("survive me\n", encoding="utf-8")

    rc = s.main(["upgrade", "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--stage"])
    # Refuses (containment exit 2) AND the external staging dir is untouched.
    assert rc != 0
    assert ext_stage.exists(), "external stage dir was deleted (containment escape)"
    assert sentinel.read_text() == "survive me\n"


# ---------------------------------------------------------------------------
# F4 -- global destination-ownership preflight (across core / skills / modules,
#       independent of lock / source state)
# ---------------------------------------------------------------------------

def test_module_destination_colliding_with_core_is_refused(tmp_path: Path, monkeypatch):
    target = tmp_path.resolve()
    _install(target)

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    core_dst = UP._CORE_MAPPINGS[0][1]   # an existing core destination
    lock = s.read_lockfile(target)
    patched = dict(UP._MODULE_MAPPINGS)
    adopted = next(m for m in lock.get("modules", []) if m in patched)
    patched[adopted] = list(patched[adopted]) + [
        InstallSpec("default-on/_lifecycle_metrics/__init__.py", core_dst,
                    verbatim=True)]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)

    with pytest.raises(ValueError, match="mapping ownership conflict"):
        s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)


def test_duplicate_with_absent_first_source_is_refused(tmp_path: Path, monkeypatch):
    target = tmp_path.resolve()
    _install(target)

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    lock = s.read_lockfile(target)
    patched = dict(UP._MODULE_MAPPINGS)
    adopted = next(m for m in lock.get("modules", []) if m in patched)
    dup_dst = "tools/_lifecycle_metrics/dup_target.py"
    # Two specs claim the same NEW dst; the FIRST points at a non-existent
    # template. The source-state-blind preflight still refuses (a per-file
    # check could skip the first on source absence and miss the duplicate).
    patched[adopted] = list(patched[adopted]) + [
        InstallSpec("default-on/_lifecycle_metrics/does_not_exist.py", dup_dst,
                    verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/__init__.py", dup_dst,
                    verbatim=True)]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)

    with pytest.raises(ValueError, match="mapping ownership conflict"):
        s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)


# ===========================================================================
# adopt-as-fork: `upgrade --adopt-collisions` (plan
# `2026-06-10-claude-cairn-upgrade-collision-adopt-as-fork`, Revised proposal)
# ===========================================================================

def _staged_collision(target: Path, *collides: str) -> list[str]:
    """Install, drop the package, leave `collides` on disk as adopter forks, and
    `--stage`. Returns the base CLI argv. Each collide gets distinct fork bytes."""
    _install(target)
    _make_pre_split(target, keep_on_disk=collides)
    for c in collides:
        (target / c).write_text(f"# adopter fork of {c}\n", encoding="utf-8")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    return base


def test_adopt_collisions_records_fork_and_unblocks(tmp_path: Path):
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    fork_bytes = (target / collide).read_bytes()

    # Adopt: records the on-disk fork; never writes the dst.
    assert s.main(base + ["--adopt-collisions"]) == 0
    assert (target / collide).read_bytes() == fork_bytes   # fork preserved

    # Attestation closure: tracked, with hash=on-disk fork and base_hash=upstream
    # (the two DIFFER -> a fork, never classified safe-to-overwrite).
    lock = s.read_lockfile(target)
    rec = next(r for r in lock["files"] if r["dst"] == collide)
    assert rec["src"] == _src_for(collide)
    assert rec["verbatim"] is True
    assert rec["hash"] == "sha256:" + s._sha256_hex(fork_bytes)
    assert rec.get("base_hash") and rec["base_hash"] != rec["hash"]

    # Re-stage: the adopted collide is now a verbatim-locally-modified fork
    # (flagged + kept, never clobbered) and the sibling package files add as
    # new-module; the hard block is gone, so --apply completes directly.
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / collide).read_bytes() == fork_bytes  # still the fork
    for d in _PKG_DSTS:
        assert (target / d).exists()                      # siblings landed
    after = s.read_lockfile(target)
    assert all(any(r["dst"] == d for r in after["files"]) for d in _PKG_DSTS)


def test_adopt_collisions_verbatim_fork_survives_two_upstream_versions(tmp_path):
    # R1: a verbatim fork must record base_hash=upstream, NOT only its own hash,
    # or a later upstream change classifies `update` and overwrites the fork.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    assert s.main(base + ["--adopt-collisions"]) == 0

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    fork_bytes = (target / collide).read_bytes()
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == collide)
    later_upstream = b"# a brand-new upstream launcher v2\n"

    # With the recorded base_hash (=upstream): the fork stays locally-modified.
    assert UP.classify_verbatim(
        fork_bytes, rec["base_hash"], later_upstream) == "locally-modified"
    # Proof of the bug the fix closes: had we recorded only `hash` (=the fork),
    # the SAME later upstream would classify `update` -> overwrite the fork.
    assert UP.classify_verbatim(
        fork_bytes, rec["hash"], later_upstream) == "update"


def test_adopt_collisions_refuses_if_a_collision_changed_since_stage(tmp_path):
    # R2 (+ R4 all-or-nothing): bind adoption to the staged bytes. Stage two
    # collisions, mutate one after --stage, adopt -> refuse, NEITHER recorded.
    target = tmp_path.resolve()
    c1, c2 = _PKG_DSTS[1], _PKG_DSTS[2]
    base = _staged_collision(target, c1, c2)
    (target / c1).write_text("# changed after stage\n", encoding="utf-8")

    assert s.main(base + ["--adopt-collisions"]) != 0
    lock = s.read_lockfile(target)
    assert not any(r["dst"] in (c1, c2) for r in lock["files"])  # all-or-nothing


def test_adopt_collisions_is_bound_to_the_staged_set_not_a_recompute(tmp_path):
    # R2: a collision appearing AFTER --stage is not in the staged manifest, so
    # adoption never blesses it (it stays untracked -> a fresh --stage blocks).
    target = tmp_path.resolve()
    c1, c2 = _PKG_DSTS[1], _PKG_DSTS[2]
    base = _staged_collision(target, c1)            # only c1 staged
    (target / c2).write_text("# appeared after stage\n", encoding="utf-8")

    assert s.main(base + ["--adopt-collisions"]) == 0
    lock = s.read_lockfile(target)
    assert any(r["dst"] == c1 for r in lock["files"])      # staged one adopted
    assert not any(r["dst"] == c2 for r in lock["files"])  # appeared one is NOT


def test_lockconflict_destination_is_distinct_and_not_adoptable(tmp_path: Path):
    # R3/R5: a new-upstream spec whose dst is already tracked under ANOTHER
    # source is a provenance conflict, not an adoptable fork.
    target = tmp_path.resolve()
    _install(target)
    collide = _PKG_DSTS[1]
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_text("# adopter fork\n", encoding="utf-8")
    # Record the dst under a BOGUS source so dst in lock_dsts but canonical_src
    # is not -> the lock-conflict branch, not the adoptable branch.
    lock = s.read_lockfile(target)
    lock["files"].append({"src": "modules/bogus/elsewhere.py", "dst": collide,
                          "verbatim": True,
                          "hash": "sha256:" + s._sha256_hex(b"x")})
    _write_lock(target, lock)

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    assert plans[collide].kind == "new-module-lockconflict"
    assert plans[collide].kind not in s._ADVANCING_KINDS

    # It is not offered to --adopt-collisions (absent from the staged manifest).
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    import json  # noqa: PLC0415
    meta = json.loads((target / s._STAGING_REL / s._STAGE_META).read_text())
    assert collide not in meta.get("collision_adopt", {})


def test_adopt_collisions_refuses_symlinked_lockfile(tmp_path: Path):
    # R4: the lockfile authority write is guarded; a symlinked lockfile is
    # refused (containment), exit 2, with no mutation.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    lockf = target / s._LOCKFILE_REL
    real = lockf.parent / "real-lock.yml"
    real.write_bytes(lockf.read_bytes())
    lockf.unlink()
    lockf.symlink_to(real.name)

    assert s.main(base + ["--adopt-collisions"]) == 2
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_mutually_exclusive_with_apply(tmp_path: Path):
    # R5: a mixed-action invocation is rejected before any work.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    assert s.main(base + ["--adopt-collisions", "--apply"]) == 2
    # nothing recorded, nothing applied
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])
    assert not (target / _PKG_DSTS[0]).exists()


def test_adopt_collisions_refuses_to_ref(tmp_path: Path):
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    assert s.main(base + ["--adopt-collisions", "--to", "HEAD"]) == 2


def test_adopt_collisions_requires_a_prior_stage(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-collisions"]) != 0   # no stage -> refuse


def test_adopt_collisions_no_collisions_is_a_noop(tmp_path: Path):
    # A clean staged upgrade (no collisions) -> adopt records nothing.
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)              # package absent -> clean new-module adds
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    before = s.read_lockfile(target)["files"]
    assert s.main(base + ["--adopt-collisions"]) == 0
    assert s.read_lockfile(target)["files"] == before   # unchanged
