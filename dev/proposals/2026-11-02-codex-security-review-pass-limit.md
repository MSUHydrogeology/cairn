# Permit a justified Security Review beyond two passes

**Author**: Codex GPT-6 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — this changes the security review contract in protected methodology and templates
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Keep the normal two-pass Security Review limit, with a Maintainer-authorized exception for a specific substantive reason.

## Decision summary

Keep the normal limit of two Security Review passes. If a further pass would resolve a specific remaining security uncertainty, the Maintainer may authorize it after seeing the reason and its expected value. This adds a decision only when an exception is sought; it can delay closure and consume another review.

## Context

The current cap sends unresolved blocking findings or unmet accepted criteria or checks to the Maintainer by name; it does not clear them automatically ([dual-review](../../docs/methodology/dual-review.md#caps-and-closure)). The Maintainer asked for the reason for more than two rounds, while retaining the Security Review trigger and Cairn's broader checks (chat, 2026-11-02). The current contract supplies no exception for an additional Security Review pass.

## Proposal

Keep two passes as the normal limit at each stage. At that limit, retain the existing named disposition of unresolved blockers and unmet criteria or checks. If an additional Security Review pass is proposed, identify the specific unresolved security question or newly changed material, why the existing passes and available evidence cannot resolve it, and what the additional pass is expected to establish. The Maintainer may authorize a further pass on that named artifact and scope, or decline it and disposition the outstanding items under existing rules. Record the reason, scope and authorization with the existing stage record. Each further pass needs its own substantive reason and authorization; no standing exception follows.

A further pass does not itself waive a finding, criterion or check, change scope, or replace the usual review. Keep existing Security Review triggers and Cairn's broader verification selections unchanged. Do not add a routine explanation of why Security Review is needed.

## Rationale

The existing cap prevents review from becoming an open-ended loop. A narrow exception lets the Maintainer commission a targeted security read when a named uncertainty makes its value clear. The decision costs human attention and potentially another pass, but is incurred only when an exception is proposed.

## Alternatives considered

- **Keep the absolute cap.** No additional procedure or review cost; the Maintainer must disposition remaining items without a further Security Review, even when a targeted pass could answer a material question.
- **Let the author or reviewer order another pass with a reason.** Faster and no Maintainer decision, but can turn the limit into repeated discretionary reviews and transfers scheduling authority away from the Maintainer.
- **Remove the limit.** Simplest text but loses a clear stopping point and risks recurring review cost without a specific benefit.

## Documentation / doctrine surface

Update the operative rule in `AGENTS.md` and its shipped counterpart `templates/core/AGENTS.md`, the proposal template, the Security Review module, and the corresponding published methodology. Search other shipped and self-hosted readers and byte pins for the existing cap; align all applicable statements without changing the review trigger or check selection. Prescription belongs in operative instructions, explanation in methodology, and deliberation here.

## Evidence / verification plan

A plan will map all statements and readers of the cap, including tests and pins, before changes. Verify that the normal limit, substantive reason, named Maintainer authorization, scoped additional pass, and existing disposition remain consistent. A statement allowing an automatic or unlimited pass, or implying an exception clears a finding, falsifies the change. Run the affected tests and standing prose gates, and use wide Boundary B for this trust-ceremony contract.

### Tests required

Map tests naming changed files with `python tools/test_tiers.py for <paths>`, search readers and pins, and run the resulting scoped checks and applicable prose gates. The plan will identify exact nodes and any missing behavioral coverage; no full certification is implied by this proposal.

### Examples / smoke checks

Check two worked cases in the changed guidance: a closed second pass advances without another pass; an unresolved named security question may receive a further scoped pass only after the Maintainer authorizes it.

### Security preflight

- **S1 — Who supplied it?** The author supplies the reason and scope in the stage record; the Maintainer supplies authorization. The proposed work's author may supply the reason, so it is not independent evidence of merit.
- **S2 — Can it fail?** Human review must reject an example that permits an extra pass without authorization or treats it as clearance. These negative examples have not yet been run; implementation must record their outcome.
- **S3 — What fires it, over what?** The existing stage record and Maintainer decision invoke this human check; scoped tests and prose gates check changed files, not the truth of authorization. Exact commands and the final adopter-facing sentence will be mapped in the plan.
- **S4 — Which way does it break?** Missing reason or authorization leaves the normal cap and named disposition in force; it grants no additional pass or clearance.
- **S5 — Who still wins?** A misleading reason or a mistaken Maintainer authorization can still produce an unnecessary or ineffective review. The procedure cannot establish the quality of human judgment by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Exceptions recur without materially resolving the named question, reasons become boilerplate, or the cap is treated as permission to defer an unmet check indefinitely.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — protected vendor-neutral methodology and templates govern a security review obligation.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 9246429b25fdd4904ec701e5713ffc745eb7ab2b  
Target: two-pass limit, scoped exception authority and retained checks  
Prior findings: none  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes. The proposal keeps the ordinary stopping point while giving the Maintainer a targeted option when a named security question remains. It expressly avoids routine explanations for required Security Review and leaves triggers and verification selections intact. -- Proposal, Proposal and Decision summary; current AGENTS.md cap; dual-review, Caps and closure.
2. **Best alternative.** Retain the absolute cap: no new procedure, but a useful additional Security pass cannot resolve uncertainty before disposition. Letting authors or reviewers authorize further passes weakens the stopping point; removing the cap invites recurring review cost. Named Maintainer authorization is proportionate. -- Proposal, Alternatives and Rationale; existing named-disposition rule.
3. **What would show it wrong?** Automatic further passes, reusable authorization, reasons becoming boilerplate, or an exception treated as clearance. The required reason, artifact/scope authorization for each pass, no-waiver clause and negative worked examples target those failures. Human judgment remains a limitation. -- Proposal, Proposal, S2–S5 and Signals.

**Verdict**: Accept as framed; no blocking findings. The exception spends attention only when requested. Closed work still advances; unresolved checks still need their existing disposition. No routine checklist, additional standing review or automated authorization mechanism is warranted.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

Coverage: read committed proposal, current proposal template, governing cap/closure and plan-review obligations, and shipped/self-hosted Security Review modules. Did not map every cap reader or byte pin, run worked examples or suites, or validate future implementation.

## Proposal review -- Codex GPT-6 -- 2026-11-02

**Verdict:** Accept as framed, subject to Maintainer Decision; no blocking findings. **Elapsed:** approximately 4 minutes. **Tokens:** unknown.

1. **Should it happen?** Yes. The existing absolute cap does not allow a further Security Review even if a specific unresolved question warrants one. The proposal keeps the ordinary stop and asks for a reason only when an exception is sought, as requested.
2. **Best alternative:** Keep the absolute cap for maximum simplicity. That avoids additional decisions but cannot obtain an extra targeted review when one would answer a remaining question. Letting agents authorize exceptions themselves saves an interruption but risks repeated review loops. The proposed Maintainer authorization is a conscious tradeoff, not a consequence of the user's words alone.
3. **What would show it wrong?** Boilerplate reasons, recurring extra passes without useful answers, or an extra pass treated as automatically clearing a finding. The proposed named question, separate authorization and negative examples address those risks but cannot guarantee good judgment.

Coverage: read the committed proposal, existing Security Review and current cap; did not map every rule reader or test future implementation. No suites run.
