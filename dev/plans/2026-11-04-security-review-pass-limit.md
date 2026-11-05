# Plan: Security Review pass limit

**Source proposal**: dev/proposals/archive/2026-11-02-codex-security-review-pass-limit.md
**Status**: awaiting-plan-review
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
