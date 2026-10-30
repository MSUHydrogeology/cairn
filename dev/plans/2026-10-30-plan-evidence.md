# Plan: Keep plan evidence necessary and concise

**Source proposal**: dev/proposals/archive/2026-10-30-codex-plan-evidence.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Remove mandatory plan evidence folders and prevent unnecessary extra documentation while preserving required checks.

## Source proposal

The accepted proposal removes the mandatory plan evidence folder, restricts separate evidence to genuine necessity, and preserves required checks, ceremonies and existing evidence. Reviews may accept concise agent summaries or verify when necessary.

## Scope

Revise `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and `doctrine/plans.md`, including the instruction to put long material in another file. Search live guidance, archive consumers, readers and byte pins for dependencies and update affected surfaces as needed. Preserve existing records and links. Do not add an enforcement mechanism or create evidence files for this plan.

**Reuse**: N/A: no code added. The search for `evidence folder`, `evidence director`, and `same.stem` identified the three plan rules, plus separate strategy and security-ceremony uses; those separate purposes are not plan-folder requirements.

### Documentation / doctrine surface

Plan authoring prescription lands in both plan templates; published methodology lands in `doctrine/plans.md`. Update other live guidance only where it conflicts or depends on the old requirement. Archived deliberation remains history.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Revise guidance and affected consumers or checks, preserving existing evidence. | Plan review | Consistent plan rules and necessary consumer changes. |

## Acceptance criteria

**C1.** Plans need no folder by default; extra plan documents or sidecars are prohibited unless genuinely necessary for implementation or an existing required safety or security ceremony, never to evade length limits or for reviewer convenience. For an exceptional evidence artifact, explain why it is necessary and cite it in the plan. Required records remain concise; reviews accept summaries or verify when necessary. Tests and scripts remain in canonical homes. Existing evidence and links are preserved; required verification and ceremonies remain intact. Live consumers discover and archive plans without folders and preserve existing folders. No new enforcement mechanism or evidence artifact is introduced.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: search live guidance, consumers, readers and byte pins; run `python tools/test_tiers.py for <changed paths>` and the listed tests, plus claim, link, snippet and neutrality gates for changed prose. Exercise actual affected discovery and archive consumers with a folderless plan and with an existing folder; report outcomes and omissions concisely. A consumer still requiring a folder, lost evidence, or a length-limit loophole fails C1. Do not run the full suite or re-anchor.

Boundary C: independent code review reads iteration evidence and runs the tightest targeted checks. Boundary B: after review, run the mapped iteration and integration/workflow selection once on the clean final commit with canonical Python 3.13, in wide mode for governing lifecycle rules; record commands, counts, interpreter, state, timing, omissions and disposition in this plan. Preserve all existing ceremony requirements.

## Plan review -- Codex gpt-6.1-terra -- 2026-10-30

**Obligation**: Internal
**Verdict**: Revise before implementation.
**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Nearly: C1 preserves checks, existing evidence and folderless archive behavior, but omits one accepted condition on exceptional artifacts. Source proposal, Proposal; plan, C1.
2. **Best alternative.** Keep the single chunk and concise records, adding the accepted explanation and citation condition rather than a new enforcement mechanism. Source proposal, Proposal; plan, Scope and C1.
3. **What would show it wrong?** An archive consumer that loses existing evidence, a folderless plan it cannot discover, or a sidecar used to bypass the length limit would fail C1. Plan, Verification.

**Blocking finding:** The accepted proposal requires explaining why a separate evidence artifact is necessary and citing it in the plan. C1 allows an exceptional artifact but does not carry those requirements, so implementation could satisfy the plan while missing accepted scope. Add both conditions to C1. Source proposal, Proposal; plan, C1.

**Coverage:** Read the committed plan and accepted proposal, the local plan-template lifecycle and review guidance, and searched committed live template/doctrine wording. Did not exhaustively inspect consumers, run archive behavior or assess security controls; implementation and Security Review cover those gaps. No suite run.

## Plan review -- Codex gpt-6.1-sol -- 2026-10-30

Reviewed commit: 20bd9d3ac2c08dd019322a07b4fd2e9655900f0c
Target: operative plan and security consequences
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: Accept security design; ordinary review's scope finding remains.
**Elapsed**: approximately 3 minutes, including serialization wait
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes for security: C1 retains required verification, security ceremonies and existing evidence, while Scope forbids new enforcement machinery. Plan, Scope and Acceptance criteria.
2. **Best alternative.** Use the existing concise lifecycle records and canonical tests/scripts, allowing exceptional evidence only when necessary; an absolute ban could obstruct existing ceremony obligations. Accepted proposal, Proposal; plan, C1.
3. **What would show it wrong?** Lost evidence during archive, a consumer requiring folders, or a ceremony losing required records. Verification exercises both folder cases and preserves ceremonies, with independent targeted review before wide final integration. Plan, Verification.

No additional security blocker found. Summaries do not waive required checks, and independent verification remains available. The ordinary pass separately identifies the accepted requirement to explain and cite exceptional artifacts; its correction remains owed before implementation.

**Covered**: committed plan, accepted proposal, relevant template folder/review rules, and doctrine's archive and verification obligations. **Not covered**: implementation, exhaustive consumer discovery, archive execution or ceremony execution. No tests or suite run.

## Response to plan review -- Codex gpt-6.1-terra -- 2026-10-30

**Elapsed**: unknown
**Tokens**: unknown

- Ordinary review: Added the accepted necessity explanation and citation conditions to C1.
- Security Review: No additional findings; implementation coverage remains outstanding.

## Implementation verification -- Codex gpt-6.1-luna -- 2026-10-30

**Elapsed**: approximately 15 seconds for mapped tests; prose gates under 2 seconds. **Tokens**: unknown.

**Boundary A**: `python tools/test_tiers.py for` the four changed guidance files and this plan selected 19 test files. `python -m pytest` on that list: 1,038 passed in 12.12 seconds. Python 3.12.9. This was measured once in the shared dirty tree before commit `dfb096b4`; unrelated API-dispatch edits and local untracked files were present. It is preliminary evidence, not a clean committed-copy result. Per the accepted test-once workflow, do not repeat iteration; the clean canonical run is owed at Boundary B after code review.

**Prose gates**: `claim_check.py` on this plan passed; `link_check.py` and `sync_doc_snippets.py --check` on all four changed prose files passed; `quality_gate.py --sub neutrality` reported 0 failures and 43 informational findings. These also ran in the shared dirty tree. `git diff --check` passed for the four implementation paths.

**Coverage and limits**: Changed surfaces are the local and shipped plan templates, plan doctrine, and architecture-review artifact guidance. The mapped board tests include archived-plan Markdown fixtures and verify they are listed; they do not create or preserve a corresponding evidence folder. The session discovery fixture is a proposal, not a plan. I did not explicitly exercise a folderless plan or preservation of an existing folder. Source inspection found `tools/board.py` reads direct Markdown entries in live and archive directories, while `tools/session.py` reads direct live Markdown entries; neither writes or archives plans. Archiving is a Git move, so no executable archive consumer was found to exercise. The test output did not capture per-file durations. No clean-tree or canonical Python 3.13 result is claimed here. Boundary B is `wide` because this changes governing lifecycle rules; run the mapped iteration and integration/workflow selection once on the clean final commit after review, and record its SHA/range, interpreter, state, commands, counts, timing and omissions below. **Certified by**: pending.

## Code review -- Codex gpt-6.1-terra -- 2026-10-30

**Reviewed**: implementation `dfb096b4`; verification record `5e2b0f9e`. **Verdict**: Revise verification. **Bounding**: WIDER RUN REQUIRED for the named scenarios below. **Elapsed**: approximately 4 minutes; **Tokens**: unknown.

**Foundations**

1. **Should it happen as framed?** Yes: both plan templates and `doctrine/plans.md` remove the automatic folder and restrict separate artifacts, while the architecture-review frame removes its folder assumption (`dfb096b4`).
2. **Best alternative.** Keep concise records and canonical tests, with the stated exception for necessary implementation or ceremony evidence; an absolute ban could obstruct a required ceremony (accepted proposal, Alternatives).
3. **What would show it wrong?** A folderless plan missed by discovery, existing evidence lost on archive, or an allowed length-limit workaround would fail C1 (plan, Verification).

**Blocking finding:** Boundary A explicitly requires exercising actual affected discovery and archive consumers with a folderless plan and an existing folder. The implementation record reports no explicit folderless plan or folder-preservation scenario, and its mapped run was in a shared dirty tree rather than a copy of the commit. Source inspection says discovery is read-only and no executable archive consumer was found; exercise applicable discovery with both cases on committed bytes, and substantiate the archive omission or exercise the actual path. Record outcomes and limitations. The clean canonical Boundary B remains due after review.

**Coverage:** Read the accepted proposal, committed implementation diff, plan and verification record; searched committed live guidance for the original folder terms and checked the strategy-template matches. No suite run; did not independently exercise discovery, archive, or security ceremonies. Separate Security Review remains due.

## Response to code review -- Codex gpt-6.1-luna -- 2026-10-30

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

- **Folderless and existing-folder discovery / archive finding: accept.** In an isolated clone of reviewed commit `4009db75e15d4b3787d2fbff70815326e35d3bfa`, I created one plan without a folder and one plan with a same-stem folder containing `record.txt`. `tools/board.py --json` listed both live plan files; `tools/session.py`'s `_in_flight_items` listed both plans. I then moved both Markdown plans into `dev/plans/archive` with `git mv`, moved the existing sidecar folder alongside its plan, and committed only inside the temporary clone. `tools/board.py --json --archive` listed both archived plans, the existing `record.txt` remained byte-identical, and the folderless plan still had no folder. No temporary scenario files were written to the shared repository.
- This exercises the actual board and session discovery readers and the manual Git archive path. Source inspection found no programmatic archive command. The earlier mapped session fixture covers a proposal, not a plan; no extra broad test run was made. Clean canonical Boundary B remains due after the Security Review.
