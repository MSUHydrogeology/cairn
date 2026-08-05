# Plan: one honest release-security command

**Source proposal**: [`dev/proposals/archive/2026-08-05-codex-release-security-orchestration.md`](../proposals/archive/2026-08-05-codex-release-security-orchestration.md)
**Status**: executing
**Plan review**: required(External + External Security Review) — as declared and ratified; **this plan's author cannot supply either tier** (see *Plan review* below)
**Last update**: 2026-08-05
**Opened**: 2026-08-05

## Source proposal

`bootstrap/security_check.py` is documented as Cairn's release-security command
but runs only Bandit and `check_cairn`. `SECURITY.md` separately asks the
Maintainer to *remember* the suite; `quality_gate.py` is in no checklist at all;
the suite exits zero after a skip; and several comments claim CI supplies a
trigger Cairn does not have.

The proposal makes the existing command complete rather than adding a second
wrapper: four phases (repository-state preflight → Bandit + `check_cairn` →
the full suite in release mode → `quality_gate.py`), a release-only pytest
disposition that refuses skipped/xfailed/xpassed outcomes, a self-retiring
Bandit allowlist, corrected trigger vocabulary, and an explicit **human-root
disposition** — Cairn will not pretend to mechanize the Maintainer's act.

Accepted as revised at `ec57bf0` (Decision scribed by Antigravity on quoted
Maintainer instruction), incorporating **Binding amendment R1** on release-token
propagation.

## Plan review — the author cannot supply the declared tier

The tier is **`required(External + External Security Review)`** because this
changes the command Cairn names as its fail-closed release security gate.

* **External** floor is *a different agent type or a human*
  (`doctrine/dual-review.md`). This plan is authored by Claude; a fresh Claude
  session is the **Internal** floor and does not satisfy External.
* **External Security Review** is a second, security-lensed pass over the same
  boundary.

So implementation **cannot begin** on this plan until a different agent type or
the Maintainer supplies both. Stated here rather than discovered later, because
the failure mode this tier exists to prevent is exactly a same-type reviewer
waving through a change to the release gate. Recorded per `doctrine/plans.md`:
the plan sits in `awaiting-plan-review`, and the plan-open and first
implementation commits stay distinct regardless.

## Scope

Executes the proposal's five parts. The proposal's own *Scope and interaction
with current plans* section is authoritative and is not re-litigated here.

**Scope fence — explicitly not this plan:**

* **The other security plans' territory.** `default-security-stance`,
  `portable-security-sweeps`, `security-verification-activation` and
  `api-web-security-modules` keep module selection, runners, policies and
  registry bindings; their shipped Python enters `scan_targets()`
  automatically and is **not** re-enumerated or baselined here.
  `content-scan-detectors` / `separator-detection` keep the scanner — the
  release command reaches their result *through* `check_cairn`.
  `dependency-advisory-coverage` keeps its no-baseline v1; this command does
  **not** run adopter-facing dependency modules against Cairn's own environment.
  `release-security-bar` stays the v0.4.0 register and decider owner: this
  supplies a better local machine-checkable decider, and does not absorb its
  manual checks, the contained floor check, examples, the release-authenticity
  ceremony, B1–B6, or any readiness declaration.
* **Any mechanization of the human root.** No tag wrapper, no CI workflow, no
  signed gate receipt, no mandatory hook. Part 5 *names* the residual; building
  machinery instead would contradict the accepted Decision.
* **The rows the proposal explicitly does not close** — install-integrity trust
  anchor, conda advisory coverage, the axis-2/axis-3 claim audit, gate-manifest
  skip-marker over-reporting, and the release checker's own integrity preflight.
* **Carrying any number forward.** The proposal binds this plan: *"Every count,
  frozen-file delta, and suite figure is re-derived at plan/implementation time
  after the other security plans land. No number in an earlier plan is an input
  here."* Treated as a hard rule, not a preference.

### Documentation / doctrine surface

`SECURITY.md` (governing security workflow), `bootstrap/PROVENANCE.md`
(source→tag ordering), and `doctrine/runtime-contract.md` (the floor-check
description, corrected from "release floor gate" to the Maintainer-run contained
check). `dev/plans/_template.md` loses its false-CI claim **prospectively at the
template source only** — existing plan sections stay append-only. One
`CHANGELOG.md > Unreleased > Changed` line. **No adopter doctrine or installed
module behaviour changes**: this is Cairn's own development apparatus.

## R1.4 — the plan-time call-path audit, performed

Binding amendment R1 clause 4 requires the plan to re-enumerate nested pytest
launchers. Performed at HEAD `04de250`, `as_of 2026-08-05`, by grepping every
`.py` under `scripts/`, `bootstrap/`, `templates/` and `tools/` for a pytest
child process:

| Launcher | Kind | Environment handling | R1 status |
|---|---|---|---|
| `scripts/quality_gate.py:158` — order-independence runner | **executable** | `subprocess.run(cmd, cwd=…, capture_output=True, text=True)` — **no `env=`**, so it inherits | in scope for R1.2/R1.3 |
| `bootstrap/tests/_gate_manifest.py:203` | **collection-only** (`--collect-only`) | `dict(os.environ, CAIRN_GATE_COLLECT_OUT=…)` — copy-and-merge, token preserved | recorded, **not** execution evidence |

**No newly discovered executable launcher.** The proposal's Response enumerated
these two; both are re-confirmed at HEAD. One candidate that post-dates that
Response was checked and excluded: `bootstrap/tests/test_security_stack.py:700`
passes an explicit `env=`, but launches the **installed** security-audit runner
inside an adopter fixture (source:
`templates/modules/team-gated/run_security_audit.py`) — **not pytest** — so it
is outside R1's scope. (`_gate_manifest.py:126` is a `"cmd"`
string inside a data table, not a launcher.)

Per R1.4 this audit is **re-run at implementation time**, since the security
cluster is landing concurrently and a new launcher may appear between now and
then.

## Sequence

```
1. Chunk A -- repository-state preflight (+ its git-hardening reuse)   [pending]
2. Chunk B -- four-phase orchestration + R1 token propagation          [pending]
3. Chunk C -- release-only pytest disposition in conftest              [pending]
4. Chunk D -- self-retiring Bandit allowlist                           [pending]
5. Chunk E -- trigger-vocabulary corrections (frozen files)            [pending]
6. Chunk F -- SECURITY.md + PROVENANCE.md: name the human root         [pending]
7. Chunk G -- CHANGELOG + board retirement at serialization            [pending]
```

### Chunk A — repository-state preflight

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/security_check.py` | Preflight: checkout root; clean tracked **and untracked** worktree; resolvable full `HEAD`. Runs first and stops the command on failure |
| A2 | same | Git invoked with steering environment stripped and execution-bearing config disabled — **reusing the narrow pattern from the existing trust-root tools**, not an ambient `git status` |
| A3 | same | Post-phase re-check: `HEAD` unchanged **and** tree still clean; the full `HEAD` printed in the summary so release notes bind the run to the tagged commit |

### Chunk B — the four phases and R1 propagation

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/security_check.py` | Phases 2–4 all attempted after preflight passes, so one run yields a complete repair list. Non-zero on any phase failed / errored / unavailable / candidate-changed / **incomplete evidence**; `PASS` only after both state checks and all three phases are clean |
| B2 | same | **R1.1** — child environment built from a **copy** of `os.environ`, `CAIRN_RELEASE_GATE_ACTIVE` set to the one recognized value, passed **explicitly** to both the suite and quality-gate subprocesses |
| B3 | `bootstrap/tests/test_security_check.py` *(frozen)* | **R1.3** — capture both direct child environments and require the **exact** token |

### Chunk C — release-only pytest disposition

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/conftest.py` *(frozen)* | Recognize the token; in release mode any actual `skipped` / `xfailed` / `xpassed` makes the session non-zero. An already-failing or interrupted session stays non-zero. **Without the token, contributor behaviour is unchanged.** An outcome rule, **not** a marker census — an inactive `skipif` marker does not fail a release for existing |
| C2 | `bootstrap/tests/test_security_check.py` | **R1.3, decisive half** — the quality-gate regression selects a release-outcome fixture through the **real order-independence child path**: a skipped/xfailed/xpassed child makes the parent phase non-zero; a clean child passes |

### Chunk D — self-retiring Bandit allowlist

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/security_check.py` | **Delete the stale `B310` entry** (measured absent — re-verify at implementation) |
| D2 | same | `run_bandit()` derives observed `(repo-relative path, test_id)` pairs from the **successfully parsed** report and fails closed if any configured `ALLOWLIST` key is absent. Rationale stays mandatory; liveness is an **additional** condition |
| D3 | `bootstrap/tests/test_security_lint.py` *(frozen)* | Pin both directions: a live key passes; an absent key fails closed |

### Chunk E — trigger vocabulary (frozen surfaces)

| # | File | Change |
|---|------|--------|
| E1 | `dev/plans/_template.md` | "the standing gates Cairn runs before a change lands" — no CI claim. **Template source only**; existing plan sections stay append-only |
| E2 | `bootstrap/tests/test_security_lint.py` *(frozen)* | CI branch described as dormant provisioning; names the release command as today's fail-closed trigger |
| E3 | `bootstrap/tests/fixtures/skills/README.md` *(frozen)* | "suite-proven"; names a recorded native-harness transcript where the suite cannot run the harness |
| E4 | `bootstrap/tests/test_python_floor.py` *(frozen)*, `bootstrap/requirements-dev.txt` | "floor check", not "CI floor check" |
| E5 | `doctrine/runtime-contract.md` | `bootstrap/container/floor-gate.sh` is the **Maintainer-run contained floor check**; an unresolvable `vermin` fails *that command*; no implication that the release command dispatches it |

### Chunk F — name the human root

| # | File | Change |
|---|------|--------|
| F1 | `SECURITY.md` | Names the one command and **requires its output, including the full clean `HEAD`, in the release notes** |
| F2 | `bootstrap/PROVENANCE.md` | States the ordering: run against the clean commit, **then** sign a tag naming that same commit |
| F3 | both | The three accepted residuals stated plainly (omission possible; no self-authentication; no cryptographic binding to the tag) **and their expiry**: a second release Maintainer, untrusted contributions, forge automation, or a missed check in practice |

### Chunk G — changelog and board

| # | File | Change |
|---|------|--------|
| G1 | `CHANGELOG.md > Unreleased > Changed` | The Maintainer-run release command now covers the complete local bar and refuses dirty or incomplete runs |
| G2 | `dev/PLANNING.md` *(at its serialization point)* | Retire the six rows the proposal's *Board effect* table disposes — including **SC5** and **G6**, whose corrected text `board-drain-guards` landed at `5e10623` |

## Acceptance criteria

* **Tests that must pass** — `python -m pytest bootstrap/tests` under the
  canonical interpreter (3.13.x), **measured in a clean worktree**: the security
  cluster is landing concurrently, and a figure taken in this shared tree is not
  a measurement of this change (established by `board-drain-guards`' code review
  [C1], where a suite figure silently absorbed 22 nodes from another session's
  uncommitted file and self-validated against an equally contaminated baseline).
* **The decisive R1 regression** (C2) is the acceptance gate for release-token
  propagation — not B3's direct-environment capture, which a future custom
  environment could satisfy while still stripping the token from the real child.
* **Every phase's refusal is proven by execution**, not asserted: dirty tree,
  changed `HEAD`, unavailable tool, skipped test, absent allowlist key. Each
  gets a mutation or fixture that makes the command non-zero.
* **Docs that must land** — `SECURITY.md`, `bootstrap/PROVENANCE.md`,
  `doctrine/runtime-contract.md`, `dev/plans/_template.md`, `CHANGELOG.md`.
  Hand-authored; none generated or snippet-synced.
* **Smoke** — `python scripts/check_cairn.py`; `python scripts/quality_gate.py`;
  `python scripts/claim_check.py <file>` per artifact.
* **Changed-file set** verified **per-commit** (`git show --format="" --name-only`),
  never by a range diff over a tree with concurrent sessions in it.
* **Frozen-file delta re-derived at implementation**, not carried from here.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  1. *The release token reaches every pytest child whose result is release
     evidence.* **Enforcer: C2**, the order-independence regression through the
     real child path. R1.3 names this as the decisive check precisely because
     B3 alone is satisfiable by a broken implementation.
  2. *Contributor behaviour is unchanged without the token.* **Enforcer:** a
     conftest test asserting ordinary skip semantics with the token absent, and
     with a wrong value.
  3. *An allowlist entry is live.* **Enforcer: D3**, both directions.
  4. *The command refuses a changed candidate.* **Enforcer:** a fixture mutating
     the tree between preflight and the post-check.
* **Failure modes.** Every phase failure must fail **closed**; the proposal
  makes "incomplete evidence" a non-zero outcome specifically so an unavailable
  tool cannot read as a pass. The **known fail-open** is the human root (Part 5)
  and it is *named*, not closed.
* **Edge cases.** Untracked files present (must refuse — reproduced 2026-08-05
  as exit 0 today); `HEAD` unresolvable; Bandit report partially parsed (liveness
  derives only from the **successfully parsed** report); an inactive `skipif`
  marker (must **not** fail a release); a wrong-valued token (contributor
  behaviour).
* **Known omissions.** The command does not authenticate its own bytes or
  process; nothing binds its output to the tag. Both are accepted residuals with
  a stated expiry, not oversights.

## Verification

Cairn has **no CI**. Every command below is run by a person or an agent at a
commit boundary; nothing enforces them automatically — which is the very claim
this plan corrects across five surfaces.

* `python -m pytest bootstrap/tests` — canonical 3.13.x, in a clean worktree.
* `python bootstrap/security_check.py` — the command under construction; its own
  output is evidence.
* `python scripts/check_cairn.py`, `python scripts/quality_gate.py`,
  `python scripts/claim_check.py <file>`.
* `python bootstrap/tests/_gate_manifest.py verify --no-collect` — this plan
  touches **five frozen files** (`test_security_check.py`, `conftest.py`,
  `test_security_lint.py`, `test_python_floor.py`,
  `fixtures/skills/README.md`); the delta is re-derived at implementation and
  batched into the **already-scheduled shared supervised re-anchor**, per the
  proposal's sequencing note. Implementation is the **last code scope admitted
  before that ceremony**.

## Plan review -- Antigravity (External, security lens) -- 2026-08-05

**Steelman.** Plan `release-security-orchestration.md` provides a complete, 7-chunk execution breakdown for accepted proposal `2026-08-05-codex-release-security-orchestration.md` (Decision `ec57bf0`). It operationalizes the consolidation of Cairn's local release security bar into a single fail-closed command (`python bootstrap/security_check.py`) across four sequential phases: repository-state preflight/postflight (Chunk A), Bandit + `check_cairn.py` (Chunk B), release-mode pytest disposition (Chunk C), and `quality_gate.py` (Chunk B/C). It enforces self-retiring Bandit allowlist liveness (Chunk D), corrects trigger vocabulary across frozen test surfaces and doctrine (Chunk E), grounds the human root in `SECURITY.md` and `PROVENANCE.md` (Chunk F), and handles serialization point updates (Chunk G). It incorporates Binding Amendment R1 in full, backed by a verified plan-time call-path audit (Section R1.4).

### Critical Plan Audit & Security Analysis

1. **Satisfaction of Plan Review Tiers (`External + External Security Review`)**:
   - The declared tier `required(External + External Security Review)` is satisfied by this review: Antigravity is a distinct agent type from the author (Claude), fulfilling the structural independence floor required by `doctrine/dual-review.md` for changes to Cairn's fail-closed release gate.

2. **R1 Call-Path Audit & Decisive Regression Enforcement**:
   - **Audit Verification**: Verified the Section R1.4 call-path audit across `scripts/`, `bootstrap/`, `templates/`, and `tools/`. `quality_gate.py:158` remains the single executable nested pytest launcher (`subprocess.run` inheriting process env). `_gate_manifest.py:203` is collection-only (`dict(os.environ, ...)`).
   - **Decisive Test Alignment**: Chunk C2 explicitly identifies the order-independence child path through `quality_gate.py` as the decisive regression gate for release-token propagation. This correctly prevents false-green results where `security_check.py` passes the token to its direct child but a nested launcher silently drops it.

3. **Dirt Control & Fail-Closed Preflight/Postflight Design**:
   - Chunk A enforces clean tracked AND untracked worktree state both before Phase 1 and after Phase 4.
   - **Git Hardening**: Chunk A2 explicitly mandates stripping `GIT_*` steering variables (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, etc.) during preflight/postflight git calls, preventing environment-tampering attacks from redirecting repository detection.

4. **Allowlist Liveness & Frozen-File Batching**:
   - Chunk D1 deletes the stale `B310` allowlist key; Chunk D2 enforces that `run_bandit()` fails closed if any configured `ALLOWLIST` key is missing from Bandit's parsed report.
   - The plan correctly batches the 5 touched frozen files (`test_security_check.py`, `conftest.py`, `test_security_lint.py`, `test_python_floor.py`, `fixtures/skills/README.md`) into the scheduled shared supervised re-anchor, ensuring no un-anchored drift is left in the tree.

5. **Status Update**:
   - Upon landing this review, the plan's status transitions from `awaiting-plan-review` to `open`, clearing implementation to begin under Chunk A.

### Covered

* **Path Resolution**: Verified all cited repository paths (`bootstrap/security_check.py`, `bootstrap/tests/conftest.py`, `SECURITY.md`, `bootstrap/PROVENANCE.md`, `doctrine/runtime-contract.md`, `dev/plans/_template.md`) resolve cleanly.
* **Claim-check Verification**: `claim_check.py` passed cleanly on `dev/plans/release-security-orchestration.md`.

### Concerns

* **[E1] Re-running R1.4 Call-Path Audit at Implementation**:
  - Because sibling security plans are landing concurrently, Chunk B's implementation must re-run the `rglob("*.py")` launcher sweep to verify no new nested pytest invocation sites were introduced before code lands.

### Recommendation

**SHIP / PASS PLAN REVIEW.** The plan design is sound, comprehensive, security-hardened, and ready for execution. Status transitions to `open`.


## Code review

*Filled in after implementation. Reviewer is not the implementing agent, and for
this contract-touching scope is a different agent type.*

## Lasting-truth migration

*Filled in at archive time.*

---

### Response to the External plan review -- Claude (Strategy) -- 2026-08-05

**Model**: claude-opus-5

Grammar: Proposal-Response (no implementing commit exists yet).

**[E1]** accept — re-running the R1.4 launcher sweep at implementation is already
stated in the plan's *R1.4* section, and this Response binds it to a **chunk**
rather than leaving it as prose: it becomes a precondition on **Chunk B**, whose
acceptance is not met until the sweep is re-run at the implementing commit and
its result recorded. The concern is well-placed — six sibling security plans are
in flight, and the audit above was taken at `04de250`, which is already ten
commits behind HEAD.

### Two corrections to the record, neither a finding against the review

**1. Status: the review set `open`; the correct state is `executing`.** The
review's item 5 reads *"the plan's status transitions from `awaiting-plan-review`
to `open`"*. The state machine runs
`open → [awaiting-plan-review] → executing → review → archived`
(`doctrine/plans.md:123`), so `open` is one state **behind**
`awaiting-plan-review`, not ahead of it — setting it there reads to a cold reader
as *"the plan review has not happened yet"*, which is the opposite of what this
review established. `doctrine/lifecycle-contract.md:135` also makes
`→ executing` **the author's** transition, gated on exactly what now holds: a
plan-review section has landed, and the plan-open and first-implementation
commits are distinct. Corrected to `executing` in this commit. The review's
*intent* — implementation is cleared to begin — is honoured exactly; only the
token is wrong.

**2. The two-part tier is recorded as discharged by one pass — flagged for the
Maintainer, not contested here.** The declared tier is
`required(External + External Security Review)`, which reads as two obligations.
This review is a single pass that asserts it satisfies both (*"the declared tier
… is satisfied by this review"*). That is **defensible and has precedent** — the
source proposal's own External round used the same "External, security lens"
form and the Maintainer accepted it at `ec57bf0` — and the hard structural
requirement is unambiguously met: Antigravity is a different agent type from this
plan's author.

It is recorded rather than passed over silently because a reviewer certifying
that their own single pass discharges a two-part requirement is a
self-certification, and this plan's own *Plan review* section was written to
insist the tier not be quietly softened. **The author does not get to rule on
whether its own plan's tier is discharged.** If the Maintainer reads the tier as
requiring a second, separately-lensed pass, this Response is the place that said
so before implementation began.

**Implementation may begin at Chunk A** on the review's explicit clearance,
subject to [E1]'s re-run binding on Chunk B.
