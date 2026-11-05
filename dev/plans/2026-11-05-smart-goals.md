# Plan: Achievable SMART goals

**Source proposal**: [Achievable plans that finish](../proposals/archive/2026-11-05-codex-atomic-implementation-plans.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal)
**Opened**: 2026-11-05
**In brief**: Teach authors to set useful, independently finishable plan goals without losing accepted work.

## Source proposal

The [accepted proposal](../proposals/archive/2026-11-05-codex-atomic-implementation-plans.md) directs existing guidance to teach SMART goals and independent completion, preserving scope and checks without splitting work by default. The Decision at `1fe81f7a` authorizes ordinary plan and code reviews, not Security Review.

## Scope

Deliver one useful outcome: local and shipped authoring surfaces and existing guides consistently teach goal-first, independent completion, demonstrated in source and real installations. This helps authors choose achievable work while retaining the proposal's larger objective. Update `AGENTS.md` and `templates/core/AGENTS.md`; local and shipped `dev/proposals/_template.md` and `dev/plans/_template.md`; and `docs/methodology/proposals.md`, `docs/methodology/plans.md`, and `docs/methodology/lifecycle.md`. Extend the existing completion mapping and tests in `bootstrap/tests/test_review_sweep_ships.py`. Update `CHANGELOG.md` in the same or next implementation commit through parent serialization.

**Reuse.** The existing `_PLAN_COMPLETION_SURFACES` mapping and source/installed completion mutation tests in `bootstrap/tests/test_review_sweep_ships.py` already check this guidance and install profiles; extend them, not a new checker or test file. Search: `rg 'completion|surface_mutation|profiles' bootstrap/tests/test_review_sweep_ships.py` found those hooks. Doctrine belongs in governing and shipped authoring surfaces; explanatory guidance belongs in the existing methodology guides.

No runtime engine, parser, status, inventory or security-control change; no new form, tracker, enforcement apparatus, mass replanning or dropped outcome. Existing plans remain valid. A coherent helper and its consumers may share a plan; future goals remain proposal/board owned. An unavailable prerequisite keeps a goal queued, not open in an unfinishable plan. Preserve existing authority for deferrals, permissions and scope changes.

## Sequence

Available prerequisites are the current scaffold, existing completion tests and canonical Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`; no unfinished external plan or ceremony is needed. Estimate roughly one to two working days including review and checks, with uncertainty from coordination and test runtime. This is a planning window, not a deadline or waiver.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align guidance and extend existing tests | Plan review folded; coordinate shared files and changelog | Local, shipped and guide wording with source and installed controls |
| C2 | Exercise examples, review and close | C1 and ordinary code review; final wide Boundary B follows review | Recorded applications, passing evidence and archive-ready plan |

## Acceptance criteria

**C1.** Guidance places the specific useful result and relevance in Scope, observable completion in Acceptance criteria, and available capabilities plus a realistic uncertain work window in Sequence. A plan can implement, obtain required checks and reviews, and archive independently; internal chunks can depend on each other. A proposal may authorize several current or future plans: the first opening archives the proposal while queued siblings remain on the board linked to that immutable source; later unchanged authorized work needs no new Decision. No accepted outcome or safeguard is silently lost. Required failed functional, scientific or security checks remain implementation work; routine human operations have separately owned, evidenced board waits, and archive grants no release authority.

Existing source checks cover all nine named guidance surfaces. For each surface, independently removing the independent-completion guidance and separately permitting a human-only final task makes its owning check fail, alongside a passing control. Real scaffold installations across all shipped profiles retain and test the shipped AGENTS, proposal and plan templates. These checks detect specified wording changes; they do not enforce agent semantics.

**C2.** Record four agent applications, not a human trial: a coherent helper-plus-consumer goal, an unavailable helper, a later-release goal, and a missing-check/human-ceremony case. Each shows specificity, observable evidence, feasibility, relevance, estimated window and uncertainty, retained original scope, and whether archive is allowed. The cases distinguish an owned human operation from an unmet required check. Ordinary code review and all applicable checks pass before archive; no human-only final archive chore is introduced.

## Scope delta

Preserved. A proposed reduction or changed authority follows the existing Maintainer disposition; this plan does not concede accepted scope.

## Verification

Boundary A: before implementation use `python tools/test_tiers.py for <changed paths>` and, for governing text, its `--range BASE..HEAD` selection; run the returned affected tests and applicable claim, content/link, snippet and neutrality gates. Map changed surfaces to their readers and installed consumers, and record omissions and non-passes. Extend the named source and installed tests with separate per-surface mutations and passing controls; run the real profile installs. Record the four applications and their outcomes in the implementation record.

Boundary C: an independent ordinary code reviewer reads the committed implementation and iteration evidence, then runs only targeted falsification checks, not a suite. No Security pass is required by the Decision. Resolve findings under the existing review rules.

Boundary B: **wide**, because authoring guidance is a shared documentation contract. After code review, on a clean unchanged final commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13, run the exact mapped iteration list for the reviewed range, mapped integration/workflow tests, owning guidance and install consumers, and standing prose gates. Record the SHA and range, interpreter, clean pre/post state, commands, outcomes and counts, elapsed time, token use or unknown, non-pass dispositions, omissions and timing misses; list test files over ten seconds as required. No full-suite override or tree certification is authorized here. Missing evidence or a failed required check keeps implementation open.
