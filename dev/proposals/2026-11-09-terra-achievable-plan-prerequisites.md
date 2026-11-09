# Keep implementation plans achievable with available prerequisites

**Author**: GPT-6.1 Terra (Proposal author)
**Status**: awaiting-review
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
approval step. Future observations and scheduled human operations stay on the
board until their prerequisites are available. Required evidence cannot be
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
opening, use prerequisites already available: do not routinely schedule future
calendar observations, private-access approvals or Maintainer-only operations
as implementation chunks. Keep such outcomes queued with their source, owner
and concrete restart condition. Open their work when ready.

Preserve unexpected escalation and permission boundaries. If later inspection
finds a missing prerequisite, stop that work and obtain the existing required
scope disposition; do not automatically defer an accepted criterion. A failed
check, defect, missing functional or scientific evidence, or required review
still prevents claiming the affected outcome complete. A genuine scientific
experiment or slow automated check can be planned when its resources and
authority are available; elapsed runtime alone does not make it a follow-up.
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

Review the five current implementation plans for the same prerequisite error;
record any material remaining scope choice together for the Maintainer.
Historical passages superseded by a later disposition are not open work.

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
