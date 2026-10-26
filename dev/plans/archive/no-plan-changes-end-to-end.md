# Plan: Trivial changes need no plan and no code review

**Author**: Claude (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md](../../proposals/archive/2026-10-26-claude-no-plan-changes-end-to-end.md)
**Status**: archived
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

## Code review -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

```
Reviewed commit: 89f3957df0303a41767425b7040b74d1c8f1db8e
Target: 63b64784^..89f3957d (C1 63b64784, C2 2a582c5d, C3 6d84b5bd, plan record 89f3957d); other agents' commits in that window were not reviewed
Prior findings: none
```

**Conclusion.** The change does what Revision 3 says for the trivial lane and for
the Boundary B condition on both triage lists, and no test or gate it touches is
red. It does not deliver one accepted outcome: the second test of a "no plan"
claim, at the implementing commit (finding F1, blocking). I also found one stale
sentence the scan could not match (F2) and one rule-text gap for the Maintainer
(F3). The verdict is blocking, so the plan moves to `revising-code`. What I did
not check is in the coverage line.

**Foundations**:

1. **Should this happen as framed?** Mostly yes: every row of Revision 3's edit table was edited, and the three rule sentences read true and agree with each other -- `git diff 63b64784^ 89f3957d -- AGENTS.md templates/core/AGENTS.md doctrine/`; but item 3's "tested again at the implementing commit" is written nowhere (`git grep -n -i -E 'against what it touched|more than one area|tested again' 89f3957d -- doctrine AGENTS.md templates/core` returns only the template's header text, not that rule) -- F1.
2. **Best alternative.** None simpler for the rules: the Boundary B condition is one bullet per list in `doctrine/plans.md:185` and `:193-196`, plus the same clause in the two short summaries (`doctrine/lifecycle.md:215-221`, `doctrine/proposals.md:185-188` and `:322-331`). For F1 the cheapest delivery is one sentence in `doctrine/proposals.md` under "Accepted proposals", not a new mechanism.
3. **What would show it wrong.** A trivial change that ships a defect, or a risky change that skips both the plan and the review -- see the falsification ledger below (2 of 13 distinct breaks killed by tests, one more by the integrity check; the survivors are named) and F1 and F3.

**Bounding**: not owed. The plan's Boundary B record is `full` (`**Boundary B mode**: full`, `**Certified by**: pending`), so there is no bounded claim to rule on. I checked the record anyway: its tested commit is `6d84b5bd`, and `89f3957d` changes only the plan file (`git show --stat 89f3957d`), so the tested bytes equal the reviewed bytes for every file except the plan.

**Waiting-line check.** C4 was the only fenced chunk. `git log -S'Waiting on Maintainer**: re-anchor' -- dev/plans/no-plan-changes-end-to-end.md` shows the Waiting line landing in `89f3957d`, inside the range. No deviation request was made in the range. Not a finding.

### What I checked and how

**1. The edited sentences.** Read in the diff and in the files at `89f3957d`.
* `AGENTS.md:333-341` and `templates/core/AGENTS.md:332-340` carry the same new Boundary B text (diff of the two hunks: identical modulo indent). The old Bounding-verdict sentences are gone from both (`git grep -i bounding 89f3957d` finds only the plan-side rule at `AGENTS.md:354`).
* `doctrine/plans.md`: the open list has five items and the skip list four (`:178-196`); "ANY of the five" and the fast multi-stage sentence name the new condition (`:205-211`); lines 88-91, 130-134 and 690-695 still read true. The Boundary B paragraph (`:366-374`) matches `AGENTS.md`.
* The condition is on both lists in all three places that list conditions: plans (`:185`, `:193`), lifecycle (`:215-221`) and proposals (`:185-188`, `:322-331`). No stale count: `git grep` for "any/all of the three|four|five" and "three skip" finds only `plans.md:205` ("five").
* The "no plan" header form is in both proposal templates, after the pinned prefix, and in `doctrine/proposals.md:204-209`.
* The easy-problem sentence is in both `AGENTS.md` copies (`:243`, `:248`).
* I found no sentence that contradicts another one, except F3 below.

**2. The scan, from scratch** (my own paragraph scan, `scan.py` in my scratch folder, over every tracked file at the named commit, excluding `dev/proposals/`, `dev/plans/`, `dev/reviews/`, `dev/strategy/`, the changelog and `bootstrap/tests/`).
* *Positive control.* At `63b64784^`, pattern "typo|one-line|trivial" with "code review|a review|Bounding verdict" found 50 paragraphs, including `doctrine/lifecycle.md:47` (the paragraph holding the old line 61), `docs/glossary.md:17`, and both example READMEs. So the scan can see the known cases.
* *HEAD.* The same pattern at `89f3957d` finds 52 paragraphs. The implementer reports 48 and 50; my scan also counts the shipped twins and a few other files, so the totals differ by two. I read all 52. Each is either edited and now says "no code review" (lifecycle 47 and 215, proposals 185 and 322, plans 366, both `AGENTS.md`, README 48 and 100, the three alt texts, both dev tours, glossary, quickstart, vision, workflow-role, release-process, solo-legacy, dimensions, both example READMEs, the figure), or stands because the review it names belongs to another lane or stage (proposal review, plan review, standard or deliberate lane, the roster tables, `dev/agent_collaboration.md:132`, `dev/measurement/tag-pass-dispositions.md:445`, `docs/agent-team-onboarding.md:69`). None is a trivial-lane review that was left in.
* *A second pattern.* "trivial|typo|just commit|one-line|obvious correction" with "reviewer|reviewed|fresh reviewer|independent review|reviewed range" gave 33 paragraphs; all stand except the dual-review one (item 7). A third pattern ("every change|small change|small fix|light path" with a review phrase) found the one the first two missed: `docs/related-practices.md:122-123`, "Small changes skip this and get a code review" (F2).

**3. Every member of the set.** Every file in Revision 3's edit table was touched by the three commits: `AGENTS.md`, `templates/core/AGENTS.md`, `doctrine/{plans,lifecycle,proposals}.md`, both proposal templates, `docs/{dev-tour,glossary,quickstart,vision,workflow-role,related-practices,release-process,solo-legacy-recipe}.md`, `dev/modules/onboarding/dev-tour.md`, `dimensions/README.md`, both example READMEs, `README.md`, `docs/getting-started.md`, `docs/index.html`, the figure. Skipped: none. Not yet done: the changelog row, which the plan puts in the archive commit (C4 text), so it is not a skip. Edited but not in the table: the short summaries in `doctrine/lifecycle.md:213-221` (the table lists line 61 only, and the Revision's "Not edited" note names 212-219) and `doctrine/proposals.md:185-188` and `:322-331`. I judge these in scope: they list the same conditions and would otherwise be the stale list the task warns about.

**4. The figure and the alt texts.** The figure's header comment (`:6-7`), `desc` (`:31`) and trivial lane say "the change with its test, and no code review". The three alt texts are the same string and say "needs no review" (`README.md:48`, `docs/getting-started.md:28`, `docs/index.html:168`); they open with the conclusion, as `docs/DOCUMENTATION_PLAN.md` asks. The figure has no script, image or link, keeps its `viewBox` (`0 0 700 390`), and the new `.note` text uses an existing class. I rendered the SVG alone in the built-in browser at 1200 px and 375 px: it fits both, nothing clips, and the trivial lane shows "change + test" and the italic note. The pane renders local files in light theme only, so I did not see dark theme, and I did not see the figure inside `README.md` or `index.html` (not checked). The C3 commit body gives the legibility result as `docs/DOCUMENTATION_PLAN.md` requires, and its overstated "none" is corrected in this plan's record: at `89f3957d`, `git grep 'then a code review'` outside the records finds one line, the figure's `desc` (standard and deliberate lanes), which is what the plan record says.

**5. Lockfile and integrity.** `dev/.cairn/cairn-lock.yml` lists `AGENTS.md` at `sha256:8becb436...ee78a6`; `git show 89f3957d:AGENTS.md | shasum -a 256` gives the same, and so does the working-tree file now. `AGENTS.md` was last changed by `63b64784` (`git log -- AGENTS.md`), so no other agent committed an edit to it in the window; the momentary different `shasum` the implementer saw was an uncommitted working-tree state that is in no commit, and it does not affect the committed bytes. I recomputed every lock hash against the blobs at `63b64784^` and at `89f3957d`: 27 files do not match at either commit, the same 27 (none new, none fixed; `dev/proposals/_template.md` is among them before and after). `bootstrap/verify_integrity.py` on a clean worktree of `89f3957d` does not list `AGENTS.md`.

**6. Tests.** In a clean detached worktree of `89f3957d`, Python 3.13.13: the six named test files plus `test_writing_rules_ship.py` and `test_review_sweep_ships.py` gave 881 passed in 2.5 s; 22 files that read edited files (the list is in the ledger) gave 1278 passed in about 42 s. The pinned sentences still exist where the tests look: the nine Boundary B patterns in `test_review_and_verification_rules_ship.py:100-125` match `AGENTS.md`/`templates/core/AGENTS.md`; `test_review_stance_in_shipped_files.py:709-718` still sees the pinned start of the `Plan review` line (mutant M3 below proves it still looks). The implementer's two failures: `test_oracle_privileged_workflows_preserved` passes alone on the clean `89f3957d` worktree (1 passed); it compares a baseline engine with the current one and reads no file these commits touched (`bootstrap/tests/test_oracle.py:162-171`), so the shared-checkout failure fits the uncommitted engine edits the implementer names. `test_a_t4_output_is_bounded` passes alone on the same worktree (1 passed); it floods a child process and reads no repository file (`test_security_stack.py:1117-1133`). I did not re-observe the original failures, so the cause is the implementer's account plus these two reads.

**7. C4 (the sentence at `doctrine/dual-review.md:344-346`, at `89f3957d`).** It read: "For work with a valid Boundary B record (`doctrine/plans.md`: a plan's Implementation verification section, a trivial change's commit body, or the commit body of an accepted proposal implemented in one commit with no plan, whose tested revision is that commit and whose clean state is a tree clean apart from the change), the reviewer first checks...". It contradicted the rule in one way: it names two records a reviewer checks first, and under the rule neither a trivial change nor a no-plan implementation has a reviewer. The edit that fits is to keep only "a plan's Implementation verification section" and drop the two commit-body items and the clause "whose tested revision is that commit and whose clean state is a tree clean apart from the change", which describes only those two. The pinned statement `boundary-c-names-the-no-plan-accepted-proposal` (`test_review_stance_in_shipped_files.py:1123-1126`) moves with it. Note: commit `cdffeb8a` (Maintainer, after the reviewed range) has since edited this sentence and the test, keeping the trivial change's commit body "where the Maintainer asks for a review". I did not review that commit.

**9. The C3 commit-body claim.** Checked in item 4: the plan record corrects it.

### Falsification ledger

Control and mutants ran in one throwaway detached worktree of `89f3957d` (reset between mutants, removed afterwards), Python 3.13.13, over the same 22 test files. Control: 1278 passed.

| # | Mutant (one deliberate break) | Result |
|---|---|---|
| M1 | `templates/core/AGENTS.md`: put back the old "Boundary C's Bounding verdict reviews it afterwards" and the code reviewer's Bounding verdict closing sentence | **Survived** (1278 passed) |
| M2 | `doctrine/plans.md`: delete the "Boundary B would run `bounded`" skip bullet | **Survived** |
| M3 | `templates/core/dev/proposals/_template.md`: alter the start of the `Plan review` line | **Killed**: `test_review_stance_in_shipped_files.py::test_proposal_header_offers_only_usual_values[shipped-proposal]` |
| M3b | The same break in `dev/proposals/_template.md` | **Killed**: the `[own-proposal]` case of the same test |
| M4 | `doctrine/plans.md`: put "ANY of the four" back | **Survived** |
| M5 | `AGENTS.md`: delete the easy-problem sentence | **Survived the tests**; **killed by** `verify_integrity.py` (`modified (hash mismatch): AGENTS.md`), a gate, not a test |
| M5b | `templates/core/AGENTS.md`: delete the same sentence | **Survived** (nothing compares the two copies) |
| M6 | `doctrine/lifecycle.md`: put "code + test + one code review" back in lane 2 | **Survived** |
| M7 | `docs/dev-tour.md` only: change the trivial lane text | **Killed**: `test_an_installed_onboarding_copy_equals_its_page[docs/dev-tour.md-...]` |
| M8 | The figure: put "and a code review" back in the `header` | **Survived** |
| M9 | `doctrine/plans.md`: delete "Needs Boundary B in `full` mode" from the open list | **Survived** |
| M10 | `doctrine/proposals.md`: replace "a 'no plan' claim without each condition shown is a review finding" with "is fine" | **Survived** |
| M11 | `docs/quickstart.md`: "with no code review" to "with one code review" | **Survived** |
| M12 | `doctrine/lifecycle.md`: delete the Boundary B condition from the trivial definition | **Survived** |

Tally of 14 rows (13 distinct breaks; M3 and M3b are one break in two files): killed by a test 3 (M3, M3b, M7), killed by a gate only 1 (M5), survived 10, equivalent 0 (no equivalence was measured, so none is claimed). The survivors are the new prose the plan's own record says no test pins ("The change is prose", Known omissions); the plan does not promise a pin, so I do not count them as defects. They do mean a future edit can silently remove the new triage bullet, the new Boundary B sentences or the easy-problem sentence. Recommendation, not a finding: one node that pins the triage bullet, the shipped Boundary B sentence and the "no code review" lane text would kill M1, M2, M6, M9, M12.

### Findings

**F1 -- blocking -- accepted outcome not delivered: the "no plan" claim is tested at proposal review but not again at the implementing commit.**
Revision 3, "What changes" item 3, third bullet: "Tested again at the implementing commit, which re-reads the skip conditions against what it touched. If it touched more than one area, a plan opens then, and the plan-open commit archives the proposal as today." The Decision says "Revision 3 is the contract", and the item's own reason is that the proposal-stage test alone missed two changes of two on 2026-10-26. The shipped text has the first half only: `doctrine/proposals.md:204-209` makes an unjustified "no plan" claim a review finding. Nothing tells the implementing agent to re-read the conditions. `AGENTS.md:340-341` and `doctrine/plans.md:373-374` say a full-mode change "opens a plan", and the triage lists say when to open one, which covers a change that is obviously risky, but not the act of re-reading, and not the "touched more than one area" case. The edit table's row for `doctrine/proposals.md` says only "the 'no plan' clause", which is why the plan's scope check did not catch it. Accepted scope is a floor (`AGENTS.md`, Git and commit workflow), so this is a deviation to be delivered or conceded by the Maintainer, not narrowed by me.
*Satisfier:* one sentence in `doctrine/proposals.md`, under "Accepted proposals" (the first bullet, `:322-326`): the implementing commit re-reads each plan-skip condition against what it touched; if it touched more than one area or its Boundary B would run `full`, a plan opens then, and the plan-open commit archives the proposal. Plus the same clause, in short, in `doctrine/plans.md` after the skip list. Or a recorded Maintainer concession that the Boundary B sentence is enough.

**F2 -- non-blocking -- one stale sentence the scan could not match.** `docs/related-practices.md:122-124`: "For substantial changes, review happens before the code exists... Small changes skip this and get a code review." Small changes are the trivial lane, which now has no code review. The scan words are absent from that paragraph, so the plan's scan and mine (patterns 1 and 2) miss it; the third pattern found it. The same file's line 40 was edited in C2, so the file was open. *Satisfier:* change to "Small changes skip this and need no review," or delete the clause; one line, descriptive layer, no rule text.

**F3 -- non-blocking, for the Maintainer -- the trivial lane's defect-repair carve-out and the Boundary B condition do not meet.** `doctrine/lifecycle.md:51-59` lets a defect repair take the trivial lane "even on a named surface" (a high-risk surface), and lane 2 now says "code + test, no proposal and no code review" (`:59-61`). `AGENTS.md:340-341` says a change whose Boundary B would run `full` "is not trivial: it opens a plan", and bounded mode refuses on a high-risk or contract surface (`AGENTS.md:322-330`). So a defect repair on a named surface is lane 2 by one text and "opens a plan" by the other; the plan triage lists apply to "an accepted proposal's implementation" (`doctrine/plans.md:177`) and lane 2 has none. Before this change such a repair got one code review; now an agent that reads only lane 2 gets none. I read the `AGENTS.md` sentence as the binding one, so I do not call the loophole open, but the lifecycle text does not say which artifact "opens a plan" means for a change with no proposal. *Satisfier (rule text, so the Maintainer's word):* one clause in lane 2, for example "a defect repair whose Boundary B would run `full` is not trivial: it takes the standard lane."

**Notes, not findings.**
* `bootstrap/tests/test_review_and_verification_rules_ship.py:24-27` (frozen) still says in its docstring that a trivial change's commit body is what "the code reviewer's Bounding verdict reviews". The patterns it pins still match, so it passes; the docstring describes the old rule and moves with the Maintainer's re-anchor.
* The new easy-problem sentence says a change with no code review "carries" no easy-problem fix. A trivial-lane defect repair is its own change, not a fix carried inside another one, so I read it as not forbidding that; the sentence could say "carries no easy-problem fix inside it".
* A trivial change with a known cheap defect next to it can neither fix it (no review) nor cite a plan's deferral reasons (no plan). The existing `AGENTS.md` deferral sentence does not say what such a change does. I did not weigh this further.

### Verdict

**Blocking.** F1 must be delivered, or conceded by the Maintainer, before this plan archives. F2 should ride the same revision. F3 is the Maintainer's call. Status set to `revising-code`. A second code-review pass runs only if the revision introduces new defects. Certification is unchanged: `**Certified by**: pending`, and the certifying run is the Maintainer's before the push; I did not run the full suite and did not set `CAIRN_FULL_SUITE`.

**Coverage -- Covered:** the rule, doctrine and template sentences in the diff; the scan at two commits with a positive control and three patterns; every file in the edit table against the commits; the figure's source and its render at 375 and 1200 px in light theme; the three alt texts; the lock hash against the blob at `89f3957d`, and all 27 lock mismatches at base and head; 1278 tests over 22 files plus 881 over 8 files; the two named failures; 13 distinct breaks beside a control. **Not covered:** dark theme, and the figure inside `README.md`/`index.html` (the pane cannot show them); the full suite and the other roughly 26 test files the implementer ran (not mine to run); `docs/DOCUMENTATION_PLAN.md`'s other asset rules beyond the ones quoted; `bootstrap/tests/test_upgrade.py` and the gate-manifest and AST re-anchor state; the engine, `CHANGELOG.md` and `PLANNING.md` commits by other agents in the window; commit `cdffeb8a`; whether adopters' installed copies of the two `AGENTS.md` sentences merge cleanly on upgrade. The scan finds words, not meaning: a trivial-lane review implied without a scan word and not in my three patterns would not be found (F2 was found that way, so others may exist).

## Code review response -- Claude Sonnet 5.5 (implementer) -- 2026-10-26

**Conclusion.** F1, F2 and F3 are accepted and delivered in `cb93f1d9`. The
wording note is accepted too. C4 is done. The plan is `ready-to-archive`.

* **F1 -- accept (followup commit `cb93f1d9`).** `doctrine/proposals.md`, under
  "Accepted proposals", now says the implementing commit re-reads each plan-skip
  condition against what it touched; more than one area, or a Boundary B that
  would run `full`, opens a plan then, and the plan-open commit archives the
  proposal. `doctrine/plans.md` says the same in short, after the skip list.
* **F2 -- accept (followup commit `cb93f1d9`).** `docs/related-practices.md`
  now says small changes skip review and need no review.
* **Easy-problem wording -- accept (followup commit `cb93f1d9`).** `AGENTS.md`
  and `templates/core/AGENTS.md` now say a change with no code review "carries no
  easy-problem fix inside it". No other claim was held on `AGENTS.md` (checked
  with `tools/intent.py list`), and the `AGENTS.md` hash was advanced again with
  `--finalize AGENTS.md` after I read the whole diff. `verify_integrity` still
  shows 23 violations and `AGENTS.md` is not among them. The planning session's
  sentence from `8b86051d` is untouched.
* **F3 -- accept (followup commit `cb93f1d9`).** The Maintainer answered the
  recommendation (the lifecycle wins) in these words, relayed by the coordinator:

  > "I accept your recommendation"

  That is the authorization for this rule text. A defect repair that meets the
  lifecycle's three conditions (a failing-test reproduction; it restores
  documented or intended behaviour with no contract change; the touched
  surface's own test family runs in the loop) stays trivial even on a named
  surface. The clause is in the Boundary B paragraph of `AGENTS.md`,
  `templates/core/AGENTS.md` and `doctrine/plans.md`, on the skip and open
  bullets of the plan triage (a clause, not a sixth item; the counts are
  unchanged), and in the short summaries in `doctrine/lifecycle.md` and
  `doctrine/proposals.md`. The proposal's Revision 3 is read with this one
  clause added. No Waiting line is owed for F3.
* **C4 -- done.** The Maintainer edited the sentence at
  `doctrine/dual-review.md:344-346` and its pinned test in `cdffeb8a`, so my
  earlier Waiting line was removed. The gate-manifest re-anchor for that edit is
  still owed to the Maintainer. It is not a Waiting line on this plan, because
  the plan archives without it.
* **Note: the frozen test's docstring** (`test_review_and_verification_rules_ship.py`,
  lines 24-27) still describes the old rule. It moves with the re-anchor. I did
  not edit it.
* **Note: a trivial change with a known cheap defect** has no stated route (no
  review for a fix, no plan for a deferral reason). I did not act on it.

**Verification.** Python 3.13.13, scoped: the 48 test files that read the edited
files, in two batches, gave 1569 and 782 passed, 0 failed. `claim_check` is
clean on the six edited Markdown files; `check_cairn`, `sync_doc_snippets`,
neutrality (0 fail) and redundancy (0 fail) are clean; `link_check` shows the
same 3 old issues. Not run: the full suite (`Certified by`: pending) and a second
code-review pass. The review's survivors (10 of 13 breaks that no test
notices) are prose the plan did not promise to pin, and I added no test.

## Archive note -- Claude (Strategy) -- 2026-10-26

The independent code review at `0a3bd5f1` found one blocking gap (the second
test of a "no plan" claim, at the implementing commit) and two smaller ones. The
fixes are in `cb93f1d9`, with the answers in the response above, and under the
one-round rule they need no second pass: each is one sentence or one exception
clause. This archive commit is distinct from the implementing and review
commits. The rule is live in `AGENTS.md`, `doctrine/lifecycle.md`,
`doctrine/plans.md`, `doctrine/proposals.md` and both proposal templates, and the
reader-facing pages repeat it.

**Dispositions:**
- `accept`: the whole of Revision 3's edit list, C1 to C3 (`63b64784`,
  `2a582c5d`, `6d84b5bd`), and C4 (`cdffeb8a`: the Boundary C sentence in
  `doctrine/dual-review.md` and the statement in the frozen
  `test_review_stance_in_shipped_files.py` that pins it).
- `accept`: F1 (the implementing commit re-reads the plan-skip conditions), F2
  (`docs/related-practices.md`), F3 (a defect repair meeting the lifecycle's
  three conditions stays trivial on a named surface), all in `cb93f1d9`. F3 rests
  on the Maintainer's quoted word in the response above.
- `defer`: the certifying full run, and the gate-manifest re-anchor for the
  edited frozen test, go to the Maintainer's existing ceremony row in
  `dev/PLANNING.md`. The plan records no Waiting line.
- `wontfix`: none.

**Not done, named.** The reviewer recommended one small test that pins the new
triage bullet, the shipped Boundary B sentence and the lane text: ten of its
thirteen deliberate breaks survived every test. That test was never in the
accepted scope, so it is offered to the Maintainer and not built.

**Pinned test collection changes:** none added. One pinned statement changed
text in a frozen file; its label is unchanged.
