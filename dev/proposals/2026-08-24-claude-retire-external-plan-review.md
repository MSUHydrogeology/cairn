# Retire External plan review: plans take Internal fresh-agent reviews only

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date opened**: 2026-08-24
**Status**: revising
**Assurance path**: high-assurance (governing doctrine and lifecycle)
**Touches**: `AGENTS.md` + `templates/core/AGENTS.md`;
`doctrine/dual-review.md`, `doctrine/plans.md`, `doctrine/proposals.md`,
`doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`,
`doctrine/session-routines.md`; `dev/proposals/_template.md`,
`dev/plans/_template.md` + shipped twins;
`dev/agent_collaboration.md` + shipped twin; `tools/lifecycle_planner.py` +
shipped twin; `bootstrap/tests/test_lifecycle_contract.py`,
`bootstrap/tests/test_pilot_evidence.py`,
`bootstrap/tests/fixtures/gate_manifest.json`
**Related**: `2026-08-21-claude-convergent-lifecycle` (awaiting-review; see
"Relationship" below), `dev/strategy/2026-08-21-claude-nimbleness-recovery.md`
**Plan review**: required(Internal) — set by the Maintainer direction this
proposal records; a recorded readiness token is a preserved recommendation
the Maintainer resolves at the Decision

## Origin

Maintainer direction, 2026-08-24, verbatim: *"we need to completely remove
the doctrine for External Plan Review from this project. It is not, and
should not ever, be required. We can thus remove all machinery and doctrine
for making such recommendations in the Plan. Plans only ever have internal
fresh-agent reviews, be they security or standard."*

## Proposal

**One rule replaces the apparatus: a plan review is an Internal,
fresh-context review — always.** Standard or security-flavored, the reviewer
is a fresh session of the same agent type, never a mandated different-type
round. External plan review ceases to exist as a tier, a requirement, a
recommendation slot, or an escalation target. Concretely:

1. **Doctrine.** `doctrine/dual-review.md` loses "Plan-readiness
   inheritance" and every External-plan-review pathway; the review-allocation
   statement becomes: *External independence lives at the proposal; Internal
   freshness lives at the plan and at code review; the Maintainer decides.*
   `AGENTS.md`'s Review section (and its shipped twin) drops the
   inheritance/escalation paragraph — including `DISTINCT REVIEW REQUIRED`,
   readiness invalidation, and "spending" an External plan round. The other
   doctrine files' mentions are conformed.
2. **Templates.** The proposal template loses the `Plan readiness` slot
   entirely — reviewers no longer record plan-review recommendations of any
   kind; that is the "machinery for making such recommendations" the
   direction removes. The plan template's review declaration becomes a closed
   two-token vocabulary: `required(Internal)` (default) or
   `not required(<rationale>)` (trivial-accept collapse, unchanged). A
   security-sensitive plan declares `required(Internal, security)` — same
   floor, security lens, still a fresh same-type session.
3. **Machinery.** `tools/lifecycle_planner.py` + shipped twin: delete
   readiness parsing and the External-tier validation for plans; a plan
   declaring an unknown tier draws a warning naming the closed vocabulary
   (advisory, per the standing direction). Tests updated:
   `test_lifecycle_contract.py`, `test_pilot_evidence.py`, and the
   `gate_manifest.json` fixture, plus a directed test that a legacy
   `required(External)` or `Plan readiness:` line in an *active* artifact
   warns and is read as `required(Internal)`.
4. **What does not change.** Proposal review: the External floor on the
   deliberate lane stays — the proposal is where different-type independence
   pays, because the design is still movable there. Code review: floor
   unchanged (independent context, never the implementing agent). Security
   Reviews attached to high-risk *surfaces*: unchanged wherever they attach
   to proposals or code; where one attaches to a plan, it is conducted as
   `required(Internal, security)`. The Maintainer may still *choose* to ask
   any additional reader for any artifact — a choice is not a tier, and
   removing the mandate does not remove the option.
5. **Archives are immutable.** Archived artifacts keep their recorded
   readiness tokens and External plan reviews as history; nothing is
   retro-edited. The tokens remain readable in longitudinal metrics and are
   refused nowhere.

## Rationale

* **The mechanism never once did useful work in its cheap direction.** The
  readiness vocabulary existed so an External proposal pass could grant a
  lighter plan review. Recorded outcomes: **19 `DISTINCT REVIEW REQUIRED`, 0
  grants** — every recorded use produced only the expensive branch. The toll
  bridge never opened; this removes the toll booth.
* **A plan is implementation detail, and implementation detail is the
  agents' lane** (expertise routing, `nimbleness-recovery` 1.2). External
  plan review re-litigates a design the proposal's External pass already
  read, at the highest per-round cost the project has — the plan corpus
  (median ~1,800 lines) outweighs the proposal corpus it restates.
* **The Internal floor is not a soft floor.** Fresh-context same-type review
  has caught real, shipping-grade defects in this project's record; what it
  trades away is a different failure lens, which the proposal-stage External
  read still provides where the design is actually at stake.

## Relationship to `convergent-lifecycle`

This proposal **goes further than** `convergent-lifecycle` §2 and, where they
conflict, **this one governs**: that proposal retires the reviewer *trigger*
but preserves declared `required(External)` plan floors and, per its RCL-06
response, binds its own derived plan to External review under the current
rule. If this proposal is **accepted first**, External plan review no longer
exists, `convergent-lifecycle`'s derived plan takes `required(Internal)`, and
its §2 floors-vs-trigger rule is read with "declared floor" meaning
`required(Internal)` and Security Review only. If this proposal is rejected,
`convergent-lifecycle` stands as written. The two do not need to merge: this
is a strict subtraction from either baseline.

## Evidence / verification plan

Doctrine and template edits pass the claim, link, and neutrality gates. The
planner change carries directed tests: the closed two-token vocabulary
accepted; a legacy External/readiness line warns and resolves to Internal; an
archived artifact with either token draws no warning. Falsification for the
review of this proposal: grep the post-change tree for `Plan readiness` and
`required(External)` across the **governing surfaces** — `AGENTS.md`,
`doctrine/`, `templates/`, both live `_template.md` files, `tools/`,
`scripts/`, `bootstrap/` — and the result must be empty. Append-only records
of active and archived deliberation artifacts legitimately retain the tokens
as history and are out of scope. The instrument is confirmed against the
pre-change tree, where the same grep matches **24 files** (as_of 2026-08-24,
archives and this proposal excluded).

## Signals the change is wrong

* A plan-stage defect ships that a different-agent-type read would plausibly
  have caught *and* the proposal-stage External read could not have — audit
  against the actual finding, not the counterfactual's flattery.
* The Maintainer finds themselves manually requesting extra plan readers
  often — the option is carrying load the tier used to carry; reintroduce
  deliberately, not by drift.

## Reviewer brief

One round expected; Internal floor (this is a subtraction whose design
question — should the tier exist — the Maintainer has already decided; the
review verifies the removal is complete and coherent, not whether to do it).
Seams: (1) the surface list above against the live grep — name any carrier
of the doctrine the removal misses; (2) the legacy-token warning path —
active vs archived handling; (3) doctrine wording — confirm no sentence
survives that makes External plan review *available as a requirement*, since
a dormant requirement is how the ratchet rebuilds.

## Review -- Codex (External) -- 2026-08-24

**Model**: GPT-5.6 (Codex)

Reviewed commit: e753882621b4a8da245eb4e350003084c1efaec7
Target: the complete opened contract, especially the security-plan form, legacy handling, convergent-lifecycle relationship, and removal evidence
Prior findings: none
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (5 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The Maintainer direction is unambiguous about removing External *plan* review,
and the proposal correctly keeps proposal-stage External independence and the
separate code-review floor. A smaller allocation model is viable, but only if
security review and migration of the live grammar remain explicit rather than
becoming ignored text after a tier name.

### Findings

#### RERP-01 — BLOCKING: `required(Internal, security)` is an ordinary Internal review, not a Security Review

The proposed security-plan spelling has no enforceable security semantics in
the current planner. `normalize_required_tier` deliberately reads only the
first word inside `required(...)`; its docstring calls remaining text a lens
annotation. `normalize_required_obligations` likewise sees one Internal-tier
clause unless `+` introduces distinct obligations. An ordinary Internal pass
therefore clears `required(Internal, security)` today, with no Security Review
record, protocol, high-capability role, or separate falsification obligation.
That contradicts item 4's claim that high-risk Security Reviews are unchanged.

Define the replacement security obligation: its record grammar, reviewer role
and fresh-context requirement, preflight, and predicate that blocks advancement
until it lands. It may be same-agent-type if the recorded Maintainer direction
requires that, but it cannot be an ignored annotation. Pin the directed pair:
an ordinary Internal pass cannot clear a security-plan requirement; the
required Internal Security Review record does. Keep proposal/code triggers
distinct and intact.

#### RERP-02 — BLOCKING: active and archived legacy records have incompatible grammars, not one warn-and-reinterpret path

`required(External)` is a plan header, while `Plan readiness:` is a
proposal-review field. The proposal says either line in an active artifact
warns and is read as `required(Internal)`, but a readiness finding cannot be
read as a plan declaration. The planner's shared External vocabulary also
validates proposal-review tiers and event records that must survive. Deleting
External-tier validation without a type-scoped replacement can invalidate the
External proposal floor item 4 keeps or discard archived metric evidence. No
inventory or migration rule states which record supplies the new Internal
requirement, how an inherited basis retires, or what `scan`, `next`, and metrics
report during the transition.

Specify separate dispositions for active External plans, active proposals with
readiness records, and immutable archives. Name parser branches and output
fields that remain proposal-External versus plan-Internal, then test each class
across `scan`, `next`, and longitudinal metrics. A warning cannot manufacture a
different artifact type.

#### RERP-03 — BLOCKING: the relationship section is stale and omits the accepted-scope migration it now requires

`convergent-lifecycle` is no longer awaiting review: commit `47315b6` records
the Maintainer Decision accepting Revision 2. Its accepted contract says a
declared `required(External)` floor is non-downgradable and that its own derived
plan takes that External review under the current rule. This proposal instead
uses a counterfactual — "if accepted first" — and declares the later plan
Internal. That is a change to accepted scope and a live review obligation, not
a choice between two unaccepted baselines.

Replace the hypothetical with a commit-bound migration: identify the accepted
commitments superseded, quote the Maintainer authorization allowing the
review-floor change, name the new plan declaration/linkage, and state whether
the former External obligation is waived or remains. A new rule can govern
future plans after acceptance, but cannot silently make itself the first
beneficiary or rewrite a sibling's accepted floor.

#### RERP-04 — BLOCKING: the falsification baseline is wrong and the grep cannot prove the claimed removal

The stated instrument does not reproduce its claim. At the reviewed commit,
the proposal's governing-surface query for `Plan readiness` or
`required(External)` over its named roots, excluding this proposal, matches
**17 files**, not 24. Its post-change empty-result test also cannot show that
External validation remains for proposal reviews/events while being removed
only for plans; lexical absence cannot distinguish correct type scoping from
deleting the shared vocabulary.

Publish the literal command, exclusions, and checked-in expected file list,
corrected to 17 or accompanied by the different measurement that yields 24.
Pair it with behavioral oracles: an External proposal review and archived
External event still parse, while a new plan receives the accepted legacy
disposition. Mutate each property in a way the grep misses and the oracle
catches.

#### RERP-05 — BLOCKING: the mandatory security preflight is absent

This proposal has no `#### Security preflight` section or N/A statement. The
template requires one or the other, and this is not credibly N/A: it changes how
a high-risk surface's Security Review is declared, selected, and allowed to
clear a plan. RERP-01 gives the concrete failure mode — an ordinary Internal
pass can impersonate the proposed security review.

Answer S1--S5 for the replacement security-review record and legacy parser:
classification source, mutation proving a standard Internal pass cannot clear
it, triggering command and artifact scope, failure direction, remaining
attacker capability, and the Security Review/current-contract verification the
implementation requires.

### Coverage and recommendation

**Covered**: the complete opened contract at
`e753882621b4a8da245eb4e350003084c1efaec7`; review-allocation and Security
Review rules in `AGENTS.md`, `doctrine/dual-review.md`, and `doctrine/roles.md`;
live and shipped templates; planner tier/multi-obligation parsing and review
predicate; the stated governing-surface grep; and the accepted
`convergent-lifecycle` Decision history.

**Not covered / low confidence**: no replacement parser, migration fixture, or
security-plan record exists yet, so proposed behavior cannot be executed. I did
not run the full suite; this is a pre-implementation review.

**Second-round recommendation**: recommended. Security-plan review and the
accepted-artifact migration must be testable before this subtraction is decided.
