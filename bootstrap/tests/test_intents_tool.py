"""
Tests for the work-intent tool (coordination-tiers).

Covers, per the executing plan (cairn-v0.2-p5-intents-tool):

* install-path: the tool lands verbatim in ``tools/intent.py``; the
  ``.md`` doctrine lands in ``dev/modules/``; ``.gitignore`` is seeded;
  skip-if-exists / ``--force`` respected.
* ``.gitignore`` seeding is non-clobber, idempotent, ``--dry-run``
  aware.
* identity resolves via ``CAIRN_AGENT`` override, the built-in
  harness registry, an **adopter-supplied** registry entry (the
  portability contract), and a static config ``agent``.
* P-3: a ``CAIRN_AGENT`` override that shadows an available harness
  session var emits a warning.
* the post-commit hook installer chains onto a plain hook and
  **refuses without mutation** (bytes + mode unchanged) for
  framework-managed / non-shell / non-executable hooks.
* the generated hook captures the install-time interpreter, and the
  full claim -> commit -> auto-release arc works off the CLI.
* install-hook on a no-git target degrades with a clear diagnostic,
  not a stack trace; a ``main``-default repo works.
* the installed tool and the generated hook carry no
  modflow_tools residue.
* the installed tool is standard-library only (no ``yaml`` import).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import ast
import os
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType

import pytest

# Allow tests to import scaffold without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _GITIGNORE_SEEDS,
    _MODULE_MAPPINGS,
    ScaffoldSecurityError,
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


def _stage_tool(tools_dir: Path) -> Path:
    """Install the intent facade + its sibling ``_intent/`` engine package into
    *tools_dir*.

    Intent-split (phase A): ``intent.py`` is a thin facade that loads ``_intent/``
    as a runtime sibling, so a faithful copy of the tool must stage **both** — the
    scaffold install mapping does the same. (Pre-split this was a single
    ``intent.py`` write; the assertions exercised below are unchanged.)
    """
    import shutil
    tools_dir.mkdir(parents=True, exist_ok=True)
    facade = tools_dir / "intent.py"
    facade.write_bytes(TOOL_TEMPLATE.read_bytes())
    pkg_dst = tools_dir / "_intent"
    if pkg_dst.exists():
        shutil.rmtree(pkg_dst)
    shutil.copytree(TOOL_TEMPLATE.parent / "_intent", pkg_dst)
    return facade


# An isolated, provably-empty HOME for subprocess envs.  Identity tier 3 is
# ``$HOME/.cairn/agent.json`` (``identity._load_config``), so a developer who
# has that file -- an ordinary, documented setup -- would otherwise resolve a
# real identity inside tests whose whole premise is that none is resolvable,
# turning them red on their machine and green in CI.  Git needs no HOME here:
# ``_git_repo`` sets user.name / user.email per-repo, not from ~/.gitconfig.
_ISOLATED_HOME = tempfile.mkdtemp(prefix="cairn-test-home-")


def _clean_env(**overrides: str) -> dict:
    """A subprocess env with identity vars cleared, then *overrides*."""
    env = dict(os.environ)
    for var in _IDENTITY_VARS:
        env.pop(var, None)
    env["HOME"] = _ISOLATED_HOME
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
    (tmp_path / "dev").mkdir(exist_ok=True)
    return _stage_tool(tmp_path / "tools")


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
        verbatim tool .py (1:many)."""
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
# .gitignore seeding contract
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
# .gitignore seeding never writes through a link
# ---------------------------------------------------------------------------

#: What a hostile checkout could make the seed append to if it followed a link:
#: a stand-in for a file elsewhere on the machine (a shell startup file, say).
_OUTSIDE_BYTES = b"# a file that belongs to someone else\nalias ll='ls -l'\n"


class TestGitignoreSeedingRefusesLinks:
    """``seed_gitignore`` routes its write through the engine's containment
    guard, like every other write into the target. A ``.gitignore`` that is a
    link is refused -- whether it points outside the target or inside it -- and
    the file behind the link is left byte-for-byte alone."""

    @staticmethod
    def _linked_gitignore(tmp_path: Path, *, inside: bool) -> tuple[Path, Path]:
        """A target whose ``.gitignore`` is a link; returns (target, file behind it)."""
        target = tmp_path / "tgt"
        target.mkdir()
        if inside:
            (target / "dev").mkdir()
            behind = target / "dev" / "shared.gitignore"
            link_to = Path("dev") / "shared.gitignore"  # relative, stays in the tree
        else:
            behind = tmp_path / "elsewhere" / "startup-file"
            behind.parent.mkdir()
            link_to = behind
        behind.write_bytes(_OUTSIDE_BYTES)
        (target / ".gitignore").symlink_to(link_to)
        return target, behind

    @staticmethod
    def _install(target: Path, *extra: str) -> int:
        cfg = target / "profile.yml"
        cfg.write_text(
            "project_name: LinkTest\ntest_command: pytest\nmodules:\n"
            "  - coordination-tiers\n"
        )
        return main(
            ["--config", str(cfg), "--target", str(target),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev", *extra]
        )

    @pytest.mark.parametrize("inside", [False, True], ids=["outside", "inside"])
    @pytest.mark.parametrize("dry_run", [False, True], ids=["write", "dry-run"])
    def test_seed_refuses_a_linked_gitignore(
        self, tmp_path: Path, inside: bool, dry_run: bool
    ) -> None:
        target, behind = self._linked_gitignore(tmp_path, inside=inside)
        with pytest.raises(ScaffoldSecurityError, match="symlinked destination"):
            seed_gitignore(target, ("dev/intents.jsonl",), dry_run=dry_run)
        assert behind.read_bytes() == _OUTSIDE_BYTES
        assert (target / ".gitignore").is_symlink()

    def test_install_through_a_link_to_an_outside_file_exits_2(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        target, outside = self._linked_gitignore(tmp_path, inside=False)
        rc = self._install(target)
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "refus" in err and "symlinked destination" in err
        assert str(target / ".gitignore") in err
        assert outside.read_bytes() == _OUTSIDE_BYTES, (
            "the install appended to a file outside the target through the link"
        )

    def test_install_through_a_link_to_a_file_inside_the_target_exits_2(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The guard's rule is one rule for every destination: a link is
        refused wherever it points. Following in-tree links would mean judging
        the final destination of a link chain here, a second rule for one
        function; an adopter whose ``.gitignore`` is a link replaces it with a
        real file and re-runs."""
        target, behind = self._linked_gitignore(tmp_path, inside=True)
        rc = self._install(target)
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "symlinked destination" in err
        assert behind.read_bytes() == _OUTSIDE_BYTES
        assert (target / ".gitignore").is_symlink()

    def test_dry_run_install_predicts_the_refusal(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A dry run that printed "Would seed .gitignore" for a file the real
        run refuses would promise something the install does not do."""
        target, outside = self._linked_gitignore(tmp_path, inside=False)
        rc = self._install(target, "--dry-run")
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "symlinked destination" in err
        assert outside.read_bytes() == _OUTSIDE_BYTES


# ---------------------------------------------------------------------------
# Identity resolution
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
# Auto-release stays quiet when there is provably nothing to release (#3)
# ---------------------------------------------------------------------------

class TestAutoReleaseQuietOnNoClaims:
    """The unresolved-identity warning is gated on there being live claims.

    A human committing from an ordinary terminal fails identity resolution
    *by construction* -- the harness session vars exist only inside an agent
    harness -- so an ungated warning fires on every hand-made commit, and
    once per replayed commit through a rebase, while auto-release is a
    provable no-op. The warning is retained for the case it was written for:
    live claims whose holder cannot be named.
    """

    def _paths_file(self, tmp_path: Path) -> Path:
        paths = tmp_path / "paths"
        paths.write_bytes(b"dev/x\x00")
        return paths

    def test_silent_when_no_claims_and_no_identity(self, tmp_path) -> None:
        """The reported defect: nothing claimed => no identity warning."""
        tool = _git_repo(tmp_path)
        log = tmp_path / "intents.jsonl"  # deliberately absent -> reads as []
        res = _run_tool(
            tool,
            ["--log-path", str(log), "_auto_release", "--commit", "abc0123456",
             "--paths-from-file", str(self._paths_file(tmp_path))],
            cwd=tmp_path, env=_clean_env(),
        )
        assert res.returncode == 0  # always fail-soft
        assert "agent identity not configured" not in res.stderr
        assert res.stderr == ""  # silent, not merely un-warned

    def test_still_warns_when_a_live_claim_cannot_be_released(
        self, tmp_path
    ) -> None:
        """Non-vacuity: the warning survives for the case it was written for."""
        tool = _git_repo(tmp_path)
        log = tmp_path / "intents.jsonl"
        # A live claim held by someone this committer cannot be resolved as.
        _run_tool(
            tool,
            ["--log-path", str(log), "claim", "--files", "dev/x",
             "--action", "held-by-another-session"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="other-session"),
        )
        res = _run_tool(
            tool,
            ["--log-path", str(log), "_auto_release", "--commit", "abc0123456",
             "--paths-from-file", str(self._paths_file(tmp_path))],
            cwd=tmp_path, env=_clean_env(),  # no identity resolvable
        )
        assert res.returncode == 0
        assert "agent identity not configured" in res.stderr


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
# Hook diversity + refusal-before-mutation
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
        (security hardening)."""
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
# VCS robustness
# ---------------------------------------------------------------------------

class TestVcsRobustness:
    def test_no_git_target_clear_diagnostic(self, tmp_path) -> None:
        tool = _stage_tool(tmp_path / "tools")
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
# Interpreter contract + end-to-end auto-release
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
        """The ACTUAL generated hook (not just the CLI) releases the
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
# Literal audit (no modflow_tools residue)
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
# stdlib-only (no PyYAML)
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
        """The dropped YAML config tier leaves no `yaml` reference --
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
        tool = _stage_tool(tmp_path / "tools")
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
        """The suggested follow-up commands must be the
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
        # Own-claim suppression requires a per-session token (a harness
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

    def test_solo_mode_read_from_canonical_cairn_path(self, tmp_path) -> None:
        """The intent config is read from the canonical ``dev/.cairn/`` location
        (the ``dev/.cairn/`` holds-config convention), not only legacy
        ``dev/intent-config.json`` (rollup #2)."""
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        (tmp_path / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (tmp_path / "dev" / ".cairn" / "intent-config.json").write_text(
            '{"solo_mode": true}\n'
        )
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")  # unclaimed by alice
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "no active claim" not in res.stderr  # canonical solo_mode read

    def test_intent_config_prefers_canonical_over_legacy(self, tmp_path) -> None:
        """When both files exist, the canonical ``dev/.cairn/`` value wins
        (prefer-new), so an adopter can migrate without deleting the old file
        (rollup #2)."""
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        # Legacy says NOT solo; canonical says solo -> canonical must win.
        (tmp_path / "dev" / "intent-config.json").write_text(
            '{"solo_mode": false}\n'
        )
        (tmp_path / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (tmp_path / "dev" / ".cairn" / "intent-config.json").write_text(
            '{"solo_mode": true}\n'
        )
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "no active claim" not in res.stderr  # canonical (true) preferred

    def test_intent_config_legacy_fallback_when_no_canonical(
        self, tmp_path
    ) -> None:
        """With no canonical file, the legacy ``dev/intent-config.json`` is the
        transitional fallback -- an existing adopter is not broken (rollup #2)."""
        tool = _git_repo(tmp_path)
        log = str(self._log(tmp_path))
        (tmp_path / "dev" / "intent-config.json").write_text(
            '{"solo_mode": true}\n'
        )
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")
        res = _run_tool(
            tool, ["--log-path", log, "_precommit_check"],
            cwd=tmp_path, env=env,
        )
        assert "no active claim" not in res.stderr  # legacy fallback read

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
        # A token-bearing identity (harness session var) so the
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
    """Layer-2 enforce modes (#53) + the token-gated own-claim match
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
        """The shipped default flipped warn→block.
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
        """A no-token (static agent name) committer cannot prove own, so
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
        """Confirm with no controlling terminal -> block."""
        src = (Path(__file__).resolve().parents[2] / "templates" / "modules"
               / "team-gated" / "intent.py")
        mod = _load_tool(src, name="intent_confirm_unit")
        monkeypatch.setattr(mod, "_confirm_tty", lambda: None)
        assert mod._confirm_proceed() is False


# ---------------------------------------------------------------------------
# Claim TTL + the offset-aware / fail-safe
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
    """The net-new claim TTL + offset-aware / fail-safe contract.

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
        """Fail-safe: a malformed (unparseable) ``ts`` degrades to
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
        """A naive (offset-less) old ``ts`` -- the aware/naive mismatch
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
# fail-safe; the test drives a REAL git commit through the hook;
# tagging mirrors the recorded design: blocked -> prevented, override ->
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
        """A real `git commit` blocked by the default-block hook records a
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
        """A recording failure (unwritable log path) must NOT change the
        enforce decision and must NOT crash the hook -- it warns visibly
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
        assert "could not record" in res.stderr  # visible skip

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


# ---------------------------------------------------------------------------
# Pruning the coordination surface
# (proposal 2026-08-11-claude-intent-ledger-pruning, accepted; deliberation
# compressed to internal, so the acceptance criteria live here.)
#
# The intent log is a coordination surface, not an archive. Three invariants
# make pruning safe, and each has a mutant below:
#   Pairwise only -- a lone release would RESURRECT its claim as active
#   [H2] an unreleased claim is reported, never deleted (it is a dead lock)
#   [H3] an unparseable line is preserved (read_log skips them; a rebuild
#        from parsed records would silently delete them)
# ---------------------------------------------------------------------------

_DAY = 86400.0


def _ts(days_ago: float) -> str:
    import datetime as _dt
    return (_dt.datetime.now(_dt.timezone.utc)
            - _dt.timedelta(days=days_ago)).isoformat()


def _ledger(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows),
        encoding="utf-8",
    )
    return path


def _corpus(path: Path) -> Path:
    """Released-old (prunable), released-recent (kept), unreleased-old
    (reported), plus a deliberately malformed line."""
    _ledger(path, [
        {"event": "claim", "id": "old-1", "ts": _ts(45), "agent": "a",
         "files": ["x.md"], "action": "old work"},
        {"event": "release", "id": "old-1", "ts": _ts(44)},
        {"event": "claim", "id": "new-1", "ts": _ts(3), "agent": "b",
         "files": ["y.md"], "action": "recent work"},
        {"event": "release", "id": "new-1", "ts": _ts(2)},
        {"event": "claim", "id": "dead-1", "ts": _ts(40), "agent": "c",
         "files": ["z.md"], "action": "died holding this"},
    ])
    with path.open("a", encoding="utf-8") as fh:
        fh.write("{ this line is not json\n")
    return path


def _engine(tools_dir: Path):
    """Load the staged engine's record_io (the TEMPLATE copy, which is what
    the shipped tool is -- never the repo's own tools/ twin)."""
    sys.path.insert(0, str(tools_dir))
    try:
        import importlib
        for name in [n for n in list(sys.modules) if n.startswith("_intent")]:
            del sys.modules[name]
        return importlib.import_module("_intent.record_io")
    finally:
        sys.path.remove(str(tools_dir))


class TestIntentSurfacePruning:
    def test_h1_a_prune_cannot_change_the_active_set(self, tmp_path: Path) -> None:
        """THE load-bearing invariant. active_intents = claims minus released
        ids; a prune that removed a release without its claim would resurrect
        that claim as active and block its paths forever."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        before = {c["id"] for c in ri.active_intents(log_path=log)}
        ri.prune_released_pairs(older_than_days=30, log_path=log)
        after = {c["id"] for c in ri.active_intents(log_path=log)}
        assert before == after == {"dead-1"}

    def test_h1_mutant_pruning_a_lone_release_resurrects_the_claim(
        self, tmp_path: Path,
    ) -> None:
        """Proves the invariant above is not vacuous, by hand-building the
        exact corruption the implementation refuses to produce: drop the
        release line only, and the claim comes back as active."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        before = {c["id"] for c in ri.active_intents(log_path=log)}
        kept = [ln for ln in log.read_text(encoding="utf-8").splitlines(True)
                if '"event": "release", "id": "old-1"' not in ln
                and '"id": "old-1"' not in ln or '"event": "claim"' in ln]
        log.write_text("".join(kept), encoding="utf-8")
        after = {c["id"] for c in ri.active_intents(log_path=log)}
        assert "old-1" in after and "old-1" not in before, (
            "the resurrection this invariant guards against must be real"
        )

    def test_h2_an_unreleased_old_claim_is_reported_not_deleted(
        self, tmp_path: Path,
    ) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert [e["id"] for e in rep["stale_unreleased"]] == ["dead-1"]
        assert '"dead-1"' in log.read_text(encoding="utf-8")

    def test_h3_an_unparseable_line_survives(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert rep["unparseable_kept"] == 1
        assert "this line is not json" in log.read_text(encoding="utf-8")

    def test_only_the_old_released_pair_leaves(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        body = log.read_text(encoding="utf-8")
        assert rep["pruned_pairs"] == 1 and rep["pruned_lines"] == 2
        assert "old-1" not in body          # both records gone
        assert '"new-1"' in body            # inside the window, kept

    def test_it_refuses_while_a_recent_claim_is_unreleased(
        self, tmp_path: Path
    ) -> None:
        """A *recent* unreleased claim means a live session may still be appending
        to the file this rewrites, so the prune refuses rather than risk the
        window.  The refusal is scoped to the liveness horizon, **not** to "any
        active claim" -- every unreleased claim is active, so that reading would
        refuse forever.  What a missed window costs is one advisory collision
        record, not mutual exclusion (see ``prune_released_pairs``' docstring)."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _ledger(tmp_path / "dev" / "intents.jsonl", [
            {"event": "claim", "id": "old-1", "ts": _ts(45), "agent": "a",
             "files": ["x.md"], "action": "old"},
            {"event": "release", "id": "old-1", "ts": _ts(44)},
            {"event": "claim", "id": "live", "ts": _ts(0.01), "agent": "b",
             "files": ["y.md"], "action": "in flight"},
        ])
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert rep["refused"] and rep["pruned_pairs"] == 0
        assert "old-1" in log.read_text(encoding="utf-8")

    def test_dry_run_writes_nothing(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        before = log.read_bytes()
        rep = ri.prune_released_pairs(
            older_than_days=30, log_path=log, dry_run=True)
        assert rep["pruned_pairs"] == 1 and log.read_bytes() == before

    def test_prune_is_idempotent(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        ri.prune_released_pairs(older_than_days=30, log_path=log)
        once = log.read_bytes()
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert rep["pruned_pairs"] == 0 and log.read_bytes() == once

    def test_an_unparseable_timestamp_is_kept_not_dropped(
        self, tmp_path: Path,
    ) -> None:
        """Fail-safe direction: the cost of keeping a record is bytes, the cost
        of dropping one is a lock."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _ledger(tmp_path / "dev" / "intents.jsonl", [
            {"event": "claim", "id": "bad-ts", "ts": "not-a-date", "agent": "a",
             "files": ["x.md"], "action": "x"},
            {"event": "release", "id": "bad-ts", "ts": "also-not-a-date"},
        ])
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert rep["pruned_pairs"] == 0
        assert "bad-ts" in log.read_text(encoding="utf-8")

    def test_no_temp_file_is_left_behind(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        ri.prune_released_pairs(older_than_days=30, log_path=log)
        leftovers = list(log.parent.glob("*.prune-tmp"))
        assert leftovers == [], f"temp file left: {leftovers}"

    def test_absent_ledger_is_a_no_op(self, tmp_path: Path) -> None:
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        missing = tmp_path / "dev" / "nope.jsonl"
        rep = ri.prune_released_pairs(older_than_days=30, log_path=missing)
        assert rep["pruned_pairs"] == 0 and not missing.exists()

    def test_the_cli_exposes_prune_with_a_dry_run(self, tmp_path: Path) -> None:
        """End to end through the shipped facade, not the engine directly."""
        repo = tmp_path
        tool = _git_repo(tmp_path)
        _corpus(repo / "dev" / "intents.jsonl")
        proc = _run_tool(tool, ["prune", "--older-than-days", "30",
                                "--dry-run"], cwd=repo)
        assert proc.returncode == 0, proc.stderr
        assert "would prune 1 released pair" in proc.stdout, proc.stdout
        assert "NEVER RELEASED" in proc.stdout, proc.stdout

    def test_cr2_a_hostile_symlink_at_the_temp_path_cannot_be_truncated(
        self, tmp_path: Path,
    ) -> None:
        """A regression guard. The original fixed `.prune-tmp` name written via
        Path.write_text FOLLOWED a pre-existing symlink: the link target was
        truncated to zero bytes and os.replace then made the ledger itself the
        symlink. O_EXCL|O_NOFOLLOW on a unique name closes both."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        outside = tmp_path / "outside.txt"
        outside.write_text("DO NOT CHANGE\n", encoding="utf-8")
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        os.symlink(str(outside), str(log.with_name(log.name + ".prune-tmp")))
        ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert outside.read_text(encoding="utf-8") == "DO NOT CHANGE\n"
        assert not log.is_symlink()
        assert list(log.parent.glob("*.tmp")) == []

    def test_cr2_an_existing_file_at_the_temp_path_refuses(
        self, tmp_path: Path,
    ) -> None:
        """O_EXCL: an occupied temp path is a refusal, never an overwrite."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        squatter = log.with_name(f"{log.name}.prune-{os.getpid()}.tmp")
        squatter.write_text("occupied\n", encoding="utf-8")
        before = log.read_bytes()
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        assert rep["refused"] and rep["pruned_pairs"] == 0
        assert log.read_bytes() == before
        assert squatter.read_text(encoding="utf-8") == "occupied\n"

    def test_cr1_a_ledger_that_changed_mid_prune_skips_instead_of_dropping(
        self, tmp_path: Path,
    ) -> None:
        """Narrowed, not closed. A concurrent append between snapshot and
        replace would not survive the replace; the pre-replace size check turns
        that into a skipped prune. Simulated by growing the file after the
        snapshot via a monkeypatched stat-time append."""
        ri = _engine(_stage_tool(tmp_path / "tools").parent)
        log = _corpus(tmp_path / "dev" / "intents.jsonl")
        before = log.read_bytes()
        real_replace = os.replace

        def _grow_then_replace(src, dst):  # the racing appender
            with open(dst, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"event": "claim", "id": "racer",
                                     "ts": _ts(0.001), "agent": "r",
                                     "files": ["q"], "action": "race"}) + "\n")
            return real_replace(src, dst)

        # Grow the file BEFORE the size re-check by appending first.
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"event": "claim", "id": "racer",
                                 "ts": _ts(0.001), "agent": "r",
                                 "files": ["q"], "action": "race"}) + "\n")
        rep = ri.prune_released_pairs(older_than_days=30, log_path=log)
        # The racer is a fresh unreleased claim, so the liveness guard refuses
        # first -- which is the outer of the two protections. Either refusal is
        # correct; what must never happen is a silent drop.
        assert rep["refused"], rep
        assert b"racer" in log.read_bytes()
        assert before in log.read_bytes()
