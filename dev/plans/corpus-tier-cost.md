<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: stop the corpus tier re-deriving a constant

**Source proposal**: [`corpus-tier-cost`](../proposals/2026-08-10-claude-corpus-tier-cost.md),
accepted at Revision 2 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10`).
**Status**: open
**Plan review**: required(**Internal**) — decided in the proposal per [E4].
Test infrastructure only: no shipped file, no adopter surface, no doctrine, no
dependency, no ceremony.
**Last update**: 2026-08-10
**Opened**: 2026-08-10

## Scope

Four chunks, all inside `bootstrap/tests/`. The contract is the proposal's
R1–R7; this plan sequences it and nothing else.

**Scope fence.** `test_gate_preflight.py` and `test_oracle.py` are fenced from
memo adoption outright (R5) — the subprocess *is* the assertion there.
`test_security_stack.py`'s two timeout nodes are irreducible by construction:
the elapsed time is the property. Parallelisation (`pytest-xdist`) is a
different mechanism with a dependency-budget cost and is **not** in scope; the
proposal names it in Alternatives and leaves it to the Maintainer.

### Documentation / doctrine surface

**None.** No doctrine, no `AGENTS.md` rule, no shipped template, no adopter
prose, no `CHANGELOG.md` entry — adopters receive none of these files. Routed
per `docs/DOCUMENTATION_PLAN.md`: nothing here is prescription or description,
so nothing leaves the deliberation layer.

## Sequence

```
A  the memo fixture + its own contract tests        [commit pending]
B  attach to the three corpus classes               [commit pending]
C  narrow the span-widening window (severable)      [commit pending]
D  measure and disposition the remaining head       [commit pending]
```

A before B is the only hard ordering: B is the parity measurement and needs the
fixture to exist. C is severable per R4 — if the mechanism argument is
rejected, drop C and keep A/B/D. D depends on nothing and can run in parallel.

### Chunk A — the memo, and the tests that prove its key

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/test_transition_lint.py` | module-scoped memo fixture wrapping exactly one callable (`tl._git`) for exactly one root. **Closed grammar**: only the five verified call families, matched structurally on command, option set and operand shape, with `<sha>` 40 hex, `<rev-range>` two such (each optionally `~1`), `<endpoint>` one. Anything else **raises** — never passed through. **Successful reads only** (`rc != 0` is never cached). **One callable per instance**, taken at construction so callable identity cannot fall out of the key |
| A2 | same | the R2 contract tests, built on **two repository roots returning different bytes for identical argv**: drop `root` → collide, red; drop the `<sha>` operand → collide, red; conflate call families 4 and 5 → collide, red; pass `HEAD~1..HEAD` → raises; force `rc != 0` then succeed → second call re-runs |
| A3 | same | docstring stating the honest contract: a *session-local cache over an unchanged repository and git environment*. Git executable identity, `replace` refs and config are outside `(root, argv)` and assumed stable for the pytest session |

Each A2 node carries a named perturbation, run and observed red, per the file's
existing convention. **Mutate the copy the test loads** — this file is its own
consumer, but the twin-mutation trap has already been hit twice in this
repository, so the perturbation record names the exact file it edited.

### Chunk B — attach, and prove nothing moved

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/test_transition_lint.py` | attach the fixture to `TestWideningIsNotCreating`, `TestWhitelistHygiene`, `TestCorpusRegression`. **No assertion changes** |
| B2 | plan record | the paired run: `(scanned, triggered)` integers and finding sets, fixture attached and detached, one host one session |

### Chunk C — narrow the span-widening window *(severable)*

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_transition_lint.py` | span-widening window `ROOT..SNAPSHOT` → `SELF_HOST..SNAPSHOT` |
| C2 | same | replacement guard is the **path-limited historical predicate**: `git rev-list --count <ROOT_SHA>..<SELF_HOST_SHA> -- dev/proposals dev/plans` returns `0`, literal pinned endpoints and literal trigger-root pathspecs — **not** a path list fed back through `_in_scope` |

Argued on the mechanism, never on cost: the dropped prefix cannot contain a
counterexample because Cairn did not host `dev/` before `SELF_HOST_SHA`.

### Chunk D — measure and disposition the remaining head

| # | File | Change |
|---|------|--------|
| D1 | plan record | for each remaining head file, measure and record **either** a memo disposition **or** a written reason. `test_gate_preflight.py` and `test_oracle.py` are fenced (R5); `test_security_stack.py`'s timeout nodes are irreducible |

**No other optimization is authorized by this plan.** A discovery worth doing
is raised to the Maintainer as a scope question.

## Acceptance criteria

Per R6 — **not seconds**:

1. **Invocation reduction** — the wrapped-call count drops, with the
   distinct-key count reported alongside it.
2. **Byte-identical results** — the three corpus classes produce the same
   integers and the same finding sets, recorded as a paired run.
3. **Every R2 mutant observed red**, each naming the file it mutated.

Wall-clock is reported for context with host and date attached and is **never**
a pass/fail threshold. The 4.66× prototype ratio, the 3.81× paired ratio, the
six-file table and the 56% suite share are dated motivation (`as_of
2026-08-10`), not criteria.

* **Tests**: `bootstrap/tests/test_transition_lint.py` in full.
* **Docs**: **N/A** — see *Documentation / doctrine surface*.
* **Examples / smoke**: `python scripts/check_cairn.py` for this record. No
  scaffold or example-gallery surface is touched.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — the memo returns exactly what an uncached call would.
  *Enforced by* the corpus assertions (exact integers and finding sets) **plus**
  A2's two-root key tests. The corpus assertions alone prove result parity for
  this consumer and **not** key completeness — the proposal's [E1] established
  that by execution, and this plan does not re-claim it.
* **Invariant** — the memo is unreachable from a mutable input. *Enforced by*
  the grammar refusal in A1, with its own node in A2.
* **Failure mode — mis-keyed.** *Closed*: colliding keys return wrong bytes and
  the exact-integer assertions fail.
* **Failure mode — stale across a history rewrite.** *Closed*: pinned SHAs stop
  resolving and `_corpus_available()` already skips the tier rather than
  failing it.
* **Failure mode — memo silently disabled.** *Open, and acceptable*: the suite
  is merely slow again; no assertion weakens.
* **Public-path → test mapping**: the public path is `transition_lint.scan`,
  exercised through its real entry point by
  [`bootstrap/tests/test_transition_lint.py`](../../bootstrap/tests/test_transition_lint.py).
  No new public path; the memo is test-local with no adopter-reachable caller.
* **Known omissions** — Chunk D's dispositions for `test_upgrade.py` and
  `test_upgrade_module_additions.py` are **unmeasured** at plan-open; D
  measures before committing to any figure.

## Verification

* **Boundary A**, per chunk: `python -m pytest
  bootstrap/tests/test_transition_lint.py` plus `scripts/check_cairn.py` for
  record changes.
* **Boundary B**, once, on a clean commit after the final implementation
  commit: `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
  then `python scripts/quality_gate.py --sub neutrality --sub redundancy`,
  under the canonical interpreter, recorded as `## Implementation
  verification`.
* **Boundary C**: one code review over that range.

Known at plan-open, so a later reader does not mistake them for regressions:
`bootstrap/tests/test_ast_attest.py` carries **2 pre-existing failures** that
reproduce at clean HEAD (verified 2026-08-10, `--shared` clone), and
`test_verify_ref.py` showed one full-suite failure that does **not** reproduce
in isolation (67/67). Neither is this plan's, and neither is a reason to hold
its Boundary B — but an unexplained *third* failure is.

<!-- Each plan-review pass is its own dated H2 section appended below:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       **Tier**: Internal
       **Findings**: <none|raised>
-->

## Code review

*Filled in after implementation commits land.* One pass, reviewer not the
implementing agent.

## Lasting-truth migration

*Filled in at archive time.* Every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's quoted
authorization) `defer`.
