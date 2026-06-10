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

def test_occupied_unlocked_destination_is_review_only_collision(tmp_path: Path):
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

    # The collision is review-only (non-advancing); the rest add as new-module.
    assert by_dst[collide].kind == "review-only"
    assert by_dst[collide].kind not in s._ADVANCING_KINDS
    assert all(by_dst[d].kind == "new-module" for d in _PKG_DSTS if d != collide)

    # A normal --apply fails closed (the collision owes a by-hand merge); the
    # local content is never overwritten.
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) != 0
    assert (target / collide).read_text() == "# adopter-local content\n"


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

def test_module_additions_skipped_under_explicit_to_ref(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    lock = s.read_lockfile(target)
    # Any non-None to_ref: structural additions are enumerated from the running
    # engine's registry, which need not match the target ref, so they are skipped.
    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref="HEAD")
    assert [p for p in plans if p.kind == "new-module"] == []


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
