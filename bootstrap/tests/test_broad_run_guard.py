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
          broken: bool = False, extra_conftest: str = "",
          competitor: str = "") -> Path:
    """A scratch repo of ``n_files`` trivial test files, carrying the real
    conftest.  ``broken=True`` adds one file that fails to parse.
    """
    tests = tmp_path / "bootstrap" / "tests"
    tests.mkdir(parents=True)
    shutil.copy(CONFTEST, tests / "conftest.py")
    if extra_conftest:
        # Appended to the SAME module, so this may only add hooks the real
        # conftest does not define.  Anything sharing a name with a real hook
        # rebinds it and DELETES the guard -- see `competitor=` below, and
        # `test_the_append_helper_cannot_be_used_to_forge_a_competitor`.
        with (tests / "conftest.py").open("a", encoding="utf-8") as fh:
            fh.write("\n\n" + extra_conftest)
    if competitor:
        # A genuine second plugin: its own module, loaded with -p, so both its
        # hook and the guard's are registered and pluggy really orders them.
        (tmp_path / "competitor_plugin.py").write_text(
            "import pytest\n\n" + competitor, encoding="utf-8")
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
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    plugin = ["-p", "competitor_plugin"] if (root / "competitor_plugin.py").exists() else []
    return subprocess.run(
        [sys.executable, "-m", "pytest", "bootstrap/tests", "-q",
         "-p", "no:cacheprovider", *plugin, *args],
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
    root = _tree(tmp_path, THRESHOLD + 20, competitor=late_hook)
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
    root = _tree(tmp_path, THRESHOLD + 5, competitor=stopper)
    stopped = _run(root, env_overrides={"PROBE_SHOULDSTOP": "1"})
    assert stopped.returncode != 4, (
        "a pending session stop was replaced by the guard's exit:\n"
        + stopped.stdout + stopped.stderr)
    assert "Refusing a broad run" not in stopped.stdout + stopped.stderr
    assert _refused(_run(root)), "the control without the stop must still refuse"


def test_a_competing_collection_finish_abort_survives_the_guard(
        tmp_path) -> None:
    """A competing plugin that aborts the session must keep its exit code and
    its diagnostic; the guard must not pre-empt it.

    **The competitor is a separate plugin module, loaded with ``-p``, and that
    is the whole point of this test.** An earlier version built the competitor
    by appending a second ``def pytest_collection_finish`` to the *same*
    conftest. Python rebinds the name, which DELETES the guard -- so that
    version ran against a tree with no guard at all and passed against the
    pre-fix code it was written to pin. A test that cannot fail is worse than
    no test, because it reports safety it never measured.
    """
    aborter = (
        "@pytest.hookimpl(trylast=True)\n"
        "def pytest_collection_finish(session):\n"
        "    pytest.exit('COMPETING_ABORT_CANARY', returncode=7)\n"
    )
    root = _tree(tmp_path, THRESHOLD + 5, competitor=aborter)
    proc = _run(root)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "COMPETING_ABORT_CANARY" in proc.stdout + proc.stderr
    assert "Refusing a broad run" not in proc.stdout + proc.stderr
    assert _refused(_run(_tree(tmp_path / "control", THRESHOLD + 5))), (
        "the control without a competitor must still refuse")


def test_shadowing_an_owned_hook_is_refused_by_name(tmp_path) -> None:
    """A same-named ``def`` appended to the conftest used to delete the original
    silently. It is now refused, loudly, naming the hook.

    Measured before the ownership guard existed: appending a benign
    ``pytest_sessionfinish`` removed the **release-mode outcome rule**, so a
    release run that skipped a security gate went from exit 1 to exit 0 and
    reported itself clean. The same append removed the broad-run guard. Nothing
    was missing afterwards -- a function of the right name was present and did
    something reasonable, which is what made it silent.

    Directional: the same tree without the shadowing append runs normally.
    """
    shadow = ("def pytest_collection_modifyitems(config, items):\n"
              "    pass\n")
    shadowed = _run(_tree(tmp_path / "shadow", 3, extra_conftest=shadow))
    assert shadowed.returncode == 4, shadowed.stdout + shadowed.stderr
    combined = shadowed.stdout + shadowed.stderr
    assert "have been replaced by a later definition" in combined
    assert "pytest_collection_modifyitems" in combined
    assert _run(_tree(tmp_path / "control", 3)).returncode == 0


def test_the_guard_loses_to_an_outer_tryfirst_wrapper_and_the_plan_says_so(
        tmp_path) -> None:
    """A known, measured limit, pinned rather than left to be rediscovered.

    Pluggy unwinds nested wrappers in the opposite order from entry, so a
    competing ``wrapper=True, tryfirst=True`` implementation is *outside* this
    guard and does its post-``yield`` work after the guard has already raised.
    Competing default and ``trylast`` wrappers are beaten by the guard's
    placement and keep their exit code; a ``tryfirst`` wrapper does not.

    This asserts the limit as it actually is. If someone closes the gap, this
    test goes red -- which is the correct signal to update the documented limit
    rather than a regression.
    """
    body = (
        "@pytest.hookimpl(wrapper=True, tryfirst=True)\n"
        "def pytest_collection_finish(session):\n"
        "    result = yield\n"
        "    pytest.exit('OUTER_WRAPPER_CANARY', returncode=7)\n"
        "    return result\n"
    )
    proc = _run(_tree(tmp_path, THRESHOLD + 5, competitor=body))
    assert proc.returncode == 4, (
        "the documented limit is that an outer tryfirst wrapper LOSES to the "
        "guard; this now returns "
        f"{proc.returncode}:\n" + proc.stdout + proc.stderr)
    assert "OUTER_WRAPPER_CANARY" not in proc.stdout + proc.stderr


def test_a_release_refused_outcome_is_not_masked_by_the_guard(tmp_path) -> None:
    """The two mechanisms in this conftest must not shadow each other.

    The release-mode outcome rule makes a session non-zero when a test skipped
    while the release token was set -- a skip is not acceptable release
    evidence. The guard exempts release mode, so it never fires there and
    cannot overwrite that refusal. This pins the intersection rather than
    trusting it: the guard's exemption is what makes the release refusal
    reachable at all, and someone narrowing that exemption later would silence
    a release control while every other test here still passed.

    Directional in both halves: the same tree without the release token is
    refused by the guard (exit 4), and with it the release rule's own non-zero
    outcome survives instead.

    Housed here rather than in ``test_security_check.py`` where the plan's row
    mapping put it. The property under test is the guard's interaction with the
    release rule, and both live in this file's subject conftest; the security
    file's fixture family builds a full quality-gate tree, which this needs
    none of. A deviation from the mapping, declared rather than silent.
    """
    root = _tree(tmp_path, THRESHOLD + 5)
    skipper = root / "bootstrap" / "tests" / "test_probe_skips.py"
    skipper.write_text(
        "import pytest\n\n"
        "def test_it_skips():\n"
        "    pytest.skip('release evidence must not include a skip')\n",
        encoding="utf-8")
    without = _run(root)
    assert _refused(without), (
        "without the release token this is an ordinary broad run and the "
        "guard must refuse it")
    with_release = _run(root, env_overrides={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert with_release.returncode != 0, (
        "a skip under release mode must make the session non-zero:\n"
        + with_release.stdout + with_release.stderr)
    assert "Refusing a broad run" not in (
        with_release.stdout + with_release.stderr), (
        "the guard fired in release mode and may have masked the release rule")
