# Bounded execution retries for adopters

**Author**: Codex Terra Medium
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Give adopters two feedback-driven attempts to correct an execution mistake before escalating, without weakening capability or review safeguards.

## Decision summary

The installed rule calls for immediate escalation when lower-tier work fails a
check. Issue [#51](https://github.com/MSUHydrogeology/cairn/issues/51) reports
that ordinary setup mistakes in reviewed implementation work prompted extra
handoffs. Ship Cairn's local bounded retry rule to adopters for v0.7. Two
additional attempts may cost time; they may also avoid unnecessary handoffs.
Neither a saving nor a speedup has been measured.

## Context

The issue describes evidence-persistence and test-environment mistakes, not a
controlled cost comparison. `templates/core/AGENTS.md` says failed lower-tier
work goes up one tier; `docs/methodology/roles.md` separately addresses work
below its floor and review-blocking defects. Cairn's own `AGENTS.md` now permits
two retries for correctable execution errors. `dev/PLANNING.md` item 3 records
the Maintainer's local-only direction and leaves adopter implementation to a
separate proposal. The readable-plans proposal addresses issues #46-#50; this
proposal does not reopen its plan-quality or cheap-follow-up scope.

## Proposal

For v0.7, align the installed governing rule and published methodology with
the local execution rule. For a correctable execution error at or above the
task's capability floor, permit at most two same-tier retries after the initial
failed attempt. Each uses concrete recorded failure feedback, retains earlier
failure evidence, and reruns only the affected check. After both retries fail,
rerun once one tier up. Escalate immediately when the failure shows the task
exceeds the assigned tier. Work below its floor is not eligible for this
budget; preserve the existing below-floor and stronger-check conditions.

Retries do not substitute for independent review or Security Review, waive an
accepted criterion or required check, expand authority, cross a plan fence or
data-governance boundary, or change the capability floors. Establish the effects
of an earlier attempt before repeating a potentially destructive operation.
Distinguish execution correction from a review finding and from evidence that
the task needs higher capability; do not turn this into a general review retry
policy. No new workflow, ledger, tool, or recurring process is proposed.

The outcome depends on an accepted Decision and reviewed plan. Coordinate
wording with concurrent work on the existing proposal without making that
proposal or its implementation a prerequisite for delivering this outcome.

## Rationale

Feedback can make a small execution correction possible at the assigned tier;
the limit prevents indefinite repetition. Immediate escalation remains for a
capability mismatch. The rule is bounded permission, not permission to bypass
the checks or authority that make the original work safe.

## Alternatives considered

Keep the installed immediate-escalation rule: no doctrine or test changes,
but correctable mistakes continue to incur the handoffs reported in #51.
Allow unlimited retries: simpler to state but loses a clear escalation point
and may prolong failed work. Neither has measured cost data here.

## Documentation / doctrine surface

Put adopter prescription in `templates/core/AGENTS.md` and reconcile
`docs/methodology/roles.md` with it. Inspect `dev/modules/model-selection.md`
and its shipped twin `templates/modules/team-gated/model-selection.md` for
conflicting claims, updating both only as needed. Preserve the independent
stronger-check rule, including its same-tier exclusion; that is not this
execution retry. Do not edit Cairn's local rule unless a genuine inconsistency
requires separate authorization. Inventory all affected readers and byte pins
before implementation; keep the surface minimal.

## Evidence / verification plan

### Tests required

Map changed files to their actual readers with `python tools/test_tiers.py for`
and inspect the triggers. In particular, examine
`bootstrap/tests/contract/test_model_tier_rule_ships.py` and
`bootstrap/tests/test_review_stance_in_shipped_files.py` for the distinct
stronger-check and escalation assertions; update only assertions made stale by
the accepted rule. Exercise an installed profile through the scaffold's real
entry point and verify the resulting governing text, including profiles without
the optional model-selection module. Check both module twins if changed.
Add focused coverage for the retry limit, immediate capability escalation,
below-floor exclusion, preserved safeguards and prior-effect rule where the
existing checks cannot detect their loss. A missing safeguard, a contradictory
installed instruction, or a retry permitted below the floor falsifies delivery.

### Examples / smoke checks

Run the applicable claim, link, snippet and neutrality prose gates and tests
that read changed files. Follow the doctrine-evolution gate in
`docs/methodology/rationale.md`; the plan must identify its trigger and result.
Use the project's scoped iteration and final wide Boundary B requirements for
the protected doctrine and template surfaces. Full certification remains a
separate authorized ceremony.

#### Security preflight

S1: The Maintainer's Decision supplies authority; task assignment, failure
evidence and capability floors inform an agent's retry judgment. The agent
performing the work supplies failure evidence, which is not independent proof.

S2: Proposed checks must fail when a retry limit or safeguard is removed from
each applicable installed surface; implementation must run and record those
mutations. No such mutation has been run for this proposal.

S3: The plan must trace each selected test and prose gate from its command and
trigger to its actual input set, and compare that set with the installed rule.
The final adopter-facing wording does not exist yet, so agreement is unverified.

S4: An unclear failure or unmet check does not grant authority to proceed; a
demonstrated capability mismatch escalates immediately. This prose rule does
not mechanically enforce classification or recovery from partial effects.

S5: An agent can misclassify a failure or misstate evidence and retry despite
the rule. Independent review, required checks and existing authority fences
remain necessary; this proposal does not claim to prevent dishonest behavior.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or reconsider if review shows the rule permits below-floor work,
weakens an independent check or fence, or cannot be expressed consistently in
the installed and published guidance without adding disproportionate process.
Repeated misclassification or increased recovery burden would also count
against it; neither has been measured.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance

Published methodology and shipped governing doctrine are protected surfaces.
They trigger heavy tier, the usual proposal review plus a separate Security
Review, and internal plan and Security plan reviews. This draft authorizes no
Decision, implementation, release, push, waiver or change to another proposal.

## Review -- Codex Terra Medium (independent reviewer) -- 2026-11-05

Reviewed commit: 5091888d7e5a75cc5b848480c2bcef60482035d6

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: two feedback-driven retries address reported execution mistakes while retaining escalation and independent assurance; savings are unmeasured -- Proposal, Context and Security preflight.
2. **Best alternative.** Keep immediate escalation: it avoids changing doctrine but retains the reported handoffs and their unmeasured cost -- `templates/core/AGENTS.md`, Model tier; Alternatives considered.
3. **What would show it wrong?** A real installed-profile test allowing a third same-tier retry, below-floor work, a bypassed check or fence, or a conflicting escalation instruction would falsify delivery -- Evidence / verification plan; `docs/methodology/roles.md`, Escalation.

The limit is two attempts after the initial failure, each with retained evidence
and affected-check feedback, followed by one higher-tier run; capability
mismatch escalates immediately. Review findings, authority, required checks,
data governance and prior effects remain distinct safeguards -- Proposal.
The independent stronger-check rule retains its same-tier exclusion --
Documentation / doctrine surface; `docs/methodology/roles.md`, Model selection.

**Non-blocking:** The readable-plans proposal item 4 preserves the existing
one-tier-up retry, while this proposal changes its timing. Recommend explicitly
accounting for either acceptance order and reconciling both outcomes without
weakening complete-plan or immediate capability-escalation requirements;
close by identifying the coordinated wording or its implementation owner --
`dev/proposals/2026-11-04-codex-readable-plans-and-finish-work.md`, Proposal 4.

**Coverage:** Read the committed proposal, local and installed retry rules,
published roles, model-selection wording and the overlapping proposal. Did not
run future installed-profile or mutation checks, assess actual retry frequency,
or conduct the separate Security Review.

## Review -- Codex Sol (Security Review) -- 2026-11-05

Reviewed commit: `5091888d7e5a75cc5b848480c2bcef60482035d6`

**Model**: gpt-6.1-sol (high). **Tier**: Security Review.
**Findings**: one non-blocking clarification. **Verdict**: ACCEPT.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: a two-retry ceiling gives ordinary execution errors a bounded correction path while leaving capability and authority gates intact -- Proposal; `templates/core/AGENTS.md`, Model tier.
2. **Best alternative.** Keep immediate escalation, which changes no rule but preserves the extra handoffs reported in issue #51 -- Alternatives considered; `templates/core/AGENTS.md`, Model tier.
3. **What would show it wrong?** An installed copy that allows a third retry, retries below the floor, or treats a partial failed operation as safe to repeat would falsify the safeguard -- Evidence / verification plan, Tests required.

The proposal correctly separates an execution mistake from a review defect, a capability mismatch, a plan fence and a data-governance boundary. S1 and S5 admit the important limit: the same agent classifies its failure, so the prose rule cannot authenticate that classification. Independent review and the original required checks remain the backstop. The implementation tests must mutate both the installed core rule and any changed module twin; a test that only reads Cairn's local rule would not establish adopter delivery.

**SR1 (non-blocking):** Clarify in the plan that "reruns only the affected check" applies to the correction loop, not final Boundary B or an otherwise required safety/security check. The proposal says those checks remain due, but the two sentences could be read apart -- Proposal; `AGENTS.md`, Verification. Close with one explicit sentence, not a new mechanism.

**Coverage:** Committed proposal, local/shipped rules, model-selection wording and named test owners. **Not covered:** real adopter installation, mutation results, measured retry cost, future plan/code or full suite.
