<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/proposals/archive/2026-08-05-codex-verification-boundaries.md, bootstrap/tests/test_verification_boundaries.py -->

# Plan: run the full suite once, at the boundary

**Source proposal**: [`dev/proposals/archive/2026-08-05-codex-verification-boundaries.md`](../proposals/archive/2026-08-05-codex-verification-boundaries.md)
**Status**: awaiting-plan-review
**Plan review**: required(External + External Security Review) -- two distinct
rounds; this plan changes when agents may omit a full-suite rerun
**Last update**: 2026-08-05
**Opened**: 2026-08-05

## Source proposal

Accepted at Decision commit `740b7b6`, the proposal replaces Cairn's universal
full-suite rerun habit with three boundaries: plan-mapped tests during
iteration; one clean, stable, commit-bound integration run before code review;
and independent targeted falsification during code review. The ordinary full
run also carries shuffle seed 0, so the subsequent quality-gate command runs
only neutrality and redundancy instead of launching pytest a second time.

The accepted safety posture is part of the implementation contract: uncertain
or unmapped code scope falls back to the full suite; code-bearing review
sharpening invalidates the integration record; prose-only work runs its relevant
gates; and `bootstrap/security_check.py` retains its separate strict release
contract without optimization here.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_verification_boundaries.py` -- focused guards for the governing/template boundary contract and the existing quality-gate command composition; lands in Chunk C.

## Plan-review precondition

Implementation does not start until both declared rounds have landed with no
outstanding REVISE:

1. **External plan review** -- a different agent type or human checks whether
   the operational, doctrine, and template texts form one executable contract,
   and attacks the Boundary A/B/C handoff as a workflow.
2. **External Security Review** -- a distinct security-lensed round attacks the
   permission not to run tests: stale/missing mappings, record reuse across
   changed bytes, concurrent `HEAD` movement, unexplained non-pass outcomes,
   review sharpening, and accidental weakening of the release ceremony.

The accepted proposal's External Security Review does not substitute for these
plan-level reads. The newest and least-examined surface is the exact
Implementation verification record schema in Chunk B; both rounds must judge
that schema before implementation.

## Scope

This plan executes the accepted v1 contract through governing instructions,
plan/code-review doctrine, self-hosted templates, adopter templates, and focused
guards. It does not add a test-selection engine or another verification runner.

**In scope:**

* compact Boundary A/B/C operational rules in Cairn's `AGENTS.md` and the
  installed `templates/core/AGENTS.md`;
* the lifecycle and review-reuse rationale in `doctrine/plans.md` and
  `doctrine/dual-review.md`;
* a reviewed Boundary A mapping prompt and append-only Boundary B record schema
  in Cairn's and adopters' plan templates;
* proposal-template guidance that distinguishes plan-mapped scope from a fixed
  speed tier;
* focused tests proving the required text surfaces exist and that the accepted
  static quality-gate composition does not dispatch order-independence; and
* retirement of the `dev/PLANNING.md` scoped-test row at archive, after lasting
  truth has landed.

**Scope fence:**

* no `pytest-xdist`, fixed `fast` marker, coverage cache, global path-to-test
  map, or automatic selector;
* no machine parser for Implementation verification records in v1 -- External
  concern [E1] retains its accepted trigger and corrected ancestry/path rule;
* no signed receipt, authentication, or malicious-committer claim;
* no edit to `bootstrap/security_check.py`, its release token, its nested
  order-independence regression, or the accepted release plan;
* no edit to `scripts/quality_gate.py`; repeatable `--sub` and seed-0 behavior
  already exist;
* no modification of frozen gate tests or fixtures, and therefore no new
  supervised re-anchor contribution from this plan; and
* no silent retrofit of an open or executing plan. Existing plans adopt only
  through their own append-only amendment and required review.

### Documentation / doctrine surface

`AGENTS.md` and `templates/core/AGENTS.md` are the operational homes. The rule
there stays imperative and compact: scoped iteration, one stable integration
record, targeted review reuse, invalidation, and fail-to-full fallback.

`doctrine/plans.md` owns the plan lifecycle details: when the record is made,
its schema, what changes invalidate it, and how it composes with code review.
`doctrine/dual-review.md` owns why independent targeted falsification is not
weaker than duplicate broad execution. `dev/plans/_template.md` and
`dev/proposals/_template.md` are Cairn's self-hosted filled forms;
`templates/core/dev/plans/_template.md` and
`templates/core/dev/proposals/_template.md` carry the generalizable adopter
shape.

No descriptive user guide changes. The change governs development practice and
belongs in the governing/doctrine/template layers.

## Cross-plan sequencing

`release-security-orchestration` is already executing and owns the same
`dev/plans/_template.md` paragraph in its Chunk E1, where it removes the false
claim that CI runs Cairn's standing gates. That correction lands first.

Chunk B of this plan then reads the landed E1 bytes and replaces the larger
verification block while preserving the no-CI truth. It must not restore the
phrase "the same ones CI enforces." If release Chunk E has not landed, Chunk B
waits; Chunks A and C may be prepared, but no partial template contract lands.

The release plan otherwise remains untouched. Its deliberate release-only
second pytest path is not evidence of a defect in this plan's ordinary command
composition.

## Sequence

```text
1. Chunk A -- governing rule and lifecycle doctrine                    [pending]
2. Chunk B -- self-hosted + adopter template contract                  [pending; after release Chunk E1]
3. Chunk C -- focused guards for text and command composition          [pending]
4. Chunk D -- clean-commit Boundary B run + append-only record         [pending]
5. Archive -- board-row retirement and lasting-truth sign-off          [pending]
```

### Chunk A -- governing rule and lifecycle doctrine

| # | File | Change |
|---|---|---|
| A1 | `AGENTS.md` | Replace the universal "run the test suite after any substantive change" bullet with the compact Boundary A/B/C matrix. Require full fallback for missing/uncertain mappings, one stable clean-commit record, targeted reviewer falsification, and invalidation after reviewed implementation/test/template/fixture changes. Keep the canonical-interpreter requirement. |
| A2 | `templates/core/AGENTS.md` | Carry the same generalizable operational rule for adopters, phrased in terms of their configured full suite and plan-mapped tests rather than Cairn-specific paths. |
| A3 | `doctrine/plans.md` | Define the post-implementation/pre-review record lifecycle, the schema from Chunk B, record validity and invalidation, prose-only disposition, and the rule that later unrelated commits do not retroactively falsify evidence for the named tested tree or make it evidence for new bytes. |
| A4 | `doctrine/dual-review.md` | Define Boundary C: verify the record against the reviewed range, then independently choose targeted falsification. List the conditions requiring a fresh full run and state that duplicate command execution is not itself structural independence. |

**A acceptance:** the four surfaces agree on the fallback and invalidation
conditions. Neither doctrine file claims automated enforcement. The installed
AGENTS template names no Cairn-only command.

### Chunk B -- template contract

| # | File | Change |
|---|---|---|
| B1 | `dev/plans/_template.md` | Replace the verification-command block with Boundary A mapping instructions and the deduplicated ordinary command pair. Preserve release E1's no-CI correction. Add an instruction -- not an empty H2 -- to append the record only after a stable implementation commit. |
| B2 | same | Define the exact record heading and fields: `## Implementation verification -- <agent> -- YYYY-MM-DD`; `Tested commit` (full SHA); `Reviewed range` (base and tested endpoint); canonical interpreter path/version; pre/post clean state and identical HEAD; command/result table with exits, outcome counts and elapsed time; explicit skip/xfail/xpass disposition; plan-specific acceptance commands; known omissions. |
| B3 | same | Amend Code review instructions: verify the tested SHA/range and path validity, run an independent targeted falsification ledger, and order a fresh full run on the accepted six triggers. Copying Boundary B's broad command does not satisfy the ledger. |
| B4 | `templates/core/dev/plans/_template.md` | Carry the same mapping, record, invalidation, and review-reuse shape using adopter-configured command placeholders. Missing mapping falls back to the adopter's full suite. |
| B5 | `dev/proposals/_template.md` | Replace "no separate slow tier" guidance with the accepted distinction: plan-specific scoped iteration is not a permanent fast tier; proposals name affected test homes/public paths and unknown scope falls back to full. Preserve Cairn's actual test homes. |
| B6 | `templates/core/dev/proposals/_template.md` | Carry the general form: name project test homes and speed/environment tiers if they exist, while refusing to infer change coverage from speed alone. |

**Record validity rule, exact enough to implement:** the tested commit must
contain the entire reviewed range; pre/post `HEAD` must equal that full SHA;
pre/post tree state must be clean; and no later commit included in the review
may change the range's implementation, test, executable-template, or fixture
paths without a replacement record. A later plan-only record/review commit may
advance live `HEAD`. A later unrelated implementation commit cannot cite the
old record for its own bytes.

**B acceptance:** all six templates/doctrine surfaces use the same record field
names and six fresh-run triggers. No empty `## Implementation verification`
heading exists in a newly opened plan, because an empty heading could be
misread as landed evidence.

### Chunk C -- focused guards

| # | File | Change |
|---|---|---|
| C1 | `bootstrap/tests/test_verification_boundaries.py` *(new, not frozen)* | Guard the operational pair: both AGENTS surfaces name scoped iteration, stable full record, targeted review, invalidation, and full fallback; the installed form remains project-general. |
| C2 | same | Guard both plan templates' record heading instruction and required field vocabulary; assert neither template contains an empty landed record heading. Guard both proposal templates against equating "fast" with affected coverage. |
| C3 | same | Load `scripts/quality_gate.py`, replace all three sub-gate functions with probes, and assert `run_gates(["neutrality", "redundancy"], ...)` never calls order-independence while invoking both static legs. Assert default CLI resolution still selects all three legs, so the focused composition does not weaken the public default. |
| C4 | same | Guard `doctrine/plans.md` and `doctrine/dual-review.md` for the tested-range, invalidation, targeted-falsification, release-separation, and non-authentication residuals. These are semantic token/section checks, not a byte-for-byte prose lock. |

**Perturbations:** remove the full fallback, delete `Reviewed range`, make
review reuse unconditional, or accidentally call the default all-gates list in
the static composition; each mutation must make a named C-node fail.

### Chunk D -- implementation verification record

Chunk D changes no governing/code/template bytes. After Chunks A--C are
committed, the implementer starts from a clean tree at stable commit `T`,
records `git rev-parse HEAD` before and after, and runs under the canonical
interpreter:

```text
python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
python scripts/check_cairn.py
python scripts/claim_check.py <each authored proposal/plan/doc, one at a time>
```

The full-suite result must have no unexplained skipped, xfailed, or xpassed
outcomes. `HEAD` movement, dirt, a wrong interpreter minor, or any non-clean
gate invalidates the run rather than becoming a partial record.

Once valid, append the complete Implementation verification section to this
plan and commit that plan-only record. This is the first dogfood of the new
contract. It must name `T`, not the later record commit.

## Acceptance criteria

* **Tests that must pass:**
  * Boundary A while iterating: the affected nodes in
    `bootstrap/tests/test_verification_boundaries.py`, plus unchanged
    `bootstrap/tests/test_quality_gate_order_independence.py` when validating
    the seed/default behavior.
  * Boundary B: one complete shuffled engine suite under canonical Python
    3.13.x, recorded per Chunk D.
* **Docs that must land:** the two AGENTS operational surfaces, two doctrine
  homes, and four proposal/plan templates named in Chunks A/B. All are
  hand-authored; no generated or snippet-synced surface is in scope.
* **Examples / smoke checks:** `scripts/check_cairn.py` over the complete
  Markdown tree and `scripts/quality_gate.py --sub neutrality --sub redundancy`.
  There is no user-facing executable example for a development-process rule.
* **Release non-regression:** `git diff -- bootstrap/security_check.py
  bootstrap/tests/conftest.py bootstrap/tests/test_security_check.py` is empty
  for this plan, and the release plan's decisive nested-child regression remains
  unchanged.
* **Prospective-only migration:** no existing plan's historical Verification or
  Code review section is rewritten. Adoption by an open plan is append-only and
  separately reviewed under that plan's declared tier.

### Author-accounting -- invariants, failure modes, edge cases

| Invariant | Enforcer |
|---|---|
| Missing/uncertain scoped coverage falls back to the full suite | `test_verification_boundaries.py::test_both_operational_surfaces_fail_to_full` plus External review of the filled template contract |
| One ordinary full run also satisfies seed-0 order coverage | `test_verification_boundaries.py::test_static_quality_composition_does_not_dispatch_pytest` and existing shuffle-hook tests |
| A record cannot honestly cover changed reviewed bytes | record field guards plus reviewer comparison of `Reviewed range`, tested SHA, and changed paths; v1 explicitly has no parser |
| Review remains independent without duplicate broad execution | doctrine/template guard requires targeted falsification and rejects broad-command copying as the ledger |
| Release verification is not shortened | unchanged release paths plus the plan scope test/assertion |
| Adopters receive the same method without Cairn-specific commands | paired template assertions in the new test file |

**Failure modes:** an author may select too narrow a mapping; the final full run
is the integration backstop and plan/code review attack the mapping. A record
may contain a copy/paste error; v1 relies on reviewer comparison, with the
accepted [E1] trigger for a parser. Concurrent `HEAD` movement invalidates the
run. A later unrelated commit does not become covered merely by ancestry.

**Known omissions:** no malicious-committer protection, signature, automatic
test selection, parser enforcement, parallel safety claim, or release-command
optimization.

## Verification

During Chunks A--C, use Boundary A rather than repeatedly running the full
suite:

* `python -m pytest bootstrap/tests/test_verification_boundaries.py -q`
* `python -m pytest bootstrap/tests/test_quality_gate_order_independence.py -q`
  when seed/default behavior changes or is challenged
* `python scripts/check_cairn.py`
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/claim_check.py <file>` once per authored Markdown file

Chunk D performs the one complete integration run and records it. A plan or
security reviewer may require additional targeted probes; neither review tier
is discharged by these author-run commands.

Implementation appends a complete `## Implementation verification -- <agent>
-- YYYY-MM-DD` section only after the stable Chunk-D run. It does not create an
empty evidence heading in advance.

## Code review

*Filled after implementation. The reviewer verifies the tested commit and
reviewed range, then supplies an independent targeted falsification ledger.
Because this implementation changes Cairn's permission not to rerun tests, the
code reviewer is a different agent type or human. A fresh full run is required
only on the accepted invalidation/uncertainty triggers, not by reflex.*

## Lasting-truth migration

At archive, confirm the Decision-to-implementation mapping for all three
boundaries, record the accepted [E1] parser trigger as an unresolved tightening
rather than v1 enforcement, and remove the **Scoped test execution for iterative
agent work** row from `dev/PLANNING.md`. The governing rule then lives in
AGENTS/doctrine/templates; the board carries no duplicate instruction.

No other PLANNING security or release row is retired by this plan.
