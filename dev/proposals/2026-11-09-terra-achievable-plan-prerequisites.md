# Keep implementation plans achievable with available prerequisites

**Author**: GPT-6.1 Terra (Proposal author)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Queue work awaiting calendar observations or scheduled human actions instead of making it a normal implementation-plan prerequisite.

## Decision summary

The metering plan included an unstarted seven-day private-data trial, so agents
could finish the software and still be unable to finish the plan. The Maintainer
has moved that trial to the queue. Clarify the existing SMART planning rule:
specific, measurable, achievable, relevant work with a realistic time estimate.
Update the existing instructions and templates, with no new tool, form or
approval step. Passive calendar waits and scheduled human operations stay on
the board until their prerequisites are available. Required evidence cannot be
silently dropped to make a plan finish.

## Context

The accepted [atomic-plans proposal](archive/2026-11-05-codex-atomic-implementation-plans.md)
already requires independently finishable outcomes using available capabilities,
evidence and authority. The plan templates nevertheless encourage authors to
design Maintainer-gated chunks. The metering plan made both private approval
and a seven-day observation a final completion dependency. On 2026-11-09 the
Maintainer directed that this work be queued and that plans be SMART.

## Proposal

Clarify the existing Scope, Sequence and Acceptance guidance in governing
instructions, proposal/plan templates and their published explanation. At plan
opening, use prerequisites already available: do not routinely schedule passive
calendar waits, private-access approvals or Maintainer-only operations as
implementation chunks. Keep such outcomes queued with their source, owner
and concrete restart condition. Open their work when ready.

Preserve unexpected escalation and permission boundaries. If later inspection
finds a missing prerequisite, stop that work and obtain the existing required
scope disposition; do not automatically defer an accepted criterion. A failed
check, defect, missing functional or scientific evidence, or required review
still prevents claiming the affected outcome complete. A genuine scientific
experiment or slow automated check can be planned when its resources and
authority are available; elapsed runtime alone does not make it a follow-up.
For example, an agent can execute and analyze an approved, ready scientific
observation even when measurement spans several days: the observation is the
work, and its duration belongs in the estimate. Waiting for future ordinary
usage and a still-ungranted private-data approval, as in the meter trial, is
not ready implementation work. If an unavailable observation is required to
substantiate an implementation's promised result, that result remains
unverified; queue the outcome before opening, or seek a named scope disposition
if already active.
Use the existing realistic work-window estimate, not an arbitrary deadline
that permits unfinished work.

## Rationale

Planning should expose unavailable prerequisites before implementation starts.
The existing board and sections can do this without another tracker or SMART
checklist. The completed software and any unmeasured benefit remain distinct
claims.

## Alternatives considered

Enforce only the present wording: no documentation cost, but the template still
invites the same final human gate. Clarifying those existing prompts is
recommended because it resolves the contradiction with little continuing
burden. A mandatory SMART form or automated gate adds fields and maintenance
without establishing whether a plan is achievable.

## Documentation / doctrine surface

Use exact patches in `AGENTS.md` and its shipped copy, the proposal and plan
template pairs, and the relevant planning explanation in
`docs/methodology/lifecycle.md` and `docs/methodology/plans.md`.
Preserve installed/self-hosted differences and unrelated rules. No runtime
behavior, schema, new mandatory header or private access changes.

## Evidence / verification plan

### Tests required

Run prose gates and the tests selected for the changed passages. Preserve
template fields, merge slots and actual install/copy correspondence. An
independent reader must distinguish an unavailable private trial from a
ready-to-run scientific calculation and an unexpected permission escalation.
Do not add wording pins. Required high-risk reviews remain applicable.

### Examples / smoke checks

During the existing closeout of the five current implementation plans, inspect
their remaining prerequisites for the same error and group material choices
for the Maintainer. This is a one-time application of the requested correction,
not an additional review pass or recurring audit. Historical passages
superseded by a later disposition are not open work.

#### Security preflight — five questions, answered in writing

- **S1:** Committed instructions, accepted scope and available resources inform
  planning; target documents do not confer permission to change their own gates.
- **S2:** Deleting an owed check under the guise of queueing would falsify the
  clarification. The independent example read and change verification have not
  run; no preventive guarantee is claimed.
- **S3:** The author follows the existing template at plan opening and the usual
  reviewer checks its achievable outcome. Installed guidance must say the same;
  the existing board carries unavailable outcomes, not a new gate.
- **S4:** Unavailable authority stops the affected action. Only the Maintainer
  may concede accepted scope; no automatic archive or permission follows.
- **S5:** A plausible but false claim that resources are available can still
  mislead review. This remains a judgment rule, not enforced containment.

### Independent scientific check

N/A: no scientific equation, assumption or result changes.

## Signals the change is wrong

Revise if readers treat a failed required test as a queueable human chore, waive
missing scientific evidence, or think ordinary unexpected permission questions
are forbidden. A new recurring form would also miss the intended simplification.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance for the named shipped instruction/template
surfaces; the existing heavy review and verification requirements apply.

## Review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

**Reviewed commit:** `31f4a55b`. **Tier:** usual. **Findings:** raised.
**Verdict:** REVISE.

**Foundations**

1. **Should this happen as framed?** Clarifying unavailable prerequisites is
   justified by the metering trial and the Maintainer's direction; preserve
   checks and existing scope authority -- `97a0eab3`, Proposal.
2. **Best alternative.** Apply the accepted atomic-plans rule without a new
   form or gate; its existing available-prerequisite and no-scheduled-human
   provisions already cover much of this -- `dev/proposals/archive/2026-11-05-codex-atomic-implementation-plans.md`, Proposal 1–6.
3. **What would show it wrong?** Apply the proposed wording to a ready scientific
   observation that must run over calendar time and to a future private trial;
   if it drops the former's required evidence or admits the latter as ready,
   the distinction fails -- Proposal and Evidence / verification plan.

**Finding (blocking):** “future calendar observations” could include an
experiment with available resources that necessarily observes future days,
while the following paragraph permits a genuine experiment. Resolve the
boundary and provide both examples so required scientific evidence cannot be
misclassified as a queueable wait. This closes when the operative rule makes
the distinction and retains the existing prohibition on waiving checks.

**Advice (non-blocking):** Explain the value of reviewing all five current
plans, or narrow it to an existing review where relevant. The accepted atomic
proposal avoids a mass rewrite and extra clearing review; do not turn the
scan into a new recurring gate or retroactively narrow scope.

**Functional prose:** The intended rule adds a restriction on planned waits;
existing scope, review and evidence safeguards are explicitly retained, but
the ambiguous observation boundary above could weaken evidence in practice.

**Coverage:** Read the committed proposal, accepted atomic-plans proposal,
current proposal and plan templates, and Maintainer direction at `97a0eab3`.
No implementation, security review, tests or exhaustive current-plan audit.
**Elapsed:** about five minutes. **Tokens:** unknown.


## Security Review -- GPT-6.1 Sol (Security Reviewer, High) -- 2026-11-09

**Foundations**

1. **Should this happen as framed?** Yes: exposing unavailable authority before
   opening work improves feasibility while retaining required evidence and
   unexpected permission stops -- Proposal at `621fe66f`; accepted
   `dev/proposals/archive/2026-11-05-codex-atomic-implementation-plans.md`,
   Proposal 3–6.
2. **Best alternative.** Enforce the existing atomic-plan rule case by case;
   this avoids edits but leaves templates inviting scheduled human gates, so
   clarify those existing prompts without another tracker --
   `dev/plans/_template.md`, Sequence, and its shipped counterpart.
3. **What would show it wrong?** Apply the final wording to an approved
   multi-day scientific observation, an unapproved future-use trial and an
   unexpected permission escalation: lost evidence, premature completion or
   continued unauthorized execution falsifies it -- Proposal and Evidence /
   verification plan at `621fe66f`.

**Reviewed commit:** `621fe66f2d0bf0d123d156bfc411ef74e243093a`.
**Tier:** Security Review. **Findings:** none. **Verdict:** ACCEPT.

Elapsed time alone cannot remove work. An authorized, resourced experiment
remains implementation work;
waiting for unavailable ordinary usage or private permission does not become
ready through scheduling. Missing evidence still prevents claiming the
promised result verified. For active work, the named scope disposition remains
necessary; a board row does not grant it.

The meter's quoted waiver at `97a0eab3` and queue at `b1ca6023` illustrate a
specific authorized change, not standing permission to defer checks. Keeping
Tokens and Elapsed avoids claiming the unperformed comparison established
accuracy. S1–S5 correctly separate documentary judgment from enforced
containment and retain the Maintainer's authority. The five-plan inspection adds no recurring audit.

**Functional prose:** The proposal restricts deliberately planned unavailable
prerequisites; it explicitly preserves scope, evidence, scientific checks and
unexpected authority boundaries. Paired wording must retain
those safeguards and installed/self-hosted differences.

**Coverage:** Read the committed revision, usual finding, accepted atomic
proposal, current local/shipped plan guidance and Meter disposition/queue.
No implementation, tests, mutations or exhaustive five-plan audit performed;
final wording and affected verification remain due. **Elapsed:** about five
minutes. **Tokens:** unknown.

## Response -- GPT-6.1 Terra (Proposal author) -- 2026-11-09

Accepted the usual review's boundary finding. Revision `621fe66f` replaces the
broad observation language with passive unavailable waits and gives both
examples: an approved, ready scientific observation is work even across days;
the unapproved future-usage meter trial stays queued. Missing evidence still
prevents claiming the promised result. The later Security Review accepts that
distinction with no findings.

Accepted the advice to avoid a new audit: the existing closeout will apply this
one-time correction to current plans; no extra clearing pass, recurring form or
automatic checker is proposed. The opening's stated heavy obligations remain.

**Withdrawn / superseded commitments:** None beyond those operative
clarifications; no accepted check or authority boundary is removed.
**Elapsed:** about five minutes. **Tokens:** unknown.
