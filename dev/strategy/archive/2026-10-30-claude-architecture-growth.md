# Architecture growth — make reading old code cheaper than writing new

**Author**: Claude Opus 5.5 (Strategy)
**Date**: 2026-10-30
**Status**: archived
**Type**: product-strategy
**Surfaces this would feed**: [`templates/modules/team-gated/architecture-review.md`](../../../templates/modules/team-gated/architecture-review.md) and its [rubric](../../../templates/modules/team-gated/architecture_review_template.md); [`dev/proposals/_template.md`](../../proposals/_template.md) and [`dev/plans/_template.md`](../../plans/_template.md) reuse answers; [`tools/gauge.py`](../../../tools/gauge.py); `dev/PLANNING.md` v0.7

## Conclusion first

Agents rebuild code instead of finding it because finding it costs more. Every
session starts without a map of the codebase, searching costs tokens and may
fail, and writing new code reliably produces something a test can pass. Code
review sees the diff, where a near-copy is invisible. Cairn's answer so far is
a rule ("search before you build") fighting that price.

Change the price instead. For v0.7, develop the architecture-review module
from a rubric nobody triggers into four working parts:

1. a **capability map**, generated on demand, so reading is cheap;
2. a **neighbors report** that shows reviewers the existing code closest to
   each new function, so duplication is visible;
3. **one home per critical capability**, enforced by a test, for the few
   capabilities where a second copy is a defect;
4. a **routine structure pass** at each release, judged by code removed with
   tests intact.

## The question

The Maintainer (chat, 2026-10-30): code architecture gets out of hand quickly,
and "Agents will build new code because it's cheaper than reading old code."
They want it addressed in v0.7 as part of complexity, and said the
architecture-review module needs more development.

## Measured, 2026-10-30

Method: parse every function in Cairn's non-test Python with the standard
library's `ast`, after setting aside 23 files that are deliberate
byte-identical copies (a shipped file and its self-hosted twin). Strip names
and constant values, then group functions of eight or more lines whose
remaining structure is identical. This finds only exact structural copies, so
it is a lower bound.

| | |
|---|---|
| Files, functions examined | 89 files, 1,016 functions |
| Groups of structurally identical functions | 15 groups, 30 functions, 676 lines |
| Function names defined in more than one file | 47 |

Examples: the GitHub and GitLab label scripts share `main`,
`list_existing_labels` and `load_manifest` (72, 38 and 33 lines);
`api_access_security.py` and `web_hosting_security.py` each carry an identical
`_emit`; `link_check.py` and `sync_doc_snippets.py` each carry
`tracked_markdown`. `build_arg_parser`, `_git`, `refuse` and `_load_engine`
are each defined in four files.

Some of this is deliberate: a script shipped to adopters must run alone, and
the standard-library rule forbids a shared package for adopters. That reason
is legitimate once and becomes a habit afterwards.

## Why agents build instead of read

- **No memory.** A person accumulates a map of a codebase; each agent session
  starts without one. Reuse is decided blind every time.
- **The price is lopsided.** Reading has an upfront, uncertain cost. Writing
  has a certain result, and a new test makes it look finished. Duplication's
  cost lands later, on someone else.
- **Review sees the diff.** The review sweep asks reviewers to rerun the
  plan's reuse search (`dev/agent_collaboration.md`, lens 5), but they must
  find the old code themselves, at the same price.
- **Structure rewards new files.** The gate freezes existing test files, so
  extending one costs a re-anchor while a new file costs nothing
  (`dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md`).
  Code follows its tests.
- **Nothing triggers the architecture review.** The module calls itself "a
  triggered remediation / on-ramp tool, not a standing routine", and ships
  questions only.

## What already works

Where a capability has a named home, it stays single. `_assert_safe_write` is
one containment check called at 50 sites in the engine. `AGENTS.md` names
`encode_display` the single terminal encoder: "there is no second escape
table". Both work because the home is named, not because anyone searched.

## Options

1. **Do nothing.** Duplication and accretion continue; the rubric stays
   unused.
2. **Stronger rules.** More "search first" text. It has the same price
   problem and joins the rules agents skim.
3. **Third-party analyzers** (jscpd for duplication, pydeps for imports, as
   listed in the agent-scale review note). Useful, but each adds a dependency
   Cairn cannot ship to adopters.
4. **Change the price with standard-library tools and named homes**
   (recommended).

## Recommendation for v0.7

**1. Capability map.** A tool lists every module, public function and class
with the first line of its docstring, grouped by folder, generated on demand,
never maintained by hand. A plan's reuse answer cites the map's entries, or
states that the map shows none. Reading the map costs a few thousand tokens
instead of a search.

**2. Neighbors report.** For each function a change adds or alters, the tool
lists the closest existing functions by normalized structure and name, with a
similarity figure. It goes into the plan and the review packet. A reviewer
then judges a visible near-copy instead of hunting for one. Advisory only: a
near-copy may be justified, and the author says why in one line.

**3. One home per critical capability.** A short committed registry names the
capabilities where a second copy is a defect: safe file reading, containment
checks, terminal encoding, running git. A test fails when a registered
capability's signature pattern appears outside its home. Keep the registry
small; it is for primitives whose divergence is a security or correctness
risk, not a style rule.

**4. Routine structure pass.** At each release cut, one agent runs the map,
the neighbors report over the whole tree, and growth figures (modules, public
names, duplication groups, files over the test-time target). It returns a
ranked list of consolidation candidates, each with its expected removal and
the tests that keep it safe. It is judged by net code removed with tests
intact. The figures go to the Maintainer, never into agents' targets.

**5. The module itself.** Keep the five lenses and add a sixth, **accretion
and reuse**. Ship the map and neighbors tools to adopters, standard library
only. Change its stance from "triggered" to "at each release, cheaply". Its
selection rule (architecture that accreted rather than was designed) already
fits most AI-assisted projects.

## How it composes

- **Visual codebase review at agent scale**
  (`dev/strategy/2026-10-28-codex-review-at-agent-scale.md`): that note
  designs views for people. The map feeds its System shape and Capabilities
  views; the neighbors report feeds its Growth and consolidation view. One
  collector, shared with `tools/gauge.py`, as that note asks.
- **The accepted apparatus proposal** made avoidable complexity a review
  finding; the neighbors report supplies the evidence.
- **Testing strategy** (v0.7 priority item): consolidating tests and code
  together keeps them aligned.
- **Metered cost** (accepted): the meter can later show whether map-first
  planning costs fewer tokens than search-first, the direct test of this
  note's premise.

## Signals this is wrong

The map is generated but plans still cite searches; the neighbors report
flags mostly justified copies; the registry grows into a style list;
duplication groups do not fall across two releases; metered planning cost
does not drop.

## Open questions

- Should a near-copy above some similarity require a one-line reason, or stay
  purely advisory? Start advisory, and measure.
- Which capabilities belong in the first registry? Start with the four named
  above.
