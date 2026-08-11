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


def test_detached_checkout_excludes_an_ignored_pytest_override(
        repo, capsys) -> None:
    """CR1's reproduced false pass, through real Git and real pytest.

    The source checkout is clean according to the production preflight even
    though an ignored root plugin can override the release hook at ``trylast``.
    The detached committed checkout must omit that plugin, so the identical
    release-mode child refuses the skip.
    """
    tests = repo / "bootstrap" / "tests"
    tests.mkdir(parents=True)
    shutil.copy(CAIRN_ROOT / "bootstrap" / "tests" / "conftest.py",
                tests / "conftest.py")
    (tests / "test_skipped.py").write_text(_SKIPPED, encoding="utf-8")
    _setup_git("add", "bootstrap/tests", cwd=repo)
    _setup_git("commit", "-q", "-m", "release fixture", cwd=repo)

    (repo / ".git" / "info" / "exclude").write_text(
        "/conftest.py\n", encoding="utf-8")
    (repo / "conftest.py").write_text(
        "import pytest\n\n"
        "@pytest.hookimpl(trylast=True)\n"
        "def pytest_sessionfinish(session, exitstatus):\n"
        "    session.exitstatus = 0\n",
        encoding="utf-8",
    )
    rc, head = security_check.repo_state_preflight()
    assert rc == 0 and head is not None
    assert _child_pytest(repo, security_check.RELEASE_GATE_VALUE).returncode == 0

    with security_check._detached_checkout(head) as checkout:
        assert not (checkout / "conftest.py").exists()
        proc = _child_pytest(checkout, security_check.RELEASE_GATE_VALUE)
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert "RELEASE MODE" in proc.stderr
    capsys.readouterr()


def test_detached_checkout_has_a_clean_index_for_the_child_preflight(
        repo, monkeypatch, capsys) -> None:
    """The exact files must also have the index baseline the child governs.

    Removing ``_populate_committed_index`` leaves the manually materialized
    files intact and byte-correct, but the real preflight reports every tracked
    path as deleted because ``worktree add --no-checkout`` starts with an empty
    per-worktree index.
    """
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()

    with security_check._detached_checkout(head) as checkout:
        with monkeypatch.context() as child:
            child.setattr(security_check, "CAIRN_ROOT", checkout)
            rc, observed = security_check.repo_state_preflight()
        assert (rc, observed) == (0, head)
    assert "preflight OK -- clean worktree" in capsys.readouterr().out


def test_detached_checkout_avoids_checkout_filter_execution(
        repo, tmp_path) -> None:
    """The detached checkout is populated from blobs, not through filters.

    A repository-local smudge filter runs during ``git worktree add`` and can
    transform tracked bytes while the index still names the original blob. The
    release checkout uses ``--no-checkout`` plus ``cat-file`` so the candidate
    program never executes and the committed payload is preserved.
    """
    filter_script = tmp_path / "smudge.py"
    marker = tmp_path / "smudge-ran"
    filter_script.write_text(
        "import pathlib, sys\n"
        f"pathlib.Path({str(marker)!r}).write_text('ran')\n"
        "sys.stdout.buffer.write(sys.stdin.buffer.read().replace(b'1', b'9'))\n",
        encoding="utf-8",
    )
    (repo / ".gitattributes").write_text(
        "tracked.py filter=fixture\n", encoding="utf-8")
    _setup_git("add", ".gitattributes", cwd=repo)
    _setup_git("commit", "-q", "-m", "filter attribute", cwd=repo)
    _setup_git("config", "filter.fixture.smudge",
               f"{sys.executable} {filter_script}", cwd=repo)
    _setup_git("config", "filter.fixture.clean", "cat", cwd=repo)
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()

    with security_check._detached_checkout(head) as checkout:
        assert (checkout / "tracked.py").read_text(encoding="utf-8") == "x = 1\n"
    assert not marker.exists(), "candidate-controlled smudge filter executed"


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
        assert env["PYTHONDONTWRITEBYTECODE"] == "1"
        assert env["PYTEST_ADDOPTS"] == "-p no:cacheprovider"
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


def test_check_cairn_fails_closed_when_the_interpreter_cannot_be_spawned(
        monkeypatch, capsys) -> None:
    def _boom(*_a, **_k):
        raise OSError("Exec format error")

    monkeypatch.setattr(security_check.subprocess, "run", _boom)
    assert security_check.run_check_cairn() == 1
    assert "cannot run check_cairn" in capsys.readouterr().err


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
    monkeypatch.setattr(security_check, "repo_state_postflight", lambda _h: 0)

    assert security_check._run_bound_phases("a" * 40) == 1
    assert ran == ["bandit", "cairn", "suite", "qg"]
    err = capsys.readouterr().err
    assert "phase bandit did not pass" in err
    assert "phase release-mode suite did not pass" in err


def test_phase_exception_is_labelled_and_later_phases_and_postflight_run(
        monkeypatch, capsys) -> None:
    ran: list[str] = []

    def _boom():
        ran.append("bandit")
        raise RuntimeError("fixture boom")

    monkeypatch.setattr(security_check, "run_bandit", _boom)
    monkeypatch.setattr(
        security_check, "run_check_cairn",
        lambda: (ran.append("cairn"), 0)[1])
    monkeypatch.setattr(
        security_check, "run_suite", lambda: (ran.append("suite"), 0)[1])
    monkeypatch.setattr(
        security_check, "run_quality_gate", lambda: (ran.append("qg"), 0)[1])
    monkeypatch.setattr(
        security_check, "repo_state_postflight",
        lambda _h: (ran.append("postflight"), 0)[1])

    assert security_check._run_bound_phases("a" * 40) == 1
    assert ran == ["bandit", "cairn", "suite", "qg", "postflight"]
    err = capsys.readouterr().err
    assert "phase bandit raised RuntimeError" in err
    assert "fixture boom" in err


def test_phase_interrupt_is_not_normalized(monkeypatch) -> None:
    monkeypatch.setattr(
        security_check, "run_bandit",
        lambda: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        security_check._run_bound_phases("a" * 40)


def test_main_refuses_when_only_the_postflight_fails(monkeypatch, capsys) -> None:
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (0, "b" * 40))
    monkeypatch.setattr(security_check, "_run_in_detached_checkout",
                        lambda _h: 0)
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
    detached: list[str] = []
    monkeypatch.setattr(security_check, "repo_state_preflight",
                        lambda: (0, head))
    monkeypatch.setattr(security_check, "_run_in_detached_checkout",
                        lambda bound: (detached.append(bound), 0)[1])
    monkeypatch.setattr(security_check, "repo_state_postflight", lambda _h: 0)
    assert security_check.main() == 0
    assert detached == [head]
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
_IMPORTORSKIP_AT_COLLECTION = (
    'import pytest\npytest.importorskip("cairn_missing_release_fixture")\n')
_MODULE_SKIP_AT_COLLECTION = (
    'import pytest\npytest.skip("fixture module skip", '
    'allow_module_level=True)\n')


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


@pytest.mark.parametrize("body", [
    _IMPORTORSKIP_AT_COLLECTION,
    _MODULE_SKIP_AT_COLLECTION,
])
def test_release_mode_refuses_collection_time_skips(tmp_path, body) -> None:
    """CR2: collection reports do not pass through runtest_logreport."""
    root = _fixture_tree(tmp_path, body)
    tests = root / "bootstrap" / "tests"
    (tests / "test_passing_control.py").write_text(
        _CLEAN, encoding="utf-8")
    proc = _child_pytest(root, security_check.RELEASE_GATE_VALUE)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "RELEASE MODE" in proc.stderr
    assert "skipped" in proc.stderr


@pytest.mark.parametrize("body", [
    _IMPORTORSKIP_AT_COLLECTION,
    _MODULE_SKIP_AT_COLLECTION,
])
def test_collection_time_skips_remain_ordinary_without_the_token(
        tmp_path, body) -> None:
    root = _fixture_tree(tmp_path, body)
    tests = root / "bootstrap" / "tests"
    (tests / "test_passing_control.py").write_text(
        _CLEAN, encoding="utf-8")
    proc = _child_pytest(root, None)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RELEASE MODE" not in proc.stderr


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


# ---------------------------------------------------------------------------
# Chunk D5/D6 -- "successfully parsed" must mean VALIDATED, not merely JSON
#
# The five shapes below were reproduced against this module's own bytes at
# 745c927 before the fix: three printed "Bandit clean over 78 shipped file(s)"
# and returned 0; two raised AttributeError -- non-zero, but a traceback where
# a security message was owed. Once D1 emptied the ALLOWLIST, liveness is
# vacuous, so report validation is the only thing between a malformed report
# and release PASS.
# ---------------------------------------------------------------------------

_WELL_FORMED_LOW = {
    "errors": [],
    "results": [{"filename": "scripts/check_cairn.py", "test_id": "B404",
                 "issue_severity": "LOW", "line_number": 1,
                 "issue_text": "subprocess import"}],
}


@pytest.mark.parametrize("stdout,rc,because", [
    ("{}", 0, "required key 'errors' is absent"),
    ('{"errors": [], "results": []}', 1, "contradict"),
    ('{"errors": [], "results": {}}', 0, "not a list"),
    ("[]", 0, "not an object"),
    ("null", 0, "not an object"),
    ('{"errors": [], "results": [{"test_id": "B1"}]}', 1, "missing required"),
    ('{"errors": {}, "results": []}', 0, "not a list"),
    ('{"errors": [], "results": [1]}', 1, "not an object"),
])
def test_a_malformed_report_fails_closed_with_a_message(
        monkeypatch, capsys, stdout, rc, because) -> None:
    class _Proc:
        returncode = rc
        stdout = ""
        stderr = ""

    _Proc.stdout = stdout
    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1
    captured = capsys.readouterr()
    assert "not a usable report" in captured.err
    assert because in captured.err
    assert "Bandit clean" not in captured.out, (
        "the clean line must never print over a report the command could not "
        "validate")


@pytest.mark.parametrize("errors,because", [
    ([1], "errors[0] is int, not an object"),
    ([{}], "errors[0] is missing required field"),
    ([{"filename": None, "reason": "nope"}],
     "errors[0].filename is not a string"),
])
def test_malformed_bandit_error_entries_fail_closed(
        monkeypatch, capsys, errors, because) -> None:
    class _Proc:
        returncode = 0
        stdout = json.dumps({"errors": errors, "results": []})
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "not a usable report" in err
    assert because in err


def test_an_unknown_severity_is_unclassifiable_not_low(monkeypatch,
                                                       capsys) -> None:
    """The fail-open both severity predicates in this repository share: a value
    in neither table reads as "below MEDIUM", so a renamed or added Bandit
    severity would be neither blocking nor liveness-confirming -- silently.
    Validation refuses the report instead."""
    body = json.loads(json.dumps(_WELL_FORMED_LOW))
    body["results"][0]["issue_severity"] = "CRITICAL"

    class _Proc:
        returncode = 1
        stdout = json.dumps(body)
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 1
    err = capsys.readouterr().err
    assert "issue_severity 'CRITICAL'" in err
    assert "unclassifiable evidence" in err


def test_the_known_severity_set_matches_bandits_own_ranking() -> None:
    """Read from the scanner, not from expectation: the closed set is
    ``bandit.core.constants.RANKING``. Skipped rather than asserted-from-memory
    when Bandit is absent -- the module must import without it, which is why the
    set is hard-coded in the first place."""
    bandit_constants = pytest.importorskip("bandit.core.constants")
    assert set(bandit_constants.RANKING) == set(
        security_check._KNOWN_SEVERITIES)


def test_a_well_formed_low_only_report_still_passes(monkeypatch, capsys) -> None:
    """The positive control, without which validation could be satisfied by
    refusing everything. Bandit exits **1** on Cairn's real surface today (125
    LOW findings, measured 2026-08-05), so rc=1 with findings present must
    remain clean -- only rc=1 with *nothing* in the report is a contradiction."""
    class _Proc:
        returncode = 1
        stdout = json.dumps(_WELL_FORMED_LOW)
        stderr = ""

    monkeypatch.setattr(security_check.subprocess, "run",
                        lambda *a, **k: _Proc())
    assert security_check.run_bandit() == 0
    assert "Bandit clean" in capsys.readouterr().out


def test_the_blocking_predicate_and_key_rule_are_single_functions() -> None:
    """D4, release-side half. Suppression and liveness must not be able to
    disagree about what "blocking" and "this finding's allowlist key" mean."""
    high = {"filename": str(CAIRN_ROOT / "scripts/check_cairn.py"),
            "test_id": "B999", "issue_severity": "HIGH"}
    assert security_check.is_blocking(high)
    assert not security_check.is_blocking(dict(high, issue_severity="LOW"))
    assert not security_check.is_blocking(dict(high, issue_severity="UNDEFINED"))
    assert not security_check.is_blocking({})
    assert security_check.finding_key(high) == ("scripts/check_cairn.py", "B999")


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


# ---------------------------------------------------------------------------
# Plan `git-native-security-foundations`, Chunk A: Git owns object ids.
# `_blob_oid` reimplemented Git's blob framing in Python; it is now
# `git hash-object --stdin` against an explicitly-named repository.
# ---------------------------------------------------------------------------


def _init_repo(path: Path, object_format: str) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", f"--object-format={object_format}",
                    "-b", "main", str(path)], check=True, capture_output=True)
    return path


@pytest.mark.parametrize("object_format,width", [("sha1", 40), ("sha256", 64)])
def test_blob_oid_matches_git_in_both_object_formats(tmp_path, object_format, width):
    """The id must come from the repository's format, not a hardcoded choice."""
    repo = _init_repo(tmp_path / object_format, object_format)
    payload = b"contents\n"
    ours = security_check._blob_oid_at(repo, payload)
    assert len(ours) == width
    theirs = subprocess.run(
        ["git", "-C", str(repo), "hash-object", "-t", "blob", "--stdin"],
        input=payload, capture_output=True, check=True).stdout.decode().strip()
    assert ours == theirs


def test_hashing_writes_no_object(tmp_path):
    """No `-w`: the object database must be untouched before and after.

    Perturbation: add `-w` to the argv.  Red -- the loose-object count rises.
    """
    repo = _init_repo(tmp_path / "nowrite", "sha1")
    objects = repo / ".git" / "objects"

    def loose() -> set:
        return {p.relative_to(objects) for p in objects.rglob("*") if p.is_file()}

    before = loose()
    security_check._blob_oid_at(repo, b"never stored\n")
    assert loose() == before


def test_a_non_repository_root_refuses_rather_than_defaulting(tmp_path):
    """The negative control the proposal names.

    Outside a repository, `git hash-object` still happily returns a plausible
    SHA-1.  Falling back to it is the defect; refusing is the contract.
    """
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    with pytest.raises(security_check._RepoStateError) as exc:
        security_check._blob_oid_at(plain, b"payload\n")
    assert "object format" in str(exc.value)


def test_a_missing_root_refuses(tmp_path):
    with pytest.raises(security_check._RepoStateError):
        security_check._blob_oid_at(tmp_path / "absent", b"payload\n")


def test_the_object_format_probe_names_the_repository_it_read(tmp_path):
    repo = _init_repo(tmp_path / "fmt", "sha256")
    assert security_check._repository_object_format(repo) == "sha256"


# ---------------------------------------------------------------------------
# Chunk E: object validation the candidate cannot configure away.
# ---------------------------------------------------------------------------


def _repo_with_malformed_reachable_object(tmp_path: Path) -> Path:
    """A repository whose HEAD is a commit object with no `author` line.

    `hash-object` refuses to write a malformed object without `--literally`;
    an earlier attempt at this fixture silently produced a CLEAN commit and
    every assertion below passed for the wrong reason.
    """
    repo = tmp_path / "candidate"
    repo.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull)

    def git(*args, **kw):
        return subprocess.run(["git", "-C", str(repo), *args], env=env,
                              capture_output=True, check=True, **kw)

    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], env=env,
                   check=True, capture_output=True)
    (repo / "f.txt").write_text("seed\n", encoding="utf-8")
    git("add", "-A")
    git("-c", "user.name=T", "-c", "user.email=t@t.invalid",
        "-c", "commit.gpgsign=false", "commit", "-q", "-m", "seed")
    tree = git("rev-parse", "HEAD^{tree}").stdout.decode().strip()
    parent = git("rev-parse", "HEAD").stdout.decode().strip()
    payload = (f"tree {tree}\nparent {parent}\n"
               f"committer T <t@t.invalid> 1700000000 +0000\n\nmalformed\n")
    bad = subprocess.run(
        ["git", "-C", str(repo), "hash-object", "-t", "commit", "-w",
         "--stdin", "--literally"],
        input=payload.encode(), env=env, capture_output=True,
        check=True).stdout.decode().strip()
    git("update-ref", "refs/heads/main", bad)
    return repo


def test_the_fixture_really_is_malformed(tmp_path):
    """Guard the guard: if this passes plain fsck, every test below is vacuous."""
    repo = _repo_with_malformed_reachable_object(tmp_path)
    proc = subprocess.run(["git", "-C", str(repo), "fsck", "--strict",
                           "--no-dangling"], capture_output=True)
    assert proc.returncode != 0, "fixture is not actually corrupt"


def test_a_candidate_severity_downgrade_cannot_hide_corruption(tmp_path):
    """Negative control 1 of 2: single-valued `fsck.*` downgrade."""
    repo = _repo_with_malformed_reachable_object(tmp_path)
    subprocess.run(["git", "-C", str(repo), "config", "fsck.missingAuthor",
                    "ignore"], check=True, capture_output=True)
    # It really does defeat a plain in-repo check ...
    assert subprocess.run(["git", "-C", str(repo), "fsck", "--strict",
                           "--no-dangling"], capture_output=True).returncode == 0
    # ... and must not defeat ours.
    with pytest.raises(security_check._ObjectIntegrityError):
        security_check._fsck_from_sterile_context(repo)


def test_a_candidate_skiplist_cannot_hide_corruption(tmp_path):
    """Negative control 2 of 2, and the one a `-c` pin cannot answer.

    `fsck.skipList` is multi-valued: `-c fsck.skipList=/dev/null` accumulates
    with the repository's entry instead of replacing it, so the candidate's
    exemption survives every command-line pin. A single negative control would
    pass under a design that defeats only the downgrade above.
    """
    repo = _repo_with_malformed_reachable_object(tmp_path)
    bad = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, check=True).stdout.decode().strip()
    skip = repo / "skip.txt"
    skip.write_text(bad + "\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "config", "fsck.skipList",
                    str(skip)], check=True, capture_output=True)
    assert subprocess.run(["git", "-C", str(repo), "fsck", "--strict",
                           "--no-dangling"], capture_output=True).returncode == 0
    with pytest.raises(security_check._ObjectIntegrityError):
        security_check._fsck_from_sterile_context(repo)


def test_a_sound_repository_passes(tmp_path):
    """The check must be able to succeed, or it proves nothing when it fails."""
    repo = tmp_path / "sound"
    repo.mkdir()
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], env=env,
                   check=True, capture_output=True)
    (repo / "f.txt").write_text("ok\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], env=env, check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=T", "-c",
                    "user.email=t@t.invalid", "-c", "commit.gpgsign=false",
                    "commit", "-q", "-m", "seed"], env=env, check=True,
                   capture_output=True)
    security_check._fsck_from_sterile_context(repo)


def test_integrity_failure_is_typed_apart_from_a_scanner_finding():
    assert issubclass(security_check._ObjectIntegrityError,
                      security_check._RepoStateError)
