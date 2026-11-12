"""Upgrade carries module-internal file additions to already-adopted modules
(plan `2026-06-10-claude-cairn-scaffold-upgrade-module-additions`).

The classifier auto-adds new core/skills files but, before this change, never
new files belonging to a module the adopter has ALREADY adopted -- so a module
that split a single tool into a facade + a sibling package upstream (the
`lifecycle_metrics.py` -> `_lifecycle_metrics/` case) could not be consumed via
`scaffold.py upgrade`. This pins the `new-module` add path and the Codex-review
hardening: the canonical source-key namespace, expected-absence through apply,
occupied-destination collision + duplicate-destination ownership, `--to`
registry contract, and the UTF-8-text-only constraint).

Promises:
- Stage reports files newly shipped inside an already-adopted module, and
  apply installs them only at absent destinations, and never re-adds a tracked module file the adopter deleted.
- The upgrade never writes through a hardlinked lockfile, nor through links planted at the old fixed temporary names beside it.
- Applied lock records preserve each destination's canonical source key and
  verbatim flag; collisions and changed staged inputs remain fail-closed.
- New-module additions stay within the selected module and accepted text
  formats.
- `upgrade --adopt-collisions` records a kept file as a fork only under the displayed authorization for its staged bytes; changed bytes, a stale stage, a wrong authorization or a link refuse with nothing recorded.
- CHANGELOG and RULES collisions are shown, never replaced: regular-file adopters can keep a fork, adapt and restage, or start fresh; links, directories and other owners are refused.
- An explicit `--to` upgrade blocks pending module-file additions rather than adding them.
- `--adopt-module` refuses malformed or ambiguous generated module markers and leaves the files and lockfile unchanged.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_module_additions.py
"""
from __future__ import annotations

import hashlib
import sys
import os
import re
import shutil
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold.config import InstallSpec, _MODULE_MAPPINGS  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not (TEMPLATES_ROOT / "modules" / "team-gated" / "_intent").exists(),
    reason="the _intent split package is not in templates",
)

# The coordination-tiers module ships its engine as a facade + a sibling
# `_intent/` package -- the canonical split case. It was `lifecycle_metrics.py`
# -> `_lifecycle_metrics/` until the subtraction sweep retired that module;
# the capability under test is the upgrade path for module-internal additions,
# not the module that happens to exemplify it, so the fixture moved rather than
# the file being deleted with its example.
_MODULE = "coordination-tiers"
_FACADE = "tools/intent.py"
_PKG_NAMES = ("__init__", "shared", "record_io", "identity", "conflict",
              "hooks", "cli")
_PKG_DSTS = [f"tools/_intent/{n}.py" for n in _PKG_NAMES]

# Independently enumerated from the committed config mapping at c13e7bc2.
_ADOPTION_MODULES = (
    "reflections", "claim-check", "incident-trackers", "documentation-plan",
    "dual-review", "domain-agents", "legacy-agent", "dual-language-tests",
    "coordination-tiers", "security-review", "issue-capture", "model-selection",
    "testing-discipline", "doc-drift-prevention", "examples-gallery",
    "content-security", "python-security", "portable-security-sweeps",
    "api-access-security", "web-hosting-security", "architecture-review",
    "security-verification",
)


def _src_for(dst: str) -> str:
    """The canonical lockfile source key for a `_lifecycle_metrics/` dst --
    install records `f"modules/{spec.src}"` (the canonical namespace)."""
    return "modules/team-gated/_intent/" + dst.rsplit("/", 1)[1]


def _install(target: Path) -> None:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n"
        f"modules_add:\n  - {_MODULE}\n",
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


class TestLockfileWritersWriteByReplacing:
    def test_install_does_not_write_through_a_hardlink(self, tmp_path: Path):
        target = tmp_path / "target"
        target.mkdir()
        lock = target / s._LOCKFILE_REL
        lock.parent.mkdir(parents=True)
        victim = tmp_path / "victim"
        victim.write_bytes(b"junk")
        os.link(victim, lock)
        _install(target)
        assert victim.read_bytes() == b"junk"
        assert lock.stat().st_nlink == 1
        assert s.read_lockfile(target) is not None

    def test_init_lock_does_not_write_through_a_hardlink(self, tmp_path: Path):
        target = tmp_path.resolve()
        _install(target)
        lock = target / s._LOCKFILE_REL
        lock.unlink()
        profile = target / "dev/.cairn/profile.yml"
        profile.write_text(
            "project_name: Demo\ntest_command: pytest\nage: greenfield\n"
            "size: small\ncomplexity: simple\nlanguage: single\n"
            "human_team: solo\nagent_team: single\n", encoding="utf-8"
        )
        victim = tmp_path / "victim-init"
        victim.write_bytes(b"junk")
        os.link(victim, lock)
        assert s.main(["upgrade", "--target", str(target), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert victim.read_bytes() == b"junk"
        assert lock.stat().st_nlink == 1

    def test_finalize_does_not_write_through_a_hardlink(self, tmp_path: Path):
        target = tmp_path.resolve()
        _install(target)
        lock = target / s._LOCKFILE_REL
        victim = tmp_path / "victim-finalize"
        victim.write_bytes(lock.read_bytes())
        lock.unlink()
        os.link(victim, lock)
        before = victim.read_bytes()
        assert s.main(["upgrade", "--target", str(target), "--finalize",
                       "AGENTS.md", "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert victim.read_bytes() == before
        assert lock.stat().st_nlink == 1

    def test_apply_does_not_write_through_a_hardlink(self, tmp_path: Path):
        target = tmp_path.resolve()
        _install(target)
        _make_pre_split(target)
        base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
        assert s.main(base + ["--stage"]) == 0
        lock = target / s._LOCKFILE_REL
        victim = tmp_path / "victim-apply"
        victim.write_bytes(lock.read_bytes())
        lock.unlink()
        os.link(victim, lock)
        before = victim.read_bytes()
        assert s.main(base + ["--apply"]) == 0
        assert victim.read_bytes() == before
        assert lock.stat().st_nlink == 1


class TestLockCommitWritesThroughExclusiveTemporaries:
    # Declared exception (internal hook): forces os.replace to fail inside internal _commit_lock_and_caches; no public way to fail the replace.
    def test_failed_commit_removes_its_staged_files(self, tmp_path: Path, monkeypatch):
        from bootstrap._scaffold import upgrade as U
        target = tmp_path / "target"
        target.mkdir()
        _install(target)
        cache = target / "dev/.cairn/base/new-template.txt"
        cache.parent.mkdir(parents=True, exist_ok=True)

        def refuse_replace(*_args):
            raise OSError("replace refused")

        with monkeypatch.context() as mp:
            mp.setattr(os, "replace", refuse_replace)
            with pytest.raises(OSError, match="replace refused"):
                U._commit_lock_and_caches(
                    target, s.read_lockfile(target), [(cache, b"new")]
                )
        assert list(target.rglob("*.tmp")) == []
        assert not cache.exists()

    @pytest.mark.parametrize("plant", ["symlink", "hardlink"])
    def test_finalize_never_writes_through_links_at_the_old_fixed_temporary_names(
        self, tmp_path: Path, plant: str,
    ):
        target = tmp_path / "target"
        target.mkdir()
        target = target.resolve()
        _install(target)
        lock = target / s._LOCKFILE_REL
        cache = target / "dev/.cairn/base/new-template.txt"
        cache.parent.mkdir(parents=True, exist_ok=True)
        victim = tmp_path / "victim"
        victim.write_bytes(b"outside")
        old_names = [
            lock.with_name(lock.name + ".tmp"),
            cache.with_name(cache.name + ".tmp"),
        ]
        for name in old_names:
            if plant == "symlink":
                name.symlink_to(victim)
            else:
                os.link(victim, name)
        assert s.main(["upgrade", "--target", str(target), "--finalize",
                       "AGENTS.md", "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert victim.read_bytes() == b"outside"
        assert all(name.read_bytes() == b"outside" for name in old_names)
        assert s.read_lockfile(target) is not None


# ---------------------------------------------------------------------------
# canonical source-key namespace + positive add
# ---------------------------------------------------------------------------

def test_pre_split_apply_records_package_in_lockfile(tmp_path: Path, capsys):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

    def files_on_disk() -> set[str]:
        rels = {p.relative_to(target).as_posix()
                for p in target.rglob("*") if p.is_file()}
        return {r for r in rels if not r.startswith("dev/.cairn")}

    tracked_before = {r["dst"] for r in s.read_lockfile(target)["files"]}
    on_disk_before = files_on_disk()

    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    staged = capsys.readouterr().out
    assert re.search(r"new module file \(added\)\s+7:", staged)
    assert _PKG_DSTS[0] in staged
    assert s.main(base + ["--apply"]) == 0

    # On disk and recorded in the lockfile under the canonical src.
    lock = s.read_lockfile(target)
    by_dst = {r["dst"]: r for r in lock["files"]}
    for dst in _PKG_DSTS:
        assert (target / dst).exists(), f"missing on disk: {dst}"
        assert dst in by_dst, f"missing from lockfile: {dst}"
        assert by_dst[dst]["src"] == _src_for(dst)
        assert by_dst[dst]["verbatim"] is True

    # Opt-in preserved: only the adopted module's missing files came in -- no
    # file of a module the adopter never adopted was added or tracked.
    assert (set(by_dst) - tracked_before, files_on_disk() - on_disk_before) == (
        set(_PKG_DSTS), set(_PKG_DSTS))


# ---------------------------------------------------------------------------
# new-upstream only: a deliberately-deleted tracked file stays deleted
# ---------------------------------------------------------------------------

def test_upgrade_never_re_adds_a_tracked_module_file_the_adopter_deleted(tmp_path: Path):
    target = tmp_path.resolve()
    _install(target)
    # The adopter deliberately deletes tracked module files; the lockfile still
    # records them.
    for dst in _PKG_DSTS:
        (target / dst).unlink()
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    assert not any((target / dst).exists() for dst in _PKG_DSTS)
    assert s.main(base + ["--apply"]) == 0
    assert not any((target / dst).exists() for dst in _PKG_DSTS)


# ---------------------------------------------------------------------------
# occupied-destination collision is a non-advancing review-only block
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
# expected-absence protected through apply (data-loss guard); --force
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


@pytest.mark.parametrize("changed", ["planning", "inventory"])
def test_staged_module_discovery_refuses_changed_inputs(
    tmp_path: Path, changed: str,
) -> None:
    """A staged apply refuses changed discovery bytes without partial writes."""
    target = tmp_path.resolve()
    _install(target)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    lock = target / s._LOCKFILE_REL
    before = (planning.read_bytes(), inventory.read_bytes(), lock.read_bytes())
    path = planning if changed == "planning" else inventory
    path.write_bytes(path.read_bytes() + b"\nchanged after stage\n")
    changed_bytes = path.read_bytes()
    assert s.main(base + ["--apply"]) != 0
    assert planning.read_bytes() == (changed_bytes if path == planning else before[0])
    assert inventory.read_bytes() == (changed_bytes if path == inventory else before[1])
    assert lock.read_bytes() == before[2]


@pytest.mark.parametrize("board_bytes", ["lf", "crlf-bom-no-final-newline"])
def test_adoption_appends_task_preserving_exact_prefix_and_updates_inventory(
    tmp_path: Path, board_bytes: str,
) -> None:
    """First adoption appends one task and never normalizes existing board bytes."""
    target = tmp_path.resolve()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: AdoptionDiscovery\ntest_command: pytest\n"
        "preset: solo-greenfield\n", encoding="utf-8")
    assert s.main(["--config", str(cfg), "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    planning_path = target / "dev/PLANNING.md"
    original = planning_path.read_bytes()
    if board_bytes == "crlf-bom-no-final-newline":
        original = b"\xef\xbb\xbf" + original.replace(b"\n", b"\r\n").rstrip(b"\r\n")
        planning_path.write_bytes(original)
    else:
        original = original.rstrip(b"\n")
        planning_path.write_bytes(original)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    planning = planning_path.read_bytes()
    inventory = (target / "dev/modules/README.md").read_text(encoding="utf-8")
    assert planning.startswith(original)
    assert planning[len(original):].decode("utf-8").startswith(
        "\n* [ ] **dual-review**" if not original.endswith(b"\n") else
        "* [ ] **dual-review**")
    assert "module-task" not in planning.decode("utf-8")
    assert "module id=dual-review" in inventory
    lock = s.read_lockfile(target)
    assert lock is not None and "dual-review" in lock["modules"]
    assert "dev/modules/README.md" in {record["dst"] for record in lock["files"]}


@pytest.mark.parametrize("module", _ADOPTION_MODULES)
def test_each_first_adoption_appends_its_task_after_original_board(
    tmp_path: Path, module: str,
) -> None:
    assert set(_ADOPTION_MODULES) == set(_MODULE_MAPPINGS)
    target = tmp_path.resolve()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: AdoptionDiscovery\ntest_command: pytest\n"
        "python_package: src\nmodules: []\n", encoding="utf-8")
    assert s.main(["--config", str(cfg), "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    lock = s.read_lockfile(target)
    assert lock is not None and module not in lock["modules"]
    planning = target / "dev/PLANNING.md"
    original = (b"\xef\xbb\xbf" + planning.read_bytes().replace(b"\n", b"\r\n")
                .rstrip(b"\r\n") + b"\r\nHuman work kept exactly")
    planning.write_bytes(original)
    assert s.main(["upgrade", "--target", str(target), "--cairn-root",
                   str(CAIRN_ROOT), "--adopt-module", module]) == 0
    result = planning.read_bytes()
    assert result.startswith(original)
    suffix = result[len(original):]
    header = f"* [ ] **{module}**".encode()
    assert suffix.startswith(b"\n" + header)
    assert suffix.count(header) == 1
    lines = suffix.decode("utf-8").splitlines()
    assert len(lines) == 4
    assert lines[1][len(header):].strip(" \u2014")
    first_use = "  First use: "
    assert lines[2].startswith(first_use)
    action, separator, expected = lines[2][len(first_use):].partition(
        " Expected result: ")
    assert separator and action.strip() and expected.strip()
    entry = "  Entry point: `"
    assert lines[3].startswith(entry) and lines[3].endswith("`.")
    assert lines[3][len(entry):-2].strip()


def test_adoption_treats_legacy_task_markers_as_project_text(
    tmp_path: Path,
) -> None:
    """Legacy task tags do not parse, authorize selection, or block adoption."""
    target = tmp_path.resolve()
    _install(target)
    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    text = planning.read_text(encoding="utf-8")
    marker = "<!-- cairn:end onboarding-tasks -->"
    legacy = ("<!-- cairn:module-task id=retired-module -->\n"
              "* [x] My preserved work\n"
              "<!-- cairn:module-task-end id=retired-module -->\n")
    text = text.replace(marker, legacy + marker)
    planning.write_text(text, encoding="utf-8")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    prefix = planning.read_bytes()
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    assert planning.read_bytes().startswith(prefix)
    assert legacy.encode() in planning.read_bytes()


@pytest.mark.parametrize("already_recorded", [False, True], ids=["new", "recorded"])
def test_adoption_refuses_ambiguous_markers_without_writes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
    already_recorded: bool,
) -> None:
    """Malformed discovery markers refuse both adoption branches before writes."""
    target = tmp_path.resolve()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: AdoptionDiscovery\ntest_command: pytest\n"
        "preset: solo-greenfield\n", encoding="utf-8")
    assert s.main(["--config", str(cfg), "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    if already_recorded:
        assert s.main(base + ["--adopt-module", "dual-review"]) == 0

    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    lock = target / s._LOCKFILE_REL
    path = inventory
    contents = path.read_text(encoding="utf-8")
    region = "<!-- cairn:generated-modules:start -->"
    malformed = "<!-- cairn:module id=dual-review"
    assert region in contents
    path.write_text(contents.replace(region, region + "\n" + malformed, 1),
                     encoding="utf-8")
    before = tuple(item.read_bytes() for item in (planning, inventory, lock))

    assert s.main(base + ["--adopt-module", "dual-review"]) == 2
    output = capsys.readouterr()
    assert "manually" in output.out + output.err
    assert tuple(item.read_bytes() for item in (planning, inventory, lock)) == before


def test_adoption_refuses_unusable_lock_before_writes(tmp_path: Path) -> None:
    """A JSON object without usable roster/file records is not adoption authority."""
    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    lock = s.read_lockfile(target)
    assert lock is not None
    lock["files"][0].pop("dst")
    lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
    before_lock = lock_path.read_bytes()
    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    before = (planning.read_bytes(), inventory.read_bytes())
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 2
    assert lock_path.read_bytes() == before_lock
    assert (planning.read_bytes(), inventory.read_bytes()) == before


@pytest.mark.parametrize("already_recorded", [False, True])
@pytest.mark.parametrize("damage", [
    "hash-malformed", "hash-missing", "base-hash-malformed",
    "base-hash-missing", "base-cache-missing", "base-cache-invalid",
    "base-pair-missing",
])
def test_adoption_refuses_damaged_baseline_before_writes(
    tmp_path: Path, already_recorded: bool, damage: str,
) -> None:
    target = tmp_path.resolve()
    _install(target)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    if already_recorded:
        assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    lock_path = target / s._LOCKFILE_REL
    lock = s.read_lockfile(target)
    record = next(rec for rec in lock["files"] if rec["dst"] == "AGENTS.md")
    if damage == "hash-malformed":
        record["hash"] = "broken"
    elif damage == "hash-missing":
        record.pop("hash")
    elif damage == "base-hash-malformed":
        record["base_hash"] = "sha256:1234"
    elif damage == "base-hash-missing":
        record.pop("base_hash")
    elif damage == "base-cache-missing":
        record.pop("base_cache")
    elif damage == "base-cache-invalid":
        record["base_cache"] = None
    else:
        record.pop("base_cache")
        record.pop("base_hash")
    lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    before = tuple(path.read_bytes() for path in (lock_path, planning, inventory))
    assert s.main(base + ["--adopt-module", "dual-review"]) == 2
    assert tuple(path.read_bytes() for path in (lock_path, planning, inventory)) == before
    assert ("dual-review" in s.read_lockfile(target)["modules"]) == already_recorded


def test_adoption_accepts_migrated_unrecoverable_baselines(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    lock_path.unlink()
    profile = target / "dev/.cairn/profile.yml"
    profile.write_bytes((target / "profile.yml").read_bytes())
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--init-lock"]) == 0
    migrated = s.read_lockfile(target)
    assert migrated["migrated"] is True
    assert any(rec.get("unrecoverable_base") and "base_cache" not in rec
               for rec in migrated["files"])
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0


def test_adoption_accepts_legacy_verbatim_without_base_hash(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    lock = s.read_lockfile(target)
    record = next(rec for rec in lock["files"] if rec["verbatim"])
    record.pop("base_hash", None)
    lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0


@pytest.mark.parametrize("state", ["missing", "malformed"])
def test_adoption_refuses_missing_or_malformed_lock_before_writes(
    tmp_path: Path, state: str,
) -> None:
    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    if state == "missing":
        lock_path.unlink()
    else:
        lock_path.write_bytes(b"not a lock\n")
    planning = target / "dev/PLANNING.md"
    inventory = target / "dev/modules/README.md"
    before = (planning.read_bytes(), inventory.read_bytes(), lock_path.exists())
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "coordination-tiers"]) == 1
    assert (planning.read_bytes(), inventory.read_bytes(), lock_path.exists()) == before


def test_adoption_refuses_invalid_utf8_board_before_lock_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    target = tmp_path.resolve()
    _install(target)
    planning = target / "dev/PLANNING.md"
    planning.write_bytes(b"\xff\xfe")
    lock_path = target / s._LOCKFILE_REL
    before_lock = lock_path.read_bytes()
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 2
    err = capsys.readouterr().err
    assert "not UTF-8" in err and "Traceback" not in err
    assert planning.read_bytes() == b"\xff\xfe"
    assert lock_path.read_bytes() == before_lock


def test_adoption_refuses_missing_board_before_lock_success(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    _install(target)
    planning = target / "dev/PLANNING.md"
    planning.unlink()
    lock_path = target / s._LOCKFILE_REL
    before_lock = lock_path.read_bytes()
    inventory = target / "dev/modules/README.md"
    before_inventory = inventory.read_bytes()
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "coordination-tiers"]) == 2
    assert not planning.exists()
    assert lock_path.read_bytes() == before_lock
    assert inventory.read_bytes() == before_inventory


def test_repeat_adoption_does_not_restore_deleted_task_but_updates_inventory(
    tmp_path: Path,
) -> None:
    """A deleted task stays deleted while independent inventory repair continues."""
    target = tmp_path.resolve()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: AdoptionDiscovery\ntest_command: pytest\n"
        "preset: solo-greenfield\n", encoding="utf-8")
    assert s.main(["--config", str(cfg), "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    planning = target / "dev/PLANNING.md"
    planning.write_text(re.sub(
        r"(?m)^\* \[ \] \*\*dual-review\*\*.*\n"
        r"(?:  .*\n)*", "", planning.read_text(encoding="utf-8")), encoding="utf-8")
    board_before = planning.read_bytes()
    inventory = target / "dev/modules/README.md"
    inventory.write_text(re.sub(
        r"(?ms)^<!-- cairn:module id=dual-review -->.*?"
        r"^<!-- cairn:module-end id=dual-review -->\n?", "",
        inventory.read_text(encoding="utf-8")), encoding="utf-8")
    assert s.main(base + ["--adopt-module", "dual-review"]) == 0
    assert planning.read_bytes() == board_before
    assert "module id=dual-review" in inventory.read_text(encoding="utf-8")


@pytest.mark.parametrize("rel", ["dev/PLANNING.md", "dev/modules/README.md"])
@pytest.mark.parametrize("location", ["outside", "inside"])
def test_adoption_refuses_linked_discovery_destinations(
    tmp_path: Path, rel: str, location: str,
) -> None:
    """Adoption preflights both generated paths before changing any state."""
    target = tmp_path / "target"
    target.mkdir()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: AdoptionDiscovery\ntest_command: pytest\n"
        "preset: solo-greenfield\n", encoding="utf-8")
    assert s.main(["--config", str(cfg), "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
    lock_path = target / s._LOCKFILE_REL
    lock_before = lock_path.read_bytes()
    destination = target / rel
    victim = (tmp_path if location == "outside" else target) / "victim.md"
    victim_bytes = (b"outside-preserved\n" if location == "outside"
                    else destination.read_bytes())
    victim.write_bytes(victim_bytes)
    destination.unlink()
    destination.symlink_to(victim)
    module_doc = target / "dev/modules/dual-review.md"
    assert not module_doc.exists()
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--adopt-module", "dual-review"]) == 2
    assert victim.read_bytes() == victim_bytes
    assert lock_path.read_bytes() == lock_before
    assert destination.is_symlink()
    assert not module_doc.exists()


def test_adoption_refuses_linked_inventory_parent_before_writes(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    lock_before = lock_path.read_bytes()
    modules = target / "dev/modules"
    moved = target / "dev/modules-real"
    modules.rename(moved)
    modules.symlink_to(moved, target_is_directory=True)
    module_doc = moved / "dual-review.md"
    assert not module_doc.exists()
    assert s.main(["upgrade", "--target", str(target), "--cairn-root",
                   str(CAIRN_ROOT), "--adopt-module", "dual-review"]) == 2
    assert modules.is_symlink()
    assert not module_doc.exists()
    assert lock_path.read_bytes() == lock_before


@pytest.mark.parametrize("rel", ["dev/PLANNING.md", "dev/modules/README.md"])
def test_adoption_replaces_hardlinked_discovery_without_changing_victim(
    tmp_path: Path, rel: str,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    _install(target)
    destination = target / rel
    original = destination.read_bytes()
    victim = tmp_path / "victim.md"
    victim.write_bytes(original)
    destination.unlink()
    os.link(victim, destination)
    assert s.main(["upgrade", "--target", str(target), "--cairn-root",
                   str(CAIRN_ROOT), "--adopt-module", "dual-review"]) == 0
    assert victim.read_bytes() == original
    assert destination.read_bytes() != original
    assert destination.stat().st_nlink == 1


# Declared exception (internal hook): injects a failure in internal _stage_exclusive during adoption; no public way to fail the stage.
def test_adoption_failed_board_stage_does_not_record_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from bootstrap._scaffold import upgrade as U

    target = tmp_path.resolve()
    _install(target)
    lock_path = target / s._LOCKFILE_REL
    planning = target / "dev/PLANNING.md"
    lock_before, board_before = lock_path.read_bytes(), planning.read_bytes()
    stage = U._stage_exclusive

    def refuse_board(path: Path, data: bytes, root: Path) -> Path:
        if path == planning:
            raise PermissionError("board staging refused")
        return stage(path, data, root)

    monkeypatch.setattr(U, "_stage_exclusive", refuse_board)
    with pytest.raises(PermissionError, match="board staging refused"):
        s.main(["upgrade", "--target", str(target), "--cairn-root",
                str(CAIRN_ROOT), "--adopt-module", "dual-review"])
    assert planning.read_bytes() == board_before
    assert lock_path.read_bytes() == lock_before
    assert "dual-review" not in s.read_lockfile(target)["modules"]


# ---------------------------------------------------------------------------
# structural module additions are skipped under an explicit --to <ref>
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
# duplicate destination ownership across mappings is refused, not deduped
# ---------------------------------------------------------------------------

# Declared exception (internal hook): Hook: UP._MODULE_MAPPINGS patched; registry is code, no public input. Fold core-collision and absent-first-source cases in as parameters.
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


# ---------------------------------------------------------------------------
# a malformed (traversing) destination is refused before any stage write
# ---------------------------------------------------------------------------

# Declared exception (internal hook): Hook: UP._MODULE_MAPPINGS patched with traversing dst; registry is code, so no public input yields it. Asserts via public --stage.
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
        InstallSpec("team-gated/_intent/__init__.py",
                    "../../../../escaped.txt", verbatim=True)]
    monkeypatch.setattr(UP, "_MODULE_MAPPINGS", patched)

    # --stage fails closed (ScaffoldSecurityError -> CLI exit 2) and writes
    # NOTHING outside the target.
    rc = s.main(["upgrade", "--target", str(target),
                 "--cairn-root", str(CAIRN_ROOT), "--stage"])
    assert rc != 0
    assert not escaped.exists()


def test_symlinked_dev_parent_does_not_escape_at_stage(tmp_path: Path):
    # The stage ROOT mutation (rmtree/mkdir) must be containment-
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
# global destination-ownership preflight (across core / skills / modules,
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


@pytest.fixture(scope="session")
def collision_seed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    target = tmp_path_factory.mktemp("collision-seed").resolve()
    _staged_collision(target, _PKG_DSTS[1])
    return target


@pytest.fixture
def staged_collision(collision_seed: Path, tmp_path: Path) -> list[str]:
    target = tmp_path.resolve()
    shutil.copytree(collision_seed, target, symlinks=True, dirs_exist_ok=True)
    return ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]


def _adopt_args(target: Path, *collides: str) -> list[str]:
    """The operator-supplied `dst@observed@upstream` triples for the given
    adoptable collisions -- exactly what `upgrade --plan` prints for the operator
    to review and copy (the authorization channel an actor cannot rewrite)."""
    lock = s.read_lockfile(target)
    plans, _ = s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, None)
    by_dst = {fp.dst: fp for fp in plans
              if fp.kind == "new-module-blocked" and fp.src}
    out = []
    for c in collides:
        fp = by_dst[c]
        obs = s._sha256_hex((target / c).read_bytes())
        up = s._sha256_hex((fp.theirs_raw or "").encode("utf-8"))
        out.append(f"{c}@{obs}@{up}")
    return out


def _prepare_new_core_upgrade(target: Path, dst: str) -> None:
    """Remove one newly mapped root file from an install to model an older
    adopter before collision handling."""
    _install(target)
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] != dst]
    _write_lock(target, lock)
    (target / dst).unlink()


def _printed_core_adoption_triple(output: str, dst: str) -> str:
    match = re.search(re.escape(dst) + r"@[0-9a-f]{64}@[0-9a-f]{64}", output)
    assert match, f"stage did not print the ready-to-use {dst} adoption command"
    return match.group(0)


@pytest.mark.parametrize("dst,src", [
    ("CHANGELOG.md", "core/CHANGELOG.md"), ("RULES.md", "core/RULES.md")
])
def test_new_core_changelog_collision_can_be_kept_as_a_fork(
    tmp_path: Path, capsys, dst: str, src: str
):
    target = tmp_path.resolve()
    _prepare_new_core_upgrade(target, dst)
    history = b"# Existing project content\r\n\r\nKeep these bytes.\r\n"
    (target / dst).write_bytes(history)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) == 0
    output = capsys.readouterr().out
    assert dst in output and "--adopt-collisions" in output
    assert "--to" not in output
    staged = target / s._STAGING_REL / "review-only"
    assert (staged / (dst + ".ours")).read_bytes() == history
    assert (staged / (dst + ".theirs")).is_file()
    triple = _printed_core_adoption_triple(output, dst)
    assert s.main(base + ["--adopt-collisions", triple]) == 0
    assert (target / dst).read_bytes() == history

    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == dst)
    assert rec["src"] == src
    assert rec["hash"] == "sha256:" + s._sha256_hex(history)
    assert rec.get("living_state") is True
    assert rec.get("base_hash") != rec["hash"]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / dst).read_bytes() == history

    from bootstrap.verify_integrity import verify
    updated = history + "\nRelease notes: \u8bb0\u5f55.\n".encode("utf-8")
    (target / dst).write_bytes(updated)
    assert verify(target) == 0
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / dst).read_bytes() == updated


@pytest.mark.parametrize("dst,src", [
    ("CHANGELOG.md", "core/CHANGELOG.md"), ("RULES.md", "core/RULES.md")
])
def test_adapted_changelog_is_restaged_before_collision_adoption(
    tmp_path: Path, capsys, dst: str, src: str
):
    target = tmp_path.resolve()
    _prepare_new_core_upgrade(target, dst)
    changelog = target / dst
    original = b"# Existing history\n\nOld format.\n"
    changelog.write_bytes(original)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) == 0
    first_command = _printed_core_adoption_triple(capsys.readouterr().out, dst)
    adapted = (
        "# Changelog\n\n### Major changes\n\n"
        "- **Changed** — Adapted history.\n"
    ).encode("utf-8")
    changelog.write_bytes(adapted)

    # The digest from before the edit cannot authorize the new bytes.
    assert s.main(base + ["--adopt-collisions", first_command]) != 0
    assert changelog.read_bytes() == adapted
    assert not any(r["dst"] == dst
                   for r in s.read_lockfile(target)["files"])
    capsys.readouterr()

    # Re-stage binds a new command to the edited bytes the adopter reviews.
    assert s.main(base + ["--stage"]) == 0
    second_command = _printed_core_adoption_triple(capsys.readouterr().out, dst)
    assert second_command != first_command
    staged = target / s._STAGING_REL / "review-only"
    assert (staged / (dst + ".ours")).read_bytes() == adapted
    assert (staged / (dst + ".theirs")).is_file()
    assert s.main(base + ["--adopt-collisions", second_command]) == 0
    assert changelog.read_bytes() == adapted

    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == dst)
    assert rec["src"] == src
    assert rec["hash"] == "sha256:" + s._sha256_hex(adapted)
    assert rec.get("base_hash") != rec["hash"]


@pytest.mark.parametrize("dst,kind", [
    ("CHANGELOG.md", "link"), ("RULES.md", "link"),
    ("CHANGELOG.md", "directory"), ("RULES.md", "directory"),
])
def test_new_core_changelog_link_collision_cannot_be_adopted(
    tmp_path: Path, dst: str, kind: str
):
    target = tmp_path.resolve()
    _prepare_new_core_upgrade(target, dst)
    victim = tmp_path.parent / f"{tmp_path.name}-outside-history.md"
    history = b"# External history\n"
    sentinel = None
    if kind == "link":
        victim.write_bytes(history)
        (target / dst).symlink_to(victim)
    else:
        collision_dir = target / dst
        collision_dir.mkdir()
        sentinel = collision_dir / "adopter-data.txt"
        sentinel.write_bytes(history)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) != 0
    assert s.main(base + ["--adopt-collisions",
                          dst + "@" + "0" * 64 + "@" + "0" * 64]) != 0
    if kind == "link":
        assert (target / dst).is_symlink()
        assert victim.read_bytes() == history
    else:
        assert (target / dst).is_dir()
        assert sentinel is not None and sentinel.read_bytes() == history
    assert not any(r["dst"] == dst
                   for r in s.read_lockfile(target)["files"])


_DUMMY_AUTH = "x.py@" + "0" * 64 + "@" + "0" * 64


def test_adopt_collisions_records_fork_and_unblocks(tmp_path: Path):
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = _staged_collision(target, collide)
    auth = _adopt_args(target, collide)
    fork_bytes = (target / collide).read_bytes()

    # Adopt: records the on-disk fork; never writes the dst.
    assert s.main(base + ["--adopt-collisions"] + auth) == 0
    assert (target / collide).read_bytes() == fork_bytes   # fork preserved

    # Attestation closure: tracked, hash=on-disk fork, base_hash=upstream (differ).
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == collide)
    assert rec["src"] == _src_for(collide)
    assert rec["verbatim"] is True
    assert rec["hash"] == "sha256:" + s._sha256_hex(fork_bytes)
    assert rec.get("base_hash") and rec["base_hash"] != rec["hash"]

    # Re-stage -> adopted collide is a verbatim-locally-modified fork (kept), the
    # siblings add as new-module, hard block gone -> --apply completes directly.
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / collide).read_bytes() == fork_bytes
    for d in _PKG_DSTS:
        assert (target / d).exists()
    after = s.read_lockfile(target)
    assert all(any(r["dst"] == d for r in after["files"]) for d in _PKG_DSTS)


@pytest.mark.parametrize("change", [
    "none",
    "bytes-swapped",
    "bytes-swapped-and-restaged",
    "wrong-upstream-digest",
    "planted-path-instead",
    "planted-path-beside",
    "collision-appeared",
])
def test_adopt_collisions_refuses_an_authorization_that_no_longer_matches_the_stage(
        tmp_path, collision_seed, capsys, change):
    """`--stage` prints the `dst@observed@upstream` triple to authorize. Pasting
    that triple adopts the file as a fork; once the reviewed bytes, the upstream
    or the set of collisions has changed (even if the stage was redone over the
    changed bytes), the same authorization is refused and nothing is recorded."""
    target = tmp_path.resolve()
    shutil.copytree(collision_seed, target, symlinks=True, dirs_exist_ok=True)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    collide, second = _PKG_DSTS[1], _PKG_DSTS[2]
    capsys.readouterr()
    assert s.main(base + ["--stage"]) == 0
    triple = _printed_triple_for(capsys.readouterr().out, collide)
    assert triple is not None
    authorizations = [triple]
    if change == "bytes-swapped":
        (target / collide).write_text("# swapped after review\n", encoding="utf-8")
    elif change == "bytes-swapped-and-restaged":
        (target / collide).write_text("# swapped after review\n", encoding="utf-8")
        assert s.main(base + ["--stage"]) == 0
    elif change == "wrong-upstream-digest":
        dst, observed, _upstream = triple.split("@")
        authorizations = [f"{dst}@{observed}@" + "b" * 64]
    elif change.startswith("planted-path"):
        (target / "unreviewed.py").write_text("# planted, never adoptable\n",
                                              encoding="utf-8")
        planted = hashlib.sha256(b"# planted, never adoptable\n").hexdigest()
        forged = f"unreviewed.py@{planted}@" + "0" * 64
        authorizations = ([forged] if change == "planted-path-instead"
                          else [triple, forged])
    elif change == "collision-appeared":
        (target / second).write_text("# appeared after authorization\n",
                                     encoding="utf-8")

    rc = s.main(base + ["--adopt-collisions", *authorizations])

    recorded = {r["dst"] for r in s.read_lockfile(target)["files"]} & {
        collide, second, "unreviewed.py"}
    assert (rc == 0, recorded) == (
        (True, {collide}) if change == "none" else (False, set()))


@pytest.mark.parametrize("combo", [
    ["--plan", "--adopt-collisions", _DUMMY_AUTH],
    ["--stage", "--adopt-collisions", _DUMMY_AUTH],
    ["--apply", "--adopt-collisions", _DUMMY_AUTH],
    ["--adopt-collisions", _DUMMY_AUTH, "--finalize"],
    ["--plan", "--apply"],
    ["--stage", "--apply"],
])
def test_upgrade_actions_are_mutually_exclusive(tmp_path: Path, combo, staged_collision):
    # Every mixed-action invocation refuses before any mutation -- in
    # particular `--plan --adopt-collisions` (a "read-only" combo) must not adopt.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    assert s.main(base + combo) == 2
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_requires_explicit_authorization(tmp_path: Path, staged_collision):
    # The action takes >=1 explicit triple (argparse nargs="+"); bare
    # `--adopt-collisions` is rejected, never a no-arg adopt.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    with pytest.raises(SystemExit):       # argparse: expected at least one argument
        s.main(base + ["--adopt-collisions"])


# Declared exception (internal hook): forces os.replace to fail inside internal _commit_lock_and_caches; no public way to fail the replace.
def test_commit_lock_and_caches_is_atomic_on_lockfile_failure(tmp_path, monkeypatch):
    # An interrupted multi-file commit leaves the prior authority coherent --
    # the old lockfile is unchanged and no live cache was replaced.
    import os  # noqa: PLC0415
    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    target = tmp_path.resolve()
    _install(target)
    lock = s.read_lockfile(target)
    before = (target / s._LOCKFILE_REL).read_bytes()
    new_cache = target / "dev/.cairn/base/tools/_fork/x.py"   # a NEW cache path
    real_replace = os.replace

    def boom(src, dst):
        if str(dst) == str(target / s._LOCKFILE_REL):
            raise OSError("injected lockfile replace failure")
        return real_replace(src, dst)

    monkeypatch.setattr(os, "replace", boom)
    lock2 = dict(lock)
    lock2["files"] = list(lock["files"]) + [
        {"src": "modules/x/x.py", "dst": "tools/_fork/x.py", "verbatim": False,
         "hash": "sha256:" + s._sha256_hex(b"fork"), "base_hash": "sha256:00",
         "base_cache": "dev/.cairn/base/tools/_fork/x.py"}]
    with pytest.raises(OSError):
        UP._commit_lock_and_caches(target, lock2, [(new_cache, b"upstream")])
    assert (target / s._LOCKFILE_REL).read_bytes() == before


@pytest.mark.parametrize("dst,expected", [
    (_PKG_DSTS[1], "new-module-lockconflict"),
    ("RULES.md", "new-core-lockconflict"),
])
def test_lockconflict_destination_is_distinct_and_not_adoptable(
    tmp_path: Path, dst: str, expected: str
):
    # A new-upstream spec whose dst is already tracked under ANOTHER source
    # is a provenance conflict, never an adoptable fork.
    target = tmp_path.resolve()
    _install(target)
    collide = dst
    (target / collide).write_text("# adopter fork\n", encoding="utf-8")
    lock = s.read_lockfile(target)
    if collide == "RULES.md":
        rec = next(r for r in lock["files"] if r["dst"] == collide)
        rec["src"] = "modules/bogus/elsewhere.py"
    else:
        _make_pre_split(target, keep_on_disk=(collide,))
        lock = s.read_lockfile(target)
        lock["files"].append({"src": "modules/bogus/elsewhere.py", "dst": collide,
                              "verbatim": True,
                              "hash": "sha256:" + s._sha256_hex(b"x")})
    _write_lock(target, lock)

    lock = s.read_lockfile(target)
    plans = {p.dst: p for p in s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None)[0]}
    assert plans[collide].kind == expected
    assert plans[collide].kind not in s._ADVANCING_KINDS
    # Authorizing it refuses (it is not in the live adoptable set).
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    obs = s._sha256_hex((target / collide).read_bytes())
    assert s.main(base + ["--adopt-collisions", f"{collide}@{obs}@" + "0" * 64]) != 0


def test_adopt_collisions_refuses_to_ref(tmp_path: Path, staged_collision):
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    assert s.main(base + ["--adopt-collisions", _DUMMY_AUTH, "--to", "HEAD"]) == 2


def _printed_triple_for(out: str, collide: str) -> str | None:
    for tok in out.split():
        if tok.startswith(collide + "@"):
            return tok
    return None


def test_plan_points_to_stage_without_a_live_digest(tmp_path, capsys):
    # `--plan` (read-only) must NOT hand out a live-read digest -- it points the
    # operator at `--stage` (whose digest binds to the reviewed artifact).
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    _install(target)
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_text("# adopter fork\n", encoding="utf-8")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--plan"]) == 0
    out = capsys.readouterr().out
    assert "upgrade --stage" in out
    assert _printed_triple_for(out, collide) is None      # no copyable triple
