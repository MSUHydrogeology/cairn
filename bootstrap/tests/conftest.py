"""Pytest conftest for Cairn's bootstrap test suite.

Carries two mechanisms, both stdlib-only and both inert unless
explicitly activated: the **order-independence shuffle hook** and the
**release-mode outcome rule**.

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

import os
import random
import sys

import pytest

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


def pytest_addoption(parser):
    """Register the ``--quality-gate-shuffle-seed`` flag.

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


def pytest_collection_modifyitems(config, items):
    """Shuffle ``items`` in-place when the seed flag is set.

    A deterministic shuffle: the same seed always produces the same
    permutation, so a failing seed is reproducible.  When the seed
    is None (no flag passed), this is a strict no-op.
    """
    seed = config.getoption("--quality-gate-shuffle-seed")
    if seed is None:
        return
    rng = random.Random(seed)
    rng.shuffle(items)


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
    and ``test_the_guard_loses_to_an_outer_tryfirst_wrapper_and_the_plan_says_so``
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
    """The guard proper, reached only after every competing hook succeeded.

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


def pytest_collectreport(report):
    """Record collection-time skips, which never reach runtest_logreport.

    Module-level ``pytest.importorskip`` and ``pytest.skip(...,
    allow_module_level=True)`` produce collection reports. They are incomplete
    release evidence for the same reason as a runtime skip.
    """
    _record_refused_report(report)


def pytest_sessionfinish(session, exitstatus):
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
