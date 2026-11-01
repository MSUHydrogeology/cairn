# Plan: Reduce template burden

**Source proposal**: dev/proposals/archive/2026-10-30-codex-template-burden.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Shorten the proposal and plan templates while retaining the instructions and safeguards authors need.

## Source proposal

The Maintainer accepted the heavy proposal: correct the contradictory plan preambles and reduce repetition in four templates while preserving obligations, machine contracts and independently usable installed guidance.

## Scope

Edit `dev/proposals/_template.md`, `dev/plans/_template.md` and their counterparts under `templates/core/dev/`; update existing affected consumers only if needed. No new documents, tools or line quota. Reuse: N/A, no code added. Doctrine surface: the four authoring templates, with governing and shipped guidance checked for consistency. Candidate repetitions include External-read rules and review skeletons, plan Boundary B instructions, copy guidance, and scope-delta instructions; the contradictory proposal-response text in both plan preambles must change. Retain useful local prompts even where duplication serves the reader.

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
