"""Tests for the fail-closed release security check (security-hardening Chunk 7).

``bootstrap/security_check.py`` is the release-facing counterpart to the dev
Bandit gate: where the gate *skips* when Bandit is absent locally, the
release check **fails closed** -- release evidence must be unskippable (R1).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import security_check  # noqa: E402


def _bandit_available() -> bool:
    try:
        import bandit  # noqa: F401
    except ImportError:
        return False
    return True


# ---------------------------------------------------------------------------
# Phase 1 -- repository-state preflight / postflight
#
# The oracle for these is **real git**, run over a throwaway repository, with
# ``security_check.CAIRN_ROOT`` repointed at it. A stub of ``git status`` would
# be a fixture written by the same understanding the subject encodes, and the
# specific fail-open being closed here (an untracked file reading as clean) is
# a fact about git's porcelain defaults, not about Cairn's code.
# ---------------------------------------------------------------------------

def _setup_git(*args: str, cwd: Path) -> None:
    """Drive the FIXTURE repository. Deliberately not ``security_check._git``:
    that helper is the subject, and building the fixture with it would let a
    broken subject construct the state it is then asked to judge."""
    proc = subprocess.run(
        ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example",
         "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=master",
         "-C", str(cwd), *args],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, f"fixture git {args}: {proc.stderr}"


@pytest.fixture()
def repo(tmp_path, monkeypatch) -> Path:
    """A one-commit throwaway repository, with the subject pointed at it."""
    root = tmp_path / "candidate"
    root.mkdir()
    _setup_git("init", "-q", cwd=root)
    (root / "tracked.py").write_text("x = 1\n", encoding="utf-8")
    _setup_git("add", "tracked.py", cwd=root)
    _setup_git("commit", "-q", "-m", "fixture", cwd=root)
    monkeypatch.setattr(security_check, "CAIRN_ROOT", root)
    return root


def test_preflight_passes_on_a_clean_checkout_and_returns_the_real_head(repo) -> None:
    rc, head = security_check.repo_state_preflight()
    assert rc == 0
    expected = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True)
    assert head == expected.stdout.strip()
    assert head is not None and len(head) == 40


def test_preflight_refuses_a_modified_tracked_file(repo, capsys) -> None:
    (repo / "tracked.py").write_text("x = 2\n", encoding="utf-8")
    rc, head = security_check.repo_state_preflight()
    assert (rc, head) == (1, None)
    assert "worktree is not clean" in capsys.readouterr().err


def test_preflight_refuses_an_untracked_file(repo, capsys) -> None:
    """The reproduced fail-open: ``git status --porcelain`` with git's default
    ``--untracked-files=normal`` DOES list untracked files, but the tracked-only
    check this command grew from (``--untracked-files=no``, the shape used by the
    gate-ceremony preflight) does not -- and an untracked ``.py`` under a scanned
    root is a file the release scan may open and no adopter can fetch."""
    (repo / "rogue.py").write_text("import os\n", encoding="utf-8")
    rc, head = security_check.repo_state_preflight()
    assert (rc, head) == (1, None)
    err = capsys.readouterr().err
    assert "worktree is not clean" in err
    assert "rogue.py" in err


def test_preflight_refuses_an_untracked_file_inside_an_untracked_directory(
        repo, capsys) -> None:
    """``--untracked-files=all`` rather than ``normal``: git's ``normal`` mode
    collapses an untracked directory to the directory name, which is still
    non-empty, so this pins the *listing* rather than only the refusal -- an
    operator has to see the file to fix it."""
    (repo / "sub").mkdir()
    (repo / "sub" / "rogue.py").write_text("import os\n", encoding="utf-8")
    rc, _head = security_check.repo_state_preflight()
    assert rc == 1
    assert "sub/rogue.py" in capsys.readouterr().err


def test_preflight_refuses_a_subdirectory_of_the_checkout(repo, monkeypatch,
                                                          capsys) -> None:
    """``git -C`` discovers upward: pointed at a subdirectory, every check below
    would answer about the enclosing repository, and the run would pass against
    a commit the invocation never named."""
    sub = repo / "nested"
    sub.mkdir()
    monkeypatch.setattr(security_check, "CAIRN_ROOT", sub)
    rc, head = security_check.repo_state_preflight()
    assert (rc, head) == (1, None)
    err = capsys.readouterr().err
    assert "not the top level of a git worktree" in err
    assert "FAIL CLOSED" in err


def test_preflight_refuses_when_there_is_no_repository(tmp_path, monkeypatch,
                                                        capsys) -> None:
    bare = tmp_path / "no-repo"
    bare.mkdir()
    monkeypatch.setattr(security_check, "CAIRN_ROOT", bare)
    rc, head = security_check.repo_state_preflight()
    assert (rc, head) == (1, None)
    assert "FAIL CLOSED" in capsys.readouterr().err


def test_preflight_fails_closed_when_git_is_unavailable(repo, monkeypatch,
                                                         capsys) -> None:
    monkeypatch.setattr(security_check.shutil, "which", lambda _n: None)
    rc, head = security_check.repo_state_preflight()
    assert (rc, head) == (1, None)
    err = capsys.readouterr().err
    assert "git was not found on PATH" in err
    assert "FAIL CLOSED" in err


def test_postflight_refuses_a_head_that_moved_mid_run(repo, capsys) -> None:
    rc, head = security_check.repo_state_preflight()
    assert rc == 0 and head is not None
    (repo / "tracked.py").write_text("x = 3\n", encoding="utf-8")
    _setup_git("commit", "-q", "-a", "-m", "candidate changed", cwd=repo)
    assert security_check.repo_state_postflight(head) == 1
    assert "HEAD moved during the run" in capsys.readouterr().err


def test_postflight_refuses_a_worktree_dirtied_mid_run(repo, capsys) -> None:
    rc, head = security_check.repo_state_preflight()
    assert rc == 0 and head is not None
    (repo / "appeared.py").write_text("y = 1\n", encoding="utf-8")
    assert security_check.repo_state_postflight(head) == 1
    assert "modified during the run" in capsys.readouterr().err


def test_postflight_passes_when_nothing_moved(repo) -> None:
    rc, head = security_check.repo_state_preflight()
    assert rc == 0 and head is not None
    assert security_check.repo_state_postflight(head) == 0


def test_state_git_calls_are_sterile(repo, monkeypatch) -> None:
    """A2: the steering environment is stripped and execution-bearing config is
    disabled on the state check itself -- the check that decides whether a
    release may be cut must not be steerable by in-repo config or by the
    environment it inherits."""
    monkeypatch.setenv("GIT_DIR", "/elsewhere/.git")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/elsewhere/gitconfig")
    monkeypatch.setenv("GIT_EXTERNAL_DIFF", "/bin/false")
    seen: dict = {}
    real_run = subprocess.run

    def _spy(cmd, **kwargs):
        seen["cmd"] = list(cmd)
        seen["env"] = dict(kwargs.get("env") or {})
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(security_check.subprocess, "run", _spy)
    assert security_check._dirty_entries() == []

    assert seen["cmd"][0].startswith("/"), (
        "git must be invoked by absolute path -- a partial path resolves "
        f"through PATH: {seen['cmd'][0]}")
    for key, value in security_check._STERILE_GIT_CONFIG.items():
        token = f"{key}={value}"
        assert token in seen["cmd"], f"missing -c {token}"
        assert seen["cmd"][seen["cmd"].index(token) - 1] == "-c"
    leaked = sorted(k for k in seen["env"]
                    if k.startswith("GIT_") and k != "GIT_TERMINAL_PROMPT")
    assert leaked == [], f"GIT_* steering variables reached git: {leaked}"
    assert seen["env"]["GIT_TERMINAL_PROMPT"] == "0"
    assert seen["env"]["PATH"] == os.environ["PATH"], (
        "the operator's PATH is deliberately preserved -- dropping it would "
        "break git's own helper lookup")


def test_scan_targets_are_explicit_files_and_name_the_expected_executables() -> None:
    """What each half of this test can and cannot do -- stated plainly, because
    the old name (``..._covering_shipped_surface``) claimed a property it did
    not have, and a test that names a property it lacks is worse than a missing
    test: it retires the question.

    * **The named literals CAN fail.** A file dropping out of the scan set
      fails them; the two skills tools below fail if the manifest union in
      ``scan_targets()`` is removed. Their oracle is path strings typed by a
      human, so there is no shared derivation with the subject.
    * **The ``_ALWAYS_ON_MAPPINGS`` loop CANNOT fail on registry drift.** Its
      oracle is the very registry the subject reads, so a gap moves both and
      the difference stays empty -- and after the manifest union landed it
      cannot fail on the loop's *deletion* either, since the union covers the
      identical ``templates/modules/{src}`` strings. It is retained as a
      readable inventory, not as a guard.
    * **The two real guards are elsewhere**: the growth tripwire ``assert
      scanned == 9`` in ``bootstrap/tests/test_upgrade_side_door_parity.py``,
      and the on-disk oracle in ``bootstrap/tests/test_security_lint.py``
      (``test_every_templates_py_on_disk_is_release_scanned``), whose input
      ``scan_targets()`` never reads."""
    targets = set(security_check.scan_targets())
    assert "bootstrap/scaffold.py" in targets
    # Cairn's own bootstrap security tooling is itself scanned.
    assert "bootstrap/security_check.py" in targets
    assert "bootstrap/verify_integrity.py" in targets
    assert "templates/modules/team-gated/link_check.py" in targets
    # content_scan is single-sourced as the content-security module script.
    assert "templates/modules/team-gated/content_scan.py" in targets
    # The two session-lifecycle tools: shipped verbatim to EVERY adoption via
    # _SKILLS_MAPPINGS, and release-unscanned for 63 days because no registry
    # loop reached them. These literals are genuine -- they fail if the
    # manifest union is removed from scan_targets().
    assert "templates/skills/_lib/lifecycle.py" in targets
    assert "templates/skills/_lib/lifecycle_planner.py" in targets
    # Always-on executable helpers (onboarding launcher + every engine member)
    # are release-scanned -- they ship verbatim outside _MODULE_MAPPINGS, so the
    # side-door-parity change (security_check consumes _ALWAYS_ON_MAPPINGS too)
    # must cover them. A regression here re-opens the pre-existing scan blind spot.
    from bootstrap._scaffold.config import _ALWAYS_ON_MAPPINGS
    assert "templates/modules/default-on/onboarding_activate.py" in targets
    for spec in _ALWAYS_ON_MAPPINGS:
        if spec.verbatim and spec.src.endswith(".py"):
            assert f"templates/modules/{spec.src}" in targets, spec.src
    # Explicit files only -- no bare directory (the no-`-r` footgun).
    assert all(t.endswith(".py") for t in targets), targets


def test_fail_closed_when_bandit_absent(monkeypatch) -> None:
    """A missing Bandit FAILS (nonzero), unlike the dev gate's local skip --
    release evidence is unskippable (R1)."""
    class _Proc:
        returncode = 127
        stdout = ""
        stderr = "No module named bandit"

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1


def test_fail_closed_on_scanner_error(monkeypatch) -> None:
    class _Proc:
        returncode = 2
        stdout = ""
        stderr = "bandit: config error"

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1


def test_fail_closed_on_bandit_file_errors(monkeypatch) -> None:
    """A file Bandit could not OPEN is not a file Bandit found clean.

    Bandit records an unreadable/unparseable target in the JSON ``errors``
    array, scans the rest, and exits **0** -- so the rc-not-in-{0,1} branch
    never fires and the gate would print "clean over N shipped file(s)" over a
    file it never read. Fail closed (scan-coverage plan, Chunk A / [I1])."""
    class _Proc:
        returncode = 0
        stdout = json.dumps({
            "errors": [{"filename": "/nonexistent/missing_file.py",
                        "reason": "No such file or directory"}],
            "results": [],
        })
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1


def test_fail_closed_when_the_manifest_refuses(monkeypatch, capsys) -> None:
    """``install_manifest`` REFUSES a malformed mapping (two sources claiming
    one destination) by raising ValueError. The gate must report that as a
    security failure, not as a traceback -- a scan set that cannot be
    enumerated is not a scan set that came back empty."""
    def _refuse():
        raise ValueError("destination-ownership conflict")

    monkeypatch.setattr(security_check, "scan_targets", _refuse)
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "cannot enumerate the shipped surface" in err
    assert "FAIL CLOSED" in err


@pytest.mark.skipif(not _bandit_available(), reason="bandit not installed")
def test_fail_closed_on_a_missing_target_with_real_bandit(tmp_path, monkeypatch) -> None:
    """The same fail-close, with the verdict coming from **real Bandit**
    rather than from a stub of it: a two-file scan set where one target does
    not exist. Two files, so it costs milliseconds."""
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    monkeypatch.setattr(security_check, "CAIRN_ROOT", tmp_path)
    monkeypatch.setattr(security_check, "scan_targets",
                        lambda: ["ok.py", "gone.py"])
    assert security_check.run_bandit() == 1


@pytest.mark.skipif(not _bandit_available(), reason="bandit not installed")
def test_run_bandit_clean_with_bandit_present() -> None:
    # The shipped surface is clean of unallowlisted MEDIUM+ after Chunks 1-3.
    assert security_check.run_bandit() == 0
