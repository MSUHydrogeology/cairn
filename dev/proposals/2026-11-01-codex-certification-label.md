# Remove the pending tree-certification marker

**Author**: Codex GPT-6.1
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Remove the per-change pending marker and record each actual whole-tree run once.

## Context

Issue #33 reports that `Certified by: pending` can imply a whole-suite run is
owed for each change. Scoped change verification already exists separately from
whole-tree certification. The Maintainer directed: “Remove the pending marker”.
That direction calls for this revised proposal, not acceptance of its scope. The
issue asks to call scoped checks certification; this proposal preserves the
existing whole-tree meaning and removes the misleading marker instead.

## Proposal

Remove the requirement for a per-change `Certified by: pending` field and its
instruction from current governing rules, plan templates, doctrine, glossary,
and the broad-run refusal message. Update existing rule tests and shipped
copies to match. Keep Boundary B's required evidence and all checks and triggers:
missing required change checks keep the work open; a required whole-tree run must
pass before the relevant push, release or re-anchor, and a Maintainer may request
one. Do not run the whole suite for this change solely because of the proposal.

Record each actual whole-tree run once in an existing appropriate shared release,
baseline, or other existing project record, including the tested commit and
result and the existing required run evidence. A successful run covers changes
at or before its commit; a failed run remains subject to the existing failure
and bisect rules. Do not create per-change pending entries or update archived
plans. The absence of a pending field does not establish that a required run
passed; consult the shared run record. No new documents, scripts, review stages,
or generic model simulations are introduced.

## Rationale

Removing the marker eliminates the false to-do rather than explaining it at
every use. One shared record preserves evidence of an actual run without
repeating it per change. The loss is a per-change indication that a later run
has not yet been recorded; the actual required checks and their triggers remain.
The protected refusal message and shipped templates make heavy the leanest lane
under the project's stated rules.

## Alternatives considered

Keep the marker and clarify it: retains the explicit per-change indication but
leaves the misleading word and repeats explanation. Rename scoped verification
as certification: matches the issue literally but changes the established
whole-tree claim. Do nothing leaves the reported ambiguity.

## Documentation / doctrine surface

Governing instructions belong in `AGENTS.md` and `templates/core/AGENTS.md`;
plan templates and `doctrine/plans.md` carry record guidance; `docs/glossary.md`
describes the terms. The existing protected refusal message and relevant rule
tests must match. This proposal is deliberation in `dev/`.

## Evidence / verification plan

### Tests required

Search live readers, shipped copies, byte pins and actual triggers before
implementation. `bootstrap/tests/test_certifying_run_rule.py` requires the old
field and checks the conditional push guard; `bootstrap/tests/test_verification_boundaries.py`
checks record vocabulary and both plan templates. Update affected assertions to
guard the retained checks and the absence of a mandatory pending field, not
merely a replacement string. Map all changed files with `tools/test_tiers.py`,
run their scoped owners and applicable installed-copy checks, and preserve
required protected-file procedures. No full suite or re-anchor is authorized.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality gates. Inspect both governing
copies, templates and the real refusal message: no per-change pending field is
required; a missing check still blocks; actual tree-run evidence identifies the
commit and outcome in one existing shared record.

#### Security preflight — five questions, answered in writing

S1: Humans supply change-check outcomes and whole-tree run evidence from the
actual commands; this change adds no deciding input or channel. S2: Existing
rule tests guard named obligations, but have not been mutated for this revision;
implementation must test the changed obligations using the applicable existing
checks. S3: Mapped pytest owners exercise rules and the real guard; prose gates
cover applicable changed documents. They cannot prove reader comprehension.
S4: No parser or fallback changes are proposed; an absent required check or
required certification remains a blocker. The guard's message changes, not its
refusal condition. S5: A false human record or misunderstanding can still
succeed; a shared record does not authenticate the reported run.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Revise or withdraw if a required check or trigger becomes optional, an actual
consumer needs per-change markers for correctness, or a shared run record cannot
be found reliably enough to establish a required run's result.

## Scope delta

**Scope delta**: lost. The original outcome of removing the false to-do while
preserving checks remains; removing the field loses the per-change indication
that no later certification is recorded. **Disposition**: defer to the
Maintainer's Decision. Retaining the marker with an explanation was rejected
because the Maintainer directed its removal.

## Assurance path

**Assurance path**: high-assurance. This touches governing doctrine, shipped
authoring templates and the protected broad-run guard message, without adding a
trust boundary.

## Review -- Codex GPT-6.1 -- 2026-11-01

Reviewed commit: 024e7e65a660a7df85e06d94cfc5f8112c76a114  
Target: proposal and verification approach  
Prior findings: none  
Assurance path: high-assurance

**Tier**: usual  
**Findings**: raised  
**Verdict**: ACCEPT  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The adjacent explanation could make the existing label less misleading, but adds text across six surfaces without evidence of how often readers stumble; the issue remains a terminology decision, not proof that this wording solves it. Evidence: proposal context and proposal; decision master, issue triage.
2. **Best alternative.** Drop the mandatory pending entry and record the certifying SHA only when a run exists, while retaining the separate tree-certification triggers. This removes the misleading to-do and some apparatus; it loses the explicit per-change indication that no later run is recorded. The accepted scoped-verification proposal originally called for this, while the current certification rule test requires `Certified by` on each surface.
3. **What would show it wrong?** An actual consumer or wording that makes a missing change check seem optional, or a concrete assessment that the explanation costs more than the ambiguity, should prompt revision or withdrawal. Evidence: proposal signals and tests required.

**Non-blocking recommendation.** Compare removing only the mandatory *pending* entry with retaining the later certification record; renaming or removing the entire field is a broader alternative than necessary. State the loss explicitly: the adopter asked for scoped certification, and this proposal preserves whole-tree certification instead. The existing scoped checks address the repeated-run concern, but do not adopt the requested terminology. A short replacement for redundant wording may serve the reader better than adding the explanation everywhere. Close by making that tradeoff clear for the Maintainer's Decision; no additional process is needed.

**Coverage:** Read the committed proposal, current proposal template, decision master, accepted scoped-verification proposal and certification rule test. Did not verify every consumer, test behavior, reader comprehension or the Security Review.

## Security Review -- Codex GPT-6.1 -- 2026-11-01

**Tier**: Security Review  
**Reviewed commit**: 024e7e65a660a7df85e06d94cfc5f8112c76a114  
**Verdict**: ACCEPT; no security findings  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. Clarifying a record label adds no authority to skip checks: the proposal explicitly keeps missing required checks blocking and preserves conditional certification triggers. Evidence: proposal, Tests required and Security preflight; current `AGENTS.md` Verification.
2. **Best alternative.** Omit the mandatory pending entry while retaining the later certification record. This reduces text and the misleading to-do, but loses an explicit per-change indication that no certification is recorded. It is a Maintainer terminology choice, not a security improvement: `doctrine/plans.md` already separates certification and blocks a push when required certification has not passed.
3. **What would show it wrong?** Wording that permits completion with an unmet change check or weakens an authorized certification trigger would defeat the stated scope. Evidence: proposal Signals; `bootstrap/tests/test_certifying_run_rule.py` tests trigger language and conditional refusal wording; `bootstrap/tests/test_verification_boundaries.py` guards the change-verification obligations.

The security risk is readers treating reassurance about pending certification as a waiver. The proposed adjacent explanation explicitly excludes that reading. Keep it short and preserve the failure rule beside it; the existing tests and later review suffice without another ledger or mechanism. This proposal authorizes no executable guard change, authentication claim or new trust boundary.

**Coverage:** Read the committed proposal, proposal template, governing verification rules, certification doctrine and named rule-test source. Did not run tests, inspect every consumer, prove reader comprehension or assess implementation wording that does not yet exist.


## Response -- Codex GPT-6.1 -- 2026-11-01

**Elapsed**: approximately 2 minutes
**Tokens**: unknown

- Ordinary review: compared removing only the pending entry and stated its loss,
  the terminology tradeoff, and the preference for concise replacement wording.
  Retain the proposed field pending the Maintainer's choice.
- Security Review: accepted; keep the explanation short and missing checks
  blocking as already specified.

### Withdrawn / superseded commitments

None.


## Revision for widened-scope review -- Codex GPT-6.1 -- 2026-11-01

**Elapsed**: approximately 3 minutes
**Tokens**: unknown

The Maintainer directed removal of the pending marker. The operative proposal
now presents that alternative and a single shared record for each actual run;
prior reviews and response remain unchanged. The change retains required checks
and is submitted for review of the widened scope, not presented as accepted.

## Widened-scope review -- Codex GPT-6.1 -- 2026-11-01

**Tier**: usual  
**Reviewed commit**: b256cc62  
**Verdict**: ACCEPT; no blocking findings  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. The guard currently tells every reader to record pending (`bootstrap/tests/conftest.py`), and governing rules require it in each change record (`AGENTS.md` Verification). Removing that instruction addresses the reported ambiguity while the proposal explicitly retains missing-check blockers and certification triggers. A single actual-run record is less repetitive; its practical retrieval has not been demonstrated.
2. **Best alternative.** Retain the existing pending field and append a separate SHA-keyed run record, as `doctrine/plans.md` currently directs. This preserves a visible per-change indication, but retains the confusing pending instruction. The proposed loss is stated for the Maintainer's Decision.
3. **What would show it wrong?** An actual consumer depending on the marker, a weakened trigger, or inability to find the run record would challenge it. The rule test reads the phrase rather than consuming a status; the real broad-run guard uses it in a message, while its refusal condition is separate. I did not establish that every consumer behaves likewise.

**Non-blocking recommendation.** During planning, identify a discoverable existing home for each authorized run type, including a Maintainer-requested run outside a release or re-anchor. `doctrine/plans.md` requires a SHA-keyed entry but does not name a universal home; the proposal's “other existing project record” leaves that choice open. Keep the solution to one record per actual run, without retroactive plan updates.

**Coverage:** Read the committed proposal, governing verification rule, certification doctrine, release-process checks, rule-test source and guard message. Did not run tests, enumerate every consumer, verify run-record retrieval, assess reader comprehension or perform Security Review.
