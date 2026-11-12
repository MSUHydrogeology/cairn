"""Stage 1 — the extracted containment leaf (`bootstrap/_scaffold/security.py`).

Two contracts:

* **Guard-routing regression** — every guarded adopter-tree write function still routes its
  destination through a containment guard, so an extraction stage cannot silently
  drop a guard.  The pinned set is Class A of the engine's mutation
  inventory, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`.
* **Single identity** — `ScaffoldSecurityError` is defined exactly once
  (in the leaf) and every consumer (engine, facade) resolves to that one class;
  the two guards likewise resolve to the leaf functions.

Stdlib only.

Promises:
- Unsafe or escaping adopter-tree writes are refused before outside bytes change.
- Public guard failures raise the scaffold facade's exported
  ``ScaffoldSecurityError``.
- Safe writes leave no operation-owned temporary behind; failed writes clean up
  only a temporary still owned by that operation.
"""
from __future__ import annotations

import ast
import os
import stat
import sys
from pathlib import Path

import pytest

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_GUARD_CALLS = {
    "_assert_safe_write", "_assert_fanout_contained", "_assert_git_binding_path"
}

#: Class A of `bootstrap/_scaffold/SECURITY_MUTATIONS.md`: functions that
#: perform GUARDED adopter-tree writes.
#: Each must call a containment guard on its destination. Pinned so a later
#: extraction that relocates one without its guard fails this test.
_GUARDED_WRITE_FUNCS = {
    "_stage_exclusive",
    "_install_one",
    "write_local_env",
    "install_onboarding",
    "write_install_lockfile",
    "_emit_skill_copy_fallback",
    "fan_out_skills",
    "_cmd_adopt_module",
    "_apply_upgrade",
    "_write_stage",
    # Module-merge destinations are
    # module-template-controlled, so this write must be guarded too.
    "merge_module_into_slot",
    # Adopt-as-fork: the collision-adoption write
    # path + the shared guarded/atomic lock-and-cache committer.
    "_cmd_adopt_collisions",
    "_commit_lock_and_caches",
    # The fixed path `<target>/.gitignore` is not safe by construction: a
    # checkout can make it a link to a file outside the tree.
    "seed_gitignore",
    "capture_model_selection_mapping",
    # The dev/ tree is made with `mkdir(parents=True)`, which follows a linked
    # `dev/` (or any linked folder below it) to the far end.
    "create_dev_tree",
    # The only engine deletion of a project file: it checks containment, then
    # removes by name through folder handles opened without following links.
    "_remove_unchanged_file",
    # The step that calls it: it also writes the lockfile, so it guards that path
    # itself before the shared committer does.
    "_cmd_remove_retired",
}


class TestReadRegularBytesRefusesAnythingElse:
    # Declared exception (internal hook): monkeypatches Path.is_symlink to swap the candidate between probe and open; a probe-open race cannot be produced through the public writer.
    def test_link_swapped_between_probe_and_open_is_refused(
        self, tmp_path, monkeypatch
    ):
        from bootstrap._scaffold import security as S
        candidate = tmp_path / "candidate"
        candidate.write_bytes(b"initial")
        victim = tmp_path / "victim"
        victim.write_bytes(b"outside")
        real_probe = Path.is_symlink

        def swap_on_probe(path):
            if path == candidate:
                candidate.unlink()
                candidate.symlink_to(victim)
                return False
            return real_probe(path)

        with monkeypatch.context() as mp:
            mp.setattr(Path, "is_symlink", swap_on_probe)
            with pytest.raises(S.ScaffoldSecurityError):
                S._read_regular_bytes(candidate)
        assert victim.read_bytes() == b"outside"


    def test_special_files_refused_without_blocking(self, tmp_path):
        from bootstrap._scaffold import security as S
        directory = tmp_path / "directory"
        directory.mkdir()
        with pytest.raises(S.ScaffoldSecurityError):
            S._read_regular_bytes(directory)

    @pytest.mark.skipif(os.name != "posix", reason="POSIX device files")
    def test_posix_special_files_refused_without_blocking(self, tmp_path):
        from bootstrap._scaffold import security as S
        with pytest.raises(S.ScaffoldSecurityError):
            S._read_regular_bytes(Path("/dev/null"))
        if hasattr(os, "mkfifo"):
            pipe = tmp_path / "pipe"
            os.mkfifo(pipe)
            with pytest.raises(S.ScaffoldSecurityError):
                S._read_regular_bytes(pipe)


class TestWriteByReplacing:


    @pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits")
    def test_permissions_strip_execute_and_special_bits(self, tmp_path):
        from bootstrap._scaffold import security as S
        dst = tmp_path / "file"
        dst.write_bytes(b"old")
        dst.chmod(0o4755)
        S._write_by_replacing(dst, b"new", tmp_path)
        assert stat.S_IMODE(dst.stat().st_mode) == 0o644
        dst.chmod(0o640)
        S._write_by_replacing(dst, b"again", tmp_path)
        assert stat.S_IMODE(dst.stat().st_mode) == 0o640


    # Declared exception (internal hook): monkeypatches os.fchmod and secrets.token_hex to swap the staged temp to a victim file; no public route swaps a temp mid-write.
    def test_swapped_temp_cannot_change_victim_mode(self, tmp_path, monkeypatch):
        from bootstrap._scaffold import security as S
        if not hasattr(os, "fchmod"):
            pytest.skip("descriptor mode setting unavailable")
        target = tmp_path / "target"
        target.mkdir()
        dst = target / "file"
        dst.write_bytes(b"old")
        dst.chmod(0o640)
        victim = tmp_path / "victim"
        victim.write_bytes(b"outside")
        victim.chmod(0o600)
        monkeypatch.setattr(S.secrets, "token_hex", lambda _: "fixed")
        staged = target / "file.fixed.tmp"
        real_fchmod = S.os.fchmod

        def swap_then_chmod(fd, mode):
            staged.unlink()
            staged.symlink_to(victim)
            real_fchmod(fd, mode)

        monkeypatch.setattr(S.os, "fchmod", swap_then_chmod)
        with pytest.raises(S.ScaffoldSecurityError):
            S._write_by_replacing(dst, b"new", target)
        assert dst.read_bytes() == b"old"
        assert victim.read_bytes() == b"outside"
        assert stat.S_IMODE(victim.stat().st_mode) == 0o600
        assert staged.is_symlink()


def test_public_seed_gitignore_refuses_outside_symlink_with_facade_exception(
        tmp_path):
    from bootstrap import scaffold

    target = tmp_path / "target"
    target.mkdir()
    outside = tmp_path / "outside.gitignore"
    outside.write_bytes(b"outside bytes\n")
    before = outside.read_bytes()
    gitignore = target / ".gitignore"
    gitignore.symlink_to(outside)

    with pytest.raises(scaffold.ScaffoldSecurityError,
                       match="symlinked destination"):
        scaffold.seed_gitignore(target, ("dev/intents.jsonl",))

    assert outside.read_bytes() == before
    assert gitignore.is_symlink()


@pytest.mark.parametrize("failure", ["open", "fstat", "read"])
def test_public_seed_gitignore_normalizes_read_errors(
        tmp_path, monkeypatch, failure):
    from bootstrap import scaffold
    from bootstrap._scaffold import security as S

    target = tmp_path / "target"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.write_bytes(b"keep me\n")
    real_open, real_fstat, real_fdopen = S.os.open, S.os.fstat, S.os.fdopen
    opened: set[int] = set()

    def open_file(path, flags, *args, **kwargs):
        if Path(path) == gitignore and flags & os.O_ACCMODE == os.O_RDONLY and failure == "open":
            raise OSError("injected read open failure")
        fd = real_open(path, flags, *args, **kwargs)
        if Path(path) == gitignore and flags & os.O_ACCMODE == os.O_RDONLY:
            opened.add(fd)
        return fd

    def fstat(fd):
        if failure == "fstat" and fd in opened:
            raise OSError("injected read fstat failure")
        return real_fstat(fd)

    class FailingReader:
        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

        def read(self):
            raise OSError("injected stream read failure")

    def fdopen(fd, mode, *args, **kwargs):
        if failure == "read" and fd in opened and mode == "rb":
            return FailingReader()
        return real_fdopen(fd, mode, *args, **kwargs)

    monkeypatch.setattr(S.os, "open", open_file)
    monkeypatch.setattr(S.os, "fstat", fstat)
    monkeypatch.setattr(S.os, "fdopen", fdopen)
    with pytest.raises(scaffold.ScaffoldSecurityError, match="non-regular"):
        scaffold.seed_gitignore(target, ("dev/intents.jsonl",))
    assert gitignore.read_bytes() == b"keep me\n"
    assert list(target.glob("*.tmp")) == []


@pytest.mark.parametrize("failure", ["write", "fchmod"])
def test_public_seed_gitignore_staging_failure_preserves_destination_and_cleans_owned_temp(
        tmp_path, monkeypatch, failure):
    from bootstrap import scaffold
    from bootstrap._scaffold import security as S

    target = tmp_path / "target"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.write_bytes(b"keep me\n")
    real_fdopen, real_fchmod = S.os.fdopen, getattr(S.os, "fchmod", None)

    class FailingWriter:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self.stream.close()

        def write(self, _data):
            raise OSError("injected staging write failure")

        def flush(self):
            self.stream.flush()

    if failure == "write":
        def fdopen(fd, mode, *args, **kwargs):
            stream = real_fdopen(fd, mode, *args, **kwargs)
            return FailingWriter(stream) if mode == "wb" else stream
        monkeypatch.setattr(S.os, "fdopen", fdopen)
    elif real_fchmod is not None:
        monkeypatch.setattr(S.os, "fchmod", lambda *_: (_ for _ in ()).throw(
            OSError("injected staging mode failure")))
    else:
        pytest.skip("descriptor mode setting unavailable")

    with pytest.raises(OSError, match="injected staging"):
        scaffold.seed_gitignore(target, ("dev/intents.jsonl",))
    assert gitignore.read_bytes() == b"keep me\n"
    assert list(target.glob("*.tmp")) == []


@pytest.mark.skipif(os.name != "posix", reason="POSIX hard links and descriptor mode setting")
def test_public_seed_gitignore_rejects_hardlink_swap_during_staging_without_deleting_unowned_name(
        tmp_path, monkeypatch):
    from bootstrap import scaffold
    from bootstrap._scaffold import security as S

    target = tmp_path / "target"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.write_bytes(b"original\n")
    victim = tmp_path / "victim"
    victim.write_bytes(b"outside\n")
    victim.chmod(0o600)
    real_fchmod = S.os.fchmod
    staged_names: list[Path] = []

    def swap_then_chmod(fd, mode):
        staged = next(target.glob("*.tmp"))
        staged_names.append(staged)
        staged.unlink()
        os.link(victim, staged)
        real_fchmod(fd, mode)

    monkeypatch.setattr(S.os, "fchmod", swap_then_chmod)
    with pytest.raises(scaffold.ScaffoldSecurityError, match="staged file changed"):
        scaffold.seed_gitignore(target, ("dev/intents.jsonl",))
    assert staged_names and staged_names[0].is_file()
    assert gitignore.read_bytes() == b"original\n"
    assert victim.read_bytes() == b"outside\n"
    assert stat.S_IMODE(victim.stat().st_mode) == 0o600


# Declared exception (internal hook): monkeypatches the private _assert_safe_write to hardlink-swap the staged file after its snapshot; no public route creates that race.
def test_public_seed_gitignore_rejects_hardlink_swap_after_staged_identity_snapshot(
        tmp_path, monkeypatch):
    from bootstrap import scaffold
    from bootstrap._scaffold import security as S

    target = tmp_path / "target"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.write_bytes(b"original\n")
    victim = tmp_path / "victim"
    victim.write_bytes(b"outside\n")
    real_guard = S._assert_safe_write
    staged_names: list[Path] = []
    swapped = False

    def swap_after_snapshot(dst, root):
        nonlocal swapped
        if dst == gitignore and not swapped:
            staged = next(target.glob("*.tmp"), None)
            if staged is not None:
                staged_names.append(staged)
                staged.unlink()
                os.link(victim, staged)
                swapped = True
        return real_guard(dst, root)

    monkeypatch.setattr(S, "_assert_safe_write", swap_after_snapshot)
    with pytest.raises(scaffold.ScaffoldSecurityError, match="staged file changed"):
        scaffold.seed_gitignore(target, ("dev/intents.jsonl",))
    assert swapped and staged_names[0].is_file()
    assert gitignore.read_bytes() == b"original\n"
    assert victim.read_bytes() == b"outside\n"
