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
"""
from __future__ import annotations

import ast
import os
import stat
import sys
from pathlib import Path

import pytest

_PKG = Path(__file__).resolve().parents[1] / "_scaffold"
_GUARD_CALLS = {"_assert_safe_write", "_assert_fanout_contained"}

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
}


class TestReadRegularBytesRefusesAnythingElse:
    def test_regular_missing_link_and_hardlink(self, tmp_path):
        from bootstrap._scaffold import security as S
        plain = tmp_path / "plain"
        plain.write_bytes(b"content")
        assert S._read_regular_bytes(plain) == b"content"
        assert S._read_regular_bytes(tmp_path / "absent") is None
        link = tmp_path / "link"
        link.symlink_to(plain)
        with pytest.raises(S.ScaffoldSecurityError):
            S._read_regular_bytes(link)
        hardlink = tmp_path / "hardlink"
        os.link(plain, hardlink)
        assert S._read_regular_bytes(hardlink) == b"content"
        with pytest.raises(S.ScaffoldSecurityError):
            S._read_regular_bytes(hardlink, single_link=True)

    def test_special_files_refused_without_blocking(self, tmp_path):
        from bootstrap._scaffold import security as S
        directory = tmp_path / "directory"
        directory.mkdir()
        for path in (directory, Path("/dev/null")):
            with pytest.raises(S.ScaffoldSecurityError):
                S._read_regular_bytes(path)
        if hasattr(os, "mkfifo"):
            pipe = tmp_path / "pipe"
            os.mkfifo(pipe)
            with pytest.raises(S.ScaffoldSecurityError):
                S._read_regular_bytes(pipe)


class TestWriteByReplacing:
    def test_replace_does_not_write_through_a_hardlink(self, tmp_path):
        from bootstrap._scaffold import security as S
        victim = tmp_path / "victim"
        victim.write_bytes(b"unchanged")
        target = tmp_path / "target"
        target.mkdir()
        dst = target / "file"
        os.link(victim, dst)
        S._write_by_replacing(dst, b"new", target)
        assert victim.read_bytes() == b"unchanged"
        assert dst.read_bytes() == b"new"
        assert dst.stat().st_nlink == 1

    def test_planted_temp_is_not_removed_or_written(self, tmp_path, monkeypatch):
        from bootstrap._scaffold import security as S
        target = tmp_path / "target"
        target.mkdir()
        dst = target / "file"
        victim = tmp_path / "victim"
        victim.write_bytes(b"unchanged")
        planted = target / "file.fixed.tmp"
        os.link(victim, planted)
        monkeypatch.setattr(S.secrets, "token_hex", lambda _: "fixed")
        with pytest.raises(FileExistsError):
            S._write_by_replacing(dst, b"new", target)
        assert planted.exists()
        assert victim.read_bytes() == b"unchanged"

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

    def test_failed_replace_removes_only_its_temp(self, tmp_path, monkeypatch):
        from bootstrap._scaffold import security as S
        dst = tmp_path / "file"
        dst.write_bytes(b"old")
        def fail(*_args):
            raise OSError("replace failed")
        monkeypatch.setattr(S.os, "replace", fail)
        with pytest.raises(OSError, match="replace failed"):
            S._write_by_replacing(dst, b"new", tmp_path)
        assert dst.read_bytes() == b"old"
        assert list(tmp_path.glob("*.tmp")) == []

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


def _guard_calls_by_function() -> dict[str, set[str]]:
    """Map ``{function_name: {guard names it calls}}`` across the engine package."""
    out: dict[str, set[str]] = {}
    for py in sorted(_PKG.glob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                calls = {
                    n.func.id for n in ast.walk(node)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                }
                out.setdefault(node.name, set()).update(calls & _GUARD_CALLS)
    return out


def test_guarded_write_functions_still_call_a_containment_guard():
    found = _guard_calls_by_function()
    for fn in sorted(_GUARDED_WRITE_FUNCS):
        assert fn in found, f"SR6: guarded-write function {fn!r} not found in the engine package"
        assert found[fn], (
            f"SR6 regression: {fn!r} no longer calls a containment guard "
            f"({sorted(_GUARD_CALLS)}) -- a guarded adopter-tree write lost its guard"
        )


def test_scaffold_security_error_defined_exactly_once_in_the_leaf():
    defs: list[str] = []
    for py in sorted(_PKG.glob("*.py")):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef) and node.name == "ScaffoldSecurityError":
                defs.append(py.name)
    assert defs == ["security.py"], (
        f"ScaffoldSecurityError must be defined exactly once (security.py); found in {defs}"
    )


def test_single_scaffold_security_error_identity_across_consumers():
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # the facade (== engine)  # noqa: PLC0415

    assert engine.ScaffoldSecurityError is S.ScaffoldSecurityError
    assert sys.modules["bootstrap.scaffold"].ScaffoldSecurityError is S.ScaffoldSecurityError
    # the guards resolve to the leaf functions too
    assert engine._assert_safe_write is S._assert_safe_write
    assert engine._assert_fanout_contained is S._assert_fanout_contained


def test_containment_guard_refuses_a_symlink_escape(tmp_path):
    """The leaf still enforces: a symlinked destination is refused with the one
    ScaffoldSecurityError class."""
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    target = tmp_path / "tgt"
    target.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    trap = target / "AGENTS.md"
    trap.symlink_to(outside / "evil")
    with pytest.raises(S.ScaffoldSecurityError, match="symlinked destination"):
        S._assert_safe_write(trap, target)
    # a normal destination within target is allowed
    S._assert_safe_write(target / "ok.md", target)


def test_security_leaf_is_a_pure_stdlib_leaf():
    """The leaf imports only the stdlib -- it must not import back into the
    engine package (install/upgrade depend on it, never the reverse)."""
    from bootstrap._scaffold import security as S  # noqa: PLC0415
    tree = ast.parse(Path(S.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert not mod.startswith("bootstrap"), f"leaf imports engine module {mod!r}"
            assert node.level == 0, "leaf must not use package-relative imports"
        if isinstance(node, ast.Import):
            for a in node.names:
                assert not a.name.startswith("bootstrap"), f"leaf imports {a.name!r}"
