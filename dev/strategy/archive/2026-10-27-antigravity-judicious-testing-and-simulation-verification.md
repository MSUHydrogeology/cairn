# Judicious testing — a smaller, faster Cairn suite and better adopter guidance

**Author**: Antigravity (Strategy); revised by Claude Opus 5.5 at the Maintainer's request, 2026-10-30; updated with the Pareto testing principle and developmental-versus-permanent boundary by Antigravity (Strategy), 2026-11-10
**Model**: Gemini 4 Argon (original draft)
**Date**: 2026-10-27
**Status**: archived
**Type**: product-strategy
**Surfaces this would feed**: [`dev/PLANNING.md`](../../PLANNING.md) v0.7; [`templates/modules/team-gated/testing-discipline.md`](../../../templates/modules/team-gated/testing-discipline.md); [`tools/test_tiers.py`](../../../tools/test_tiers.py); [`bootstrap/tests/_gate_manifest.py`](../../../bootstrap/tests/_gate_manifest.py); [`tools/gauge.py`](../../../tools/gauge.py)

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

## Outside evidence: how the Claude Code team verifies before review -- Claude Sonnet 5.5 -- 2026-11-10

Added at the Maintainer's request. Source: [Anthropic's engineering account of
Claude Code's code review](https://claude.dev/blog/solving-code-review-at-anthropic/)
(Osmani, Lunt and Wang, 2026-10-15; its on-page title is "How the Claude Code
team does code review"). A subagent read the full page on 2026-11-10 and
reported to me; I did not read the page myself. It is one team's account, not a
controlled study.

**What bears on testing.**

- **Evidence before review.** The author agent runs tests, the build and the
  linter and shows the output; a fresh-context subagent then reviews the diff.
  Humans are told to read that evidence, and to ask for a real review if they
  cannot say what the checks would miss. This is Cairn's rule to state checks
  not run, applied at the pull request.
- **Required checks run on every platform**, and a merge queue re-runs them
  against the latest main. That bears on Cairn's own macOS and Windows runs.
- **Incidents and reverts feed an eval set** that scores any change to the
  reviewer. The same idea fits our consolidation: judge a pruned suite by the
  defects that later get through, as well as by what each removed test caught.

**Their numbers, as stated.** From June to September, merged pull requests
more than doubled while the share reverted fell by more than 40 percent. The
post does not say how the revert share was measured, and I did not check
whether Cairn tracks reverts. Treat it as direction only.

**What does not transfer.** The setup assumes agents write most of the code
(the post says about 90 percent) and that merge volume is the pressure. Cairn's
pressure is the suite's own growth and cost. The post names its own gaps: each
layer misses some problems, and there are no circuit breakers that tighten
approval when reverts rise.

**Suggestion, not a decision.** When the consolidation proposal measures
regressions, include a count of defects found after a test was removed, and
name where it comes from. The post is also cited, for the review question, in
[Code review at agent scale](../2026-10-28-codex-review-at-agent-scale.md).

## The Pareto testing principle and developmental versus permanent tests -- Antigravity (Strategy) -- 2026-11-10

**Conclusion first.** Cairn's first two pruning rounds (`2a` suite consolidation and `14` promise-unit testing) did not shrink the suite: collected test cases rose by 21% during v0.7, from 5,913 at `v0.6.1` to 7,165 on 2026-11-10 (`dev/PLANNING.md` item 22). They stalled because they required 100% fault-equivalence proof before deleting any test, while new v0.7 tools committed their developmental tests into the permanent suite. Stopping test bloat without adding new ceremony takes two judgment rules:

1. **The Pareto testing principle (80% risk coverage for 20% of the runtime and maintenance cost).** Keep the 20% of tests that catch 80% or more of real caller-visible failures—public entry workflows, scientific/data invariants and one parameterized check per security/refusal class—and drop the long tail of slow or narrow edge permutations.
2. **Developmental tests are scratch work; permanent tests guard only external promises.** Tests written while building or debugging a change run in scratch space (with their result recorded in the commit or verification record) and are deleted before merge or plan archive. A test enters and stays in `tests/` only when an external caller relies on the promise it checks.

### Why the v0.7 test-reduction plans stalled (measured on `0.7-dev`, 2026-11-10)

- **The 100%-equivalence ratchet blocked removals.** Both `2a` ([`dev/plans/archive/2026-11-04-suite-consolidation.md`](../../plans/archive/2026-11-04-suite-consolidation.md)) and `14` ([`dev/plans/2026-11-08-promise-unit-testing.md`](../../plans/archive/2026-11-08-promise-unit-testing.md)) required proving via old/new behavior mutants (plus a fresh Medium probe and a High Security Review per removal set) that retained tests still catch every mutant a deleted test caught. Because almost every pin or micro-branch test catches *some* mutant, the `test_upgrade.py` pilot shrank only from 159 to 154 cases (-3%), and agents marked 70 test files `KEEP` in a single day because public checks *"overlap only in part; they do not establish whole-node equivalence."*
- **New v0.7 tools kept their developmental scaffolding.** While pruning removed a handful of nodes, new v0.7 internal tools added hundreds of permanent tests for helper functions, byte caps and branch variations (`meter.py` and `gauge.py` added 158 test functions; the new prose-tool test file took 32.4 s of wall time).

### Outside evidence on agentic test bloat and Pareto defect distribution

- **Coding agents over-generate mocks and narrow unit tests (Hora & Robbes, Jan 2026, arXiv:2602.00409).** Across more than 1.2 million commits in 2025 across Python, TypeScript and JavaScript repositories, autonomous coding agents modified tests and added internal mocks at a much higher rate than human developers (36% of agent commits added mocks versus 26% for humans; read from abstract and summary, full text not read). Agents optimize for local prompt completion ("prove my change works") while externalizing the long-term runtime, context-token and maintenance cost onto every future session.
- **Practitioner `AGENTS.md` / `CLAUDE.md` anti-bloat heuristics (2025–2026 engineering accounts).** Software teams running coding agents have converged on explicit judgment rules in repository instructions rather than coverage ratchets:
  - *Same branch is not a new test:* before adding a test that differs from a neighbor only in an input value, confirm the production code actually branches on that difference; if a passthrough field or one uniform guard handles all disallowed values, one test covers it.
  - *Separate verification at the change from permanent regression tests:* as in the Claude Code review workflow above, running a check to verify a diff is distinct from keeping that check in the suite forever.
- **Empirical Pareto distribution of software faults (Boehm & Basili, 2001; Ostrand & Weyuker, 2002).** Across industrial releases, roughly 80% of defects cluster in about 20% of modules and paths (Ostrand & Weyuker, *ISSTA* 2002, measured across 13 releases of an industrial system; abstract/secondary summary read). Spending 80% of suite runtime on internal helpers, Cairn-only reporting scripts, or exhaustive parameter combinations inverts risk-based verification.

### Where anti-bloat changes belong so they do not cause new bloat

Mechanical enforcement (new AST gates, per-test mutation ceremonies, or mandatory removal ledgers) caused the current slowdown. To let the remaining v0.7 plans work in peace, the fix must be **judgment-based, zero-ceremony, and placed in existing surfaces**:

1. **One short paragraph in `dev/agent_collaboration.md` (and `templates/core/dev/agent_collaboration.md`) under `## Verification`:**
   - State the **Pareto testing principle** and **developmental versus permanent** rule directly: permanent tests check only listed external promises through public entry points (aiming for ~80% fault coverage in ~20% of runtime); developmental tests are scratch work deleted before archive; same-branch input variations do not get separate tests; and pruning non-promise, private-helper or over-budget tests requires no per-test mutant-equivalence proof.
2. **One line in `dev/plans/_template.md` (and `templates/core/dev/plans/_template.md`) under `## Verification`:**
   - Ask the plan author to separate **Developmental checks** (scratch probes run during coding and deleted before archive) from **Permanent promise tests** (often *"none — covered by existing public promise test X"*).
3. **Update `templates/modules/team-gated/testing-discipline.md` (and `dev/modules/testing-discipline.md`):**
   - Replace the 100%-mutant-equivalence requirement for test removal (*"Before removing a test, map its caller-visible fault to a retained check with a behavior-mutant comparison..."*) with the Pareto promise filter and the *"same branch is not a new test"* rule.
4. **Unstick active plans (`14` and `15`) immediately by Maintainer direction:**
   - Authorize dropping the per-node Medium/High mutant-equivalence trial in [`dev/plans/2026-11-08-promise-unit-testing.md`](../../plans/archive/2026-11-08-promise-unit-testing.md) and [`dev/plans/2026-11-08-functional-prose-editing.md`](../../plans/archive/2026-11-08-functional-prose-editing.md): if a test calls a private `_name`, pins wording, or duplicates a public promise check on the same branch, delete it directly as long as the component's public `Promises:` list has a passing public-entry check.

## Key references

Bibliographic records verified against Crossref on 2026-10-27 (and arXiv/DOI indexes on 2026-11-10 for the three added entries); full texts not read.

- Goodenough & Gerhart (1975), test data selection, doi:10.1109/TSE.1975.6312836
- Rothermel et al. (1998), minimization and fault detection, doi:10.1109/ICSM.1998.738487
- Boehm & Basili (2001), "Software Defect Reduction Top 10 List" (Pareto 80/20 defect clustering), *Computer*, 34(1), 135–137, doi:10.1109/2.962984
- Ostrand & Weyuker (2002), "The distribution of faults in a large industrial software system", *ISSTA '02*, doi:10.1145/566172.566181
- Kurtz et al. (2014), mutant subsumption, doi:10.1109/ICSTW.2014.20
- Chen et al. (2018), metamorphic testing, doi:10.1145/3143561
- Oberkampf & Roy (2010), *Verification and Validation in Scientific Computing*, doi:10.1017/CBO9780511760396
- Hora & Robbes (2026), "Are Coding Agents Generating Over-Mocked Tests? An Empirical Study", arXiv:2602.00409
