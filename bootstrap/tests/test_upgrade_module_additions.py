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
  apply installs them only at absent destinations.
- Applied lock records preserve each destination's canonical source key and
  verbatim flag; collisions and changed staged inputs remain fail-closed.
- New-module additions stay within the selected module and accepted text
  formats.
- `upgrade --adopt-collisions` records a kept file as a fork only under the displayed authorization for its staged bytes; changed bytes, a stale stage, a wrong authorization or a link refuse with nothing recorded.
- A CHANGELOG collision is shown, never replaced: the adopter keeps it as a fork, adapts it and restages, or starts fresh; links and other owners are refused.
- An explicit `--to` upgrade blocks pending module-file additions rather than adding them.
- `--adopt-module` refuses malformed or ambiguous generated module markers and leaves the files and lockfile unchanged.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_module_additions.py
"""
from __future__ import annotations

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

    def test_old_fixed_names_cannot_redirect_commit(self, tmp_path: Path):
        from bootstrap._scaffold.upgrade import _commit_lock_and_caches
        target = tmp_path / "target"
        target.mkdir()
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
            os.link(victim, name)
        _commit_lock_and_caches(target, s.read_lockfile(target), [(cache, b"new")])
        assert victim.read_bytes() == b"outside"
        assert cache.read_bytes() == b"new"
        assert all(name.exists() for name in old_names)
        assert s.read_lockfile(target) is not None


# ---------------------------------------------------------------------------
# canonical source-key namespace + positive add
# ---------------------------------------------------------------------------

def test_pre_split_apply_records_package_in_lockfile(tmp_path: Path, capsys):
    target = tmp_path.resolve()
    _install(target)
    _make_pre_split(target)

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


# ---------------------------------------------------------------------------
# new-upstream only: a deliberately-deleted tracked file stays deleted
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
# a malformed (traversing) destination is refused before any stage write
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


def _prepare_changelog_upgrade(target: Path) -> None:
    """Make a freshly installed target look like one from before the root
    changelog mapping existed, optionally leaving CHANGELOG.md for collision
    scenarios."""
    _install(target)
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] != "CHANGELOG.md"]
    _write_lock(target, lock)
    (target / "CHANGELOG.md").unlink()


def _printed_changelog_adoption_triple(output: str) -> str:
    match = re.search(r"CHANGELOG\.md@[0-9a-f]{64}@[0-9a-f]{64}", output)
    assert match, "stage did not print the ready-to-use changelog adoption command"
    return match.group(0)


def test_new_core_changelog_collision_can_be_kept_as_a_fork(tmp_path: Path, capsys):
    target = tmp_path.resolve()
    _prepare_changelog_upgrade(target)
    history = b"# Existing history\r\n\r\nKeep these bytes.\r\n"
    (target / "CHANGELOG.md").write_bytes(history)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) == 0
    output = capsys.readouterr().out
    assert "CHANGELOG.md" in output and "--adopt-collisions" in output
    assert "--to" not in output
    staged = target / s._STAGING_REL / "review-only"
    assert (staged / "CHANGELOG.md.ours").read_bytes() == history
    assert (staged / "CHANGELOG.md.theirs").is_file()
    triple = _printed_changelog_adoption_triple(output)
    assert s.main(base + ["--adopt-collisions", triple]) == 0
    assert (target / "CHANGELOG.md").read_bytes() == history

    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == "CHANGELOG.md")
    assert rec["src"] == "core/CHANGELOG.md"
    assert rec["hash"] == "sha256:" + s._sha256_hex(history)
    assert rec.get("living_state") is True
    assert rec.get("base_hash") != rec["hash"]
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / "CHANGELOG.md").read_bytes() == history

    from bootstrap.verify_integrity import verify
    updated = history + "\nRelease notes: \u8bb0\u5f55.\n".encode("utf-8")
    (target / "CHANGELOG.md").write_bytes(updated)
    assert verify(target) == 0
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert (target / "CHANGELOG.md").read_bytes() == updated


def test_new_core_changelog_fresh_start_preserves_separate_history(tmp_path: Path):
    target = tmp_path.resolve()
    _prepare_changelog_upgrade(target)
    history = b"# Existing history\n\nSaved before starting fresh.\n"
    (target / "CHANGELOG.md").write_bytes(history)
    saved = tmp_path.parent / f"{tmp_path.name}-saved-CHANGELOG.md"
    (target / "CHANGELOG.md").replace(saved)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert saved.read_bytes() == history
    assert "Cairn Plain Language 1.0" in (target / "CHANGELOG.md").read_text()
    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == "CHANGELOG.md")
    assert rec["src"] == "core/CHANGELOG.md"
    assert rec.get("living_state") is True


def test_adapted_changelog_is_restaged_before_collision_adoption(
    tmp_path: Path, capsys
):
    target = tmp_path.resolve()
    _prepare_changelog_upgrade(target)
    changelog = target / "CHANGELOG.md"
    original = b"# Existing history\n\nOld format.\n"
    changelog.write_bytes(original)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) == 0
    first_command = _printed_changelog_adoption_triple(capsys.readouterr().out)
    adapted = (
        "# Changelog\n\n### Major changes\n\n"
        "- **Changed** — Adapted history.\n"
    ).encode("utf-8")
    changelog.write_bytes(adapted)

    # The digest from before the edit cannot authorize the new bytes.
    assert s.main(base + ["--adopt-collisions", first_command]) != 0
    assert changelog.read_bytes() == adapted
    assert not any(r["dst"] == "CHANGELOG.md"
                   for r in s.read_lockfile(target)["files"])
    capsys.readouterr()

    # Re-stage binds a new command to the edited bytes the adopter reviews.
    assert s.main(base + ["--stage"]) == 0
    second_command = _printed_changelog_adoption_triple(capsys.readouterr().out)
    assert second_command != first_command
    staged = target / s._STAGING_REL / "review-only"
    assert (staged / "CHANGELOG.md.ours").read_bytes() == adapted
    assert (staged / "CHANGELOG.md.theirs").is_file()
    assert s.main(base + ["--adopt-collisions", second_command]) == 0
    assert changelog.read_bytes() == adapted

    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == "CHANGELOG.md")
    assert rec["hash"] == "sha256:" + s._sha256_hex(adapted)
    assert rec.get("base_hash") != rec["hash"]


def test_new_core_changelog_refuses_another_source_owner(tmp_path: Path):
    target = tmp_path.resolve()
    _prepare_changelog_upgrade(target)
    history = b"# Existing history\n"
    (target / "CHANGELOG.md").write_bytes(history)
    lock = s.read_lockfile(target)
    # Make the existing file appear owned under a different core source.
    agent_rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
    agent_rec["dst"] = "CHANGELOG.md"
    _write_lock(target, lock)
    plans, _ = s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, None)
    conflicts = [p for p in plans if p.dst == "CHANGELOG.md"
                 and p.kind == "new-core-lockconflict"]
    assert conflicts, "another lockfile source must block the new changelog"
    assert (target / "CHANGELOG.md").read_bytes() == history


def test_new_core_changelog_link_collision_cannot_be_adopted(tmp_path: Path):
    target = tmp_path.resolve()
    _prepare_changelog_upgrade(target)
    victim = tmp_path.parent / f"{tmp_path.name}-outside-history.md"
    history = b"# External history\n"
    victim.write_bytes(history)
    (target / "CHANGELOG.md").symlink_to(victim)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

    assert s.main(base + ["--stage"]) != 0
    assert s.main(base + ["--adopt-collisions",
                          "CHANGELOG.md@" + "0" * 64 + "@" + "0" * 64]) != 0
    assert (target / "CHANGELOG.md").is_symlink()
    assert victim.read_bytes() == history
    assert not any(r["dst"] == "CHANGELOG.md"
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


def test_adopt_collisions_verbatim_fork_survives_two_upstream_versions(tmp_path, staged_collision):
    # A verbatim fork must record base_hash=upstream, NOT only its own hash,
    # or a later upstream change classifies `update` and overwrites the fork.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    assert s.main(base + ["--adopt-collisions"] + _adopt_args(target, collide)) == 0

    import bootstrap._scaffold.upgrade as UP  # noqa: PLC0415
    fork_bytes = (target / collide).read_bytes()
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == collide)
    later_upstream = b"# a brand-new upstream launcher v2\n"
    assert UP.classify_verbatim(
        fork_bytes, rec["base_hash"], later_upstream) == "locally-modified"
    # Proof of the closed bug: with only `hash` (=the fork) it would be `update`.
    assert UP.classify_verbatim(
        fork_bytes, rec["hash"], later_upstream) == "update"


def test_adopt_collisions_works_without_a_prior_stage(tmp_path: Path):
    # Authorization is the operator's typed digests (from `--plan`), so adoption
    # does not depend on the mutable stage existing at all.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    _install(target)
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_text("# adopter fork\n", encoding="utf-8")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    auth = _adopt_args(target, collide)            # what `--plan` would print
    assert s.main(base + ["--adopt-collisions"] + auth) == 0
    assert any(r["dst"] == collide for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_refuses_changed_bytes_despite_rewritten_stage(tmp_path, staged_collision):
    # Remaining-P1: authorization is the operator's typed digest, NOT the mutable
    # stage. An actor who changes the candidate bytes AND rewrites the stage
    # metadata still cannot get the changed bytes adopted -- the operator's
    # reviewed digest no longer matches the on-disk bytes.
    import json  # noqa: PLC0415
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    auth = _adopt_args(target, collide)            # the operator's REVIEWED triple
    # An actor swaps the bytes after review and rewrites the (now-irrelevant) stage.
    (target / collide).write_text("# swapped by an actor after review\n",
                                  encoding="utf-8")
    meta_path = target / s._STAGING_REL / s._STAGE_META
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        meta["collision_adopt"] = {}      # whatever an attacker writes is ignored
        meta_path.write_text(json.dumps(meta), encoding="utf-8")

    assert s.main(base + ["--adopt-collisions"] + auth) != 0
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_refuses_a_wrong_upstream_authorization(tmp_path: Path, staged_collision):
    # Remaining-P1 (upstream variant): the upstream merge base is bound to the
    # operator's typed upstream digest; if it does not match the live upstream
    # (a swapped source), refuse.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    good = _adopt_args(target, collide)[0]
    dst, obs, _up = good.split("@")
    bad = f"{dst}@{obs}@" + "b" * 64            # correct bytes, wrong upstream
    assert s.main(base + ["--adopt-collisions", bad]) != 0
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_records_only_the_authorized_bytes(tmp_path: Path, staged_collision):
    # The destination is read once and that buffer is recorded, so the lock
    # hash equals the operator's authorized observed digest.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    auth = _adopt_args(target, collide)
    _dst, obs, _up = auth[0].split("@")
    assert s.main(base + ["--adopt-collisions"] + auth) == 0
    rec = next(r for r in s.read_lockfile(target)["files"] if r["dst"] == collide)
    assert rec["hash"] == "sha256:" + obs


def test_adopt_collisions_refuses_authorizing_a_nonadoptable_file(tmp_path, staged_collision):
    # The operator cannot authorize a path that is not a live
    # adoptable collision -- eligibility is recomputed from _MODULE_MAPPINGS, so
    # an arbitrary planted file refuses (exact-set disagreement).
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    base = staged_collision
    planted = "unreviewed.py"
    (target / planted).write_text("# planted, never adoptable\n", encoding="utf-8")
    obs = s._sha256_hex((target / planted).read_bytes())
    forged = f"{planted}@{obs}@" + "0" * 64
    assert s.main(base + ["--adopt-collisions", forged]) != 0
    assert not any(r["dst"] == planted for r in s.read_lockfile(target)["files"])


def test_adopt_collisions_refuses_when_a_collision_appeared_after_authorization(tmp_path, staged_collision):
    # A collision appearing after the operator authorized makes the authorized
    # set disagree with the live adoptable set -> refuse; NOTHING adopted.
    target = tmp_path.resolve()
    c1, c2 = _PKG_DSTS[1], _PKG_DSTS[2]
    base = staged_collision
    auth = _adopt_args(target, c1)              # only c1 authorized
    (target / c2).write_text("# appeared after authorization\n", encoding="utf-8")
    assert s.main(base + ["--adopt-collisions"] + auth) != 0
    assert not any(r["dst"] in (c1, c2) for r in s.read_lockfile(target)["files"])


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


def test_lockconflict_destination_is_distinct_and_not_adoptable(tmp_path: Path):
    # A new-upstream spec whose dst is already tracked under ANOTHER source
    # is a provenance conflict, never an adoptable fork.
    target = tmp_path.resolve()
    _install(target)
    collide = _PKG_DSTS[1]
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_text("# adopter fork\n", encoding="utf-8")
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


def test_stage_prints_paste_ready_adopt_authorization(tmp_path, capsys):
    # UX + binding: `--stage` prints the exact `--adopt-collisions dst@obs@up`
    # the operator copies, with the observed digest minted from the `.ours`
    # review artifact (the reviewed bytes).
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    _install(target)
    _make_pre_split(target, keep_on_disk=(collide,))
    reviewed = b"# the bytes i review\n"
    (target / collide).write_bytes(reviewed)
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    out = capsys.readouterr().out
    triple = _printed_triple_for(out, collide)
    assert triple is not None and "--adopt-collisions" in out
    _dst, obs, _up = triple.split("@")
    assert obs == s._sha256_hex(reviewed)          # bound to the reviewed bytes
    # And the printed triple adopts cleanly (the dst is unchanged).
    assert s.main(base + ["--adopt-collisions", triple]) == 0


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


def test_stage_authorization_binds_to_reviewed_bytes_not_a_live_change(tmp_path, capsys):
    # The --stage authorization is minted from the exact
    # `.ours` review buffer, NOT a later live read. An actor who swaps the live
    # destination AFTER staging cannot get the changed bytes adopted with the
    # printed (reviewed-byte) triple.
    target = tmp_path.resolve()
    collide = _PKG_DSTS[1]
    _install(target)
    _make_pre_split(target, keep_on_disk=(collide,))
    (target / collide).write_bytes(b"# reviewed bytes\n")
    base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]
    assert s.main(base + ["--stage"]) == 0
    triple = _printed_triple_for(capsys.readouterr().out, collide)
    assert triple is not None
    # An actor swaps the live destination after the review pair was written.
    (target / collide).write_bytes(b"# swapped by an actor after staging\n")
    assert s.main(base + ["--adopt-collisions", triple]) != 0
    assert not any(r["dst"] == collide for r in s.read_lockfile(target)["files"])
