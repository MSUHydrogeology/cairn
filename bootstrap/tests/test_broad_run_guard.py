# SPDX-License-Identifier: MIT
"""The broad-run guard: a pytest session spanning too many test files is
refused before any test executes.

**Why file span and not test count.** A scoped run and a broad run are not
distinguishable by how many tests they collect -- one parametrized module can
carry more items than an entire scoped mapping. They are sharply
distinguishable by how many *files* they span, which is why the guard counts
paths.

**Why every test here spawns a real pytest.** The guard's behaviour is a
property of a pytest session -- hook ordering, exit codes, and the interaction
with collection errors. Calling the hook function directly would exercise none
of that. Each test builds a scratch tree carrying a copy of the real conftest
and runs pytest in it, so what is measured is the shipped mechanism.

**Why the child environment is scrubbed rather than inherited.** The guard is
switched off by an environment variable, and these tests very often run inside
a session that has set it -- the order-independence sub-gate sets it for every
child, and an operator running the full suite sets it by hand. A child that
simply inherited the parent's environment would find the guard disabled, and
every refusal assertion here would pass without testing anything. That failure
is silent, which is what makes it worth a paragraph.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parents[2]
CONFTEST = CAIRN_ROOT / "bootstrap" / "tests" / "conftest.py"

#: Kept in step with the conftest by ``test_the_threshold_constant_is_shared``
#: below rather than by hope.
THRESHOLD = 40


def _tree(tmp_path: Path, n_files: int, *, tests_per_file: int = 1,
          broken: bool = False, extra_conftest: str = "") -> Path:
    """A scratch repo of ``n_files`` trivial test files, carrying the real
    conftest.  ``broken=True`` adds one file that fails to parse.
    """
    tests = tmp_path / "bootstrap" / "tests"
    tests.mkdir(parents=True)
    shutil.copy(CONFTEST, tests / "conftest.py")
    if extra_conftest:
        with (tests / "conftest.py").open("a", encoding="utf-8") as fh:
            fh.write("\n\n" + extra_conftest)
    for i in range(n_files):
        body = "".join(
            f"def test_n{i}_{j}():\n    assert True\n\n"
            for j in range(tests_per_file)
        )
        (tests / f"test_probe_{i:03d}.py").write_text(body, encoding="utf-8")
    if broken:
        (tests / "test_probe_broken.py").write_text(
            "def unterminated(\n", encoding="utf-8")
    return tmp_path


def _run(root: Path, *args: str, env_overrides: dict | None = None
         ) -> subprocess.CompletedProcess:
    """Run pytest in ``root`` with both exemption tokens explicitly removed.

    Removal is unconditional and happens before any override is applied, so a
    test asserting a refusal cannot be silently satisfied by an inherited
    token.  See the module docstring.
    """
    env = dict(os.environ)
    env.pop("CAIRN_FULL_SUITE", None)
    env.pop("CAIRN_RELEASE_GATE_ACTIVE", None)
    env.update(env_overrides or {})
    return subprocess.run(
        [sys.executable, "-m", "pytest", "bootstrap/tests", "-q",
         "-p", "no:cacheprovider", *args],
        cwd=str(root), env=env, capture_output=True, text=True, check=False,
    )


def _refused(proc: subprocess.CompletedProcess) -> bool:
    return proc.returncode == 4 and "Refusing a broad run" in (
        proc.stdout + proc.stderr)


# --------------------------------------------------------------------------
# The threshold


def test_a_run_at_or_under_the_file_threshold_is_never_refused(tmp_path) -> None:
    """A scoped run is the normal case and must never pay for this guard --
    including a scoped run that collects a great many tests, which is the case
    a test-count threshold would wrongly catch."""
    proc = _run(_tree(tmp_path, THRESHOLD, tests_per_file=50))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Refusing a broad run" not in proc.stdout + proc.stderr


def test_a_run_over_the_file_threshold_is_refused_regardless_of_selector(
        tmp_path) -> None:
    """Breadth is measured after selectors are applied, so a broad run cannot
    be disguised by adding one."""
    root = _tree(tmp_path, THRESHOLD + 20)
    assert _refused(_run(root)), "bare run"
    assert _refused(_run(root, "-p", "no:randomly")), "with a plugin option"


def test_the_file_threshold_boundary_is_exact(tmp_path) -> None:
    """One file either side of the limit, so an off-by-one cannot pass."""
    under = _run(_tree(tmp_path / "under", THRESHOLD))
    over = _run(_tree(tmp_path / "over", THRESHOLD + 1))
    assert under.returncode == 0, under.stdout + under.stderr
    assert _refused(over)


def test_the_threshold_constant_is_shared_with_the_conftest(tmp_path) -> None:
    """This file's own THRESHOLD is a copy, and a copy that drifts turns every
    boundary assertion above into a test of the wrong number."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_guard_probe", CONFTEST)
    assert spec is not None and spec.loader is not None
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    assert probe.BROAD_RUN_FILE_THRESHOLD == THRESHOLD


# --------------------------------------------------------------------------
# Precedence: real failure evidence outranks a cost prompt


def test_a_pre_existing_collection_failure_keeps_its_own_exit_code(
        tmp_path) -> None:
    """A collection error exits 2 and that is what a machine reads to know
    collection broke.  Overwriting it with the guard's 4 would replace real
    failure evidence with a cost prompt -- and the run is over either way, so
    the prompt buys nothing.

    The clean control matters as much as the broken case: without it, an
    implementation that never refused anything would pass this test.
    """
    broken = _run(_tree(tmp_path / "broken", THRESHOLD + 1, broken=True))
    assert broken.returncode == 2, broken.stdout + broken.stderr
    assert "Refusing a broad run" not in broken.stdout + broken.stderr
    control = _run(_tree(tmp_path / "clean", THRESHOLD + 1))
    assert _refused(control), "the clean control must still refuse"


# --------------------------------------------------------------------------
# Hook placement


def test_the_guard_refusal_follows_a_late_deselection(tmp_path) -> None:
    """The guard must read the item list *after* every other plugin has
    filtered it.

    Directional, deliberately: a late hook removes enough items to drop the
    span below the limit, and the refusal must disappear.  Asserting only that
    a count matches would pass against a guard reading a stale pre-filter list,
    because a modifier that removes nothing leaves the two lists equal -- which
    is the default for a modifier registered only to prove ordering.
    """
    keep = THRESHOLD - 5
    late_hook = (
        "def pytest_collection_modifyitems(config, items):\n"
        "    keep = [i for i in items\n"
        f"            if int(i.nodeid.split('_')[2].split('.')[0]) < {keep}]\n"
        "    items[:] = keep\n"
    )
    root = _tree(tmp_path, THRESHOLD + 20, extra_conftest=late_hook)
    proc = _run(root)
    assert proc.returncode == 0, (
        "a late deselection dropped the span under the limit, so the guard "
        "must not fire:\n" + proc.stdout + proc.stderr)
    assert _refused(_run(_tree(tmp_path / "unfiltered", THRESHOLD + 20)))


# --------------------------------------------------------------------------
# Exemptions


def test_the_override_token_allows_a_full_run(tmp_path) -> None:
    """The deliberate escape hatch: the run proceeds and tests actually
    execute."""
    proc = _run(_tree(tmp_path, THRESHOLD + 20),
                env_overrides={"CAIRN_FULL_SUITE": "1"})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "passed" in proc.stdout


def test_release_mode_is_exempt_from_the_guard(tmp_path) -> None:
    """A release run is a full run by definition and must not be refused."""
    proc = _run(_tree(tmp_path, THRESHOLD + 20),
                env_overrides={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_collect_only_is_exempt_from_the_guard(tmp_path) -> None:
    """Nothing executes under ``--collect-only``, so there is no cost to
    refuse -- and the gate manifest's own collector depends on this."""
    proc = _run(_tree(tmp_path, THRESHOLD + 20), "--collect-only")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_neither_exemption_token_switches_on_by_accident(tmp_path) -> None:
    """Equality, not truthiness.  A stale ``=0`` in a shell is exactly the case
    where an operator believes the guard is on, so it must not exempt."""
    root = _tree(tmp_path, THRESHOLD + 20)
    assert _refused(_run(root, env_overrides={"CAIRN_FULL_SUITE": "0"}))
    assert _refused(
        _run(root, env_overrides={"CAIRN_RELEASE_GATE_ACTIVE": "0"}))
    assert _refused(_run(root, env_overrides={"CAIRN_FULL_SUITE": "true"}))


def test_noconftest_bypasses_the_guard(tmp_path) -> None:
    """``--noconftest`` does not load the conftest, so the guard is not there
    to fire.  Pinned as a fact so prose cannot drift back into claiming the
    guard covers every invocation.

    This is not a supported override.  The same flag also disables the
    release-mode outcome rule this conftest carries; the supported escape
    hatch is the override token.
    """
    proc = _run(_tree(tmp_path, THRESHOLD + 20), "--noconftest")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Refusing a broad run" not in proc.stdout + proc.stderr


# --------------------------------------------------------------------------
# The meta-guard


def test_the_exemption_tokens_do_not_leak_into_these_tests(tmp_path) -> None:
    """The helper above must scrub both tokens, so that a refusal assertion
    cannot be satisfied by inheritance.

    Without this, running the suite under the override -- which is now the
    ordinary way to run it, and what the order-independence sub-gate does for
    every child -- would turn every refusal test in this file green while
    testing nothing at all.
    """
    root = _tree(tmp_path, THRESHOLD + 20)
    poisoned = dict(os.environ)
    poisoned["CAIRN_FULL_SUITE"] = "1"
    poisoned["CAIRN_RELEASE_GATE_ACTIVE"] = "1"
    saved = {k: os.environ.get(k)
             for k in ("CAIRN_FULL_SUITE", "CAIRN_RELEASE_GATE_ACTIVE")}
    try:
        os.environ.update(
            {"CAIRN_FULL_SUITE": "1", "CAIRN_RELEASE_GATE_ACTIVE": "1"})
        assert _refused(_run(root)), (
            "the helper inherited an exemption token from this process")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


# --------------------------------------------------------------------------
# Evidence precedence beyond a collection error


def test_a_pending_session_stop_is_not_replaced_by_the_guard(tmp_path) -> None:
    """``testsfailed`` alone is not proof that collection went cleanly.

    pytest can carry a pending stop disposition with ``testsfailed`` still at
    zero. Measured before the guard consulted it: a collection modifier setting
    ``session.shouldstop`` produced exit 2 at forty files and had it replaced
    by the guard's exit 4 at forty-one -- the guard destroying a failure class
    that already existed.

    Directional: the same tree without the pending stop must still refuse, so
    a guard that simply stopped firing would fail this.
    """
    stopper = (
        "def pytest_collection_modifyitems(config, items):\n"
        "    import os as _os\n"
        "    if _os.environ.get('PROBE_SHOULDSTOP') == '1' and items:\n"
        "        items[0].session.shouldstop = 'STOP_STATE_CANARY'\n"
    )
    root = _tree(tmp_path, THRESHOLD + 5, extra_conftest=stopper)
    stopped = _run(root, env_overrides={"PROBE_SHOULDSTOP": "1"})
    assert stopped.returncode != 4, (
        "a pending session stop was replaced by the guard's exit:\n"
        + stopped.stdout + stopped.stderr)
    assert "Refusing a broad run" not in stopped.stdout + stopped.stderr
    assert _refused(_run(root)), "the control without the stop must still refuse"


def test_a_competing_collection_finish_abort_survives_the_guard(
        tmp_path) -> None:
    """The guard is a hook *wrapper*, so every competing
    ``pytest_collection_finish`` runs to completion before it decides.

    A plain hook cannot achieve this -- it competes for ordering, so a
    competing implementation that aborts the session either runs after the
    guard and never executes, or runs before it and is overwritten. Measured
    before the wrapper existed: a competing ``trylast`` hook calling
    ``pytest.exit(..., returncode=7)`` never ran and its diagnostic vanished
    behind exit 4.

    Asserting the diagnostic survives, not only the exit code: losing the
    message is the half a reader actually needs.
    """
    aborter = (
        "@pytest.hookimpl(trylast=True)\n"
        "def pytest_collection_finish(session):\n"
        "    pytest.exit('COMPETING_ABORT_CANARY', returncode=7)\n"
    )
    root = _tree(tmp_path, THRESHOLD + 5, extra_conftest=aborter)
    proc = _run(root)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "COMPETING_ABORT_CANARY" in proc.stdout + proc.stderr
    assert "Refusing a broad run" not in proc.stdout + proc.stderr
