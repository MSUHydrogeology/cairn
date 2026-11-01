# Clarify the pending tree-certification label

**Author**: Codex GPT-6.1
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Explain that pending tree certification does not mean a completed change needs another run now.

## Context

Issue #33 asks for scoped certification and a separate whole-suite check: the
label `Certified by: pending` can imply a full run is owed for every change.
The scoped-verification proposal and archived plan already distinguish the
change's Boundary B checks from tree certification. `AGENTS.md` retains the
pending label, while `doctrine/plans.md` says the later tree run is separate.
The decision master records the remaining terminology question. This is a
reported reading problem, not measured evidence of how often people misread it.

## Proposal

Keep the existing label, checks, triggers and certification meaning. Beside the
first instruction to record `Certified by: pending`, say that it tracks whether
a later authorized tree-certifying run covers the commit; it is not an unmet
change check or a request to run the whole suite now. A missing required change
check still keeps the work open. Apply that explanation consistently to the
self-hosted and installed governing rules, both plan templates,
`doctrine/plans.md`, and `docs/glossary.md`; retain the later append-only
certification entry and leave historical records unchanged. Preserve conditional
push, release, re-anchor and Maintainer-request triggers. Do not add scripts,
documents, generic model simulations, new review stages or evidence ledgers.

## Rationale

An adjacent explanation addresses the misleading to-do without changing a
recognized field or claiming scoped checks certify the whole tree. The existing
scope and trigger rules remain authoritative. Shipped templates are a protected
surface, so heavy review applies despite the small wording change.

## Alternatives considered

Rename or remove the field: this may read more naturally, but would require
changing consumers and reconciling older records. Redefine certification as
scoped checks: that answers the issue literally but changes an established
whole-tree claim. Make no change: lowest cost, but leaves the reported ambiguity
at the point readers encounter the label. The Maintainer may prefer that cost.

## Documentation / doctrine surface

Prescription belongs in `AGENTS.md` and `templates/core/AGENTS.md`; the plan
templates and `doctrine/plans.md` carry the corresponding record guidance.
`docs/glossary.md` describes the term. This proposal is deliberation in `dev/`.

## Evidence / verification plan

### Tests required

Search live readers, shipped copies, byte pins and actual triggers before
implementation. Existing `bootstrap/tests/test_certifying_run_rule.py` checks
for `Certified by` and the conditional push guard; `bootstrap/tests/test_verification_boundaries.py`
checks record vocabulary and both plan templates. Run mapped owners and installed
copy checks as selected by `tools/test_tiers.py`, including any additional
readers found. Do not change protected `bootstrap/tests/conftest.py`: its broad
run refusal already explains that tree certification is separate. If a required
consumer cannot accommodate the explanation without changing a protected file,
stop and reassess scope. Preserve all required checks and the independent review.

### Examples / smoke checks

Run claim, link, snippet and neutrality gates applicable to the changed prose.
Review the actual wording in both governing copies and templates: a reader should
be able to finish a change with all required checks passed while tree
certification remains pending. No whole-suite run is authorized by this proposal.

#### Security preflight — five questions, answered in writing

S1: A human records Boundary B results and the later certifying SHA from the
actual runs; the wording adds no deciding input or channel. S2: The existing
rule tests detect removal of named obligations; a changed-obligation mutation
has not been run for this proposal and must be assessed during implementation.
S3: Mapped pytest owners select the live rule surfaces; the prose gates check
changed documents. The statement above promises clarification, not automated
proof of reader comprehension. S4: No parser, default or fallback changes;
existing failed or missing checks still block completion. S5: A misleading
record or a reader misunderstanding the distinction can still succeed; wording
cannot authenticate a run or guarantee comprehension.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or revise if the wording implies that a required check may be skipped,
changes an authorized certification trigger, conflicts with an actual consumer,
or the clarification costs more than the ambiguity warrants.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. The proposed changes touch governing
doctrine and shipped authoring templates; no new trust boundary is intended.

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
