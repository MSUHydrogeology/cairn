"""Tests for the doc-drift-prevention tooling (Cairn v0.2 foldback).

Component D ships two stack-neutral, stdlib-only scripts under the
team-gated ``doc-drift-prevention`` module: ``link_check.py`` (the link /
anchor half) and ``sync_doc_snippets.py`` (the snippet half). The claim
half is intentionally *not* shipped here -- the default-on ``claim-check``
module already installs ``claim_check.py`` and the doc-drift gate composes
with it.

Covered:

* **install-path** -- both scripts land verbatim in ``scripts/`` under the
  module (1:many); the ``_MODULE_MAPPINGS`` entry is right.
* **link_check behavioral fixtures** -- relative file links,
  same-file / cross-file anchors, missing file, missing anchor, and the
  external-link default (ignored unless opted in).
* **sync_doc_snippets behavioral fixtures** -- clean check,
  drifted check (exit 1), ``--sync`` rewrites only the doc (not the
  source), and the path-safety contract (``..`` / absolute rejected,
  missing region a crisp error).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import importlib.util
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"

sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import _MODULE_MAPPINGS, main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


link_check = _load("dd_link_check", _TEAM_GATED / "link_check.py")
snippets = _load("dd_sync_doc_snippets", _TEAM_GATED / "sync_doc_snippets.py")


def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: DriftTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


def _commit_tree(root: Path) -> None:
    git = shutil.which("git")
    assert git is not None
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@example.invalid",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@example.invalid",
    })
    subprocess.run([git, "-C", str(root), "init", "-q"], env=env, check=True)
    subprocess.run([git, "-C", str(root), "add", "-A"], env=env, check=True)
    subprocess.run([git, "-C", str(root), "commit", "-qm", "fixtures"],
                   env=env, check=True)


_BOUND_CALLERS = (
    "scripts/link_check.py",
    "templates/modules/team-gated/link_check.py",
    "scripts/sync_doc_snippets.py",
    "templates/modules/team-gated/sync_doc_snippets.py",
)


def _literal_wildcard_helper(helper_bytes: bytes) -> bytes:
    source = helper_bytes.decode("utf-8")
    old = 'result = [snapshot.resolved, "--no-pager", "-C", target, *overrides]'
    new = ('result = [snapshot.resolved, "--literal-pathspecs", "--no-pager", '
           '"-C", target, *overrides]')
    source, count = source.replace(old, new), source.count(old)
    assert count == 1, "the blanket-literal argv mutation must have one target"
    return source.encode("utf-8")


def _mutate_markdown_discovery(caller: Path) -> None:
    source = caller.read_text(encoding="utf-8")
    old = '("ls-files", "-z", "--cached", "--stage")'
    new = '("ls-files", "-z", "--cached", "--stage", "*.md")'
    source, count = source.replace(old, new), source.count(old)
    assert count == 1, "the tracked-Markdown mutation must have one target"
    caller.write_text(source, encoding="utf-8")


def _bound_cli_tree(base: Path, rel: str, helper_bytes: bytes, *,
                    literal_wildcard: bool = False) -> tuple[Path, Path]:
    """Make one delivery-shaped copy and plant a positively observable helper."""
    delivery = base / "delivery"
    caller = delivery / rel
    caller.parent.mkdir(parents=True)
    shutil.copyfile(CAIRN_ROOT / rel, caller)
    tools = delivery / "tools"
    tools.mkdir()
    helper = tools / "git_read.py"
    if literal_wildcard:
        helper_bytes = _literal_wildcard_helper(helper_bytes)
    helper.write_bytes(helper_bytes)
    if literal_wildcard:
        _mutate_markdown_discovery(caller)
    pin = hashlib.sha256(helper_bytes).hexdigest()
    source = caller.read_text(encoding="utf-8")
    source, count = re.subn(
        r'(?m)^_GIT_READ_SHA256 = "[0-9a-f]{64}"$',
        f'_GIT_READ_SHA256 = "{pin}"', source, count=1,
    )
    assert count == 1, f"{rel} lacks its single fixed helper pin"
    caller.write_text(source, encoding="utf-8")
    return caller, helper


def _run_bound_cli(caller: Path, cwd: Path, marker: Path, *, cached=False):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key != "PYTHONPATH"}
    env["CAIRN_TEST_HELPER_MARKER"] = str(marker)
    if not cached:
        return subprocess.run(
            [sys.executable, str(caller), "--help"], cwd=cwd, env=env,
            text=True, capture_output=True, timeout=30,
        )
    script = (
        "import runpy,sys,types; "
        "sys.modules['_cairn_verified_git_read']=types.ModuleType('decoy'); "
        f"sys.argv=[{str(caller)!r},'--help']; "
        f"runpy.run_path({str(caller)!r},run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-c", script], cwd=cwd, env=env,
        text=True, capture_output=True, timeout=30,
    )


def _marked_helper() -> bytes:
    helper = (CAIRN_ROOT / "tools" / "git_read.py").read_bytes()
    return helper + (
        b"\nimport os as _cairn_test_os\n"
        b"from pathlib import Path as _cairn_test_Path\n"
        b"_cairn_test_Path(_cairn_test_os.environ['CAIRN_TEST_HELPER_MARKER'])"
        b".write_text('trusted-helper-ran', encoding='utf-8')\n"
    )


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_module_ships_both_tools_verbatim(self) -> None:
        specs = _MODULE_MAPPINGS["doc-drift-prevention"]
        dsts = {s.dst: s for s in specs}
        assert "dev/modules/doc-drift-prevention.md" in dsts
        assert dsts["scripts/link_check.py"].verbatim is True
        assert dsts["scripts/sync_doc_snippets.py"].verbatim is True
        # The claim half is NOT bundled here (composed from claim-check).
        assert "scripts/claim_check.py" not in dsts

    def test_tools_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["doc-drift-prevention"]) == 0
        for name in ("link_check.py", "sync_doc_snippets.py"):
            installed = tmp_path / "scripts" / name
            assert installed.is_file(), f"{name} not installed"
            assert installed.read_bytes() == (_TEAM_GATED / name).read_bytes(), (
                f"{name} differs from template -- not verbatim"
            )
        assert (tmp_path / "dev" / "modules"
                / "doc-drift-prevention.md").is_file()


class TestGitReadPhysicalBindings:
    @pytest.mark.parametrize("rel", _BOUND_CALLERS)
    def test_real_cli_loads_its_physically_pinned_helper_before_help(
            self, rel: str, tmp_path: Path) -> None:
        caller, _helper = _bound_cli_tree(tmp_path, rel, _marked_helper())
        cwd = tmp_path / "outside-cwd"
        cwd.mkdir()
        decoy = cwd / "tools" / "git_read.py"
        decoy.parent.mkdir()
        decoy.write_text(
            "from pathlib import Path\n"
            f"Path({str(tmp_path / 'cwd-marker')!r}).write_text('decoy')\n",
            encoding="utf-8",
        )
        marker = tmp_path / "helper-marker"
        result = _run_bound_cli(caller, cwd, marker)
        assert result.returncode == 0, result.stderr
        assert marker.read_text(encoding="utf-8") == "trusted-helper-ran"
        assert not (tmp_path / "cwd-marker").exists()

    @pytest.mark.parametrize("rel", _BOUND_CALLERS)
    @pytest.mark.parametrize(
        "mutation", ("missing", "tampered", "oversized", "leaf-link",
                     "parent-link", "wrong-pin", "cached-module"),
    )
    def test_each_delivery_member_refuses_separate_binding_mutations(
            self, rel: str, mutation: str, tmp_path: Path) -> None:
        caller, helper = _bound_cli_tree(tmp_path, rel, _marked_helper())
        marker = tmp_path / "helper-marker"
        outside = tmp_path / "outside"
        outside.mkdir()
        if mutation == "missing":
            helper.unlink()
        elif mutation == "tampered":
            helper.write_bytes(helper.read_bytes() + b"\n# changed bytes\n")
        elif mutation == "oversized":
            helper.write_bytes(helper.read_bytes() + b"x" * (256 * 1024 + 1))
        elif mutation == "leaf-link":
            external = outside / "git_read.py"
            external.write_bytes(helper.read_bytes())
            helper.unlink()
            try:
                helper.symlink_to(external)
            except (OSError, NotImplementedError):
                pytest.skip("symlinks unavailable")
        elif mutation == "parent-link":
            tools = helper.parent
            external_tools = outside / "tools"
            external_tools.mkdir()
            shutil.copyfile(helper, external_tools / "git_read.py")
            shutil.rmtree(tools)
            try:
                tools.symlink_to(external_tools, target_is_directory=True)
            except (OSError, NotImplementedError):
                pytest.skip("directory symlinks unavailable")
        elif mutation == "wrong-pin":
            source = caller.read_text(encoding="utf-8")
            source, count = re.subn(
                r'(?m)^_GIT_READ_SHA256 = "[0-9a-f]{64}"$',
                '_GIT_READ_SHA256 = "' + "0" * 64 + '"', source, count=1,
            )
            assert count == 1
            caller.write_text(source, encoding="utf-8")
        elif mutation != "cached-module":
            raise AssertionError(f"unhandled mutation {mutation}")

        cwd = outside / "cwd"
        cwd.mkdir()
        cwd_decoy = cwd / "tools" / "git_read.py"
        cwd_decoy.parent.mkdir()
        cwd_decoy.write_text(
            "from pathlib import Path\n"
            f"Path({str(tmp_path / 'cwd-marker')!r}).write_text('decoy')\n",
            encoding="utf-8",
        )
        result = _run_bound_cli(
            caller, cwd, marker, cached=(mutation == "cached-module"),
        )
        if mutation != "cached-module":
            assert result.returncode != 0, result.stdout
            assert "git-read-binding-failed" in result.stderr, result.stderr
            assert not marker.exists(), "rejected binding executed helper bytes"
        else:
            assert result.returncode == 0, result.stderr
            assert marker.read_text(encoding="utf-8") == "trusted-helper-ran"
        assert not (tmp_path / "cwd-marker").exists()


def _markdown_discovery_tree(base: Path, *, literal_decoy: bool) -> Path:
    root = base / "repo"
    root.mkdir(parents=True)
    (root / "src.py").write_text(
        "# snippet-start: demo\nnew body\n# snippet-end: demo\n",
        encoding="utf-8",
    )
    (root / "broken.md").write_text(
        "# Broken\n\n[missing](missing.md)\n\n"
        "<!-- snippet: src.py#demo -->\n```python\nstale body\n```\n",
        encoding="utf-8",
    )
    if literal_decoy:
        (root / "*.md").write_text("# Clean literal filename\n", encoding="utf-8")
    _commit_tree(root)
    return root


def _discovery_cli_env(base: Path) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key != "PYTHONPATH"}
    env.update({
        "GIT_LITERAL_PATHSPECS": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "CAIRN_TEST_HELPER_MARKER": str(base / "helper-marker"),
    })
    return env


def _run_discovery_cli(base: Path, rel: str, root: Path, *,
                       literal_wildcard: bool = False, args: list[str] | None = None,
                       env_overrides: dict[str, str] | None = None):
    caller, _helper = _bound_cli_tree(
        base, rel, _marked_helper(), literal_wildcard=literal_wildcard,
    )
    cwd = base / "outside-cwd"
    cwd.mkdir(parents=True)
    env = _discovery_cli_env(base)
    if env_overrides:
        env.update(env_overrides)
    if args is None:
        args = (["--root", str(root)] if rel.endswith("link_check.py") else
                ["--root", str(root), "--check"])
    result = subprocess.run(
        [sys.executable, str(caller), *args], cwd=cwd, env=env,
        text=True, capture_output=True, timeout=30,
    )
    return result, caller


def _hostile_git_path(base: Path) -> tuple[Path, Path]:
    """Return a PATH prefix whose git records execution before delegation."""
    if os.name == "nt":
        pytest.skip("hostile PATH marker uses a POSIX executable wrapper")
    real_git = shutil.which("git")
    assert real_git is not None and Path(real_git).is_absolute()
    directory = base / "hostile-bin"
    directory.mkdir(parents=True)
    marker = base / "hostile-git-ran"
    wrapper = directory / "git"
    wrapper.write_text(
        "#!/bin/sh\n"
        f"printf called >> {str(marker)!r}\n"
        f"exec {str(Path(real_git).resolve())!r} \"$@\"\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return directory, marker


def _mutate_owner_to_path_git(caller: Path) -> None:
    source = caller.read_text(encoding="utf-8")
    source, import_count = source.replace(
        "import types\n", "import types\nimport subprocess\n", 1,
    ), source.count("import types\n")
    assert import_count == 1, "the isolated route mutant needs subprocess"
    old = ('    result = _GIT_READ.run_git(\n'
           '        str(root), ("ls-files", "-z", "--cached", "--stage"))')
    new = ('    raw = subprocess.run(\n'
           '        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--stage"],\n'
           '        capture_output=True, check=False,\n'
           '    )\n'
           '    result = types.SimpleNamespace(\n'
           '        state="completed", returncode=raw.returncode,\n'
           '        stdout=raw.stdout, stderr=raw.stderr,\n'
           '    )')
    source, count = source.replace(old, new), source.count(old)
    assert count == 1, "the selected physical owner's index route must mutate once"
    caller.write_text(source, encoding="utf-8")


def _assert_discovery_finding(result: subprocess.CompletedProcess[str], kind: str) -> None:
    assert result.returncode == 1
    if kind == "link":
        assert "broken.md" in result.stderr and "broken link" in result.stderr
    else:
        assert "broken.md" in result.stderr and "snippet(s) drifted" in result.stderr


@pytest.mark.skipif(os.name == "nt", reason="hostile PATH marker uses a POSIX wrapper")
@pytest.mark.parametrize("rel", _BOUND_CALLERS)
def test_each_markdown_owner_refuses_hostile_git_and_catches_path_route_mutant(
    tmp_path: Path, rel: str,
) -> None:
    """Each physical CLI owner binds Git for tracked Markdown discovery."""
    root = _markdown_discovery_tree(tmp_path / "fixture", literal_decoy=False)
    hostile_bin, marker = _hostile_git_path(root)
    hostile_env = {
        "PATH": str(hostile_bin) + os.pathsep + os.environ.get("PATH", ""),
    }
    kind = "link" if rel.endswith("link_check.py") else "snippet"

    clean, _ = _run_discovery_cli(tmp_path / "clean", rel, root)
    _assert_discovery_finding(clean, kind)

    safe, _ = _run_discovery_cli(
        tmp_path / "safe-hostile", rel, root, env_overrides=hostile_env,
    )
    assert safe.returncode != 0, safe.stdout + safe.stderr
    assert "tracked Markdown discovery failed" in safe.stderr, safe.stderr
    assert not marker.exists(), "safe discovery executed hostile PATH Git"

    _, caller = _run_discovery_cli(tmp_path / "mutant", rel, root)
    _mutate_owner_to_path_git(caller)
    mutant_env = _discovery_cli_env(tmp_path / "mutant")
    mutant_env["PATH"] = hostile_env["PATH"]
    mutant = subprocess.run(
        [sys.executable, str(caller), "--root", str(root)]
        + ([] if kind == "link" else ["--check"]),
        cwd=tmp_path / "mutant" / "outside-cwd", env=mutant_env,
        text=True, capture_output=True, timeout=30,
    )
    assert marker.exists(), "unsafe PATH route did not execute hostile Git"
    _assert_discovery_finding(mutant, kind)


@pytest.mark.parametrize(
    "kind,rel",
    [("link", "scripts/link_check.py"),
     ("snippet", "scripts/sync_doc_snippets.py")],
)
def test_real_discovery_cli_finds_planted_issue_without_decoy(
    tmp_path: Path, kind: str, rel: str,
) -> None:
    root = _markdown_discovery_tree(tmp_path, literal_decoy=False)
    result, caller = _run_discovery_cli(tmp_path / "candidate", rel, root)
    _assert_discovery_finding(result, kind)
    if kind == "link":
        assert "across 1 file(s)" in result.stderr
    else:
        assert "1 snippet(s) drifted" in result.stderr
        synced = subprocess.run(
            [sys.executable, str(caller), "--root", str(root), "--sync",
             str(root / "broken.md")],
            env=_discovery_cli_env(tmp_path / "candidate"),
            text=True, capture_output=True, timeout=30,
        )
        assert synced.returncode == 0, synced.stderr
        clean = subprocess.run(
            [sys.executable, str(caller), "--root", str(root), "--check"],
            env=_discovery_cli_env(tmp_path / "candidate"),
            text=True, capture_output=True, timeout=30,
        )
        assert clean.returncode == 0 and "1 doc(s) scanned" in clean.stdout


@pytest.mark.skipif(
    os.name == "nt",
    reason="literal '*.md' filename is unavailable on Windows; this decoy case is POSIX-specific",
)
@pytest.mark.parametrize(
    "kind,rel",
    [("link", "scripts/link_check.py"),
     ("snippet", "scripts/sync_doc_snippets.py")],
)
def test_real_discovery_cli_keeps_broken_file_with_decoy_and_catches_literal_mutant(
    tmp_path: Path, kind: str, rel: str,
) -> None:
    root = _markdown_discovery_tree(tmp_path, literal_decoy=True)
    candidate, caller = _run_discovery_cli(tmp_path / "candidate", rel, root)
    _assert_discovery_finding(candidate, kind)
    if kind == "link":
        assert "across 2 file(s)" in candidate.stderr
    else:
        assert "1 snippet(s) drifted" in candidate.stderr

    mutant, _mutant_caller = _run_discovery_cli(
        tmp_path / "mutant", rel, root, literal_wildcard=True,
    )
    with pytest.raises(AssertionError):
        _assert_discovery_finding(mutant, kind)
    assert mutant.returncode == 0
    if kind == "link":
        assert "1 Markdown file(s) scanned" in mutant.stdout
    else:
        assert "1 doc(s) scanned" in mutant.stdout
    assert (root / "broken.md").exists() and (root / "*.md").exists()

    if kind == "snippet":
        synced = subprocess.run(
            [sys.executable, str(caller), "--root", str(root), "--sync",
             str(root / "broken.md")],
            env=_discovery_cli_env(tmp_path / "candidate"),
            text=True, capture_output=True, timeout=30,
        )
        assert synced.returncode == 0, synced.stderr
        clean = subprocess.run(
            [sys.executable, str(caller), "--root", str(root), "--check"],
            env=_discovery_cli_env(tmp_path / "candidate"),
            text=True, capture_output=True, timeout=30,
        )
        assert clean.returncode == 0 and "2 doc(s) scanned" in clean.stdout
    else:
        (root / "missing.md").write_text("# Now present\n", encoding="utf-8")
        clean = subprocess.run(
            [sys.executable, str(caller), "--root", str(root)],
            env=_discovery_cli_env(tmp_path / "candidate"),
            text=True, capture_output=True, timeout=30,
        )
        assert clean.returncode == 0 and "2 Markdown file(s) scanned" in clean.stdout


# ---------------------------------------------------------------------------
# link_check behavioral fixtures
# ---------------------------------------------------------------------------

class TestFilterSources:
    """Archive / ephemeral SOURCE exclusion -- parity with modflow_tools'
    verify_doc_links (the reference deployment).  Filters sources only:
    a live doc linking TO an archived file is still validated."""

    def _paths(self, root: Path) -> list[Path]:
        return [
            root / "AGENTS.md",
            root / "docs" / "guide.md",
            root / "docs" / "archive" / "old.md",          # docs/ stays gated
            root / "dev" / "proposals" / "live.md",
            root / "dev" / "proposals" / "archive" / "old.md",
            root / "dev" / "plans" / "archive" / "prog" / "deep.md",  # nested
            root / "dev" / "reflections" / "2026-05-29-x.md",
        ]

    def test_excludes_dev_archive_and_reflections(self, tmp_path: Path) -> None:
        kept = link_check.filter_sources(self._paths(tmp_path), tmp_path)
        rel = sorted(str(p.relative_to(tmp_path)) for p in kept)
        # docs/archive/ is KEPT: the rule is anchored to dev/ as the first
        # segment so docs/ stays fully link-gated.
        assert rel == sorted([
            "AGENTS.md",
            "docs/guide.md",
            "docs/archive/old.md",
            "dev/proposals/live.md",
        ]), rel

    def test_include_archives_returns_all(self, tmp_path: Path) -> None:
        allp = self._paths(tmp_path)
        assert link_check.filter_sources(
            allp, tmp_path, include_archives=True) == allp

    def test_link_to_archived_file_still_validated(self, tmp_path: Path) -> None:
        """Excluding archive sources does not stop a live doc's link to an
        archived file from being checked (SOURCES-only semantics)."""
        (tmp_path / "dev" / "archive").mkdir(parents=True)
        (tmp_path / "live.md").write_text(
            "# Live\n\n[gone](dev/archive/missing.md)\n")
        res = link_check.check_tree(tmp_path, [tmp_path / "live.md"])
        assert any(f.kind == "link" for f in res.flags), (
            "a broken link into dev/archive/ should still flag")


class TestLinkCheck:
    def _tree(self, root: Path) -> None:
        (root / "b.md").write_text("# B\n\n## target\n\nbody\n")
        (root / "a.md").write_text(
            "# A\n\n"
            "## A heading\n\n"
            "[rel](b.md)\n\n"             # ok: relative file
            "[self](#a-heading)\n\n"      # ok: same-file anchor
            "[cross](b.md#target)\n\n"    # ok: cross-file anchor
            "[ext](https://example.com)\n\n"  # external: ignored by default
            "[missing](nope.md)\n\n"      # broken: file
            "[badanchor](#no-such)\n"     # broken: anchor
        )

    def test_resolves_and_flags(self, tmp_path: Path) -> None:
        self._tree(tmp_path)
        res = link_check.check_tree(
            tmp_path, [tmp_path / "a.md", tmp_path / "b.md"])
        kinds = sorted(f.kind for f in res.flags)
        assert kinds == ["anchor", "link"], (
            f"expected exactly one broken link + one broken anchor, got "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )
        assert res.external_links == 1, "external link should be counted"

    def test_main_exit_code(self, tmp_path: Path) -> None:
        self._tree(tmp_path)
        rc = link_check.main(
            ["--root", str(tmp_path),
             str(tmp_path / "a.md"), str(tmp_path / "b.md")])
        assert rc == 1
        # A clean tree exits 0.
        (tmp_path / "a.md").write_text("# A\n\n## A heading\n\n[ok](#a-heading)\n")
        rc = link_check.main(["--root", str(tmp_path), str(tmp_path / "a.md")])
        assert rc == 0

    def test_external_default_ignored(self, tmp_path: Path) -> None:
        (tmp_path / "x.md").write_text("# X\n\n[e](https://nope.invalid)\n")
        res = link_check.check_tree(tmp_path, [tmp_path / "x.md"])
        assert res.flags == [], "external link must not be probed by default"
        assert res.external_links == 1

    def test_escaping_relative_link_flagged(self, tmp_path: Path) -> None:
        """A relative link to a real file *outside* the repo root is a flag,
        not a silent pass (Codex code-review finding 1)."""
        root = tmp_path / "repo"
        root.mkdir()
        (tmp_path / "outside.md").write_text("# Outside\n")  # exists, outside
        doc = root / "doc.md"
        doc.write_text("# Doc\n\n[escape](../outside.md)\n")
        res = link_check.check_tree(root, [doc])
        assert [f.kind for f in res.flags] == ["link"], (
            "escaping relative link should be flagged, got "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )
        assert "escapes the repo root" in res.flags[0].message

    @pytest.mark.skipif(shutil.which("git") is None, reason="git unavailable")
    def test_default_discovery_uses_all_tracked_markdown_with_literal_decoy(
            self, tmp_path: Path, monkeypatch, capsys) -> None:
        (tmp_path / "broken.md").write_text(
            "# Broken\n\n[missing](missing.md)\n", encoding="utf-8")
        (tmp_path / "*.md").write_text("# Literal filename\n", encoding="utf-8")
        _commit_tree(tmp_path)
        monkeypatch.setenv("GIT_LITERAL_PATHSPECS", "1")
        calls = []
        reader = link_check._GIT_READ
        original = reader.run_git

        def observed(target, args, **kwargs):
            calls.append(args)
            return original(target, args, **kwargs)

        monkeypatch.setattr(reader, "run_git", observed)
        assert [path.name for path in link_check.tracked_markdown(tmp_path)] == [
            "*.md", "broken.md"]
        assert link_check.main(["--root", str(tmp_path)]) == 1
        assert calls and all(args == (
            "ls-files", "-z", "--cached", "--stage") for args in calls)
        assert "broken.md" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Fold 4: link_check explicit-anchor {#custom-id} regression
# ---------------------------------------------------------------------------

class TestExplicitAnchor:
    """Regression tests for the {#custom-id} anchor attribute fix.

    A heading ``### T {#t}`` previously slugged to ``t-t`` (the braces
    content fed into github_slug), so a link to ``#t`` silently resolved
    to nothing.  The fix registers the literal id (``t``) and the auto-slug
    of the heading text without the attribute (``t`` again in this case, or
    a distinct slug for longer headings).

    The regression test must cover
    leading/trailing whitespace in the attribute and the no-match / garbage
    cases.
    """

    def test_explicit_anchor_registered(self) -> None:
        """The literal id from {#custom-id} is in the anchor set."""
        text = "# Top\n\n## Section {#my-anchor}\n"
        anchors = link_check.file_anchors(text)
        assert "my-anchor" in anchors, f"expected 'my-anchor' in {anchors}"

    def test_auto_slug_without_attr_also_registered(self) -> None:
        """The auto-slug of the heading text WITHOUT the {#...} attr is also
        registered so both reference forms resolve."""
        text = "# Top\n\n## Section {#custom}\n"
        anchors = link_check.file_anchors(text)
        # 'section' is the slug of 'Section' (without the attr)
        assert "section" in anchors, f"auto-slug 'section' missing from {anchors}"
        assert "custom" in anchors, f"explicit id 'custom' missing from {anchors}"

    def test_no_double_slug_bug(self) -> None:
        """### T {#t} must NOT produce the doubled 't-t' slug."""
        text = "### T {#t}\n"
        anchors = link_check.file_anchors(text)
        assert "t-t" not in anchors, f"double-slug 't-t' must not appear in {anchors}"
        assert "t" in anchors, f"explicit id 't' must appear in {anchors}"

    def test_link_to_explicit_anchor_resolves(self, tmp_path: Path) -> None:
        """An intra-doc link to an explicit anchor must not be flagged."""
        (tmp_path / "doc.md").write_text(
            "# Doc\n\n"
            "## Reference {#ref-anchor}\n\n"
            "[see ref](#ref-anchor)\n"
        )
        res = link_check.check_tree(tmp_path, [tmp_path / "doc.md"])
        assert res.flags == [], (
            f"link to explicit anchor should resolve cleanly, got: "
            f"{[(f.kind, f.message) for f in res.flags]}"
        )

    def test_leading_trailing_whitespace_in_attr(self) -> None:
        """The {# id } form with spaces inside the braces is handled --
        the id is stripped and registered as 'id', not ' id '."""
        text = "## Title {#  spaced-id  }\n"
        anchors = link_check.file_anchors(text)
        assert "spaced-id" in anchors, (
            f"id with surrounding spaces should be stripped; anchors={anchors}"
        )
        assert "spaced-id" == "spaced-id"  # sanity

    def test_whitespace_before_brace(self) -> None:
        """The pattern handles extra spaces between heading text and '{'."""
        text = "## Title   {#whitespace-before}\n"
        anchors = link_check.file_anchors(text)
        assert "whitespace-before" in anchors, (
            f"whitespace before brace should be handled; anchors={anchors}"
        )

    def test_no_attr_unchanged(self) -> None:
        """A heading without {#...} still produces the normal github slug."""
        text = "## Normal Heading\n"
        anchors = link_check.file_anchors(text)
        assert "normal-heading" in anchors, (
            f"standard slug should still work; anchors={anchors}"
        )

    def test_garbage_brace_not_matched(self) -> None:
        """Braces that don't match the {#id} pattern are not treated as
        explicit anchors -- e.g. ``## Title {not-an-id}`` or empty ``{#}``."""
        # No leading '#' inside braces -> not an explicit anchor
        text_no_hash = "## Title {not-an-id}\n"
        anchors_no_hash = link_check.file_anchors(text_no_hash)
        # Should slug normally (no explicit anchor extracted)
        assert "title-not-an-id" in anchors_no_hash or "title" in anchors_no_hash, (
            f"garbage brace should not strip content; got {anchors_no_hash}"
        )

    def test_empty_explicit_id_skipped(self) -> None:
        """An empty {#} attribute contributes no anchor (empty id skipped)."""
        text = "## Title {#}\n"
        anchors = link_check.file_anchors(text)
        # The empty id must not be registered; the auto-slug of 'Title' should be
        assert "" not in anchors, f"empty string must not be in anchors: {anchors}"


# ---------------------------------------------------------------------------
# sync_doc_snippets behavioral fixtures
# ---------------------------------------------------------------------------

class TestSnippetSync:
    def _source(self, root: Path) -> None:
        (root / "src.py").write_text(
            "x = 1\n"
            "# snippet-start: demo\n"
            "model = Model(config)\n"
            "model.build()\n"
            "# snippet-end: demo\n"
            "y = 2\n"
        )

    def _doc(self, body: str) -> str:
        return (
            "# Doc\n\n"
            "<!-- snippet: src.py#demo -->\n"
            "```python\n"
            f"{body}"
            "```\n"
        )

    def test_clean_check_passes(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        (tmp_path / "d.md").write_text(
            self._doc("model = Model(config)\nmodel.build()\n"))
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(tmp_path / "d.md")]) == 0

    def test_drift_detected_and_synced(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(self._doc("model = Model(config)  # stale\n"))
        src_before = (tmp_path / "src.py").read_bytes()
        # --check flags the drift.
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1
        # --sync rewrites the doc, then --check is clean.
        assert snippets.main(
            ["--root", str(tmp_path), "--sync", str(doc)]) == 0
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 0
        assert "model.build()" in doc.read_text()
        assert "# stale" not in doc.read_text()
        # The source is never rewritten.
        assert (tmp_path / "src.py").read_bytes() == src_before

    @pytest.mark.skipif(shutil.which("git") is None, reason="git unavailable")
    def test_default_discovery_uses_all_tracked_markdown_with_literal_decoy(
            self, tmp_path: Path, monkeypatch, capsys) -> None:
        self._source(tmp_path)
        doc = tmp_path / "broken.md"
        doc.write_text(self._doc("stale body\n"), encoding="utf-8")
        (tmp_path / "*.md").write_text("# Literal filename\n", encoding="utf-8")
        _commit_tree(tmp_path)
        monkeypatch.setenv("GIT_LITERAL_PATHSPECS", "1")
        calls = []
        reader = snippets._GIT_READ
        original = reader.run_git

        def observed(target, args, **kwargs):
            calls.append(args)
            return original(target, args, **kwargs)

        monkeypatch.setattr(reader, "run_git", observed)
        assert [path.name for path in snippets.tracked_markdown(tmp_path)] == [
            "*.md", "broken.md"]
        assert snippets.main(["--root", str(tmp_path), "--check"]) == 1
        assert calls and all(args == (
            "ls-files", "-z", "--cached", "--stage") for args in calls)
        assert "broken.md" in capsys.readouterr().err

    def test_escaping_source_rejected(self, tmp_path: Path) -> None:
        doc = tmp_path / "d.md"
        doc.write_text(
            "# Doc\n\n<!-- snippet: ../evil.py#demo -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1
        # Absolute paths are refused too.
        doc.write_text(
            "# Doc\n\n<!-- snippet: /etc/passwd#demo -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1

    def test_missing_region_is_crisp_error(self, tmp_path: Path) -> None:
        self._source(tmp_path)
        doc = tmp_path / "d.md"
        doc.write_text(
            "# Doc\n\n<!-- snippet: src.py#absent -->\n```\nx\n```\n")
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 1

    def test_outside_doc_rejected(self, tmp_path: Path) -> None:
        """--sync must refuse a directive-bearing doc outside the repo root,
        without rewriting it (Codex code-review finding 2)."""
        root = tmp_path / "repo"
        root.mkdir()
        (root / "src.py").write_text(
            "# snippet-start: demo\nnew\n# snippet-end: demo\n")
        doc = tmp_path / "outside.md"
        before = ("<!-- snippet: src.py#demo -->\n~~~\nold\n~~~\n")
        doc.write_text(before)
        rc = snippets.main(["--root", str(root), "--sync", str(doc)])
        assert rc == 1, "an outside doc must be refused"
        assert doc.read_text() == before, "the outside doc must not be rewritten"

    def test_longer_fence_wraps_shorter(self, tmp_path: Path) -> None:
        """A 4-fence block that contains a shorter same-char fence in its
        body is one block, not closed early (Codex code-review finding 3)."""
        (tmp_path / "src.py").write_text(
            "# snippet-start: fenced\na\n~~~\nb\n# snippet-end: fenced\n")
        doc = tmp_path / "d.md"
        # 4-tilde fences wrapping a body that contains a 3-tilde literal.
        doc.write_text(
            "# Doc\n\n<!-- snippet: src.py#fenced -->\n"
            "~~~~\na\n~~~\nb\n~~~~\n")
        # The body equals the region, so a correct parser sees no drift.
        assert snippets.main(
            ["--root", str(tmp_path), "--check", str(doc)]) == 0


# ---------------------------------------------------------------------------
# link_check --check-external SSRF guard (security-hardening Chunk 1)
# ---------------------------------------------------------------------------

class TestLinkCheckSSRF:
    """The external-link probe must refuse non-public destinations and
    validate every redirect hop (no live network: literal IPs resolve via
    getaddrinfo without DNS, and refused hosts never reach the opener)."""

    def test_host_public_classification(self) -> None:
        # Non-public literals -> blocked. Includes ranges that are
        # non-global but carry no single denylist flag, so only the
        # `not is_global` contract catches them (Codex finding 1):
        #   100.64.0.1  -> CGNAT shared space (100.64.0.0/10)
        #   2001:db8::1 -> IPv6 documentation range (non-global)
        #   fc00::1     -> IPv6 unique-local
        for ip in ("127.0.0.1", "10.0.0.1", "192.168.1.1",
                   "169.254.169.254", "100.64.0.1",
                   "::1", "fe80::1", "fc00::1", "2001:db8::1"):
            assert link_check._host_is_public(ip) is False, ip
        # A public literal -> allowed (no DNS needed).
        assert link_check._host_is_public("93.184.216.34") is True
        # Unresolvable / empty -> fail-closed.
        assert link_check._host_is_public("") is False

    def test_allow_host_bypass(self) -> None:
        # An explicitly allow-listed internal host passes without a public
        # classification; everything else still requires public.
        assert link_check._host_allowed("127.0.0.1", {"127.0.0.1"}) is True
        assert link_check._host_allowed("127.0.0.1", set()) is False

    def test_probe_refuses_non_public_host(self, tmp_path: Path) -> None:
        flags: list = []
        link_check._probe_external(
            tmp_path / "x.md", 1, "http://169.254.169.254/latest/meta-data/",
            flags, allow_hosts=set())
        assert any("SSRF guard" in f.message for f in flags), flags

    def test_probe_refuses_non_http_scheme(self, tmp_path: Path) -> None:
        flags: list = []
        link_check._probe_external(
            tmp_path / "x.md", 1, "ftp://example.com/x", flags,
            allow_hosts=set())
        assert any("non-http(s) scheme" in f.message for f in flags), flags

    def test_redirect_hop_to_private_is_refused(self, tmp_path, monkeypatch):
        """A public first hop that 302-redirects to a link-local address is
        refused at the second hop (manual, validated redirects)."""
        class _FakeOpener:
            def open(self, req, timeout=None):
                raise link_check.urllib.error.HTTPError(
                    req.full_url, 302, "Found",
                    {"Location": "http://169.254.169.254/"}, None)

        monkeypatch.setattr(link_check.urllib.request, "build_opener",
                            lambda *a, **k: _FakeOpener())
        flags: list = []
        # First hop is a public literal IP (passes), then the redirect target
        # is link-local (must be refused before contact).
        link_check._probe_external(
            tmp_path / "x.md", 1, "http://93.184.216.34/", flags,
            allow_hosts=set())
        assert any("SSRF guard" in f.message for f in flags), flags
