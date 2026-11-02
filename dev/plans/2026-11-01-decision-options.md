# Plan: Show decision options' operating costs

**Source proposal**: dev/proposals/archive/2026-11-01-codex-decision-options.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Make the additions and operating costs of Maintainer decision options visible before a choice.

## Source proposal

The Maintainer accepted the heavy proposal as revised under Option 1: add cross-cutting decision guidance to the governing instruction and its shipped counterpart, with collaboration alignment and high assurance.

## Scope

Update `AGENTS.md`, `templates/core/AGENTS.md` and relevant guidance in `dev/agent_collaboration.md`. Inspect shipped authoring templates and `docs/methodology/roles.md` and align them only where needed to carry the accepted guidance accurately. Preserve existing authority, safeguards, accepted scope and model floors; add no form, checklist or fixed option count. Do not alter trust baselines; release ceremonies remain separate.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Cross-cutting prescription belongs in both governing files; collaboration guidance is deliberative, and any needed roles clarification is descriptive.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inspect current counterparts, readers and byte pins; align the guidance and exercise the two decision examples. | Both required plan reviews and author response | Concise governing and supporting prose, with iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration verification. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Material options state additions or changes and meaningful build, operation, understanding and maintenance costs, with estimates or uncertainty where needed. The least involved credible option, including doing nothing when viable, states its losses and safeguards; the recommendation and reason are separate. Comparisons cannot waive required checks, accepted scope or model floors. Existing Decisions briefly name material new recurring additions; one without such an addition needs no extra sentence or inventory. Governing copies agree in substance, and supporting guidance does not contradict them. A human comparison exercises a recurring check and a credible simpler option, and a routine Decision without a recurring addition; record the sample and reviewer. Omitting the recurring check must fail that comparison. No fixed form or invented alternative is required.

**C2.** Ordinary and separate Security Reviews assess the committed implementation. All required checks and accepted criteria are met; final wide Boundary B evidence covers review fixes.

## Scope delta

**Scope delta**: preserved.

## Verification

Before editing, inspect direct readers and byte pins and map changed paths with `python tools/test_tiers.py for <paths>`; for governing text use the complete reviewed range. Run mapped iteration tests and applicable claim, link, snippet and neutrality gates, plus `python scripts/check_cairn.py`. Compare shipped and self-hosted guidance and perform the two human examples above; record reviewer, outcomes and omissions. Security preflight S2 and S3 remain the proposal's human comparison in C1, not an automated claim.

Boundary C: independent reviewers read the committed implementation and iteration evidence, run only targeted falsification checks, and name missing coverage. After review and fixes, run wide Boundary B on a clean, unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow tests, owning families, known consumers and public paths, standing gates and plan-specific examples. Record SHA and range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Tree certification and trust-baseline changes are separate release work; do not run the full certifying suite here.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: 02ffdb26524aa56f6d49b7760fd47fd3f8830c32  
Target: entire plan against the accepted proposal  
Prior findings: none  
Assurance path: high-assurance, inherited from accepted proposal

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. C1 carries the accepted cost disclosure into both governing copies, prohibits comparisons from waiving checks, scope or model floors, and requires disclosure of losses and safeguards. C2 retains separate Security Review before final verification. -- Plan, Scope, Sequence and C1/C2; accepted proposal, Proposal and Decision.
2. **Best alternative.** Use concise governing prose and align supporting text only where it contradicts that rule; avoid adding template fields. This is already the plan's conditional approach and preserves the accepted outcome without a new form. -- Plan, Scope; accepted proposal, Alternatives considered and Decision.
3. **What would show it wrong?** A sample hiding a recurring security check, treating the simpler option as permission to skip a safeguard, or demanding an inventory for a routine Decision. C1 explicitly rejects the omitted-check sample and exercises the routine case; final wide verification includes those examples after review fixes. -- Plan, C1 and Verification; accepted proposal, security preflight S2/S3.

No new trust boundary or security machinery is planned. Cost comparison remains advice to the Maintainer, not authority to remove accepted obligations.

Coverage: examined the committed plan, accepted proposal, governing authority, current plan template, collaboration review guidance and descriptive roles guidance. Did not assess implementation wording, execute the human examples, inspect every shipped consumer or run implementation tests; those remain C1/C2 work.

## Ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

**Obligation:** Internal
**Verdict:** Support; no blocking findings.

**Foundations**

- **Should it happen as framed?** Yes. The plan carries Option 1 into both governing copies and collaboration guidance, preserves authority and safeguards, and exercises recurring and routine Decisions. Evidence: plan Scope and C1; accepted proposal Decision and Proposal.
- **Best alternative:** Conditional alignment of supporting material, already in the plan, avoids fixed fields while retaining the accepted cross-cutting guidance. Evidence: plan Scope; accepted proposal Alternatives considered.
- **What would show it wrong?** A comparison that hides a recurring check or lost safeguard, invents an alternative, or adds routine inventory would defeat the outcome. Evidence: plan C1 and Verification; accepted proposal Signals and security preflight.

**Advice:** Coordinate overlapping mapped checks across concurrent changes when they share the same final committed bytes and required coverage; record the exact range and outcomes. Do not repeat a check without a changed input or an unresolved concern, and retain the required post-review wide Boundary B for this plan.

**Coverage:** Read the plan and appended Security Review at `15a91195`, accepted proposal and Decision, and current plan template. Did not assess final wording, run examples, inspect every reader, or run implementation checks; those remain implementation and review work. No suite run. Elapsed: approximately 3 minutes; tokens: unknown.

## Plan response -- Codex gpt-6.1 -- 2026-11-01

Both reviews support the plan and raise no findings. Accept the ordinary review advice: coordinate overlapping checks on the same final committed bytes, record their exact range and outcomes, and retain this plan’s post-review wide Boundary B. No operative change is needed.

**Elapsed**: approximately 2 minutes; **Tokens**: unknown
