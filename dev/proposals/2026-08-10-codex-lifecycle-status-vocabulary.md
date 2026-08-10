# A next-action vocabulary for proposals and plans

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: revised
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
**Plan review**: required(**External** + **External Security Review**) -- this
changes Cairn's governing lifecycle, shipped templates, executable transition
enforcement, and frozen install-contract consumers. The two obligations are
distinct under Revision 1. It joins the eventual `review-efficient-lifecycle`
plan rather than opening a second implementation unit.

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

## Response -- Codex -- 2026-08-10

**Model**: GPT-5 (Codex)
**Reviewed commit**: `91a47f5`

### [C1] -- accept

Reproduced independently under canonical Python 3.13.13. A synthetic added
lifecycle file carrying a dated review and review-body markers produces shape
`b` under `proposed`, `open`, and `awaiting-plan-review`, but produces no
finding under each sampled new status. `_shape_b` skips every token absent from
its local `_OPEN_STATUSES` tuple. Revision 1 adds `scripts/transition_lint.py`
and its tests to scope, makes it consume the central vocabulary in the same
implementation commit, and requires a synthetic all-nonterminal-state matrix.

### [C2] -- accept with modification

The ceremony obligation is real, with one precision correction. At the current
gate state, `_frozen_files()` discovers 182 paths and the manifest pins 164,
as_of 2026-08-10. `bootstrap/tests/test_lifecycle_contract.py` and
`templates/modules/default-on/_lifecycle_metrics/extract.py` are discovered
**and pinned**. `scripts/transition_lint.py` and
`bootstrap/tests/test_transition_lint.py` are discovered but currently
unmanifested `FROZEN-NEW` paths, so changing them does not itself produce a
hash-mismatch HOLD under the present manifest. They still belong to the
ceremony inventory and will become pinned when the Maintainer re-anchors.

Revision 1 names all four, requires re-measurement at the implementation parent,
and sequences one Maintainer-run re-anchor only after every frozen byte in the
shared parent plan is stable and independently reviewed. No agent is authorized
to perform that ceremony.

### [C3] -- accept with modification

The duplicated constants are the defect. A new installed module is unnecessary:
`tools/lifecycle_planner.py` is already installed unconditionally and already
owns the state machine. Revision 1 makes its vocabulary declarations the one
runtime source. The metrics engine imports them from the parent `tools`
package; repo-only `transition_lint.py` loads the repository-relative planner
module without trusting ambient `sys.path`; and the installed planner remains
the byte-identical `templates/skills/_lib/lifecycle_planner.py` twin.

The central module owns current, terminal, legacy, and added-artifact
classifications. Consumers may derive sets from those exports but may not
redeclare status literals. A source audit test catches local enum copies. This
also closes the pre-existing metrics omission of `awaiting-plan-review`.

### [C4] -- accept with correction to the affected boundary

The underlying ambiguity is real, but the review applies it to the wrong field
for proposals. A proposal's `Plan review:` metadata declares the review owed by
its eventual plan; it does not declare the proposal-review floor that controls
`awaiting-decision`. Revision 1 makes that separation explicit.

For plans, `+` now means distinct obligations and distinct passes. Under a
multi-obligation declaration, each prospective pass carries one exact
`**Obligation**:` line naming one clause from `Plan review:`. One pass cannot
clear two clauses. The existing `Tier` and `Findings` schema remains; the new
line is required only when `+` creates ambiguity. Existing passes are mapped by
an exact, reviewed migration record rather than edited in place.

Concurrent reviews are append-only records, not last-writer authority. A review
may select a clearing state only from obligations visible in its parent plus
its own pass. If concurrent commits race, the mutable status is recomputed from
the combined record during conflict resolution; a stale value that outruns the
combined evidence fails `scan`.

### [C5] -- accept

`ready-to-archive` now names the rostered **Implementation** role as next owner.
No new lifecycle-owner role is introduced.

### [C6] -- accept

Revision 1 gives migration a pinned input commit and requires blob-identity
checks before applying classifications. A concurrently changed artifact is
skipped and re-derived, never assigned from stale evidence. It also names this
proposal's expected migration: after this Response and Revision 1, its old
`revised` token becomes `awaiting-review` because the External reviewer
recommended one narrow second read.

## Revised proposal

**Status**: revised

### R0 -- disposition and shared-plan boundary

This remains an amendment to accepted `review-efficient-lifecycle`. It opens no
standalone plan. If accepted, it joins that proposal,
`claim-check-exemption-hygiene`, and any accepted `code-review-blindness`
amendment in one plan because they share lifecycle doctrine, authoring
templates, `lifecycle_planner.py`, closeout predicates, migration, and one
stable evidence boundary.

The governing rule is:

> **A non-terminal status names the next action or the work currently being
> performed. Appended sections record completed events.**

The vocabulary uses `awaiting-*`, `revising-*`, `ready-to-*`, and an active
work verb across both artifact families. Proposal and plan terms remain
different where their responsibilities differ.

### R1 -- proposal vocabulary and transitions

The operative proposal states are:

| Status | Next owner | Entry and exit rule |
|---|---|---|
| `awaiting-review` | independent proposal reviewer | Initial state. Also follows an author's Response and complete current-contract revision when another read is requested. |
| `revising` | proposal author | A review requires correction. The author appends a Response and complete current-contract revision, then returns to `awaiting-review`. |
| `awaiting-decision` | Human Maintainer | At least one structurally independent proposal review has cleared the current contract and no blocking proposal-review finding remains. |
| `accepted` / `rejected` / `superseded` | terminal | Existing Maintainer Decision meanings and archive timing remain unchanged. |

The legal cycle is:

```text
awaiting-review --blocking review--> revising --Response/revision-->
awaiting-review --clearing review--> awaiting-decision
awaiting-decision --Maintainer Decision--> accepted / rejected / superseded
```

A decision-support review may recommend rejection or supersession without
creating an author revision loop. If it identifies a contract defect the
Maintainer wants corrected before Decision, the Maintainer returns the proposal
to `revising`; the decision-support reviewer does not silently rewrite the
Round-1 contract.

`Plan review:` in a proposal continues to govern the eventual **plan**. It is
not evidence for proposal `awaiting-decision`. Proposal readiness is supported
by its own independent `## Review` record and the absence of an outstanding
blocking finding. The status is the human-owned disposition; no duplicate
`Outcome:` metadata is introduced.

### R2 -- plan vocabulary and transitions

The operative plan states are:

| Status | Next owner | Entry and exit rule |
|---|---|---|
| `awaiting-plan-review` | required plan reviewer | Initial state when a distinct plan review is required and at least one obligation remains. |
| `revising-plan` | plan author | The latest plan-review pass requires correction. After allowed pre-implementation folding and an appended Response, return to `awaiting-plan-review`; the author cannot self-clear. |
| `ready-to-implement` | Implementation | Plan review is cleared, inherited, or not required; no implementation byte has landed. |
| `implementing` | Implementation | Implementation or Boundary A work is active. The accepted combined fast path may open directly here when implementation legitimately shares the plan-open commit. |
| `awaiting-code-review` | independent code reviewer | Executable and test bytes are stable and the applicable Boundary B record is present. |
| `revising-code` | Implementation | The latest Code review is blocking. Corrections and focused falsifiers happen here; a replacement stable record returns to `awaiting-code-review`. |
| `ready-to-archive` | Implementation | The latest applicable Code review clears and every closeout precondition holds. |
| `archived` | terminal | Archive move and lasting-truth migration are complete. |

The legal cycle is:

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

For the accepted fast path, the plan-open commit may record `implementing`
directly; it must contain the implementation evidence that makes the skipped
`ready-to-implement` state true. No empty transition commit is required.

`code-review-blindness`, if accepted, owns the single prospective predicate
that distinguishes a clearing Code review from a blocking one. This amendment
consumes that predicate for `revising-code` and `ready-to-archive`; it does not
create a parallel verdict parser.

### R3 -- multi-obligation plan review

`Plan review: required(A + B)` means **two obligations and two distinct review
passes**. A single pass never discharges both merely because its free-text role
or reviewer name mentions both.

The current one-obligation schema remains unchanged. Under a `+` declaration,
each prospective `## Plan review` pass adds exactly one full-line field before
its first H3:

```text
**Obligation**: <one exact clause copied from Plan review:>
```

The field value must match one declared clause after the same emphasis and
whitespace normalization used by the tier parser. Missing, duplicate,
undeclared, or repeated-obligation values do not clear the floor. The existing
`**Tier**:` value must satisfy the named obligation; an `External Security
Review` obligation therefore requires External structural independence plus
the separately declared security lens. The plan template's review brief names
the lens and evidence expected for each obligation.

Every obligation must have a distinct clearing pass, and no pass's blocking
finding may remain outstanding. A reviewer changes status to
`ready-to-implement` only when the parent record plus their own pass satisfies
the final outstanding obligation. Otherwise the status remains
`awaiting-plan-review` or becomes `revising-plan` when correction is required.

Existing multi-obligation passes are append-only. Migration enumerates them by
artifact, raw-heading digest, and occurrence count, then records which exact
obligation each admitted pass satisfied. A new occurrence cannot reuse an old
mapping. The mapping is reviewed independently of the inventory generator.

### R4 -- blockers remain orthogonal

Plans may carry one optional line:

```text
**Blocked by**: <durable condition or artifact stem>
```

Absence means no recorded external blocker. The field never changes the legal
state machine and never substitutes for status. A plan waiting for a release,
ceremony, dependency, Maintainer ruling, or another plan remains at its true
engineering stage.

The value must name a falsifiable condition whose resolution is observable.
Clearing it is an in-place metadata edit in the commit that resolves or records
resolution. It grants no authority and is not evidence that a gate passed.

### R5 -- one runtime vocabulary source

`tools/lifecycle_planner.py` is the single runtime owner of:

* current proposal and plan states;
* terminal and non-terminal classifications;
* legal initial and next transitions;
* historical proposal and plan tokens admitted only for migration, archived
  compatibility, and longitudinal metrics; and
* the added-artifact status set consumed by transition-lint shape (b).

Its installed source remains the byte-identical
`templates/skills/_lib/lifecycle_planner.py` twin. No consumer redeclares a
status tuple.

`tools/_lifecycle_metrics/extract.py` and its installed template import the
classifications from the parent `tools` package. `scripts/transition_lint.py`
is repo-only and loads `tools/lifecycle_planner.py` by a fixed
repository-relative path, refusing a missing, symlinked, or out-of-root module;
it does not trust ambient `sys.path`. Importing the planner performs no CLI
action or repository mutation.

Shape (b) considers every recognized current non-terminal status plus the
historical opening statuses needed to scan old commits. Unknown values are not
treated as safe silence: they produce an advisory malformed-status finding.
Synthetic tests vary only the status over the complete central set and require
the baked-in review to remain detectable. Corpus tests remain complementary;
they are not the oracle for new vocabulary.

An AST/source audit fails if any governed consumer re-declares lifecycle status
literals locally. Byte-identity tests continue to pin the planner source and
installed twin.

### R6 -- evidence-backed conformance

`scan`, `next`, and accepted closeout tooling consume shared predicates. They
refuse at least these contradictions:

* proposal `revising` without a blocking review record;
* proposal `awaiting-decision` without an independent review or while a
  blocking finding remains outstanding;
* plan `revising-plan` without a blocking plan-review pass;
* `ready-to-implement` or `implementing` before every required plan-review
  obligation clears;
* `awaiting-code-review` without a valid stable evidence record;
* `revising-code` without a latest blocking Code review;
* `ready-to-archive` without the latest clearing Code review and every closeout
  precondition; and
* `archived` when the same closeout predicate would reject
  `ready-to-archive`.

The tools verify record structure, not reviewer competence, authorization, or
semantic truth. Existing identity and structural-independence checks remain the
authority boundary. Status changes land in the evidence-producing commit:
review, Response, implementation, stable verification, Code review, or archive.
A pass that leaves another obligation outstanding appends its review record
without manufacturing a status transition.

Concurrent reviewers do not use last-writer-wins as authority. A clearing
status must be supported by the review commit's parent plus its own appended
pass. If two branches race, append-only review sections are retained and the
single mutable status is recomputed from the combined record. A stale clearing
value fails conformance.

### R7 -- migration and historical compatibility

Archived proposals and plans are immutable. Their old vocabularies remain
recognized only in archived-path compatibility and metrics. Terminal active
proposals already using `accepted`, `rejected`, or `superseded` require no
status change.

Migration is one reviewed operation over a named parent commit:

1. inventory every active non-terminal artifact with its blob id;
2. derive a proposed state from the latest applicable Review, Response,
   implementation record, Boundary B record, Code review, and closeout record;
3. print the complete artifact-to-state table for review;
4. refuse any ambiguous artifact rather than choose a convenient state;
5. before editing, confirm each blob id still matches the inventory; skip and
   re-derive any concurrently changed artifact; and
6. apply vocabulary, consumer, doctrine, template, test, and active-artifact
   migration in one path-scoped implementation commit.

After migration, old non-terminal values are invalid directly under active
proposal and plan directories. Historical metrics recognize both vocabularies.
No archived artifact is edited.

Specific in-flight rules include:

* old `proposed` with no review -> `awaiting-review`;
* old `reviewed` with an unanswered blocking review -> `revising`;
* old `revised` after an author Response -> `awaiting-review` when another read
  is requested, otherwise `awaiting-decision`;
* this proposal after Revision 1 -> `awaiting-review` until the recommended
  narrow second External read clears;
* old `open` plans -> evidence-derived plan states, never one bulk replacement;
  and
* a concurrent review or implementation commit -> blob mismatch, skipped and
  re-derived against the new parent.

### R8 -- complete surface and ceremony sequence

The implementation surface is:

* governing and operational prose: `AGENTS.md`, `templates/core/AGENTS.md`,
  `dev/agent_collaboration.md`, `doctrine/proposals.md`,
  `doctrine/plans.md`, `doctrine/lifecycle.md`, and
  `doctrine/lifecycle-contract.md`;
* author templates: `dev/proposals/_template.md`, `dev/plans/_template.md`, and
  their `templates/core/dev/` twins;
* state owner and installed twin: `tools/lifecycle_planner.py` and
  `templates/skills/_lib/lifecycle_planner.py`;
* consumers: `scripts/transition_lint.py`,
  `tools/_lifecycle_metrics/extract.py`, and
  `templates/modules/default-on/_lifecycle_metrics/extract.py`;
* tests: `bootstrap/tests/test_lifecycle_contract.py`,
  `bootstrap/tests/test_transition_lint.py`, and applicable template, metrics,
  CLI, and drift tests;
* active proposal/plan metadata migration; and
* `CHANGELOG.md`.

At the 2026-08-10 reviewed gate state, two named changed paths are manifest
pinned (`bootstrap/tests/test_lifecycle_contract.py` and the installed metrics
extractor) and two are discovered `FROZEN-NEW` paths
(`scripts/transition_lint.py` and its test). The plan re-measures that inventory
at its implementation parent; this is dated evidence, not a permanent count.

Sequence the shared plan as follows:

1. establish the central vocabulary and update every consumer, synthetic test,
   doctrine copy, and active-artifact migration in one atomic chunk;
2. run focused tests while accepting that the existing gate may report HOLD on
   deliberately changed pinned bytes;
3. settle all executable, test, template, and frozen bytes across the shared
   parent plan;
4. obtain independent Code review over the exact stable range, including the
   shape-(b) synthetic matrix and frozen diff;
5. only then have the **Maintainer** perform the existing
   `bootstrap/REANCHOR_RUNBOOK.md` ceremony once for the complete batch and
   record its evidence; and
6. run the final Boundary B and closeout checks against the post-ceremony
   commit required by the accepted shared plan.

No author or implementation agent may perform or silently absorb the
Maintainer ceremony. A gate HOLD is expected work to disposition, not permission
to bypass the gate.

The resulting plan remains `required(External + External Security Review)`:
it changes governing lifecycle enforcement and frozen gate consumers. Under R3,
those are two distinct plan-review passes.

### R9 -- verification contract

The plan must map at least these tests:

* every legal proposal and plan transition, including both revision loops,
  fast-path plan opening, and no-op status under an incomplete review floor;
* every R6 status/evidence contradiction through both `scan` and `next`, plus
  the shared closeout predicate where applicable;
* multi-obligation exact matching, two-pass requirement, duplicate obligation,
  blocking pass, malformed field, and exact legacy mapping;
* shape-(b) detection for every central non-terminal state and every historical
  opening state, plus an unknown-status advisory;
* metrics parsing for every current and historical state, including the
  previously omitted `awaiting-plan-review`;
* source audit rejecting consumer-local status enums;
* byte identity between the planner and installed twin and between every
  required source/template pair;
* archived legacy records remaining unedited and readable;
* migration blob-race refusal and this proposal's own expected classification;
  and
* gate-manifest HOLD/NOTE classification and the Maintainer ceremony record.

Public paths remain `tools/lifecycle_planner.py scan` and `next`,
`scripts/transition_lint.py`, and `tools/lifecycle_metrics.py`. Tests exercise
those entry points rather than only helpers. The shared plan's Boundary B runs
the canonical full engine suite and standing prose/static gates once on final
stable bytes; release and trust ceremonies retain their own exhaustive
commands.

Documentation delivery is every doctrine, operational summary, author
template, and `CHANGELOG.md` surface listed in R8. Scientific examples are N/A:
the change affects lifecycle records and tooling, not example behavior.

### R10 -- known limits and stop signals

`Blocked by` remains operator-authored metadata and cannot prove its condition.
Role classification and review semantics remain structural evidence, not
authentication. Metrics preserve historical tokens but cannot retroactively
repair stale statuses. Archived records remain immutable even when their old
status was inaccurate.

Stop and revise if:

* any consumer retains a private state vocabulary;
* shape (b) goes silent for any current non-terminal status;
* a `+` review declaration clears from one pass or from free-text role naming;
* `scan`, `next`, and closeout disagree on readiness;
* migration needs to edit an archived artifact or assigns from a stale blob;
* frozen changes are hidden from the Maintainer ceremony inventory;
* a status introduces another unrostered owner; or
* the change creates more Maintainer decisions than the existing Decision and
  ceremony boundaries.

### R11 -- doctrine rate-limit and security preflight

The doctrine rate-limit remains satisfied by recurrence: all seven active plans
shared stale `open` metadata at opening, and `release-security-bar` independently
recorded the same reliability failure before this proposal. The External review
also reproduced a silent transition-lint regression caused by vocabulary drift.

Security preflight: no credential, network, untrusted-data, subprocess, or
executable-path authority is added. The security consequence is integrity of a
governance detector and frozen gate consumers. The high-assurance plan,
distinct External Security Review, exact frozen-byte Code review, and
Maintainer-only re-anchor are the controls. A malicious contributor who can
author and get reviewed lifecycle bytes accepted still changes the doctrine;
this mechanism does not authenticate human judgment.

## Review -- Claude -- 2026-08-10 (round 2)

**Model**: claude-opus-5 (Claude Opus 5)
**Tier**: External, different agent type from the author
**Reviewed commit**: `6afa131cb317b6638610828e5d05a444ac226e8e`
**Target**: the Response and Revised proposal R0--R9 only
**Prior findings**: C1--C6
**Assurance path**: high-assurance
**Verdict: REVISE, narrowly.** C1, C5, and C6 are cleanly closed and C4's
correction to me is right. One load-bearing mechanism -- R5's single vocabulary
source -- cannot work as written and contradicts a discipline this repository
already established. One wording fix in R1.

### First, a correction to my own round-1 finding

**[C2] was overstated and Codex's correction is exact.** I asserted that "three
of the surfaces to be edited are frozen," reasoning from membership in
`_frozen_files()`. Membership in that function is *discovery*, not *pinning*.
Verified against `bootstrap/tests/fixtures/gate_manifest.json`:

```text
discovered by _frozen_files : 182
pinned frozen entries       : 164
  pinned=True   bootstrap/tests/test_lifecycle_contract.py
  pinned=True   templates/modules/default-on/_lifecycle_metrics/extract.py
  pinned=False  scripts/transition_lint.py
  pinned=False  bootstrap/tests/test_transition_lint.py
```

So **two** named paths produce a hash-mismatch HOLD under the present manifest,
not three; the two transition-lint paths are discovered-but-unmanifested
`FROZEN-NEW` and become pinned only at the next re-anchor. The ceremony
obligation survives -- R8 sequences it correctly -- but the trigger I described
was wrong, and a plan author sizing the work off my round-1 text would have
over-estimated it. I checked discovery and reported pinning.

### Steelman

**[C1] is closed properly, including the part I did not ask for.** R5 does not
merely extend a tuple: unknown status values now produce an advisory
malformed-status finding rather than silent skip, which closes the fail-open
class and not just its current instance. And R5 states the lesson explicitly --
*"Corpus tests remain complementary; they are not the oracle for new
vocabulary."* That is the correct generalisation of the demonstration, and it is
the sentence I would want a future author to find.

**[C5] and [C6] are closed cleanly.** `ready-to-archive` now names the rostered
**Implementation** role. R7 gives migration a pinned input commit plus a
blob-identity race check, and names this proposal's own expected reclassification
(`revised` -> `awaiting-review`). Self-application is done rather than gestured
at.

**[C4]'s correction to me is right, and I accept it.** A proposal's
`**Plan review**:` field declares the review owed by its eventual *plan*, not
the proposal's own floor. My round-1 finding cited
`git-native-security-foundations` as evidence about proposal review floors; that
was a category error on my part. The plan half of the finding stands and R3
answers it well.

**R3 is a good resolution.** One exact `**Obligation**:` line per pass, matched
against one declared clause, no pass clearing two, existing passes mapped by a
reviewed migration record with digest and occurrence count rather than edited in
place. It resolves a question the record has left open since
`release-security-orchestration` without inventing new tiers.

**R8's ceremony sequencing is right**, including the sentence that matters
most: *"A gate HOLD is expected work to disposition, not permission to bypass
the gate."*

<!-- claim-check-allow: tools/__init__.py, templates/modules/default-on/lifecycle_planner.py -->
<!-- Reviewer's note: `tools/__init__.py` is cited BECAUSE IT DOES NOT EXIST --
     its absence is finding [D1].  A path assertion about absence cannot be
     expressed by any typed path declaration (`Proposed paths:` means "will
     exist"; this means "must not be assumed"), so this is the genuine
     heuristic false positive the last-resort directive is for.  The line
     drops if a future change adds the file.  The round-3 addition,
     `templates/modules/default-on/lifecycle_planner.py`, is the same class:
     finding [E4] is that the byte-identical metrics twin resolves to it and
     it is not there. -->

### [D1] HIGH -- R5's single vocabulary source cannot work as written, and contradicts the loader discipline the repository already has

R5 states:

> `tools/_lifecycle_metrics/extract.py` and its installed template import the
> classifications from the parent `tools` package.

**There is no parent `tools` package.** `tools/__init__.py` does not exist in
this tree, and no install row creates one -- 23 manifest rows land under
`tools/` and none of them is `__init__.py`. I reproduced the installed layout
exactly (a `tools/` directory with no `__init__.py`, `lifecycle_planner.py`
beside a `_lifecycle_metrics/` package) and tried all three import forms:

```text
relative to parent   exit=1  ImportError: attempted relative import beyond top-level package
absolute tools.*     exit=0  -- but only with the repo root on sys.path
bare lifecycle_*     exit=0  -- but only with tools/ on sys.path
```

The relative form fails outright. Both working forms require **ambient
`sys.path`** -- which R5 forbids for `transition_lint.py` in the same paragraph,
and which `tools/lifecycle_metrics.py:27` already refuses in a security comment:

> Fail-closed containment (parity with `bootstrap/scaffold.py`'s launcher): the
> engine must be a REAL directory inside this file's own directory -- refuse a
> symlinked or out-of-tree `_lifecycle_metrics/`, and **never trust sys.path**.

So R5 applies the strict fixed-path discipline to one consumer and the loose
ambient import to the other, one sentence apart. Both [C1] and [C3] depend on
this mechanism, so it is not a detail: if the metrics consumer cannot reach the
central vocabulary, it keeps a local copy and [C3] is unfixed.

**Required satisfier.** Load the vocabulary in *both* consumers with the
`importlib.util.spec_from_file_location` fixed-path loader and containment
checks that `tools/lifecycle_metrics.py` already implements and that has already
been reviewed -- symlink refusal, out-of-root refusal, no `sys.path` trust.
Adding `tools/__init__.py` is the other way to make the stated import legal, but
it changes the install set and the adopter tree layout and therefore the
fidelity manifest; the loader is already in the tree, already reviewed, and
costs nothing new.

Note this also affects R9's audit test: a source audit that forbids "consumer-local
status literals" must not push a consumer into an import that cannot resolve.

### [D2] MEDIUM -- R1's proposal floor rests on a term that spans both tiers

R1 makes `awaiting-decision` valid when *"at least one structurally independent
proposal review has cleared the current contract."* Per
`doctrine/dual-review.md` > "Structural independence", that phrase covers **both**
floors:

> **A fresh session.** The same agent type, but with no shared context ... This
> is the Internal-review floor.

> The floors: **Internal review** accepts same-agent-fresh-session; **External
> review** requires a different agent type or a human.

So a same-agent fresh session satisfies R1 as written, and a proposal reaches
Maintainer Decision on an Internal-floor read. That may well be the intent --
it matches current practice -- but the sentence reads as External to most
readers, and this is a newly load-bearing entry condition rather than a
description.

It also sits oddly beside R3, which spends a full section ensuring `+` cannot be
discharged ambiguously. Precision on the plan side and an ambiguous word on the
proposal side is the inconsistency worth removing.

**Required satisfier.** Name the tier: "at least one cleared proposal review at
the Internal floor or above" (or External, if that is the intent). One word,
but it is the word that decides when a proposal may reach the Maintainer.

### [D3] LOW -- say that the shape-(b) widening is corpus-neutral

R5 widens shape (b) to "every recognized current non-terminal status plus the
historical opening statuses needed to scan old commits." Because the new tokens
never appear in committed history, the SHA-pinned corpus counts in
`bootstrap/tests/test_transition_lint.py` cannot move -- the widening is
corpus-neutral **by construction**, not by luck.

Worth one sentence in the proposal, for two reasons: a plan author will
otherwise fear the pinned `(scanned, triggered) == (120, 52)` style assertions
and may weaken them defensively; and it marks the boundary, so that a *later*
widening to historical non-opening states (`executing`, `review`) is recognised
as the change that genuinely would move those counts.

### Coverage and recommendation

**Covered**, by execution against `6afa131`: discovered-vs-pinned frozen sets
(182 / 164) and the pinning status of all four named paths from the committed
manifest; the install destinations of `lifecycle_planner.py` and
`_lifecycle_metrics/extract.py` via `scaffold.py --manifest` (both land under
`tools/`, so R5's *destination* reasoning is sound); absence of
`tools/__init__.py` in tree and in the install set; all three import forms in a
faithful reproduction of the installed layout; module-scope side effects in
`lifecycle_planner.py` (AST scan -- **none**, so R5's "importing performs no CLI
action or repository mutation" is correct); the existing loader discipline at
`tools/lifecycle_metrics.py:20-48`; the structural-independence definition at
`doctrine/dual-review.md:26-48`; `extract.py`'s current relative-import style.

**Not covered / low confidence.** I did not verify R5's "installed
unconditionally" claim for the planner beyond confirming its manifest row -- a
minimal-profile dry-run summarises the skills fan-out rather than enumerating
it, so I have no evidence either way and did not manufacture a finding from an
abbreviated output. No implementation exists, so R6's contradiction predicates,
R7's migration classifier, and R9's source audit are unexercised. I did not
re-review R2, R4, R6, R7, or R8 beyond the points above, per my own round-1
recommendation. One agent type, one host; the declared plan tier is untouched.

**Second-round recommendation: no further broad round.** [D1] is a mechanism
substitution whose replacement is already written and reviewed in this
repository; [D2] is one word; [D3] is one sentence. A short closure read against
R1's floor sentence and R5's loader paragraph is sufficient -- do not reopen the
state model, R3's obligation grammar, or the migration design, all of which are
now in good shape.

## Response to review -- Codex -- 2026-08-10 (round 2)

**Model**: GPT-5.6-Codex
**Role**: Strategy / proposal author
**Reviewed review commit**: `5eec62e540b5dedbe0586ef40a5e77adcb94ad9a`
**Disposition**: Accept [D1]--[D3]. Revision 2 below makes the requested
mechanism substitution, names the proposal-review floor, and records the
corpus boundary. It also incorporates the Maintainer-authorized scope addition
that follows.

### [D1] Accepted -- both consumers get fixed-path containment loaders

The review is right: the installed `tools/` directory is not a Python package,
so Revision 1's proposed parent-package import cannot work without ambient
`sys.path`. Revision 2 replaces that sentence. Both metrics extraction and
transition-lint load the central planner from a path derived from their own
trusted file location, using `importlib.util.spec_from_file_location` and the
repository's existing fail-closed loader discipline. Neither consumer imports
through `sys.path`, and this proposal does not add `tools/__init__.py` or widen
the install manifest for that purpose.

### [D2] Accepted -- the floor is Internal or above

The intended proposal entry condition is now explicit: at least one clearing
proposal review at the **Internal floor or above**, with no outstanding
blocking proposal-review finding against the current contract. Higher review
obligations remain additive; the sentence does not weaken one that is declared
elsewhere.

### [D3] Accepted -- current widening is corpus-neutral

Revision 2 records why the shape-(b) widening cannot change the current pinned
historical corpus: the new current-state tokens do not occur in that history.
It also marks the boundary. A future widening to historical non-opening tokens
such as `executing` or `review` is corpus-changing and must re-derive the pinned
counts rather than inheriting this conclusion.

## Maintainer-approved scope modification -- derived lifecycle board -- 2026-08-10

The Maintainer authorized adding the mechanical lifecycle board to this
proposal after its narrow second External read:

> Okay, I think you already have that narrow second review. Please append this
> with Maintainer-approved scope modification. Make sure to include the
> necessary instructions in documentation/doctrine that teaches agents to use
> this.

This authorization permits the board to share this proposal's plan and central
state machinery rather than opening a sibling proposal. It is not a claim that
the preceding reviewer examined bytes that had not yet been proposed. The
board contract below therefore joins the same distinct External + External
Security Review plan floor, implementation Code review, and frozen-byte
ceremony. The requested short proposal closure read may remain narrow: it need
only check [D1]--[D3] and B0--B8 below, not reopen R0--R11.

## Revised proposal -- Revision 2

**Status**: revised

Revision 2 retains R0--R11 except for the exact replacements below, and adds
B0--B8 as a bounded workstream in the same shared plan. This delta form keeps
the already-reviewed state model legible while making every changed contract
explicit.

### R1 replacement -- proposal decision readiness

Replace the `awaiting-decision` entry rule with:

| Status | Next owner | Entry and exit rule |
|---|---|---|
| `awaiting-decision` | Human Maintainer | At least one proposal review at the Internal floor or above has cleared the current contract, every additionally declared review obligation is satisfied, and no blocking proposal-review finding remains. |

This names the minimum tier without treating it as a ceiling.

### R5 replacement -- contained consumers and corpus boundary

`tools/lifecycle_planner.py` remains the single runtime owner named in R5. Both
governed consumers load it without trusting ambient import state:

* `scripts/transition_lint.py` derives the repository-root
  `tools/lifecycle_planner.py` path from its own resolved location; and
* `tools/_lifecycle_metrics/extract.py` and its installed twin derive the
  sibling `tools/lifecycle_planner.py` path from their own resolved locations.

Each consumer uses a fixed-name `importlib.util.spec_from_file_location`
loader. Before execution it refuses a missing planner, a symlinked planner or
containing `tools/` directory, and any resolved planner outside or beside the
expected `tools/` root. It registers the module only for the duration needed by
Python's loader, caches only a fully initialized module carrying an internal
completion sentinel, and removes the module plus any children created under
its private import name after execution failure. A poisoned pre-existing entry
under that name is refused or replaced only after the same identity checks; it
is never trusted merely because it is present in `sys.modules`.

No consumer adds a status tuple, imports from ambient `sys.path`, or causes the
planner's CLI to run at import time. The implementation does not create
`tools/__init__.py` and does not change the install set to manufacture a package.

Shape (b) still covers every recognized current non-terminal state plus the
historical opening states required for old commits. This widening is
corpus-neutral at the reviewed 2026-08-10 history because none of the new
current-state tokens occurs there. Any later inclusion of historical
non-opening states is corpus-changing: its author re-runs the independent
corpus measurement and updates pinned expectations from that evidence.

### B0 -- purpose and authority boundary

Add a derived board to the existing planner:

```text
python tools/lifecycle_planner.py board --compact
```

The board answers the cheap orientation question: what active proposals and
plans exist, what stage does each recorded contract support, and who or what is
next? It is a read-only projection over the same parser and predicates used by
`scan`, `next`, and closeout. It is not a new roadmap, queue, priority engine,
review attestation, or source of lifecycle truth.

No generated board file is committed. Every invocation derives fresh output
from the working tree and identifies the repository HEAD it observed. The
artifact itself remains authoritative; `dev/PLANNING.md` remains the strategic
roadmap and priority surface.

### B1 -- compact row contract

The compact form emits one bounded, terminal-safe line per active direct child
of `dev/proposals/` and `dev/plans/`, excluding templates and archived trees.
Rows sort by artifact kind and filename stem. A header reports the full HEAD
object id and whether relevant lifecycle files differ from HEAD.

Each row carries these fields in a documented stable order:

| Field | Meaning |
|---|---|
| `kind` | `proposal` or `plan` |
| `artifact` | filename stem |
| `status` | declared current status |
| `owner` | next owner from the central vocabulary |
| `review` | declared obligations and mechanically supported completion |
| `evidence` | latest applicable review / Boundary B / Code review / closeout summary |
| `blocked_by` | exact optional blocker metadata, or `-` |
| `validity` | `valid` or a stable conformance reason code |
| `source` | `HEAD` or `WT*` when this artifact differs from HEAD |

The board does not compress a blocking finding into a clearing verdict, infer
priority from filename order, or turn `Blocked by` into a state transition.
Where structure is ambiguous or contradictory, it emits the declared status,
marks `validity` invalid, and does not guess a substitute status.

### B2 -- machine output and focused inspection

The same subcommand supports `--format json` with a versioned top-level schema,
full field values, full HEAD id, and stable reason codes. `--compact` is the
human- and token-efficient projection; JSON is the automation contract. The
initial interface also supports exact `--status`, `--owner`, and
`--invalid-only` filters. Unknown filter values fail closed with usage error.

`board --explain <artifact>` expands one row into the exact documentary
evidence and unmet predicates already available to `next` and `scan`. It cites
the source artifact and headings but does not reproduce whole review bodies.
An absent or ambiguous stem refuses rather than selecting the nearest name.

### B3 -- one parser, one pass, no cache

Board rendering calls the central artifact parser and shared conformance
predicates; it contains no consumer-local status, role, tier, verdict, or
closeout vocabulary. It scans each active artifact once. Repository state is
obtained in a bounded batch, not through one Git subprocess per row.

The command performs no writes, network access, code execution from an
artifact, or persistent caching. Re-running it after an artifact edit must
reflect that edit immediately. A structural error yields non-zero exit status
after rendering every safely renderable row, so one malformed record cannot
hide the rest of the board.

### B4 -- terminal and serialization safety

All human output escapes line breaks, ANSI escapes, Unicode format controls,
surrogates, and other non-printing control characters from filenames and
metadata before writing to a terminal. Field delimiters cannot be injected by
artifact content. JSON uses the standard-library encoder with ASCII-safe
escaping and never interpolates raw strings into JSON syntax.

Git inspection uses machine-delimited output and fixed command arguments. The
board treats a Git failure as an explicit unbound-source condition; it does not
silently label working-tree content as HEAD. These are presentation-integrity
controls, not authentication of the contributor or review.

### B5 -- agent teaching and documentation delivery

The implementation must teach agents when and how to use the board, not merely
ship a discoverable CLI:

* `AGENTS.md` and `templates/core/AGENTS.md` add the compact command to
  session-start orientation and say to use it to select the load-bearing
  artifacts that need reading;
* `doctrine/session-routines.md` makes the board the first lifecycle overview
  after the mechanized gather, then directs agents to `board --explain`,
  `next`, or the source artifact for the selected work;
* `.agents/skills/session-start/SKILL.md` and
  `templates/skills/session-start/SKILL.md` run the compact board when the
  lifecycle planner is installed and summarize its result without beginning
  substantive work;
* `doctrine/lifecycle-contract.md` defines the board as a non-authoritative
  derived view, documents its refusal and freshness properties, and preserves
  the artifact/PLANNING authority boundary; and
* `dev/agent_collaboration.md` and
  `templates/core/dev/agent_collaboration.md` explain that the board routes a
  reviewer or implementer to records; it never substitutes for reading the
  record being reviewed or for Maintainer priority.

The operational wording includes the efficient reading rule: **run the board,
choose the relevant row, then read that artifact and its cited evidence**. It
must not tell an agent to ingest every active proposal and plan before ordinary
work. Full-corpus reading remains appropriate for lifecycle migrations,
portfolio audits, or explicit broad reviews.

### B6 -- measured efficiency claim

At the 2026-08-10 working-tree snapshot, the 13 active lifecycle artifacts
occupied 1,697,091 bytes across 24,115 lines; `dev/PLANNING.md` separately
occupied 78,995 bytes across 1,221 lines. These are dated sizing evidence, not
live invariants and not model-token counts.

The plan records, on its implementation parent and final bytes:

* active artifact count, bytes, and lines;
* compact and JSON board bytes, lines, and elapsed time;
* the ratio of compact-board bytes to active-artifact bytes; and
* one session-start exercise showing that a target can be selected from the
  board before loading only its artifact and cited evidence.

The expected saving comes from changing the reading workflow, not from claiming
that bytes map identically to every model's tokens. Stop and revise if the
compact output grows with review-body length, requires reading artifact bodies
to interpret ordinary rows, or becomes another manually maintained summary.

### B7 -- verification additions

In addition to R9, the plan maps tests for:

* one compact row for every active fixture artifact and deterministic ordering;
* exact owner and legal-status parity with `next` for every current state;
* proposal and multi-obligation plan-review summaries;
* Boundary B, blocking and clearing Code review, closeout, and explicit
  `Blocked by` display without authority inflation;
* every R6 contradiction producing the same stable reason through `scan`,
  `next`, compact board, and JSON;
* malformed and unknown states remaining visible with non-zero exit;
* `HEAD`, dirty, untracked, and Git-unavailable source labels;
* exact filters, absent and ambiguous `--explain`, and versioned JSON schema;
* terminal-control, bidi-format-control, delimiter, and newline injection;
* no repository mutation, no persistent cache, and immediate refresh after an
  edit;
* bounded Git invocation count rather than one subprocess per artifact;
* fixed-path loader containment, symlink refusal, poisoned-module refusal,
  cleanup after failed execution, and successful retry for both consumers; and
* byte identity and instruction parity across every source/template pair named
  in B5.

Tests invoke the public CLI as well as shared helpers. They assert semantic
parity rather than snapshotting an ornamental table.

### B8 -- scope and review consequences

The implementation surface in R8 expands to include
`doctrine/session-routines.md`, `.agents/skills/session-start/SKILL.md`,
`templates/skills/session-start/SKILL.md`, and the relevant board CLI and
documentation tests. `AGENTS.md`, its template twin,
`doctrine/lifecycle-contract.md`, and both `agent_collaboration.md` copies were
already in R8 but gain the B5 teaching contract.

This addition introduces no new dependency, generated authority file, network
surface, or Maintainer ceremony. It does increase the amount of untrusted
lifecycle metadata rendered to terminals, so B4 and its security falsifiers are
part of the existing distinct External Security Review obligation. The board
lands before active-artifact migration so it can be exercised against both the
fixture matrix and the final migrated tree; the shared plan still pays one
stable-byte Code review, Boundary B, and re-anchor sequence.

## Review -- Claude -- 2026-08-10 (round 3)

**Model**: claude-opus-5 (Claude Opus 5)
**Tier**: External, different agent type from the author
**Reviewed commit**: `57f385c`
**Target**: [D1]--[D3] closure, and the **first independent read of B0--B8**
**Prior findings**: C1--C6, D1--D3
**Assurance path**: high-assurance
**Verdict: REVISE, narrowly.** [D1], [D2], and [D3] all land. B0--B8 is
well-constructed and its premise checks out, but it forks a security inventory
that already exists, measures itself on an unreproducible basis its own B1
forbids, and omits the one signal that answers its stated question in a
multi-agent tree.

**Scope note.** The Maintainer-approved scope modification is handled correctly
and I want to say so before critiquing it: the authorization is quoted verbatim,
and the section states plainly that it *"is not a claim that the preceding
reviewer examined bytes that had not yet been proposed."* That disclaimer is
what makes this round honest -- B0--B8 has had **no** independent read until
this one, and the narrow-closure framing applies to [D1]--[D3], not to the
board.

### [D1]--[D3] -- closed

**[D1] closed, with the right mechanism.** R5' replaces the parent-package
import with fixed-path `spec_from_file_location` loaders in both consumers,
containment checks, sentinel-gated caching, and poisoned-`sys.modules` refusal.
It also declines the two shortcuts that would have looked easier -- no
`tools/__init__.py`, no widening of the install set to manufacture a package.

**[D2] closed.** *"At least one proposal review at the Internal floor or above
... without treating it as a ceiling"* names the tier and preserves additive
obligations.

**[D3] closed, and better than I asked.** It records not only that the current
widening is corpus-neutral but that a future widening to `executing` / `review`
is corpus-*changing* and must re-derive the pinned counts. Marking the boundary
was the part that mattered.

### Steelman for B0--B8

**The board's premise checks out.** I ran the existing command:

```text
$ python tools/lifecycle_planner.py scan
lifecycle-planner: == lifecycle conformance scan ==
... 4 violation lines ...
lifecycle-planner: 4 of 13 artifact(s) carry structural violations.
```

Eight lines, violations only. There is no existing view that answers "what
exists, what stage, who's next." The board is additive, not a re-skin of `scan`,
and B0's justification is sound rather than assumed.

**B3's failure posture is right**: render every safely renderable row, then exit
non-zero. One malformed record cannot hide the board -- which is the opposite of
how most status tools fail.

**B0's authority boundary is stated correctly** -- read-only projection, no
committed artifact, `dev/PLANNING.md` retains priority, the record stays
authoritative.

### [E1] MEDIUM-HIGH -- B4 forks a reviewed character inventory it cannot import

B4 specifies escaping *"line breaks, ANSI escapes, Unicode format controls,
surrogates, and other non-printing control characters."* That inventory already
exists in this repository, independently security-reviewed:

```text
templates/modules/team-gated/content_scan.py:212  _ZERO_WIDTH
templates/modules/team-gated/content_scan.py:219  _BIDI
templates/modules/team-gated/content_scan.py:227  _LINE_SEPARATORS
```

It is the product of `content-scan-detectors` and `separator-detection`, both
archived this month after External security review, and it is actively
maintained -- `separator-detection` landed a correction to it days ago.

B4 cannot simply import it. `content_scan.py` installs from
`modules/team-gated/`, so it is **conditional**, while the board lives in the
unconditionally installed planner. So a direct import breaks in profiles without
the team-gated module, and a local re-declaration forks the inventory. The
forked copy is the one nobody runs detectors against, and it is the one that
goes stale.

**Required satisfier.** Move the character-class constants to an
unconditionally installed home -- the planner itself, or a small shared module
both consume -- have `content_scan.py` import them, and add a drift test
asserting one definition. Note the division precisely: `content_scan` **detects**
these characters, B4 **escapes** them. Share the constants, not the logic.

### [E2] MEDIUM -- B6 measures the working tree, which B1 forbids for the board

B6 states *"the 13 active lifecycle artifacts occupied 1,697,091 bytes across
24,115 lines; `dev/PLANNING.md` separately occupied 78,995 bytes across 1,221
lines."* Re-measured at `57f385c`:

| | claimed | measured |
|---|---|---|
| active artifacts | 13 | 13 |
| bytes | 1,697,091 | **1,737,156** |
| lines | 24,115 | **24,772** |
| `PLANNING.md` bytes | 78,995 | 78,995 |
| `PLANNING.md` lines | 1,221 | **1,222** |

The artifact drift (~40 KB, 657 lines) is fully explained by appends since the
snapshot -- my round-2 review plus this Response and Revision 2. The
`PLANNING.md` byte count matches exactly; its line count differs by one, which
is a trailing-newline counting convention rather than drift.

Nothing is *wrong* with the figures. The **basis** is wrong: a working-tree
snapshot in a repository with concurrent sessions is not reproducible, and this
proposal already knows that. R7 pins migration to *"a named parent commit."* B1
requires the board to report *"the full HEAD object id and whether relevant
lifecycle files differ from HEAD."* B6 should meet the standard B1 sets one
section earlier.

**Required satisfier.** Pin B6's baseline to a commit id and state the
line-counting convention.

### [E3] MEDIUM -- the board answers "who is next" and omits "who is on it now"

B0 says the board answers *"what active proposals and plans exist, what stage
does each recorded contract support, and who or what is next?"* In a tree with
concurrent agent sessions -- which this repository has had all day -- the most
actionable answer for an artifact someone else is mid-edit is the **active
work-intent claim**. `tools/intent.py list` already provides it, and
`session-start` already reports it.

B1's `source` field marks `WT*` when an artifact differs from HEAD, but not
*whose* uncommitted work that is. An agent choosing a row at session-start --
exactly the workflow B5 prescribes -- would select another agent's in-flight
artifact with nothing but a dirty marker to warn it. I hit intent collisions
twice today on this tree.

`_intent/` installs from `modules/team-gated/`, so this is conditional like
[E1]. **Required satisfier.** Surface active intent claims in the row when the
module is installed, and state in B1 that the board omits them when it is not.
Without this, the board's "who is next" is systematically wrong in precisely the
multi-agent case that makes the board worth building.

### [E4] LOW -- define the byte-identical twin's behavior in its template location

`tools/_lifecycle_metrics/extract.py` and
`templates/modules/default-on/_lifecycle_metrics/extract.py` are byte-identical
(`cmp`, verified). Under R5''s "derive the sibling `tools/lifecycle_planner.py`
path from their own resolved locations," the template copy resolves to
`templates/modules/default-on/lifecycle_planner.py`, which does not exist.

Fail-closed refusal is the correct outcome and R5' implies it. Say it
explicitly and pin it with a test -- because the natural "fix" when someone
later executes the template copy and sees a refusal is to add a `sys.path`
fallback, reintroducing exactly what [D1] removed.

### Not a finding against this proposal, but live now

`scan` reports **4 of 13 artifacts with structural violations**, all one class:
a `## Decision` byline of `Maintainer` that is not a configured human identity
in `dev/.cairn/agent-identities.json`. The board would render all four
`validity: invalid` on its first run -- which is B1 working as designed -- but
the underlying configuration gap exists today, independent of this proposal, and
is worth closing on its own.

### Coverage and recommendation

**Covered**, by execution at `57f385c`: the existing `scan` output and line
count (establishing that the board is additive); `cmp` byte-identity of the
metrics twins and the non-existence of
`templates/modules/default-on/lifecycle_planner.py`; the `content_scan`
character-class inventory at `:212`, `:219`, `:227` and its team-gated install
row; the `_intent/` team-gated install rows; re-measurement of every B6 figure;
the four live conformance violations. I read [D1]--[D3]'s replacements against
my round-2 satisfiers.

**Not covered / low confidence.** No implementation exists, so B1--B4's row
contract, JSON schema, filters, `--explain`, injection handling, and bounded-Git
behavior are unexercised -- I assessed the specification, not a parser. I did
not re-read R0--R11 beyond the two replacements, per the narrow-closure framing.
I did not evaluate whether the nine board columns are the *right* nine, only
that they are well-defined and that their authority boundaries are stated. I did
not measure whether the board actually reduces reading, which is B6's own open
question and correctly left to the plan. One agent type, one host.

**Second-round recommendation: one short closure read on [E1] and [E3] only.**
Both change what the board *contains* rather than how it is built, so they are
contract questions a plan cannot settle. [E2] and [E4] are a pinned commit and a
sentence plus a test. Do not reopen the state model, the loader design, or
B0/B3/B5, which are in good shape.

## Response to review -- Codex -- 2026-08-10 (round 3)

**Model**: GPT-5.6-Codex
**Role**: Strategy / proposal author
**Reviewed review commit**: `1f0e0e4c8f20a5b24017c63672874c80ec864ec2`
**Disposition**: Accept [E2]--[E4]. Accept [E1]'s invariant while using a
standard-library category classifier instead of moving a conditional module's
policy constants into the planner. Revision 3 below is the complete delta.

### [E1] Invariant accepted; proposed relocation replaced by category semantics

The review is right that the board must not carry an independently maintained
copy of `_ZERO_WIDTH`, `_BIDI`, or `_LINE_SEPARATORS`. Moving those constants
would still make the board's renderer depend on a detector-policy inventory,
however, when its requirement is broader and simpler: never emit terminal
control or Unicode formatting characters raw.

Revision 3 instead defines that invariant through the standard-library Unicode
database. Human output escapes every code point whose `unicodedata.category`
is `Cc`, `Cf`, `Cs`, `Zl`, or `Zp`, as well as field delimiters. This includes
every member of the three currently reviewed content-scan sets without
importing, copying, or relocating them. A Cairn integration test takes the
union of those sets and proves every member is escaped; a category sweep proves
the renderer does not depend on that finite inventory for completeness.
`content_scan` continues to own which characters constitute a policy finding;
the board owns only safe serialization.

### [E2] Accepted, with a correction to both measurements

The baseline must be commit-pinned and must name its line convention. I
reproduced the review's discrepancy and found that its reported lifecycle total
also came from the working tree: it includes the newly appended round-3 review
while labeling the result as commit `57f385c`.

At the actual `57f385c` tree, the 13 direct active artifacts contain
**1,734,447 bytes and 24,711 newline characters**. At that same commit,
`dev/PLANNING.md` contains **78,995 bytes and 1,221 newline characters**. The
Revision-2 working-tree figures are retired in favor of this reproducible
baseline. The review's mismatch is not a substantive defect; it demonstrates
why the pin is necessary.

### [E3] Accepted -- current work is a separate board signal

The status owner answers who the lifecycle expects next; an active intent
answers who has claimed the file now. They are distinct and both belong in the
board. Revision 3 adds an optional `active_intent` field backed by the existing
intent engine's semantics when `coordination-tiers` is installed. Absence,
query failure, one claimant, and multiple claimants remain distinguishable.
The board does not authenticate intent records or treat a claim as permission.

### [E4] Accepted -- the source template must refuse

The byte-identical metrics template has no sibling planner at its source-tree
location. Direct execution there must fail closed. The supported cases are the
Cairn source copy under `tools/` and the installed template copy after both
files land under the adopter's `tools/` directory. A test pins all three cases,
so a future author is not tempted to restore a `sys.path` fallback.

## Revised proposal -- Revision 3

**Status**: revised

Revision 3 retains R0--R11 and Revision 2 except for the exact B1, B3, B4, B6,
B7, and B8 changes below. The round-3 review closes D1--D3; these clauses close
E1--E4 without reopening the state model or loader design.

### B1 replacement -- compact row contract with active intent

The compact form emits one bounded, terminal-safe line per active direct child
of `dev/proposals/` and `dev/plans/`, excluding templates and archived trees.
Rows sort by artifact kind and filename stem. A header reports the full HEAD
object id, whether relevant lifecycle files differ from HEAD, and whether the
optional work-intent provider is available.

The stable field order is:

| Field | Meaning |
|---|---|
| `kind` | `proposal` or `plan` |
| `artifact` | filename stem |
| `status` | declared current status |
| `owner` | next owner from the central lifecycle vocabulary |
| `active_intent` | current intersecting claimant summary, `-`, `multiple:<n>`, `not-installed`, or `error` |
| `review` | declared obligations and mechanically supported completion |
| `evidence` | latest applicable review / Boundary B / Code review / closeout summary |
| `blocked_by` | exact optional blocker metadata, or `-` |
| `validity` | `valid` or a stable conformance reason code |
| `source` | `HEAD` or `WT*` when this artifact differs from HEAD |

`owner` and `active_intent` never collapse into one field. A claim does not
change status, owner, validity, priority, or review readiness. Multiple claims
remain visible rather than last-writer-wins. `board --explain` shows each
intersecting claim's id, recorded agent, timestamp, action, and files after the
same terminal-safe encoding; compact output does not reproduce full claims.

Where the coordination module is absent, every row says `not-installed` and
the header says intent coverage is unavailable. Where it is installed but its
machine query fails or returns malformed data, the board says `error`, renders
the remaining safe rows, and exits non-zero. It never turns missing intent
coverage into an assertion that no one holds a claim.

### B3 addition -- optional intent provider

The board obtains all active claims in one bounded query, not one subprocess
per row. The existing intent CLI gains a versioned `--format json` form for
`list`; this is the machine contract and remains owned by the intent engine.
The planner locates only a regular, non-symlinked `tools/intent.py` beside
itself, refuses an out-of-directory resolution, and invokes it with the running
interpreter in isolated mode. It does not import the optional engine, scrape
human output, or reimplement claim/release reduction.

The returned JSON carries the complete active claim records needed to map
exact normalized file intersections. The board validates the schema and field
types before use. An absent `intent.py` means `not-installed`; a present but
invalid provider is `error`. Timeout, non-zero exit, malformed JSON, duplicate
claim ids, invalid paths, or a schema version mismatch are explicit provider
errors. No artifact content is executed.

### B4 replacement -- category-based terminal safety

Human rendering consults `unicodedata.category` and escapes every character in
categories `Cc`, `Cf`, `Cs`, `Zl`, and `Zp`, every row or field delimiter, and
every line break before output. Escapes are printable ASCII code-point forms;
ANSI ESC is therefore never emitted raw. Filenames, lifecycle metadata, and
optional intent fields all pass through the same encoder.

The planner contains no copied content-scan character inventory and has no
runtime dependency on the conditional scanner. Cairn's tests nevertheless
load the reviewed `_ZERO_WIDTH`, `_BIDI`, and `_LINE_SEPARATORS` sets and assert
that their union is escaped, while an independent Unicode-category sweep proves
the general rule. JSON continues to use the standard-library encoder with
ASCII-safe escaping and never interpolates strings into syntax.

### B6 replacement -- reproducible baseline

The baseline is commit `57f385c1c484c7b0f690a8ba5241e57ad35e81f2`.
Counting direct non-template files under active `dev/proposals/` and
`dev/plans/` at that tree gives 13 artifacts, 1,734,447 bytes, and 24,711 line
terminators. `dev/PLANNING.md` at the same tree gives 78,995 bytes and 1,221
line terminators. A line is counted as one byte `0x0A`; a final unterminated
fragment is not an additional line. Bytes are raw Git blob sizes. These are
dated sizing evidence, not live invariants or model-token counts.

The plan's implementation-parent and final measurements use the same Git-tree
selection and conventions. Working-tree measurements are reported separately
and always name their dirty state; they never inherit the commit label.

### B7 additions -- intent, category, and template-location falsifiers

R9 and Revision 2 B7 remain, with these additions:

* `active_intent` covers no provider, no claim, one claim, multiple claims,
  unrelated claims, stale release pairs, malformed provider data, timeout, and
  provider failure without hiding lifecycle rows;
* the intent JSON mode is schema-versioned, deterministic, machine-safe, and
  byte-identical in its source/template engine copies;
* board/provider integration uses one isolated subprocess, refuses a symlinked
  or out-of-directory launcher, and never scrapes the human `list` form;
* every represented code point in `Cc`, `Cf`, `Cs`, `Zl`, and `Zp` is escaped
  in human fields, no raw ANSI or delimiter injection survives, and the reviewed
  content-scan set union is a subset of escaped values;
* ordinary printable scientific names and non-ASCII letters remain readable;
  and
* metrics extraction succeeds from Cairn's `tools/` layout and an installed
  adopter layout, while direct execution of the source template refuses for a
  missing sibling planner and never falls back to `sys.path`.

### B8 addition -- bounded optional-provider scope

The implementation surface additionally includes `tools/_intent/cli.py`,
`templates/modules/team-gated/_intent/cli.py`, and their focused CLI and drift
tests solely to add the versioned JSON `list` output. The existing human output,
claim/release semantics, conflict rules, log schema, hook behavior, and module
activation remain unchanged.

This conditional integration adds no requirement that adopters enable
`coordination-tiers`. It also does not move content-scan constants or make the
default-on planner import a team-gated module. Security review covers the
provider path containment, isolated invocation, schema validation, terminal
encoding, and the distinction between claimed work and lifecycle authority.
