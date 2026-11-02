# Separate scientific model evidence from routine tree certification

**Author**: Codex gpt-6.1-terra
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — governing doctrine and shipped authoring templates are protected surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Keep long scientific model runs in the evidence for the work that needs them, instead of making them routine tree certification.

## Decision summary

Clarify that a long scientific model run used as evidence belongs to the proposal, plan or release that requires it; it is not automatically part of routine tree certification. An applicable accepted criterion or release requirement still calls for the run. This makes the distinction explicit without adding a new record or changing when certification runs.

## Context

[Issue #33](https://github.com/MSUHydrogeology/cairn/issues/33) reports an adopter whose full-suite certification included lengthy physical model runs. The issue asks that certification mean scoped change checks and that the whole suite become a separate ordinary check. Cairn instead now distinguishes scoped change verification from **tree certification**, which still means the configured full suite and standing gates at authorized integration points (`AGENTS.md`, Verification). The plan template already puts work-specific acceptance commands in Boundary B and scientific checks have their own proposal slot. These rules do not explicitly say whether a long model-evidence run belongs in the configured certification suite. The adopter account is reported, not independently inspected.

## Proposal

Clarify in governing and shipped guidance that scientific model runs used to establish evidence are specified and recorded with the work or release that requires them. Do not include such a run in routine tree certification merely because it is scientific evidence. Every member of the configured required suite remains required, including a scientific or slow run; accepted criteria, safety and security checks, and release requirements remain required too. Removing or rescheduling any such check needs separate authorization. Subject and duration do not exempt a run. Retain independent scientific checks and their required failing and positive controls. Preserve the current tree-certification definition, commands, triggers, and distinction from change verification. Use existing evidence records and introduce no new form, gate, label or review round.

## Rationale

A long simulation may answer a scientific question about a particular change rather than provide a useful repeatable suite check for every integration point. Keeping its obligation with the relevant work makes the reason and timing visible while retaining required evidence.

## Alternatives considered

Keep the existing text: no edits, but the reported ambiguity remains. Adopt issue #33's scoped meaning of certification: that would change the present tree-certification contract and is not delivered by this proposal. The Maintainer can choose that direction instead; it needs its own scope and review.

## Documentation / doctrine surface

Put cross-cutting prescription in `AGENTS.md` and `templates/core/AGENTS.md`, and align `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and `docs/methodology/plans.md` where necessary. Keep deliberation here in `dev/`; align proposal templates only if their existing scientific-check text conflicts.

## Evidence / verification plan

Read the current shipped and self-hosted verification and scientific-check guidance, search for direct readers and pins, and map affected tests before editing. Check two examples: an ordinary tree certification where the model run is neither a configured suite member nor otherwise required, and a required-run case where a scientific run is already a configured suite member and also serves a safety or work-specific requirement. The former must not acquire the model run solely from the new wording; the latter must retain it at every required point. Wording that waives a required run or silently changes the full-suite definition falsifies the proposal. Run applicable claim, link, snippet and neutrality gates and mapped direct-reader tests; after review record wide Boundary B on a clean final commit under canonical Python 3.13.

### Tests required

Use `python tools/test_tiers.py for` on final changed paths and search for readers and byte pins; run the mapped tests. No executable behavior change is proposed.

### Examples / smoke checks

Run `python scripts/check_cairn.py` and applicable prose gates. Compare installed and self-hosted wording against both examples.

#### Security preflight — five questions, answered in writing

S1: Authors supply the requirements and evidence; the Maintainer supplies Decisions. S2: The required-run example above should expose a waiver; it has not yet been run. S3: The implementation record will name the examples and the person applying them; no automatic check is claimed. S4: A missing required run keeps the work open under existing rules. S5: A misclassified or omitted criterion can still hide a required run; review must check the actual work and release requirements.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A required scientific run is omitted, a routine certification silently gains one, or readers cannot tell which work owns its evidence.

## Scope delta

None; opening scope.

## Assurance path

**Assurance path**: high-assurance

## Security Review -- Codex Sol -- 2026-11-01

**Tier**: Security Review  
**Reviewed commit**: 1b33ccf2  
**Verdict**: Support; no blocking security findings.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: locating work-specific scientific evidence with its requirement does not waive safety checks. The operative proposal expressly retains accepted criteria, configured required checks, release requirements and the full-suite commands. Evidence: Proposal; committed `AGENTS.md`, Verification.
2. **Best alternative?** Keep existing guidance: it already distinguishes change evidence from certification, but does not expressly address long scientific runs. A short clarification adds no apparatus and avoids redefining certification. Evidence: Proposal, Context and Alternatives; committed plan template, verification boundaries.
3. **What would show it wrong?** Excluding an existing required suite test because it is slow or scientific, or treating evidence ownership as permission to skip a required rerun, would contradict the preserved contract. Evidence: Proposal, Proposal and Signals; `AGENTS.md`, known-unmet-check rule.

**Non-blocking advice.** Make the examples distinguish optional work-specific evidence from a scientific run already required by suite membership or a safety/security requirement. Such a run remains required; removing or rescheduling it needs separate authorized scope, not this clarification. Scientific and safety evidence can overlap, so classification by subject or duration cannot decide exemption. Retain independent scientific checks, their deliberate failing control and any required positive control from the proposal template. Exercise this overlap within the already planned required-run example; add no checklist, record or stage.

**Coverage:** Read the committed proposal, governing verification rules, plan acceptance/fence guidance, scientific-check template and certification-rule assertions at `1b33ccf2`. Examined whether exclusions could bypass safety or accepted evidence. Did not inspect the adopter suite, final wording or all consumers; ran no implementation checks or suite.

## Review -- Codex gpt-6.1-terra -- 2026-11-01

Reviewed commit: 1b33ccf214ea91cf42952f0f5a0b625769eae6d2  
Target: entire proposal, especially clarity and burden  
Prior findings: none  
Assurance path: high-assurance

**Tier**: usual  
**Findings**: raised  
**Verdict**: ACCEPT  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the distinction makes the owner of scientific evidence clearer using existing records, while preserving required runs. The reported savings are not measured. -- Proposal, Context and Proposal.
2. **Best alternative.** Keep the current guidance: it already separates change verification from tree certification and records accepted scientific checks, but does not expressly resolve the reported ambiguity. -- `dev/plans/_template.md:231, 299-309`; Proposal, Alternatives considered.
3. **What would show it wrong?** A required run being omitted or the wording silently changing the full-suite contract would defeat the proposal. -- Proposal, Evidence / verification plan and Signals the change is wrong.

**N1 — non-blocking.** The ordinary-certification example assumes no work-specific requirement, but does not explicitly say whether the model run is already part of the configured suite. State that premise and add a configured-suite case: it should remain required under the proposal. This distinguishes a clarification from removing a check and makes the example easier to apply. Evidence: Proposal, Proposal and Evidence / verification plan.

Coverage: Read the committed proposal, proposal review rules and cited plan-template guidance; assessed clarity, purpose and added burden. Did not inspect the adopter's project, run examples or conduct the separate Security Review. No suite run.


## Response -- Codex gpt-6.1-terra -- 2026-11-01

**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

- N1: Accepted. The examples now distinguish a run outside the suite and other requirements from a configured suite member, which remains required.
- Security advice: Accepted. Required suite, safety and scientific checks and their controls remain in place; the required-run example covers overlapping purposes without a new record or stage.

### Withdrawn / superseded commitments

None.

## Decision -- Maintainer -- 2026-11-01

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated** (chat, 2026-11-01; scribed by Antigravity):

> "Accept both as revised under Option 1"

**Tier**: heavy. Accepted as revised under Option 1 with high assurance and required Internal + Internal Security Review plan review. Recurring additions: none.
