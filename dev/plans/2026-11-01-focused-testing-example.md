# Plan: Align the focused-testing example

**Source proposal**: dev/proposals/archive/2026-11-01-codex-focused-testing-example.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Correct the shipped testing example so it illustrates focused testing without weakening required verification.

## Source proposal

The accepted heavy proposal replaces the testing example in the shipped documentation-plan template while preserving its operational reminder and paired rationale. The Decision requires ordinary and Security plan review.

## Scope

Change only the quoted testing example in `templates/modules/default-on/documentation_plan_template.md`. Preserve the surrounding paired-update explanation, testing policy, and install behavior. Reuse: N/A: no code added.

### Documentation / doctrine surface

The example is in the shipped, domain-local governing template; deliberation remains in `dev/`. No cross-cutting prescription or descriptive documentation changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Replace the example and verify its readers and installed path | Both required plan reviews and author response | Focused reminder and implementation evidence |

## Acceptance criteria

C1: The example reminds readers to run focused tests for changed files, does not imply these exhaust required integration or security checks, and preserves the rationale pairing. Only the quoted example changes. Search direct readers and byte pins, validate the search with a known-positive result, and resolve or report any reader requiring the old wording. Confirm the installed public path retains the replacement. Run the mapped checks and prose gates; record results and omissions. No independent scientific check applies.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation, `python tools/test_tiers.py for templates/modules/default-on/documentation_plan_template.md` selected `bootstrap/tests/test_review_stance_in_shipped_files.py`; its `_DESCRIPTIVE_FILES` parameterization reads the template for review-stance obligations, not the testing example. Re-run the selector on the implementation bytes. Search paths, filename and old wording for readers and byte pins, with the known-positive `bootstrap/_scaffold/config.py` mapping as a control; inspect findings and triggers.

Boundary A: run the selected test file and `python scripts/claim_check.py`, `python scripts/link_check.py`, and `python scripts/sync_doc_snippets.py --check` on the changed template, plus `python scripts/quality_gate.py --sub neutrality`. These check path claims, links, snippet drift, and vendor neutrality respectively. Compare the paragraph with `AGENTS.md` verification guidance. Record commands, outcomes and omissions.

Check triggers and limits: `claim_check.py` main passes the explicit file to `check_file`, which reads and scans its text for resolvable path and line claims; it does not judge the testing advice. `link_check.py` main passes explicit files to `check_tree`, which reads Markdown links and anchors; external links are not probed by default. `sync_doc_snippets.py` main passes the explicit file to `_process_doc`, which reads snippet directives and compares their blocks to source regions; absent directives, it checks no snippet. `quality_gate.py` selects `_run_neutrality` for `--sub neutrality`; its walker includes Markdown under `templates/`, then scans vendor tokens and forbidden directives, not testing semantics. The mapped test's `test_descriptive_page_omits_the_old_wording` reads the template through `_DESCRIPTIVE_FILES` and rejects old review-stance phrases, not the testing example. The human paragraph comparison and fresh install inspection address that gap.

The installer mapping in `bootstrap/_scaffold/config.py` sends the template to `docs/DOCUMENTATION_PLAN.md`; `bootstrap/tests/test_documentation_plan_module.py` exercises the default install and content. Inspect a fresh installed copy for the replacement and include the install test family in wide Boundary B. Identify other integration or workflow checks from the tier map and reader search, and record their coverage or omissions. No installer change is planned.

Boundary C: independent code reviewers use targeted falsification, including a separate Security Review, before final integration. Boundary B: on the clean final reviewed commit under canonical Python 3.13.x, run wide coverage of the mapped iteration tests, applicable integration and workflow tests, install public path, standing gates and acceptance checks. Record full SHA and reviewed range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens or unknown, non-pass disposition and omissions. Record timing misses and test files over ten seconds as required. A missing required check keeps the work open; full-tree certification is separate and not authorized by this plan.

## Ordinary plan review -- Codex GPT-6.1 Sol -- 2026-11-01

**Obligation:** Internal
**Verdict:** Revise before implementation; one blocking finding.

**Foundations**

- **Should it happen as framed?** Yes: C1 changes only the example, preserves the pairing and required checks, and maps the installed destination. Evidence: plan Scope and C1; `bootstrap/_scaffold/config.py:1094-1095`.
- **Best alternative:** No simpler path delivers the accepted outcome: deleting the example loses the concrete pairing, while leaving it retains the conflicting full-suite example. Evidence: accepted proposal Alternatives; template paired-update paragraph.
- **What would show it wrong?** A check that does not actually read the changed passage, an old-wording pin, or an installed copy without the replacement would undermine the stated assurance. Evidence: accepted proposal S3 and Tests required; plan Verification.

**Blocking finding:** The accepted proposal S3 requires the existing checks' actual triggers and coverage to be opened and recorded in the plan. Verification names the prose gates and describes their purposes, but does not establish their invocation triggers or what each actually reads; the selected test's description alone does not cover the gates. Open each named trigger through its runner and record applicable coverage and limitations in the operative plan before implementation. Do not add checks beyond the accepted scope merely to fill the record.

**Coverage:** Read the plan, accepted proposal and Decision, current plan template, shipped example, installer mapping and named test references at `dcf727d1`. Did not trace every gate runner or independently inspect installed output; implementation and Security Review remain outstanding. No suite run. Elapsed: approximately 5 minutes; tokens: unknown.

## Response -- Codex GPT-6.1 Sol -- 2026-11-01

Accepted the blocking finding. Verification now names each gate's runner, input and coverage limits, and distinguishes the mapped test's review-stance check from human inspection of the example and installed output. Security plan review remains outstanding.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: 542f94185934ed590f3f7224bcd92d2f3655f72e  
Target: entire revised plan against the accepted proposal  
Prior findings: none in this separate Security pass  
Assurance path: heavy, inherited from accepted proposal

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 2 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. The plan confines the edit to the misleading quoted example and expressly preserves integration and security obligations, surrounding rationale and installer behavior. The separate Security code review precedes final wide verification. -- Plan, Scope, C1 and Verification; accepted proposal, Proposal and Decision.
2. **Best alternative.** A concise replacement plus paragraph comparison and installed-copy inspection delivers the outcome without a new test-selection mechanism. Deleting the example loses the pairing illustration; the planned existing checks and human inspection retain it. -- Plan, C1 and Verification; template, paired-update paragraph; accepted proposal, Alternatives considered.
3. **What would show it wrong?** Replacement wording suggesting changed-file tests exhaust required assurance, a hidden old-wording reader, or an installed copy retaining the old example. The plan assigns reader searches a known-positive mapping control and explicitly distinguishes gate coverage from human semantic and installation checks. -- Plan, C1 and Verification; installer mapping in `bootstrap/_scaffold/config.py`; `bootstrap/tests/test_documentation_plan_module.py`, TestForkableContent.

No blocking security gap found. The revised trigger descriptions accurately limit what the existing checks establish; they do not claim the review-stance test verifies testing semantics.

Coverage: read the committed plan, accepted proposal, current plan template, shipped example, gate entry points, mapped test and installer mapping/content-test paths. Did not run implementation checks, reader discovery or a fresh install, or inspect replacement wording that is not yet implemented. No suite run.
