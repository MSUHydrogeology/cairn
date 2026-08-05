<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/dual-review.md doctrine/plans.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Run the full suite once, at the boundary

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-05
**Status**: proposed
**Touches**: the verification contract in `AGENTS.md`,
`dev/plans/_template.md`, `dev/proposals/_template.md`,
`templates/core/AGENTS.md`, `templates/core/dev/plans/_template.md`,
`templates/core/dev/proposals/_template.md`, `doctrine/plans.md`, and
`doctrine/dual-review.md`; the documented use of `scripts/quality_gate.py`;
focused contract tests for the resulting command shape
**Related**: `release-security-orchestration`, `release-security-bar`,
`review-gate-enforcement`; `dev/PLANNING.md` > **Scoped test execution for
iterative agent work**
**Review**: required(External + External Security Review) -- this changes when
Cairn permits an implementer or code reviewer not to rerun the complete engine
suite, and therefore changes the regression-detection boundary.

## Context

Cairn's operational rule currently says to run
`python -m pytest bootstrap/tests` after any substantive change. The plan
template permits targeted tests while iterating but says the full suite gates
the cut. In practice, implementing agents run it at chunk boundaries and code
reviewers run it again because no reusable evidence names the exact tree that
was tested.

The nominal verification list also duplicates the suite. It asks for the full
engine suite and then `python scripts/quality_gate.py`; the quality gate's
default `order-independence` leg launches the full suite again with shuffle seed
0. A conscientious agent can therefore pay for two complete suite runs at one
boundary without gaining a second test corpus.

The cost is no longer incidental. At HEAD `ec57bf0`, the
canonical Python 3.13.13 interpreter collects **1,987 tests** across **97
top-level test files**, measured 2026-08-05. A full execution observed during
this proposal passed all 1,987 tests in **250.99 seconds**. Other commits landed
while that run was in progress, so the timing is diagnostic rather than a
clean-commit verification record; the count was re-collected at `ec57bf0` after
the tree settled. The invalid timing run is itself a useful demonstration:
evidence that does not pin and preserve one tested commit cannot safely be
reused.

This proposal does not try to make the suite less thorough. It gives each kind
of test run one job:

* plan-mapped tests guide iteration;
* one complete run catches unknown integration coupling at the implementation
  boundary;
* code review independently attacks the changed behavior; and
* the release ceremony retains its separate strict full-suite obligation.

## Proposal

### 1. Replace the universal rerun rule with three verification boundaries

#### Boundary A -- scoped iteration

During a plan chunk, run the exact tests and public-path probes named by that
chunk's acceptance criteria, plus any standing non-pytest gate for the touched
surface. The plan's existing author-accounting requirement already maps each
changed invariant and public entry point to a behavioral test; that reviewed
mapping is the source of the iteration scope.

This is not a universal "fast suite." Different changes need different tests.
A change to lockfile parsing may need upgrade and security-audit compatibility
nodes; a prose-only change may need only `check_cairn` and a focused neutrality
gate. The implementing agent adds a newly discovered dependency to the plan's
verification rows before relying on it.

The fail-closed default is simple: if a substantive code change has no reviewed
test mapping, or its affected surface cannot be bounded confidently, run the
full suite. "I could not identify the tests" never becomes permission to test
nothing.

#### Boundary B -- one integration record

After the final implementation commit and before code review, run one complete
integration verification against a clean, stable commit under the canonical
interpreter. The ordinary Cairn command pair becomes:

```text
python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

The first command satisfies both the engine-suite obligation and the existing
single-seed order-independence obligation. The second runs the two non-pytest
quality legs without launching the suite again. `--sub` is already repeatable;
this proposal changes the documented composition, not the quality-gate CLI.
`scripts/check_cairn.py`, per-file claim checks, and surface-specific gates
remain separate because they inspect different evidence.

The plan receives an append-only `## Implementation verification` record that
names:

* the full tested commit SHA and base/range the implementation represents;
* the canonical interpreter path and `python --version` output;
* clean-tree and unchanged-HEAD checks before and after the commands;
* every command, exit disposition, test outcome counts, and elapsed time;
* any skipped, xfailed, or xpassed outcome -- ordinarily zero -- with an
  explicit disposition; and
* the scoped commands run for plan-specific acceptance criteria.

The record is committed after the run, so its plan-only commit may advance
`HEAD` without changing the tested implementation bytes. If `HEAD` changes
during the run, the tree is dirty, or implementation/test/template/fixture
bytes in the reviewed implementation range change afterward, the record is
invalid and Boundary B runs again against the new final commit. A later
unrelated commit does not rewrite what the record proved about its named tree,
but it cannot use that record as evidence for its own new bytes. Appending
review or verification prose alone does not invalidate code evidence whose
tested SHA and reviewed range remain reachable and unchanged.

This is a process attestation under Cairn's trusted-contributor model, not a
cryptographic receipt. It prevents accidental reuse across commits and makes
the evidence inspectable; it does not prove that a dishonest author ran the
command. That threat is outside this change, just as it is outside today's
commit-body test reports.

#### Boundary C -- independent code review

The code reviewer confirms that Boundary B names the exact implementation
under review and then runs the tests needed for the reviewer's own
falsification ledger: the changed surface, a negative or edge case, and any
claim whose recorded evidence is doubtful. The reviewer does **not** rerun the
full suite by default merely to reproduce a broad green result already bound to
the same implementation commit.

A reviewer still orders a fresh full run when:

* no valid Boundary B record exists;
* the review finds an unrecorded cross-surface dependency;
* the recorded outcome contains an unexplained skip/xfail/xpass;
* the review changes implementation, tests, executable templates, or fixtures;
* the change touches a trust ceremony whose accepted plan explicitly requires
  independent full-suite execution; or
* the reviewer has a concrete reason to distrust or falsify the broad result.

Review sharpening that changes code invalidates the prior record. The final
implementation receives one replacement Boundary B run; the reviewer need not
repeat a full run after a prose-only review section is appended.

### 2. Make documentation-only work honestly cheap

A change confined to deliberation records or ordinary prose does not run the
engine suite unless it changes executable snippets, generated/frozen fixtures,
the gate manifest, or a contract whose own plan names pytest coverage. It runs
the applicable claim, link, snippet, and neutrality checks instead.

This replaces the current fiction that every substantive wording change gains
evidence from nearly two thousand engine tests. The relevant gate remains
mandatory; the irrelevant one stops being ceremony.

### 3. Keep release verification separate and strict

The accepted `release-security-orchestration` proposal still owns release
execution. Its command runs the complete suite in release mode, refuses
skip/xfail/xpass outcomes, binds the run to a clean `HEAD`, and performs its
own preflight/postflight. A Boundary B record from implementation does not
satisfy or shorten that release ceremony.

This proposal does **not** amend that accepted proposal's decision to exercise
the quality gate's nested order-independence path during release. The possible
release-only duplicate is paid once per release, not once per implementation
and review. Its implementation plan may identify the overlap, but removing it
requires an explicit amendment to the accepted release contract rather than an
implicit optimization here.

### 4. Apply the rule prospectively

The new contract applies automatically to plans opened from the revised
template. An already-open plan keeps its written verification contract.
Before implementation starts, its author may append an adoption amendment that
names Boundary A tests and adopts the Boundary B/C handoff; any required plan
review must confirm that amendment. An executing plan does not silently weaken
its gates mid-stream.

At implementation archive, this proposal retires the **Scoped test execution
for iterative agent work** board row. The lasting rule lives in `AGENTS.md` and
the plan/code-review doctrine rather than in a roadmap exception.

## Scope and interaction with current work

* `release-security-orchestration` owns `bootstrap/security_check.py`, release
  token propagation, and strict release outcomes. This proposal owns ordinary
  implementation/review reuse and does not edit that command.
* `review-gate-enforcement` may later validate the shape of an Implementation
  verification section, but this proposal does not make that parser expansion
  a precondition. Human-readable records are sufficient for v1.
* Existing security plans keep every plan-specific runner, mutation test,
  ceremony, and External review they already require. Reusing the full-suite
  result does not reuse a Security Reviewer's adversarial probes.
* Frozen gate and AST ceremonies retain their accepted exact commands. A
  generic efficiency proposal does not override a trust-root plan's stronger
  evidence contract.

## Why no global change-to-test map

A central path-to-test table looks attractive, but it becomes a second
dependency graph that can drift silently. Cairn's plans already require the
author to name the test for each invariant and public path, and plan review
already attacks that mapping. Reusing that reviewed work gives the selector an
owner and an expiry: it lasts for one implementation, not forever.

The complete integration run remains the backstop for dependencies the plan
did not know about. If repeated omissions reveal a stable cross-plan mapping,
that evidence can justify a generated or mechanically checked map later.

## Alternatives considered

### Install `pytest-xdist` and keep running everything

Deferred. Parallelism may eventually shorten Boundary B without changing its
coverage, but this suite manipulates git repositories and refs, loads shared
gate fixtures, and contains subprocess/time-sensitive tests. A parallel-safety
audit is a real project, and a new dev dependency is unnecessary to stop the
current duplicate runs. If one four-minute run per implementation remains too
expensive, that audit is the next optimization.

### Add a permanent `fast` marker

Rejected for v1. A fixed fast set answers "which tests are quick," not "which
tests cover this change." It would either grow into another near-full suite or
miss newly coupled behavior while continuing to report green.

### Use coverage-cache selection such as testmon/picked-style tooling

Rejected for now. Dynamic selection adds a plugin, a cache-provenance problem,
and weak visibility into subprocess and generated-tree dependencies. Cairn can
obtain most of the savings through lifecycle boundaries without trusting a new
selector.

### Keep requiring reviewers to rerun the full suite

Rejected. Independent review is valuable because the reviewer chooses a
different attack, not because two agents execute the same broad command. A
commit-bound record plus targeted falsification preserves the distinct jobs.

### Trust the implementation commit body as the reusable record

Rejected. The suite is normally run before the implementing commit exists, so
the message cannot name a commit that was already stable for the duration of
the run. A post-commit, plan-only record is a small cost for an exact evidence
boundary.

## Evidence and verification plan

### Author-accounting -- invariants and enforcers

| Invariant | Enforcer |
|---|---|
| A reduced iteration run is never selected without a reviewed mapping | the plan contract and its reviewer own the mapping; a template guard keeps the instruction and `missing mapping => full` fallback present, but v1 does not claim a parser verifies every filled plan |
| One suite run satisfies both engine and seed-0 order obligations | a quality-gate contract test invokes pytest with `--quality-gate-shuffle-seed=0`, then runs repeatable `--sub neutrality --sub redundancy` and asserts no order-independence subprocess is dispatched by the second command |
| Evidence cannot be reused across changed implementation bytes | plan template and doctrine require full tested SHA, clean pre/post state, stable HEAD, and invalidation after code/test/template/fixture changes in the reviewed range |
| Code review remains independent | the final-review template requires a targeted falsification ledger even when Boundary B is reused; copying the implementation command alone does not satisfy it |
| Release strength does not inherit the optimization | release docs and tests continue to require `bootstrap/security_check.py`'s own clean-HEAD strict run |
| Docs-only work does not silently skip relevant checks | verification matrix names claim/link/snippet/neutrality gates and the conditions that escalate prose to pytest |

**Failure disposition.** A missing or stale record, changed `HEAD`, dirty tree,
wrong interpreter minor, incomplete outcome count, unexplained non-pass outcome,
or unmapped substantive code surface escalates to the full suite. The mechanism
fails toward more testing, not less.

**Known omission.** The record is not signed or independently generated. It
reduces redundant honest work under the repository's trusted-contributor model;
it is not evidence against a malicious committer with write access.

### Tests required

* Add focused contract coverage for the documented combined command: seed 0 is
  accepted by `bootstrap/tests/conftest.py`; repeatable static `--sub` values do
  not dispatch `_run_order_independence`; omitting `--sub` retains today's all-
  gates behavior.
* Guard the plan-template verification matrix and Implementation verification
  record fields so a later template edit cannot restore the universal rerun
  claim or drop commit binding silently.
* Assert the code-review template continues to require targeted falsification
  when a Boundary B record is reused.
* Run the full suite once for this proposal's own final implementation record,
  under the new seed-0 composition, and record zero unexplained non-pass
  outcomes.

### Documentation delivered

* `AGENTS.md` carries the compact operational matrix and invalidation rule.
* `doctrine/plans.md` owns the implementation-record and review-reuse
  lifecycle.
* `doctrine/dual-review.md` explains why targeted independent falsification is
  not weaker than duplicate broad execution.
* The proposal and plan templates teach authors to map Boundary A and record
  Boundary B; their `templates/core/` counterparts carry the same boundary
  and record shape for adopters.

## Expected outcome

An ordinary plan pays for the complete engine suite once after its final
implementation commit, not once per chunk and again by default during code
review. The same run also satisfies the ordinary seed-0 order check instead of
being repeated inside `quality_gate.py`. Reviewers spend their time attacking
the change, while Cairn retains a full integration backstop and an independent,
strict release run.


## External review -- Antigravity (External, security lens) -- 2026-08-05

**Steelman.** Proposal `2026-08-05-codex-verification-boundaries.md` resolves a critical efficiency and duplication bottleneck in Cairn's verification workflow. Today, Cairn's operational rule requires running the full test suite (`python -m pytest bootstrap/tests`) after every substantive edit, and `scripts/quality_gate.py`'s default `order-independence` sub-gate runs the entire test suite a second time under shuffle seed 0. With 1,987 tests taking ~251 seconds (~4.2 minutes) per run, a single iteration pays ~8.4 minutes in duplicate test executions without increasing coverage. The proposal replaces the universal rerun rule with three explicit verification boundaries:
1. **Boundary A (Scoped Iteration)**: During plan chunk development, run mapped tests, acceptance criteria probes, and surface-specific gates. Fail closed to the full suite if mapping is absent or surface is uncertain.
2. **Boundary B (One Integration Record)**: Upon completing implementation, run **one** full integration pass using the deduplicated pair:
   ```text
   python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
   python scripts/quality_gate.py --sub neutrality --sub redundancy
   ```
   This satisfies engine suite + seed-0 order independence in a single pytest run, followed by non-pytest quality sub-gates. The result is recorded in an append-only `## Implementation verification` plan section bound to the tested commit SHA.
3. **Boundary C (Independent Code Review)**: The reviewer verifies the Boundary B record matches `HEAD`, then performs targeted falsification testing over changed surfaces and edge cases rather than rerunning the full suite by default (unless invalid record, code sharpening, or ceremony rules require it).

It also makes prose-only work honestly cheap (running claim/link/snippet/neutrality gates instead of pytest) while keeping the Maintainer release ceremony (`security_check.py`) strictly separate and un-compromised.

### Critical Security Audit & Analysis

1. **Deduplication Mechanics & CLI Verification (`quality_gate.py`)**:
   - **Empirical Check**: Inspected `scripts/quality_gate.py:779-799`. Passing `--sub neutrality --sub redundancy` sets `sub_gates = ["neutrality", "redundancy"]`. Because `"order-independence"` is omitted from `sub_gates`, `_run_order_independence()` is skipped entirely.
   - **Verification**: `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` executes all 1,987 tests under seed 0 shuffling in a single pass. Combining this with `quality_gate.py --sub neutrality --sub redundancy` eliminates 100% of redundant pytest executions while preserving full test and quality coverage.

2. **Commit SHA Binding & Evidence Invalidation (Boundary B)**:
   - **Security Invariant**: A verification record is only valid if it names the exact full commit SHA (`HEAD`) of the tested implementation state, verified clean pre-run and post-run.
   - **Invalidation Rule**: If any implementation code, test file, template, or fixture byte changes after the test run, the Boundary B record becomes invalid and must be re-run against the new `HEAD`. Reviewers (Boundary C) must explicitly assert that the recorded SHA matches the implementation commit under review.

3. **Fail-Closed Fallback Invariants**:
   - **Boundary A Fallback**: If an agent cannot confidently bound the affected test surface or lacks a reviewed test mapping, the fallback is to execute the full suite. "Uncertain scope" never permits un-tested commits.
   - **Boundary C Invalidation**: Any code change made during review sharpening invalidates the prior Boundary B record, requiring a fresh Boundary B integration run before final landing.

4. **Release Gate Boundary Preservation**:
   - The proposal explicitly fences out `bootstrap/security_check.py` and the Maintainer release ceremony. Release-mode verification retains its strict full-suite run with skip/xfail/xpass refusals.

### Covered

* **Empirical CLI Audit**: Verified `quality_gate.py` argument parsing and sub-gate execution logic.
* **Claim-check Verification**: `claim_check.py` passed cleanly on `dev/proposals/2026-08-05-codex-verification-boundaries.md`.
* **Path Resolution**: All cited paths (`AGENTS.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `templates/core/AGENTS.md`, `doctrine/plans.md`, `doctrine/dual-review.md`) resolve accurately.

### Concerns

* **[E1] Future Machine Parsing of Implementation Verification Records**:
  - While Markdown text records are sufficient for v1, future tooling (`lifecycle_planner.py` or transition linters) should mechanically validate that the `Tested HEAD` in `## Implementation verification` matches `git rev-parse HEAD`, preventing human or agent copy-paste errors.

### Recommendation

**ACCEPT / SHIP PROPOSAL.** The proposal is technically sound, empirically verified, security-hardened, and significantly improves development velocity without compromising quality or verification rigor. Proceed to Decision.

