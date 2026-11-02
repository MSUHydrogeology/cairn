# Show the operating cost of decision options

**Author**: Codex gpt-6.1-terra
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — shipped authoring guidance and governing doctrine are protected surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Show what decision options add and cost so the Maintainer can choose with the burden in view.

## Decision summary

When asking the Maintainer to choose, describe what each material option adds and its continuing cost, and include a less involved option when it could meet the goal. Give a separate recommendation and reason. This adds a little explanation to a decision, but makes added files, checks and human steps visible before they become commitments.

## Context

[Issue #40](https://github.com/MSUHydrogeology/cairn/issues/40) reports an adopter choosing recommended options that introduced files, hashes, flags and checks without those additions or costs being stated. This is a reported experience, not an independently inspected project. Its requested Questions for the Maintainer blocks are absent from the current proposal and plan templates. The proposal templates already ask for a meaningful tradeoff and an alternative; `dev/agent_collaboration.md` asks for a recommendation and the cost of being wrong. `docs/methodology/roles.md` asks a reviewer briefing to explain what options change on disk. None explicitly asks decision presentations generally to show operating burden or an adequate less involved option.

## Proposal

Add concise guidance for decisions presented to the Maintainer, including chat and written artifacts: state what each material option adds or changes and its meaningful costs to build, run, understand and maintain, using estimates or uncertainty where needed. Include the least involved credible option, including doing nothing when viable, and say what it loses. Give the agent's recommendation and reason separately from the option labels. Where a Decision accepts new recurring machinery, name that addition in the Decision record so it can be read back. Do not require a fixed number of options, a table, or a new review or checklist.

## Rationale

A recommendation remains useful, but a label alone can conceal the work it commits others to. Comparing an adequate simpler choice makes that burden visible. Recording accepted additions makes the commitment traceable without adding a separate artifact.

## Alternatives considered

Keep existing guidance: no extra authoring, but the reported cost can remain implicit. Add fields to every proposal and plan template: a reliable prompt, but the named blocks no longer exist and fixed fields impose work even when no choice is presented.

## Documentation / doctrine surface

Place the operative cross-cutting instruction in `AGENTS.md` and its shipped counterpart `templates/core/AGENTS.md`; align the relevant decision guidance in `dev/agent_collaboration.md` and shipped authoring templates only where needed. `docs/methodology/roles.md` remains descriptive and should be aligned if the final wording changes its account of briefings.

## Evidence / verification plan

Inspect current guidance and its shipped counterparts, direct readers and byte pins before editing. Check a concrete decision with a recurring check and a credible simpler option: both additions, operating costs, losses and the recommendation should be clear without a new form. A decision that obscures those facts or requires invented alternatives falsifies the change. Run claim, link, snippet and neutrality gates and the tests that read changed files; map exact nodes before implementation. After review, run wide Boundary B on a clean final commit under canonical Python 3.13, recording its range, checks and omissions.

### Tests required

Identify tests reading or pinning the final changed files with `python tools/test_tiers.py for` and a reader search; run the mapped nodes. No software behavior change is proposed.

### Examples / smoke checks

Run `python scripts/check_cairn.py` and the applicable claim, link, snippet and neutrality checks. Compare the shipped guidance with the self-hosted wording.

#### Security preflight — five questions, answered in writing

S1: Authors supply the option descriptions and Maintainer supplies the Decision; neither is mechanically verified by this wording. S2: A sample omitting a recurring check should fail the human comparison; this proposed check has not yet been run. S3: The implementation record will name the sample and reviewer; no automated check is claimed. S4: Missing costs remain an incomplete briefing, not authorization to add machinery. S5: An author can still omit or misstate an addition; the Maintainer and reviewers must judge the evidence.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The guidance causes routine decisions to accumulate boilerplate, conceals a material loss in the simpler choice, or fails to surface a recurring cost in a realistic example.

## Scope delta

None; opening scope.

## Assurance path

**Assurance path**: high-assurance

## Review -- Codex gpt-6.1-terra -- 2026-11-01

Reviewed commit: 2d8c0bf03a6a36db7960745654771a25a4cf3f35  
Target: entire proposal  
Prior findings: none  
Assurance path: high-assurance

**Tier**: usual  
**Findings**: raised  
**Verdict**: ACCEPT  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: visible additions and costs help the Maintainer assess a recommendation; the no-form constraint limits overhead. -- Proposal, Decision summary and Proposal.
2. **Best alternative.** Keep current guidance and rely on judgment; it already asks for a cheaper alternative and the cost of being wrong, but does not expressly ask for the additions and operating costs of each material option. -- `dev/agent_collaboration.md:89, 309-311`; Proposal, Context.
3. **What would show it wrong?** A realistic briefing that becomes boilerplate without exposing a material cost, or that invents an implausible option, would undermine the change. -- Proposal, Signals the change is wrong and Evidence / verification plan.

**N1 — non-blocking.** The Decision-record sentence requires naming accepted recurring machinery but leaves its boundary and burden implicit. A routine record could accumulate machinery inventories, defeating the stated aim. Clarify that the record names material new recurring additions in the Decision itself, and exercise a routine case with no such addition to show no extra record is needed. Evidence: Proposal, Proposal and Signals the change is wrong. The heavy tier and plan review follow the named protected doctrine/template surfaces (`AGENTS.md`, Project conventions); that assurance is not a new process invented by this proposal.

Coverage: Read the committed proposal, review template and cited collaboration guidance; assessed burden and the stated assurance path. Did not independently verify the adopter's report, inspect every shipped counterpart or conduct the separate Security Review.

## Security Review -- Codex Sol -- 2026-11-01

**Tier**: Security Review  
**Reviewed commit**: aa1784b7  
**Verdict**: Support; no blocking security findings.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: exposing a material recurring check or human step before acceptance supports informed Maintainer authority without changing who decides. Evidence: committed Proposal and Security preflight; `AGENTS.md`, Roles.
2. **Best alternative?** Apply the existing simpler-alternative guidance without a new cross-cutting rule. That avoids additional prose but leaves recurring operating cost implicit; a brief material-cost instruction addresses that gap. Evidence: `dev/agent_collaboration.md`, Review loop and Maintainer-call guidance, at the reviewed commit.
3. **What would show it wrong?** A routine decision requiring a machinery inventory, or a simpler option omitting a required security check, would defeat the intended improvement. Evidence: Proposal, Signals the change is wrong; `AGENTS.md`, model-tier and high-risk obligations.

**Non-blocking advice.** Concur with N1: name material new recurring commitments briefly in the existing Decision, without itemized accounting or a “none” declaration. A routine decision with no recurring addition should need no extra sentence. An option comparison must disclose a lost safeguard; it cannot waive required checks, accepted scope or the model capability floor. Keep the no-checklist constraint; compare recurring-addition and routine cases in the planned human comparison.

**Coverage:** Read the proposal and ordinary review at `aa1784b7`, plus committed governing authority, model-tier rules and collaboration/role guidance. Examined authorization, concealed safeguards and recurring-record burden. Did not verify the adopter report, final wording, every shipped consumer or runtime security; ran no implementation checks.
