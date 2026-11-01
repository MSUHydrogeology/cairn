# Plan: Reduce template burden

**Source proposal**: dev/proposals/archive/2026-10-30-codex-template-burden.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Shorten the proposal and plan templates while retaining the instructions and safeguards authors need.

## Source proposal

The Maintainer accepted the heavy proposal: correct the contradictory plan preambles and reduce repetition in four templates while preserving obligations, machine contracts and independently usable installed guidance.

## Scope

Edit `dev/proposals/_template.md`, `dev/plans/_template.md` and their counterparts under `templates/core/dev/`; update existing affected consumers only if needed. No new documents, tools or line quota. Reuse: N/A, no code added. Doctrine surface: the four authoring templates, with governing and shipped guidance checked for consistency. Candidate repetitions include External-read rules and review skeletons, plan Boundary B instructions, copy guidance, and scope-delta instructions; the contradictory proposal-response text in both plan preambles must change. Retain useful local prompts even where duplication serves the reader.

Concrete candidates at baseline `2c24fec4`: self-hosted proposal External-read instructions at lines 91–121 and review skeleton at 435; installed proposal equivalents at 73–103 and 382. Self-hosted plan External-read instructions at 96–126 and skeleton at 418; installed plan equivalents at 98–128 and 414. Both plan templates repeat Boundary B at 305–325 and 356–366 (self-hosted), and 299–320 and 352–362 (installed). Copy instructions recur at each template's opening and its “Never copy” bullet: proposal lines 1 and 139 (self-hosted), 1 and 121 (installed); plan lines 1 and 146 (self-hosted), 3 and 148 (installed). Assess each for consolidation without losing its point-of-use prompt or any obligation.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory rules, readers, slots, pins and tests; consolidate templates and any necessarily affected existing consumers. | Both plan reviews and their dispositions. | Four usable templates and scoped iteration evidence. |
| C2 | Independent code and Security Reviews; address findings, then run final integration. | C1 committed. | Review and wide Boundary B records. |

## Acceptance criteria

C1: Both plan preambles describe in-place proposal revision. Each original obligation and machine-recognized heading, slot or other contract remains accessible to its intended reader or its changed consumer is verified; installed readers need only shipped guidance. Compare all four with the accepted rules and each other, naming the location of each obligation. Compare baseline and final reading and authoring burden, including cross-reading and retained repetition; explain immaterial safe cuts. No routine evidence folder. A missing obligation, broken consumer or greater cross-reading falsifies the outcome.

C2: Both reviews are recorded and findings disposed; the final clean commit passes the required wide checks. Security preflight S2/S3: use the individual-copy mutations below to test the named checks and their selectors; report uncovered obligations rather than claiming automated coverage. S1, S4 and S5 remain as in the proposal. Independent scientific check: N/A, no scientific result or assumption changed.

## Scope delta

**Scope delta**: preserved

## Verification

Baseline is the decision commit `2c24fec4`. Before editing, search all tracked readers, byte pins, slot and lifecycle consumers for each of the four paths and relevant markers; verify negative searches with known positives in `bootstrap/tests/test_review_stance_in_shipped_files.py` and `bootstrap/tests/test_install_report_slots.py`. Open each identified consumer and its actual entry point. The current `python tools/test_tiers.py for` selection for the four paths is: `bootstrap/tests/test_board_json_contract.py`, `test_certifying_run_rule.py`, `test_claim_check_module.py`, `test_core_dev_folders.py`, `test_documentation_plan_module.py`, `test_incident_trackers_module.py`, `test_install_module.py`, `test_install_report_slots.py`, `test_quickstart_sequence.py`, `test_replacement_tools.py`, `test_review_and_verification_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_scaffold.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_session_routines.py`, `test_status_vocabulary_advisory.py`, and `test_verification_boundaries.py` (all latter names in `bootstrap/tests/`). Re-run the selector for all changed paths and execute its exact iteration list, plus applicable claim, link, snippet and neutrality gates. Preserve pinned checks; do not weaken a test to permit a lost rule.

For S2/S3, list the four files and each relevant obligation/consumer set from the committed tree. In separate copies of the commit remove a required slot marker, a required review/security instruction, and a verification or scope obligation from each applicable member; run the actual mapped consumer entry point or comparison against each mutant. Report the selector, input set, outcomes and omissions; where automated tests do not detect a loss, the explicit baseline-to-final obligation comparison is the human check, exercised against a known deletion. Do not claim all-member coverage without mutating each member. Installed paths are checked through the scaffold/install entry point as well as their source text; retain parser markers unless changed consumers are verified together.

After both code reviews and any targeted re-review, run Boundary B once in `wide` mode on the clean final commit with canonical Python 3.13.x: the reviewed-range iteration selection, mapped integration/workflow tests, owning families, installed public paths and standing gates. Record the full SHA/range, clean pre/post state, interpreter, commands, counts, timing, non-pass dispositions, omissions and `Certified by: pending` in the implementation record. No full-tree certification or re-anchor is authorized here.

## Plan review -- Codex (GPT-6) -- 2026-11-01

**Reviewed commit**: 68b362c1
**Obligation**: Internal
**Verdict**: Revise; one blocking finding.
**Elapsed**: 2 minutes (estimated)
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes. The accepted proposal preserves installed guidance and machine contracts while correcting the contradictory preambles; the plan carries both into C1 and requires wide verification.
2. **Best alternative.** Correct only the contradiction if meaningful safe cuts cannot be made. This reduces risk but leaves the duplicated instructions; the proposal requires explaining that result rather than presuming it.
3. **What would show it wrong?** A lost obligation, broken consumer, or increased cross-reading would defeat the proposal's purpose; C1 explicitly checks each.

**R1 -- Blocking:** The accepted proposal's Evidence / verification plan requires the plan to identify concrete repeated passages. Its Scope names topics but no passages or locations. For example, the committed self-hosted plan template describes External reads at lines 98–115 and supplies an External review skeleton at line 417; Boundary B appears at lines 305–325 and 356–366. Identify concrete candidates across the affected templates so the author can assess meaningful consolidation while retaining useful prompts. The accepted requirement is not yet met.

Coverage: compared the plan with the accepted proposal and its apparatus predecessor and sampled the committed plan template. Did not inventory every template obligation or consumer, run implementation checks, or assess security controls independently.


## Plan review -- Codex (gpt-6.1-sol) -- 2026-11-01

```
Reviewed commit: 68b362c1b6c1e2ae89e2be31a89ae296bdcc23c3
Target: security preservation, consumer checks and installed guidance
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT (Security obligation only)
**Elapsed**: 4 minutes (estimated)
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes. C1 preserves every obligation and machine contract, requires independently usable installed guidance, and forbids greater cross-reading. Those match the accepted proposal's Proposal and Security preflight; C2 keeps separate code and Security Reviews (plan, Acceptance criteria and Sequence).
2. **Best alternative.** Consolidate within each template using existing consumers and concise records. The plan already chooses that route: no new documents or tools, no routine evidence folder, and no weakened pins (Scope and Verification). Moving rules to doctrine would lose adopter access (`bootstrap/tests/test_review_stance_in_shipped_files.py`, opening installed-boundary explanation).
3. **What would show it wrong.** A removed gate or marker escaping detection, or installed text depending on unshipped guidance. Verification requires individual-copy deletions across applicable members, actual consumer entry points, a human comparison exercised against deletion where automation misses, and scaffold/install checks. The named controls are real: `test_review_stance_in_shipped_files.py` lists all four template carriers; `test_install_report_slots.py::_install` invokes `bootstrap/scaffold.py`.

No blocking security finding. Ordinary review's scope-delivery finding remains independent; this pass grants no implementation authority while it is unresolved.

Coverage: read the committed plan, accepted proposal and Decision, current plan-review template, and named consumer-control sources. Did not inventory every consumer, execute mutations or tests, measure burden, or verify future implementation; those remain implementation evidence and independent code review.

## Response to plan review -- Codex (gpt-6.1) -- 2026-11-01

**Elapsed**: 2 minutes (estimated)
**Tokens**: unknown

R1: Accepted; Scope now names concrete repeated passages in all four templates at the baseline. Security Review: no findings.

## C1 implementation evidence -- Codex (gpt-6.1-sol) -- 2026-11-01

**Elapsed**: 4 minutes (estimated)
**Tokens**: unknown

**Commits**: `6965d3ba` implements the cuts; `bf60c2ab` corrects both plan preambles to say proposal operative text is revised in place, its review history remains appended, and plan cells revise in place until implementation.

**Obligation comparison**:

| File | Preserved obligations and locations; readers / consumers |
|---|---|
| `dev/proposals/_template.md` | Lifecycle; Review (three questions, External, Security Review); Evidence / verification (tests, smoke checks, S1–S5, scientific checks); Scope delta; Assurance path; Review / Response / Decision skeletons. Read directly by `test_review_stance_in_shipped_files.py`, `test_scope_reduction_trap.py`, `test_scaffold.py`'s security-preflight check, and board / verification readers. |
| `templates/core/dev/proposals/_template.md` | Same author obligations and fields, with project prompts in the five existing slots. Its slot and install consumers include `test_install_report_slots.py`, `test_documentation_plan_module.py`, and `bootstrap/scaffold.py`; shipped readers also use the review and scope checks above. |
| `dev/plans/_template.md` | Lifecycle and Review (External and Security Review); Scope / Sequence / Acceptance criteria; Scope delta; Verification (A/B/C and record fields); sidecar rules; Dispositions and Plan / Code review skeletons. Read by the review, scope, verification-boundary, board, scaffold and security-preflight checks. |
| `templates/core/dev/plans/_template.md` | Same plan obligations, with project prompts in its three existing slots. Installed slot and scaffold consumers include `test_install_report_slots.py`, `test_documentation_plan_module.py`, and `bootstrap/scaffold.py`; shipped readers also use the review, scope and verification checks above. |

Across all four files, heading sets and markers match baseline: 19 headings and the same five proposal slots per copy (`triage-extra-triggers`, `documentation-tier-home`, `tests-tier-home`, `examples-smoke-home`, `assurance-path-triggers`); 14 headings and the same three plan slots per copy (`documentation-tier-home`, `acceptance-doc-tooling`, `verification-commands`). Installed guidance remains usable from shipped `AGENTS.md` and `dev/` without doctrine.

**Candidate disposition and burden**: opening copy instructions state the operative range; the later Keep Short bullets retain detailed exclusions. The shorter Boundary B reminder follows its full contract and record fields. External-read rules and review skeletons remain because each template serves a separate lifecycle stage and their obligations are pinned. Scope delta remains distinct: a proposal may narrow its as-opened baseline before Decision, while a plan may not silently reduce accepted scope. Against baseline `2c24fec4`, the final templates are 24 lines and 274 whitespace-counted words shorter combined (a rough burden measure, not a target).

**Iteration and controls**: the exact 18-file selector passed 1,037 tests in 12.53 seconds on Python 3.12.9 at `6965d3ba`; after the preamble correction, the two directly relevant review / verification files passed 577 tests in 1.58 seconds at `bf60c2ab`. The matching deletion controls detected removed slot, review / security, and scope obligations across separate copies of the four files: installed slot losses were detected through the scaffold install test; self-hosted slot losses were detected by comparing the baseline marker with each known-deletion mutant. Readers named in the plan include `test_review_stance_in_shipped_files.py`, `test_install_report_slots.py` (whose `_install` runs `bootstrap/scaffold.py`), `test_scope_reduction_trap.py`, and `test_verification_boundaries.py`. Claim, link, snippet-sync, and neutrality gates passed; `claim_check.py` passed on all four templates.

**Omissions**: the self-hosted slot comparison is a human control because no runtime installer consumes those source copies. Boundary B remains due after code review; no full-tree certification or re-anchor was run.
