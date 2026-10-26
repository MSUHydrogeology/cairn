# Plan: Trivial changes need no plan and no code review

**Author**: Claude (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md](../proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md)
**Status**: ready-to-implement
**Plan review**: not required(prose edits to one rule and the docs that repeat it; the proposal's two reviews checked the edit list; this plan opens in the fast multi-stage form)
**Opened**: 2026-10-26
**In brief**: Edit the rules and the pages that repeat them so a trivial change owes no code review, and a change that cannot bound its effects opens a plan.

## Source proposal

The Decision (2026-10-26) accepts Revision 3 of the source proposal. A trivial
change owes no code review. "Trivial" covers the typo lane and a no-plan
implementation. A change fails the plan-skip test when its Boundary B would run
full, so it opens a plan. A "no plan" claim is shown in the proposal header and
re-read at the implementing commit. This plan edits the files the proposal's
table lists.

## Scope

**In.** Every row of the proposal's Revision 3 edit list, in four chunks (below).
**Out.** The archived example proposals, `bootstrap/tests/test_quickstart_sequence.py`
(frozen), `doctrine/lifecycle-contract.md`, and `dev/agent_collaboration.md:133`,
which already say what the new rule says.

**Reuse.** `N/A: no code added`. Search for sites to edit: a paragraph-level scan
over the tracked tree (method in C1's criteria), because a line search missed
wrapped sentences in the proposal's own review.

### Documentation / doctrine surface

Governing layer (`AGENTS.md` and its shipped twin), doctrine (`doctrine/plans.md`,
`lifecycle.md`, `proposals.md`), the shipped proposal template, and the
descriptive layer (`docs/`, `README.md`, `dimensions/README.md`, the example
READMEs and one figure).

## Sequence

How to work: directly on `0.5-dev` in the shared checkout, no branch, no
worktree for writing. Run `python tools/intent.py claim --files <paths> --action
"<what>"` before editing, and commit by explicit path.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Rules: `AGENTS.md` and `templates/core/AGENTS.md` (Boundary B paragraph; the easy-defect sentence), `doctrine/plans.md` (the same Boundary B paragraph; the fourth skip condition in the triage rule; recheck 88-91, 131-134, 690-691), `doctrine/lifecycle.md:61`, `doctrine/proposals.md:191-203`, and the `Plan review` clause in both proposal templates | none | one commit |
| C2 | Docs and examples: `docs/dev-tour.md` and `dev/modules/onboarding/dev-tour.md` (kept identical), `docs/glossary.md`, `docs/quickstart.md`, `docs/vision.md`, `docs/workflow-role.md`, `docs/related-practices.md`, `docs/release-process.md`, `docs/solo-legacy-recipe.md`, `dimensions/README.md`, both example READMEs | C1 landed | one commit |
| C3 | Front pages and figure: `README.md`, `docs/getting-started.md`, `docs/index.html`, `docs/assets/three-lanes-of-change.svg` (header comment, `desc`, the "code review" chip), re-rendered | C2 landed | one commit |
| C4 | `doctrine/dual-review.md:344-346`: decide whether it still reads true. A frozen test pins it. Then the changelog entry | **MAINTAINER-GATED**: editing the pinned sentence needs the gate-manifest re-anchor, which is the Maintainer's. If it still reads true, nothing is edited and the chunk is only the changelog entry | one commit, or a Waiting line |

## Acceptance criteria

* **C1.**
  * *The scan, with controls.* A paragraph-level scan over every tracked file
    outside `dev/proposals/`, `dev/plans/`, `dev/reviews/`, `dev/strategy/`, the
    changelog and the tests: "typo", "one-line" or "trivial" in a paragraph that
    also says "code review", "a review" or "Bounding verdict". Before any edit it
    must find `doctrine/lifecycle.md:61` and `docs/glossary.md:18`. After C1 to
    C3 every remaining hit is listed with the reason it stands.
  * `doctrine/plans.md` triage lists four skip conditions, the fourth being that
    Boundary B would run bounded; a grep for "would run bounded" finds one hit
    there.
  * The proposal template's `Plan review` line still starts with the text
    `bootstrap/tests/test_review_stance_in_shipped_files.py:709-711` pins.
  * `AGENTS.md` and `templates/core/AGENTS.md` say the same, and
    `python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md`
    leaves the integrity report with no new mismatch (baseline taken from a
    detached worktree of `HEAD`).
* **C2.** The scan finds no hit in these files. `diff -q docs/dev-tour.md
  dev/modules/onboarding/dev-tour.md` is silent. The quickstart still carries the
  strings the frozen test reads ("**6** modules listed", "**22 unfilled block
  slots**").
* **C3.** The figure's header comment, `desc` and chip, and the alt text in
  `README.md`, `docs/getting-started.md` and `docs/index.html`, all say the
  trivial lane is the change with its test. A grep for the old phrase ("then a
  code review" near "trivial") finds none. The figure is rendered at 375 and
  1200 px, and the legibility pass is recorded as the house rules require.
* **C4.** Either `dual-review.md:344-346` is unchanged with a line saying why it
  still reads true, or a Waiting line names the re-anchor. The changelog entry
  exists.

## Scope delta

**Scope delta**: preserved. The baseline is the proposal's Revision 3 edit list,
as accepted.

## Verification

**Boundary A.** Run the tests that own each touched surface:
`test_review_stance_in_shipped_files.py`, `test_verification_boundaries.py`,
`test_review_and_verification_rules_ship.py`, `test_certifying_run_rule.py`,
`test_scope_reduction_trap.py`, `test_stewardship_rules_ship.py`,
`test_writing_rules_ship.py`, plus every test that reads a changed file, found by
search. The gates: `claim_check`, `link_check`, `check_cairn`, the neutrality and
redundancy gates, `sync_doc_snippets --check`.

**Boundary B.** After the last commit, on a clean tree under Python 3.13. Edits
to `AGENTS.md` and a shipped template are contract-adjacent and effects are not
easily bounded, so the mode is `full` with `**Certified by**: pending`; the
certifying run is the Maintainer's, before the push. The full suite is never run
for this plan.

**Boundary C.** A fresh reviewer verifies the record and runs targeted checks:
the scan again, with a control; the figure render; whether the new triage
condition contradicts any sentence left behind. This plan archives only after
that review.

## Dispositions

*Filled at archive-preparation.*
