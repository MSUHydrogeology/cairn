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

### [E1] discharged, and the audit method corrected -- 2026-08-05

**[E1] asked for the `rglob("*.py")` launcher sweep to be re-run before code
lands, because sibling security plans are landing concurrently. Re-run at
`67133c4`. Result: no new nested pytest launcher site exists.** The review's
characterization holds exactly:

| site | kind | env |
|---|---|---|
| `scripts/quality_gate.py` — argv literal `:158`, `subprocess.run` `:164` | the **single executable** nested pytest launcher | **inherited** (no `env=` kwarg) |
| `bootstrap/tests/_gate_manifest.py:202` | collection-only (`--collect-only`) | explicitly set |

**The audit method needs stating, because two obvious ways to run it both fail.**
This is the sharpening [E1] earns, and it was found by running the sweep rather
than by reasoning about it.

* **A per-call-node AST sweep gets a false negative on the site that matters.**
  Walk every `subprocess.{run,Popen,call,check_call,check_output}` call and test
  whether the call contains a `"pytest"` literal: `quality_gate.py` is **missed
  entirely**. Its argv is bound to `cmd` at `:157-161` and the call at `:164`
  unparses to `subprocess.run(cmd, cwd=..., capture_output=True, text=True)` —
  no `pytest` string anywhere in the call node. Measured: that sweep reports
  **1** launcher, and it is the collection-only one. A method that finds only
  the harmless site and misses the executable one is worse than no method,
  because it reports success.
* **A file-level sweep over-reports.** Broadening to "any launcher in a file
  containing a `"pytest"` literal" finds the real site, and also
  `_gate_manifest.py:285` and `:300`, both `env=INHERITED` — **both are `git`
  calls** (`git merge-base --is-ancestor`, `git show`) in a file that happens to
  contain a `pytest` literal elsewhere. Two false positives against one true
  find.
* **So Chunk B's re-run must classify, not just count.** For each launcher site
  report (a) whether the argv is direct or variable-bound, and (b) whether the
  resolved argv actually names `pytest`. Chunk C2's decisive regression gate
  targets the *executable* path, so a sweep that cannot distinguish an executable
  launcher from a collection-only one or from a git call cannot establish C2's
  premise.

Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13),
`as_of` 2026-08-05 at `67133c4`.

### A publication gap in the gate trust root, found while auditing -- 2026-08-05

Out of this plan's declared scope, recorded here because this plan owns the
release security bar and the finding is a release-trust-bar fact.

**`refs/cairn/gate-anchor` exists locally and does not exist on `origin`.**
Measured: `git for-each-ref refs/cairn/` reports one ref, `gate-anchor` at
`e45e1fc` (which matches the trust root `dev/PLANNING.md` records for
`gate-reanchor-preflight`). `git ls-remote origin 'refs/cairn/*'` returns
**nothing**.

**No ordinary push will ever publish it.** Git's default refspec covers
`refs/heads/*`; `refs/cairn/*` is skipped by `git push`, by `git push origin
master`, by `git push --all` (heads only) and by `--tags` (tags only). There is
no configured `remote.origin.push` and no `push.default` to override that.
Publishing it takes an explicit refspec:

```
git push origin refs/cairn/gate-anchor:refs/cairn/gate-anchor
```

**And nothing tells anyone to do that.** `bootstrap/REANCHOR_RUNBOOK.md` contains
**zero occurrences of `git push`**. It documents advancing the anchor locally via
`git update-ref` and requires *"local write access to `refs/cairn/gate-anchor`
itself"*, but says nothing about publishing the ref or about a collaborator
fetching it — and a fetch needs its own refspec too. The same applies to
`refs/cairn/gate-authorization`, which the runbook resolves `A` from and which is
not present locally at all right now (expected between ceremonies, same
publication problem when it is).

Consequence, stated plainly: **the differential-oracle gate's trust root is
single-machine by construction.** A fresh clone has no anchor. If this `.git` is
lost the anchor is gone, and re-establishing it is a Maintainer ceremony under a
runbook that does not mention publication. That is a gap in the runbook, not a
defect in the gate — and it is exactly the class of "named trigger that does not
govern" that `AGENTS.md` requires be opened and checked rather than assumed.

**Not fixed here.** The runbook is a ceremony document and the anchor is an
executable trust root; changing either takes its own scope. Routed to
`dev/PLANNING.md` at the next serialization point.

## Plan review -- Codex (External Security Review) -- 2026-08-05

**Tier**: External

**Findings**: raised

**Recommendation: REVISE.** Antigravity's pass satisfies the structurally
independent External tier, but it does not perform the required six-class/input-
trust triage. This pass supplies the owed External Security Review. The Git and
release-token designs are fit for implementation; Chunk D needs two narrow
fail-closed rules added to its executable contract first.

### Execution evidence

At `9bf3524`, a variable-aware AST sweep under Python 3.13.13 found exactly two
pytest subprocesses after resolving their argv:

* `scripts/quality_gate.py:164` -- **variable-bound, executable**, inherited
  environment;
* `bootstrap/tests/_gate_manifest.py:202` -- **direct, collection-only**,
  `dict(os.environ, CAIRN_GATE_COLLECT_OUT=...)`.

The calls at `_gate_manifest.py:285` and `:300` are Git, confirming the recorded
file-level false positives. Sixteen focused `test_security_check.py` /
`TestSterileGitLauncher` tests passed. Real Bandit scanned 77 targets, emitted
118 findings and zero errors, and emitted no `B310`; the current release checker
still returned clean with that stale allowlist entry, so Chunk D addresses a
reproduced defect.

Two additional direct probes matter to D2: `run_bandit()` currently reports
clean for JSON `{}` with return code 0, and for
`{"errors": [], "results": []}` with return code 1. These are syntactically
parsed reports but not trustworthy clean evidence.

### Findings

**[S1 -- important, blocking] Allowlist liveness must use the activation
predicate, not every observed pair.** D2 says to derive observed `(path,
test_id)` pairs from the parsed report. The allowlist actually suppresses only
MEDIUM/HIGH findings. If a matching pair remains only as LOW, an all-results
liveness set calls the entry live even though it currently suppresses nothing;
a later severity increase silently reactivates the old exception.

Remediation: derive `live_allowlist_keys` through the exact same normalized path,
test-id, and blocking-severity predicate used by suppression. A configured key
is live only if it suppresses at least one finding in this run. Add a regression
where the matching `(path, test_id)` exists only at LOW and must be rejected as
stale. Keep the existing present, absent, and moved-path cases.

**[S2 -- important, blocking] “Successfully parsed” must mean a validated
Bandit report, not merely valid JSON.** Once D1 empties the allowlist, liveness is
vacuous. The current parser accepts `{}` as a clean report, and also accepts a
return code of 1 with empty `errors` and `results`; both were reproduced. A
Bandit failure or incompatible output can therefore become release `PASS`.

Remediation: before errors, liveness, or suppression, validate the top-level
object and required `errors`/`results` list shapes and the fields used in every
finding. Reject return-code/report contradictions, including rc=1 with no
findings. Bind these cases to D2/D3 tests. This is semantic parser validation,
not a demand for a new schema dependency.

### Six-boundary walk and input triage

* **Deserialization -- applicable.** Bandit JSON is **USER-CONTROLLED** external-
  process output. `json.loads` itself cannot execute code, but semantic shape is
  not yet validated; S2 applies. No pickle or object-construction loader is in
  the release path.
* **Subprocess invocation -- applicable.** Planned Git, Bandit,
  `check_cairn.py`, pytest, and `quality_gate.py` calls all use fixed argv and
  `shell=False`. Repository paths, scan targets, scripts, and test arguments are
  **TRUSTED-INPUT** under the accepted solo-maintainer/trusted-contributor model.
  Git/Bandit/Python binaries and packages are operator-toolchain
  **TRUSTED-INPUT**; the plan accurately does not authenticate that process.
* **Parsing -- applicable.** Git status/HEAD output and Bandit JSON cross process
  boundaries. Git output is constrained by the sterile launcher and used for
  emptiness/full-object-id checks. Bandit output is **USER-CONTROLLED** parser
  input and needs S1-S2. The allowlist and its rationales are repo-controlled
  **TRUSTED-INPUT** policy.
* **File/path handling -- applicable.** `CAIRN_ROOT`, phase scripts, test roots,
  and derived Bandit targets are repo-controlled **TRUSTED-INPUT**. A1's exact
  checkout-root check, tracked/untracked cleanliness, resolvable full HEAD, and
  postflight equality cover the intended local candidate. Implementation must
  preserve the existing trust-root launcher's exact-root and no-upward-discovery
  behavior.
* **Network I/O -- no direct release-orchestrator call.** Bandit, Git state
  checks, and the default Cairn checks are local. Pytest executes
  **TRUSTED-INPUT** repository code with ambient host access, so transitive
  network activity is possible and uncontained. That is correctly included in
  the accepted “does not contain code executed by pytest” residual and expires
  with untrusted contributions.
* **Credentials/environment -- applicable.** Ambient `GIT_*` values are
  **USER-CONTROLLED** process input; A2 correctly requires dropping every such
  key and disabling execution-bearing config through the existing sterile-Git
  pattern. `PATH`, the interpreter, HOME, and any credentials inherited by test
  children remain operator-toolchain **TRUSTED-INPUT** under this ceremony. The
  release token is not a credential: it is a fixed mode bit. The parent
  overwrites it exactly, the executable nested pytest call inherits it, and C2
  tests the governing path. Repository tests can mutate their own process or
  environment, but that is accurately covered by the no-containment/no-process-
  authentication residual and its named expiry.

### Ruling

The accepted residuals are not misdescribed. In particular, the token proves a
mode reached a cooperative child; it does not authenticate the child, protect
ambient secrets, or contain test code. A2 must reuse the full sterile pattern --
drop all `GIT_*` keys and pin relevant execution-bearing config -- rather than
turning the plan's “etc.” into a finite denylist.

After S1-S2 are bound into Chunk D and its regressions, this Security Review has
no further design objection. Code review must re-run the classified launcher
sweep and execute the real C2 nested path; direct-child environment capture is
supporting evidence only.
