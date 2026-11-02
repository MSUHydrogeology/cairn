# Plan: Align the focused-testing example

**Source proposal**: dev/proposals/archive/2026-11-01-codex-focused-testing-example.md
**Status**: awaiting-plan-review
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

The installer mapping in `bootstrap/_scaffold/config.py` sends the template to `docs/DOCUMENTATION_PLAN.md`; `bootstrap/tests/test_documentation_plan_module.py` exercises the default install and content. Inspect a fresh installed copy for the replacement and include the install test family in wide Boundary B. Identify other integration or workflow checks from the tier map and reader search, and record their coverage or omissions. No installer change is planned.

Boundary C: independent code reviewers use targeted falsification, including a separate Security Review, before final integration. Boundary B: on the clean final reviewed commit under canonical Python 3.13.x, run wide coverage of the mapped iteration tests, applicable integration and workflow tests, install public path, standing gates and acceptance checks. Record full SHA and reviewed range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens or unknown, non-pass disposition and omissions. Record timing misses and test files over ten seconds as required. A missing required check keeps the work open; full-tree certification is separate and not authorized by this plan.
