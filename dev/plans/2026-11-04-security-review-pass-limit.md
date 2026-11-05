# Plan: Security Review pass limit

**Source proposal**: dev/proposals/archive/2026-11-02-codex-security-review-pass-limit.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**Author**: CodexTerra (gpt-6.1-terra), ordinary plan author
**In brief**: Keep the normal Security Review limit while allowing a specifically authorized further pass.

## Source proposal

The accepted heavy proposal retains the normal two-pass limit and named
disposition at the cap, with a Maintainer-authorized exception for each
further scoped pass. Neither an exception nor an ordinary review clears a
Security obligation, finding, criterion or check.

## Scope

Align the cap in `AGENTS.md`, `templates/core/AGENTS.md`, both proposal
templates, `dev/modules/security-review.md`, its shipped counterpart, and
`docs/methodology/dual-review.md`; map other applicable readers and pins
before editing. Keep existing triggers and verification selections. Shared
core guidance for sequence items 4-6 has one writer, Herschel; coordinate a
combined editing and verification window without changing plan 4.

**Reuse**: N/A: no code added. The existing stage record carries the reason,
scope and authorization; no new form or authorization mechanism.

### Documentation / doctrine surface

Prescription belongs in governing and shipped instructions; the published
methodology explains the same contract. Existing tests guard shipped text.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map cap statements, readers and pins; align guidance and focused guards. | Both independent plan reviews and their dispositions; coordinate shared writer. | Consistent instructions and affected tests. |
| C2 | Exercise worked cases and affected checks; obtain ordinary and Security code reviews, then wide Boundary B. | C1 | Recorded change evidence. |

## Acceptance criteria

**C1.** Two passes remain normal at each stage; unresolved blockers or unmet
criteria/checks receive named disposition at the cap. Each further pass needs
a specific unresolved security question or newly changed material, why prior
passes and evidence cannot resolve it, its expected value, and a Maintainer
authorization for the named artifact and scope. Each further pass needs its
own reason and authorization. Agents have no scheduling or clearance authority;
no routine Security necessity explanation is added. Triggers, usual review and
verification remain unchanged. Enumerate applicable statements and readers,
including positive search controls and byte pins; align them without weakening
existing obligations.

**C2.** Human-applied examples show a closed second pass advances and an
unresolved question gets a further scoped pass only after authorization.
Reject missing reason or authorization, reusable authorization, automatic
passes and treating a pass as clearance. The existing stage record and
Maintainer decision own this check; text tests cannot establish authorization
or sound judgment. Ordinary and Security code reviews are independent.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: map `python tools/test_tiers.py for <changed paths>`, readers and
pins, run the selected tests and standing claim, link, snippet, neutrality and
redundancy gates. Inspect actual test triggers; add focused coverage only for
an uncovered plausible fault. Search controls must find a known cap statement.
Boundary C: independent reviewers falsify the contract with targeted checks.
Boundary B: wide, after both code reviews, on a clean final commit under
canonical Python 3.13; include the reviewed-range iteration selection,
applicable integration/workflow consumers and standing gates. Record SHA,
range, interpreter, clean pre/post state, commands, counts, elapsed time,
non-passes and omissions. No full certification is implied.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 keeps the normal cap and named disposition while requiring a specific reason and Maintainer authorization for each scoped exception -- accepted proposal, Proposal and Decision; plan, C1.
2. **Best alternative.** Reuse the existing stage record and human decision, as planned; a new authorization tool would add burden without establishing sound judgment -- accepted proposal, S1-S5; plan, Reuse and C2.
3. **What would show it wrong?** A worked case that permits a reusable authorization or treats an extra pass as clearance would falsify the change -- plan, C2; `docs/methodology/dual-review.md`, Caps and closure.

Reviewed commit: 7e439763b266170100cc7b63131f91e9f7c246e5

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The plan maps live and shipped cap statements, retains review triggers and checks, and requires independent code reviews followed by wide Boundary B. Its examples test human application, not the truth of authorization through text matching.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal and Decision, plan template, governing and shipped cap statements, Security Review modules and methodology. **Not covered**: all readers and pins, future examples or implementation, Security Review, tests and full suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 retains the normal two-pass cap, named disposition and separate checks while requiring a reason, expected value and named Maintainer authorization for every further scoped pass -- accepted proposal, Proposal/Decision; plan, C1-C2.
2. **Best alternative.** Keep reasons and authorization in existing stage records, as planned. An absolute cap is cheaper but loses the accepted targeted exception; a new register or parser adds upkeep without proving authorization -- accepted proposal, Alternatives/S1-S5; plan, Reuse.
3. **What would show it wrong?** Human-applied examples must reject an unapproved or reusable exception and any claimed clearance, while closed second-pass work advances without another read -- plan, C2; `docs/methodology/dual-review.md`, Caps and closure.

Reviewed commit: 7e439763b266170100cc7b63131f91e9f7c246e5
Ordinary review read: 3781123b.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

An exception commissions one read; it grants no scope concession, waived check
or automatic closure. Each later pass needs fresh authorization for its own
artifact/scope. Ordinary review and Security triggers remain independent;
routine invocation acquires no new permission or necessity-explanation ritual.

The existing `test_review_stance_in_shipped_files.py` obligation checks protect
separate usual/Security passes and matching plan obligations; they do not
establish the truth or merit of an exception. C1's cap-reader/pin inventory and
C2's human-applied negative examples therefore remain necessary implementation
evidence. The shipped module already states the cap while the self-hosted copy
lacks that paragraph; the named alignment scope can resolve this drift.

Shared-writer coordination changes editing ownership, not review independence.
Wide Boundary B follows both code reviews; no release/security ceremony is
shortened or authorized by this pass.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, ordinary review, accepted source/reviews/response/
Decision, current review template, governing/module cap statements and actual
text-guard bodies. **Not covered**: exhaustive reader/pin mapping, future worked
cases, implementation or authorization authenticity. No implementation tests,
suite or ceremony run; misleading reasons and mistaken human judgment remain possible.

## Author response -- Codex LunaLOW -- 2026-11-04

No findings. Both required plan-review obligations match and accept the plan.
The nonblocking human-application cases remain in C2: a closed second pass
advances, while each further scoped pass needs its own reason and Maintainer
authorization; missing or reusable authorization and automatic clearance do
not qualify. No operative change is needed.

**Status**: ready-to-implement. Implementation follows after this transition.
