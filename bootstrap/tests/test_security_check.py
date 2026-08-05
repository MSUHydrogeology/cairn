"""Tests for the fail-closed release security check (security-hardening Chunk 7).

``bootstrap/security_check.py`` is the release-facing counterpart to the dev
Bandit gate: where the gate *skips* when Bandit is absent locally, the
release check **fails closed** -- release evidence must be unskippable (R1).
"""
from __future__ import annotations

import json
import os
import shutil
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


# ---------------------------------------------------------------------------
# Phases 3-4 -- the release-mode suite, the quality gate, and R1 propagation
# ---------------------------------------------------------------------------

def _spy_run(monkeypatch, rc: int = 0):
    """Replace ``subprocess.run`` inside the subject and record every call."""
    calls: list[dict] = []

    class _Proc:
        returncode = rc

    def _fake(cmd, **kwargs):
        calls.append({"cmd": list(cmd), "env": kwargs.get("env"),
                      "cwd": kwargs.get("cwd")})
        return _Proc()

    monkeypatch.setattr(security_check.subprocess, "run", _fake)
    return calls


def test_the_release_token_name_and_value_are_pinned_literals() -> None:
    """The token is a **cross-file contract** -- ``bootstrap/tests/conftest.py``
    recognizes this exact pair -- so it needs an oracle that is not the constant
    itself.

    Measured while building this file: mutating ``RELEASE_GATE_VALUE`` to
    ``"true"`` left every *other* node here green, because they read the
    expected value from the subject. Two hand-typed literals close that."""
    assert security_check.RELEASE_GATE_ENV == "CAIRN_RELEASE_GATE_ACTIVE"
    assert security_check.RELEASE_GATE_VALUE == "1"


def test_the_release_token_reaches_both_direct_children(monkeypatch) -> None:
    """**R1.3, direct half.** Both phase-3 and phase-4 children are handed the
    token EXPLICITLY and at the EXACT recognized value.

    This half is necessary and **not sufficient**: an implementation that built
    a correct dict here and still stripped the token from the real child would
    pass. The sufficient check is
    ``test_a_skipping_grandchild_makes_the_quality_gate_phase_nonzero``, which
    drives the genuine ``quality_gate -> pytest`` grandchild path."""
    calls = _spy_run(monkeypatch, rc=0)
    assert security_check.run_suite() == 0
    assert security_check.run_quality_gate() == 0
    assert len(calls) == 2
    for call in calls:
        env = call["env"]
        assert env is not None, (
            "the child environment must be passed EXPLICITLY, not inherited -- "
            f"{call['cmd']}")
        assert env[security_check.RELEASE_GATE_ENV] == \
            security_check.RELEASE_GATE_VALUE
        # A superset of the operator's environment: the quality gate's
        # order-independence sub-gate launches pytest as a grandchild with no
        # env= of its own, so anything dropped here never reaches it.
        assert set(os.environ) - {security_check.RELEASE_GATE_ENV} <= set(env)


def test_setting_the_token_does_not_leak_into_this_process(monkeypatch) -> None:
    """R1.1: built from a **copy**. A mutation of ``os.environ`` would make the
    parent's own pytest session release-mode too, and would survive into the
    Bandit and check_cairn phases that must not see it."""
    monkeypatch.delenv(security_check.RELEASE_GATE_ENV, raising=False)
    _spy_run(monkeypatch, rc=0)
    security_check.run_suite()
    assert security_check.RELEASE_GATE_ENV not in os.environ


def test_a_nonzero_suite_exit_is_a_refusal(monkeypatch, capsys) -> None:
    """Including the exits that are not test failures: pytest 4 is a usage
    error and 5 is "no tests collected" -- absent evidence, not a clean gate."""
    for rc in (1, 4, 5):
        _spy_run(monkeypatch, rc=rc)
        assert security_check.run_suite() == 1, rc
        assert f"exited {rc}" in capsys.readouterr().err


def test_suite_fails_closed_when_the_tests_directory_is_absent(
        tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(security_check, "CAIRN_ROOT", tmp_path)
    assert security_check.run_suite() == 1
    assert "fail closed" in capsys.readouterr().err


def test_suite_fails_closed_when_the_interpreter_cannot_be_spawned(
        monkeypatch, capsys) -> None:
    def _boom(*_a, **_k):
        raise OSError("Exec format error")

    monkeypatch.setattr(security_check.subprocess, "run", _boom)
    assert security_check.run_suite() == 1
    assert "cannot run the suite" in capsys.readouterr().err


def test_quality_gate_fails_closed_when_the_script_is_absent(
        tmp_path, monkeypatch, capsys) -> None:
    (tmp_path / "scripts").mkdir()
    monkeypatch.setattr(security_check, "CAIRN_ROOT", tmp_path)
    assert security_check.run_quality_gate() == 1
    assert "missing -- fail closed" in capsys.readouterr().err


def test_a_nonzero_quality_gate_exit_is_a_refusal(monkeypatch, capsys) -> None:
    _spy_run(monkeypatch, rc=1)
    assert security_check.run_quality_gate() == 1
    assert "quality_gate exited 1" in capsys.readouterr().err


def test_main_names_all_four_phases_in_order() -> None:
    assert [label for label, _fn in security_check._phases()] == [
        "bandit", "check_cairn", "release-mode suite", "quality_gate"]


def test_main_attempts_every_phase_after_the_first_failure(monkeypatch,
                                                           capsys) -> None:
    """B1: one run yields a COMPLETE repair list. Short-circuiting on the first
    failure would make a Maintainer re-run the whole gate per defect."""
    ran: list[str] = []

    def _phase(name, rc):
        def _fn():
            ran.append(name)
            return rc
        return _fn

    monkeypatch.setattr(security_check, "run_bandit", _phase("bandit", 1))
    monkeypatch.setattr(security_check, "run_check_cairn", _phase("cairn", 0))
    monkeypatch.setattr(security_check, "run_suite", _phase("suite", 1))
    monkeypatch.setattr(security_check, "run_quality_gate", _phase("qg", 0))
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (0, "a" * 40))
    monkeypatch.setattr(security_check, "repo_state_postflight", lambda _h: 0)

    assert security_check.main() == 1
    assert ran == ["bandit", "cairn", "suite", "qg"]
    err = capsys.readouterr().err
    assert "phase bandit did not pass" in err
    assert "phase release-mode suite did not pass" in err


def test_main_refuses_when_only_the_postflight_fails(monkeypatch, capsys) -> None:
    monkeypatch.setattr(security_check, "run_bandit", lambda: 0)
    monkeypatch.setattr(security_check, "run_check_cairn", lambda: 0)
    monkeypatch.setattr(security_check, "run_suite", lambda: 0)
    monkeypatch.setattr(security_check, "run_quality_gate", lambda: 0)
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (0, "b" * 40))
    monkeypatch.setattr(security_check, "repo_state_postflight", lambda _h: 1)
    assert security_check.main() == 1
    assert "FAIL" in capsys.readouterr().err


def test_main_stops_at_a_failed_preflight_and_runs_no_phase(monkeypatch) -> None:
    """A1: the preflight *stops the command*. Scanning a dirty tree and then
    reporting the dirt would waste a five-minute run and, worse, print scanner
    output an operator could mistake for release evidence."""
    ran: list[str] = []
    for name in ("run_bandit", "run_check_cairn", "run_suite",
                 "run_quality_gate"):
        monkeypatch.setattr(security_check, name,
                            (lambda n: lambda: (ran.append(n), 0)[1])(name))
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (1, None))
    assert security_check.main() == 1
    assert ran == []


def test_main_reports_the_full_head_on_a_clean_pass(monkeypatch, capsys) -> None:
    """A3: release notes have to be able to bind the run to a commit id."""
    head = "c" * 40
    monkeypatch.setattr(security_check, "run_bandit", lambda: 0)
    monkeypatch.setattr(security_check, "run_check_cairn", lambda: 0)
    monkeypatch.setattr(security_check, "run_suite", lambda: 0)
    monkeypatch.setattr(security_check, "run_quality_gate", lambda: 0)
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (0, head))
    monkeypatch.setattr(security_check, "repo_state_postflight", lambda _h: 0)
    assert security_check.main() == 0
    out = capsys.readouterr().out
    assert "PASS" in out and head in out


# ---------------------------------------------------------------------------
# Chunk C -- the release-mode outcome rule, and R1.3's decisive half
#
# The subject here is a **conftest plugin**, so it can only be exercised by an
# actual pytest session. Every test below copies the REAL
# ``bootstrap/tests/conftest.py`` into a throwaway tree and runs a child
# pytest over it: a re-implementation of the hooks in a fixture would be a
# check verified by a second copy of the thing it judges.
# ---------------------------------------------------------------------------

_CLEAN = "def test_ok():\n    assert True\n"
_SKIPPED = 'import pytest\n\n\ndef test_s():\n    pytest.skip("fixture skip")\n'
_SKIPIF_ACTIVE = (
    'import pytest\n\n\n@pytest.mark.skipif(True, reason="fixture")\n'
    "def test_si():\n    assert True\n")
_SKIPIF_INACTIVE = (
    'import pytest\n\n\n@pytest.mark.skipif(False, reason="fixture")\n'
    "def test_si():\n    assert True\n")
_XFAILED = ('import pytest\n\n\n@pytest.mark.xfail(reason="fixture")\n'
            "def test_xf():\n    assert False\n")
_XPASSED = ('import pytest\n\n\n@pytest.mark.xfail(reason="fixture")\n'
            "def test_xp():\n    assert True\n")


def _fixture_tree(tmp_path: Path, body: str) -> Path:
    """A throwaway tree carrying the real conftest plus one test module."""
    tests = tmp_path / "bootstrap" / "tests"
    tests.mkdir(parents=True)
    shutil.copy(CAIRN_ROOT / "bootstrap" / "tests" / "conftest.py",
                tests / "conftest.py")
    (tests / "test_fixture_outcome.py").write_text(body, encoding="utf-8")
    return tmp_path


def _child_pytest(root: Path, token: str | None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop(security_check.RELEASE_GATE_ENV, None)
    if token is not None:
        env[security_check.RELEASE_GATE_ENV] = token
    return subprocess.run(
        [sys.executable, "-m", "pytest", "bootstrap/tests", "-q",
         "-p", "no:cacheprovider"],
        cwd=str(root), env=env, capture_output=True, text=True, check=False,
    )


def test_the_conftest_recognizes_the_same_token_pair() -> None:
    """The token is a two-file contract and the conftest holds its own literals
    (it must import before ``sys.path`` reaches the repo root). This is what
    keeps the two sides equal."""
    import importlib.util

    path = CAIRN_ROOT / "bootstrap" / "tests" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_cairn_conftest_probe", path)
    assert spec is not None and spec.loader is not None
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)      # a fresh module object: pytest
    # registers plugins by identity, so this does not double-register hooks.
    assert probe.RELEASE_GATE_ENV == security_check.RELEASE_GATE_ENV
    assert probe.RELEASE_GATE_VALUE == security_check.RELEASE_GATE_VALUE


@pytest.mark.parametrize("body,label", [
    (_SKIPPED, "skipped"), (_SKIPIF_ACTIVE, "skipped"),
    (_XFAILED, "xfailed"), (_XPASSED, "xpassed"),
])
def test_release_mode_refuses_incomplete_evidence(tmp_path, body, label) -> None:
    root = _fixture_tree(tmp_path, body)
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "RELEASE MODE" in proc.stderr
    assert label in proc.stderr


@pytest.mark.parametrize("body", [_SKIPPED, _SKIPIF_ACTIVE, _XFAILED, _XPASSED])
@pytest.mark.parametrize("token", [None, "", "0", "true", "yes", "2"])
def test_contributor_behaviour_is_unchanged_without_the_exact_token(
        tmp_path, body, token) -> None:
    """Invariant 2. Absent, empty, falsy, and plausible-but-wrong values all
    leave ordinary skip semantics alone -- a release posture that switches on
    by accident is one a contributor learns to work around."""
    root = _fixture_tree(tmp_path, body)
    proc = _child_pytest(root, token)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RELEASE MODE" not in proc.stderr


def test_release_mode_leaves_an_inactive_skipif_marker_alone(tmp_path) -> None:
    """An outcome rule, NOT a marker census: a ``skipif`` whose condition is
    false ran normally and is not incomplete evidence. A census would refuse a
    release for a skip that never happened."""
    root = _fixture_tree(tmp_path, _SKIPIF_INACTIVE)
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RELEASE MODE" not in proc.stderr


def test_release_mode_passes_a_fully_clean_session(tmp_path) -> None:
    root = _fixture_tree(tmp_path, _CLEAN)
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_release_mode_does_not_overwrite_an_interrupted_exit_code(
        tmp_path) -> None:
    """A session that already ended non-zero keeps **its own** code. Collapsing
    pytest's 2 (interrupted) into 1 would report the more serious outcome as
    the less serious one -- and an interrupted session's skips are not the
    reason it must not ship."""
    root = _fixture_tree(tmp_path, _SKIPPED + (
        "\n\ndef test_interrupt():\n    raise KeyboardInterrupt\n"))
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode == 2, (
        f"expected pytest's INTERRUPTED (2), got {proc.returncode}\n"
        + proc.stdout + proc.stderr)
    assert "RELEASE MODE" in proc.stderr, (
        "the refusal report must still print -- an operator repairing a failing "
        "release run needs to see the skips too")


def test_release_mode_reports_skips_alongside_a_real_failure(tmp_path) -> None:
    root = _fixture_tree(tmp_path, _SKIPPED + (
        "\n\ndef test_f():\n    assert False\n"))
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode == 1
    assert "RELEASE MODE" in proc.stderr


def _quality_gate_tree(tmp_path: Path, body: str) -> Path:
    """A throwaway tree carrying the real conftest AND the real quality gate."""
    root = _fixture_tree(tmp_path, body)
    scripts = root / "scripts"
    scripts.mkdir()
    for name in ("quality_gate.py", "quality_gate_unused_def_whitelist.py"):
        shutil.copy(CAIRN_ROOT / "scripts" / name, scripts / name)
    return root


@pytest.mark.parametrize("body,expect_refusal", [
    (_SKIPPED, True), (_XFAILED, True), (_XPASSED, True), (_CLEAN, False),
])
def test_the_release_token_survives_the_real_grandchild_launcher(
        tmp_path, monkeypatch, body, expect_refusal) -> None:
    """**R1.3, the decisive half.** The chain under test is the real one:

    ``security_check.run_quality_gate()`` -> ``scripts/quality_gate.py`` ->
    ``pytest`` -> ``bootstrap/tests/conftest.py``

    The middle link launches pytest with **no** ``env=`` of its own
    (``quality_gate.py``, argv bound to ``cmd`` then ``subprocess.run(cmd,
    ...)``), so the token reaches the grandchild by *inheritance* through a
    process ``security_check`` handed an explicit environment. Nothing in
    ``test_the_release_token_reaches_both_direct_children`` would notice that
    link being broken -- a correct dict handed to a child that strips it
    satisfies the direct check and fails the release gate silently.

    Every part is genuine except the tree: the real quality gate, the real
    conftest, a real pytest, and ``run_quality_gate()``'s own environment
    construction."""
    root = _quality_gate_tree(tmp_path, body)
    monkeypatch.setattr(security_check, "CAIRN_ROOT", root)
    monkeypatch.delenv(security_check.RELEASE_GATE_ENV, raising=False)
    rc = security_check.run_quality_gate()
    assert rc == (1 if expect_refusal else 0)


def test_the_grandchild_is_clean_without_the_token(tmp_path, monkeypatch) -> None:
    """The other direction of the same chain, and the guard against a test that
    passes for the wrong reason: with the token removed from the child
    environment builder, the identical skipping fixture is *accepted*. So the
    refusal above is the token's doing, not the fixture merely being red."""
    root = _quality_gate_tree(tmp_path, _SKIPPED)
    monkeypatch.setattr(security_check, "CAIRN_ROOT", root)
    monkeypatch.setattr(security_check, "_release_child_env",
                        lambda: {k: v for k, v in os.environ.items()
                                 if k != security_check.RELEASE_GATE_ENV})
    assert security_check.run_quality_gate() == 0


# ---------------------------------------------------------------------------
# Chunk D -- the self-retiring allowlist
#
# The plan cell put these in ``test_security_lint.py``; that file carried
# another session's uncommitted edit at implementation time, and a path-scoped
# commit naming it would have taken their work under this message. Homed here
# instead -- ``run_bandit()``'s liveness rule lives in ``security_check.py``,
# which is this file's subject.
# ---------------------------------------------------------------------------

def _bandit_report(monkeypatch, results: list[dict]) -> None:
    class _Proc:
        returncode = 1 if results else 0
        stdout = json.dumps({"errors": [], "results": results})
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())


def _finding(rel: str, test_id: str, severity: str) -> dict:
    return {"filename": str(CAIRN_ROOT / rel), "test_id": test_id,
            "issue_severity": severity, "line_number": 1,
            "issue_text": "fixture finding"}


def test_a_live_allowlist_entry_passes(monkeypatch, capsys) -> None:
    """Direction 1: the entry names a MEDIUM+ finding the scan reports, so the
    suppression is doing work and the gate is clean."""
    key = ("scripts/check_cairn.py", "B999")
    monkeypatch.setattr(security_check, "ALLOWLIST", {key: "fixture rationale"})
    _bandit_report(monkeypatch, [_finding(*key, "MEDIUM")])
    assert security_check.run_bandit() == 0
    assert "1 live allowlist entr" in capsys.readouterr().out


def test_an_absent_allowlist_entry_fails_closed(monkeypatch, capsys) -> None:
    """Direction 2, the one this chunk adds: the scan reports nothing at that
    (file, test_id), so the entry is a standing permission for a future finding
    and the gate refuses until it is deleted."""
    key = ("scripts/check_cairn.py", "B999")
    monkeypatch.setattr(security_check, "ALLOWLIST", {key: "fixture rationale"})
    _bandit_report(monkeypatch, [])
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "does not report at MEDIUM+" in err
    assert "scripts/check_cairn.py  B999" in err


def test_an_entry_matched_only_at_low_severity_is_not_live(monkeypatch,
                                                           capsys) -> None:
    """The subtle half. An entry whose finding Bandit reports at LOW filters
    nothing -- ``blocking`` never consults the allowlist below MEDIUM -- so
    counting it live would be exactly the fail-open the rule closes."""
    key = ("scripts/check_cairn.py", "B404")
    monkeypatch.setattr(security_check, "ALLOWLIST", {key: "fixture rationale"})
    _bandit_report(monkeypatch, [_finding(*key, "LOW")])
    assert security_check.run_bandit() == 1
    assert "does not report at MEDIUM+" in capsys.readouterr().err


def test_liveness_never_derives_from_a_partially_scanned_report(monkeypatch,
                                                                capsys) -> None:
    """An unreadable target must not retire an entry by making its finding
    'absent'. The ``errors`` branch returns first, so the refusal is the scan
    error -- not a stale-entry verdict computed over a report that is missing
    the file the entry names."""
    key = ("scripts/check_cairn.py", "B999")
    monkeypatch.setattr(security_check, "ALLOWLIST", {key: "fixture rationale"})

    class _Proc:
        returncode = 0
        stdout = json.dumps({
            "errors": [{"filename": "/gone.py", "reason": "No such file"}],
            "results": [],
        })
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "could not scan" in err
    assert "does not report at MEDIUM+" not in err


def test_blocking_findings_and_stale_entries_are_reported_together(
        monkeypatch, capsys) -> None:
    """One run, a complete repair list -- the same posture as main()'s phases."""
    stale = ("scripts/check_cairn.py", "B999")
    monkeypatch.setattr(security_check, "ALLOWLIST", {stale: "fixture"})
    _bandit_report(monkeypatch, [_finding("bootstrap/scaffold.py", "B888",
                                          "HIGH")])
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "unallowlisted MEDIUM+" in err
    assert "does not report at MEDIUM+" in err


def test_the_shipped_allowlist_is_empty_after_the_b310_retirement() -> None:
    """D1. Measured 2026-08-05 under Bandit 1.9.4 / Python 3.13.13: the sole
    entry's finding was absent from the report. It was deleted rather than left
    as a latch, and this pins that -- re-adding an entry has to come with a
    finding the scan actually reports, which the liveness rule then enforces."""
    assert security_check.ALLOWLIST == {}


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
