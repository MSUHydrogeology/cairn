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
is silent, which is what makes it worth a paragraph. The same scrubbing covers
``CAIRN_SUITE_LEDGER``: this plan's own mandated verification command sets it
to ``0`` (opt the *outer* session out of ledger writes), and a test reading a
*child's* ledger row for its ``scope`` would silently see nothing at all if
that value leaked down.
"""
from __future__ import annotations

import json
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


def _run(root: Path, *args: str, env_overrides: dict | None = None,
         family_clean: bool = False) -> subprocess.CompletedProcess:
    """Run pytest in ``root`` with all three of this conftest's tokens
    explicitly removed from the child's environment before any override is
    applied, so a test asserting a refusal -- or a specific ledger outcome --
    cannot be silently satisfied by something this process inherited.  See the
    module docstring.

    ``family_clean=True`` drops the ``-p no:cacheprovider`` flag every other
    call here carries. The sibling's ledger classifies ``scope`` from the raw
    invocation, and its closed option family
    (``bootstrap/tests/conftest.py::LEDGER_FAMILY_FLAGS``) does not include
    ``-p`` -- so a run carrying it can never classify ``full``, regardless of
    what actually happened. Tests that read the ledger's ``scope`` field need
    the unflagged invocation; every other test here, which never looks at the
    ledger, keeps the flag for cache hygiene.
    """
    env = dict(os.environ)
    env.pop("CAIRN_FULL_SUITE", None)
    env.pop("CAIRN_RELEASE_GATE_ACTIVE", None)
    env.pop("CAIRN_SUITE_LEDGER", None)
    # The nesting marker, and it is not optional. A parent session that is
    # itself recording exports CAIRN_SUITE_LEDGER_SESSION; a child that
    # inherits it classifies itself as nested and writes no row at all. Tests
    # here that read a child's ledger row would then fail with "wrote no
    # ledger row", but only when the parent has the ledger enabled -- which is
    # the canonical Boundary B command and NOT the CAIRN_SUITE_LEDGER=0 form
    # used while iterating. Scrubbed so the two agree.
    env.pop("CAIRN_SUITE_LEDGER_SESSION", None)
    env.update(env_overrides or {})
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    plugin = ["-p", "competitor_plugin"] if (root / "competitor_plugin.py").exists() else []
    cache_flag = [] if family_clean else ["-p", "no:cacheprovider"]
    return subprocess.run(
        [sys.executable, "-m", "pytest", "bootstrap/tests", "-q",
         *cache_flag, *plugin, *args],
        cwd=str(root), env=env, capture_output=True, text=True, check=False,
    )


def _ledger_rows(ledger_path: Path) -> list[dict]:
    """Every decodable JSONL row in ``ledger_path``, in file order."""
    if not ledger_path.is_file():
        return []
    return [json.loads(line) for line in
            ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]


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


def test_the_guard_loses_to_an_outer_tryfirst_wrapper(tmp_path) -> None:
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


def test_a_shadow_carrying_the_ownership_decorator_is_still_refused(
        tmp_path) -> None:
    """The decorator must not disarm the guard it arms.

    ``@_own`` sits above every hook in the conftest, so an agent copying the
    file's own convention writes ``@_own def <existing hook>`` -- and if the
    decorator re-registered silently, that would overwrite the record of the
    function it just deleted, leaving the identity check comparing the shadow
    against itself. Measured before the double-registration refusal existed:
    that restored the complete pre-fix hazard, and stayed silent under the
    order-independence seed.

    Directional: the undecorated shadow is refused too, by the other arm.
    """
    decorated = ("@_own\n"
                 "def pytest_sessionfinish(session, exitstatus):\n"
                 "    pass\n")
    proc = _run(_tree(tmp_path / "decorated", 3, extra_conftest=decorated))
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "twice" in proc.stdout + proc.stderr
    plain = ("def pytest_sessionfinish(session, exitstatus):\n"
             "    pass\n")
    assert _run(_tree(tmp_path / "plain", 3, extra_conftest=plain)).returncode == 4


def test_the_check_runs_before_the_option_hook_it_used_to_live_in(
        tmp_path) -> None:
    """Shadowing ``pytest_addoption`` must not evade the check.

    The check ran from ``pytest_addoption`` until a Security Review measured
    that ``pytest_addhooks`` is call #1 for a conftest plugin. An append
    shadowing both hooks was silent for every invocation that omits the shuffle
    flag -- which is all Boundary A iteration.
    """
    both = ("def pytest_addoption(parser):\n"
            "    pass\n"
            "def pytest_sessionfinish(session, exitstatus):\n"
            "    pass\n")
    proc = _run(_tree(tmp_path, 3, extra_conftest=both))
    assert proc.returncode == 4, proc.stdout + proc.stderr
    combined = proc.stdout + proc.stderr
    assert "pytest_addoption" in combined and "pytest_sessionfinish" in combined


def test_a_code_object_swap_evades_the_ownership_check(tmp_path) -> None:
    """A known, measured limit, pinned rather than left to be rediscovered --
    the same treatment ``test_the_guard_loses_to_an_outer_tryfirst_wrapper``
    gives FSI-SR1's limit.

    The check compares object identity (``globals().get(name) is not fn``),
    which catches every *rebinding* of a hook's name -- a second ``def``, a
    ``functools.wraps`` wrap, a bare reassignment -- because each makes
    ``globals()[name]`` a different object from the one ``_own`` recorded.
    It does not catch a mutation of that *same* object's internals:
    swapping ``__code__`` leaves the name bound to the identical object
    ``_OWNED_HOOKS`` already holds, so the comparison finds nothing to
    report, and the release-mode outcome rule the swapped hook carries goes
    silent with it -- discovered while falsifying this guard for round 3 of
    code review, found round 2's Security Review did not (the disarming
    shape it found and closed was ``@_own`` on the shadow; this one carries
    no ``@_own`` decoration to catch).

    Not the accidental-shadowing threat model this guard was built for (see
    the module docstring): it requires code written specifically to defeat
    the check, the same class as an explicit ``_OWNED_HOOKS.pop(name)``
    ahead of a shadow. Directional: the same tree without the swap reports
    the release evidence normally.
    """
    swap = (
        "def _swap_pytest_sessionfinish():\n"
        "    def _evil(session, exitstatus):\n"
        "        return None\n"
        "    pytest_sessionfinish.__code__ = _evil.__code__\n"
        "_swap_pytest_sessionfinish()\n"
    )
    root = _tree(tmp_path / "swapped", 1, extra_conftest=swap)
    (root / "bootstrap" / "tests" / "test_probe_skips.py").write_text(
        "import pytest\n\n"
        "def test_it_skips():\n"
        "    pytest.skip('release evidence must not include a skip')\n",
        encoding="utf-8")
    proc = _run(root, env_overrides={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert proc.returncode == 0, (
        "the documented limit is that a __code__ swap evades the ownership "
        "check and silences the release-mode outcome rule; this now returns "
        f"{proc.returncode}:\n" + proc.stdout + proc.stderr)
    combined = proc.stdout + proc.stderr
    assert "RELEASE MODE" not in combined
    assert "have been replaced by a later definition" not in combined

    control = _tree(tmp_path / "control", 1)
    (control / "bootstrap" / "tests" / "test_probe_skips.py").write_text(
        "import pytest\n\n"
        "def test_it_skips():\n"
        "    pytest.skip('release evidence must not include a skip')\n",
        encoding="utf-8")
    unswapped = _run(control, env_overrides={"CAIRN_RELEASE_GATE_ACTIVE": "1"})
    assert unswapped.returncode != 0, (
        "the control without the swap must still report the release "
        "evidence:\n" + unswapped.stdout + unswapped.stderr)
    assert "RELEASE MODE" in unswapped.stdout + unswapped.stderr


def test_the_ownership_registry_is_complete(tmp_path) -> None:
    """Every module-level ``pytest_*`` callable in the conftest must carry
    ``@_own``, or a shadow of it evades the identity check entirely -- the
    check only compares names already in ``_OWNED_HOOKS``, so an unregistered
    hook can be replaced with no diagnostic at all.

    Needs no subprocess: imports the conftest directly (the same pattern as
    ``test_the_threshold_constant_is_shared_with_the_conftest``) and compares
    its own ``globals()`` against its own registry.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("_ownership_probe", CONFTEST)
    assert spec is not None and spec.loader is not None
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)

    hook_names = {
        name for name, value in vars(probe).items()
        if name.startswith("pytest_") and callable(value)
    }
    assert hook_names, "found no pytest_* callables -- the probe measured nothing"
    unowned = sorted(hook_names - probe._OWNED_HOOKS.keys())
    assert not unowned, (
        f"{unowned} define a pytest_* hook without @_own -- a later shadow of "
        "that name would replace it with no diagnostic")


# --------------------------------------------------------------------------
# Chunk S -- the sibling seam (dev/plans/full-suite-interception.md, row A6)


def test_a_refused_session_is_scoped_unknown(tmp_path) -> None:
    """A6 -- a regression guard on the sibling's contract, not a change to it.

    The sibling's accepted classifier (``bootstrap/tests/conftest.py``'s
    ``_ledger_scope``, and its read-only twin in ``tools/suite_cost.py``)
    already requires ``collected > 0``, ``executed > 0`` and ``not_run == 0``
    for ``scope == "full"``. A session this guard refuses has ``executed ==
    0`` by construction -- the refusal fires at collection-finish, before any
    test runs. This pins that property against a later relaxation of the
    sibling's contract rather than adding special-case code for a shape the
    general rule already covers; see the plan's Scope > "A second expansion"
    for the full derivation and the Maintainer's disposition ("Sure, I like
    the regression guard idea").

    **Correcting a claim in this plan's own "Sequencing" section, which this
    test's mutation-testing exposed.** That section says a refused session
    "writes a row with `collected` ≈ the full set and `executed` = 0" --
    measured here, `collected` (`session.testscollected`) is **0**, not ≈
    the full set: `Session.perform_collect` (`_pytest/main.py`, pytest 9.0.3)
    only assigns `self.testscollected = len(items)` *after*
    `hook.pytest_collection_finish` returns, and this guard's `UsageError`
    propagates out of that hook before the assignment is reached. So
    `collected > 0` is independently sufficient to keep a refused session out
    of `full` -- removing only `executed > 0` from the classifier's postcondition
    (leaving `collected > 0` and `not_run == 0`) does **not** flip this test's
    first half, confirmed by mutation; removing both `collected > 0` and
    `executed > 0` does (`not_run = collected - executed = 0 - 0 = 0` still
    holds). The assertions below check both fields directly so a reader does
    not have to take either claim on faith.

    Reads the ledger row directly (raw JSONL), not through
    ``tools/suite_cost.py`` -- that reader's own refused-session handling is
    row A7 of the same chunk, unimplemented as of this test (see the code
    review's finding on that row).

    Directional on both halves, per the row mapping: a refused session
    resolves ``unknown``, **and** the same tree under the override resolves
    ``full`` -- a classifier answering ``unknown`` unconditionally would pass
    the first half and fail the second. Both runs use ``family_clean=True``:
    without it, ``-p no:cacheprovider`` alone forces ``unknown`` regardless of
    ``executed``, which would make the second half vacuous (measured -- see
    ``_run``'s own docstring).
    """
    refused_root = _tree(tmp_path / "refused", THRESHOLD + 5)
    refused_ledger_dir = refused_root / "dev" / "measurement"
    refused_ledger_dir.mkdir(parents=True)
    refused_ledger = refused_ledger_dir / "suite-runs.jsonl"

    refused = _run(refused_root, family_clean=True)
    assert _refused(refused), refused.stdout + refused.stderr
    refused_rows = _ledger_rows(refused_ledger)
    assert refused_rows, "the refused session wrote no ledger row at all"
    row = refused_rows[-1]
    assert row["exitstatus"] == 4, row
    assert row["executed"] == 0, row
    assert row["collected"] == 0, row
    assert row["scope"] == "unknown", (
        f"a refused session (executed=0) classified {row['scope']!r}, not "
        "'unknown' -- the sibling's full-classification postconditions no "
        "longer exclude a session that never ran anything")

    full_root = _tree(tmp_path / "full", THRESHOLD + 5)
    full_ledger_dir = full_root / "dev" / "measurement"
    full_ledger_dir.mkdir(parents=True)
    full_ledger = full_ledger_dir / "suite-runs.jsonl"

    full = _run(full_root, env_overrides={"CAIRN_FULL_SUITE": "1"},
                family_clean=True)
    assert full.returncode == 0, full.stdout + full.stderr
    full_rows = _ledger_rows(full_ledger)
    assert full_rows, "the overridden session wrote no ledger row at all"
    full_row = full_rows[-1]
    assert full_row["executed"] == THRESHOLD + 5, full_row
    assert full_row["scope"] == "full", (
        f"the same tree, actually run to completion under the override, "
        f"classified {full_row['scope']!r} -- a classifier that answers "
        "'unknown' unconditionally would still have passed the first half "
        "of this test")
