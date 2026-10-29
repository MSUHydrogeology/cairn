# Make the next speed change earn its complexity

**Author**: Codex (GPT-6, Strategy)
**Model**: GPT-6
**Date**: 2026-10-29
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: `dev/PLANNING.md` — faster certifying runs and existing-suite maintenance

## The question / felt gap

Use the next already-required certification to identify one worthwhile test-family
optimization. Keep ordinary work on scoped checks. The available evidence justifies
investigating cost; it does not yet select a current bottleneck or justify adding a
parallel runner.

The roadmap records a clean-machine, single-process run at `7c910851`:
5,479 passed in 24 minutes 55 seconds, Python 3.13.13. This exceeds the
10-minute budget in `AGENTS.md`. It is a historical measurement, not a new timing
of the current tree. The test-consolidation row already requires preserved property
and fault-detection evidence rather than a test-line deletion quota.

## Method

Read `AGENTS.md`, the current strategy and proposal templates,
`bootstrap/DEPENDENCY_BUDGET.md`, `dev/PLANNING.md`,
`dev/plans/archive/corpus-tier-cost.md`, and the existing judicious-testing
strategy at `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md`.
Inspect `bootstrap/tests/conftest.py` and search existing timing evidence before
building instrumentation. A standard-library JSON read of
`dev/measurement/suite-runs.jsonl` found 188 records; its last record ends
2026-08-26. Those records include per-file timing but cannot identify today's
slowest family. The local canonical interpreter reports Python 3.13.13.

No suite was run for this exploration. The findings would change if current
per-family timing showed that cost is broadly distributed or dominated by work
whose real subprocesses and elapsed time are the property being tested.

## Findings

1. **Avoid a second measurement run.** The separate v0.6 forward-baseline item
   already requires certification of its clean candidate. The Maintainer can
   authorize recording pytest's duration report during that required run. A person
   must retain the report with its commit, interpreter, command and idle-machine
   conditions; this note installs no automatic collector. The certification
   command and its fixed shuffle seed remain unchanged except for reporting.
2. **A broad cache is an old question.** The archived corpus-cost plan measured
   6,509 git invocations against 1,279 distinct keys in the transition-lint
   corpus tier and implemented a local memo there. Its remaining expensive
   families had little repetition. It explicitly fenced oracle and gate-preflight
   subprocess assertions from memo adoption and identified security timeout
   tests where elapsed time is the assertion. Those results are historical;
   neither repeat that optimization blindly nor treat them as proof about new
   families.
3. **Parallelism has a separate cost.** The dependency budget makes dev-only
   exceptions explicit. A parallel runner also needs evidence about collection,
   fixed shuffling, reporting and shared-state safety. CPU count alone does not
   establish a safe speedup. It is a proposal-sized alternative, not a command
   flag to add during release certification.
4. **The narrower boundary has not removed the installation fence.**
   `dev/PLANNING.md` retains actual forward-baseline installation as separate
   work. Before proposing ordinary-test edits, check the installed signed
   authority and the current protection classification; an archived machinery
   plan does not prove that ordinary tests are unfrozen on this machine.

## Options

* **Do nothing beyond scoped verification.** Cheapest immediately, but leaves
  integration and release certification above the documented budget.
* **One measured family, preserving its promises.** Reuse setup or remove
  duplicate derivation only where the current timing and fault model support it.
  This buys evidence before committing to a suite-wide rewrite.
* **Parallel execution.** Potentially useful if independent families dominate;
  requires its own dev-dependency proposal and compatibility proof.
* **Suite-wide consolidation now.** Could improve maintenance, but file counts
  and line ratios cannot identify equivalent behavioral coverage or predict
  runtime savings. Too wide for the next speed step.

## Recommendation

Keep the next implementation proposal to one measured ordinary family. First
attach duration reporting to the next authorized certification, with no extra
broad run. Rank the current expensive families and inspect the leading ordinary
candidate for repeated setup or duplicate behavioral cases. If no worthwhile
ordinary candidate exists, return that result before proposing a dependency.

A resulting proposal should preserve a written inventory of the selected
family's properties and public entry points, compare the same scoped command
before and after, and challenge the claimed preserved behavior with targeted
faults. Record setup/call/teardown costs as well as elapsed time so moving cost
between phases cannot masquerade as a gain. Keep required real executions real.
Do not promise the whole suite will reach ten minutes from one family change.

This is an investigation recommendation, not authorization to change verification
rules, drop accepted coverage, install dependencies or establish a new baseline.

## Open questions

* Which family dominates the clean current candidate, and how much of its cost
  is avoidable repeated setup?
* Is ordinary-test maintenance enabled by the installed signed authority at
  implementation time?
* If parallelism becomes the better option, which collection, ordering,
  reporting and state-isolation properties must its proposal preserve?

## Fold-up note

No new methodology rule proposed. Apply Cairn's existing scoped-verification,
measurement and dependency-budget rules to its own suite.
