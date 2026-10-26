# Plan: Trivial changes need no plan and no code review

**Author**: Claude (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md](../proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md)
**Status**: awaiting-code-review
**Waiting on Maintainer**: re-anchor gate manifest: dual-review.md:344-346
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

## Implementation verification -- Claude (Implementation, Sonnet) -- 2026-10-26

**Conclusion.** C1 to C3 are committed and C4 is waiting on the Maintainer. Every
rule and page in the edit list now says a trivial change has no code review.
The scoped tests pass (2350 passed, 0 failed in the last run, after one
load-related failure that passes when re-run). I did not run the full suite and
did not render the figure in dark theme.

**Boundary B mode**: full, as the plan declared. The run below is scoped, because
`CAIRN_FULL_SUITE=1` is not set for this plan.
**Certified by**: pending. The certifying run is the Maintainer's, before the push.
**Tested commit**: `6d84b5bd9514e4dc75691f1a3a75267bf744f1c0`, the last implementation commit.
**Reviewed range**: three commits of mine, `63b64784` (C1), `2a582c5d` (C2) and
`6d84b5bd` (C3). The range `73bdafed..6d84b5bd` also holds other agents'
commits (engine and `PLANNING.md`), which are not part of this review.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
**Pre-run state**: a detached worktree of `6d84b5bd`, `git status --short` empty.
**Post-run state**: the same worktree, still empty, `HEAD` unchanged. The shared
checkout was not clean (other agents' uncommitted engine edits), so I measured in
the worktree and removed it afterwards.

| Command (from the worktree root) | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `pytest -q` on 35 test files (first batch of 48; the guard allows 40) | 0 | 1569 passed | 57 s |
| `pytest -q` on the other 13 test files | 1 | 781 passed, 1 failed (`test_security_stack.py::test_a_t4_output_is_bounded`) | 84 s |
| `pytest -q` `test_security_stack.py` alone, re-run | 0 | 131 passed | 20 s |
| `quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality 0 fail (41 info), redundancy 0 fail | a few seconds |
| `link_check.py` | 1 | 3 issues, all `docs/DOCUMENTATION_PLAN.md` in `documentation-plan.md`; the same 3 on `HEAD` at the start | seconds |
| `check_cairn.py` in the shared checkout | 0 | no issues | seconds |
| `sync_doc_snippets.py --check` | 0 | no drift (367 docs) | seconds |
| `claim_check.py`, one call per edited Markdown file | 0 | no flags | seconds |
| `verify_integrity.py --target .` | 1 | 23 violations, the same list as the baseline taken from `HEAD` (`635293aa`) before C1; `AGENTS.md` is not in either | seconds |

The 48 test files are the tests that read a changed file (found by
`git grep` for the changed paths and names in `bootstrap/tests`), plus the seven
the plan names. The 2350 passed is the sum of the two batches, 1569 plus 781.

**Non-pass disposition.**
* `test_a_t4_output_is_bounded` failed once under load (other agents were running
  tests). The test's own comment says a loaded machine can fail it. It passed
  alone, and the whole file passed 131 of 131. I treat it as a flake, not as
  something this change touched: no engine file is in my commits.
* `test_oracle.py::test_oracle_privileged_workflows_preserved` failed in the
  shared checkout during C1 (profile.yml bytes differ, 622 against 596). The
  cause is other agents' uncommitted edits to `bootstrap/_scaffold/upgrade.py`.
  It passed 18 of 18 on a clean `HEAD` worktree and passes in the tested-commit
  worktree above.
* `check_cairn.py` in the worktree reports 3 `__pycache__` paths cited in other
  agents' records. Those folders exist only in the shared checkout. It is clean
  there.
* `link_check.py`'s 3 issues are older than this plan.

**Plan-specific acceptance, by criterion.**
* *C1, the scan.* Before any edit, a paragraph-level scan (a script in my scratch
  folder, not in the repo) found `doctrine/lifecycle.md:61` (in the paragraph at
  line 47) and `docs/glossary.md:18` (in the paragraph at line 17), so it could
  find the known cases. It reported 48 paragraphs before and reports 50 after. The
  count rose because the scan looks for words, and my new sentences say "no code
  review". Every one of the 50 is edited or stands for one of these reasons:
  * *Edited, now says "no code review":* `lifecycle.md:47` and `:215`,
    `proposals.md:185` and `:322`, `plans.md:366`, `AGENTS.md:333`,
    `templates/core/AGENTS.md:332`, `README.md:100`, `docs/index.html:161` and
    `:187`, both dev tours, `glossary.md`, `quickstart.md:14` and `:501`,
    `vision.md`, `release-process.md`, `solo-legacy-recipe.md`,
    `dimensions/README.md`, both example READMEs, and the figure's header
    comment, `desc` and Provenance line.
  * *Stands, because it names the standard or deliberate lane's review:* the rest
    of each paragraph above, and the alt text in `README.md:48`,
    `getting-started.md:28` and `index.html:168`.
  * *Stands, because the word is about something else:* "typo guard" and
    "mechanical maintenance, not authoring a review" (`plans.md:66`, `:589`,
    `proposals.md:112`, `:291`), proposal review and the archive step
    (`proposals.md:34`, `:72`, `lifecycle.md:158`, `AGENTS.md:31`, `:287`), the
    roster and tier tables (`roles.md:167`, `model-selection.md`, both copies),
    `agent_collaboration.md:132` (already says a trivial change owes no review),
    `BOOTSTRAP.md:589`, `audit_report.py:11`, `quickstart.md:306`, `plans.md:130`
    ("Trivial accepts skip the plan entirely": still true).
  * `dev/modules/onboarding/dev-tour.md` and `docs/dev-tour.md` are
    byte-identical (`diff -q` silent).
* *C1, the triage rule.* `grep -n "would run .bounded" doctrine/plans.md` finds one hit,
  in the skip list. The open list gains "Needs Boundary B in `full` mode", so it
  has five items and the skip list has four. "ANY of the four" now reads "ANY of
  the five", and the "fast multi-stage" sentence names the new condition.
  `plans.md` lines 88-91, 131-134 and 690-691 still read true and are unedited.
  I also added the condition to the short trivial / non-trivial summaries in
  `lifecycle.md` and `proposals.md`, which list the same conditions.
* *C1, the template.* Both proposal templates keep the start of the `Plan review`
  line that `test_review_stance_in_shipped_files.py` pins; the new
  `not required(no plan: ...)` text is appended. My first wording cited
  `doctrine/plans.md` by path, which `check_cairn` flags in a shipped template,
  so the text says "the plan triage rule" instead.
* *C1, integrity.* I took the baseline from a detached worktree of `HEAD`
  (`635293aa`): 23 violations, `AGENTS.md` not among them. I read the whole
  `AGENTS.md` diff (19 changed lines, all mine), then ran
  `scaffold.py upgrade --target . --finalize AGENTS.md`; the lockfile moved one
  hash (committed in `63b64784`). After: 23 violations, the identical list. I did
  not finalize the `dev/` templates. One oddity: a `shasum` of `AGENTS.md`
  returned a different value for a moment while other agents' tests were running,
  then returned to the finalized hash; I do not know why, and the final verify is
  clean.
* *C2.* The scan finds no stale hit in these files (see above). The two quickstart
  strings the frozen test reads are present (2 grep hits).
* *C3.* The figure's header comment, `desc`, and the trivial-lane chip, and the alt
  text in the three pages, say the trivial lane is the change with its test.
  `grep "then a code review"` finds the standard and deliberate lanes in the
  figure's `desc` and nothing near "trivial". My C3 commit body says the grep
  finds "none"; that overstated it, and this line corrects it.
* *C3, legibility pass, what I did.* I rendered the SVG alone in the built-in
  browser at 1200 px and at 375 px (light theme) and looked at both screenshots.
  It fits both widths with no clipping. At 375 px the chip text is small, about
  7 px on screen (13 px at a 0.54 scale), the same as before the change.
  The alt text is present on all three embeds and opens with the conclusion.
* *C3, what I did not do.* I did not see the dark theme: the pane renders local
  files in light only. The new note reuses the existing `.note` class, which
  follows the ink colour, and I changed no colour rule. I did not see the figure
  inside `index.html` or the README: the pane loads a local page as a static
  snapshot and the relative image did not load. The figure's `viewBox` is
  unchanged, so I expect the layout around it to be unchanged, but I did not
  measure it.
* *C4.* **Waiting.** `doctrine/dual-review.md:344-346` lists "a trivial change's
  commit body, or the commit body of an accepted proposal implemented in one
  commit with no plan" as records the code reviewer checks first. Under the new
  rule neither has a code review, so the sentence no longer matches the rule. I
  did not edit it. `test_review_stance_in_shipped_files.py`
  (`boundary-c-names-the-no-plan-accepted-proposal`, about lines 1123-1126) pins
  that text, so the sentence, that test and the gate manifest move together in the
  Maintainer's re-anchor. A replacement for the Maintainer to consider: keep the
  list at "a plan's Implementation verification section" and drop the two commit
  bodies. The changelog entry is the plan-archive commit's, not mine.

**Known omissions.**
* The full suite was not run, so the change is uncertified. `Certified by:
  pending`.
* I ran no mutation sweep. The change is prose; the one rule test it could affect
  (`test_review_and_verification_rules_ship.py`) passed.
* The scan finds words, not meaning. I read every hit; a sentence that implies a
  trivial-lane review without any of the scan's words would not be found.
* I did not run Boundary C or review my own work; that is the fresh reviewer's.

## Dispositions

*Filled at archive-preparation.*
