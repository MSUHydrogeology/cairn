"""Pytest conftest for Cairn's bootstrap test suite.

Carries several mechanisms, all stdlib-only and all inert unless explicitly
activated: the **order-independence shuffle hook**, the **release-mode outcome
rule**, the **broad-run guard**, and the **suite-cost ledger** (documented at
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
            "module. A same-named `def` appended to this file rebinds the "
            "name and deletes the original -- including the release-mode "
            "outcome rule and the broad-run guard. Extend the existing hook "
            "-- an unrecognised `pytest_*` name is refused by pytest itself."
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


@_own
def pytest_runtest_logreport(report):
    """Record release-refused test outcomes as they actually happen.

    Reading the report rather than the marker is the whole point: ``skipped``
    with a ``wasxfail`` attribute is an *xfail*, ``passed`` with one is an
    *xpass*, and ``skipped`` without one is a real skip -- in any phase
    (a ``skipif`` fires in setup, a ``pytest.skip()`` call in the test body).
    An inactive marker produces none of these and is invisible here, which is
    what makes this an outcome rule.

    Release evidence is recorded **first** and the ledger accumulation last, so
    an ordering failure inside the diagnostics cannot cost the release rule its
    record.  Ordering is defence in depth, not the guarantee -- the guarantee is
    that ``_ledger_step`` swallows everything.
    """
    _record_refused_report(report)
    _ledger_step(_ledger_accumulate_report, report)


@_own
def pytest_collectreport(report):
    """Record collection-time skips, which never reach runtest_logreport.

    Module-level ``pytest.importorskip`` and ``pytest.skip(...,
    allow_module_level=True)`` produce collection reports. They are incomplete
    release evidence for the same reason as a runtime skip.
    """
    _record_refused_report(report)
    _ledger_step(_ledger_accumulate_collect, report)


@_own
def pytest_configure(config):
    """Claim the ledger's ownership marker for this session, if it is free.

    A session that finds the marker already set is running *inside* one that is
    already recording, so it records nothing and releases nothing.  See
    ``_ledger_begin_session``.
    """
    _ledger_step(_ledger_begin_session, config)


@_own
def pytest_deselected(items):
    """Count deselected items for the ledger's node accounting.

    Deselection is invisible to the report hooks -- a deselected node emits no
    runtest report at all -- so without this the difference between "collected
    and skipped" and "never selected" would be unrecoverable from a row.
    """
    _ledger_step(_ledger_accumulate_deselected, items)


@_own
def pytest_sessionfinish(session, exitstatus):
    """Run the release-mode outcome rule, then append the ledger row.

    Two independent mechanisms share this hook, and the order is deliberate:
    the release rule -- which can change the session's exit status -- runs to
    completion first, and the ledger, which may never change it, runs last
    inside ``_ledger_step``.
    """
    _release_mode_outcome_rule(session, exitstatus)
    _ledger_step(_ledger_finish_session, session, exitstatus)


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


# --- The suite-cost ledger ----------------------------------------------------
#
# One JSONL row per top-level pytest session, appended to a gitignored ledger
# that ``tools/suite_cost.py`` renders for a human.  The suite's cost had been
# re-measured by hand repeatedly and lost every time, because the number -- not
# the place to look it up -- was what survived.  This writes it down.
#
# Everything below fails toward silence.  A diagnostics hook that can fail a
# suite is worse than no diagnostics at all: it teaches an operator to switch
# diagnostics off, and then there is no measurement *and* no trust.  So every
# ledger path is wrapped, none reads or writes ``session.exitstatus``, and every
# unrecognized state produces no row rather than a wrong one.

#: Operator opt-out and its **one** recognized value.  Equality, not
#: truthiness, matching the two tokens above -- a guard keyed on truthiness
#: switches off on a stale ``=0`` left in a shell, which is precisely when the
#: operator believes it is on.  The direction is stated because it inverts:
#: unset means *record*, and only the exact string ``0`` means *do not*.
SUITE_LEDGER_ENV = "CAIRN_SUITE_LEDGER"
SUITE_LEDGER_OFF_VALUE = "0"

#: The ownership marker.  A session that finds this already set is running
#: inside a session that is already recording -- a suite-spawned child, or an
#: in-process ``pytest.main()`` call -- and records nothing.  It is claimed by
#: the session that finds it free, and released only by that same session, so a
#: child can never unset a marker it does not own.
SUITE_LEDGER_SESSION_ENV = "CAIRN_SUITE_LEDGER_SESSION"
SUITE_LEDGER_SESSION_VALUE = "1"

#: Optional operator-supplied label, copied into the row.  This is the *only*
#: way a row is attributable to a piece of work; nothing else in the schema
#: binds a run to a plan, which is why the reader reports frequency per day and
#: never per plan.
SUITE_LEDGER_LABEL_ENV = "CAIRN_SUITE_LEDGER_LABEL"

#: Budget for the final encoded line, excluding the newline.  A row that cannot
#: be made to fit degrades to a skeleton rather than to silence: knowing a
#: session happened and that its detail was lost beats knowing nothing.
LEDGER_ROW_BUDGET = 4096

#: Lock acquisition: retry for this long, at this interval.  Generous for a
#: single open+flock+write+close, and short enough that a wedged holder costs a
#: session its row rather than its wall-clock time.
LEDGER_LOCK_DEADLINE_S = 0.25
LEDGER_LOCK_INTERVAL_S = 0.01

#: Field caps, in bytes of the **sanitized** string.  JSON re-escapes
#: backslashes and quotes, so only the pinned encoding below establishes the
#: 4,096-byte budget; these caps keep any single field from consuming it.
LEDGER_LABEL_BYTES = 128
LEDGER_TOKEN_BYTES = 128
LEDGER_TOKEN_COUNT = 64
LEDGER_INVOCATION_BYTES = 1024
LEDGER_TARGET_BYTES = 160
LEDGER_TARGET_COUNT = 16
LEDGER_PATH_BYTES = 160

#: The seven outcome buckets, in precedence order of resolution (see
#: ``_ledger_outcome``).
LEDGER_OUTCOMES = (
    "passed", "failed", "errors", "skipped", "xfailed", "xpassed", "aborted",
)

#: The closed option family a ``full`` classification may carry.  Anything
#: else -- a plugin option, a future option, ``--ignore`` -- forces ``unknown``,
#: because an option this code has never seen may narrow the run in a way the
#: postconditions cannot detect.
LEDGER_FAMILY_FLAGS = ("-q", "--no-header", "--no-summary")
LEDGER_SHUFFLE_FLAG = "--quality-gate-shuffle-seed"

#: Per-session accumulation.  Module state, reset at ``pytest_configure``, so a
#: sequence of in-process sessions in one interpreter cannot leak into each
#: other.
_LEDGER: dict = {}


def _ledger_reset() -> None:
    _LEDGER.clear()
    _LEDGER.update({
        "enabled": False,
        "owned": False,
        "collector_s": 0.0,
        "finish_t0": None,
        "faults": 0,
        "ts_start": None,
        "mono_start": None,
        "nodes": {},
        "by_file": {},
        "deselected": 0,
        "collection_errors": 0,
    })


_ledger_reset()


def _ledger_step(fn, *args) -> None:
    """Run one ledger step, guarded and timed.  **This is guard 1.**

    ``BaseException``, not ``Exception``: a ``KeyboardInterrupt`` arriving
    inside the lock retry loop would otherwise replace a session's real outcome
    -- exit 1 with a release report -- with an interrupt that had nothing to do
    with the code under test.  Nothing raised in a ledger path may reach pytest,
    so the ledger cannot decide a session's exit status even by accident.

    The elapsed time is charged to ``collector_s`` on every path, including the
    raising one, so the overhead figure a row reports is the overhead the
    session actually paid.
    """
    start = time.perf_counter()
    try:
        fn(*args)
    except BaseException:
        _LEDGER["faults"] = _LEDGER.get("faults", 0) + 1
    finally:
        _LEDGER["collector_s"] = (
            _LEDGER.get("collector_s", 0.0) + (time.perf_counter() - start))


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


def _ledger_repo_root() -> Path:
    return _suite_root().parents[1]


def _ledger_dir() -> Path:
    return _ledger_repo_root() / "dev" / "measurement"


def _ledger_path() -> Path:
    return _ledger_dir() / "suite-runs.jsonl"


def _ledger_rel(path: Path, root: Path) -> str:
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
    return rel or "."


def _ledger_resolve_rel(token, invocation_dir: Path, repo_root: Path) -> str:
    """One invocation positional or ``config.args`` entry, resolved.

    Resolution, not string comparison: the ordinary canonical command passes a
    *relative* path and the order-independence command passes an *absolute
    resolved* one, so no literal token family contains both spellings.
    """
    raw = str(token).split("::", 1)[0]
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = invocation_dir / candidate
    try:
        candidate = candidate.resolve()
    except OSError:                              # pragma: no cover
        pass
    return _ledger_rel(candidate, repo_root)


# --- Guards -------------------------------------------------------------------


def _ledger_opted_out() -> bool:
    return os.environ.get(SUITE_LEDGER_ENV) == SUITE_LEDGER_OFF_VALUE


def _ledger_begin_session(config) -> None:
    """Claim the session, or stand down.  **This is guards 2, 4 and 5.**

    Release mode and the operator opt-out both mean "do not record", and both
    are checked before the marker is claimed: a session that will never write
    must not take ownership of a marker it would then have to release.
    """
    _ledger_reset()
    if _release_mode():
        return
    if _ledger_opted_out():
        return
    if os.environ.get(SUITE_LEDGER_SESSION_ENV) is not None:
        return
    os.environ[SUITE_LEDGER_SESSION_ENV] = SUITE_LEDGER_SESSION_VALUE
    _LEDGER["owned"] = True
    _LEDGER["enabled"] = True
    _LEDGER["ts_start"] = _ledger_now()
    _LEDGER["mono_start"] = time.monotonic()


def _ledger_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --- Accumulation -------------------------------------------------------------


def _ledger_accumulate_report(report) -> None:
    """Fold one runtest report into the per-node record and the per-file cost.

    Durations are accumulated in **seconds as floats** and converted to integer
    milliseconds exactly once, at row-build time.  Converting each report would
    round every sub-millisecond phase to zero, and a file made of a thousand
    fast tests would report a cost of nothing.
    """
    if not _LEDGER.get("enabled"):
        return
    nodeid = getattr(report, "nodeid", "") or ""
    when = getattr(report, "when", None)
    node = _LEDGER["nodes"].setdefault(nodeid, {
        "phases": set(), "errors": False, "failed": False, "xpassed": False,
        "xfailed": False, "skipped": False, "setup_passed": False,
    })
    node["phases"].add(when)
    if getattr(report, "failed", False):
        if when in ("setup", "teardown"):
            node["errors"] = True
        elif when == "call":
            node["failed"] = True
    if hasattr(report, "wasxfail"):
        if getattr(report, "passed", False):
            node["xpassed"] = True
        else:
            node["xfailed"] = True
    if getattr(report, "skipped", False):
        node["skipped"] = True
    if when == "setup" and getattr(report, "passed", False):
        node["setup_passed"] = True
    duration = getattr(report, "duration", None)
    if isinstance(duration, (int, float)) and not isinstance(duration, bool) \
            and math.isfinite(duration) and duration > 0:
        key = nodeid.split("::", 1)[0] or "<unknown>"
        _LEDGER["by_file"][key] = _LEDGER["by_file"].get(key, 0.0) + float(duration)


def _ledger_accumulate_collect(report) -> None:
    """Count collect reports that did not complete cleanly.

    A collection-time **skip** counts here alongside a collection *failure*,
    and the field name understates that on purpose -- the schema is fixed.  A
    module-level ``pytest.skip`` or a failed ``importorskip`` means a file's
    tests were never collected at all, so they appear in no count anywhere else
    in the row: ``collected`` never saw them, so ``not_run`` cannot see them
    either.  This is the only field a reader can re-derive "the collection was
    incomplete" from, and without it a session that silently skipped half the
    suite would classify as having covered it completely.

    A *runtime* skip is a different thing and is deliberately not here: the test
    was collected and reported, the suite did cover it, and treating an ordinary
    optional-dependency skip as incomplete coverage would mean no real session
    ever classified as complete.
    """
    if not _LEDGER.get("enabled"):
        return
    if getattr(report, "failed", False) or getattr(report, "skipped", False):
        _LEDGER["collection_errors"] = _LEDGER.get("collection_errors", 0) + 1


def _ledger_accumulate_deselected(items) -> None:
    if not _LEDGER.get("enabled"):
        return
    _LEDGER["deselected"] = _LEDGER.get("deselected", 0) + len(list(items or ()))


def _ledger_outcome(node) -> str:
    """Resolve one node's several phase reports into one outcome.

    The order is the contract, and each step exists because the step above it
    would otherwise mis-file a real case: a teardown failure on a passing test
    is an *error*, not a pass; an xfail arrives as a ``skipped`` call report
    carrying ``wasxfail``, so it must be claimed before the skip rule; and a
    node whose setup passed but whose call never reported did not pass -- it was
    cut short, which is what ``aborted`` names.
    """
    if node["errors"]:
        return "errors"
    if node["failed"]:
        return "failed"
    if node["xpassed"]:
        return "xpassed"
    if node["xfailed"]:
        return "xfailed"
    if node["skipped"]:
        return "skipped"
    if node["setup_passed"] and "call" not in node["phases"]:
        return "aborted"
    return "passed"


# --- Sanitizing, capping, encoding --------------------------------------------


def _ledger_ascii(text) -> str:
    """Total: every str maps to an ASCII str, including lone surrogates."""
    return str(text).encode("ascii", "backslashreplace").decode("ascii")


def _ledger_cap(text, limit: int) -> tuple[str, bool]:
    """Sanitize to ASCII, **then** cap.  Returns ``(value, was_capped)``.

    Capping the sanitized form is the only order that bounds anything: a
    non-ASCII character can expand to six ASCII bytes, so a cap applied first
    bounds a length nobody will ever see.
    """
    value = _ledger_ascii(text)
    raw = value.encode("ascii")
    if len(raw) <= limit:
        return value, False
    return raw[:limit].decode("ascii"), True


def _ledger_encode(row) -> str:
    """The **pinned** encoding.  Every byte budget here is stated against it.

    ``sort_keys`` and the compact separators make the encoded length a function
    of the content alone, ``ensure_ascii`` keeps a byte budget and a character
    budget the same thing, and ``allow_nan=False`` refuses the JSON extension
    ``json.loads`` in another tool may not accept -- a row nobody can parse is
    not a record.
    """
    return json.dumps(row, ensure_ascii=True, separators=(",", ":"),
                      allow_nan=False, sort_keys=True)


def _ledger_skeleton(row) -> dict:
    """The total fallback: a row that always encodes.

    Every value is coerced to something JSON accepts before the skeleton fields
    are applied, so this cannot itself raise on a row that was unencodable for a
    reason nobody anticipated.  Silence would be the worse failure: a missing
    row is indistinguishable from a session that never ran.
    """
    safe: dict = {}
    for key, value in row.items():
        if value is None or isinstance(value, (bool, int)):
            safe[key] = value
        elif isinstance(value, float):
            safe[key] = value if math.isfinite(value) else None
        elif isinstance(value, str):
            safe[key] = _ledger_cap(value, LEDGER_TARGET_BYTES)[0]
        else:
            safe[key] = None
    safe["label"] = None
    safe["invocation"] = None
    safe["scope_basis"] = None
    safe["scope"] = "unknown"
    safe["by_file"] = {}
    safe["by_file_kept"] = 0
    safe["truncated"] = True
    return safe


def _ledger_fit(row) -> tuple[str, bool]:
    """Encode ``row`` within budget, evicting ``by_file`` as needed.

    Eviction is smallest-duration-first, ties broken by longest path, so what a
    pruned breakdown keeps is the expensive end -- the part a cost reader is
    looking for.  Returns ``(line, skeletonized)``.
    """
    work = dict(row)
    by_file = dict(work.get("by_file") or {})
    while True:
        work["by_file"] = by_file
        work["by_file_kept"] = len(by_file)
        try:
            line = _ledger_encode(work)
        except (ValueError, TypeError):
            return _ledger_encode(_ledger_skeleton(row)), True
        if len(line.encode("ascii")) <= LEDGER_ROW_BUDGET:
            return line, False
        if not by_file:
            return _ledger_encode(_ledger_skeleton(row)), True
        victim = min(by_file.items(), key=lambda kv: (kv[1], -len(kv[0])))[0]
        del by_file[victim]
        work["truncated"] = True


# --- head resolution ----------------------------------------------------------


def _ledger_is_sha(text: str) -> bool:
    return len(text) == 40 and all(c in "0123456789abcdef" for c in text.lower())


def _ledger_head(repo_root: Path):
    """Resolve HEAD by reading git's files directly -- no subprocess.

    Returns a 40-hex string or ``None``.  ``None`` is a *recorded* state, not a
    failure: a row with an unknown commit still carries a timing, and dropping
    the row would silently under-count sessions.
    """
    try:
        dotgit = repo_root / ".git"
        if dotgit.is_file():
            text = dotgit.read_text(encoding="utf-8", errors="replace").strip()
            if not text.startswith("gitdir:"):
                return None
            gitdir = Path(text.split(":", 1)[1].strip())
            if not gitdir.is_absolute():
                gitdir = repo_root / gitdir
            gitdir = gitdir.resolve()
        elif dotgit.is_dir():
            gitdir = dotgit.resolve()
        else:
            return None
        head_file = gitdir / "HEAD"
        if not head_file.is_file():
            return None
        raw = head_file.read_text(encoding="utf-8", errors="replace").strip()
        if _ledger_is_sha(raw):
            return raw
        if not raw.startswith("ref:"):
            return None
        ref = raw.split(":", 1)[1].strip()
        if not ref or ref.startswith("/") or ".." in ref.split("/"):
            return None
        common = gitdir
        commondir_file = gitdir / "commondir"
        if commondir_file.is_file():
            rel = commondir_file.read_text(
                encoding="utf-8", errors="replace").strip()
            candidate = Path(rel)
            if not candidate.is_absolute():
                candidate = gitdir / candidate
            candidate = candidate.resolve()
            # Validated, not trusted: a `commondir` pointing somewhere that is
            # not a git directory is a malformed repository, and a SHA read out
            # of an arbitrary file would be worse than no SHA at all.
            if not (candidate / "HEAD").is_file():
                return None
            common = candidate
        loose = common / ref
        if loose.is_file():
            value = loose.read_text(encoding="utf-8", errors="replace").strip()
            return value if _ledger_is_sha(value) else None
        packed = common / "packed-refs"
        if packed.is_file():
            for line in packed.read_text(
                    encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith(("#", "^")):
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[1].strip() == ref \
                        and _ledger_is_sha(parts[0]):
                    return parts[0]
        return None
    except (OSError, ValueError, UnicodeError):
        return None


# --- Scope classification -----------------------------------------------------


def _ledger_scope(*, invocation_args, invocation_dir, repo_root, suite_root_rel,
                  targets, collect_only, inipath, addopts_set, plugins_set,
                  collected, executed, not_run, deselected, collection_errors,
                  interrupted, truncated) -> str:
    """Classify a session's coverage.  ``full`` requires **both** channels.

    Channel 1 is the raw invocation: every option token must be a member of a
    closed family, and every positional must *resolve* to the suite root.
    Channel 2 is the resolved outcome: the run actually covered that root and
    nothing narrowed it.  Either channel alone is fooled -- an argv that looks
    complete can be narrowed by ``PYTEST_ADDOPTS``, and a postcondition set that
    happens to hold says nothing about an option this code has never seen.

    Under-claiming is cheap here and over-claiming is not: a ``full`` row that
    was not full corrupts every cost figure derived from it, while an
    ``unknown`` row merely costs one data point.
    """
    if truncated:
        # A classification that cannot be re-derived from the row must not be
        # asserted -- the reader's disagreement check is the only audit there
        # is, and it needs the evidence the cap just removed.
        return "unknown"
    if collect_only:
        return "unknown"
    positionals = []
    index = 0
    args = list(invocation_args or ())
    while index < len(args):
        token = str(args[index])
        if token.startswith("-"):
            if token in LEDGER_FAMILY_FLAGS:
                index += 1
                continue
            if token.startswith(LEDGER_SHUFFLE_FLAG + "="):
                if not _ledger_is_int(token.split("=", 1)[1]):
                    return "unknown"
                index += 1
                continue
            if token == LEDGER_SHUFFLE_FLAG:
                if index + 1 >= len(args) or not _ledger_is_int(args[index + 1]):
                    return "unknown"
                index += 2
                continue
            return "unknown"
        positionals.append(token)
        index += 1
    if not positionals:
        return "unknown"
    resolved = [_ledger_resolve_rel(p, invocation_dir, repo_root)
                for p in positionals]
    if resolved == [suite_root_rel] and list(targets) == [suite_root_rel]:
        if (not inipath and not addopts_set and not plugins_set
                and collected > 0 and executed > 0 and not_run == 0
                and deselected == 0 and collection_errors == 0
                and not interrupted):
            return "full"
        return "unknown"
    inside = [suite_root_rel] if suite_root_rel == "." else None
    def _within(value: str) -> bool:
        if inside is not None:
            return True
        return value == suite_root_rel or value.startswith(suite_root_rel + "/")
    if resolved and all(_within(v) for v in resolved) \
            and targets and all(_within(v) for v in targets):
        return "targeted"
    return "unknown"


def _ledger_is_int(text) -> bool:
    try:
        int(str(text))
    except (TypeError, ValueError):
        return False
    return True


# --- Row construction ---------------------------------------------------------


def _ledger_invocation(config) -> tuple[list, bool]:
    params = getattr(config, "invocation_params", None)
    args = list(getattr(params, "args", ()) or ())
    truncated = False
    if len(args) > LEDGER_TOKEN_COUNT:
        args = args[:LEDGER_TOKEN_COUNT]
        truncated = True
    kept: list[str] = []
    total = 0
    for token in args:
        value, capped = _ledger_cap(token, LEDGER_TOKEN_BYTES)
        truncated = truncated or capped
        size = len(value.encode("ascii"))
        if total + size > LEDGER_INVOCATION_BYTES:
            truncated = True
            break
        total += size
        kept.append(value)
    return kept, truncated


def _ledger_targets(config, invocation_dir: Path, repo_root: Path):
    args = list(getattr(config, "args", ()) or ())
    truncated = False
    if len(args) > LEDGER_TARGET_COUNT:
        args = args[:LEDGER_TARGET_COUNT]
        truncated = True
    kept: list[str] = []
    for arg in args:
        value, capped = _ledger_cap(
            _ledger_resolve_rel(arg, invocation_dir, repo_root),
            LEDGER_TARGET_BYTES)
        truncated = truncated or capped
        kept.append(value)
    return kept, truncated


def _ledger_build_row(session, exitstatus) -> dict:
    config = getattr(session, "config", None)
    repo_root = _ledger_repo_root()
    suite_root_rel = _ledger_rel(_suite_root(), repo_root)
    params = getattr(config, "invocation_params", None)
    invocation_dir = Path(str(getattr(params, "dir", os.getcwd()))).resolve()

    truncated = False
    invocation, capped = _ledger_invocation(config)
    truncated = truncated or capped
    targets, capped = _ledger_targets(config, invocation_dir, repo_root)
    truncated = truncated or capped

    raw_label = os.environ.get(SUITE_LEDGER_LABEL_ENV)
    if raw_label is None:
        label = None
    else:
        label, capped = _ledger_cap(raw_label, LEDGER_LABEL_BYTES)
        truncated = truncated or capped

    nodes = _LEDGER.get("nodes", {})
    counts = {name: 0 for name in LEDGER_OUTCOMES}
    for node in nodes.values():
        counts[_ledger_outcome(node)] += 1
    collected = int(getattr(session, "testscollected", 0) or 0)
    executed = len(nodes)
    not_run = collected - executed
    if not_run < 0:
        # Left visible rather than clamped to a plausible-looking zero: the
        # accounting invariant `0 <= executed <= collected` is what a reader
        # checks, and a clamp would hide exactly the breakage it names.
        not_run = 0

    by_file: dict = {}
    for path, seconds in _LEDGER.get("by_file", {}).items():
        key, capped = _ledger_cap(path, LEDGER_PATH_BYTES)
        truncated = truncated or capped
        by_file[key] = by_file.get(key, 0) + int(round(seconds * 1000))

    interrupted = bool(getattr(session, "shouldstop", False)
                       or getattr(session, "shouldfail", False))
    try:
        exit_code = int(exitstatus)
    except (TypeError, ValueError):
        exit_code = None
    if exit_code == 2:
        interrupted = True

    mono_start = _LEDGER.get("mono_start")
    wall_s = None
    if isinstance(mono_start, float):
        wall_s = round(time.monotonic() - mono_start, 6)
    finish_t0 = _LEDGER.get("finish_t0")
    collector_s = _LEDGER.get("collector_s", 0.0)
    if isinstance(finish_t0, float):
        collector_s += time.perf_counter() - finish_t0

    inipath = getattr(config, "inipath", None) is not None
    addopts_set = os.environ.get("PYTEST_ADDOPTS") is not None
    plugins_set = os.environ.get("PYTEST_PLUGINS") is not None
    collect_only = False
    if config is not None:
        try:
            collect_only = bool(config.getoption("--collect-only", default=False))
        except (ValueError, AttributeError):        # pragma: no cover
            collect_only = False

    scope = _ledger_scope(
        invocation_args=getattr(params, "args", ()) or (),
        invocation_dir=invocation_dir, repo_root=repo_root,
        suite_root_rel=suite_root_rel, targets=targets,
        collect_only=collect_only, inipath=inipath, addopts_set=addopts_set,
        plugins_set=plugins_set, collected=collected, executed=executed,
        not_run=not_run, deselected=int(_LEDGER.get("deselected", 0)),
        collection_errors=int(_LEDGER.get("collection_errors", 0)),
        interrupted=interrupted, truncated=truncated,
    )

    row = {
        "ts_start": _LEDGER.get("ts_start"),
        "ts_end": _ledger_now(),
        "wall_s": wall_s,
        "collector_ms": round(collector_s * 1000, 3),
        "head": _ledger_head(repo_root),
        "interpreter": "%s %d.%d.%d" % (
            sys.implementation.name, *sys.version_info[:3]),
        "invocation": invocation,
        "scope": scope,
        "scope_basis": {
            "targets": targets,
            "inipath": inipath,
            # Booleans, never values: an environment variable's *content* is
            # not the project's to publish, and whether it was set is the whole
            # of what the classification depends on.
            "addopts_set": addopts_set,
            "plugins_set": plugins_set,
        },
        "label": label,
        "collected": collected,
        "executed": executed,
        "not_run": not_run,
        "deselected": int(_LEDGER.get("deselected", 0)),
        "collection_errors": int(_LEDGER.get("collection_errors", 0)),
        "exitstatus": exit_code,
        "interrupted": interrupted,
        "truncated": truncated,
        "by_file": by_file,
        "by_file_total": len(by_file),
        "by_file_kept": len(by_file),
    }
    row.update(counts)
    return row


# --- Durability ---------------------------------------------------------------


def _ledger_append(path: Path, line: str,
                   deadline_s: float = LEDGER_LOCK_DEADLINE_S,
                   interval_s: float = LEDGER_LOCK_INTERVAL_S) -> bool:
    """Append one line under an exclusive lock, repairing a partial tail first.

    Returns True if a line was written.  Deadline expiry writes nothing: a
    session that cannot get the lock loses its row, which is why the session
    count a reader reports is a lower bound and says so.

    The tail repair is what keeps one interrupted writer from corrupting the
    *next* row as well -- appended after a fragment, an otherwise valid line
    would be unparseable, so two sessions would be lost instead of one.
    """
    if fcntl is None:                             # pragma: no cover
        return False
    payload = line.encode("ascii") + b"\n"
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        deadline = time.monotonic() + deadline_s
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    return False
                time.sleep(interval_s)
        try:
            if os.lseek(fd, 0, os.SEEK_END) > 0:
                with open(str(path), "rb") as probe:
                    probe.seek(-1, os.SEEK_END)
                    if probe.read(1) != b"\n":
                        os.write(fd, b"\n")
            return os.write(fd, payload) == len(payload)
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _ledger_finish_session(session, exitstatus) -> None:
    """Write this session's row, then release the marker it owns.

    The release sits in a ``finally`` and is conditional on ownership: a child
    session that took the no-op path above must not unset a marker belonging to
    the parent still running around it, or the parent's own children would
    start recording.
    """
    _LEDGER["finish_t0"] = time.perf_counter()
    try:
        if not _LEDGER.get("enabled"):
            return
        if _release_mode():
            return
        if _ledger_opted_out():
            return
        if not _ledger_dir().is_dir():
            return
        line, _skeletonized = _ledger_fit(_ledger_build_row(session, exitstatus))
        _ledger_append(_ledger_path(), line)
    finally:
        if _LEDGER.get("owned") and os.environ.get(
                SUITE_LEDGER_SESSION_ENV) == SUITE_LEDGER_SESSION_VALUE:
            os.environ.pop(SUITE_LEDGER_SESSION_ENV, None)
        _LEDGER["owned"] = False
        _LEDGER["enabled"] = False
