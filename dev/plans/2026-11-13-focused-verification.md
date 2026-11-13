# Plan: Focus verification on delivered promises

**Source proposal**: dev/proposals/archive/2026-11-12-codex-focused-verification-cost.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-13
**In brief**: Check changed promises as plans finish and join related work at the end of the development arc.

## Build summary

Make the self-hosted, shipped and public guidance agree on focused checks and evidence reuse. Plans finish after their own required checks and reviews; the arc owner joins interactions later. Keep security, scientific and release obligations intact.

## Source proposal

The [accepted proposal](../proposals/archive/2026-11-12-codex-focused-verification-cost.md) places this consistency repair in v0.7 and defines the changed selection and integration rules. Its Decision authorizes this plan, not baseline application, signing, publication or another full suite.

## Scope

Doctrine and shipped guidance: `dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md`; public explanations: `docs/methodology/plans.md`, `docs/methodology/dual-review.md`; authoring templates: `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`. `AGENTS.md` routing remains unchanged. No new forms, tools, checkers, roles, gates, coordination rewrite or permanent tests are in scope. Reuse: N/A, no code added.

## Sequence

Estimate 4.5–8 agent-hours and 2–5 elapsed hours including release packet refresh, with reviewer availability and affected reader bindings uncertain. Plan review precedes implementation. After approval C1 and C2 can run in parallel, each owning only its named files; the coordinator owns plan records, board, changelog, review disposition and closure. Each worker claims its exact paths and commits its own files. Required ordinary and Security code reviews follow the combined implementation; correct findings and run affected checks before archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Guidance and public explanations: the two collaboration files and two methodology files | Reviewed plan | Consistent operative and public rules |
| C2 | Both plan and both proposal templates | Reviewed plan | Matching authoring guidance and one short example |
| C3 | Coordinator joins evidence, reviews and corrections; records closure | C1 and C2 | Reviewed, verified plan ready to archive |

The existing item 12 release-closeout owner refreshes the AST packet's exact-candidate binding and affected reader bindings after the final committed guidance, reusing applicable AST body analysis. This is release work in `dev/PLANNING.md` item 12, not a plan completion or human baseline gate. The baseline remains unpassed until the named Maintainer operation supplies evidence. The known certification at `072d82d2` had 5,344 passed, 63 skipped and six failed in 49m06s; five corrected cases have 14 targeted passes. No full repeat is required for this documentation change.

## Acceptance criteria

**C1.** Name changed caller-visible promises, public entry points and outputs; select the smallest checks for plausible faults and reuse results only where bytes, platform, input and obligation still apply, citing source and limits. Review may use committed evidence or static calculation when adequate, with executable evidence for forward behavior. Remove blanket scratch attempts and per-member mutations; universal claims inventory their members and check applicable paths. Preserve scientific *touches* triggers and independent error and positive controls, required security checks and reviews, and S2's valid existing negative control; a new security check has a demonstrated failing case.

Plans complete required checks, reviews and dispositions before archive. One joined run follows connected plans, or occurs earlier at a named critical shared boundary. Before arc completion or release, the arc owner records final combined revision coverage, producers, consumers, results and omissions; applicable prior results cover unchanged behavior and inputs, and corrections rerun only affected interactions. The arc owner owns and records a post-archive defect's repair under existing rules without reopening the archived plan. Failed promises and required checks remain plan work before archive.

**C2.** Templates express the same rules and preserve scientific, security and release triggers. One short plan example names a changed output and its check, a reused control with its limit, and a later joined run. It does not require a mutant or scratch attempt for each claim. Shipped and self-hosted template pairs agree.

**C3.** Independent ordinary and Security reviews test the combined text against the accepted proposal and name gaps; findings and required checks are disposed before archive. The item 12 owner receives the candidate-refresh trigger and evidence location. No human baseline operation blocks this plan's closure.

## Scope delta

**Scope delta**: preserved.

## Verification

Check the eight files against the accepted proposal and existing obligations, including a known-positive search when searching for retired instructions. Compare each shipped pair with its self-hosted counterpart. Run claim, link, snippet and neutrality prose gates; inspect readers and byte pins before selecting affected tests. At minimum run `bootstrap/tests/contract/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site` for the installer acceptance slot and `bootstrap/tests/test_review_sweep_ships.py::test_every_install_carries_the_sweep_as_shipped` for installed review guidance if their actual paths exercise the edited text. Select other real affected public/shipping nodes from their test bodies, not all 18 mapper owners; explain omissions and any applicable prior evidence. Do not add wording pins or permanent tests for this prose. A failed required check remains open; no full suite solely for this change. Record commands, results, limits, elapsed time and tokens in existing plan records.
