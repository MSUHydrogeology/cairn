"""
Tests for the Cairn v0.2 P5 work-intent tool (coordination-tiers).

Covers, per the executing plan (cairn-v0.2-p5-intents-tool):

* install-path: the tool lands verbatim in ``tools/intent.py``; the
  ``.md`` doctrine lands in ``dev/modules/``; ``.gitignore`` is seeded;
  skip-if-exists / ``--force`` respected.
* C6: ``.gitignore`` seeding is non-clobber, idempotent, ``--dry-run``
  aware.
* C3 / P-2: identity resolves via ``CAIRN_AGENT`` override, the built-in
  harness registry, an **adopter-supplied** registry entry (the
  portability contract), and a static config ``agent``.
* P-3: a ``CAIRN_AGENT`` override that shadows an available harness
  session var emits a warning.
* I4 / P-5: the post-commit hook installer chains onto a plain hook and
  **refuses without mutation** (bytes + mode unchanged) for
  framework-managed / non-shell / non-executable hooks.
* C5: the generated hook captures the install-time interpreter, and the
  full claim -> commit -> auto-release arc works off the CLI.
* F4: install-hook on a no-git target degrades with a clear diagnostic,
  not a stack trace; a ``main``-default repo works.
* C4: the installed tool and the generated hook carry no
  modflow_tools residue.
* F1: the installed tool is standard-library only (no ``yaml`` import).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

# Allow tests to import scaffold without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _GITIGNORE_SEEDS,
    _MODULE_MAPPINGS,
    main,
    seed_gitignore,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
TOOL_TEMPLATE = TEMPLATES_ROOT / "modules" / "team-gated" / "intent.py"

#: Identity env vars that must be cleared for deterministic resolution.
_IDENTITY_VARS = (
    "CAIRN_AGENT",
    "CAIRN_PYTHON",
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_THREAD_ID",
    "ANTIGRAVITY_TRAJECTORY_ID",
)

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scaffold(target: Path, modules: list[str]) -> int:
    """Scaffold *modules* into *target* via the real CLI entry point."""
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: CoordTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


def _load_tool(path: Path, name: str = "p5_intent") -> ModuleType:
    """Import the installed tool by file path (dataclass-safe)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _clean_env(**overrides: str) -> dict:
    """A subprocess env with identity vars cleared, then *overrides*."""
    env = dict(os.environ)
    for var in _IDENTITY_VARS:
        env.pop(var, None)
    env.update(overrides)
    return env


def _git_repo(tmp_path: Path, *, branch: str = "master") -> Path:
    """Create a git repo at *tmp_path* with the tool at tools/intent.py."""
    subprocess.run(
        ["git", "init", "-q"], cwd=tmp_path, check=True, env=_clean_env(),
    )
    # Rename the initial branch deterministically (init.defaultBranch
    # varies across git versions).
    subprocess.run(
        ["git", "symbolic-ref", "HEAD", f"refs/heads/{branch}"],
        cwd=tmp_path, check=True, env=_clean_env(),
    )
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path,
                   check=True, env=_clean_env())
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path,
                   check=True, env=_clean_env())
    (tmp_path / "tools").mkdir(exist_ok=True)
    (tmp_path / "dev").mkdir(exist_ok=True)
    (tmp_path / "tools" / "intent.py").write_bytes(TOOL_TEMPLATE.read_bytes())
    return tmp_path / "tools" / "intent.py"


def _run_tool(tool: Path, args: list[str], *, cwd: Path,
              env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tool), *args],
        cwd=cwd, capture_output=True, text=True,
        env=env if env is not None else _clean_env(),
    )


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_tool_registered_1many(self) -> None:
        """coordination-tiers installs both the doctrine .md and the
        verbatim tool .py (1:many, the P1 pattern)."""
        specs = _MODULE_MAPPINGS["coordination-tiers"]
        dsts = {s.dst: s for s in specs}
        assert "dev/modules/coordination-tiers.md" in dsts
        assert "tools/intent.py" in dsts
        assert dsts["tools/intent.py"].verbatim is True
        assert dsts["dev/modules/coordination-tiers.md"].verbatim is False

    def test_tool_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        installed = tmp_path / "tools" / "intent.py"
        assert installed.is_file(), "tool not installed"
        assert installed.read_bytes() == TOOL_TEMPLATE.read_bytes(), (
            "installed tool differs from template -- not verbatim"
        )
        assert (
            tmp_path / "dev" / "modules" / "coordination-tiers.md"
        ).is_file()

    def test_gitignore_seeded(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        gi = tmp_path / ".gitignore"
        assert gi.is_file()
        assert "dev/intents.jsonl" in gi.read_text().splitlines()

    def test_rerun_skips_existing_tool(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        installed = tmp_path / "tools" / "intent.py"
        edited = installed.read_text() + "\n# adopter edit\n"
        installed.write_text(edited)
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        assert installed.read_text() == edited, (
            "re-scaffold without --force clobbered an edited tool"
        )


# ---------------------------------------------------------------------------
# .gitignore seeding contract (C6)
# ---------------------------------------------------------------------------

class TestGitignoreSeeding:
    def test_coordination_tiers_in_seed_map(self) -> None:
        assert "dev/intents.jsonl" in _GITIGNORE_SEEDS["coordination-tiers"]

    def test_idempotent_no_duplicate(self, tmp_path: Path) -> None:
        added1 = seed_gitignore(tmp_path, ("dev/intents.jsonl",))
        added2 = seed_gitignore(tmp_path, ("dev/intents.jsonl",))
        assert added1 == ["dev/intents.jsonl"]
        assert added2 == []  # already present -- nothing re-added
        lines = (tmp_path / ".gitignore").read_text().splitlines()
        assert lines.count("dev/intents.jsonl") == 1

    def test_non_clobber_preserves_existing(self, tmp_path: Path) -> None:
        gi = tmp_path / ".gitignore"
        gi.write_text("*.log\n__pycache__/\n")
        seed_gitignore(tmp_path, ("dev/intents.jsonl",))
        text = gi.read_text()
        assert "*.log" in text and "__pycache__/" in text
        assert "dev/intents.jsonl" in text.splitlines()

    def test_dry_run_writes_nothing(self, tmp_path: Path) -> None:
        would = seed_gitignore(tmp_path, ("dev/intents.jsonl",), dry_run=True)
        assert would == ["dev/intents.jsonl"]
        assert not (tmp_path / ".gitignore").exists()


# ---------------------------------------------------------------------------
# Identity resolution (C3, P-2, P-3)
# ---------------------------------------------------------------------------

class TestIdentity:
    @pytest.fixture()
    def tool(self, tmp_path: Path) -> ModuleType:
        return _load_tool(TOOL_TEMPLATE, name=f"p5_id_{tmp_path.name}")

    def _clear(self, monkeypatch) -> None:
        for var in _IDENTITY_VARS:
            monkeypatch.delenv(var, raising=False)

    def test_cairn_agent_override(self, tool, monkeypatch, tmp_path) -> None:
        self._clear(monkeypatch)
        monkeypatch.setenv("CAIRN_AGENT", "  alice  ")
        cfg = tmp_path / "agent.json"
        assert tool.resolve_agent_identity(config_path=cfg) == "alice"

    def test_harness_session_derivation_stable(
        self, tool, monkeypatch, tmp_path
    ) -> None:
        self._clear(monkeypatch)
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-XYZ")
        cfg = tmp_path / "agent.json"
        first = tool.resolve_agent_identity(config_path=cfg)
        second = tool.resolve_agent_identity(config_path=cfg)
        assert first == second  # per-session stable
        assert first.startswith("claude-")
        # Whole-id hash, never a prefix slice.
        assert "sess-XYZ" not in first

    def test_none_when_unconfigured(self, tool, monkeypatch, tmp_path) -> None:
        self._clear(monkeypatch)
        cfg = tmp_path / "agent.json"  # does not exist
        assert tool.resolve_agent_identity(config_path=cfg) is None

    def test_static_config_agent(self, tool, monkeypatch, tmp_path) -> None:
        self._clear(monkeypatch)
        cfg = tmp_path / "agent.json"
        cfg.write_text(json.dumps({"agent": "carol"}))
        assert tool.resolve_agent_identity(config_path=cfg) == "carol"

    def test_adopter_supplied_registry(
        self, tool, monkeypatch, tmp_path
    ) -> None:
        """P-2 portability contract: an adopter registers a NEW harness
        via the JSON config -- no edit to the tool -- and an identity
        resolves from its session var."""
        self._clear(monkeypatch)
        cfg = tmp_path / "agent.json"
        cfg.write_text(json.dumps({
            "harness_session_vars": [["myharness", "MY_SESSION_ID"]],
        }))
        # The new var is NOT a built-in; only the config makes it known.
        assert ("myharness", "MY_SESSION_ID") not in tool.HARNESS_SESSION_VARS
        monkeypatch.setenv("MY_SESSION_ID", "deadbeef")
        ident = tool.resolve_agent_identity(config_path=cfg)
        assert ident is not None and ident.startswith("myharness-")

    def test_effective_registry_appends_extras(self, tool, tmp_path) -> None:
        cfg = {"harness_session_vars": [["x", "X_VAR"]]}
        eff = tool.effective_harness_vars(cfg)
        assert eff[: len(tool.HARNESS_SESSION_VARS)] == tool.HARNESS_SESSION_VARS
        assert ("x", "X_VAR") in eff

    def test_override_shadow_warning(self, tmp_path: Path) -> None:
        """P-3: CAIRN_AGENT set while a harness session var is present
        emits the escape-hatch warning (via _auto_release, fail-soft)."""
        repo = _git_repo(tmp_path)
        tool = repo
        paths = tmp_path / "paths"
        paths.write_bytes(b"dev/x\x00")
        env = _clean_env(CAIRN_AGENT="static", CLAUDE_CODE_SESSION_ID="s1")
        res = _run_tool(
            tool,
            ["_auto_release", "--commit", "abc", "--paths-from-file",
             str(paths)],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0  # always fail-soft
        assert "shadowing the per-session identity" in res.stderr


# ---------------------------------------------------------------------------
# Hook diversity + refusal-before-mutation (I4, P-5)
# ---------------------------------------------------------------------------

class TestHookDiversity:
    def _hook(self, repo: Path) -> Path:
        out = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=repo, capture_output=True, text=True, check=True,
            env=_clean_env(),
        ).stdout.strip()
        hooks = Path(out)
        if not hooks.is_absolute():
            hooks = repo / hooks
        return hooks / "post-commit"

    def test_fresh_install_creates_executable_hook(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        res = _run_tool(tool, ["install-hook"], cwd=tmp_path)
        assert res.returncode == 0
        hook = self._hook(tmp_path)
        assert hook.is_file()
        assert os.access(str(hook), os.X_OK)
        text = hook.read_text()
        assert "cairn/intent/post-commit BEGIN" in text

    def test_hook_block_shlex_quotes_metachar_paths(self) -> None:
        """The baked-in interpreter / script paths are single-quoted via
        shlex.quote, so a path with a space, a double-quote, or a shell
        substitution can't break the hook or be evaluated by /bin/sh
        (security-hardening R13)."""
        import shlex as _shlex
        mod = _load_tool(TOOL_TEMPLATE, name="p5_hookquote")
        evil = Path("/x/$(touch pwned)/intent.py")
        block = mod._build_hook_block("/usr/bin/python3", evil)
        # The dangerous path appears only inside its shlex-quoted (single-
        # quoted) form -- never double-quoted (which /bin/sh would expand).
        assert _shlex.quote(str(evil)) in block
        assert '"/x/$(touch pwned)/intent.py"' not in block
        # A space-bearing interpreter path is also quoted.
        block2 = mod._build_hook_block("/opt/my python/bin/python3", evil)
        assert _shlex.quote("/opt/my python/bin/python3") in block2

    def test_chain_preserves_existing_plain_hook(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        hook = self._hook(tmp_path)
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text('#!/bin/sh\necho "my existing hook"\n')
        hook.chmod(0o755)
        res = _run_tool(tool, ["install-hook"], cwd=tmp_path)
        assert res.returncode == 0
        text = hook.read_text()
        assert 'echo "my existing hook"' in text  # preserved
        assert "cairn/intent/post-commit BEGIN" in text  # chained

    @pytest.mark.parametrize("contents,mode", [
        ("#!/bin/sh\n# File generated by pre-commit\nexit 0\n", 0o755),
        ("#!/usr/bin/env python\nprint('hi')\n", 0o755),
        ("#!/bin/sh\necho hi\n", 0o644),  # non-executable
    ], ids=["framework", "non-shell", "non-executable"])
    def test_refuse_without_mutation(self, tmp_path, contents, mode) -> None:
        """P-5: every refused path leaves the file's bytes AND mode
        byte-for-byte unchanged (no partial append, no chmod)."""
        tool = _git_repo(tmp_path)
        hook = self._hook(tmp_path)
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(contents)
        hook.chmod(mode)
        before_bytes = hook.read_bytes()
        before_mode = stat.S_IMODE(hook.stat().st_mode)
        res = _run_tool(tool, ["install-hook"], cwd=tmp_path)
        assert res.returncode == 4, res.stderr
        assert "REFUSING" in res.stderr
        assert hook.read_bytes() == before_bytes, "bytes mutated on refusal"
        assert stat.S_IMODE(hook.stat().st_mode) == before_mode, (
            "mode mutated on refusal"
        )

    def test_idempotent_reinstall_single_block(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        text = self._hook(tmp_path).read_text()
        assert text.count("cairn/intent/post-commit BEGIN") == 1

    def test_uninstall_removes_cairn_only_hook(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        res = _run_tool(tool, ["install-hook", "--uninstall"], cwd=tmp_path)
        assert res.returncode == 0
        assert not self._hook(tmp_path).exists()

    def test_uninstall_preserves_chained_hook(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        hook = self._hook(tmp_path)
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text('#!/bin/sh\necho keep-me\n')
        hook.chmod(0o755)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        _run_tool(tool, ["install-hook", "--uninstall"], cwd=tmp_path)
        text = hook.read_text()
        assert "keep-me" in text
        assert "cairn/intent/post-commit BEGIN" not in text


# ---------------------------------------------------------------------------
# F4 -- VCS robustness
# ---------------------------------------------------------------------------

class TestVcsRobustness:
    def test_no_git_target_clear_diagnostic(self, tmp_path) -> None:
        (tmp_path / "tools").mkdir()
        tool = tmp_path / "tools" / "intent.py"
        tool.write_bytes(TOOL_TEMPLATE.read_bytes())
        res = _run_tool(tool, ["install-hook"], cwd=tmp_path)
        assert res.returncode == 1
        assert "not inside a git working tree" in res.stderr
        assert "Traceback" not in res.stderr  # no stack trace

    def test_main_default_branch_auto_release(self, tmp_path) -> None:
        """No master-hardcoding: a `main`-default repo auto-releases."""
        tool = _git_repo(tmp_path, branch="main")
        env = _clean_env(CAIRN_AGENT="e2e")
        _run_tool(tool, ["install-hook"], cwd=tmp_path, env=env)
        (tmp_path / "dev" / "PLANNING.md").write_text("x\n")
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True,
                       env=env)
        _run_tool(tool, ["claim", "--files", "dev/PLANNING.md",
                         "--action", "main-branch"], cwd=tmp_path, env=env)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=tmp_path,
                       check=True, env=env)
        res = _run_tool(tool, ["list"], cwd=tmp_path, env=env)
        assert "no active intents" in res.stdout


# ---------------------------------------------------------------------------
# Interpreter contract + end-to-end auto-release (C5)
# ---------------------------------------------------------------------------

class TestInterpreterAndEndToEnd:
    def _hook_path(self, repo: Path) -> Path:
        out = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=repo, capture_output=True, text=True, check=True,
            env=_clean_env(),
        ).stdout.strip()
        hooks = Path(out)
        if not hooks.is_absolute():
            hooks = repo / hooks
        return hooks / "post-commit"

    def test_generated_hook_captures_interpreter(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        text = self._hook_path(tmp_path).read_text()
        # The captured interpreter is baked in; no bare `python -m`.
        assert sys.executable in text
        assert "python -m" not in text

    def test_end_to_end_claim_commit_autorelease(self, tmp_path) -> None:
        """C5: the ACTUAL generated hook (not just the CLI) releases the
        committing agent's claim, including on the root commit."""
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="e2e-agent")
        _run_tool(tool, ["install-hook"], cwd=tmp_path, env=env)
        (tmp_path / "dev" / "PLANNING.md").write_text("hello\n")
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, env=env)
        claim = _run_tool(
            tool, ["claim", "--files", "dev/PLANNING.md", "--action", "e2e"],
            cwd=tmp_path, env=env,
        )
        assert claim.returncode == 0
        before = _run_tool(tool, ["list"], cwd=tmp_path, env=env)
        assert "dev/PLANNING.md" in before.stdout  # active before commit
        subprocess.run(["git", "commit", "-q", "-m", "root commit"],
                       cwd=tmp_path, check=True, env=env)
        after = _run_tool(tool, ["list"], cwd=tmp_path, env=env)
        assert "no active intents" in after.stdout  # auto-released


# ---------------------------------------------------------------------------
# C4 -- literal-audit (no modflow_tools residue)
# ---------------------------------------------------------------------------

class TestLiteralAudit:
    _BANNED = ("modflow_tools", "MODFLOW_TOOLS", ".modflow_tools")

    def test_template_tool_has_no_residue(self) -> None:
        text = TOOL_TEMPLATE.read_text()
        for token in self._BANNED:
            assert token not in text, f"residue {token!r} in shipped tool"

    def test_installed_tool_has_no_residue(self, tmp_path) -> None:
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        text = (tmp_path / "tools" / "intent.py").read_text()
        for token in self._BANNED:
            assert token not in text

    def test_generated_hook_has_no_residue(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        out = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=tmp_path, capture_output=True, text=True, check=True,
            env=_clean_env(),
        ).stdout.strip()
        hooks = Path(out)
        if not hooks.is_absolute():
            hooks = tmp_path / hooks
        text = (hooks / "post-commit").read_text()
        for token in self._BANNED:
            assert token not in text
        assert "cairn/intent/post-commit" in text  # residue-free sentinel


# ---------------------------------------------------------------------------
# F1 -- stdlib-only (no PyYAML)
# ---------------------------------------------------------------------------

class TestDependencyGate:
    def test_tool_is_stdlib_only(self) -> None:
        tree = ast.parse(TOOL_TEMPLATE.read_text())
        top_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_modules.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    top_modules.add(node.module.split(".")[0])
        stdlib = set(sys.stdlib_module_names)
        non_stdlib = {m for m in top_modules if m not in stdlib}
        assert non_stdlib == set(), (
            f"tool imports non-stdlib module(s): {sorted(non_stdlib)}"
        )

    def test_no_yaml_anywhere(self) -> None:
        """C3: the dropped YAML config tier leaves no `yaml` reference --
        the tool never fails when PyYAML is absent."""
        assert "yaml" not in TOOL_TEMPLATE.read_text()
