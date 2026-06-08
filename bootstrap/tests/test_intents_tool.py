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
# Session-token link: reflections <session> <-> intent log `agent`
# ---------------------------------------------------------------------------

class TestSessionTokenLink:
    """`resolve_session_token` / `intent whoami` expose the *token* portion
    of the harness-derived identity so a per-session surface outside the
    intent log (the reflections channel's `<session>`) reuses the same
    session id. The invariant the link rests on: a harness-derived identity
    is exactly `<tool_tag>-<token>`."""

    @pytest.fixture()
    def tool(self, tmp_path: Path) -> ModuleType:
        return _load_tool(TOOL_TEMPLATE, name=f"p5_tok_{tmp_path.name}")

    def _clear(self, monkeypatch) -> None:
        for var in _IDENTITY_VARS:
            monkeypatch.delenv(var, raising=False)

    def test_token_is_identity_suffix(
        self, tool, monkeypatch, tmp_path
    ) -> None:
        self._clear(monkeypatch)
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-XYZ")
        cfg = tmp_path / "agent.json"
        token = tool.resolve_session_token(config_path=cfg)
        identity = tool.resolve_agent_identity(config_path=cfg)
        assert token is not None
        assert len(token) == 8 and all(c in "0123456789abcdef" for c in token)
        # The link invariant: <agent>-<session> reconstructs the identity.
        assert identity == f"claude-{token}"
        # Whole-id hash, never a prefix slice of the raw session id.
        assert "sess-XYZ" not in token

    def test_token_none_without_harness_session(
        self, tool, monkeypatch, tmp_path
    ) -> None:
        """A static (non-session) identity still resolves, but yields NO
        token -- it is not per-session, so it cannot supply a collision-safe
        `<session>` (the caller falls back to a random token)."""
        self._clear(monkeypatch)
        cfg = tmp_path / "agent.json"
        cfg.write_text(json.dumps({"agent": "carol"}))
        assert tool.resolve_agent_identity(config_path=cfg) == "carol"
        assert tool.resolve_session_token(config_path=cfg) is None

    def test_whoami_links_identity_and_token(self, tmp_path) -> None:
        """End to end: `whoami` prints the identity, `whoami
        --session-token` prints the token, and the two compose."""
        tool = _git_repo(tmp_path)
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-XYZ")
        ident = _run_tool(tool, ["whoami"], cwd=tmp_path, env=env)
        token = _run_tool(
            tool, ["whoami", "--session-token"], cwd=tmp_path, env=env,
        )
        assert ident.returncode == 0 and token.returncode == 0
        assert ident.stdout.strip() == f"claude-{token.stdout.strip()}"

    def test_whoami_session_token_exits_nonzero_without_session(
        self, tmp_path
    ) -> None:
        tool = _git_repo(tmp_path)
        res = _run_tool(
            tool, ["whoami", "--session-token"], cwd=tmp_path,
            env=_clean_env(),
        )
        assert res.returncode == 1
        assert res.stdout.strip() == ""


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


# ---------------------------------------------------------------------------
# Work-intent pre-commit check (foldback-hardening Chunk C)
# ---------------------------------------------------------------------------

def _precommit_hook(repo: Path) -> Path:
    """Resolve the repo's pre-commit hook path (hooksPath-aware)."""
    out = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"],
        cwd=repo, capture_output=True, text=True, check=True,
        env=_clean_env(),
    ).stdout.strip()
    hooks = Path(out)
    if not hooks.is_absolute():
        hooks = repo / hooks
    return hooks / "pre-commit"


def _stage(repo: Path, env: dict, relpath: str, content: str = "x\n") -> None:
    (repo / relpath).parent.mkdir(parents=True, exist_ok=True)
    (repo / relpath).write_text(content)
    subprocess.run(["git", "add", relpath], cwd=repo, check=True, env=env)


class TestPrecommitInstall:
    def test_install_absent_then_status(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        res = _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        assert res.returncode == 0, res.stderr
        hook = _precommit_hook(tmp_path)
        assert hook.is_file() and os.access(str(hook), os.X_OK)
        text = hook.read_text()
        assert "cairn/intent/pre-commit BEGIN" in text
        # The interpreter is baked in; no bare `python -m`.
        assert sys.executable in text
        assert "python -m" not in text
        st = _run_tool(tool, ["hooks-status"], cwd=tmp_path)
        assert "pre-commit (work-intent check): installed" in st.stdout
        assert "post-commit (auto-release): not-installed" in st.stdout

    def test_install_metachar_path_is_shlex_quoted(self) -> None:
        """The baked-in interpreter / script paths are single-quoted via
        shlex.quote, so a shell-substitution path can't be evaluated."""
        import shlex as _shlex
        mod = _load_tool(TOOL_TEMPLATE, name="p5_precommitquote")
        evil = Path("/x/$(touch pwned)/intent.py")
        block = mod._precommit_hook_block("/usr/bin/python3", evil)
        assert _shlex.quote(str(evil)) in block
        assert '"/x/$(touch pwned)/intent.py"' not in block

    def test_uninstall_residue_free(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        res = _run_tool(
            tool, ["install-precommit", "--uninstall"], cwd=tmp_path,
        )
        assert res.returncode == 0
        assert not _precommit_hook(tmp_path).exists()

    def test_uninstall_preserves_other_content(self, tmp_path) -> None:
        """Sentinel-scoped strip: a hand-added line survives --uninstall."""
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        hook = _precommit_hook(tmp_path)
        text = hook.read_text()
        # Splice a custom line ahead of the sentinel block.
        text = text.replace(
            "# >>> cairn/intent/pre-commit BEGIN",
            'echo keep-me\n# >>> cairn/intent/pre-commit BEGIN',
            1,
        )
        hook.write_text(text)
        hook.chmod(0o755)
        _run_tool(tool, ["install-precommit", "--uninstall"], cwd=tmp_path)
        remaining = hook.read_text()
        assert "keep-me" in remaining
        assert "cairn/intent/pre-commit BEGIN" not in remaining

    def test_idempotent_reinstall_single_block(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        text = _precommit_hook(tmp_path).read_text()
        assert text.count("cairn/intent/pre-commit BEGIN") == 1

    def test_refuse_foreign_without_mutation(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        hook = _precommit_hook(tmp_path)
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/bin/sh\necho mine\n")
        hook.chmod(0o755)
        before_bytes = hook.read_bytes()
        before_mode = stat.S_IMODE(hook.stat().st_mode)
        res = _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        assert res.returncode == 4, res.stderr
        assert "REFUSING" in res.stderr
        assert hook.read_bytes() == before_bytes
        assert stat.S_IMODE(hook.stat().st_mode) == before_mode

    def test_no_git_target_clear_diagnostic(self, tmp_path) -> None:
        (tmp_path / "tools").mkdir()
        tool = tmp_path / "tools" / "intent.py"
        tool.write_bytes(TOOL_TEMPLATE.read_bytes())
        res = _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        assert res.returncode == 1
        assert "not inside a git working tree" in res.stderr
        assert "Traceback" not in res.stderr

    def test_hooks_status_reports_both(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        _run_tool(tool, ["install-hook"], cwd=tmp_path)
        _run_tool(tool, ["install-precommit"], cwd=tmp_path)
        res = _run_tool(tool, ["hooks-status"], cwd=tmp_path)
        assert "post-commit (auto-release): installed" in res.stdout
        assert "pre-commit (work-intent check): installed" in res.stdout

    def test_status_suggests_installed_command_shape(self, tmp_path) -> None:
        """Codex review P2: the suggested follow-up commands must be the
        installed script shape (`python tools/intent.py ...`), not a bare
        `intent` console command Cairn never installs."""
        tool = _git_repo(tmp_path)
        res = _run_tool(tool, ["hooks-status"], cwd=tmp_path)
        assert "python tools/intent.py install-hook" in res.stdout
        assert "python tools/intent.py install-precommit" in res.stdout
        # No bare `intent <cmd>` suggestion (the non-existent entry point).
        assert "-> install post-commit: intent " not in res.stdout
        assert "-> install pre-commit:  intent " not in res.stdout


class TestPrecommitCheck:
    """The classifier under the real `git diff --cached` staged set."""

    def _log(self, repo: Path) -> Path:
        return repo / "dev" / "intents.jsonl"

    def test_unclaimed_warns(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0
        assert "no active claim" in res.stderr
        assert "dev/a.md" in res.stderr

    def test_claimed_by_this_session_silent(self, tmp_path) -> None:
        # N1: own-claim suppression requires a per-session token (a harness
        # session var) -- a static agent name collides across same-type
        # sessions and cannot prove "own".
        tool = _git_repo(tmp_path)
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-own")
        log = str(self._log(tmp_path))
        _stage(tmp_path, env, "dev/a.md")
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/a.md",
                   "--action", "edit"], cwd=tmp_path, env=env,
        )
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0
        assert res.stderr.strip() == ""

    def test_other_session_warns_even_with_own_claim(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/a.md",
                   "--action", "bob-edit"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        env = _clean_env(CAIRN_AGENT="alice")
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/a.md",
                   "--action", "alice-edit"], cwd=tmp_path, env=env,
        )
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "HELD BY ANOTHER" in res.stderr
        assert "bob" in res.stderr
        assert "no active claim" not in res.stderr  # own claim => not unclaimed

    def test_env_override_suppresses_self_not_other(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/b.md",
                   "--action", "bob"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        env = _clean_env(CAIRN_AGENT="alice", CAIRN_INTENT_ALLOW_UNCLAIMED="1")
        _stage(tmp_path, env, "dev/a.md")  # unclaimed by alice
        _stage(tmp_path, env, "dev/b.md")  # held by bob
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "no active claim" not in res.stderr  # self-nag suppressed
        assert "HELD BY ANOTHER" in res.stderr       # other-session surfaces
        assert "dev/b.md" in res.stderr

    def test_solo_mode_suppresses_self_not_other(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/b.md",
                   "--action", "bob"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        (tmp_path / "dev" / "intent-config.json").write_text(
            '{"solo_mode": true}\n'
        )
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")
        _stage(tmp_path, env, "dev/b.md")
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "no active claim" not in res.stderr
        assert "HELD BY ANOTHER" in res.stderr

    def test_unknown_identity_failsoft(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        env = _clean_env()  # no identity vars resolvable
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0
        assert "UNKNOWN IDENTITY" in res.stderr
        assert "Traceback" not in res.stderr

    def test_identity_agrees_with_autorelease(self, tmp_path) -> None:
        """The pre-commit check resolves the SAME identity the post-commit
        auto-release uses, so a claim made in-session is recognized as own
        and then auto-released on commit."""
        tool = _git_repo(tmp_path)
        # N1: a token-bearing identity (harness session var) so the
        # in-session claim is recognized as own (not the static-name path).
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-own")
        log = str(self._log(tmp_path))
        _run_tool(tool, ["install-hook"], cwd=tmp_path, env=env)
        _stage(tmp_path, env, "dev/a.md")
        _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/a.md",
                   "--action", "x"], cwd=tmp_path, env=env,
        )
        # pre-commit: own claim => silent
        chk = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert chk.stderr.strip() == ""
        # commit (default-log post-commit hook) auto-releases the claim
        subprocess.run(
            ["git", "commit", "-q", "-m", "c"], cwd=tmp_path, check=True,
            env=env,
        )
        after = _run_tool(tool, ["list"], cwd=tmp_path, env=env)
        assert "no active intents" in after.stdout

    def test_path_scoped_commit_sees_only_committed_path(self, tmp_path) -> None:
        """Path-scoped-commit regression: the hook fires against the
        partial temp index `git commit <path>` builds, so it sees only the
        committed path even when another path is also staged."""
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="alice")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env)
        (tmp_path / "dev" / "a.md").write_text("a\n")
        (tmp_path / "dev" / "b.md").write_text("b\n")
        subprocess.run(
            ["git", "add", "dev/a.md", "dev/b.md"], cwd=tmp_path, check=True,
            env=env,
        )
        res = subprocess.run(
            ["git", "commit", "-m", "c", "dev/a.md"],
            cwd=tmp_path, capture_output=True, text=True, env=env,
        )
        # No claims exist (nothing was claimed) + no token, so the
        # block-by-default has nothing to enforce -> the commit proceeds.
        assert res.returncode == 0
        assert "dev/a.md" in res.stderr
        assert "dev/b.md" not in res.stderr  # not in the path-scoped index


class TestEnforceModeAndN1:
    """Layer-2 enforce modes (#53) + the N1 token-gated own-claim match
    (cairn-concurrent-session-coordination)."""

    def _log(self, repo: Path) -> Path:
        return repo / "dev" / "intents.jsonl"

    def _set_enforce(self, repo: Path, mode: str) -> None:
        cfg = repo / "dev" / "intent-config.json"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(json.dumps({"enforce": mode}), encoding="utf-8")

    def _claim_other_session(self, tool: Path, repo: Path, path: str) -> None:
        """File a claim under a DIFFERENT session token (sess-OTHER)."""
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-OTHER")
        _run_tool(
            tool, ["--log-path", str(self._log(repo)), "claim", "--files",
                   path, "--action", "other-work"], cwd=repo, env=env,
        )

    def test_block_refuses_other_session(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        self._set_enforce(tmp_path, "block")
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode != 0
        assert "enforce=block" in res.stderr

    def test_no_config_blocks_cross_claim_by_default(self, tmp_path) -> None:
        """foldback-drain Fold A / R2: the shipped default flipped warn→block.
        With NO ``dev/intent-config.json``, a token-bearing committer facing a
        *different* live session's claim is now refused (not merely warned)."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        # no enforce config at all -> block-on-cross-claim is the default
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode != 0          # default now BLOCKS the cross-claim
        assert "enforce=block" in res.stderr
        assert "HELD BY ANOTHER" in res.stderr  # the warning still surfaces

    def test_explicit_warn_never_blocks_but_surfaces(self, tmp_path) -> None:
        """An adopter opts back into advisory-only with explicit
        ``{"enforce":"warn"}`` -- it surfaces the overlap but never blocks."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        self._set_enforce(tmp_path, "warn")
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0
        assert "HELD BY ANOTHER" in res.stderr  # still surfaced

    def test_bypass_env_overrides_block(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        self._set_enforce(tmp_path, "block")
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        env["CAIRN_INTENT_ALLOW_UNCLAIMED"] = "1"
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0

    def test_static_identity_does_not_suppress_own(self, tmp_path) -> None:
        """N1: a no-token (static agent name) committer cannot prove own, so
        even its own claim surfaces as other-session -- fail-safe over-warn,
        never a silent coordination miss (two same-type sessions would
        otherwise share the static identity and false-suppress)."""
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="alice")  # static name, NO session token
        _stage(tmp_path, env, "dev/a.md")
        _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "claim", "--files",
                   "dev/a.md", "--action", "mine"], cwd=tmp_path, env=env,
        )
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        # Under the block-by-default flip (Fold A), a no-token committer still
        # does NOT block: ownership is unprovable (static identity is shared),
        # so the block is withheld and the overlap only warns -- the
        # misfire-avoidance the proposal names. The warning still surfaces, and
        # the hook emits the explicit "block WITHHELD" downgrade note -- which
        # is what proves the token-gate (not some other path) is why exit is 0.
        assert res.returncode == 0  # no token -> warn-only (not blocked)
        assert "HELD BY ANOTHER" in res.stderr  # NOT suppressed (no token)
        assert "WITHHELD" in res.stderr  # block downgraded, not silently absent

    def test_confirm_no_tty_degrades_to_block(self, tmp_path, monkeypatch) -> None:
        """F4/R2: confirm with no controlling terminal -> block."""
        src = (Path(__file__).resolve().parents[2] / "templates" / "modules"
               / "team-gated" / "intent.py")
        mod = _load_tool(src, name="intent_confirm_unit")
        monkeypatch.setattr(mod, "_confirm_tty", lambda: None)
        assert mod._confirm_proceed() is False


# ---------------------------------------------------------------------------
# Claim TTL (foldback-drain Fold A / R1) + the N3 offset-aware / fail-safe
# parse contract
# ---------------------------------------------------------------------------

def _rewrite_claim_ts(log_path: Path, value: str) -> None:
    """Set every claim record's ``ts`` in *log_path* to *value* (release
    records untouched). Used to age a claim past the TTL or to inject a
    malformed / naive timestamp that exercises the fail-safe parse path."""
    out: list[str] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("event") == "claim":
            rec["ts"] = value
        out.append(json.dumps(rec))
    log_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def _age_claims(log_path: Path, *, hours: float) -> None:
    """Age every claim record's ``ts`` to *hours* ago (offset-aware ISO)."""
    import datetime as _dt
    aged = _dt.datetime.now().astimezone() - _dt.timedelta(hours=hours)
    _rewrite_claim_ts(log_path, aged.isoformat())


class TestClaimTTL:
    """The net-new claim TTL (R1) + N3 offset-aware / fail-safe contract.

    A *stale* (past-TTL) cross-claim still WARNS but never blocks (a crashed /
    abandoned session must not wedge a live committer); a malformed / naive
    timestamp never crashes the hook -- it degrades to non-blocking."""

    def _log(self, repo: Path) -> Path:
        return repo / "dev" / "intents.jsonl"

    def _set_config(self, repo: Path, **kw: object) -> None:
        cfg = repo / "dev" / "intent-config.json"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(json.dumps(kw), encoding="utf-8")

    def _claim_other_session(self, tool: Path, repo: Path, path: str) -> None:
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-OTHER")
        _run_tool(
            tool, ["--log-path", str(self._log(repo)), "claim", "--files",
                   path, "--action", "other-work"], cwd=repo, env=env,
        )

    def test_stale_cross_claim_warns_but_does_not_block(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        _age_claims(self._log(tmp_path), hours=5)  # past the 4h default TTL
        # default enforce=block (no config) -- a stale claim must NOT block
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0           # stale -> not blocked (anti-wedge)
        assert "HELD BY ANOTHER" in res.stderr   # still surfaced as a warning

    def test_fresh_cross_claim_still_blocks(self, tmp_path) -> None:
        """Control: a within-TTL cross-claim DOES block under the default, so
        the stale pass is the TTL working -- not a silently broken block."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        _age_claims(self._log(tmp_path), hours=1)  # within the 4h TTL
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode != 0
        assert "enforce=block" in res.stderr

    def test_configurable_ttl_window(self, tmp_path) -> None:
        """``claim_ttl_hours`` is honored: a 2h-old claim blocks under an 8h
        window but only warns under a 1h window."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        _age_claims(self._log(tmp_path), hours=2)
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        # wide window -> 2h claim is fresh -> blocks
        self._set_config(tmp_path, enforce="block", claim_ttl_hours=8)
        res_wide = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res_wide.returncode != 0
        # narrow window -> 2h claim is stale -> warns only
        self._set_config(tmp_path, enforce="block", claim_ttl_hours=1)
        res_narrow = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res_narrow.returncode == 0
        assert "HELD BY ANOTHER" in res_narrow.stderr

    def test_malformed_ts_does_not_crash_or_block(self, tmp_path) -> None:
        """N3 fail-safe: a malformed (unparseable) ``ts`` degrades to
        non-blocking and never crashes the hook (no traceback)."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        _rewrite_claim_ts(self._log(tmp_path), "not-a-timestamp")
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert res.returncode == 0           # fail-safe: do not block
        assert "Traceback" not in res.stderr  # and never crash the hook

    def test_naive_offset_ts_does_not_crash(self, tmp_path) -> None:
        """N3: a naive (offset-less) old ``ts`` -- the aware/naive mismatch
        that would raise TypeError -- is handled without crashing; an old
        naive ts is treated as stale -> non-blocking."""
        import datetime as _dt
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        naive_old = (_dt.datetime.now() - _dt.timedelta(hours=9)).replace(
            tzinfo=None
        )
        _rewrite_claim_ts(self._log(tmp_path), naive_old.isoformat())
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "Traceback" not in res.stderr
        assert res.returncode == 0           # old naive ts -> stale -> no block

    def test_real_two_session_shared_index_sweep_is_blocked(
        self, tmp_path
    ) -> None:
        """The proposal's FIRST verification step: a real ``git commit`` in a
        shared index, with a *different* live session holding the staged path,
        is refused by the default-block pre-commit hook (no config needed)."""
        tool = _git_repo(tmp_path)
        env_mine = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env_mine)
        # a DIFFERENT live session claims the shared file (default log path,
        # which is exactly what the installed hook reads)
        env_other = _clean_env(CLAUDE_CODE_SESSION_ID="sess-OTHER")
        _run_tool(
            tool, ["claim", "--files", "dev/shared.md", "--action", "other"],
            cwd=tmp_path, env=env_other,
        )
        # MINE stages + commits the claimed path -> the hook must refuse it
        (tmp_path / "dev" / "shared.md").write_text("mine\n")
        subprocess.run(
            ["git", "add", "dev/shared.md"], cwd=tmp_path, check=True,
            env=env_mine,
        )
        res = subprocess.run(
            ["git", "commit", "-m", "sweep"],
            cwd=tmp_path, capture_output=True, text=True, env=env_mine,
        )
        assert res.returncode != 0, "default-block hook must refuse the sweep"
        log = subprocess.run(
            ["git", "log", "--oneline"], cwd=tmp_path,
            capture_output=True, text=True, env=env_mine,
        )
        assert "sweep" not in log.stdout     # the commit did not land


# ---------------------------------------------------------------------------
# Sensing write-path (self-evolution-loop Part B) -- the pre-commit hook
# records a work-intent collision as an incident-trackers row. Best-effort &
# fail-safe (R1); the test drives a REAL git commit through the hook (F2);
# tagging mirrors P4's Design 2 (S4): blocked -> prevented, override ->
# occurred, no-token -> NO incident (unprovable -> would over-count the gate).
# ---------------------------------------------------------------------------

class TestSensingWritePath:
    def _log(self, repo: Path) -> Path:
        return repo / "dev" / "intents.jsonl"

    def _claim_other(self, tool: Path, repo: Path, path: str) -> None:
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-OTHER")
        _run_tool(
            tool, ["--log-path", str(self._log(repo)), "claim", "--files",
                   path, "--action", "other"], cwd=repo, env=env,
        )

    def _tracker(self, repo: Path) -> Path:
        return repo / "dev" / "measurement" / "collision_log.md"

    def test_block_records_prevented_real_commit(self, tmp_path) -> None:
        """F2: a real `git commit` blocked by the default-block hook records a
        `prevented` incident row (the collision was caught by the gate)."""
        tool = _git_repo(tmp_path)
        env_mine = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env_mine)
        self._claim_other(tool, tmp_path, "dev/shared.md")
        (tmp_path / "dev" / "shared.md").write_text("mine\n")
        subprocess.run(["git", "add", "dev/shared.md"], cwd=tmp_path,
                       check=True, env=env_mine)
        res = subprocess.run(
            ["git", "commit", "-m", "sweep"], cwd=tmp_path,
            capture_output=True, text=True, env=env_mine,
        )
        assert res.returncode != 0  # blocked
        tracker = self._tracker(tmp_path)
        assert tracker.is_file(), "incident tracker should be auto-created"
        txt = tracker.read_text()
        assert "| prevented |" in txt
        assert "work-intent-claim-conflict" in txt
        assert "dev/shared.md" in txt
        assert "| direct | pending |" in txt   # auto-write provenance

    def test_no_token_collision_records_no_incident(self, tmp_path) -> None:
        """A no-token committer's overlap is unprovable -> WITHHELD, and NO
        incident is recorded (tagging it would over-count the gate)."""
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="alice")  # static name, no session token
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env)
        self._claim_other(tool, tmp_path, "dev/shared.md")
        (tmp_path / "dev" / "shared.md").write_text("mine\n")
        subprocess.run(["git", "add", "dev/shared.md"], cwd=tmp_path,
                       check=True, env=env)
        res = subprocess.run(
            ["git", "commit", "-m", "c"], cwd=tmp_path,
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 0          # no-token -> warn-only, proceeds
        assert "WITHHELD" in res.stderr
        assert not self._tracker(tmp_path).exists()  # NO incident recorded

    def test_clean_commit_records_no_incident(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env)
        (tmp_path / "dev" / "a.md").write_text("x\n")
        subprocess.run(["git", "add", "dev/a.md"], cwd=tmp_path, check=True,
                       env=env)
        res = subprocess.run(
            ["git", "commit", "-m", "c"], cwd=tmp_path,
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 0
        assert not self._tracker(tmp_path).exists()

    def test_record_failure_does_not_break_the_block(self, tmp_path) -> None:
        """R1: a recording failure (unwritable log path) must NOT change the
        enforce decision and must NOT crash the hook -- it warns visibly (F4)
        and the commit is still blocked."""
        tool = _git_repo(tmp_path)
        env_mine = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env_mine)
        # A file where a directory is needed -> tracker create/insert fails.
        (tmp_path / "dev" / "blocker").write_text("x")
        (tmp_path / "dev" / "intent-config.json").write_text(
            '{"incident_log_path": "dev/blocker/nope.md"}'
        )
        self._claim_other(tool, tmp_path, "dev/shared.md")
        (tmp_path / "dev" / "shared.md").write_text("mine\n")
        subprocess.run(["git", "add", "dev/shared.md"], cwd=tmp_path,
                       check=True, env=env_mine)
        res = subprocess.run(
            ["git", "commit", "-m", "x"], cwd=tmp_path,
            capture_output=True, text=True, env=env_mine,
        )
        assert res.returncode != 0              # block still fires
        assert "Traceback" not in res.stderr    # never crashes
        assert "could not record" in res.stderr  # F4: visible skip

    def test_confirm_ack_records_occurred(self, tmp_path, monkeypatch) -> None:
        """A confirm-acknowledged proceed past a different live session's claim
        records an `occurred` incident (the override the gate counts)."""
        tool = _git_repo(tmp_path)
        self._claim_other(tool, tmp_path, "dev/a.md")
        (tmp_path / "dev" / "intent-config.json").write_text('{"enforce":"confirm"}')
        env_mine = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        (tmp_path / "dev" / "a.md").write_text("x\n")
        subprocess.run(["git", "add", "dev/a.md"], cwd=tmp_path, check=True,
                       env=env_mine)
        mod = _load_tool(tool, name="intent_occurred_unit")
        monkeypatch.setattr(mod, "_confirm_proceed", lambda: True)
        for v in _IDENTITY_VARS:
            monkeypatch.delenv(v, raising=False)
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-MINE")
        monkeypatch.chdir(tmp_path)

        class _Args:
            log_path = str(tmp_path / "dev" / "intents.jsonl")
            paths_from_file = None

        rc = mod._precommit_check_impl(_Args())
        assert rc == 0  # confirm-ack proceeds
        tracker = self._tracker(tmp_path)
        assert tracker.is_file()
        assert "| occurred |" in tracker.read_text()

    def test_two_incidents_both_land_in_the_table(self, tmp_path) -> None:
        """Table insertion stays inside the `## Incidents` table across writes;
        the header is not duplicated and trailing content is not displaced."""
        mod = _load_tool(TOOL_TEMPLATE, name="intent_tableunit")
        mod._record_incident(tmp_path, impact="prevented", description="first")
        mod._record_incident(tmp_path, impact="occurred", description="second")
        txt = self._tracker(tmp_path).read_text()
        assert txt.count("| direct | pending |") == 2
        assert txt.count("| Date | Event Class |") == 1  # header once
