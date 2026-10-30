# Plan: Keep plan evidence necessary and concise

**Source proposal**: dev/proposals/archive/2026-10-30-codex-plan-evidence.md
**Status**: awaiting-plan-review
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

**C1.** Plans need no folder by default; extra plan documents or sidecars are prohibited unless genuinely necessary for implementation or an existing required safety or security ceremony, never to evade length limits or for reviewer convenience. Required records remain concise; reviews accept summaries or verify when necessary. Tests and scripts remain in canonical homes. Existing evidence and links are preserved; required verification and ceremonies remain intact. Live consumers discover and archive plans without folders and preserve existing folders. No new enforcement mechanism or evidence artifact is introduced.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: search live guidance, consumers, readers and byte pins; run `python tools/test_tiers.py for <changed paths>` and the listed tests, plus claim, link, snippet and neutrality gates for changed prose. Exercise actual affected discovery and archive consumers with a folderless plan and with an existing folder; report outcomes and omissions concisely. A consumer still requiring a folder, lost evidence, or a length-limit loophole fails C1. Do not run the full suite or re-anchor.

Boundary C: independent code review reads iteration evidence and runs the tightest targeted checks. Boundary B: after review, run the mapped iteration and integration/workflow selection once on the clean final commit with canonical Python 3.13, in wide mode for governing lifecycle rules; record commands, counts, interpreter, state, timing, omissions and disposition in this plan. Preserve all existing ceremony requirements.
