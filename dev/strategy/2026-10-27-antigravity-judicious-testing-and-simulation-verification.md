# Judicious testing — a smaller, faster Cairn suite and better adopter guidance

**Author**: Antigravity (Strategy); revised by Claude Opus 5.5 at the Maintainer's request, 2026-10-30
**Model**: Gemini 4 Argon (original draft)
**Date**: 2026-10-27
**Status**: revised
**Type**: product-strategy
**Surfaces this would feed**: [`dev/PLANNING.md`](../PLANNING.md) v0.7; [`templates/modules/team-gated/testing-discipline.md`](../../templates/modules/team-gated/testing-discipline.md); [`tools/test_tiers.py`](../../tools/test_tiers.py); [`bootstrap/tests/_gate_manifest.py`](../../bootstrap/tests/_gate_manifest.py); [`tools/gauge.py`](../../tools/gauge.py)

## Conclusion first

Cairn's test suite costs the Maintainer time and money and grows faster than
the code it tests. The main cause is structural: the gate freezes every
existing test file, so an agent fixing a bug writes a new file instead of
adding a row to an existing one. Two deliverables follow, kept separate:

1. **Cairn's own suite.** Narrow the freeze to security and trust tests at
   the forward baseline. Then consolidate, keeping each fault a removed test
   caught covered by a retained test. Hold the certifying run to its budget.
2. **Adopter guidance.** The shipped `testing-discipline` module now teaches
   how to choose tests and how to keep a suite small (landed 2026-10-30).

Both are queued together as one v0.7 item, marked as costing time and money
now.

## The question

The Maintainer raised two concerns (2026-10-27): test volume grows much
faster than product code, and scientists rarely learn test selection while
simulation models run too long for ordinary unit tests. On 2026-10-30 the
Maintainer added that long test runs are among the project's biggest costs.

## Measured

On `0.6-dev`, 2026-10-30:

| | |
|---|---|
| Test files | 132 (`bootstrap/tests/test_*.py`) |
| Test lines | 93,929 (before this revision's one new file) |
| Test functions | 3,606; 5,479 collected tests at `7c910851` |
| Product code (engine, scripts, tools) | 29,852 lines |
| Tests ÷ product | about 3.1× (2.80× on 2026-10-27) |
| Certifying run | 24 min 55 s at `7c910851`, one process, nothing else running |
| Suite budget (`AGENTS.md`) | 10 minutes |
| Added on `0.6-dev` in two days | 7,691 test lines |

By tier (`python tools/test_tiers.py list`, 2026-10-30): security 46 files and
46,777 lines; integration 37 and 13,086; contract 25 and 11,564; workflow 14
and 10,885; unit 10 and 3,170. Half the suite by lines is security and trust
machinery.

## Why it grows

**The freeze rewards new files.** `bootstrap/tests/_gate_manifest.py` hashes
every existing test file; editing one holds the gate until the Maintainer
re-anchors, while a new file passes. Agents therefore add files. The
narrower freeze (security and trust tests only) is built and awaits
installation at the forward baseline (`dev/PLANNING.md`, "Nimbleness 3").

**Each plan and finding gets its own test file.** Upgrade hardening on
`0.6-dev` added refusals case by case, each with tests
(`dev/strategy/2026-10-30-claude-upgrade-growth.md`).

**Wording is pinned.** Many contract tests pin exact shipped sentences. A
sentence change then needs a test change, and the test does not show whether
the rule still means the same thing.

**Nothing asks a test to earn its place.** Until 2026-10-30, no Cairn rule
asked which fault a new test catches that the suite would otherwise miss.

## Selection heuristics, with their limits

These guide choices; none is a law.

- **Regimes and boundaries.** Test each class of input that should behave
  alike once, plus the transitions. Extra examples inside a regime rarely
  find new faults, but keep them where a regime is poorly understood.
- **Properties over snapshots.** Conservation, symmetry and round trips
  outlive refactors; golden outputs fail on harmless changes.
- **Promises over wording.** Test what a rule requires, not its sentence.
  Path and link checks cannot replace an assertion about a rule's meaning,
  so prose tests shrink but do not vanish.
- **One new fault per new test.** A test that catches nothing the suite
  misses adds cost without detection.
- **Small domains for simulations.** A few cells and steps exercise the
  real equations quickly and catch many sign and balance errors, but not
  those that need scale, long accumulation or parallel execution, so larger
  benchmarks and milestone runs remain.

## Tiers and cost are separate

The module's tiers describe scope and come from location; Cairn now places
each file by a per-tier configuration (`tools/test_tiers.json`), checked by
`bootstrap/tests/contract/test_test_tiers.py`. The check covers every file pytest
would collect, in subfolders and under either naming form, so the planned
move into tier folders cannot hide a test. Runtime is a separate property: a
workflow test can be fast and a security test slow. Timing budgets are the
project's choice and are measured, not assigned by tier.

The tier map does not yet speed up work. Every tier but unit spans more
than the broad-run guard's 40-file limit, so a tier cannot be run alone
outside a certifying run. Moving files into tier folders, or teaching the
guard about tiers, touches frozen test machinery and belongs with the
forward-baseline ceremony.

## Verification is not validation

Conservation and convergence checks show the code solves its equations.
Whether the equations fit a scientific use needs evidence against
observations, through the proposal template's Independent scientific check.

## Options

1. **Do nothing.** The suite keeps growing and the certifying run stays
   above twice its budget.
2. **Run tests faster only** (a parallel runner). It hides the cost and
   adds a dev-only dependency without changing what is written.
3. **Remove the incentive, then consolidate, then speed up** (recommended).

## Recommendation

**Landed 2026-10-30 (`8f514e05`):** the tier map and its check, and the
module's testing strategy.

**v0.7, priority (one board item):**

1. At the forward-baseline ceremony, install the narrowed freeze and move
   ordinary tests into tier folders, so one Maintainer ceremony covers both.
2. A consolidation proposal for Cairn's suite. For each removed test, name
   the fault it caught and the retained test that still catches it; mutation
   evidence where a claim names a set. The test-to-product ratio is a
   diagnostic, not a deletion target.
3. Hold the certifying run to its 10-minute budget, measured at each run.
   Consider a parallel runner only after consolidation.
4. Add test-growth figures to `tools/gauge.py --pulse` for the Maintainer.

## Signals this is wrong

Consolidation lets a regression through that a removed test would have
caught; small-domain checks miss defects that larger runs find; the suite
regrows within a release after the freeze narrows.

## Key references

Bibliographic records verified against Crossref on 2026-10-27; full texts
not read.

- Goodenough & Gerhart (1975), test data selection, doi:10.1109/TSE.1975.6312836
- Rothermel et al. (1998), minimization and fault detection, doi:10.1109/ICSM.1998.738487
- Kurtz et al. (2014), mutant subsumption, doi:10.1109/ICSTW.2014.20
- Chen et al. (2018), metamorphic testing, doi:10.1145/3143561
- Oberkampf & Roy (2010), *Verification and Validation in Scientific Computing*, doi:10.1017/CBO9780511760396
