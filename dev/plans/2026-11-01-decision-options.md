# Plan: Show decision options' operating costs

**Source proposal**: dev/proposals/archive/2026-11-01-codex-decision-options.md
**Status**: awaiting-code-review
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

## Implementation verification -- Codex GPT-6.1 Luna -- 2026-11-01

Changed surfaces: `AGENTS.md`, `templates/core/AGENTS.md`,
`dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md`, and
`docs/methodology/roles.md`. The proposal template already asks for meaningful
costs and an alternative; no field or template block was added. Local and
shipped guidance agree in substance.

The shared mapped iteration selection covered the three v0.6 plans and the
lifecycle-description plan. `python tools/test_tiers.py for --range
b210f9b4d2e938e33905e8c99faabd7ab7e91148..d7434ba616289d8f1c1927d23784ab1a6b33b876`
selected 18 files: `test_ceremony_review_report.py`,
`test_check_release_publication.py`, `test_default_security_stance.py`,
`test_doc_governance.py`, `test_finalize_retired_living_state.py`,
`test_module_roster.py`, `test_onboarding_seed_roster.py`,
`test_oracle_activation.py`, `test_portable_security_sweeps.py`,
`test_presets.py`, `test_prune_tools.py`, `test_replacement_tools.py`,
`test_review_and_verification_rules_ship.py`,
`test_scientific_check_guidance_ships.py`, `test_session_routines.py`,
`test_session_start_drain_rules.py`, `test_status_vocabulary_advisory.py`,
and `test_upgrade_added_slots.py`. The governing-text selector reported 46
unpinned `AGENTS.md` readers omitted; folder sweepers remain for release
verification.

The 18-file selection passed: 667 passed in 61.04 seconds under Python 3.12.9.
This exceeded the 30-second iteration target; per-file durations were not
collected. Later shared corrections were checked with targeted tests recorded
in the related plans. No full suite or install comparison was run here.

`python scripts/check_cairn.py` passed (189 Markdown files; 95 external links
not probed). `python scripts/link_check.py` passed (189 files; 96 external
links not probed). `python scripts/quality_gate.py --sub neutrality` reported
zero failures and 43 informational findings. Snippet sync was not applicable:
no synced snippet changed.

**Maintainer authorization** (chat, 2026-11-01): "Yes, use agent reviews" to
substitute independent agent reviewers for the two plan examples that called
for a person to compare them by hand. No automated or security check was
waived. Independent reviewer Codex GPT-6.1 applied the prepared examples at
`d7434ba6`: the recurring weekly check versus manual review disclosed the
cost and lost safeguard, omitting the check failed, and a routine Decision
with no new recurring addition needed no inventory. This is a reasoning
example, not proof that future authors will identify every obligation.
Elapsed: approximately 32 minutes; tokens: unknown.

## Completion follow-ups

**Issue #40 closure** remains a finish step after code review and final wide
Boundary B. The accepted guidance addresses the issue's three requests:
visible option additions and costs, a separate recommendation, and brief
Decision disclosure of material new recurring machinery. Close the issue only
after final verification confirms these outcomes; otherwise keep it open and
name the remaining request.

## Code review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict**: Accept; no findings. Reviewed `d7434ba6` and implementation evidence at `e8c11a43`.

**Foundations**: Should this happen as framed? Yes: both governing copies require material additions and costs, a credible least involved option with losses, and a separate recommendation, while preserving checks, scope and model floors. Best alternative: retain existing guidance; it avoids added wording but leaves recurring operating costs implicit (proposal Context and Alternatives). What would show it wrong? A briefing that hides a recurring check or makes routine Decisions accumulate inventory would defeat C1; the recorded examples reject the omission and do not require routine inventory.

**Evidence**: Compared the governing and supporting changes with C1 and the accepted proposal. The implementation record reports 667 mapped tests passing, prose gates and the independent examples, and names omitted unpinned readers. The examples are reasoned comparisons, not proof future authors disclose every cost.

**Coverage**: Read committed implementation, proposal, plan and iteration evidence. Did not rerun tests, inspect an installed copy or perform the separate Security Review; wide final verification remains outstanding. No suite run. Elapsed: approximately 5 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: d7434ba616289d8f1c1927d23784ab1a6b33b876  
Target: decision-options changes in `d7434ba6^..d7434ba6`; evidence `e8c11a43`, ordinary review `3fae9a3b`  
Prior findings: none  
**Tier**: Security Review  
**Verdict**: ACCEPT; no findings.  
**Elapsed**: approximately 4 minutes across preparation and final review. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Both governing copies require visible additions, meaningful costs and lost safeguards, explicitly prohibit waiving checks, accepted scope or model floors, and retain Maintainer authority. Supporting guidance agrees. -- Committed governing paragraphs, collaboration additions and roles diff; C1.
2. **Best alternative.** Reuse concise guidance in existing records. Removing the rule leaves costs implicit; adding fields creates unnecessary continuing work. The implementation adds no form, gate or review round. -- Accepted proposal, Alternatives; implementation diff.
3. **What would show it wrong?** Calling an omitted recurring security check the simpler choice, or requiring an inventory for an ordinary Decision. The recorded independent examples reject the omitted check and preserve the no-inventory routine case; the governing no-waiver sentence prevents cost comparison from authorizing removal. -- Iteration evidence, authorized examples; governing instruction.

**Bounding**: ACCEPTED — challenged counterpart agreement and the possibility that cost disclosure grants waiver authority. Targeted source assertions confirmed identical new governing paragraphs and retained no-waiver text. The shared record reports 667 mapped passes under Python 3.12.9, prose gates and 46 selector omissions; these are author evidence, not rerun here.

Coverage: examined accepted scope, committed implementation, supporting guidance, iteration and ordinary review; performed source assertions. Did not inspect installed output, repeat tests or certify the tree. No suite or mutation run. No reached Maintainer fence or deviation request in this range; final canonical-Python wide Boundary B remains owed before closure.

## Response to code reviews -- Codex GPT-6.1 Luna -- 2026-11-01

Both the ordinary and Security code reviews accept the implementation with no
findings. No code revision is needed. Preserve the issue #40 closure check in
Completion follow-ups; final wide Boundary B and confirmation of all three
requested outcomes remain before archival. Elapsed: under one minute; tokens:
unknown.
