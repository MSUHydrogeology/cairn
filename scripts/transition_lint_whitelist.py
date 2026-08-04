"""Commit-SHA suppression whitelist for ``scripts/transition_lint.py``.

**This is a fail-open side-door by construction**, so it gets the
treatment a side-door needs: every entry carries a mandatory written
rationale, a stale entry trips the suite, and an entry that has become
redundant is **deleted rather than left as a latch**.

A ``dict`` rather than the ``frozenset`` used by
``scripts/quality_gate_unused_def_whitelist.py``, precisely because that
file's structure makes the rationale optional -- it carries reasons as
free-floating comments, which no scanner can check.  Here the rationale
*is* the value, so ``test_every_whitelist_entry_has_a_nonempty_rationale``
can assert it.

**Adding an entry.**  An entry needs a written reason **and** a paired
follow-up on the heuristic that produced the finding.  Entries
accumulating past a handful is the signal to **retire the tool** to a
manual checklist item, not to grow the list.

**It ships populated, and that reverses the original proposal's "ships
empty ... the acid test".**  Both findings below are on immutable
history and can never be fixed by anyone; leaving them live would make
the one documented invocation a permanent three-line wall from day one --
the "trains people to ignore it" failure arriving immediately.  The acid
test belongs in pytest, where the corpus tier asserts these same findings
with the whitelist **bypassed** (``scan(..., whitelist={})``).
"""
from __future__ import annotations

WHITELIST: dict[str, str] = {
    "17b7e5c6b51fb1ad145921196f930f2a2137504e": (
        "The original incident: a proposal-open commit whose added file "
        "already carried two landed, dated review sections -- two shape-(b) "
        "findings, one per section. A true positive on immutable history "
        "that no future commit can fix. Kept live in pytest by "
        "TestCorpusRegression.test_window_one_reproduces_the_pinned_findings, "
        "which runs with the whitelist bypassed."
    ),
    "f4a8308dedf4055d53d3a6f22867b64e7fbc1740": (
        "'dev/proposals: add Gemini External Review for check_cairn "
        "self-host-compat' adds no body inside any review section -- a true "
        "shape-(a) positive, and the commit whose capital 'Review' is why "
        "the claim matcher is case-insensitive. Immutable history. Kept live "
        "in pytest by the same bypassed-whitelist corpus node."
    ),
}
