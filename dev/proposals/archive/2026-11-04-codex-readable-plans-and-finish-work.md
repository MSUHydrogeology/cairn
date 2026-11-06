# Make plans readable and finish the work

**Author**: Codex Terra (ordinary proposal author, medium)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy -- the changes reach shipped doctrine and templates, named high-risk surfaces; the authoring model floor is separate.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Make decisions easier to read, plans executable by their assigned tier, and completion records and cheap follow-ups timely.

## Decision summary

Important explanations can disappear during revision, and small finishing
tasks can be left behind. Make authors and reviewers read a proposal's top as
the decision-maker will, keep explanation when shortening text, specify plan
chunks for their implementer, and finish cheap follow-ups and update the
roadmap and changelog when work finishes. This adds judgment and coordination
at existing steps, not a new checklist or tool. Parallel writers must still
coordinate shared records; finishing an entry may incur existing lockfile work.
Requiring cheap advice to be fixed reduces authors' discretion and can add
tests, review, coordination and delay for each follow-up.

## Context

The board groups [issues 46-50](../PLANNING.md) as item 3. Their reports are
adopter accounts, not measurements of all projects: [46](https://github.com/MSUHydrogeology/cairn/issues/46)
reports delayed entries; [47](https://github.com/MSUHydrogeology/cairn/issues/47)
an unreadable proposal top; [48](https://github.com/MSUHydrogeology/cairn/issues/48)
explanations trimmed to a perceived cap; [49](https://github.com/MSUHydrogeology/cairn/issues/49)
underspecified plan chunks; and [50](https://github.com/MSUHydrogeology/cairn/issues/50)
cheap items deferred. Their issue bodies were read on 2026-11-04.

The accepted [leaner-reviews proposal](archive/2026-11-03-claude-leaner-reviews.md)
already makes proposal and plan budgets targets and allows revisions to grow
for accepted findings. The current templates reflect that; this proposal adds
what to preserve when trimming, not another budget. The accepted
[completion proposal](archive/2026-11-03-codex-implementation-plan-completion.md)
separates human trust and release operations from agent-owned completion; it
does not excuse unfinished agent-owned work. The plan template already requires
Maintainer authorization and one of three reasons for a deferral. The reported
gap is that this limit appears late, without an earlier duty to finish cheap
work. Issue 46 also notes parallel changelog lockfile conflicts; this proposal
does not change that separate mechanism.

## Proposal

1. At the commit or plan archive that finishes work, update the applicable
   roadmap and changelog, coordinating their existing shared-file ownership.
   The end-of-session routine checks for omissions; it is not the normal time
   to reconstruct entries. Do not require an entry for work the project's
   existing rules do not record. Coordinate this wording with the accepted
   completion work; human-only operations remain separately tracked and
   unpassed until performed.
2. Before reading the body or code, a proposal reviewer reads the title,
   one-line summary and decision summary cold, states the gist in one or two
   sentences, and names as a finding where the body was needed to understand
   the top. After each revision, the author rereads and, where needed, revises
   the top as a whole. This is a reading judgment, not a score or new field.
3. In proposal and plan templates, preserve the accepted target and revision
   rules. When shortening, remove detail already available elsewhere, such as
   identifiers, file-level specifics and citable evidence, before explanation;
   shorten the decision summary last. A modest overrun that preserves clarity
   is preferable to obscure compression.
4. Plan review asks whether each chunk can be executed at its assigned tier
   without the implementer making design decisions, and names the missing
   specification. Return an underspecified chunk to the plan author, not a
   higher tier as a substitute for a complete plan. Preserve model floors,
   authority boundaries and the existing one-tier-up retry after a failed check.
5. State near chunks and code-review response that cheap follow-ups are done
   before archive; deferring one is a plan defect. Define cheap as a few
   person-steps, no new Decision, no new public name beyond the plan's, and a
   test fitting its existing test files. Count person-steps, not machine time.
   Code review identifies cheap findings and advice; the response accounts for
   each as fixed or under an existing deferral reason. A defer without the
   Maintainer's verbatim authorization is invalid. This does not authorize
   scope expansion, a boundary crossing, or waiving a required check: stop for
   the existing authority when needed. Non-cheap advice retains its existing
   disposition routes.

## Rationale

These additions put existing intentions where authors and reviewers can act
on them. They cost a cold read and finish-time coordination, but avoid a new
record, scoring system or routine. Even small fixes can repeatedly require
tests and review before archive, with coordination and delay; their frequency
and total cost are unmeasured. The duty trades author discretion over cheap
advice for finishing it. The cheap-work definition is a practical boundary,
not permission to make unreviewed changes outside the plan.

## Alternatives considered

Do nothing costs no edits but leaves the reported timing and readability gaps.
Only repeat the existing deferral and word-budget rules is cheaper to write but
does not establish the earlier duty, cold read or trimming priority. A new
checklist or runner adds upkeep without proving comprehension.
Retaining the existing one-line author disposition for nonblocking advice is
lighter and preserves discretion, but loses the duty to finish cheap advice.

## Documentation / doctrine surface

Route cross-cutting instructions to `AGENTS.md` and its shipped twin; author
and reviewer guidance to `dev/agent_collaboration.md` and its shipped twin;
proposal and plan wording to their live and shipped templates. Update relevant
`docs/methodology/` descriptions and session guidance where needed to avoid
contradiction, and coordinate shared edits with item 4. Do not edit archived
records. Apply the doctrine-evolution gate and retain existing authority,
review and verification requirements.

## Evidence / verification plan

The plan maps each changed instruction, reader and byte pin, including live
and installed twins, to existing test homes and public entry points. Extend
existing `bootstrap/tests/` doctrine, template or install tests only for
plausible uncovered faults; no per-function quota. Exercise a fresh scaffold
installation and inspect the actual emitted instructions. In separate copies,
remove or reverse each new obligation and show the relevant existing-home
behavior or assertion fails; a text match alone cannot establish that a person
understood the prose. Preserve the completion proposal's own required controls.
Run affected tests selected by `tools/test_tiers.py for`, plus applicable
claim, link, snippet and neutrality gates; final Boundary B is wide for this
doctrine surface after review. Certification remains at its existing triggers,
not an automatic full-suite run for this proposal.

### Tests required

The plan identifies exact existing nodes and scaffold entry points after mapping
the final changed files; missing coverage is added to their existing homes.
An installed twin retaining contrary wording, or a negative control that does
not fail, falsifies the coverage claim.

### Examples / smoke checks

Use `python scripts/check_cairn.py`, the relevant prose gates and a fresh
`bootstrap/scaffold.py` install in a disposable copy. Verify finish-time and
session wording together, including absence of contradictory instructions.

#### Security preflight

**S1:** The Maintainer supplies Decisions; authors supply plans, records and
prose, and reviewers read committed evidence. Those records confer no new
authority. **S2:** Deletion and contrary-wording mutations are proposed above;
they have not been run. **S3:** The affected-test selector and scaffold install
select the implementation's mapped surfaces; the intended adopter instruction
is to update applicable roadmap and changelog entries when work finishes.
Implementation must show the selected checks and installed wording agree.
**S4:** No parser or execution fallback changes; missing permission or required
evidence still stops work. **S5:** This assumes cooperative agents; a dishonest
agent can misstate a review or record, so existing controls remain necessary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Readers still need the body to explain the top, plan chunks require unplanned
design, cheap work accumulates at archive, or finish-time entries cause
uncoordinated overwrites. Installed instructions contradict the live rules or
the new wording is used to bypass authority or checks.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. Shipped authoring templates and governing
doctrine are protected surfaces; usual and Security Reviews are separate.

**Elapsed**: unknown. **Tokens**: unknown.

## Review -- Codex Terra (usual proposal reviewer, medium) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Mostly: the five requested outcomes are present, but the decision-maker needs the cost of making cheap advice mandatory, not just coordination and a cold read -- Proposal 1-5; issues 46-50; finding below.
2. **Best alternative.** Keep the readability, assigned-tier and timely-record changes, but leave non-blocking advice to the author's one-line disposition; that loses the requested duty to finish cheap advice and risks the same accumulation -- issue 50; `AGENTS.md`, Review; leaner-reviews Decision.
3. **What would show it wrong?** An installed instruction that allows a required check to be transferred to a board row, or a cheap suggestion that triggers work beyond its authority, would defeat completion and scope safeguards -- completion proposal, Alternatives considered; Proposal 5; test installed wording and a representative advice response during implementation.

```text
Reviewed commit: 7b63e78b
Target: opening proposal, issue outcomes, scope, readability and costs
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Verdict**: REVISE; one non-blocking finding.

**Finding -- decision cost.** Proposal 5 requires cheap findings and advice to be fixed or deferred with Maintainer authorization, whereas `AGENTS.md` permits a one-line disposition of other advice. Even a few person-steps can add tests, review, coordination and delay across many suggestions; the summary and rationale name only a cold read and coordination. State this recurring cost and the loss of author discretion plainly for the Decision, with the existing safeguards and the lighter alternative. No estimate is measured here.

The opening says the project will make decisions easier to read, specify executable chunks, and finish small follow-ups and records promptly. Its meaning is understandable now, but this was not a genuine cold read: I read the body before recording that gist. A later reader should make that judgment independently; this is not evidence that the proposed habit was exercised.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Read the committed proposal, current proposal template, accepted leaner-reviews and completion contracts, and issue bodies 46-50. Did not assess Security Review, implementation, installed output, actual future comprehension or run a suite; no Decision or authority granted.

## Review -- Codex Sol (separate Security Review, high) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes: make decisions understandable, chunks executable, and finishing timely without granting new authority -- Proposal 1-5; issues 46-50; `AGENTS.md`, Roles and Working tree and commits.
2. **Best alternative.** Keep one-line dispositions for optional advice while adopting the other changes; this costs less but loses the mandatory cheap-advice outcome, a concession only the Maintainer can make -- Proposal 5; `dev/agent_collaboration.md`, The review loop and scope-reduction trap.
3. **What would show it wrong?** During implementation, challenge installed wording with a cheap out-of-scope suggestion, a failed implementation check proposed for board transfer, and an underspecified chunk assigned upward; any permitted bypass falsifies the contract -- Proposal 4-5; completion proposal, Alternatives considered; Evidence / verification plan.

```text
Reviewed commit: 7b63e78b76bafa15315bee5bbaea2bcb5228cdac
Append base: 1eb95c2dbb6977f8e590b171ecf0d446d47410a6
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT -- proposal only.

S1/S4 preserve Maintainer Decisions, permission stops and required evidence;
author-written records are not authority. S5 correctly leaves dishonest
records outside this wording's protection. S2/S3 describe future mutations
and installed-output mapping, not completed checks.

I tried contrary readings: cheapness permitting a new private function under
the narrow defect-fix exception; archive making a baseline operation passed;
and model escalation substituting for specification. Proposal 5 retains
existing authority, item 1 retains unpassed operations, and item 4 expressly
rejects the substitution. `AGENTS.md` retains the narrower defect exception,
review caps and data-governance floor. Board parsing only displays declarations
(`tools/board.py::_roadmap_waits`); the accepted completion contract forbids
transferring agent-owned failures.

Mandatory cheap advice reduces discretion, but does not authorize recursive
review or scope expansion. The usual review's cost concern remains; this pass
does not dispose of it. No baseline outcome is removed. Live/shipped routing
and contrary-wording controls remain owed, not demonstrated.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Coverage**: Separate committed copy, S1-S5, current templates and live/shipped
safeguards, issue bodies 46-50 and both accepted contracts. Not covered: genuine
cold-read comprehension, implementation, installed-output mutations, suites,
baseline authentication or release operations; no authority granted.

## Response -- Codex Terra (proposal author, medium) -- 2026-11-04

- **Decision cost:** Accepted. The summary and rationale now name the recurring
  cost and reduced discretion; Alternatives states the lighter one-line
  disposition and what it loses. No estimate of the cost is claimed.
- **Security Review:** No findings; its implementation challenges remain
  evidence to address, not completed checks.

**Elapsed**: unknown. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Decision -- gpt-6.1-sol (High), delegated decision-maker -- 2026-11-06

**Model**: gpt-6.1-sol (High).
**Authority**: temporary Maintainer delegation -- chat, 2026-11-06, relayed by the coordinating agent. This is the Sol agent's decision under that explicit exception, not a claim that the Maintainer selected this option personally.

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

**Tier**: heavy.
**Elapsed**: unknown. **Tokens**: unknown.
**Source**: operative proposal, appended usual and Security Reviews, and author responses as committed at `831d0e3b`; the proposal bytes remained unchanged through `8380bc9b`.

**ACCEPTED.** Choose all five readable-plan and finishing outcomes for v0.7, including the duty to finish cheap follow-ups within existing authority.

**Reason.** The proposal addresses the five reported gaps at the existing
writing, review and completion steps. I accept the usual review's now-explicit
tradeoff: cheap advice reduces author discretion and can require repeated
testing, review and coordination. The separate Security Review found no new
permission to expand scope or transfer failed agent checks to a human wait.

**Options and costs.** Keeping readability, assigned-tier specification and
timely records while retaining one-line optional-advice dispositions is the
least involved credible alternative. It preserves discretion and reduces
follow-up work, but loses the opened duty to finish cheap advice. Repeating the
existing word-budget and deferral rules costs less wording work but does not
supply the cold read or trimming priority. The selected outcome adds those
judgments and finish-time shared-record coordination; the frequency and cost of
mandatory small fixes are unmeasured. It adds no tool, checklist or routine
human ceremony; an exceptional deferral still needs the existing Maintainer
authorization recorded in its plan, with no predictable new count.

**Delivery fence.** Cheapness cannot authorize new scope, a trust-boundary
crossing, a waived check or an unspecific plan. Preserve the narrower defect-fix
exception and model floors. If adopter retries are also accepted, reconcile the
shared escalation wording as that proposal specifies: complete plans remain
mandatory and correctable execution errors receive only its bounded budget.
Required failed checks remain implementation work; applicable finish-time
records remain coordinated, not end-of-session reconstruction.

Accept the complete operative scope and its stated limitations; no outcome or
required check is waived. High-assurance treatment, both required plan reviews,
ordinary and separate Security code reviews, mapped checks and final wide
Boundary B remain due. Proposal controls described as unrun remain unrun.
This authorizes reversible local planning and implementation, not an actual
release, push, publication, signing, trust-ref movement, credentials/private-log
access or other hard-to-undo action. Those operations remain with the Maintainer.


## Doctrine gate disposition -- GPT-6.1 Sol (High) -- 2026-11-06

**Disposition:** allow this accepted five-outcome bundle (`27300e1e`) to proceed
through reversible local planning, implementation, review and verification,
including every named local/shipped copy, despite the unmet doctrine-rate-limit
evidence prerequisite. This is my one-bundle exception under the Maintainer's
temporary delegation, not a finding that the gate passed or the incident was
high-risk. The original status, reviews and Decision remain intact.

**Authority:** Maintainer chat, 2026-11-06:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

**Evidence:** the [doctrine-evolution gate](../../docs/methodology/rationale.md#how-the-doctrine-evolves-under-evidence)
requires qualifying recurrence within a deployment-pinned tracker window or
genuine routine-close synthesis.
The recorded issue bodies do not establish either: #47/#48 may describe one
proposal episode; #46 is one report, #49 has no occurrence count, and #50 names
two plans without the qualifying window/close record. No security/data-loss
basis supports the high-risk bypass. No synthesis or tracker is fabricated.

**Options and reason:** keeping the gate queues these outcomes until qualifying
evidence or an already-authorized routine close supplies the prerequisite; it
preserves the anti-churn safeguard but delays accepted work for unknown time.
Summary-only work can proceed independently, but repeats template coordination
later. I choose the named exception: the existing heavy reviews and one combined
window bound a coherent, reversible change without inventing a collection
process or requesting a special session-end. Benefit and recurring cost remain
unmeasured, especially the new mandatory cheap-advice duty; that is substantive
policy, not mere clarification.

**Grouped Scope delta:** degraded assurance -- waive only this bundle's
recurrence/window-or-routine-synthesis prerequisite for local preparation.
Remove none of the five outcomes; do not weaken them to evade the gate. Keep the
unmet evidence and this exception visible here and in the resulting combined
plan, with return review in the existing board section. The normal gate revives
for any widened scope or later doctrine bundle; no permanent rule change or
standing exception is authorized. Summary enhancement `6801982a` is requested
design, not an incident-remedy gate failure.

Both plan reviews precede Low implementation; both code reviews, mapped prose/
installed-copy/mutation checks, model floors, safety fences and final wide
Boundary B remain due. The exception adds zero routine human operations or new
approval steps. Publication/release, private access and hard-to-undo actions
remain outside delegation. No new proposal, tracker, trial, source change or
review clearance is made here. **Elapsed:** approximately 3 minutes through
judgment; finalization additional/unknown. **Tokens:** unknown.
