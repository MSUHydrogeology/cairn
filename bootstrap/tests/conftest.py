"""Pytest conftest for Cairn's bootstrap test suite.

Carries several mechanisms, all stdlib-only and all inert unless explicitly
activated: the **order-independence shuffle hook**, the **release-mode outcome
rule** and the **broad-run guard** (documented at
the section that implements it, near the end of this file).

Release mode (``CAIRN_RELEASE_GATE_ACTIVE``)
--------------------------------------------

``bootstrap/security_check.py`` sets this variable, at exactly one
recognized value, on the pytest children whose result it reports as
release evidence.  While it is set, an actual ``skipped`` /
``xfailed`` / ``xpassed`` outcome makes the session **non-zero**: "the
security gate may have skipped on the machine that cut the release" is
not acceptable release evidence, and a suite that exits 0 after a skip
says nothing about the code that did not run.

Three boundaries, each deliberate:

* **Without the token -- including at any other value -- contributor
  behaviour is unchanged.**  A local skip is a feature for someone
  without dev-deps installed; only a release run refuses it.
* It is an **outcome rule, not a marker census**.  An *inactive*
  ``skipif`` marker (condition false, test ran normally) does not fail
  a release for existing.  Counting markers would refuse a release for
  a skip that never happened.
* An **already-failing or interrupted session stays at its own exit
  code**.  Overwriting a ``2`` (interrupted) with a ``1`` would hide
  the more serious outcome behind the less serious one.

When pytest is invoked without ``--quality-gate-shuffle-seed``
(the normal case), the hook is a no-op and tests run in the
default collection order.  When the flag is passed, the hook
deterministically reorders ``items`` using a fresh ``random.Random``
seeded with the int value, so the same seed always produces the
same order.

Repeat-call protection: an invocation can pass multiple
``--quality-gate-shuffle-seed`` values; pytest keeps only the last
one.  That is sufficient for the quality-gate sub-gate's "run once
per seed" contract (the sub-gate spawns a subprocess per seed).
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

try:                                        # POSIX only; Windows is unclaimed.
    import fcntl
except ImportError:                         # pragma: no cover
    fcntl = None                            # type: ignore[assignment]

#: The release-mode token and its **one** recognized value.  Duplicated as
#: literals here rather than imported from ``bootstrap.security_check``: this
#: module is loaded by pytest as a plugin before ``sys.path`` is guaranteed to
#: reach the repository root, and a conftest that fails to import takes the
#: whole suite with it.  The two sides are held together by
#: ``bootstrap/tests/test_security_check.py``
#: (``test_the_conftest_recognizes_the_same_token_pair``), which loads this
#: file and compares both strings -- not by hope.
RELEASE_GATE_ENV = "CAIRN_RELEASE_GATE_ACTIVE"
RELEASE_GATE_VALUE = "1"

#: The broad-run override and its **one** recognized value.  Same
#: equality-not-truthiness rule as the release token above, and for the same
#: reason: a guard that switches off on any non-empty string switches off on a
#: stale ``=0`` left in a shell, which is the one case where the operator
#: believes it is on.
FULL_SUITE_ENV = "CAIRN_FULL_SUITE"
FULL_SUITE_VALUE = "1"

#: A run spanning more than this many distinct test *files* is refused.
#:
#: Files, not test items, because file span is what separates a scoped run from
#: a broad one.  Measured on this repository: a full collection spans ~115 files
#: and ~4,400 items, while the six-file mapping used for scoped work spans 6
#: files and over a thousand items.  File span discriminates by roughly 20x
#: where item count barely discriminates at all -- a single parametrized module
#: can carry more items than an entire scoped mapping.
BROAD_RUN_FILE_THRESHOLD = 40

#: Every hook this module implements, captured at definition time.
#:
#: **Appending a same-named ``def`` to this file rebinds the module attribute
#: and silently REMOVES the original.** That is ordinary Python, and it is a
#: live hazard here because this conftest is a shared surface several plans add
#: hooks to. Measured 2026-08-21 against the shipped file: appending a benign
#: ``pytest_sessionfinish`` took the **release-mode outcome rule** with it, so a
#: release run that skipped a security gate went from refusing (exit 1) to
#: reporting itself clean (exit 0). The same append deleted the broad-run guard,
#: and an equivalent one in a test file made that test pass against code a
#: Security Review had already found defective.
#:
#: Every deletion of that kind is silent by construction: nothing is missing, a
#: function of the right name is present, and it does something reasonable.
_OWNED_HOOKS: dict[str, object] = {}


def _own(fn):
    """Record a hook implementation so that shadowing it becomes detectable.

    **Refuses a second registration of a name already held**, and that refusal
    is the load-bearing half. Without it the decorator disarms the guard it
    exists to arm: a shadowing ``def`` carrying ``@_own`` -- which is exactly
    what an agent copying this file's own convention writes, since ``@_own``
    sits above every hook here -- overwrites the record of the function it just
    deleted, leaving the identity check comparing the shadow against itself.
    Measured: that restores the complete pre-fix hazard, silently, and stays
    silent under the order-independence seed.

    The collision is visible at the second decoration, which is why this needs
    no ordering trick: import order is definition order.
    """
    name = fn.__name__
    if name in _OWNED_HOOKS:
        raise RuntimeError(
            "bootstrap/tests/conftest.py defines " + name + " twice. The "
            "second definition replaces the first and would delete it "
            "silently -- including, depending on the name, the release-mode "
            "outcome rule or the broad-run guard. Extend the existing hook "
            "instead of adding another."
        )
    _OWNED_HOOKS[name] = fn
    return fn


def _refuse_if_a_hook_was_shadowed() -> None:
    """Refuse the session if any hook this module owns has been replaced.

    Checked from inside a hook rather than at module scope on purpose: module
    scope executes top-to-bottom, so a check placed in the file body runs
    *before* an append further down and sees the state it is meant to catch as
    still correct. A hook body runs after the import has completed, which is the
    only moment the final bindings are visible.

    Runs from ``pytest_addhooks``, which is call #1 for a conftest plugin --
    ahead of ``pytest_addoption``. An earlier version ran from ``addoption`` and
    claimed no earlier hook existed; that was false, and it left an append
    shadowing both hooks silent.

    **A known limit, stated rather than left to be rediscovered.** The
    comparison is by object identity (``globals().get(name) is not fn``), so
    it catches every *rebinding* of the module attribute -- a second ``def``,
    a ``functools.wraps`` wrap, a bare reassignment -- because all of those
    make ``globals()[name]`` a different object from the one ``_own`` recorded.
    It does **not** catch a mutation of that *same* object's internals:
    ``pytest_sessionfinish.__code__ = other.__code__`` leaves the name bound
    to the identical object ``_OWNED_HOOKS`` already holds, so the comparison
    finds nothing to report. Measured: this silences the release-mode outcome
    rule as completely as the pre-fix hazard -- exit 0, no ``RELEASE MODE``
    report, no diagnostic anywhere -- on a tree with a real skip present.  An
    explicit ``_OWNED_HOOKS.pop(name)`` ahead of a shadowing ``def`` reaches
    the same result by a different route (the shadow's own identity check
    then compares the registry against itself). Both require code written
    specifically to defeat this check; neither is the accidental shadowing --
    a future contributor copying this file's own ``def``/``@_own`` idiom --
    this guard was built to catch, and neither is closed here.
    """
    shadowed = sorted(
        name for name, fn in _OWNED_HOOKS.items()
        if globals().get(name) is not fn
    )
    if shadowed:
        raise pytest.UsageError(
            "Refusing to run: this conftest's hook(s) "
            + ", ".join(shadowed)
            + " have been replaced by a later definition in the same "
            "module. A same-named `def` -- or any other rebinding, including "
            "a `functools.wraps` wrapper -- appended to this file changes "
            "what pluggy will call, and this check cannot tell a wrap from a "
            "deletion: either way the binding recorded at import time, which "
            "may be the release-mode outcome rule or the broad-run guard, is "
            "no longer what runs. Extend the existing hook -- an "
            "unrecognised `pytest_*` name is refused by pytest itself."
        )


#: ``{outcome: {nodeid, ...}}`` for the current session.  A set, so a node
#: reporting the same refused outcome in more than one phase is one offender.
_REFUSED: dict[str, set[str]] = {}


def _release_mode() -> bool:
    """True only for the exact recognized pair.

    Equality, not truthiness: ``CAIRN_RELEASE_GATE_ACTIVE=0`` must **not**
    activate release mode, and neither must a stray non-empty value left in a
    shell.  A release posture that switches on by accident is one a
    contributor learns to work around.
    """
    return os.environ.get(RELEASE_GATE_ENV) == RELEASE_GATE_VALUE


@_own
def pytest_addhooks(pluginmanager):
    """Earliest hook a plugin receives -- call #1, ahead of ``pytest_addoption``.

    The shadow check runs here rather than in ``pytest_addoption`` so that an
    append shadowing *both* is still caught. Measured hook order for a conftest
    plugin: ``pytest_addhooks`` then ``pytest_addoption``. An earlier review
    recorded that no earlier hook existed; that was false, and the residual it
    described was therefore avoidable rather than necessary.
    """
    _refuse_if_a_hook_was_shadowed()


@_own
def pytest_addoption(parser):
    """Register the ``--quality-gate-shuffle-seed`` flag, and verify this
    module's own hooks have not been shadowed.

    Default ``None`` means "do not shuffle" (the normal pytest
    invocation path).  Any int activates the shuffle.
    """
    parser.addoption(
        "--quality-gate-shuffle-seed",
        action="store",
        default=None,
        type=int,
        help=(
            "If set, shuffle test collection order deterministically "
            "using this integer as the seed.  Stdlib `random.Random`; "
            "no pytest plugin dependency.  Used by "
            "scripts/quality_gate.py --sub order-independence."
        ),
    )


@_own
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Shuffle ``items`` in-place when the seed flag is set.

    A deterministic shuffle: the same seed always produces the same
    permutation, so a failing seed is reproducible.  When the seed
    is None (no flag passed), this is a strict no-op.
    """
    _apply_security_marker(items)
    seed = config.getoption("--quality-gate-shuffle-seed")
    if seed is None:
        return
    rng = random.Random(seed)
    rng.shuffle(items)


def _apply_security_marker(items) -> None:
    """Mark every collected item whose file is a security-family member.

    Applied from the manifest rather than written into each file: the seventeen
    members are gate-frozen, so marking them in place would add seventeen
    entries to the re-anchor ceremony to express a fact about none of them.

    Import failure is deliberately NOT swallowed. Everywhere else this collector
    fails toward silence, because a missing diagnostic costs a measurement. Here
    silence would deselect nothing and the family would run in the per-change
    loop -- the safe direction. But a manifest that cannot be imported is a
    broken security control, and the release ceremony reads the same marker, so
    the failure must be loud where it happens rather than discovered at a
    release.
    """
    family = _security_family()
    for item in items:
        if Path(str(item.fspath)).name in family:
            item.add_marker(pytest.mark.security)


def _security_family():
    """The manifest's membership set, loaded by path.

    By path and not by ``import security_manifest``: this collector runs with
    the repository root on ``sys.path``, not its own directory, so a bare import
    raises ``ModuleNotFoundError`` -- measured, as an ``INTERNALERROR`` during
    collection. Resolving against ``__file__`` makes the load independent of how
    pytest was invoked and of the caller's working directory.
    """
    import importlib.util

    path = Path(__file__).resolve().parent / "security_manifest.py"
    if not path.is_file():
        # Absent means "this is not Cairn's own suite" -- the scratch fixture
        # trees throughout these tests copy conftest.py and nothing beside it.
        # Marking nothing there is the SAFE direction: no member is deselected,
        # so the family runs. Treating absence as an error instead made every
        # subprocess fixture tree fail with an INTERNALERROR, measured.
        #
        # Absent and unreadable are different conditions and are handled
        # differently on purpose. A manifest that EXISTS but cannot be loaded is
        # a broken security control in a tree that is meant to have one, and it
        # raises -- the release ceremony reads this same marker, so that failure
        # has to be loud where it happens rather than found at a release.
        return {}
    spec = importlib.util.spec_from_file_location("_cairn_security_manifest", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SECURITY_FAMILY


def _full_suite_override() -> bool:
    """True when the operator has explicitly allowed a broad run.

    Equality, not truthiness, matching ``_release_mode`` -- see
    ``FULL_SUITE_ENV``.
    """
    return os.environ.get(FULL_SUITE_ENV) == FULL_SUITE_VALUE


def _collected_file_span(session) -> int:
    """How many distinct test files the collected items came from.

    Reads ``item.path`` and falls back to ``item.fspath`` and then to the
    nodeid's pre-``::`` prefix.  An item that yields none of the three is
    counted as its own file rather than dropped: undercounting the span is the
    direction that lets a broad run through, so an unrecognized item shape
    fails toward refusal.
    """
    files = set()
    for i, item in enumerate(session.items):
        path = getattr(item, "path", None) or getattr(item, "fspath", None)
        if path is None:
            nodeid = getattr(item, "nodeid", "") or ""
            path = nodeid.split("::", 1)[0] or f"<unresolved-{i}>"
        files.add(str(path))
    return len(files)


@_own
@pytest.hookimpl(wrapper=True)
def pytest_collection_finish(session):
    """Refuse a broad run nobody asked for.

    Runs at collection-finish, not in ``pytest_collection_modifyitems``:
    ``trylast`` there is a priority among equal-priority implementations, not a
    guarantee of last place, so a competing plugin can leave the guard reading
    a pre-filter item list.

    **A wrapper, and that is the load-bearing part.** The ``yield`` lets every
    ordinary ``pytest_collection_finish`` implementation run to completion
    first, and the guard is evaluated only on the path where all of them
    returned normally.  A plain hook cannot do this: it competes for ordering,
    so a competing implementation that aborts the session -- ``pytest.exit(...,
    returncode=7)``, say -- either runs after this one and never executes, or
    runs before it and is then overwritten.  Measured before this wrapper
    existed: a competing aborting hook at ``trylast`` never ran at all and its
    diagnostic vanished behind exit 4.

    **A known limit, stated because the wrapper does not close it.** Pluggy
    unwinds nested wrappers in the opposite order from entry, so an *outer*
    wrapper does its post-``yield`` work after this one returns.  Measured: a
    competing ``wrapper=True`` at default priority and at ``trylast`` both keep
    their exit code and diagnostic, but a competing ``wrapper=True,
    tryfirst=True`` loses to this guard's exit 4 and its diagnostic never
    appears.  That last shape is an open finding (FSI-SR1), not a closed one,
    and ``test_the_guard_loses_to_an_outer_tryfirst_wrapper``
    pins it as it actually behaves.  An earlier version of this docstring
    claimed the ``yield`` waits for *every* other implementation; it does not,
    and a docstring asserting a property the code lacks is worse than the gap
    it conceals.

    A cost prompt must never overwrite stronger evidence.  The run is over
    either way, so the prompt buys nothing -- and the exit code is the part a
    machine reads.
    """
    result = yield
    _refuse_broad_run_if_warranted(session)
    return result


def _refuse_broad_run_if_warranted(session) -> None:
    """The guard proper, called from ``pytest_collection_finish``'s wrapper
    after its own ``yield`` returns -- not after every competing hook has
    succeeded.  An outer ``wrapper=True, tryfirst=True`` implementation is
    still suspended at its own ``yield`` when this runs and has not succeeded
    yet (FSI-SR1, open); every other competing shape has.

    ``testsfailed`` alone is **not** sufficient evidence that collection went
    cleanly, which is the defect this function exists to close.  pytest carries
    a pending stop or fail disposition on the session that leaves
    ``testsfailed`` at zero: measured, a collection modifier setting
    ``session.shouldstop`` produced exit 2 at forty files and had it replaced
    by the guard's exit 4 at forty-one.  All three are consulted, and any of
    them means real evidence already exists and this guard stays silent.
    """
    if session.testsfailed:
        return
    if getattr(session, "shouldstop", False):
        return
    if getattr(session, "shouldfail", False):
        return
    if _full_suite_override():
        return
    if _release_mode():
        return
    if session.config.getoption("--collect-only", default=False):
        return
    span = _collected_file_span(session)
    if span <= BROAD_RUN_FILE_THRESHOLD:
        return
    raise pytest.UsageError(
        f"Refusing a broad run: this invocation collected {len(session.items)} "
        f"test(s) across {span} files (limit {BROAD_RUN_FILE_THRESHOLD}).\n"
        f"Run the tests your change actually maps to, or set "
        f"{FULL_SUITE_ENV}={FULL_SUITE_VALUE} to allow the full suite "
        f"deliberately.\n"
        f"If you are verifying someone else's work, the run belongs to "
        f"whoever asked for it -- report back rather than running it here."
    )


def _record_refused_report(report) -> None:
    """Record one runtime or collection report when release mode is active."""
    if not _release_mode():
        return
    if hasattr(report, "wasxfail"):
        outcome = "xpassed" if report.passed else "xfailed"
    elif report.skipped:
        outcome = "skipped"
    else:
        return
    _REFUSED.setdefault(outcome, set()).add(report.nodeid)


@_own
def pytest_runtest_logreport(report):
    """Record release-refused test outcomes as they actually happen.

    Reading the report rather than the marker is the whole point: ``skipped``
    with a ``wasxfail`` attribute is an *xfail*, ``passed`` with one is an
    *xpass*, and ``skipped`` without one is a real skip -- in any phase
    (a ``skipif`` fires in setup, a ``pytest.skip()`` call in the test body).
    An inactive marker produces none of these and is invisible here, which is
    what makes this an outcome rule.

    """
    _record_refused_report(report)


@_own
def pytest_collectreport(report):
    """Record collection-time skips, which never reach runtest_logreport.

    Module-level ``pytest.importorskip`` and ``pytest.skip(...,
    allow_module_level=True)`` produce collection reports. They are incomplete
    release evidence for the same reason as a runtime skip.
    """
    _record_refused_report(report)


@_own
def pytest_configure(config):
    """Register the security-family marker.

    Membership itself lives in ``bootstrap/tests/security_manifest.py``; this
    only makes the marker known so ``-m`` selections are not warnings.
    """
    config.addinivalue_line(
        "markers",
        "security: a member of the security test family (see "
        "bootstrap/tests/security_manifest.py). Deselected from the per-change "
        "loop with -m 'not security'; always run by the release ceremony, "
        "which executes the entire suite with skips and xfails failing closed.",
    )




@_own
def pytest_sessionfinish(session, exitstatus):
    """Run the release-mode outcome rule.

    It can change the session's exit status, which is why it owns this hook
    alone: anything sharing it would be running after a decision it cannot see.
    """
    _release_mode_outcome_rule(session, exitstatus)


def _release_mode_outcome_rule(session, exitstatus):
    """Refuse a release session that produced incomplete evidence.

    The report is printed whenever there is one -- an operator repairing a
    failing release run needs to see the skips too, not discover them on the
    next pass. Only the *exit code* is conditional: a session that already
    ended non-zero keeps its own code (see the module docstring).
    """
    if not _release_mode():
        return
    refused = {k: sorted(v) for k, v in _REFUSED.items() if v}
    if not refused:
        return
    total = sum(len(v) for v in refused.values())
    lines = [
        f"RELEASE MODE ({RELEASE_GATE_ENV}={RELEASE_GATE_VALUE}): "
        f"{total} outcome(s) are incomplete release evidence. A suite that "
        f"exits 0 after a skip says nothing about the code that did not run.",
    ]
    for outcome in sorted(refused):
        lines.append(f"  {outcome}:")
        lines.extend(f"    {nodeid}" for nodeid in refused[outcome])
    lines.append(
        "  Install the missing dev dependency, or make the guarded condition "
        "hold, and re-run. Outside release mode these are ordinary skips.")
    print("\n".join(lines), file=sys.stderr)
    if exitstatus == 0:
        session.exitstatus = 1


# --- Paths --------------------------------------------------------------------


def _suite_root() -> Path:
    """The directory containing this collector.

    This is the definition of "the suite root" the ``full`` classification is
    stated against: a session is ``full`` when it covered *its own* suite root
    completely.  Deriving it from ``__file__`` rather than from a constant is
    what lets a throwaway tree carrying a copy of this file exhibit the property
    without any recursion into the real suite.
    """
    return Path(__file__).resolve().parent













# --- Guards -------------------------------------------------------------------








# --- Accumulation -------------------------------------------------------------










# --- Sanitizing, capping, encoding --------------------------------------------












# --- head resolution ----------------------------------------------------------






# --- Scope classification -----------------------------------------------------






# --- Row construction ---------------------------------------------------------








# --- Durability ---------------------------------------------------------------




