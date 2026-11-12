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

Promises:
- `claim`, `release` and `list` keep an append-only log; release takes an exact claim id and refuses an unknown one, naming the closest real id.
- Install writes the tool to tools/intent.py, the doctrine to dev/modules/, and seeds .gitignore without clobbering or duplicating lines.
- Install and module adoption refuse to write through a link, and write nothing when they refuse.
- `install-hook` and `install-precommit` refuse a foreign hook without changing it; `--uninstall` removes only Cairn's block.
- The pre-commit check warns on unclaimed staged paths and blocks only a fresh overlap with a different live session, per the configured enforce mode.
- A claim older than the TTL warns but never blocks; the bypass variable overrides a block, and solo_mode never silences the other-session warning.
- `prune` drops only released claim/release pairs older than the grace window; it never drops an unreleased claim or an unparseable line.
- The installed tool uses only the Python standard library.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import ast
import hashlib
import os
import importlib.util
import json
import shutil
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
    _DEV_DIRS,
    _GITIGNORE_SEEDS,
    _MODULE_MAPPINGS,
    ScaffoldSecurityError,
    create_dev_tree,
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
    as a runtime sibling, and its verified Git reader is a fixed sibling under
    ``tools/``. A faithful copy stages the engine and helper as scaffold does.
    (Pre-split this was a single
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
    (tools_dir / "git_read.py").write_bytes(
        (TEMPLATES_ROOT / "skills" / "_lib" / "git_read.py").read_bytes()
    )
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


def _git_repo(tmp_path: Path, *, branch: str = "master",
              git_executable: str | None = None) -> Path:
    """Create a git repo at *tmp_path* with the tool at tools/intent.py."""
    git = git_executable or "git"
    subprocess.run(
        [git, "init", "-q"], cwd=tmp_path, check=True, env=_clean_env(),
    )
    # Rename the initial branch deterministically (init.defaultBranch
    # varies across git versions).
    subprocess.run(
        [git, "symbolic-ref", "HEAD", f"refs/heads/{branch}"],
        cwd=tmp_path, check=True, env=_clean_env(),
    )
    subprocess.run([git, "config", "user.email", "t@t"], cwd=tmp_path,
                   check=True, env=_clean_env())
    subprocess.run([git, "config", "user.name", "t"], cwd=tmp_path,
                   check=True, env=_clean_env())
    (tmp_path / "dev").mkdir(exist_ok=True)
    return _stage_tool(tmp_path / "tools")


@pytest.mark.parametrize(
    "entry_source",
    [
        CAIRN_ROOT / "tools" / "_intent" / "conflict.py",
        TEMPLATES_ROOT / "modules" / "team-gated" / "_intent" / "conflict.py",
    ],
    ids=["tools-intent-conflict", "shipped-intent-conflict"],
)
def test_each_physical_intent_conflict_entry_binds_helper_before_git(
        tmp_path: Path, entry_source: Path) -> None:
    """Exercise each physical conflict owner through the installed hook command."""
    helper = TEMPLATES_ROOT / "skills" / "_lib" / "git_read.py"
    helper_bytes = helper.read_bytes()
    entry_bytes = entry_source.read_bytes()
    binding_compare = b"if hashlib.sha256(source).hexdigest() != _GIT_READ_SHA256:"
    assert entry_bytes.count(binding_compare) == 1

    repo = tmp_path / "repo"
    repo.mkdir()
    tool = _git_repo(repo)
    assert (repo / "tools" / "git_read.py").read_bytes() == helper_bytes
    conflict_path = repo / "tools" / "_intent" / "conflict.py"
    conflict_path.write_bytes(entry_bytes)
    helper_path = repo / "tools" / "git_read.py"

    decoy_marker = tmp_path / "intent-cwd-decoy-ran"
    (repo / "git_read.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(decoy_marker)!r}).write_text('ran')\n",
        encoding="utf-8",
    )

    # Positive control: the fixed installed entry and canonical sibling helper
    # complete the real pre-commit command in a clean, empty repository.
    good = _run_tool(tool, ["_precommit_check"], cwd=repo)
    assert good.returncode == 0, good.stderr
    assert "Git read helper binding failed" not in good.stderr
    assert not decoy_marker.exists()

    marker = tmp_path / "tampered-helper-executed"
    git_probe_marker = tmp_path / "intent-git-probed-before-binding"
    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    fake_git = fake_bin / "git"
    fake_git.write_text(
        f"#!{sys.executable}\n"
        "from pathlib import Path\n"
        f"Path({str(git_probe_marker)!r}).write_text('ran')\n"
        "raise SystemExit(1)\n",
        encoding="utf-8",
    )
    fake_git.chmod(0o755)
    probe_env = _clean_env(
        PATH=str(fake_bin) + os.pathsep + os.environ.get("PATH", ""),
    )
    malicious = (
        "from pathlib import Path\n"
        "from types import SimpleNamespace\n"
        f"Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
        "def bind_verified_source(source, digest):\n    return None\n"
        "def run_git(root, args, **kwargs):\n"
        "    return SimpleNamespace(state='completed', returncode=0, "
        "stdout=(root + '\\n').encode(), stderr=b'')\n"
        "def read_hook_index(root, args, **kwargs):\n"
        "    return SimpleNamespace(state='completed', returncode=0, "
        "stdout=b'', stderr=b'')\n"
    ).encode("utf-8")

    # In-process cache substitution after one verified call retains the
    # already-bound module and never executes the replacement bytes.
    cache_marker = tmp_path / "intent-cache-replacement-ran"
    cache_payload = (
        "from pathlib import Path\n"
        f"Path({str(cache_marker)!r}).write_text('ran')\n"
    ).encode("utf-8")
    cache_script = (
        "import sys\nfrom pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "from tools.intent import _git_toplevel\n"
        "root = Path(sys.argv[1])\n"
        "assert _git_toplevel() == root\n"
        "Path(sys.argv[2]).write_bytes(bytes.fromhex(sys.argv[4]))\n"
        "assert _git_toplevel() == root\n"
        "assert not Path(sys.argv[3]).exists()\n"
    )
    cached = subprocess.run(
        [sys.executable, "-c", cache_script, str(repo), str(helper_path),
         str(cache_marker), cache_payload.hex()],
        cwd=repo, capture_output=True, text=True, env=_clean_env(),
    )
    assert cached.returncode == 0, cached.stderr
    assert not cache_marker.exists()

    # Missing and linked helper leaves both become unknown; the physical
    # marker-bearing payload stays inert in each case.
    helper_path.unlink()
    missing = _run_tool(tool, ["_precommit_check"], cwd=repo, env=probe_env)
    assert missing.returncode == 0
    assert "staged path discovery is unavailable" in missing.stderr
    assert not marker.exists()
    assert not git_probe_marker.exists()
    helper_path.write_bytes(helper_bytes)

    linked_source = tmp_path / "linked-intent-git-read.py"
    linked_source.write_bytes(malicious)
    helper_path.unlink()
    try:
        helper_path.symlink_to(linked_source)
    except OSError:
        helper_path.write_bytes(helper_bytes)
    else:
        linked = _run_tool(tool, ["_precommit_check"], cwd=repo, env=probe_env)
        assert linked.returncode == 0
        assert "staged path discovery is unavailable" in linked.stderr
        assert not marker.exists()
        assert not git_probe_marker.exists()
        helper_path.unlink()
        helper_path.write_bytes(helper_bytes)

    helper_path.write_bytes(malicious)

    # The actual generated-tool entry fails closed at the binding layer. The
    # command's documented policy reports the failure and allows the hook.
    rejected = _run_tool(tool, ["_precommit_check"], cwd=repo, env=probe_env)
    assert rejected.returncode == 0
    assert "staged path discovery is unavailable" in rejected.stderr
    assert not marker.exists()
    assert not git_probe_marker.exists()

    # The literal source pin itself is a distinct guard. A mismatched record
    # refuses the canonical helper before any helper byte executes.
    digest = hashlib.sha256(helper_bytes).hexdigest().encode("ascii")
    pin = b'_GIT_READ_SHA256 = "' + digest + b'"'
    assert entry_bytes.count(pin) == 1
    conflict_path.write_bytes(entry_bytes.replace(
        pin, b'_GIT_READ_SHA256 = "' + b"0" * 64 + b'"'))
    helper_path.write_bytes(helper_bytes)
    wrong_pin = _run_tool(tool, ["_precommit_check"], cwd=repo, env=probe_env)
    assert wrong_pin.returncode == 0
    assert "staged path discovery is unavailable" in wrong_pin.stderr
    assert not marker.exists()
    assert not git_probe_marker.exists()

    # Mutate this physical source/twin copy only: bypassing its digest guard
    # must trip the same marker that was inert under the verified entry.
    conflict_path.write_bytes(entry_bytes.replace(binding_compare, b"if False:"))
    helper_path.write_bytes(malicious)
    bypassed = _run_tool(tool, ["_precommit_check"], cwd=repo)
    assert bypassed.returncode == 0, bypassed.stderr
    assert marker.is_file()
    with pytest.raises(AssertionError, match="positive binding marker"):
        assert not marker.exists(), "positive binding marker should remain absent"

    # The installed launcher rejects a linked package parent before importing
    # it; keep this separate from helper-leaf failure to catch early setup
    # failures explicitly rather than counting them as a binding pass.
    parent_repo = tmp_path / "parent-repo"
    parent_repo.mkdir()
    parent_tool = _git_repo(parent_repo)
    parent_package = parent_repo / "tools" / "_intent"
    (parent_package / "conflict.py").write_bytes(entry_bytes)
    parent_saved = parent_repo / "tools" / "_intent-real"
    parent_package.rename(parent_saved)
    parent_package.symlink_to(parent_saved, target_is_directory=True)
    parent_result = _run_tool(
        parent_tool, ["_precommit_check"], cwd=parent_repo, env=probe_env,
    )
    assert parent_result.returncode != 0
    assert "is a symlink or resolves outside" in parent_result.stderr
    assert not git_probe_marker.exists()


def _run_tool(tool: Path, args: list[str], *, cwd: Path,
              env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tool), *args],
        cwd=cwd, capture_output=True, text=True,
        env=env if env is not None else _clean_env(),
    )


def test_next_installed_plan_review_and_identity_stops(tmp_path: Path) -> None:
    _git_repo(tmp_path)
    for name in ("board.py", "session.py"):
        (tmp_path / "tools" / name).write_bytes(
            (TEMPLATES_ROOT / "skills" / "_lib" / name).read_bytes()
        )
    proposals = tmp_path / "dev" / "proposals" / "archive"
    plans = tmp_path / "dev" / "plans"
    proposals.mkdir(parents=True)
    plans.mkdir()
    (tmp_path / "dev" / "intents.jsonl").write_text("", encoding="utf-8")
    (proposals / "2026-01-01-sample.md").write_text(
        "# Proposal\n\n**Status**: accepted\n"
        "**Review**: usual\n"
        "## Review -- Reviewer -- 2026-01-02\n**Verdict**: SHIP\n\n"
        "## Decision -- Maintainer -- 2026-01-01\n"
        "**Tier**: standard\n**ACCEPTED.** Authority.\n", encoding="utf-8")
    plan = plans / "2026-01-01-sample.md"
    header = ("# Plan\n\n**Status**: ready-to-implement\n"
              "**Source proposal**: dev/proposals/archive/2026-01-01-sample.md\n"
              "**Plan review**: required(Internal)\n")
    review = "## Plan review -- Reviewer -- 2026-01-01\n**Verdict**: {}\n"

    def run(env):
        result = subprocess.run(
            [sys.executable, str(tmp_path / "tools" / "board.py"), "--next", "--json"],
            cwd=tmp_path, env=env, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    plan.write_text(header + review.format("REVISE") + "Blocking issue remains.\n",
                    encoding="utf-8")
    assert "stop" in run(_clean_env(CAIRN_AGENT="known"))
    plan.write_text(header + review.format("ACCEPT") + " -- plan only\n",
                    encoding="utf-8")
    assert run(_clean_env(CAIRN_AGENT="known"))["role"] == "implementer"
    assert "stop" in run(_clean_env())
    assert "stop" in run(_clean_env(CAIRN_AGENT="unknown-agent"))
    claim = _run_tool(tmp_path / "tools" / "intent.py", [
        "claim", "--files", "dev/plans/2026-01-01-sample.md",
        "--action", "test", "--agent", "known"], cwd=tmp_path)
    assert claim.returncode == 0, claim.stderr
    assert run(_clean_env(CAIRN_AGENT="known"))["role"] == "implementer"
    assert "stop" in run(_clean_env(CAIRN_AGENT="other"))
    assert "stop" in run(_clean_env())


def test_next_installed_cli_refuses_malformed_ledger_and_resolver_fallback(
    tmp_path: Path,
) -> None:
    _git_repo(tmp_path)
    for name in ("board.py", "session.py"):
        (tmp_path / "tools" / name).write_bytes(
            (TEMPLATES_ROOT / "skills" / "_lib" / name).read_bytes()
        )
    proposal = tmp_path / "dev" / "proposals" / "2026-01-01-sample.md"
    proposal.parent.mkdir(parents=True)
    proposal.write_text(
        "# Proposal\n\n**Status**: awaiting-review\n**Review**: usual\n",
        encoding="utf-8",
    )
    ledger = tmp_path / "dev" / "intents.jsonl"
    ledger.write_text("", encoding="utf-8")

    def run() -> dict:
        result = subprocess.run(
            [sys.executable, str(tmp_path / "tools" / "board.py"),
             "--next", "--json"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="trial-agent"),
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    assert run()["role"] == "reviewer"

    ledger.write_text("{broken\n", encoding="utf-8")
    malformed = run()
    assert malformed["stop"] == "claims ledger is unreadable or invalid"

    ledger.write_text("", encoding="utf-8")
    git_admin = tmp_path / ".git"
    git_admin.rename(tmp_path / "git-admin")
    git_admin.write_text("gitdir: /missing/cairn-worktree/.git\n",
                         encoding="utf-8")
    fallback = run()
    assert fallback["stop"] == "claims resolver fallback prevents owner selection"


def test_next_installed_cli_names_orphan_release_not_generic_ledger_text(
    tmp_path: Path,
) -> None:
    """A release that matches no claim is reported by its specific reason and
    id; only an unreadable ledger keeps the generic text."""
    _git_repo(tmp_path)
    for name in ("board.py", "session.py"):
        (tmp_path / "tools" / name).write_bytes(
            (TEMPLATES_ROOT / "skills" / "_lib" / name).read_bytes()
        )
    proposal = tmp_path / "dev" / "proposals" / "2026-01-01-sample.md"
    proposal.parent.mkdir(parents=True)
    proposal.write_text(
        "# Proposal\n\n**Status**: awaiting-review\n**Review**: usual\n",
        encoding="utf-8",
    )
    ledger = tmp_path / "dev" / "intents.jsonl"

    def run() -> dict:
        result = subprocess.run(
            [sys.executable, str(tmp_path / "tools" / "board.py"),
             "--next", "--json"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="trial-agent"),
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    ledger.write_text(
        json.dumps({"event": "release", "id": "typo (impl, low)-1",
                    "ts": "2026-01-01T00:01:00+00:00"}) + "\n",
        encoding="utf-8",
    )
    orphan = run()["stop"]
    assert orphan.startswith("release authority is inconsistent"), orphan
    assert "typo (impl, low)-1" in orphan

    ledger.write_text("{broken\n", encoding="utf-8")
    assert run()["stop"] == "claims ledger is unreadable or invalid"


def test_next_installed_accepts_repeated_valid_releases_but_keeps_refusals(
    tmp_path: Path,
) -> None:
    """Valid repeated release metadata is idempotent, while malformed or
    contradictory history and another agent's active overlap still stop NEXT."""
    _git_repo(tmp_path)
    for name in ("board.py", "session.py"):
        (tmp_path / "tools" / name).write_bytes(
            (TEMPLATES_ROOT / "skills" / "_lib" / name).read_bytes()
        )
    proposal = tmp_path / "dev" / "proposals" / "2026-01-01-sample.md"
    proposal.parent.mkdir(parents=True)
    proposal.write_text(
        "# Proposal\n\n**Status**: awaiting-review\n**Review**: usual\n",
        encoding="utf-8",
    )
    ledger = tmp_path / "dev" / "intents.jsonl"

    def run() -> dict:
        result = subprocess.run(
            [sys.executable, str(tmp_path / "tools" / "board.py"),
             "--next", "--json"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="trial-agent"),
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    def claim(claim_id: str, files: list[str], agent: str = "closed-agent"):
        return {"event": "claim", "id": claim_id,
                "ts": "2026-01-01T00:00:00+00:00", "agent": agent,
                "files": files, "action": "synthetic test claim"}

    def release(claim_id: str, commit: str | None = None):
        row = {"event": "release", "id": claim_id,
               "ts": "2026-01-01T00:01:00+00:00"}
        if commit is not None:
            row["commit"] = commit
        return row

    def write(rows: list[dict]) -> None:
        ledger.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )

    closed_claim = claim("closed", ["dev/other.md"])
    first_release = release("closed", "a" * 40)
    write([closed_claim, first_release])
    assert run()["role"] == "reviewer"  # first-release positive control

    repeated_release = release("closed", "b" * 40)
    write([closed_claim, first_release, repeated_release])
    repeated = run()
    assert repeated.get("role") == "reviewer", repeated

    # The strict reader must still reject an invalid later release, a
    # pre-claim/orphan release, and a duplicate claim even after closure.
    invalid_second = release("closed", 7)
    write([closed_claim, first_release, invalid_second])
    assert "stop" in run()
    write([first_release, closed_claim])
    assert "stop" in run()
    write([closed_claim, first_release, closed_claim])
    assert "stop" in run()

    # A different active ID that overlaps the artifact continues to stop even
    # while a separate ID has two valid release records.
    write([closed_claim, first_release, repeated_release,
           claim("active", ["dev/proposals/2026-01-01-sample.md"],
                 agent="another-agent")])
    assert "stop" in run()


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


#: The one-line remedy every refusal of a linked ``.gitignore`` carries.
_REMEDY = "replace the link with a regular file, then re-run"


class TestGitignoreSeedWritesByReplacing:
    # Declared exception (internal hook): swap must land between read and write; injected by monkeypatching internal _read_regular_bytes.
    def test_swapped_hardlink_never_receives_appended_bytes(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        from bootstrap._scaffold import install as I

        ignore = tmp_path / ".gitignore"
        ignore.write_bytes(b"existing\n")
        victim = tmp_path / "outside"
        victim.write_bytes(b"outside\n")
        real_read = I._read_regular_bytes

        def swap_after_read(path: Path, *, single_link: bool = False) -> bytes | None:
            raw = real_read(path, single_link=single_link)
            ignore.unlink()
            os.link(victim, ignore)
            return raw

        with monkeypatch.context() as mp:
            mp.setattr(I, "_read_regular_bytes", swap_after_read)
            assert seed_gitignore(tmp_path, ("new",)) == ["new"]
        assert victim.read_bytes() == b"outside\n"
        assert ignore.read_bytes() == b"existing\nnew\n"
        assert ignore.stat().st_nlink == 1

    def test_read_only_file_is_not_replaced(self, tmp_path: Path) -> None:
        ignore = tmp_path / ".gitignore"
        ignore.write_bytes(b"existing\n")
        ignore.chmod(0o444)
        try:
            with pytest.raises(ScaffoldSecurityError, match="not writable"):
                seed_gitignore(tmp_path, ("new",))
            assert ignore.read_bytes() == b"existing\n"
            assert stat.S_IMODE(ignore.stat().st_mode) == 0o444
        finally:
            ignore.chmod(0o644)

    def test_hardlink_refused_before_any_read(self, tmp_path: Path) -> None:
        victim = tmp_path / "victim"
        victim.write_bytes(b"outside\n")
        os.link(victim, tmp_path / ".gitignore")
        with pytest.raises(ScaffoldSecurityError, match="file of its own"):
            seed_gitignore(tmp_path, (), dry_run=True)
        assert victim.read_bytes() == b"outside\n"

    def test_non_utf8_bytes_preserved_and_preflight_does_not_read(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        from bootstrap._scaffold import install as I
        ignore = tmp_path / ".gitignore"
        ignore.write_bytes(b"\xff\xfe\nold\n")
        with monkeypatch.context() as mp:
            mp.setattr(I, "_read_regular_bytes", lambda *_a, **_kw: pytest.fail("read"))
            assert seed_gitignore(tmp_path, (), dry_run=True) == []
        assert seed_gitignore(tmp_path, ("new",)) == ["new"]
        assert ignore.read_bytes() == b"\xff\xfe\nold\nnew\n"
        assert seed_gitignore(tmp_path, ("new",)) == []

    def test_pipe_refused_before_open(self, tmp_path: Path) -> None:
        if not hasattr(os, "mkfifo"):
            pytest.skip("named pipes unavailable")
        os.mkfifo(tmp_path / ".gitignore")
        with pytest.raises(ScaffoldSecurityError, match="plain file"):
            seed_gitignore(tmp_path, (), dry_run=True)


def _tree(root: Path) -> list[str]:
    """Every path under *root* -- files, folders and links, none followed --
    so "nothing was written" can mean no file and no empty folder either."""
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        found += [str((base / n).relative_to(root)) for n in dirnames + filenames]
    return sorted(found)


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
    def _write_profile(target: Path) -> None:
        (target / "profile.yml").write_text(
            "project_name: LinkTest\ntest_command: pytest\nmodules:\n"
            "  - coordination-tiers\n"
        )

    @staticmethod
    def _run_install(target: Path, *extra: str) -> int:
        return main(
            ["--config", str(target / "profile.yml"), "--target", str(target),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev", *extra]
        )

    @classmethod
    def _install(cls, target: Path, *extra: str) -> int:
        cls._write_profile(target)
        return cls._run_install(target, *extra)

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
        self._write_profile(target)
        before = _tree(target)
        rc = self._run_install(target)
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "refus" in err and "symlinked destination" in err
        assert str(target / ".gitignore") in err
        assert _REMEDY in err
        assert outside.read_bytes() == _OUTSIDE_BYTES, (
            "the install appended to a file outside the target through the link"
        )
        assert _tree(target) == before, (
            "the refusal came after the install had started writing"
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
        self._write_profile(target)
        before = _tree(target)
        rc = self._run_install(target)
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "symlinked destination" in err
        assert _REMEDY in err
        assert behind.read_bytes() == _OUTSIDE_BYTES
        assert (target / ".gitignore").is_symlink()
        assert _tree(target) == before

    def test_adopt_module_refuses_before_recording_anything(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Adoption seeds ``.gitignore`` as its last step, after the lockfile
        and the module's files are written. A linked ``.gitignore`` must stop
        it before the first of those writes: a lockfile that records a module
        whose seed was refused is a half-done adoption nobody asked for."""
        target = tmp_path / "tgt"
        target.mkdir()
        assert self._install(target) == 0
        outside = tmp_path / "elsewhere" / "startup-file"
        outside.parent.mkdir()
        outside.write_bytes(_OUTSIDE_BYTES)
        (target / ".gitignore").unlink()
        (target / ".gitignore").symlink_to(outside)
        lock_path = target / "dev" / ".cairn" / "cairn-lock.yml"
        lock_before = lock_path.read_bytes()
        module = "architecture-review"  # opt-in; not in the roster installed above
        module_files = [target / sp.dst for sp in _MODULE_MAPPINGS[module]]
        assert not any(f.exists() for f in module_files)
        capsys.readouterr()

        rc = main(["upgrade", "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT), "--adopt-module", module])

        err = capsys.readouterr().err
        assert rc == 2, err
        assert ".gitignore seed refused (containment)" in err
        assert "symlinked destination" in err
        assert _REMEDY in err
        assert outside.read_bytes() == _OUTSIDE_BYTES
        assert lock_path.read_bytes() == lock_before, (
            "the lockfile was rewritten before the seed was refused"
        )
        assert not any(f.exists() for f in module_files), (
            "the module's files were installed before the seed was refused"
        )

    def test_dry_run_install_predicts_the_refusal(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A dry run that printed "Would seed .gitignore" for a file the real
        run refuses would promise something the install does not do."""
        target, outside = self._linked_gitignore(tmp_path, inside=False)
        self._write_profile(target)
        before = _tree(target)
        rc = self._run_install(target, "--dry-run")
        err = capsys.readouterr().err
        assert rc == 2, err
        assert "symlinked destination" in err
        assert _REMEDY in err
        assert outside.read_bytes() == _OUTSIDE_BYTES
        assert _tree(target) == before


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

    def test_unavailable_git_does_not_auto_release_claims(self, tmp_path) -> None:
        repo = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="reader-owner")
        _run_tool(
            repo, ["claim", "--files", "dev/held.md", "--action", "edit"],
            cwd=tmp_path, env=env,
        )
        without_git = _clean_env(CAIRN_AGENT="reader-owner", PATH="")
        result = _run_tool(repo, ["_auto_release"], cwd=tmp_path,
                           env=without_git)
        assert result.returncode == 0
        assert "committed path discovery is unavailable" in result.stderr
        still_active = _run_tool(repo, ["list"], cwd=tmp_path, env=env)
        assert "dev/held.md" in still_active.stdout


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
        assert "git " not in text
        assert "PATHS_TMP" not in text

    @pytest.mark.parametrize("hook", ["install-hook", "install-precommit"])
    def test_metacharacter_paths_never_execute_in_hooks(
        self, tmp_path, hook: str,
    ) -> None:
        """Promise: a checkout path holding a shell substitution is quoted into
        the installed hook, so committing never executes it.  Each case also
        shows the hook ran (auto-release, or a block), so a hook that failed to
        start cannot pass by leaving the sentinel absent."""
        repo = tmp_path / "$(touch pwned)"
        repo.mkdir()
        tool = _git_repo(repo)
        if hook == "install-hook":
            env = _clean_env(CAIRN_AGENT="hook-quote")
        else:
            env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        installed = _run_tool(tool, [hook], cwd=repo, env=env)
        assert installed.returncode == 0, installed.stderr
        if hook == "install-hook":
            claim_env = env
        else:
            claim_env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-OTHER")
        claim = _run_tool(
            tool, ["claim", "--files", "dev/a.md", "--action", "quote"],
            cwd=repo, env=claim_env,
        )
        assert claim.returncode == 0, claim.stderr
        _stage(repo, env, "dev/a.md")
        commit = subprocess.run(
            ["git", "commit", "-q", "-m", "work"], cwd=repo, env=env,
            capture_output=True, text=True,
        )
        if hook == "install-hook":
            assert commit.returncode == 0, commit.stderr
            listed = _run_tool(tool, ["list"], cwd=repo, env=env)
            assert "no active intents" in listed.stdout
        else:
            assert commit.returncode != 0
            assert "enforce=block" in commit.stderr
        assert list(tmp_path.rglob("pwned")) == []

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
        assert "board.py --next || true" in text

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


@pytest.mark.parametrize(
    "ledger",
    [
        '{"event":"mystery","id":"x","ts":"2026-01-01T00:00:00+00:00"}',
        '{"event":"claim","id":"x","id":"y","ts":"2026-01-01T00:00:00+00:00","agent":"a","files":["a.md"],"action":"edit"}',
        '{"event":"claim","id":"x","ts":"bad","agent":"a","files":["a.md"],"action":"edit"}',
        '[]',
        '{broken',
        "linked",
    ],
    ids=["unknown-event", "duplicate-key", "bad-timestamp", "not-an-object",
         "broken-json", "linked-ledger"],
)
def test_a_malformed_or_linked_claims_ledger_stops_owner_selection(
    tmp_path: Path, ledger: str,
) -> None:
    """Promise: ``board.py --next`` will not pick an owner from a claims ledger
    that is malformed or is a link; it stops with the ledger-unreadable reason.
    The empty-ledger control proves the repository otherwise selects an owner."""
    _git_repo(tmp_path)
    for name in ("board.py", "session.py"):
        (tmp_path / "tools" / name).write_bytes(
            (TEMPLATES_ROOT / "skills" / "_lib" / name).read_bytes()
        )
    proposal = tmp_path / "dev" / "proposals" / "2026-01-01-sample.md"
    proposal.parent.mkdir(parents=True)
    proposal.write_text(
        "# Proposal\n\n**Status**: awaiting-review\n**Review**: usual\n",
        encoding="utf-8",
    )
    path = tmp_path / "dev" / "intents.jsonl"
    path.write_text("", encoding="utf-8")

    def run() -> dict:
        result = subprocess.run(
            [sys.executable, str(tmp_path / "tools" / "board.py"),
             "--next", "--json"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="trial-agent"),
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    assert run()["role"] == "reviewer"
    if ledger == "linked":
        target = tmp_path / "dev" / "real-intents.jsonl"
        path.rename(target)
        try:
            path.symlink_to(target)
        except OSError as exc:
            pytest.skip(f"symlinks unavailable: {exc}")
    else:
        path.write_text(ledger + "\n", encoding="utf-8")
    stopped = run()
    assert "role" not in stopped
    assert "unreadable or invalid" in stopped["stop"]


# Declared exception (internal hook): Named in security_manifest.py (must stay). Hook: patched os.open swaps the ledger leaf between check and open.
@pytest.mark.parametrize("replacement", ["symlink", "fifo", "regular"])
def test_strict_claim_reader_refuses_leaf_swap_before_open(
    tmp_path, monkeypatch, replacement
):
    if replacement == "fifo" and not hasattr(os, "mkfifo"):
        pytest.skip("named pipes unavailable")
    tool = _load_tool(TOOL_TEMPLATE, name="strict_claim_reader_swap")
    reader = tool._load_engine().read_log
    ledger = tmp_path / "intents.jsonl"
    foreign = tmp_path / "foreign.jsonl"
    payload = ('{"event":"claim","id":"x","ts":"2026-01-01T00:00:00+00:00",'
               '"agent":"a","files":["a.md"],"action":"edit"}\n')
    ledger.write_text(payload, encoding="utf-8")
    foreign.write_text("not json\n", encoding="utf-8")
    assert reader(ledger, strict=True)[0]["id"] == "x"
    real_open = os.open

    def swap_open(path, flags, *args, **kwargs):
        if Path(path) == ledger:
            ledger.rename(tmp_path / "original.jsonl")
            if replacement == "symlink":
                ledger.symlink_to(foreign)
            elif replacement == "fifo":
                os.mkfifo(ledger)
            else:
                ledger.write_text("not json\n", encoding="utf-8")
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(os, "open", swap_open)
    with pytest.raises(OSError):
        reader(ledger, strict=True)


# Declared exception (internal hook): Hook: patched os.fstat renames the ledger after open; post-open identity recheck is a different branch from the pre-open swap.
def test_strict_claim_reader_refuses_name_change_after_open(tmp_path, monkeypatch):
    tool = _load_tool(TOOL_TEMPLATE, name="strict_claim_reader_after_open")
    reader = tool._load_engine().read_log
    ledger = tmp_path / "intents.jsonl"
    ledger.write_text("", encoding="utf-8")
    real_fstat = os.fstat

    def swap_after_open(fd):
        result = real_fstat(fd)
        ledger.rename(tmp_path / "original.jsonl")
        ledger.write_text("not json\n", encoding="utf-8")
        return result

    monkeypatch.setattr(os, "fstat", swap_after_open)
    with pytest.raises(OSError):
        reader(ledger, strict=True)


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

def _precommit_hook(repo: Path, git_executable: str | None = None) -> Path:
    """Resolve the repo's pre-commit hook path (hooksPath-aware)."""
    out = subprocess.run(
        [git_executable or "git", "rev-parse", "--git-path", "hooks"],
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
        assert "git diff" not in text
        assert "PATHS_TMP" not in text
        # The interpreter is baked in; no bare `python -m`.
        assert sys.executable in text
        assert "python -m" not in text
        st = _run_tool(tool, ["hooks-status"], cwd=tmp_path)
        assert "pre-commit (work-intent check): installed" in st.stdout
        assert "post-commit (auto-release): not-installed" in st.stdout

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


class TestIntentParentHelp:
    """The adopter-facing parent help states the conditional policy."""

    def test_parent_help_matches_source_and_installed_entrypoint(
        self, tmp_path,
    ) -> None:
        """Source and installed twins keep a working public help command."""
        source_tool = CAIRN_ROOT / "tools" / "intent.py"
        installed_tool = _git_repo(tmp_path)
        for tool, cwd in ((source_tool, CAIRN_ROOT), (installed_tool, tmp_path)):
            res = subprocess.run(
                [sys.executable, str(tool), "--help"],
                cwd=cwd,
                capture_output=True, text=True, env=_clean_env(),
            )
            assert res.returncode == 0, res.stderr


class TestManualRelease:
    def test_release_by_claim_id_does_not_authenticate_label(self, tmp_path) -> None:
        """Manual release closes the named claim by ID, without owner auth."""
        tool = _git_repo(tmp_path)
        log = str(tmp_path / "dev" / "intents.jsonl")
        claimant = _run_tool(
            tool, ["--log-path", log, "claim", "--files", "dev/a.md",
                   "--action", "bob-work"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        assert claimant.returncode == 0, claimant.stderr
        claim_id = claimant.stdout.strip()
        released = _run_tool(
            tool, ["--log-path", log, "release", claim_id],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="alice"),
        )
        assert released.returncode == 0, released.stderr
        assert claim_id in released.stderr
        active = _run_tool(
            tool, ["--log-path", log, "list"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="alice"),
        )
        assert "no active intents" in active.stdout

    @staticmethod
    def _claim(tool: Path, tmp_path: Path, agent: str) -> tuple[Path, str]:
        log = tmp_path / "dev" / "intents.jsonl"
        claimant = _run_tool(
            tool, ["--log-path", str(log), "claim", "--files", "dev/a.md",
                   "--action", "work"],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT=agent),
        )
        assert claimant.returncode == 0, claimant.stderr
        return log, claimant.stdout.strip()

    def test_release_of_unknown_id_is_refused_and_names_closest(
            self, tmp_path) -> None:
        """An id that matches no claim exits 2, names the closest real id, and
        leaves the ledger bytes unchanged."""
        tool = _git_repo(tmp_path)
        log, claim_id = self._claim(tool, tmp_path, "bob")
        before = log.read_bytes()
        typo = claim_id[:-1] + ("0" if claim_id[-1] != "0" else "1")
        refused = _run_tool(
            tool, ["--log-path", str(log), "release", typo],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        assert refused.returncode == 2, refused.stderr
        assert typo in refused.stderr
        assert claim_id in refused.stderr
        assert log.read_bytes() == before

    def test_release_refuses_hand_typed_near_miss_and_suggests_real_id(
            self, tmp_path) -> None:
        """The id typed with ``, low`` (a space) is refused; the real id
        (``,-low``, as the claim wrote it) is suggested."""
        tool = _git_repo(tmp_path)
        log, claim_id = self._claim(
            tool, tmp_path, "claude-x (implementation, low)")
        assert "(implementation,-low)" in claim_id
        before = log.read_bytes()
        hand_typed = claim_id.replace(",-low", ", low")
        assert hand_typed != claim_id
        refused = _run_tool(
            tool, ["--log-path", str(log), "release", hand_typed],
            cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
        )
        assert refused.returncode == 2, refused.stderr
        assert claim_id in refused.stderr
        assert log.read_bytes() == before

    def test_release_of_real_id_and_repeat_release_still_succeed(
            self, tmp_path) -> None:
        """A correct release works, and a repeat release of the same real
        claim is still accepted (the repeated-release policy)."""
        tool = _git_repo(tmp_path)
        log, claim_id = self._claim(tool, tmp_path, "bob")
        for _ in range(2):
            released = _run_tool(
                tool, ["--log-path", str(log), "release", claim_id],
                cwd=tmp_path, env=_clean_env(CAIRN_AGENT="bob"),
            )
            assert released.returncode == 0, released.stderr
            assert claim_id in released.stderr
        rows = [json.loads(line) for line in
                log.read_text(encoding="utf-8").splitlines()]
        assert [r["event"] for r in rows] == ["claim", "release", "release"]


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

    def test_unavailable_git_is_unknown_not_a_clean_index(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        env = _clean_env(CAIRN_AGENT="alice")
        _stage(tmp_path, env, "dev/a.md")
        without_git = _clean_env(CAIRN_AGENT="alice", PATH="")
        result = _run_tool(
            tool, ["--log-path", str(self._log(tmp_path)), "_precommit_check"],
            cwd=tmp_path, env=without_git,
        )
        assert result.returncode == 0
        assert "pre-commit coordination is unknown" in result.stderr
        assert "no active claim" not in result.stderr

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
        env = _clean_env(CLAUDE_CODE_SESSION_ID="commit-session")
        other = _clean_env(CLAUDE_CODE_SESSION_ID="other-session")
        _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env)
        (tmp_path / "dev" / "a.md").write_text("a\n")
        (tmp_path / "dev" / "b.md").write_text("b\n")
        subprocess.run(
            ["git", "add", "dev/a.md", "dev/b.md"], cwd=tmp_path, check=True,
            env=env,
        )
        claim = _run_tool(
            tool, ["claim", "--files", "dev/b.md", "--action", "other"],
            cwd=tmp_path, env=other,
        )
        assert claim.returncode == 0, claim.stderr
        res = subprocess.run(
            ["git", "commit", "-m", "c", "dev/a.md"],
            cwd=tmp_path, capture_output=True, text=True, env=env,
        )
        # The partial index contains only a. Another session's claim on b
        # must neither appear in this commit's warning nor block it.
        assert res.returncode == 0
        assert "dev/a.md" in res.stderr
        assert "dev/b.md" not in res.stderr  # not in the path-scoped index
        remaining = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "-z"],
            cwd=tmp_path, capture_output=True, check=True, env=env,
        ).stdout
        assert remaining == b"dev/b.md\0"

    def test_linked_and_split_index_path_scoped_commits(self, tmp_path) -> None:
        tool = _git_repo(tmp_path)
        main_env = _clean_env(CLAUDE_CODE_SESSION_ID="main-session")
        for name in ("a.md", "b.md"):
            (tmp_path / "dev" / name).write_text("base\n")
        subprocess.run(["git", "add", "dev/a.md", "dev/b.md"],
                       cwd=tmp_path, check=True, env=main_env)
        subprocess.run(["git", "commit", "-m", "base"], cwd=tmp_path,
                       check=True, env=main_env)
        installed = _run_tool(tool, ["install-precommit"], cwd=tmp_path,
                              env=main_env)
        assert installed.returncode == 0, installed.stderr
        other_claim = _run_tool(
            tool, ["claim", "--files", "dev/b.md", "--action", "held"],
            cwd=tmp_path, env=_clean_env(CLAUDE_CODE_SESSION_ID="other-session"),
        )
        assert other_claim.returncode == 0, other_claim.stderr

        for name, split in (("linked", False), ("split", True)):
            worktree = tmp_path.parent / f"{tmp_path.name}-{name}"
            subprocess.run(
                ["git", "worktree", "add", "-b", f"intent-{name}",
                 str(worktree), "HEAD"],
                cwd=tmp_path, check=True, env=main_env,
            )
            env = _clean_env(CLAUDE_CODE_SESSION_ID=f"{name}-session")
            if split:
                subprocess.run(["git", "update-index", "--split-index"],
                               cwd=worktree, check=True, env=env)
            (worktree / "dev/a.md").write_text(f"{name} a\n")
            (worktree / "dev/b.md").write_text(f"{name} b\n")
            subprocess.run(["git", "add", "dev/a.md", "dev/b.md"],
                           cwd=worktree, check=True, env=env)
            result = subprocess.run(
                ["git", "commit", "-m", name, "dev/a.md"], cwd=worktree,
                capture_output=True, text=True, env=env,
            )
            assert result.returncode == 0, result.stderr
            assert "dev/a.md" in result.stderr
            assert "dev/b.md" not in result.stderr
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "-z"],
                cwd=worktree, capture_output=True, check=True, env=env,
            ).stdout
            assert staged == b"dev/b.md\0"


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

    def test_confirm_mode_without_a_terminal_blocks(self, tmp_path) -> None:
        """Promise: with ``enforce=confirm`` and nobody to ask (the commit runs
        in its own session, with no controlling terminal), another live
        session's claim on a staged path blocks the commit.  The same commit
        under ``warn`` goes through, so the refusal is the confirm rule."""
        tool = _git_repo(tmp_path)
        self._claim_other_session(tool, tmp_path, "dev/a.md")
        env = _clean_env(CLAUDE_CODE_SESSION_ID="sess-MINE")
        installed = _run_tool(tool, ["install-precommit"], cwd=tmp_path, env=env)
        assert installed.returncode == 0, installed.stderr
        _stage(tmp_path, env, "dev/a.md")

        def commit() -> subprocess.CompletedProcess:
            return subprocess.run(
                ["git", "commit", "-q", "-m", "work"], cwd=tmp_path, env=env,
                capture_output=True, text=True, start_new_session=True,
            )

        self._set_enforce(tmp_path, "confirm")
        assert commit().returncode != 0
        self._set_enforce(tmp_path, "warn")
        assert commit().returncode == 0


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


_PRECOMMIT_INDEX_ROUTE_ARGS = {
    "staged": ("diff", "--cached", "--name-only", "-z"),
    "rename": ("diff", "--cached", "--name-status", "-M", "-z"),
}
_PRECOMMIT_ROUTE_SESSION = "session-git-route"


def _route_instrument_conflict(source_bytes: bytes, function: str,
                               *, mutate: bool) -> bytes:
    """Add a conditional PATH switch at one physical owner call site."""
    source = source_bytes.decode("utf-8")
    tree = ast.parse(source)
    owners = [node for node in ast.walk(tree)
              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
              and node.name == function]
    assert len(owners) == 1, f"missing unique route owner {function}"
    calls = [node for node in ast.walk(owners[0])
             if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute)
             and node.func.attr == "read_hook_index"
             and isinstance(node.func.value, ast.Call)
             and isinstance(node.func.value.func, ast.Name)
             and node.func.value.func.id == "_git_read"]
    assert len(calls) == 1, f"{function} has {len(calls)} hook-index reads"
    call = calls[0]
    assert len(call.args) >= 2
    args_source = ast.get_source_segment(source, call.args[1])
    call_source = ast.get_source_segment(source, call)
    assert args_source and call_source
    if mutate:
        call_source, count = call_source.replace(
            "_git_read().read_hook_index(",
            "_cairn_test_route_git_adapter(", 1), 1
        assert count == 1
    wrapped = f"_cairn_test_route_invoke({args_source}, lambda: {call_source})"
    lines = source.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    start_line, end_line = call.lineno - 1, call.end_lineno - 1
    encoded = source.encode("utf-8")
    start = len(source[:starts[start_line]].encode("utf-8")) + call.col_offset
    end = len(source[:starts[end_line]].encode("utf-8")) + call.end_col_offset
    source = (encoded[:start] + wrapped.encode("utf-8")
              + encoded[end:]).decode("utf-8")
    source += '''

def _cairn_test_route_invoke(args, invoke):
    import json as _route_json
    import os as _route_os
    from pathlib import Path as _route_Path
    active = (_route_os.environ.get("CAIRN_TEST_INDEX_ROUTE_ACTIVE") == "1"
              and tuple(args) == tuple(_route_json.loads(
                  _route_os.environ["CAIRN_TEST_INDEX_ROUTE_ARGS"])))
    old_path = _route_os.environ.get("PATH", "")
    if active:
        _route_Path(_route_os.environ["CAIRN_TEST_INDEX_ROUTE_TRIGGER"]).write_text(
            "triggered", encoding="utf-8")
        with _route_Path(_route_os.environ["CAIRN_TEST_INDEX_ROUTE_TRACE"]).open(
                "a", encoding="utf-8") as _route_trace:
            _route_trace.write("trigger\\n")
        _route_os.environ["PATH"] = _route_os.environ["CAIRN_TEST_INDEX_ROUTE_PATH"]
    try:
        return invoke()
    finally:
        if active:
            _route_os.environ["PATH"] = old_path

def _cairn_test_route_git_adapter(target, args, **kwargs):
    import os as _route_os
    import subprocess as _route_subprocess
    from types import SimpleNamespace as _RouteResult
    completed = _route_subprocess.run(
        ["git", *args], cwd=target, env=_route_os.environ.copy(),
        capture_output=True, check=False)
    return _RouteResult(state="completed", returncode=completed.returncode,
                        stdout=completed.stdout, stderr=completed.stderr)
'''
    return source.encode("utf-8")


def _route_git_setup(git: str, repo: Path, *args: str, env: dict):
    return subprocess.run([git, *args], cwd=repo, env=env,
                          capture_output=True, check=False)


def _stage_with_known_git(git: str, repo: Path, env: dict, relpath: str,
                          content: str) -> None:
    path = repo / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    result = _route_git_setup(git, repo, "add", relpath, env=env)
    assert result.returncode == 0, result.stderr


def _precommit_route_fixture(base: Path, entry_source: Path | bytes, git: str,
                             git_path: str) -> tuple[Path, Path, dict]:
    base.mkdir(parents=True)
    repo = base / "repo"
    repo.mkdir()
    tool = _git_repo(repo, git_executable=git)
    source_bytes = (entry_source if isinstance(entry_source, bytes)
                    else entry_source.read_bytes())
    (repo / "tools/_intent/conflict.py").write_bytes(source_bytes)
    (repo / "dev/a.md").write_text("initial committed file\n", encoding="utf-8")
    session_env = _clean_env(
        PATH=git_path, CLAUDE_CODE_SESSION_ID=_PRECOMMIT_ROUTE_SESSION,
    )
    staged = _route_git_setup(git, repo, "add", "dev/a.md", env=session_env)
    assert staged.returncode == 0, staged.stderr
    committed = _route_git_setup(
        git, repo, "commit", "--quiet", "-m", "initial", env=session_env)
    assert committed.returncode == 0, committed.stderr
    installed = _run_tool(
        tool, ["install-precommit"], cwd=repo, env=session_env)
    assert installed.returncode == 0, installed.stderr
    hook = _precommit_hook(repo, git)
    assert hook.is_file() and os.access(hook, os.X_OK)
    return repo, tool, session_env


def _assert_precommit_healthy_controls(repo: Path, tool: Path,
                                       git: str, env: dict) -> None:
    empty = _route_git_setup(
        git, repo, "commit", "--quiet", "--allow-empty", "-m", "empty",
        env=env)
    assert empty.returncode == 0, empty.stderr
    assert empty.stdout == empty.stderr == b""

    _stage_with_known_git(git, repo, env, "dev/a.md", "healthy unclaimed edit\n")
    warning = _route_git_setup(
        git, repo, "commit", "--quiet", "-m", "unclaimed edit", env=env)
    assert warning.returncode == 0, warning.stderr
    warning_text = warning.stderr.decode("utf-8", errors="replace")
    assert "no active claim" in warning_text and "dev/a.md" in warning_text

    claim = _run_tool(
        tool, ["claim", "--files", "dev/a.md", "--action", "rename test"],
        cwd=repo, env=env)
    assert claim.returncode == 0, claim.stderr
    renamed = _route_git_setup(git, repo, "mv", "dev/a.md", "dev/b.md", env=env)
    assert renamed.returncode == 0, renamed.stderr
    index = _route_git_setup(
        git, repo, "diff", "--cached", "--name-status", "-M", "-z", env=env)
    assert index.returncode == 0, index.stderr
    assert index.stdout.split(b"\x00")[:3] == [b"R100", b"dev/a.md", b"dev/b.md"]
    result = _route_git_setup(
        git, repo, "commit", "--quiet", "-m", "claimed rename", env=env)
    text = result.stderr.decode("utf-8", errors="replace")
    assert result.returncode == 0, text
    assert "no active claim" not in text and "dev/b.md" not in text


def _precommit_route_run(repo: Path, git: str, git_path: str,
                         route: str) -> tuple[
                             subprocess.CompletedProcess, Path, Path, Path]:
    args = _PRECOMMIT_INDEX_ROUTE_ARGS[route]
    if route == "rename":
        claim = _run_tool(
            repo / "tools/intent.py",
            ["claim", "--files", "dev/a.md", "--action", "route rename"],
            cwd=repo,
            env=_clean_env(PATH=git_path,
                           CLAUDE_CODE_SESSION_ID=_PRECOMMIT_ROUTE_SESSION),
        )
        assert claim.returncode == 0, claim.stderr
        moved = _route_git_setup(git, repo, "mv", "dev/a.md", "dev/b.md",
                                 env=_clean_env(PATH=git_path))
        assert moved.returncode == 0, moved.stderr
        index_args = ("diff", "--cached", "--name-status", "-M", "-z")
        index = _route_git_setup(git, repo, *index_args,
                                 env=_clean_env(PATH=git_path))
        assert index.returncode == 0, index.stderr
        assert index.stdout.split(b"\x00")[:3] == [
            b"R100", b"dev/a.md", b"dev/b.md"]
    else:
        _stage_with_known_git(git, repo, _clean_env(PATH=git_path),
                              "dev/a.md", "hostile staged edit\n")
        index = _route_git_setup(git, repo, "diff", "--cached", "--name-only",
                                 "-z", env=_clean_env(PATH=git_path))
        assert index.returncode == 0, index.stderr
        assert index.stdout.split(b"\x00") == [b"dev/a.md", b""]

    hostile_bin = repo / "hostile-bin"
    hostile_bin.mkdir()
    trace = repo / "route-events"
    marker = repo / "hostile-git-ran"
    fake_git = hostile_bin / "git"
    fake_git.write_text(
        f"#!{sys.executable}\n"
        "from pathlib import Path\n"
        "import os\n"
        f"Path({str(marker)!r}).write_text('ran', encoding='utf-8')\n"
        f"with Path({str(trace)!r}).open('a', encoding='utf-8') as stream:\n"
        "    stream.write('git\\n')\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    fake_git.chmod(0o755)
    trigger = repo / "route-trigger"
    env = _clean_env(
        PATH=git_path,
        CLAUDE_CODE_SESSION_ID=_PRECOMMIT_ROUTE_SESSION,
        CAIRN_TEST_INDEX_ROUTE_ACTIVE="1",
        CAIRN_TEST_INDEX_ROUTE_ARGS=json.dumps(list(args)),
        CAIRN_TEST_INDEX_ROUTE_PATH=str(hostile_bin) + os.pathsep + git_path,
        CAIRN_TEST_INDEX_ROUTE_TRIGGER=str(trigger),
        CAIRN_TEST_INDEX_ROUTE_TRACE=str(trace),
    )
    result = _route_git_setup(git, repo, "commit", "--quiet", "-m",
                              f"{route} route", env=env)
    return result, trigger, marker, trace


@pytest.mark.parametrize(
    ("entry_source", "route", "function"),
    [
        (CAIRN_ROOT / "tools/_intent/conflict.py", "staged",
         "_staged_paths_via_git"),
        (CAIRN_ROOT / "templates/modules/team-gated/_intent/conflict.py",
         "staged", "_staged_paths_via_git"),
        (CAIRN_ROOT / "tools/_intent/conflict.py", "rename",
         "_rename_map_via_git"),
        (CAIRN_ROOT / "templates/modules/team-gated/_intent/conflict.py",
         "rename", "_rename_map_via_git"),
    ],
    ids=["tools-staged", "template-staged", "tools-rename", "template-rename"],
)
def test_generated_precommit_hook_refuses_target_local_git_routes(
        tmp_path: Path, entry_source: Path, route: str, function: str) -> None:
    git = shutil.which("git")
    assert git and Path(git).is_absolute()
    git = str(Path(git).resolve())
    git_path = str(Path(git).parent) + os.pathsep + os.environ.get("PATH", "")

    healthy_repo, healthy_tool, healthy_env = _precommit_route_fixture(
        tmp_path / "healthy", entry_source, git, git_path)
    _assert_precommit_healthy_controls(healthy_repo, healthy_tool, git,
                                       healthy_env)

    safe_source = _route_instrument_conflict(
        entry_source.read_bytes(), function, mutate=False)
    safe_repo, _safe_tool, _safe_env = _precommit_route_fixture(
        tmp_path / "safe", safe_source, git, git_path)
    safe, safe_trigger, safe_marker, safe_trace = _precommit_route_run(
        safe_repo, git, git_path, route)
    safe_text = safe.stderr.decode("utf-8", errors="replace")
    assert safe.returncode == 0, safe_text
    expected = ("staged path discovery is unavailable" if route == "staged"
                else "staged rename discovery is unavailable")
    assert expected in safe_text and "pre-commit coordination is unknown" in safe_text
    assert "no active claim" not in safe_text
    assert safe_trigger.read_text(encoding="utf-8") == "triggered"
    assert not safe_marker.exists()
    assert safe_trace.read_text(encoding="utf-8").splitlines() == ["trigger"]

    mutant_source = _route_instrument_conflict(
        entry_source.read_bytes(), function, mutate=True)
    mutant_repo, _mutant_tool, _mutant_env = _precommit_route_fixture(
        tmp_path / "mutant", mutant_source, git, git_path)
    mutant, mutant_trigger, mutant_marker, mutant_trace = _precommit_route_run(
        mutant_repo, git, git_path, route)
    mutant_text = mutant.stderr.decode("utf-8", errors="replace")
    assert mutant.returncode == 0, mutant_text
    assert expected not in mutant_text
    assert mutant_trigger.read_text(encoding="utf-8") == "triggered"
    assert mutant_marker.is_file()
    assert mutant_trace.read_text(encoding="utf-8").splitlines() == [
        "trigger", "git"]
    if route == "staged":
        assert "no active claim" not in mutant_text
    else:
        assert "no active claim" in mutant_text and "dev/b.md" in mutant_text


def _route_instrument_postcommit_conflict(source_bytes: bytes, function: str,
                                          *, mutate: bool) -> bytes:
    """Switch PATH at one real post-commit Git read; optionally bypass it."""
    source = source_bytes.decode("utf-8")
    tree = ast.parse(source)
    owners = [node for node in ast.walk(tree)
              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
              and node.name == function]
    assert len(owners) == 1, f"missing unique route owner {function}"
    calls = [node for node in ast.walk(owners[0])
             if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute)
             and node.func.attr == "run_git"
             and isinstance(node.func.value, ast.Call)
             and isinstance(node.func.value.func, ast.Name)
             and node.func.value.func.id == "_git_read"]
    assert len(calls) == 1, f"{function} has {len(calls)} run_git reads"
    call = calls[0]
    args_source = ast.get_source_segment(source, call.args[1])
    call_source = ast.get_source_segment(source, call)
    assert args_source and call_source
    if mutate:
        call_source, count = call_source.replace(
            "_git_read().run_git(",
            "_cairn_test_postcommit_git_adapter(", 1), 1
        assert count == 1
    wrapped = (
        f"_cairn_test_postcommit_invoke({args_source}, "
        f"lambda: {call_source})"
    )
    lines = source.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    start_line, end_line = call.lineno - 1, call.end_lineno - 1
    encoded = source.encode("utf-8")
    start = len(source[:starts[start_line]].encode("utf-8")) + call.col_offset
    end = len(source[:starts[end_line]].encode("utf-8")) + call.end_col_offset
    source = (encoded[:start] + wrapped.encode("utf-8")
              + encoded[end:]).decode("utf-8")
    source += '''

def _cairn_test_postcommit_invoke(args, invoke):
    import json as _route_json
    import os as _route_os
    from pathlib import Path as _route_Path
    expected = tuple(_route_json.loads(
        _route_os.environ.get("CAIRN_TEST_POSTCOMMIT_ROUTE_ARGS", "[]")))
    active = (_route_os.environ.get("CAIRN_TEST_POSTCOMMIT_ROUTE_ACTIVE") == "1"
              and tuple(args[:len(expected)]) == expected)
    old_path = _route_os.environ.get("PATH", "")
    if active:
        _route_Path(_route_os.environ["CAIRN_TEST_POSTCOMMIT_ROUTE_TRIGGER"]).write_text(
            "triggered", encoding="utf-8")
        with _route_Path(_route_os.environ["CAIRN_TEST_POSTCOMMIT_ROUTE_TRACE"]).open(
                "a", encoding="utf-8") as _route_trace:
            _route_trace.write("trigger\\n")
        _route_os.environ["PATH"] = _route_os.environ["CAIRN_TEST_POSTCOMMIT_ROUTE_PATH"]
    try:
        return invoke()
    finally:
        if active:
            _route_os.environ["PATH"] = old_path

def _cairn_test_postcommit_git_adapter(target, args, **kwargs):
    import os as _route_os
    import subprocess as _route_subprocess
    from types import SimpleNamespace as _RouteResult
    completed = _route_subprocess.run(
        ["git", *args], cwd=target, env=_route_os.environ.copy(),
        capture_output=True, check=False)
    return _RouteResult(state="completed", returncode=completed.returncode,
                        stdout=completed.stdout, stderr=completed.stderr)
'''
    return source.encode("utf-8")


_POSTCOMMIT_ROUTE_ARGS = {
    "head": ("rev-parse", "--verify", "HEAD"),
    "paths": ("diff-tree", "--root", "--no-commit-id", "--name-only",
              "-r", "-z"),
}


@pytest.mark.parametrize(
    ("entry_source", "route", "function"),
    [
        (CAIRN_ROOT / "tools" / "_intent" / "conflict.py", "head",
         "_head_commit_via_git"),
        (TEMPLATES_ROOT / "modules" / "team-gated" / "_intent" / "conflict.py",
         "head", "_head_commit_via_git"),
        (CAIRN_ROOT / "tools" / "_intent" / "conflict.py", "paths",
         "_committed_paths_via_git"),
        (TEMPLATES_ROOT / "modules" / "team-gated" / "_intent" / "conflict.py",
         "paths", "_committed_paths_via_git"),
    ],
    ids=["tools-head", "template-head", "tools-paths", "template-paths"],
)
def test_generated_postcommit_hook_refuses_target_local_git_routes(
        tmp_path: Path, entry_source: Path, route: str, function: str) -> None:
    """Safe failures retain claims; a one-route PATH bypass trips the wrapper."""
    git = shutil.which("git")
    assert git and Path(git).is_absolute()
    git = str(Path(git).resolve())
    git_path = str(Path(git).parent) + os.pathsep + os.environ.get("PATH", "")
    tool = _git_repo(tmp_path, git_executable=git)
    repo = tmp_path
    conflict_path = repo / "tools" / "_intent" / "conflict.py"
    conflict_path.write_bytes(entry_source.read_bytes())
    _run_tool(tool, ["install-hook"], cwd=repo,
              env=_clean_env(PATH=git_path))

    # A completed empty diff-tree result is distinct from the routed failure:
    # it is silent and leaves an unrelated claim active.
    env = _clean_env(PATH=git_path, CAIRN_AGENT="postcommit-route-owner")
    held = _run_tool(tool, ["claim", "--files", "dev/held.md", "--action",
                            "postcommit route"], cwd=repo, env=env)
    assert held.returncode == 0, held.stderr
    empty = subprocess.run(
        [git, "commit", "--quiet", "--allow-empty", "-m", "empty control"],
        cwd=repo, env=env, capture_output=True, check=False)
    assert empty.returncode == 0, empty.stderr
    empty_text = empty.stderr.decode("utf-8", errors="replace")
    assert "committed revision is unavailable" not in empty_text
    assert "committed path discovery is unavailable" not in empty_text
    still_held = _run_tool(tool, ["list"], cwd=repo, env=env)
    assert "dev/held.md" in still_held.stdout

    hostile_bin = repo / "hostile-bin"
    hostile_bin.mkdir()
    marker = repo / "hostile-git-ran"
    trace = repo / "route-events"
    fake_git = hostile_bin / "git"
    fake_git.write_text(
        f"#!{sys.executable}\n"
        "from pathlib import Path\n"
        "import os, sys\n"
        f"Path({str(marker)!r}).write_text('ran', encoding='utf-8')\n"
        f"with Path({str(trace)!r}).open('a', encoding='utf-8') as stream:\n"
        "    stream.write('git\\n')\n"
        f"os.execv({git!r}, [{git!r}, *sys.argv[1:]])\n",
        encoding="utf-8",
    )
    fake_git.chmod(0o755)

    def run_commit(mutate: bool):
        source = _route_instrument_postcommit_conflict(
            entry_source.read_bytes(), function, mutate=mutate)
        conflict_path.write_bytes(source)
        target_file = repo / "dev" / "routed.md"
        target_file.parent.mkdir(exist_ok=True)
        target_file.write_text(
            "mutant routed edit\n" if mutate else "safe routed edit\n",
            encoding="utf-8")
        staged = subprocess.run([git, "add", "--", "dev/routed.md"],
                                cwd=repo, env=env, capture_output=True)
        assert staged.returncode == 0, staged.stderr
        claim = _run_tool(
            tool, ["claim", "--files", "dev/routed.md", "--action",
                   "postcommit route"], cwd=repo, env=env)
        assert claim.returncode == 0, claim.stderr
        claim_id = claim.stdout.strip()
        trigger = repo / "route-trigger"
        route_env = dict(env)
        route_env.update({
            "CAIRN_TEST_POSTCOMMIT_ROUTE_ACTIVE": "1",
            "CAIRN_TEST_POSTCOMMIT_ROUTE_ARGS": json.dumps(
                list(_POSTCOMMIT_ROUTE_ARGS[route])),
            "CAIRN_TEST_POSTCOMMIT_ROUTE_PATH": str(hostile_bin) + os.pathsep + git_path,
            "CAIRN_TEST_POSTCOMMIT_ROUTE_TRIGGER": str(trigger),
            "CAIRN_TEST_POSTCOMMIT_ROUTE_TRACE": str(trace),
        })
        result = subprocess.run([git, "commit", "--quiet", "-m",
                                 f"{route} route"], cwd=repo,
                                env=route_env, capture_output=True, check=False)
        return result, trigger, claim_id

    # Replace source with the uninstrumented owner for each isolated run.
    conflict_path.write_bytes(entry_source.read_bytes())
    safe, safe_trigger, safe_claim_id = run_commit(mutate=False)
    safe_text = safe.stderr.decode("utf-8", errors="replace")
    assert safe.returncode == 0, safe_text
    expected = ("committed revision is unavailable" if route == "head"
                else "committed path discovery is unavailable")
    assert expected in safe_text
    assert safe_trigger.read_text(encoding="utf-8") == "triggered"
    assert not marker.exists()
    assert trace.read_text(encoding="utf-8").splitlines() == ["trigger"]
    safe_events = [json.loads(line) for line in
                   (repo / "dev" / "intents.jsonl").read_text(
                       encoding="utf-8").splitlines()]
    assert not any(event.get("event") == "release"
                   and event.get("id") == safe_claim_id for event in safe_events)
    held_after_safe = _run_tool(tool, ["list"], cwd=repo, env=env)
    assert "dev/routed.md" in held_after_safe.stdout

    # The one-call adapter mutation executes the target-local wrapper and
    # delegates to real Git, so the real hook reaches its auto-release effect.
    conflict_path.write_bytes(entry_source.read_bytes())
    mutant, mutant_trigger, mutant_claim_id = run_commit(mutate=True)
    mutant_text = mutant.stderr.decode("utf-8", errors="replace")
    assert mutant.returncode == 0, mutant_text
    assert expected not in mutant_text
    assert mutant_trigger.read_text(encoding="utf-8") == "triggered"
    assert marker.is_file()
    assert trace.read_text(encoding="utf-8").splitlines() == [
        "trigger", "trigger", "git"]
    mutant_events = [json.loads(line) for line in
                     (repo / "dev" / "intents.jsonl").read_text(
                         encoding="utf-8").splitlines()]
    assert any(event.get("event") == "release"
               and event.get("id") == mutant_claim_id for event in mutant_events)
    released = _run_tool(tool, ["list"], cwd=repo, env=env)
    assert "dev/routed.md" not in released.stdout


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

    # Declared exception (internal hook): operator acknowledgement needs a TTY; monkeypatched _confirm_proceed stands in for the keypress.
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


class TestIntentSurfacePruning:
    @pytest.mark.parametrize(
        "case", ["corpus", "recent-claim", "bad-timestamp", "hostile-link"],
    )
    def test_prune_drops_only_old_released_pairs_and_writes_through_no_link(
        self, tmp_path: Path, case: str,
    ) -> None:
        """Promise: ``prune`` removes only a released claim/release pair older
        than the window.  An unreleased claim (old or recent), an unparseable
        line, an unparseable timestamp and a pair inside the window all stay;
        the active set is unchanged; a link planted at the prune's own temp
        file name is never written through (the prune may refuse or finish, but
        the file the link points at keeps its bytes)."""
        tool = _git_repo(tmp_path)
        log = tmp_path / "dev" / "intents.jsonl"
        outside = tmp_path / "outside.txt"
        outside.write_text("DO NOT CHANGE\n", encoding="utf-8")
        if case == "recent-claim":
            _ledger(log, [
                {"event": "claim", "id": "old-1", "ts": _ts(45), "agent": "a",
                 "files": ["x.md"], "action": "old"},
                {"event": "release", "id": "old-1", "ts": _ts(44)},
                {"event": "claim", "id": "live", "ts": _ts(0.01), "agent": "b",
                 "files": ["y.md"], "action": "in flight"},
            ])
        elif case == "bad-timestamp":
            _ledger(log, [
                {"event": "claim", "id": "bad-ts", "ts": "not-a-date",
                 "agent": "a", "files": ["x.md"], "action": "x"},
                {"event": "release", "id": "bad-ts", "ts": "also-not-a-date"},
            ])
        else:
            _corpus(log)
        names_before = sorted(p.name for p in log.parent.iterdir())
        lines_before = log.read_text(encoding="utf-8").splitlines()
        active_before = _run_tool(tool, ["list"], cwd=tmp_path).stdout
        if case == "hostile-link":
            # The prune names its temp file after its own process id, so plant
            # the link under that name from inside the process that then runs
            # the real command.
            pruned = subprocess.run(
                [sys.executable, "-c",
                 "import os, runpy, sys\n"
                 "tool, ledger, outside = sys.argv[1:4]\n"
                 "os.symlink(outside, ledger + '.prune-%d.tmp' % os.getpid())\n"
                 "sys.argv = [tool, 'prune', '--older-than-days', '30']\n"
                 "runpy.run_path(tool, run_name='__main__')\n",
                 str(tool), str(log), str(outside)],
                cwd=tmp_path, capture_output=True, text=True, env=_clean_env(),
            )
        else:
            pruned = _run_tool(tool, ["prune", "--older-than-days", "30"],
                               cwd=tmp_path)
        assert pruned.returncode == 0, pruned.stderr
        old_pair_gone = [line for line in lines_before if '"old-1"' not in line]
        allowed = {
            "corpus": [old_pair_gone],
            "hostile-link": [lines_before, old_pair_gone],
        }.get(case, [lines_before])
        assert log.read_text(encoding="utf-8").splitlines() in allowed
        assert _run_tool(tool, ["list"], cwd=tmp_path).stdout == active_before
        assert outside.read_text(encoding="utf-8") == "DO NOT CHANGE\n"
        assert not log.is_symlink()
        assert [p.name for p in log.parent.iterdir()
                if p.name not in names_before and not p.is_symlink()] == []

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

class TestDevTreeRefusesLinks:
    """``create_dev_tree`` guards every folder it makes, like every other write
    into the target. A link at ``dev/`` (or at a folder below it) would send
    each ``mkdir`` to the other end, so the whole set is checked before the
    first folder is made. The refusal is pinned at each folder in turn: a folder
    with children is also caught by its children's guards, but a leaf folder is
    caught only by its own, and skipping that one lets the install finish over
    the link or refuse late, after other folders were already made."""

    @staticmethod
    def _target_with_link(tmp_path: Path, link: str) -> tuple[Path, Path]:
        """A target where *link* (relative to it) points at an empty folder
        outside; returns (target, that folder)."""
        target = tmp_path / "tgt"
        target.mkdir()
        outside = tmp_path / "elsewhere"
        outside.mkdir()
        link_path = target / link
        link_path.parent.mkdir(parents=True, exist_ok=True)
        link_path.symlink_to(outside, target_is_directory=True)
        return target, outside

    @pytest.mark.parametrize("link", _DEV_DIRS)
    @pytest.mark.parametrize("dry_run", [False, True], ids=["write", "dry-run"])
    def test_create_dev_tree_refuses_a_linked_folder_and_makes_none(
        self, tmp_path: Path, link: str, dry_run: bool
    ) -> None:
        target, outside = self._target_with_link(tmp_path, link)
        before = _tree(target)
        with pytest.raises(ScaffoldSecurityError, match="symlinked"):
            create_dev_tree(target, dry_run=dry_run)
        assert list(outside.iterdir()) == [], (
            "folders were made at the far end of the link"
        )
        assert _tree(target) == before, (
            "folders were made before the linked one was reached"
        )

    def test_install_over_a_linked_dev_makes_no_folder_anywhere(
        self, tmp_path: Path
    ) -> None:
        target, outside = self._target_with_link(tmp_path, "dev")
        TestGitignoreSeedingRefusesLinks._write_profile(target)
        before = _tree(target)
        with pytest.raises(ScaffoldSecurityError, match="symlinked"):
            TestGitignoreSeedingRefusesLinks._run_install(target)
        assert list(outside.iterdir()) == []
        assert _tree(target) == before


@pytest.mark.parametrize("relative", [False, True], ids=["absolute", "relative"])
def test_linked_worktree_claim_reaches_both_real_hooks(
    tmp_path: Path, relative: bool,
) -> None:
    """A linked CLI claim is read by the main hook tools and auto-released."""
    main = tmp_path / "main"
    main.mkdir()
    main_tool = _git_repo(main)
    (main / "dev" / "seed.txt").write_text("seed\n", encoding="utf-8")
    subprocess.run(["git", "add", "tools", "dev/seed.txt"], cwd=main,
                   check=True, env=_clean_env())
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=main,
                   check=True, env=_clean_env())
    linked = tmp_path / "linked"
    subprocess.run(["git", "worktree", "add", "-q", "-b", "linked",
                    str(linked)], cwd=main, check=True, env=_clean_env())
    dotgit = linked / ".git"
    admin = Path(dotgit.read_text(encoding="utf-8").split(": ", 1)[1].strip())
    if not admin.is_absolute():
        admin = linked / admin
    if relative:
        # Git for Windows marks this file hidden; creating it again fails.
        with dotgit.open("r+", encoding="utf-8") as pointer:
            pointer.write("gitdir: " + os.path.relpath(admin, linked) + "\n")
            pointer.truncate()
        (admin / "gitdir").write_text(
            os.path.relpath(dotgit, admin) + "\n", encoding="utf-8")
    linked_tool = _stage_tool(linked / "tools")
    env = _clean_env(CLAUDE_CODE_SESSION_ID="shared-worktree-test")
    assert _run_tool(main_tool, ["install-hook"], cwd=main, env=env).returncode == 0
    assert _run_tool(main_tool, ["install-precommit"], cwd=main, env=env).returncode == 0
    claim = _run_tool(linked_tool, ["claim", "--files", "change.txt",
                                    "--action", "linked edit"],
                      cwd=linked, env=env)
    assert claim.returncode == 0, claim.stderr
    assert "using checkout-local claims log" not in claim.stderr
    expected_log = main / "dev" / "intents.jsonl"
    assert expected_log.is_file()
    assert not (linked / "dev" / "intents.jsonl").exists()
    (linked / "change.txt").write_text("change\n", encoding="utf-8")
    subprocess.run(["git", "add", "change.txt"], cwd=linked, check=True, env=env)
    committed = subprocess.run(["git", "commit", "-q", "-m", "linked change"],
                               cwd=linked, capture_output=True, text=True, env=env)
    assert committed.returncode == 0, committed.stderr
    assert "no active claim" not in committed.stderr
    assert "CONFLICT CHECK" not in committed.stderr
    released = _run_tool(main_tool, ["list"], cwd=main, env=env)
    assert released.returncode == 0, released.stderr
    assert "no active intents" in released.stdout
    held_dev = tmp_path / "held-main-dev"
    (main / "dev").rename(held_dev)
    fallback = _run_tool(linked_tool, ["claim", "--files", "fallback.txt",
                                       "--action", "local fallback"],
                         cwd=linked, env=env)
    assert fallback.returncode == 0, fallback.stderr
    assert "main checkout is missing" in fallback.stderr
    assert not (main / "dev").exists(), "fallback must not create main/dev"
    assert (linked / "dev" / "intents.jsonl").is_file()


def _pointer_fixture(base: Path, *, relative: bool = False) -> tuple[Path, Path, Path]:
    """Build the documented Git pointer topology with independently known paths."""
    main = base / "main"
    common = main / ".git"
    admin = common / "worktrees" / "linked"
    linked = base / "linked"
    (main / "dev").mkdir(parents=True)
    admin.mkdir(parents=True)
    linked.mkdir()
    admin.joinpath("commondir").write_text(
        os.path.relpath(common, admin) if relative else str(common),
        encoding="utf-8",
    )
    admin.joinpath("gitdir").write_text(
        os.path.relpath(linked / ".git", admin) if relative else str(linked / ".git"),
        encoding="utf-8",
    )
    (linked / ".git").write_text(
        "gitdir: " + (os.path.relpath(admin, linked) if relative else str(admin)) + "\n",
        encoding="utf-8",
    )
    return main, admin, linked


@pytest.mark.parametrize("guard", ["backpointer", "link", "no-dev"])
def test_pointer_guard_negative_controls_through_intent_cli(
    tmp_path: Path, guard: str,
) -> None:
    main, admin, linked = _pointer_fixture(tmp_path)
    (linked / "dev").mkdir()
    _stage_tool(linked / "tools")
    main_log = main / "dev" / "intents.jsonl"
    main_log.write_text(
        '{"event":"claim","id":"outside","ts":"2026-01-01T00:00:00",'
        '"agent":"other","files":["x"],"action":"outside"}\n',
        encoding="utf-8",
    )
    env = _clean_env(CAIRN_AGENT="pointer-check")
    tool = linked / "tools" / "intent.py"
    if guard == "backpointer":
        copied = tmp_path / "copied"
        copied.mkdir()
        (copied / ".git").write_text("gitdir: unrelated\n", encoding="utf-8")
        (admin / "gitdir").write_text(str(copied / ".git"), encoding="utf-8")
    elif guard == "link":
        original = admin / "commondir"
        saved = admin / "commondir.real"
        original.rename(saved)
        original.symlink_to(saved)
    else:
        main_log.unlink()
        (main / "dev").rmdir()
        result = _run_tool(tool, ["claim", "--files", "new.txt", "--action", "x"],
                           cwd=linked, env=env)
        assert result.returncode == 0, result.stderr
        assert "dev directory is absent" in result.stderr
        assert not (main / "dev").exists()
        assert (linked / "dev" / "intents.jsonl").is_file()
        return
    result = _run_tool(tool, ["list"], cwd=linked, env=env)
    assert result.returncode == 0, result.stderr
    assert "using checkout-local claims log" in result.stderr
    assert "outside" not in result.stdout
    assert "no active intents" in result.stdout


@pytest.mark.parametrize("component", ["checkout", "gitdir", "commondir", "backpointer"])
@pytest.mark.parametrize("link", [False, True], ids=["real-directory", "symlink"])
def test_raw_dotdot_components_through_intent_cli(
    tmp_path: Path, component: str, link: bool,
) -> None:
    """A link erased by normalization must not acquire shared-log access."""
    main, admin, linked = _pointer_fixture(tmp_path)
    tool = _stage_tool(linked / "tools")
    jump = tmp_path / "jump"
    if link:
        other = tmp_path / "other"
        other.mkdir()
        try:
            jump.symlink_to(other, target_is_directory=True)
        except OSError as exc:
            pytest.skip(f"symlinks unavailable: {exc}")
    else:
        jump.mkdir()
    destinations = {
        "checkout": linked, "gitdir": admin,
        "commondir": main / ".git", "backpointer": linked / ".git",
    }
    raw = jump / ".." / destinations[component].relative_to(tmp_path)
    assert raw.resolve() == destinations[component]
    if component == "checkout":
        tool = raw / "tools" / "intent.py"
    else:
        pointer = {"gitdir": linked / ".git", "commondir": admin / "commondir",
                   "backpointer": admin / "gitdir"}[component]
        prefix = "gitdir: " if component == "gitdir" else ""
        pointer.write_text(prefix + str(raw) + "\n", encoding="utf-8")
    result = _run_tool(tool, ["claim", "--files", "x", "--action", "raw path"],
                       cwd=linked, env=_clean_env(CAIRN_AGENT="raw-path"))
    assert result.returncode == 0, result.stderr
    assert ("using checkout-local claims log" in result.stderr) == link
    assert (linked / "dev" / "intents.jsonl").is_file() == link
    assert (main / "dev" / "intents.jsonl").is_file() == (not link)


@pytest.mark.parametrize("mode", ["ordinary", "copied", "file-alias"])
def test_resolved_launcher_origin_selects_engine_code(tmp_path: Path, mode: str) -> None:
    trusted = tmp_path / "trusted"
    alias = tmp_path / "alias"
    for root in (trusted, alias):
        (root / "dev").mkdir(parents=True)
        (root / ".git").mkdir()
    tool = _stage_tool(trusted / "tools")
    alias_tool = alias / "tools" / "intent.py"
    planted = alias_tool.parent / "_intent"
    planted.mkdir(parents=True)
    marker = tmp_path / "sibling-executed"
    (planted / "__init__.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n"
        "def main(argv=None):\n    return 0\n", encoding="utf-8",
    )
    if mode == "copied":
        alias_tool.write_bytes(tool.read_bytes())
        tool = alias_tool
    elif mode == "file-alias":
        try:
            alias_tool.symlink_to(tool)
        except OSError as exc:
            pytest.skip(f"symlinks unavailable: {exc}")
        tool = alias_tool
    result = _run_tool(tool, ["list"], cwd=tmp_path, env=_clean_env())
    assert result.returncode == 0, result.stderr
    assert marker.exists() == (mode == "copied")
    if mode != "copied":
        assert "no active intents" in result.stdout


def test_checkout_alias_through_intent_cli_falls_back(tmp_path: Path) -> None:
    main, _admin, linked = _pointer_fixture(tmp_path)
    _stage_tool(linked / "tools")
    alias = tmp_path / "linked-alias"
    try:
        alias.symlink_to(linked, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"symlinks unavailable: {exc}")
    result = _run_tool(alias / "tools" / "intent.py",
                       ["claim", "--files", "x", "--action", "alias"],
                       cwd=linked, env=_clean_env(CAIRN_AGENT="raw-alias"))
    assert result.returncode == 0, result.stderr
    assert "checkout or .git path contains a link or reparse point" in result.stderr
    assert (linked / "dev" / "intents.jsonl").is_file()
    assert not (main / "dev" / "intents.jsonl").exists()


@pytest.mark.parametrize("mode,change", [
    ("shared", "unchanged"), ("shared", "missing-dev"),
    ("shared", "missing-main"), ("shared", "linked-dev"),
    ("override", "missing-dev"), ("patched", "missing-dev"),
    ("main", "missing-dev"),
])
def test_late_shared_append_through_facade_main(
    tmp_path: Path, mode: str, change: str,
) -> None:
    """Default CLI paths are explicit; their cached shared parent is not created."""
    main, _admin, linked = _pointer_fixture(tmp_path)
    root = main if mode == "main" else linked
    tool = _stage_tool(root / "tools")
    override = linked / "override" / "nested" / "intents.jsonl"
    code = '''
import importlib.util
from pathlib import Path
import sys
spec = importlib.util.spec_from_file_location('late_intent', sys.argv[1])
tool = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tool
spec.loader.exec_module(tool)
main, mode, change, override = Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5])
assert tool.INTENTS_LOG_PATH == main / 'dev' / 'intents.jsonl'
if change == 'missing-main':
    main.rename(main.with_name('main-held'))
elif change in ('missing-dev', 'linked-dev'):
    dev = main / 'dev'
    held = main / 'dev-held'
    dev.rename(held)
    if change == 'linked-dev':
        try:
            dev.symlink_to(held, target_is_directory=True)
        except OSError:
            raise SystemExit(77)
args = ['claim', '--files', 'x', '--action', 'late append']
if mode == 'override':
    args = ['--log-path', str(override)] + args
elif mode == 'patched':
    tool.INTENTS_LOG_PATH = override
raise SystemExit(tool.main(args))
'''
    result = subprocess.run(
        [sys.executable, "-c", code, str(tool), str(main), mode, change, str(override)],
        cwd=root, capture_output=True, text=True,
        env=_clean_env(CAIRN_AGENT="late-append"),
    )
    if result.returncode == 77:
        pytest.skip("directory symlinks unavailable")
    refused = mode == "shared" and change != "unchanged"
    if refused:
        assert result.returncode != 0
        assert "shared claims directory is missing or linked; refusing append" in result.stderr
        assert not (main / "dev" / "intents.jsonl").exists()
        assert not (main / "dev-held" / "intents.jsonl").exists()
        assert not (tmp_path / "main-held" / "dev" / "intents.jsonl").exists()
    else:
        assert result.returncode == 0, result.stderr
        expected = override if mode in {"override", "patched"} else main / "dev" / "intents.jsonl"
        assert json.loads(expected.read_text(encoding="utf-8"))["event"] == "claim"
    if change == "missing-dev" and mode != "main":
        assert not (main / "dev").exists()
    if change == "missing-main":
        assert not main.exists()
    assert not (linked / "dev" / "intents.jsonl").exists()


@pytest.mark.parametrize(
    "layout",
    ["valid", "checkout", "dotgit", "admin", "commondir", "common",
     "backpointer", "main", "dev", "malformed", "submodule",
     "separate-git-dir", "bare", "moved"],
)
def test_odd_layouts_and_links_at_any_pointer_component_use_the_local_ledger(
    tmp_path: Path, layout: str,
) -> None:
    """Promise: a checkout whose Git pointer chain is odd, or has a link at any
    component, lists its own checkout-local ledger and never the main checkout's.
    The ``valid`` case is the control: the same chain without a fault does read
    the main checkout's ledger."""
    main, admin, linked = _pointer_fixture(tmp_path)
    tool = _stage_tool(linked / "tools")
    (linked / "dev").mkdir()
    (main / "dev" / "intents.jsonl").write_text(
        json.dumps({"event": "claim", "id": "outside", "ts": _ts(0.01),
                    "agent": "other", "files": ["x"], "action": "outside"})
        + "\n", encoding="utf-8",
    )
    probe = tmp_path / "symlink-probe"
    try:
        probe.symlink_to(tmp_path, target_is_directory=True)
        probe.unlink()
    except OSError as exc:
        pytest.skip(f"symlinks unavailable: {exc}")
    if layout == "checkout":
        alias = tmp_path / "linked-alias"
        alias.symlink_to(linked, target_is_directory=True)
        tool = alias / "tools" / "intent.py"
    elif layout == "dotgit":
        (linked / ".git").rename(linked / ".git.real")
        (linked / ".git").symlink_to(linked / ".git.real")
    elif layout == "admin":
        admin.rename(admin.with_name("linked.real"))
        admin.symlink_to(admin.with_name("linked.real"), target_is_directory=True)
    elif layout in {"commondir", "backpointer"}:
        pointer = admin / ("commondir" if layout == "commondir" else "gitdir")
        pointer.rename(pointer.with_name(pointer.name + ".real"))
        pointer.symlink_to(pointer.with_name(pointer.name + ".real"))
    elif layout in {"common", "main", "dev"}:
        held = {"common": main / ".git", "main": main, "dev": main / "dev"}[layout]
        held.rename(held.with_name(held.name + ".real"))
        held.symlink_to(held.with_name(held.name + ".real"), target_is_directory=True)
    elif layout == "malformed":
        (linked / ".git").write_text("not a git pointer\n", encoding="utf-8")
    elif layout in {"submodule", "separate-git-dir"}:
        elsewhere = tmp_path / f"{layout}-admin"
        elsewhere.mkdir()
        (linked / ".git").write_text(f"gitdir: {elsewhere}\n", encoding="utf-8")
    elif layout == "bare":
        (linked / ".git").unlink()
        (linked / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    elif layout == "moved":
        main.rename(tmp_path / "moved-main")
    result = _run_tool(tool, ["list"], cwd=linked,
                       env=_clean_env(CAIRN_AGENT="layout-check"))
    assert result.returncode == 0, result.stderr
    if layout == "valid":
        assert "outside" in result.stdout
        assert "checkout-local" not in result.stderr
    else:
        assert "checkout-local" in result.stderr
        assert "outside" not in result.stdout


# Declared exception (internal hook): Windows reparse attributes cannot be created on macOS; resolver is fed directly.
@pytest.mark.parametrize(
    "component", ["checkout", "dotgit", "admin", "commondir", "common",
                  "backpointer", "main", "dev"],
)
def test_shared_resolver_rejects_reparse_attributes_at_pointer_components(
    tmp_path: Path, monkeypatch, component: str,
) -> None:
    from types import SimpleNamespace

    source = TEMPLATES_ROOT / "modules" / "team-gated" / "_intent" / "shared.py"
    shared = _load_tool(source, name=f"shared_reparse_{component}")
    main, admin, linked = _pointer_fixture(tmp_path)
    targets = {
        "checkout": linked,
        "dotgit": linked / ".git",
        "admin": admin,
        "commondir": admin / "commondir",
        "common": main / ".git",
        "backpointer": admin / "gitdir",
        "main": main,
        "dev": main / "dev",
    }
    target = targets[component]
    real_lstat = os.lstat

    def lstat_with_reparse(path):
        info = real_lstat(path)
        if Path(path) == target:
            return SimpleNamespace(
                st_mode=info.st_mode,
                st_file_attributes=getattr(info, "st_file_attributes", 0) | 0x400,
            )
        return info

    monkeypatch.setattr(shared, "_REPO_ROOT", linked)
    monkeypatch.setattr(shared.os, "lstat", lstat_with_reparse)
    path, reason = shared._shared_intents_path()
    assert path == linked / "dev" / "intents.jsonl"
    assert reason and ("link" in reason or "reparse" in reason)


# Declared exception (internal hook): Windows drive-letter case cannot be produced through the CLI on macOS; _path_key called directly.
@pytest.mark.skipif(os.name != "nt", reason="Windows drive normalization requires Windows")
def test_windows_drive_case_normalization_for_pointer_chain(tmp_path: Path, monkeypatch) -> None:
    source = TEMPLATES_ROOT / "modules" / "team-gated" / "_intent" / "shared.py"
    shared = _load_tool(source, name="shared_windows_drive_case")
    main, admin, linked = _pointer_fixture(tmp_path)

    def flipped(path: Path) -> str:
        drive, tail = os.path.splitdrive(str(path))
        return drive.swapcase() + tail

    admin_pointer = linked / ".git"
    admin_pointer.write_text(f"gitdir: {flipped(admin)}\n", encoding="utf-8")
    (admin / "commondir").write_text(flipped(main / ".git"), encoding="utf-8")
    (admin / "gitdir").write_text(flipped(linked / ".git") + "\n", encoding="utf-8")
    monkeypatch.setattr(shared, "_REPO_ROOT", linked)
    path, reason = shared._shared_intents_path()
    assert reason is None
    assert shared._path_key(path) == shared._path_key(main / "dev" / "intents.jsonl")
