# Separate scientific model evidence from routine tree certification

**Author**: Codex gpt-6.1-terra
**Status**: awaiting-review
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

Clarify in governing and shipped guidance that scientific model runs used to establish evidence are specified and recorded with the work or release that requires them. Do not include such a run in routine tree certification merely because it is scientific evidence. When an applicable accepted criterion, explicitly configured required check, or release requirement calls for it, run and record it as required; this clarification does not waive that obligation. Preserve the current tree-certification definition, commands, triggers, and distinction from change verification. Use existing evidence records and introduce no new form, gate, label or review round.

## Rationale

A long simulation may answer a scientific question about a particular change rather than provide a useful repeatable suite check for every integration point. Keeping its obligation with the relevant work makes the reason and timing visible while retaining required evidence.

## Alternatives considered

Keep the existing text: no edits, but the reported ambiguity remains. Adopt issue #33's scoped meaning of certification: that would change the present tree-certification contract and is not delivered by this proposal. The Maintainer can choose that direction instead; it needs its own scope and review.

## Documentation / doctrine surface

Put cross-cutting prescription in `AGENTS.md` and `templates/core/AGENTS.md`, and align `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and `docs/methodology/plans.md` where necessary. Keep deliberation here in `dev/`; align proposal templates only if their existing scientific-check text conflicts.

## Evidence / verification plan

Read the current shipped and self-hosted verification and scientific-check guidance, search for direct readers and pins, and map affected tests before editing. Check two examples: an ordinary tree certification with no work-specific model-run requirement, and a release or accepted change that explicitly requires one. The former must not acquire the model run solely from the new wording; the latter must retain it. Wording that waives a required run or silently changes the full-suite definition falsifies the proposal. Run applicable claim, link, snippet and neutrality gates and mapped direct-reader tests; after review record wide Boundary B on a clean final commit under canonical Python 3.13.

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
