# A next-action vocabulary for proposals and plans

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: proposed
**Touches**: `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/agent_collaboration.md`, `doctrine/proposals.md`, `doctrine/plans.md`,
`doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`,
`dev/proposals/_template.md`, `dev/plans/_template.md`, their
`templates/core/dev/` twins, `tools/lifecycle_planner.py`,
`templates/skills/_lib/lifecycle_planner.py`,
`tools/_lifecycle_metrics/extract.py`, lifecycle tests, active lifecycle
artifacts, and `CHANGELOG.md`
**Related**: [`review-efficient-lifecycle`](2026-08-10-codex-review-efficient-lifecycle.md),
[`claim-check-exemption-hygiene`](2026-08-10-codex-claim-check-exemption-hygiene.md),
and [`code-review-blindness`](2026-08-10-claude-code-review-blindness.md)
**Amends**: `review-efficient-lifecycle`
**Plan review**: required(**External**) -- this changes Cairn's governing
lifecycle, its shipped templates, and executable transition enforcement. It
joins the eventual `review-efficient-lifecycle` plan rather than opening a
second implementation unit.

## Context

Cairn's proposal vocabulary is better than its plan vocabulary, but neither
consistently answers the operational question a scientist or agent asks when
opening an artifact: **what happens next, and who owns it?**

Proposal states mostly name completed events:

```text
proposed -> reviewed -> revised -> accepted / rejected / superseded
```

`reviewed` does not say whether the author owes a revision or the Maintainer
owes a Decision. `revised` does not say whether another required review remains
or whether the proposal is ready for Decision.

Plan states have the same problem more acutely:

```text
open -> [awaiting-plan-review] -> executing -> review -> archived
```

`open` persists across implementation, code review, correction, and archive
preparation in practice. All seven non-template files directly under
`dev/plans/` carry `**Status**: open`, as_of 2026-08-10, even though their
records and repository commits are at different stages. The problem is already
recorded inside `release-security-bar`: its implementation register explicitly
warns that plan status was not a reliable signal after implementing commits
had landed. This is recurrence, not a single confusing label.

The accepted `review-efficient-lifecycle` proposal makes closeout and review
inputs cheaper, while `code-review-blindness` defines the prospective
Code-review verdict contract. Neither gives the lifecycle a status vocabulary
that exposes who acts next. This amendment supplies that missing state model
without adding another implementation plan.

## Proposal

Adopt one rule across both artifact families:

> **A non-terminal status names the next action or the work currently being
> performed. Appended sections record completed events.**

The proposal and plan vocabularies use the same grammar -- `awaiting-*`,
`revising-*`, `ready-to-*`, and an active work verb -- while preserving the
different jobs of deliberation and execution.

### 1. Proposal states

Replace `proposed`, `reviewed`, and `revised` with:

```text
awaiting-review
      | clear
      v
awaiting-decision -----------------> accepted / rejected / superseded
      ^                                      Maintainer
      |
awaiting-review <------ revising
      revise              author
```

The legal meanings are:

| Status | Next owner | Evidence and transition rule |
|---|---|---|
| `awaiting-review` | required reviewer | Initial status. It also follows an author's Response when another required read remains. A review that does not yet satisfy the declared tier leaves this status unchanged. |
| `revising` | proposal author | A reviewer has raised a blocking critique. The review commit selects this state; the author's append-only Response and complete current-contract revision return the proposal to `awaiting-review`. |
| `awaiting-decision` | Human Maintainer | The declared review floor is satisfied and no blocking proposal-review finding remains. A clearing reviewer selects this state. A later blocking decision-support review may return it to `revising`; an advisory decision-support review leaves it unchanged. |
| `accepted` / `rejected` / `superseded` | terminal | Existing Maintainer Decision meanings and archive timing remain unchanged. |

The status is the review disposition; no duplicate `Outcome:` field is added.
The review section still carries its reasoning, tier, author, and findings.
The reviewer who appends the review is therefore also responsible for choosing
`revising`, `awaiting-decision`, or no status change when another declared tier
is still owed.

This removes two ambiguities in the current machine. A `reviewed` proposal can
no longer hide whether a response is required, and a `revised` proposal can no
longer hide whether an independent read is still owed.

### 2. Plan states

Replace `open`, `executing`, and `review` and add explicit readiness and
correction states:

```text
awaiting-plan-review <-> revising-plan
          |
          v
ready-to-implement -> implementing -> awaiting-code-review
                                           |
                                           v
                                      revising-code
                                           |
                                           +----> awaiting-code-review

awaiting-code-review -> ready-to-archive -> archived
```

The legal meanings are:

| Status | Next owner | Evidence and transition rule |
|---|---|---|
| `awaiting-plan-review` | required plan reviewer | Initial status for a distinct-review plan. A review that does not yet satisfy the declared tier leaves it unchanged. |
| `revising-plan` | plan author | The latest plan review requires correction. After folding allowed pre-implementation edits and appending the Response, the author returns the plan to `awaiting-plan-review`; the author cannot self-clear it. |
| `ready-to-implement` | implementer | Plan review is cleared, inherited, or not required. No implementation bytes have landed yet. |
| `implementing` | implementer | Implementation or Boundary A work is active. For the accepted fast path, a plan whose opening commit also contains permitted implementation may begin here instead of recording an empty `ready-to-implement` transition. |
| `awaiting-code-review` | code reviewer | Executable and test bytes are stable and the applicable Boundary B evidence is recorded. The reviewer owns the next action. |
| `revising-code` | implementer | The latest Code review is blocking. Corrections and focused falsifiers happen here; a replacement stable evidence record returns the plan to `awaiting-code-review`. |
| `ready-to-archive` | lifecycle owner | The latest applicable Code review clears, findings and follow-ups are dispositioned, and closeout preconditions hold. No implementation work remains. |
| `archived` | terminal | Existing archive move and lasting-truth migration are complete. |

The two revision names are deliberately specific. A generic plan status of
`revising` would still force the reader to search the artifact to learn whether
the design or the implementation is being corrected.

The accepted `code-review-blindness` contract, once decided, supplies the
clearing-versus-blocking Code-review predicate. This amendment consumes that
single predicate; it does not create a second verdict parser. Until that
contract is accepted, the shared implementation plan cannot finalize the
`awaiting-code-review` transitions.

### 3. Blockers are orthogonal

Add one optional metadata line to plans:

```text
**Blocked by**: <durable condition or artifact stem>
```

Absence means no recorded external blocker. The field never changes the legal
state machine and never substitutes for a status. A plan waiting for a release,
ceremony, dependency, Maintainer ruling, or another plan remains at its true
work stage and records the external condition separately.

The field is not a general narrative status. It must name a falsifiable
condition whose resolution can be observed. Clearing it is an in-place plan
metadata edit made with the commit that resolves or records resolution of the
condition.

### 4. Status and evidence move together

Do not create empty commits merely to advance a label. The evidence-producing
commit updates the status:

* proposal opening creates `awaiting-review`;
* a proposal-review commit selects `revising` or `awaiting-decision`;
* an author Response returns `revising` to `awaiting-review`;
* plan opening selects `awaiting-plan-review`, `ready-to-implement`, or the
  permitted combined fast-path `implementing` state;
* the first implementation commit advances `ready-to-implement` to
  `implementing`;
* the stable Boundary B record advances `implementing` or `revising-code` to
  `awaiting-code-review`;
* the Code-review commit selects `revising-code` or `ready-to-archive`; and
* the archive commit advances `ready-to-archive` to `archived`.

A review that leaves the artifact correctly waiting for another required tier
does not manufacture a status transition. It remains its own review commit
because the append-only review record changed, while the functional status
correctly remains `awaiting-review` or `awaiting-plan-review`.

### 5. Executable conformance

`tools/lifecycle_planner.py` and its installed twin must validate status against
the record that makes the status true. At minimum they refuse:

* a proposal in `revising` without a latest blocking review;
* a proposal in `awaiting-decision` before its declared review floor clears or
  while a blocking review remains unanswered;
* a plan in `revising-plan` without a blocking plan-review pass;
* `ready-to-implement` or `implementing` before required plan review clears;
* `awaiting-code-review` without a valid stable evidence record;
* `revising-code` without a latest blocking Code review;
* `ready-to-archive` without a latest clearing Code review and every closeout
  precondition; and
* `archived` when the same closeout predicate would reject
  `ready-to-archive`.

The `next` command lists only evidence-compatible transitions and scaffolds the
status change in the same patch as its required record. `scan`, `next`, and the
accepted closeout command must consume shared predicates rather than implement
three interpretations of readiness.

Role names remain evidence, not authentication. Existing structural
independence and Maintainer-identity checks continue to govern reviewer and
Decision authority; this proposal does not infer authority from the status
word alone.

### 6. Migration and compatibility

Archived proposals and plans are immutable. The checker recognizes their
historical state vocabulary in place and does not request retroactive edits.
Terminal active proposals already using `accepted`, `rejected`, or
`superseded` also need no vocabulary migration.

The implementation performs one evidence-derived migration of every active,
non-terminal proposal and plan. It reads the latest applicable review,
Response, implementation-verification record, accepted review basis, and
closeout evidence, then proposes a status for human-readable inspection. It
must not translate every `open` plan to the same new state. Ambiguous records
refuse migration and name the missing evidence.

After that migration, old non-terminal values are invalid in active artifacts.
This prevents `open` from surviving forever as an accidental compatibility
escape hatch. Lifecycle metrics recognize both historical and current
vocabularies so longitudinal measurements do not erase pre-migration work.

### Documentation / doctrine surface

The governing contract belongs in `doctrine/proposals.md`,
`doctrine/plans.md`, `doctrine/lifecycle.md`, and
`doctrine/lifecycle-contract.md`. The operational summary belongs in
`AGENTS.md` and `dev/agent_collaboration.md`. Author-facing instructions belong
in both self-hosted templates and their shipped `templates/core/dev/` twins.
The tool and installed twin enforce the same contract for Cairn and adopters.

This proposal clears the doctrine-evolution rate limit through recurrence:
all seven active plans currently share one stale `open` label despite being at
different evidenced stages, and `release-security-bar` independently recorded
the same failure before this proposal was drafted. The change affects lifecycle
enforcement and is therefore high assurance under the accepted
`review-efficient-lifecycle` contract.

## Rationale

Scientists should be able to open a plan and know whether they need to find a
reviewer, wait for an implementation, answer findings, perform a ceremony, or
archive completed work. Reconstructing that answer from hundreds of lines and
several commits is avoidable process cost.

The parallel vocabulary also makes automation safer. A tool can report
"reviewer owns the next action" or "ready to archive" from an evidence-backed
state instead of guessing from the presence of a heading. That supports the
accepted lifecycle-efficiency goal without weakening independent review.

Keeping terminal proposal Decisions unchanged preserves the stable distinction
between deliberation outcome and implementation progress. Keeping blockers in
a separate field prevents a release date or Maintainer ceremony from obscuring
which engineering stage is actually complete.

## Alternatives considered

**Change plan statuses only.** Rejected. Proposal states have the same
completed-event ambiguity, especially `reviewed` and `revised`. Two artifact
families should teach one mental model.

**Retain the existing words and add `Next action:`.** Rejected. Two mutable
fields can disagree, and every consumer must decide which one is authoritative.
The status should do its one job directly.

**Use one universal state list for both artifact types.** Rejected. Proposals
deliberate toward a Maintainer Decision; plans execute toward reviewed and
archived bytes. Shared grammar is useful, but identical nouns would conceal
their different boundaries.

**Use a single `revising` plan state.** Rejected. Plans have independent
pre-implementation and post-Code-review correction loops. Naming the object
being revised is worth two extra vocabulary entries.

**Add `blocked` states for each stage.** Rejected. Blocking cause and work stage
are orthogonal. A separate, optional `Blocked by` field keeps the state machine
finite and the obstacle explicit.

**Infer status dynamically and remove the field.** Rejected. Some readiness
claims remain human-owned, and a recorded status is useful in plain Markdown,
Git diffs, and environments without the planner tool. The checker validates the
claim; it does not become the only way to read it.

**Do nothing.** Rejected. A status vocabulary that is consistently ignored is
not a lightweight process; it is misleading metadata.

The Maintainer's preference during drafting was: "We need a better vocabulary
for plan statuses" and, after seeing the parallel proposal model, "Excellent,
please propose that nice, parallel refinement to the vocabulary." These shape
this draft but are not a lifecycle Decision.

## Evidence / verification plan

### Author-accounting -- invariants, failure modes, edge cases

| Claim | Enforcer |
|---|---|
| Every active non-terminal artifact uses the new vocabulary | lifecycle-planner `scan` plus corpus tests |
| Every actionable status identifies one next owner or active work phase | closed state tables in doctrine and `_legal_transitions` tests |
| Readiness states cannot outrun their evidence | shared conformance predicates exercised through both `scan` and `next` |
| A blocking review cannot produce a clearing readiness state | prospective proposal/plan fixtures and the `code-review-blindness` predicate |
| Archived history remains immutable and readable | legacy archived fixtures plus a no-migration assertion |
| Self-hosted and adopter behavior agree | byte-identity test for lifecycle-planner twins and template drift checks |

Failure is closed for unknown active statuses, unsupported transitions, and
status/evidence contradictions. Archived legacy vocabulary is an intentional,
path-bounded compatibility allowance. An ambiguous active artifact refuses
automatic migration and remains visible for manual classification.

Edge cases include a review below the still-required tier, multiple review
rounds on one date, a clearing review with non-blocking observations, a
blocking decision-support review, plan review correction before any code,
repeated Code-review correction, a plan opened with implementation under the
accepted fast path, external blocking after readiness, and an archive carrying
historical vocabulary.

No new public entry point is added. Existing public paths are
`tools/lifecycle_planner.py scan` and `next`, mapped to
[`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py).
The accepted `tools/lifecycle.py closeout` path will be mapped in the shared
implementation plan when that proposed command exists.

Known omission: the `Blocked by` field records a condition but cannot prove the
condition is true or resolved. It is operator-visible coordination metadata,
not an authorization gate.

#### Security preflight -- five questions, answered in writing

N/A: this changes lifecycle classification and validation but adds, moves, and
widens no trust boundary. It does not parse untrusted execution inputs, invoke
subprocesses, handle credentials, or grant authority. Existing identity checks
remain structurally advisory rather than authentication.

### Tests required

Extend [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py)
to cover every legal transition, every evidence contradiction listed above,
multi-tier no-op review transitions, both revision loops, fast-path opening,
and archived legacy compatibility.

Extend lifecycle CLI and transition-lint tests where they currently assume
`open`, `executing`, or `review`. Add a corpus test that rejects every old
non-terminal status directly under active proposal and plan directories after
migration. Retain byte identity between `tools/lifecycle_planner.py` and
`templates/skills/_lib/lifecycle_planner.py`.

The implementation plan must map and run the affected lifecycle, transition,
template, and metrics tests under the canonical Python 3.13 interpreter. The
full Boundary B suite remains the final integration record; this proposal does
not create a special reduced verification rule for its own enforcement.

### Examples / smoke checks

Run `tools/lifecycle_planner.py scan` over the migrated Cairn tree and show no
old active non-terminal status remains. Exercise `next` once through a clearing
path and once through each revision loop using temporary fixtures. Run
`scripts/check_cairn.py` and `scripts/link_check.py` for doctrine/template
drift and path integrity.

Documentation delivery is the governing doctrine, operational summaries,
author templates, and `CHANGELOG.md` release note named under the doctrine
surface. No runnable scientific example changes; example-gallery execution is
N/A because the proposal changes only lifecycle records and tooling.

## Signals the change is wrong

* A reader still needs to inspect history to know who acts next. Recovery:
  revise the state names or split the ambiguous state before implementation.
* `scan`, `next`, and closeout disagree about a readiness state. Recovery:
  stop the migration and consolidate the predicate before shipping.
* An archived artifact must be edited to make the new checker pass. Recovery:
  narrow or correct the legacy compatibility rule.
* A no-op status transition is required merely because another declared review
  tier landed. Recovery: keep the functional waiting state and record only the
  append-only review event.
* Active artifacts can retain `open`, `reviewed`, `revised`, `executing`, or
  `review` indefinitely through grandfathering. Recovery: restrict legacy
  vocabulary to archived history and terminal Decisions.
* The migration assigns one status to every active plan without inspecting its
  evidence. Recovery: refuse the migration and re-derive each artifact.
* The additional vocabulary creates more Maintainer prompts. Recovery: keep
  routine status selection with authors and reviewers; only
  `awaiting-decision` and existing ceremonies belong to the Maintainer.


## Review -- Claude -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)
**Tier**: External, different agent type from the author
**Reviewed commit**: `b63691eac92becc53e26ecf00650c1ee7ba2497d`
**Target**: the complete proposal
**Prior findings**: none
**Assurance path**: high-assurance (lifecycle enforcement, shipped templates)
**Verdict: REVISE.** The state model is right and the diagnosis reproduces
exactly. The change-surface accounting is incomplete, and the gap is not
cosmetic: as written, this proposal silently disables a shipped lint's
detection in a file its `Touches` list does not name.

### Steelman

**Every factual claim reproduces.** All seven non-template files under
`dev/plans/` carry `**Status**: open` -- api-web-security-modules,
fork-advisory-semantics, portable-security-sweeps, release-security-bar,
security-preflight-checklist, security-verification-activation,
stage-commit-patterns -- while sitting at visibly different evidenced stages.
`release-security-bar.md:332` independently records the failure before this
proposal existed: *"plan status is not a reliable signal this week."*
`doctrine/lifecycle-contract.md` exists as cited. The recurrence argument for
the doctrine rate-limit is properly earned, not asserted.

**Three design calls are right and non-obvious.** Keeping `Blocked by`
orthogonal to the state machine, so a release date cannot obscure an
engineering stage. Rejecting a parallel `Next action:` field because two mutable
fields can disagree. And §4's rule that status moves with evidence rather than
in empty label-advancing commits -- including the subtle corollary that a review
satisfying only part of a declared floor must *not* manufacture a transition.

**Splitting `revising-plan` from `revising-code`** is correct for the stated
reason: the reader should not have to search the artifact to learn which loop
is running.

### [C1] HIGH -- the new vocabulary silently disables transition-lint's shape-(b) detection

`scripts/transition_lint.py:234` carries a fourth status vocabulary the proposal
does not mention:

```python
_OPEN_STATUSES = ("proposed", "open", "awaiting-plan-review")
```

consumed at `:549` as `if declared not in _OPEN_STATUSES: continue` -- a
**fail-open**. Any unrecognised status skips shape-(b) detection silently.

I built a synthetic repository, committed a lifecycle file carrying a baked-in
review (`**Steelman**`, `[R1]`, `**Covered**`, dated heading), and varied only
the `**Status**:` line:

```text
CURRENT vocabulary (control)
  proposed              -> ['b']
  open                  -> ['b']
  awaiting-plan-review  -> ['b']
PROPOSED vocabulary
  awaiting-review       -> []   DETECTION LOST
  revising              -> []   DETECTION LOST
  ready-to-implement    -> []   DETECTION LOST
  implementing          -> []   DETECTION LOST
  revising-plan         -> []   DETECTION LOST
```

Shape (b) is the detector for the `17b7e5c` incident class -- an open commit
whose added file already carries a real review. After this migration it would
fire on nothing.

**And nothing would report the loss.** transition-lint's corpus tier is
SHA-pinned to history written in the old vocabulary, so all 40 of its nodes stay
green while live detection is dead. That is precisely the failure `AGENTS.md`
names: *a tool that returns success without testing the claimed property is a
worse defect than no tool, because it is silent.*

The coupling is already documented in the tree --
`bootstrap/tests/test_transition_lint.py:631` carries perturbation **C6** on
`_OPEN_STATUSES` -- so this is a surface the repository knows is status-sensitive.

**Required satisfier.** Add `scripts/transition_lint.py` to `Touches`; extend
`_OPEN_STATUSES` in the *same commit* as the vocabulary change, never after; and
add a node asserting that every new opening status is shape-(b) detectable, with
the fixture above as its basis. A corpus-only test cannot pin this, so the node
must be synthetic.

### [C2] HIGH -- three of the surfaces to be edited are frozen, and the proposal never says so

Checked against the live gate manifest (182 frozen paths, `as_of 2026-08-10`):

| surface | frozen? | in `Touches`? |
|---|---|---|
| `tools/lifecycle_planner.py` | no | yes |
| `templates/skills/_lib/lifecycle_planner.py` | no | yes |
| `tools/_lifecycle_metrics/extract.py` | no | yes |
| `templates/modules/default-on/_lifecycle_metrics/extract.py` | **FROZEN** | no |
| `bootstrap/tests/test_lifecycle_contract.py` | **FROZEN** | implied by *Tests required* |
| `scripts/transition_lint.py` | **FROZEN** | **no** |

`AGENTS.md` treats the gate manifest as a byte-level-stable install contract and
routes changes to it through a Maintainer-run ceremony. The proposal's `Touches`
list, `Documentation / doctrine surface`, and verification plan name no gate
interaction at all -- yet its own *Tests required* section mandates extending a
frozen test file.

I confirmed frozen-set membership directly; I did **not** run the gate to
observe the HOLD, so the exact ceremony cost is for the plan to establish.

**Required satisfier.** Name the frozen surfaces, state the re-anchor obligation
and who performs it, and sequence it. A lifecycle-vocabulary change that
discovers its trust-ceremony cost mid-implementation will either stall or route
around the gate.

### [C3] MEDIUM -- five hard-coded vocabularies, and one is already wrong

```text
tools/lifecycle_planner.py:769,771                       _PROPOSAL_STATES, _PLAN_STATES
templates/skills/_lib/lifecycle_planner.py:769,771       (byte-identical twin)
tools/_lifecycle_metrics/extract.py:96                   _PLAN_STATUS_ENUM
templates/modules/default-on/_lifecycle_metrics/extract.py:96   (twin, frozen)
scripts/transition_lint.py:234                           _OPEN_STATUSES  (frozen)
```

Note that `_PLAN_STATUS_ENUM = ('open', 'executing', 'review', 'archived')`
**already omits `awaiting-plan-review`** -- a pre-existing defect this migration
would inherit and then double, since §6 requires metrics to carry both the
historical and the current vocabulary.

**Required satisfier.** Do not edit five tuples. Establish one vocabulary
module as the single source and have every consumer import it, with a test that
fails when any consumer re-declares the list locally. Otherwise the sixth
consumer -- and there will be one -- diverges silently exactly as
`_OPEN_STATUSES` and `_PLAN_STATUS_ENUM` already have.

### [C4] MEDIUM -- the reviewer is handed a decision the record does not support

§1 makes the *reviewer* select `awaiting-decision`, valid only when *"the
declared review floor is satisfied."* Two active artifacts declare a two-part
floor today (`git-native-security-foundations`,
`api-web-security-modules`: `External + External Security Review`), so the first
reviewer must decide whether one pass discharges one tier or both.

**That question is explicitly unresolved in the record.**
`dev/plans/archive/release-security-orchestration.md:843` states the disposition
there *"does not rule on whether the two-part"* tier is discharged, and `:415`
routes it to the Maintainer. This proposal makes an open question load-bearing on
every review commit and resolves it by silence.

Secondary, and real in this repository: `Status:` is a single mutable field that
two concurrently-landing reviewers would both write. Several sessions have been
committing to this tree in parallel today.

**Required satisfier.** Either resolve the multi-tier rule inside this proposal
(a reviewer may select `awaiting-decision` only when their own pass satisfies the
*last* outstanding declared tier, and otherwise leaves the status unchanged --
which §1 already half-states), or declare it a precondition and name who rules.
State the concurrent-write disposition explicitly: last-writer-wins is
acceptable if said out loud.

### [C5] LOW -- `ready-to-archive` names an owner Cairn does not have

The `Next owner` column reads **"lifecycle owner."** That string appears nowhere
in `dev/agent_collaboration.md`, `doctrine/`, or `AGENTS.md`. The one state whose
entire purpose is naming who acts next names an actor with no roster entry. Use a
rostered role, or define the role in the same change.

### [C6] LOW -- the migration must handle artifacts in flight, including this one

This proposal carries `**Status**: proposed`, which §6 makes invalid for active
artifacts after migration. Not a design defect -- but the migration will run
while several proposals sit mid-review, and §6's evidence-derived classifier has
to place a proposal whose only review is the one arriving in the same window.
Name that case; it is the migration's most likely refusal.

### Coverage and recommendation

**Covered**, by execution: the seven-plan `Status: open` corpus;
`release-security-bar:332`; existence of `doctrine/lifecycle-contract.md`; the
shape-(b) detection matrix across six status values with a working control
(synthetic repositories, real `transition_lint.scan`); `_OPEN_STATUSES` and its
fail-open consumption at `:549`; frozen-set membership of six candidate surfaces
against the live 182-path manifest; all five hard-coded vocabularies and the
`awaiting-plan-review` omission in `_PLAN_STATUS_ENUM`; `_PLAN_STATES` /
`_PROPOSAL_STATES` and `_legal_transitions` at `:769-794`; the unresolved
two-part tier question at `release-security-orchestration.md:415`, `:843`; the
absence of "lifecycle owner" from the roster; the multi-tier declarations in
active artifacts.

**Not covered / low confidence.** I did not run the gate to observe a HOLD on a
frozen edit, so [C2]'s ceremony cost is asserted from manifest membership plus
`AGENTS.md`, not from execution. I did not exercise `next` or `scan` against
fixtures in the new vocabulary -- no implementation exists. I did not evaluate
whether the eight plan states are the *right* eight, only that they are
well-formed and that their transitions are stated; a reader-comprehension claim
is not something I can falsify from inside the tree. I did not check adopter
lockfile or upgrade-path consequences of a changed installed twin. One agent
type, one host; the declared `required(**External**)` plan tier is untouched by
this proposal review.

**Second-round recommendation: recommended, narrow.** [C1] and [C2] are
change-surface omissions rather than design errors, and [C3]'s single-source fix
is the durable repair for both. Re-read only the corrected surface list, the
single-vocabulary mechanism, and the multi-tier rule; the state model, the
`Blocked by` orthogonality, and the evidence-moves-with-status rule do not need
another pass.

**A note on what [C1] means for the parent plan.** This proposal, the accepted
`review-efficient-lifecycle`, and the revised `code-review-blindness` all edit
the same predicates and share one plan. Three amendments converging on
`lifecycle_planner.py` while a fourth vocabulary sits frozen in
`transition_lint.py` is precisely the condition under which a silent regression
ships. Whatever else the plan does, it should establish the single vocabulary
source ([C3]) **first**, before any of the three lands its own edits.
