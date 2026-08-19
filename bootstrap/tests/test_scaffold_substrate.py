"""0B.4 — activate the 0A contracts on the LANDED launcher+engine substrate.

The 0A guards were proven against synthetic fixtures; these prove them against
the real `bootstrap/scaffold.py` launcher and the `bootstrap/_scaffold/` engine:

* **Canonical identity:** `bootstrap.scaffold` IS `bootstrap._scaffold`
  (one `sys.modules` entry / object per file), and the engine file is the
  canonical one.
* **Facade patch-through:** patching `bootstrap.scaffold._cairn_is_git`
  reaches the engine's own namespace (the `test_upgrade.py:509` pattern).
* **Executable topology:** the launcher installs correctly when invoked as
  a script from an unrelated cwd (`/tmp`), not just from the Cairn root.
* **Fail-closed against import hijack:** a decoy `bootstrap/_scaffold/` on
  `PYTHONPATH` does NOT become the loaded engine — the launcher loads
  file-relative, so the canonical engine stays the real one.
* **Scan completeness:** the real engine package is now in the release
  Bandit scan set.
* **Import-purity:** importing the trust anchors writes no files and
  runs no CLI.

Stdlib only.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = CAIRN_ROOT / "bootstrap" / "scaffold.py"
ENGINE_INIT = CAIRN_ROOT / "bootstrap" / "_scaffold" / "__init__.py"

_TEMPLATES = CAIRN_ROOT / "templates"
pytestmark = pytest.mark.skipif(
    not _TEMPLATES.exists(), reason="Cairn templates not available"
)


def _run(args, *, cwd, env_extra=None):
    import os
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, *args], cwd=str(cwd), env=env,
        capture_output=True, text=True, check=False,
    )


# --- canonical identity + facade (in-process) ---------------------------------

def test_launcher_is_the_canonical_engine_identity():
    import bootstrap.scaffold as s  # noqa: PLC0415
    assert sys.modules["bootstrap.scaffold"] is sys.modules["bootstrap._scaffold"]
    assert s is sys.modules["bootstrap._scaffold"]
    assert Path(s.__file__) == ENGINE_INIT, "the alias must resolve to the engine file"


def test_facade_exposes_full_public_surface():
    # The facade is the engine, so the historically-imported surface is present
    # by construction. Spot-check the high-traffic symbols + the exception class.
    import bootstrap.scaffold as s  # noqa: PLC0415
    for name in ("main", "read_lockfile", "_MODULE_MAPPINGS", "_GITIGNORE_SEEDS",
                 "load_config", "ScaffoldSecurityError", "_cairn_root"):
        assert hasattr(s, name), f"facade missing {name}"


def test_facade_patch_through_reaches_engine(monkeypatch):
    """The facade IS the engine, so patching the facade mutates the
    engine's own namespace (a single object identity).

    Scope note (post scaffold-split): this guarantees facade==engine identity, NOT
    that a facade patch reaches a symbol's *internal* callers once that symbol has
    been extracted into a submodule. A symbol owned by ``bootstrap._scaffold.<m>``
    is referenced by that submodule's own functions via its own module global, so
    to influence those callers a test must patch the OWNING module (see
    ``test_upgrade.py::test_to_ref_requires_git_source``, which patches
    ``bootstrap._scaffold.upgrade._cairn_is_git``). ``_cairn_is_git`` now lives in
    the upgrade submodule; the facade still re-exports it, and patching the facade
    still mutates the engine namespace, which is what this test pins."""
    import bootstrap.scaffold as s  # noqa: PLC0415
    sentinel = object()
    monkeypatch.setattr(s, "_cairn_is_git", lambda root: sentinel)
    assert sys.modules["bootstrap._scaffold"]._cairn_is_git(CAIRN_ROOT) is sentinel


# --- scan completeness (0A.1 activated on the real package) -------------------

def test_release_scan_now_covers_launcher_and_engine():
    from bootstrap.security_check import scan_targets  # noqa: PLC0415
    targets = set(scan_targets())
    assert "bootstrap/scaffold.py" in targets, "the launcher must be scanned"
    assert "bootstrap/_scaffold/__init__.py" in targets, "the engine must be scanned (recursive)"


# --- executable topology from an unrelated cwd (subprocess) -----------------

def test_launcher_installs_from_an_unrelated_cwd(tmp_path):
    target = tmp_path / "adopter"
    target.mkdir()
    (target / "profile.yml").write_text(
        'project_name: "SubstrateTest"\ntest_command: "pytest"\npreset: solo-greenfield\n',
        encoding="utf-8",
    )
    # cwd is an unrelated dir, NOT the Cairn root -- proves the launcher anchors
    # paths from its own __file__, not the working directory.
    proc = _run(
        [str(LAUNCHER), "--config", str(target / "profile.yml"),
         "--target", str(target), "--cairn-root", str(CAIRN_ROOT),
         "--allow-dev", "--non-interactive"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, f"launcher install failed:\n{proc.stderr[-1500:]}"
    assert (target / "AGENTS.md").is_file()
    assert (target / "dev" / ".cairn" / "cairn-lock.yml").is_file()


# --- fail-closed against the import hijack (subprocess) ---------------------

def test_hostile_pythonpath_does_not_hijack_the_engine(tmp_path):
    """A decoy `bootstrap/_scaffold/` injected first on PYTHONPATH must NOT
    become the loaded engine: the launcher loads file-relative, so the canonical
    `bootstrap._scaffold` stays the real one under the Cairn root."""
    decoy = tmp_path / "attacker"
    (decoy / "bootstrap" / "_scaffold").mkdir(parents=True)
    (decoy / "bootstrap" / "_scaffold" / "__init__.py").write_text(
        "HIJACKED = True\n", encoding="utf-8"
    )
    probe = textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(CAIRN_ROOT)!r})   # Cairn after the decoy (PYTHONPATH wins first)
        import bootstrap.scaffold as s
        eng = sys.modules["bootstrap._scaffold"]
        assert not hasattr(s, "HIJACKED"), "facade was hijacked"
        assert not hasattr(eng, "HIJACKED"), "engine was hijacked"
        assert hasattr(eng, "_MODULE_MAPPINGS"), "did not load the real engine"
        assert {str(CAIRN_ROOT)!r} in eng.__file__, "engine loaded from outside the Cairn root"
        print("SAFE")
    """)
    proc = _run(["-c", probe], cwd=tmp_path,
                env_extra={"PYTHONPATH": str(decoy)})
    assert proc.returncode == 0 and "SAFE" in proc.stdout, (
        f"hostile-PYTHONPATH defense failed:\n{proc.stderr[-1500:]}"
    )


# (Direct fail-closed-on-escape is covered by the hostile-PYTHONPATH substrate
# test above and by the loader-prototype escape test in test_loader_identity.py,
# which exercise the same _verify_within_root contract the launcher uses.)


# --- import-purity of the trust anchors (subprocess) ------------------------

def test_importing_trust_anchors_writes_nothing(tmp_path):
    """Importing the anchors must define names only -- **no file writes, no CLI /
    upgrade *execution*** (no ``main`` runs, no plan/apply fires). This is the
    import-purity property the trust anchors actually guarantee."""
    probe = textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(CAIRN_ROOT)!r})
        import bootstrap.security_check
        import bootstrap.verify_integrity
        print("IMPORTED")
    """)
    proc = _run(["-c", probe], cwd=tmp_path)
    assert proc.returncode == 0 and "IMPORTED" in proc.stdout, proc.stderr[-1500:]
    # The fresh cwd must be untouched by a mere import.
    leftovers = [p.name for p in tmp_path.iterdir()]
    assert leftovers == [], f"importing the anchors wrote files: {leftovers}"


def test_trust_anchor_imports_are_owner_specific_not_runtime_isolated(tmp_path):
    """The revised claim, per Maintainer disposition.

    The trust anchors import their owned symbol from the *narrowest owning module*
    (``security_check`` -> ``_scaffold.config``; ``verify_integrity`` ->
    ``_scaffold.lockfile``) -- that establishes **ownership identity**. It does NOT
    establish a narrow *runtime loading* boundary: Python runs
    ``bootstrap._scaffold.__init__`` (the re-export facade) before any child
    import, and that facade eagerly imports every owner. So importing a trust
    anchor loads the **whole engine package** (guard + all eight modules), not just
    the requested closure.

    This test pins that AS-BUILT reality (rather than asserting a runtime isolation
    that does not exist), so a future move to a lazy facade would change it
    deliberately. The security property that matters -- import writes nothing and
    runs no CLI/upgrade -- is covered by the sibling test above; everything loaded
    here is Cairn's own Bandit-scanned Layer-4 engine code."""
    probe = textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(CAIRN_ROOT)!r})
        import bootstrap.security_check  # imports from bootstrap._scaffold.config
        loaded = sorted(
            n.split(".")[-1] for n in sys.modules
            if n.startswith("bootstrap._scaffold.")
        )
        print(",".join(loaded))
    """)
    proc = _run(["-c", probe], cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr[-1500:]
    loaded = set(proc.stdout.strip().split(","))
    # Ownership/identity is real: the owner (config) and the guard are loaded.
    assert {"_guard", "config"} <= loaded
    # Honest as-built boundary: the full engine, including the top layers, loads.
    assert {"install", "upgrade", "cli"} <= loaded, (
        "the facade no longer eager-loads the engine -- if this was made lazy, "
        "update the SR2 wording + this regression deliberately"
    )


# --- substrate Security Review regressions ----------------------------------
#
# Two of these exercise the launcher's submodule finder + failed-load cleanup, which the
# real engine cannot trigger yet (it has no submodules until Stage 1). They run a
# COPY of the production launcher over a synthetic engine tree, so the contract
# is pinned BEFORE security.py is extracted.

# The guard-installing prologue the REAL engine __init__ runs as its first action
# A fake engine must replicate it, else its submodule imports are
# unmediated -- exactly the gap the architecture closes.
_GUARD_PROLOGUE = (
    "from pathlib import Path\n"
    "from ._guard import install as _g\n"
    "_g(Path(__file__).resolve().parent, Path(__file__).resolve().parents[2])\n"
)


def _fake_engine_tree(tmp_path):
    """A throwaway fake Cairn root ``<tmp>/cairn/bootstrap/{scaffold.py(copy),
    _scaffold/{_guard.py(copy)}}`` so the production launcher loads a controllable
    engine that installs the real guard. The fake root is ``boot.parent``; put
    escape targets OUTSIDE it (e.g. under ``tmp_path`` directly). Returns the
    bootstrap dir."""
    boot = tmp_path / "cairn" / "bootstrap"
    (boot / "_scaffold").mkdir(parents=True)
    shutil.copy(LAUNCHER, boot / "scaffold.py")
    shutil.copy(ENGINE_INIT.parent / "_guard.py", boot / "_scaffold" / "_guard.py")
    return boot


def test_F1_sitecustomize_canonical_preload_is_refused(tmp_path):
    """A hostile sitecustomize that preloads `bootstrap._scaffold` before the
    launcher runs must NOT satisfy the canonical name — the REAL launcher refuses
    the cache entry whose __file__ is not the expected engine."""
    decoy = tmp_path / "attacker"
    (decoy / "bootstrap" / "_scaffold").mkdir(parents=True)
    (decoy / "bootstrap" / "_scaffold" / "__init__.py").write_text(
        'HIJACKED = True\ndef main(): print("PWNED"); return 0\n', encoding="utf-8"
    )
    (decoy / "sitecustomize.py").write_text("import bootstrap._scaffold\n", encoding="utf-8")
    proc = _run([str(LAUNCHER)], cwd=tmp_path, env_extra={"PYTHONPATH": str(decoy)})
    assert "PWNED" not in proc.stdout, "attacker main() executed -- preload bypass"
    assert proc.returncode != 0
    assert "preload hijack" in proc.stderr or "ScaffoldLoaderError" in proc.stderr


def test_F2_submodule_symlink_escape_is_refused(tmp_path):
    """A `_scaffold` submodule symlinked outside the Cairn root must be
    refused BEFORE execution (the finder verifies the real source first)."""
    boot = _fake_engine_tree(tmp_path)
    outside = tmp_path / "outside"   # sibling of the fake Cairn root (boot.parent)
    outside.mkdir()
    (outside / "security.py").write_text("PWNED = True\n", encoding="utf-8")
    (boot / "_scaffold" / "__init__.py").write_text(
        _GUARD_PROLOGUE + "from . import security\ndef main(): return 0\n", encoding="utf-8"
    )
    (boot / "_scaffold" / "security.py").symlink_to(outside / "security.py")
    probe = "import bootstrap.scaffold as s; print('LOADED', s.security.__file__)"
    proc = _run(["-c", probe], cwd=tmp_path, env_extra={"PYTHONPATH": str(boot.parent)})
    assert "LOADED" not in proc.stdout, "symlinked-out submodule executed -- escape"
    assert proc.returncode != 0
    assert "escapes the Cairn root" in proc.stderr


def test_F4_failed_load_leaves_clean_namespace_and_retry_is_clean(tmp_path):
    """An engine init that imports a child then fails must leave NO residue —
    neither the parent nor the child — and a retry must start clean."""
    boot = _fake_engine_tree(tmp_path)
    (boot / "_scaffold" / "security.py").write_text("PWNED = 1\n", encoding="utf-8")
    (boot / "_scaffold" / "__init__.py").write_text(
        _GUARD_PROLOGUE + 'from . import security\nraise RuntimeError("boom")\n',
        encoding="utf-8",
    )
    probe = textwrap.dedent("""
        import sys
        def attempt():
            try:
                import bootstrap.scaffold  # noqa: F401
            except RuntimeError:
                return "raised"
            return "no-error"
        first = attempt()
        # both the parent and the child must be gone after the failure
        residue = [k for k in sys.modules if k.startswith("bootstrap._scaffold")]
        # a retry must not reuse stale child state (still fails cleanly)
        second = attempt()
        residue2 = [k for k in sys.modules if k.startswith("bootstrap._scaffold")]
        print("FIRST", first)
        print("RESIDUE", residue)
        print("SECOND", second)
        print("RESIDUE2", residue2)
    """)
    proc = _run(["-c", probe], cwd=tmp_path, env_extra={"PYTHONPATH": str(boot.parent)})
    assert proc.returncode == 0, proc.stderr[-1500:]
    out = proc.stdout
    assert "FIRST raised" in out and "SECOND raised" in out
    assert "RESIDUE []" in out, f"failed load left residue:\n{out}"
    assert "RESIDUE2 []" in out, f"retry left residue:\n{out}"


# --- the import boundary mediates DIRECT engine child imports --------------
#
# The launcher-installed finder did not mediate `import bootstrap._scaffold.<m>`
# (no launcher in the call path) -- the route Stages 4/5 + the canonical-identity
# contract use. The boundary now lives in bootstrap/_scaffold/_guard.py, installed
# by the engine __init__ as its first action, so it runs before ANY child resolves.

def test_R1_importing_the_engine_installs_the_guard_finder():
    import bootstrap._scaffold  # noqa: F401,PLC0415
    from bootstrap._scaffold import _guard as G  # noqa: PLC0415
    assert any(isinstance(f, G.EngineFinder) for f in sys.meta_path), (
        "importing the engine must install the verifying finder"
    )


def test_R1_finder_refuses_a_symlinked_child_source(tmp_path):
    from bootstrap._scaffold import _guard as G  # noqa: PLC0415
    root = tmp_path / "root"
    engine_dir = root / "bootstrap" / "_scaffold"
    engine_dir.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "evil.py").write_text("PWNED = True\n", encoding="utf-8")
    (engine_dir / "evil.py").symlink_to(outside / "evil.py")
    finder = G.EngineFinder(engine_dir, root)
    with pytest.raises(G.ScaffoldLoaderError, match="escapes the Cairn root"):
        finder.find_spec("bootstrap._scaffold.evil")
    # a legit within-root child still resolves to a spec
    (engine_dir / "good.py").write_text("OK = 1\n", encoding="utf-8")
    spec = finder.find_spec("bootstrap._scaffold.good")
    assert spec is not None and spec.name == "bootstrap._scaffold.good"


def test_R1_guard_rejects_a_polluted_cached_child(tmp_path, monkeypatch):
    """A `bootstrap._scaffold.*` child preloaded from outside the engine dir must
    be refused -- a polluted cached namespace is not the Cairn engine."""
    import types  # noqa: PLC0415
    from bootstrap._scaffold import _guard as G  # noqa: PLC0415
    evil = types.ModuleType("bootstrap._scaffold.evilchild")
    evil.__file__ = str(tmp_path / "evil.py")            # outside the engine dir
    monkeypatch.setitem(sys.modules, "bootstrap._scaffold.evilchild", evil)
    with pytest.raises(G.ScaffoldLoaderError, match="polluted namespace"):
        G.install(ENGINE_INIT.parent, CAIRN_ROOT)


def test_R1_direct_child_symlink_escape_is_refused_end_to_end(tmp_path):
    """The reviewer's direct-import reproducer, against the real guard
    architecture: a fake engine whose __init__ installs the guard (as the real
    one does) refuses a symlinked-out child on `import bootstrap._scaffold.<m>`."""
    root = tmp_path / "cairn"
    eng = root / "bootstrap" / "_scaffold"
    eng.mkdir(parents=True)
    shutil.copy(ENGINE_INIT.parent / "_guard.py", eng / "_guard.py")
    (eng / "__init__.py").write_text(
        "from pathlib import Path\n"
        "from ._guard import install as _g\n"
        "_g(Path(__file__).resolve().parent, Path(__file__).resolve().parents[2])\n",
        encoding="utf-8",
    )
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "security.py").write_text("PWNED = True\n", encoding="utf-8")
    (eng / "security.py").symlink_to(outside / "security.py")
    # cwd=tmp_path has no bootstrap/ at its top, so the fake engine (on PYTHONPATH)
    # wins over the real repo -- a neutral cwd is essential here.
    proc = _run(["-c", "import bootstrap._scaffold.security"], cwd=tmp_path,
                env_extra={"PYTHONPATH": str(root)})
    assert proc.returncode != 0, "direct symlinked-child import was not refused"
    assert "escapes the Cairn root" in proc.stderr


# --- re-review-2: the guard's own bootstrap + an unverifiable cached child -----

def _real_engine_with_symlinked_guard(tmp_path):
    """A tree using the REAL launcher + REAL engine __init__ (which verifies
    _guard.py before importing it), but with _guard.py symlinked outside."""
    boot = tmp_path / "cairn" / "bootstrap"
    (boot / "_scaffold").mkdir(parents=True)
    shutil.copy(LAUNCHER, boot / "scaffold.py")
    shutil.copy(ENGINE_INIT, boot / "_scaffold" / "__init__.py")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "_guard.py").write_text(
        "def install(*a, **k): print('PWNED_GUARD')\n", encoding="utf-8")
    (boot / "_scaffold" / "_guard.py").symlink_to(outside / "_guard.py")
    return boot


def test_RR2_symlinked_guard_refused_via_launcher(tmp_path):
    """Finding 1: the engine __init__ verifies _guard.py before importing it, so
    a symlinked-out guard cannot execute on the launcher path."""
    boot = _real_engine_with_symlinked_guard(tmp_path)
    proc = _run([str(boot / "scaffold.py"), "--help"], cwd=tmp_path,
                env_extra={"PYTHONPATH": str(boot.parent)})
    assert "PWNED_GUARD" not in proc.stdout, "symlinked guard executed (launcher)"
    assert proc.returncode != 0
    assert "failed path verification" in proc.stderr


def test_RR2_symlinked_guard_refused_via_direct_import(tmp_path):
    """Finding 1: same defense on the direct `import bootstrap._scaffold` path."""
    boot = _real_engine_with_symlinked_guard(tmp_path)
    proc = _run(["-c", "import bootstrap._scaffold"], cwd=tmp_path,
                env_extra={"PYTHONPATH": str(boot.parent)})
    assert "PWNED_GUARD" not in proc.stdout, "symlinked guard executed (direct import)"
    assert proc.returncode != 0
    assert "failed path verification" in proc.stderr


def test_RR2_cached_child_without_file_is_rejected(monkeypatch):
    """Finding 2: a synthetic cached child with no __file__ cannot satisfy source
    verification -- it must be refused, not trusted by omission."""
    import types  # noqa: PLC0415
    from bootstrap._scaffold import _guard as G  # noqa: PLC0415
    evil = types.ModuleType("bootstrap._scaffold.evil_nofile")   # deliberately no __file__
    monkeypatch.setitem(sys.modules, "bootstrap._scaffold.evil_nofile", evil)
    with pytest.raises(G.ScaffoldLoaderError, match="no source path"):
        G.install(ENGINE_INIT.parent, CAIRN_ROOT)
