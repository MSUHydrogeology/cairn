# Plan: Align the focused-testing example

**Source proposal**: dev/proposals/archive/2026-11-01-codex-focused-testing-example.md
**Status**: awaiting-code-review
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

## Plan review response -- Codex GPT-6.1 Sol -- 2026-11-01

The ordinary finding was addressed in the operative Verification section and response at `542f9418`. The separate Security plan review found no issues. Both required plan review obligations are recorded; implementation can begin.

**Elapsed**: less than one minute. **Tokens**: unknown.

## Implementation verification -- Luna -- 2026-11-01

**Boundary B mode**: wide, pending the required post-review integration run. The shipped template is a named high-risk surface; the final run must include mapped install and workflow coverage plus standing gates.

**Tested commit**: `a39171cc048101f12847e080b47ef786c5b75387`  
**Iteration range**: `c2d000f4`..`a39171cc048101f12847e080b47ef786c5b75387`  
**Interpreter/runtime**: `/Users/kendal30/conda_envs/miniforge3/bin/python`, Python 3.12.9  
**Pre-run state**: clean isolated copy at the tested commit. **Post-run state**: clean, same `HEAD`.

| Command | Exit | Outcome | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_review_stance_in_shipped_files.py` | 0 | 482 passed | 1.652 s | unknown |
| `python scripts/claim_check.py templates/modules/default-on/documentation_plan_template.md` | 0 | OK | 0.041 s | unknown |
| `python scripts/link_check.py templates/modules/default-on/documentation_plan_template.md` | 0 | 1 Markdown file; no issues | 0.084 s | unknown |
| `python scripts/sync_doc_snippets.py --check templates/modules/default-on/documentation_plan_template.md` | 0 | 1 document; no drift | 0.041 s | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational findings | 0.888 s | unknown |

**Plan-specific acceptance commands**: `python tools/test_tiers.py for templates/modules/default-on/documentation_plan_template.md` selected only `bootstrap/tests/test_review_stance_in_shipped_files.py`. Reader search found the positive installer mapping at `bootstrap/_scaffold/config.py:1094` and the mapped test reference at `bootstrap/tests/test_review_stance_in_shipped_files.py:1556`; the old wording is absent from the shipped template. The replacement keeps the paired rationale and says required integration and security checks still apply.

**Non-pass disposition**: none. **Known omissions**: the fresh installed output, `bootstrap/tests/test_documentation_plan_module.py`, and wide integration/workflow coverage remain for the post-review Boundary B run. No full-tree suite was run. **Elapsed for the recorded checks**: about 3 seconds total. **Token use**: unknown.

## Code review -- Codex GPT-6.1 Sol -- 2026-11-01

**Verdict**: Accept; no findings. Reviewed implementation `a39171cc048101f12847e080b47ef786c5b75387` and iteration record at `776bb359`.

**Foundations**: Should it happen as framed? Yes: the diff changes only the example, retains the paired rationale, and explicitly retains required integration and security checks, as C1 requires. Best alternative: removing the example would also remove the misleading suite instruction but lose the concrete reminder/rationale pairing; the replacement preserves it. What would show this wrong? An installed copy with the old example, a reader requiring its old wording, or wording implying focused tests exhaust required checks would defeat C1. The recorded gates do not establish those semantic or installation claims.

**Evidence**: The implementation diff and accepted proposal establish the limited scope; the iteration record reports the mapped test and prose gates passing on an isolated committed copy. A targeted committed-tree search found the installer mapping and test reference, plus documentation and administrative references; a search for the exact old sentence found no match in bootstrap, scripts, templates or docs. The lockfile and allowlist references name the path, not the old sentence. The install inspection and wide final verification remain pending, as recorded.

**Coverage**: Read the accepted proposal, plan, implementation diff, iteration evidence and targeted search results. Did not run the implementation tests, inspect a fresh installed copy, or perform Security Review; the latter two remain separate obligations. No suite run. Elapsed: approximately 4 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: a39171cc048101f12847e080b47ef786c5b75387  
Target: focused-testing template diff, `c2d000f4`..`a39171cc`, with iteration and ordinary review at `79a03dfa`  
Prior findings: none  
**Tier**: Security Review  
**Verdict**: ACCEPT; no findings.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The replacement explicitly requires integration and security checks alongside focused changed-file tests. It preserves the operational reminder/rationale pairing without changing policy, installer logic or trust boundaries. -- Implementation diff at `a39171cc`; accepted proposal, Proposal; plan C1.
2. **Best alternative.** Retain this concise example. Deletion removes the concrete pairing; adding selection machinery exceeds the accepted wording-only correction. -- Template, paired-update paragraph; accepted proposal, Alternatives considered and scope.
3. **What would show it wrong?** A broader edit, missing security obligation or changed install destination. A targeted committed-byte assertion compared parent and implementation: replacing exactly the quoted example reproduces the entire resulting file; the required integration/security phrase, rationale and installer mapping remain. All assertions passed. -- `a39171cc`, template and `bootstrap/_scaffold/config.py`.

**Bounding**: ACCEPTED — challenged the mapped test's semantic gap using direct committed-byte comparison. The iteration record correctly limits that test to review-stance wording; fresh-install inspection and install-family coverage remain explicitly owed in post-review wide Boundary B, rather than claimed complete here.

No fenced chunk or deviation request is present in the reviewed plan history, so no Waiting line became due. Luna's implementation fits the accepted-plan execution floor.

Coverage: read accepted scope, committed diff, iteration evidence, ordinary review and installer mapping; performed the targeted byte assertions. Did not rerun implementation checks, run a suite or mutation, inspect a fresh installation, or certify the tree. Final canonical-Python wide Boundary B remains outstanding.

## Completion follow-up

Close GitHub issue #42 once the acceptance criteria and final required verification are complete.
