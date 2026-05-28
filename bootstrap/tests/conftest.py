"""Pytest conftest for Cairn's bootstrap test suite.

Carries the **order-independence shuffle hook** that
``scripts/quality_gate.py``'s order-independence sub-gate dispatches
to.  Pure stdlib (``random.Random``), so no third-party pytest
plugin is required.

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

import random


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
