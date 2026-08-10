<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: stop the corpus tier re-deriving a constant

**Source proposal**: [`corpus-tier-cost`](../proposals/2026-08-10-claude-corpus-tier-cost.md),
accepted at Revision 2 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10`).
**Status**: awaiting-plan-review
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

## Plan review -- Claude (Internal, fresh-context) -- 2026-08-10

**Tier**: Internal
**Findings**: raised

**Method.** Fresh context, nothing inherited from the authoring session. Read
`AGENTS.md`, this plan, the source proposal in full (both reviews, the
Response, the Revised proposal, the Decision), `dev/plans/_template.md`,
`bootstrap/tests/test_transition_lint.py` and `scripts/transition_lint.py`.
Confirmed `scripts/transition_lint.py` and `bootstrap/tests/test_transition_lint.py`
are byte-identical to HEAD before measuring (`git diff --stat HEAD --` empty).
Canonical interpreter throughout: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the path bound in `dev/.cairn/local-env.json`.

Run, not reasoned:

* **Baseline** — `python -m pytest bootstrap/tests/test_transition_lint.py -q`
  -> `40 passed in 110.99s`, this host, 2026-08-10. (Consistent with the
  Response's 107.75 / 112.34s, not with the review host's 49.79s. Context only.)
* **Real argv census** — loaded the committed module, wrapped `tl._git` with a
  correct `(root, argv)` memo + recorder, executed all eleven corpus methods:
  **6509 wrapped calls, 1279 distinct keys, 1 distinct root, 0 keys with
  `rc != 0`**, 18.46s. The 6509/1279 pair reproduces [E1]'s figure exactly.
* **Key-dimension mutants** — re-ran the same eleven methods with the trailing
  `<path>` operand stripped from the key. Result below ([I2]).
* **Ordering** — collected the real suite (`--collect-only -q`, 2788 items),
  then replayed `random.Random(seed).shuffle(items)` — the exact hook in
  `bootstrap/tests/conftest.py` — for seeds 0-19, and analysed each maximal
  run of consecutive `test_transition_lint.py` items. Result below ([I1]).
* **Fixture-scope experiment** — standalone two-class pytest module in the
  scratch tree, module-scoped `usefixtures` fixture on the first class only.
  Executed: `1 failed, 1 passed`. Result below ([I1]).
* **Chunk C** — `git rev-list --count <ROOT_SHA>..<SELF_HOST_SHA> --
  dev/proposals dev/plans` -> `0`; same with trailing-slash pathspecs -> `0`;
  same with `--full-history` -> `0` (the prefix carries 2 merges, so this
  conjunct matters). Window arithmetic re-derived: 415 / 120 / 332 / 867, and
  `SELF_HOST..SNAPSHOT` = 452.
* **C11 under the narrowed window** — ran both arms at `ROOT..SNAPSHOT` and at
  `SELF_HOST..SNAPSHOT`: pinned findings 23, shipped 13, `len(pinned_b) == 2`,
  shas `== {INCIDENT_SHA}`, `shipped_b == pinned_b` — **identical in both**.
* **Chunk D exemptions** — confirmed `test_a_t2_timeout_is_enforced_and_bounded`
  and `test_a_t6_descendants_do_not_outlive_the_timeout` exist in
  `bootstrap/tests/test_security_stack.py`, and all five named head files exist.

**Verified sound, so a later reader does not re-audit them.** The "five
verified call families" claim is accurate about the source: `scripts/transition_lint.py`
has exactly five `_git(` call sites (293, 307, 336, 384, 451). C11's assertions
survive Chunk C's narrowing unchanged. Chunk C's replacement predicate is
robust in the safe direction — the plan's pathspecs (`dev/proposals`,
no trailing slash) are *broader* than `_in_scope`'s prefixes, so a count of
`0` implies the narrower predicate. And `rc != 0` never occurs across all 1279
distinct corpus keys, so "successful reads only" costs this consumer nothing —
there is no call site where a non-zero rc is the expected repeated result.

**Summary: 2 BLOCKING, 4 SUBSTANTIVE, 5 MINOR.**

### BLOCKING

**[I1] The module-scoped fixture leaks onto the synthetic tier, and the closed
grammar then raises. Every command this plan runs is blind to it.**

*Defect.* A1/B1 specify a **module-scoped** fixture attached to three classes.
Module scope is not class scope: pytest tears such a fixture down when the
*module* changes, so it stays installed for any later test in the same module —
including the synthetic nodes, whose argv is outside the closed grammar by
construction.

*Evidence, run.* (a) Standalone repro — module-scoped `usefixtures` fixture on
class one, a plain class two after it: `1 failed, 1 passed`, failing inside the
patched callable with `grammar refuses 'HEAD~1..HEAD'`. (b) The synthetic argv
is real: instrumenting the committed module, `tl.scan("HEAD~1..HEAD", repo)`
emits `('log', '--format=%H%x1f%s', 'HEAD~1..HEAD')` and
`tl.main(["HEAD~1..HEAD", ...])` emits
`('rev-parse', '--verify', '--quiet', 'HEAD~1^{commit}')` — neither matches
`<sha>`/`<rev-range>`/`<endpoint>`. (c) The window is reachable: replaying the
conftest shuffle over the real 2788-item collection, seeds **9, 11, 15 and 19**
of 0-19 each place a synthetic victim after a corpus test inside one
module-scope window (`TestShapeA::test_a_review_claim_with_no_added_body_flags`,
`TestExitContract::test_empty_range_is_clean_and_zero`,
`TestNarrowing::test_a_rename_into_archive_never_triggers`,
`TestNarrowing::test_a_proposal_derived_plan_is_not_absorbed_into_a_rename`).

*Why this is blocking rather than a note.* Natural order is clean (the corpus
classes sit after the synthetic ones and `TestSourceLevelBans` needs no `_git`),
seed 0 is clean, and seeds 0-2 are clean. So the plan's Boundary A
(`pytest bootstrap/tests/test_transition_lint.py`), its Boundary B
(`--quality-gate-shuffle-seed=0`), `quality_gate --sub order-independence` at
its default seed list `[0]`, and the `--seed-count 3` example in that gate's own
docstring **all pass**. The plan would land green and arm a failure for whoever
next runs a wider seed sweep or adds a node to this module. Correctness here is
an accident of collection order that no assertion pins.

*Suggested fix.* Split storage from installation: keep the cache dict and the
counters in a module-scoped fixture, and install the wrapper from a
**function-scoped** autouse fixture on each of the three classes, via
`monkeypatch.setattr(tl, "_git", wrapper)` so it is removed after every test.
The cross-test cache benefit is unchanged; the leak becomes structurally
impossible. Add one node asserting `tl._git` is unwrapped inside a synthetic
test, so the property is pinned rather than inherited from ordering.

**[I2] `<path>` is a live key dimension that neither named enforcer can
witness — the [E1] failure repeating on a component the revision did not
enumerate.**

*Defect.* Author-accounting states the memo-fidelity invariant is "*Enforced
by* the corpus assertions ... **plus** A2's two-root key tests". A2's five
mutants are: drop `root`, drop the `<sha>` operand, conflate families 4/5,
non-grammar refusal, `rc != 0`. None exercises the trailing `<path>` operand of
families 4 (`show <sha>:<path>`) and 5 (`show ... <sha> -- <path>`). Separately,
the plan **never states what the key is** — A1 specifies *admission* ("matched
structurally on command, option set and operand shape"); no line says the key is
the verbatim `(root, argv)` tuple. R1 dropped the original Part 1's "keyed on
the complete argument tuple plus the working root" and did not replace it.

*Evidence, run.* Re-ran all eleven corpus methods with a memo whose key strips
the `<path>` operand (`<sha>:<path>` -> `<sha>`; everything from `--` onward
dropped): **all eleven pass, and the distinct-key count is unchanged at 1279**.
The corpus population cannot produce the collision — `_shape_a` short-circuits
on the first trigger with sufficient evidence and `_shape_b` filters to `A`
entries, so no `(root, family, sha)` in the whole call set ever sees two paths,
even though 6 commits in `ROOT..SNAPSHOT` carry 2-3 in-scope trigger paths. A
path-dropping key therefore ships green through *both* enforcers the plan names.

*Suggested fix.* One sentence in A1 pinning the key as the verbatim
`(root, argv)` tuple with no derivation, and one A2 node: two distinct paths at
one sha in one root returning different bytes; dropping `<path>` must collide
and go red. Until then Author-accounting's first invariant overstates what A2
delivers, in the same way [E1] found the original claim overstating the corpus
assertions.

### SUBSTANTIVE

**[I3] A1's operand grammar is under-specified and, read literally, refuses 32%
of the real distinct keys.** A1 names three metavariables — `<sha>` 40 hex,
`<rev-range>` two such, `<endpoint>` one. The measured operands are not those.
From the census: family 4 contributes 232 distinct keys whose single operand is
`<sha>:<path>` — **0 of 232 are bare 40-hex**; family 5 contributes 174 keys
whose 348 operands are half SHAs and half paths. 406 of 1279 keys carry a
`<path>` the glossary never defines. Family 1's real operand is
`<endpoint>^{commit}` (run: `('rev-parse','--verify','--quiet',
'18a489f4...~1^{commit}')`) — the `^{commit}` suffix appears nowhere in the plan.
This is [E2]'s defect class re-compressed during the plan write-up. *Fix*: write
the grammar as five literal argv templates with `<path>` defined, and say
plainly that `<path>` carries no immutability claim of its own — it is keyed,
not validated. Also worth stating: only **four** of the five families are
reachable from the three memoized classes; family 1 is reachable only through
`main()`, which only synthetic nodes call — so its presence in the grammar is
either dead or a symptom of [I1].

**[I4] The plan drops a documentation obligation the accepted proposal
attaches to Chunk C.** The proposal's *Documentation / doctrine surface* says:
"The one exception, if Part 3 lands: `dev/plans/archive/transition-lint.md` owns
the corpus tier's rationale, and a narrowed window is a fact about that plan's
shipped artifact. The plan's archive record gets an appended note." The Revised
proposal keeps Part 3 as R4 and does not withdraw that. This plan's
*Documentation / doctrine surface* says "**None.**" and no chunk carries the
note. Verified the obligation is real: `dev/plans/archive/transition-lint.md`
line 575 pins C11's window as `0f1fc68..8f47c76` with its figure, so Chunk C
makes that record stale. *Fix*: add a C3 row appending the note, and reword
"None." to "no doctrine/adopter surface; one archive-record correction".

**[I5] R7's third bullet is unsequenced, so "sequences it and nothing else" is
not met.** R7 says the withdrawn `_immutable_git.py` helper "no longer
materializes; its `Proposed paths:` entry and `claim-check-allow` directive drop
at implementation". Both are still live in the proposal (the directive at its
line 7, the entry at line 170) and no chunk removes them. *Fix*: name it in a chunk,
or state in Scope that R7 is a record correction the plan deliberately leaves to
the Maintainer — but do not leave it silently unmapped under a claim of
completeness.

**[I6] Chunk D has no acceptance criterion.** *Acceptance criteria* is
"Per R6" and all three items are about the memo (invocation reduction,
byte-identical results, mutants red). None can be evaluated against D, whose
only artifact is a plan-record row. "Done" for the chunk the proposal cared most
about closing ("No file in the head is left unaddressed") is undefined. *Fix*:
add a fourth criterion — each of the five remaining head files carries a
recorded measurement plus either a memo disposition or a written reason.

### MINOR

**[I7] Criterion 1 is not executable as written.** "The wrapped-call count
drops" has no detached arm: with the fixture detached nothing wraps the calls,
so there is no count to compare against. The paired run needs a **count-only,
non-caching** wrapper as the detached arm. That is what produced this review's
6509/1279 pair; name the instrument in B2 so the figure is reproducible.

**[I8] Chunk C should be fenced after B2's paired measurement.** C narrows the
span-widening window 867 -> 452 commits, which cuts invocations independently of
the memo. The Sequence fences only "A before B". If C lands before B2, criterion
1's figure conflates two mechanisms — which undercuts the plan's own "argued on
the mechanism, never on cost". *Fix*: one line in Sequence — C after B2.

**[I9] C2's guard must not route through the memoized `_git`.**
`rev-list --count <range> -- <paths>` is a sixth family outside the closed
grammar. If C2 lands inside `TestWideningIsNotCreating` (which B1 memoizes) and
calls `tl._git`, it raises. Use `subprocess.run` directly, as
`test_every_whitelist_entry_is_a_full_40_char_sha_that_resolves` already does.
Add `--full-history` to the command: the dropped prefix contains 2 merges, and
without it the guard relies on history simplification not hiding a commit.
(Measured: all variants return `0`, so this is hardening, not a correction.)

**[I10] Two existing source-level bans are traps for A2's new nodes.**
`TestSourceLevelBans::test_no_corpus_node_carries_a_head_relative_range` asserts
no string constant containing `HEAD` appears inside any `@requires_corpus`
class — so A2's "pass `HEAD~1..HEAD` -> raises" node must not be placed in a
corpus-decorated class. And `test_every_pinned_sha_constant_is_a_full_40_hex`
walks module `globals()` for any name ending `_SHA`, so a two-root fixture
constant named `..._SHA` must be 40 hex. Neither is a defect; both will cost an
implementation round if unnoticed.

**[I11] Two small conformance points.** `dev/plans/_template.md` carries a
`## Source proposal` H2 ("a one-paragraph summary of what the proposal
decided"); this plan uses a bold header field instead, where two of three
sibling plans carry the section. And *Scope* says "Four chunks, all inside
`bootstrap/tests/`" while B2 and D1 are plan-record rows (and [I4] would add a
third file).
