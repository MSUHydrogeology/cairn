# Plan: Model-tier rules, with same-maker checks and medium proposal authoring

**Author**: Claude Sonnet 5.5 (Strategy, plan author)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-model-tier-rules.md](../proposals/archive/2026-10-26-claude-model-tier-rules.md)
**Status**: awaiting-code-review
**Plan review**: required(Internal)
**Opened**: 2026-10-26
**In brief**: Every Cairn project gets a short rule to use the cheapest model that is safe and to name it when starting a helper agent; a stronger model from the same maker may now check cheaper work; and proposals are written at the medium tier by default.

## Source proposal

The Decision (2026-10-26) accepts the proposal as revised: five rules (R1 to R5), no new tool, field or
gate. Answers **1 and 2 differ from the Revision's defaults, so this plan changes the Revision's text**
and follows the Decision: (1) "Let a stronger model from the same maker count"; (2) "Yes, lower it to
medium now". Answers 3 and 4 match the defaults. The rate-limit gate is not engaged: the Maintainer's
direction started this change (Answer 3).

## Scope

**In.** R1 (the lane sets the tier to write at; Security Review and bright-line work stay high; no floor
on a named high-risk surface moves). R2 (a "Model tier" block under Roles in `AGENTS.md` and
`templates/core/AGENTS.md`). R3 (one `CLAUDE.md` bullet). R4 (the escalation sentence in
`doctrine/roles.md`). R5 (one `dev/PLANNING.md` deferred-table row). The module and `roles.md` cleanups
(dangling "Worked example" mentions; "Notes on the gating" shrunk). The text pin. Doctrine surface: the
governing layer (`AGENTS.md` copies, `roles.md`), the module twins, `CLAUDE.md`, `dev/PLANNING.md`. And
the two Decision changes:

* **Answer 1.** Remove the different-maker condition: six places in three files
  (`doctrine/roles.md` twice; the shipped module and its `dev/modules/` twin twice each; the
  Decision says five) and three patterns in the frozen test. New rule: a stronger model from
  the same maker counts as the check when it is at a tier strictly above the cheaper author;
  a model at the same tier does not. The other conditions, the exclusion list and "the check
  is not a review" stay.
* **Answer 2.** Proposal authoring is medium. Strategy / Research (research,
  premise-checking, novel design), proposal review and Security Review stay high; a
  premise-check inside a proposal is its own task, spawned at high. R1, R2 and the floor
  tables change to match. R5 changes too: medium is now the floor for proposals, so it
  compares proposals written at medium with those written at high, not "below high".

**Out.** The rate-limit gate, `templates/core/VENDOR.md`, `check_model_selection.py`,
`doctrine/rationale.md` (its one hit is "distance on request", which stays). The sentence that a context
packet sent to a second maker crosses the data-governance gate stays: it is still true and pinned.

**Reuse.** Searched `bootstrap/tests/` for tests pinning non-Review `AGENTS.md` text:
`test_stewardship_rules_ship.py` and `test_writing_rules_ship.py` do; the new test copies their style.
The Revision puts the R2 pins in the table in `test_review_stance_in_shipped_files.py`, but that table
is read only inside `## Review` and R2 sits under Roles. So the R2 pins go in a new file (where they
live changes, not what is pinned), which keeps the frozen edit to the three old patterns.

Proposed paths:
- bootstrap/tests/test_model_tier_rule_ships.py

**Frozen files.** Derived from `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` and the
glob in `bootstrap/tests/_gate_manifest.py` (`bootstrap/tests/**/*.py`, `scripts/*.py`). Of everything
touched, **one file is frozen: `test_review_stance_in_shipped_files.py`, edited in C1** from its current
text (another session edited it in `cdffeb8a`). Everything else touched is not frozen; the new test file
joins the next anchor. **The re-anchor is MAINTAINER-ONLY**, already in the 0.5 cut (`dev/PLANNING.md`,
"### 0.5" and the Queued re-anchor row); no agent chunk runs it.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | `roles.md`, module twins, mapping, and the frozen patterns that pin them | none | R1, R4, both Answers in the doctrine |
| C2 | Both `AGENTS.md` copies and the new test file | at C2's start, `python tools/intent.py list`; proceed only if no other session holds `AGENTS.md` | R2 and its tests |
| C3 | `CLAUDE.md` bullet; PLANNING edits, made at the archive commit (a shared board file) | none | R3, R5 |
| C4 | Boundary B record | after C1 to C3 | Implementation verification section |
| -- | Gate-manifest re-anchor | **MAINTAINER-ONLY**, at the 0.5 cut | not an agent chunk |

C1's pins land with the text they pin, in one commit. The `CHANGELOG.md` line comes with the archive commit.

## Acceptance criteria

**C1.**

1. `git grep -nE "same maker is not one|\*\*and\*\* (is )?a different model architecture" -- doctrine templates dev/modules docs`
   returns nothing. Control: at the plan-open commit it returns 8 lines covering the six
   places. Sentences wrap, so a person also reads each of the six places. Remaining
   "different model architecture" hits are only "distance on request".
2. The new sentence (same-maker stronger model counts; same tier does not) is in `roles.md`
   and both module copies. `pytest bootstrap/tests/test_review_stance_in_shipped_files.py` passes;
   that shows only that text and pattern agree (the same person wrote both), so a person
   reads that each place says what the Decision says.
3. The frozen edit is narrow: `pytest --collect-only -q` on that file lists the same node ids
   before and after (a dropped node is a `COLLECTION-DROPPED` the re-anchor must accept, so no
   label is renamed); a label now naming the old subject gets one comment, as in `cdffeb8a`.
4. Proposal authoring is medium, in three named places: a new row `| Proposal authoring | medium |`
   after the Strategy / Research row in both module copies, and "proposal authoring" in the
   Standard-stakes bullet of `roles.md` (it leaves the High-stakes bullet, `roles.md:167-172`; the
   roster line at `:42-43` describes a frame, not a tier, and stays). The premise-check rule is
   one sentence in all three: a premise-check inside a proposal is its own task, spawned at
   high, its result handed to the medium draft. Strategy / Research (research, premise-checking,
   novel design), Proposal review, Security Review and scribing stay high; the `| Proposal review |
   high |` and `| Plan review | medium |` rows stay byte-equal (pinned). `cmp
   templates/modules/team-gated/model-selection.md dev/modules/model-selection.md` is silent;
   `python scripts/check_model_selection.py` exits 0. In
   `dev/.cairn/model-selection-mapping.yml`, "proposal authoring" moves from the high row to
   the medium row, and the low row names the trivial lane.
5. R1 and R4: `roles.md` and the module's Implementation rows name the lanes; `roles.md` has
   the escalation sentence, generalizing fan-out condition (d). `grep -n -i "worked example"`
   on `roles.md` and the module shows no mention of the cut passage; "Notes on the gating" is
   about 6 lines and keeps the install-gate sentence; `test_model_selection_stub.py` passes.
6. `python bootstrap/scaffold.py upgrade --target . --finalize dev/modules/model-selection.md dev/.cairn/model-selection-mapping.yml`
   (named paths, never bare, so no other session's work is swept in); then
   `python bootstrap/verify_integrity.py --target .` lists neither. Baseline: 23 violations
   from other sessions' files, none among this plan's four lockfile files.

**C2.**

1. At the start of C2, `python tools/intent.py list` shows no claim on either `AGENTS.md`; if one is held, wait.
2. The R2 block sits under `## Roles`, identical in both copies, with the Revision's clauses
   and one change: proposal authoring medium, and Security Review, proposal review,
   premise-checking and other bright-line work high. `python scripts/quality_gate.py --sub neutrality --sub redundancy`
   passes (no model or vendor named).
3. The new test file has: `test_both_agents_copies_carry_the_model_tier_rule`,
   `test_the_rule_sits_under_roles`, `test_deleting_the_name_the_model_sentence_is_reported`
   (mutant red beside a green control), `test_a_profile_with_no_module_still_installs_the_rule`
   (a real `solo-greenfield` install), `test_the_different_maker_condition_is_gone_and_same_tier_is_excluded`
   (the frozen patterns already pin the new sentence, so this pins only what they do not: the
   fan-out paragraph at `roles.md:221` carries it, the old text is absent from all six places,
   and the same-tier exclusion is stated; a mutant putting one old clause back in one place goes
   red beside a green control) and
   `test_proposal_authoring_is_medium_and_proposal_review_stays_high`.
4. `python scripts/token_budget.py` shows `AGENTS.md` at 8,520 tokens or fewer (8,290 today
   plus the Revision's measured 207, with margin); over that, shorten R2.
5. `python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md`; the integrity check
   lists no `AGENTS.md` record. `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/solo-greenfield.yml --target <empty dir>`
   exits 0.

**C3.**

1. The `CLAUDE.md` addendum gains one bullet: pass the model on every new agent call; a
   resumed agent keeps its old model, so start a fresh lower-tier agent for new work. It is
   finalized by path as above.
2. At the archive commit, the `dev/PLANNING.md` deferred table has a row beside "Watch the new review header" with
   the Revision's R5 fields, reworded for Answer 2: after ten proposal reviews, compare
   proposals written at medium with those written at high; if fewer than three of the ten were
   written at high, report counts only and say the comparison is not available. The Queued re-anchor row's "new
   unfrozen test files" sentence names `test_model_tier_rule_ships.py`. The same commit replaces the stale clause at `dev/PLANNING.md:71`,
   "decide in the proposal whether to relax the condition that lets a cheaper author work under a
   check, which today requires a different maker's model and so is closed to a single-vendor
   adopter", with "the condition that lets a cheaper author work under a check was relaxed
   2026-10-26: a stronger model from the same maker now counts".
3. `python scripts/check_cairn.py` and `python tools/board.py` run clean; the board lists this plan.

**C4.** The Verification record has every field `AGENTS.md` names for Boundary B.

**Not turned into a command.** C1.2 (does each sentence say the Decision's rule), the C1.4 row and
sentence placement, and C1.5's "names the lanes" and "about 6 lines" are read by a person. Nothing sees a spawn call, so "name the model at every spawn" is checked
only by the sentence's presence and a reader of author and review names; the reviewer's below-floor flag
is a behavior, not text; R3's claim that a resumed agent keeps its model is harness behavior, not in the
tree; R5 needs ten reviews and the goodnight owner.

## Security preflight, redone for Answer 1

S1: the orchestrating agent picks the checker and its tier, as today. S2: a same-maker checker may share
the author's blind spots, the cost the Maintainer accepted; pre-declared criteria, a checkable artifact,
a strictly higher tier and escalation still bound it. S3: no command fires it; a reader or reviewer, as
today. S4: mislabeled tiers let a weaker check pass; the exclusion list (scientific, security-sensitive,
architecture, irreversible, large edits) is untouched. S5: bright-line work never downshifts; the
data-governance gate applies first, and a same-maker checker sends nothing to a second maker, so
exposure falls.

**Does it need its own Security Review? No (Maintainer confirmed 2026-10-26; the header stays `required(Internal)`).** None of the `AGENTS.md` high-risk
surfaces is edited in the sense that rule means: no engine code; R2 names no vendor; the lockfile
schema, fidelity manifest and `--manifest` do not change (only a content hash advances); and the
proposal's own test, "a trust boundary added, moved, or widened", fails here.

## Verification

**Boundary A.** Tests that read each touched file, found by searching `bootstrap/tests/`, `scripts/` and
`tools/` for its name:

| Touched | Tests and gates |
|---|---|
| `roles.md`, module twins, mapping | `test_review_stance_in_shipped_files.py`, `test_model_selection_stub.py`, `test_check_cairn_content.py`; `check_model_selection.py`; `cmp` on the twins |
| both `AGENTS.md` | the new file, `test_upgrade.py::TestTemplateGatingSafety` (`## Roles` is never in a gated region and survives a solo install), and the tests that read it: `test_writing_rules_ship.py`, `test_certifying_run_rule.py`, `test_comprehension_floor.py`, `test_review_and_verification_rules_ship.py`, `test_verification_boundaries.py`, `test_review_sweep_ships.py`, `test_scope_reduction_trap.py`, `test_stewardship_rules_ship.py`, `test_loop_fidelity_gate.py`, `test_agreement_retired.py`, `test_security_verification.py`, `test_module_merge_lockfile.py` |
| `CLAUDE.md`, PLANNING; every edited Markdown | `test_claim_check_module.py`, `test_board_json_contract.py`, `test_verify_integrity.py`; `claim_check.py <file>`, `check_cairn.py`, `link_check.py`, neutrality and redundancy legs |

**Boundary B mode: `full`.** The change edits a frozen gate test and installed templates whose bytes
feed the lockfile hash, and 45 test files mention `AGENTS.md` (`git grep -l AGENTS.md bootstrap/tests | wc -l`;
a mention count, not a count of tests that read it); I cannot bound those effects
confidently, so uncertainty resolves to `full`. The full suite runs only as a certifying run, so the
record (`Implementation verification -- <agent> -- YYYY-MM-DD`, after C3) holds the scoped runs above
and **`Certified by`: pending**. **Nobody sets `CAIRN_FULL_SUITE` for this change.**

**Boundary C: one code-review loop**, by a fresh session that is not the implementer. It should attack:
(1) the same-maker removal across the tree, not the diff, searching paraphrases such as "another
company"; (2) whether the premise-check sentence reads the same in all three C1.4 places; (3) whether R2 contradicts the pinned wording-cleanup row; (4) the frozen file's node ids; (5)
that each `--finalize` named only its path; (6) the module twins' byte-identity; (7) the new test's
mutant and control, run against the old text.

**Scope delta**: preserved. The Revision's one removed unit (raising the writing floor on named
high-risk surfaces) is closed by Answer 4; no `defer` is owed.
## Plan review -- Claude Sonnet 5.5 (Internal, fresh session) -- 2026-10-26

```
Reviewed commit: 18ba5907aaea55eba365987dd4500ef27d33cdcc
Target: the whole plan, read against the Revision and Decision of dev/proposals/archive/2026-10-26-claude-model-tier-rules.md and the tree at the reviewed commit
Prior findings: none
Assurance path: high-assurance, inherited from the source proposal
```

**Obligation**: Internal
**Tier**: Internal
**Model**: Sonnet 5.5, fresh session. I did not write this plan.
**Findings**: raised (0 blocking, 6 non-blocking)
**Verdict**: deliverable as written; fold the six non-blocking points, then `ready-to-implement`.

**Conclusion first.** The plan delivers the Decision. Its counts are right against the
current tree, the departure from the Revision (R2 pins in a new file) is correct, and
the frozen-file, claim-gate and Boundary B reasoning all hold. Nothing blocks. The six
points below tighten wording, close two gaps the plan leaves for code review to find,
and fix one measure that Answer 2 quietly empties. Setting Status to `revising-plan`
because findings were raised and the author's fold carries it on; no second pass.

**Foundations**

1. **Should this happen as framed (does the plan deliver the Decision)?** Yes. Answer 1
   (same maker counts, strictly higher tier, same tier does not) and Answer 2 (proposal
   authoring medium; Strategy / Research, proposal review, Security Review high) each
   map to a chunk and a criterion, and the Out list leaves the Decision alone --
   `git grep -nE "same maker is not one|\*\*and\*\* (is )?a different model architecture" -- doctrine templates dev/modules docs`
   returns 8 lines in 6 places at 18ba5907, as the plan says.
2. **Best alternative.** The plan is already the lean version: three commits of prose
   plus one new test file, no new tool or field. The only simpler path I found is trimming
   duplicate pins in the new test file (finding 5); nothing simpler reaches the Decision's
   outcomes, because the six places and three patterns must move together --
   `bootstrap/tests/test_review_stance_in_shipped_files.py:944-955` and `:1148-1157`.
3. **What would show it wrong.** A paraphrase of the old condition surviving outside the
   grep's roots, or a pinned pattern that cannot be made to match the new sentence without
   renaming a node id. I looked for both and found neither:
   `git grep -nIiE "different (model )?(architecture|maker|vendor|company|lab|family)|same maker|second maker|cost rule|downshift"`
   over the live tree (one stale scope note, finding 3); the three patterns are labels
   `condition-a-is-a-different-model-architecture`, `the-cost-rule-check-is-not-a-review`
   (module) and `the-cost-rule-check-is-not-a-review` (roles), and
   `pytest --collect-only -q` lists their ids, so keeping the labels keeps the nodes.

**Lenses used, with evidence**

* **1 Claims.** The six-place count: `doctrine/roles.md:221`, `:230`; each module copy at
  `:129-130` and `:143`. The Decision's "five" is a miscount and the plan says so correctly.
  The three frozen patterns are in `_MODEL_OBLIGATIONS` (two, covering both module copies)
  and `_DOCTRINE_OBLIGATIONS` (one, roles.md). Note `roles.md:221` is not pinned by any
  frozen pattern; only the grep and the new test reach it (finding 5). Frozen claim:
  `gate_manifest.json` `frozen_files` lists `test_review_stance_in_shipped_files.py`,
  `test_model_selection_stub.py`, `test_stewardship_rules_ship.py` and
  `scripts/check_model_selection.py`; the glob in `_gate_manifest.py:352-356` freezes
  `bootstrap/tests/**/*.py` and `scripts/*.py`. Of those, the plan edits only the first;
  it runs the others unedited. The new test file is a "FROZEN-UNTRACKED" note until
  anchored (`_gate_manifest.py:644-660`), the same as `test_writing_rules_ship.py`.
  "cdffeb8a" precedent (label kept, one comment) checked with `git show cdffeb8a`.
  Baseline "23 violations, none among the four lockfile files": reproduced with
  `python bootstrap/verify_integrity.py --target .` (23; no AGENTS, CLAUDE, mapping or
  model-selection line). `upgrade --finalize [PATH ...]` exists as the plan uses it
  (`python bootstrap/scaffold.py upgrade --help`). AGENTS.md at 8,290 tokens:
  `python scripts/token_budget.py`.
* **The R2-in-a-new-file departure: correct.** `_STANCE_OBLIGATIONS` is documented as
  "for the `## Review` section" (`test_review_stance_in_shipped_files.py:93`) and its only
  consumer reads `_review_section(rel)` (`:376-388`). R2 sits under `## Roles`, so a pin
  in that table would never see it, or would force R2 into Review. The plan read this
  right, and the new file keeps the frozen edit to the three old patterns.
* **5 Cross-document consistency.** Found one place the old text lives that the plan does
  not name: `dev/PLANNING.md:71`, "which today requires a different maker's model". Not a
  rule text, so not pinned, but stale once C1 lands (finding 3). Also
  `bootstrap/tests/test_upgrade.py:271-282` (`TestTemplateGatingSafety`) reads the
  `## Roles` heading of `templates/core/AGENTS.md` and fails if it sits in a `cairn:if`
  region; this is the test R2's placement most directly touches, and Boundary A does not
  list it (finding 4).
* **2 Production path / 4 fail-closed.** The mutant for R2 (delete the sentence, red
  beside a green control) is stated; the real `solo-greenfield` install test exercises
  the shipped path, as `test_writing_rules_ship.py` does. No equivalent mutant is stated
  for the same-maker change (finding 5).
* **3 Design completeness.** The AGENTS.md claim gate: `python tools/intent.py list` at my
  review shows no claim on either `AGENTS.md` (5 claims, none touching them), so C2's
  start gate is open now and C2.1 re-checks it at start, which is the right trigger.
  Boundary B `full`: correct. AGENTS.md says bounded mode refuses on contract surfaces and
  that uncertainty resolves to `full`; this change edits a frozen gate test and installed
  templates whose bytes are pinned by tests and hashed into the lockfile, so it is not
  prose-only and not boundable with confidence. Recording a scoped result with
  `Certified by: pending` is what the certifying-run rule requires.
* **6 Drift / 7 Process placement.** The `## Roles` carrier is identical in both
  AGENTS.md copies (`diff` of the two sections is empty), so "identical in both copies"
  is achievable. The re-anchor stays MAINTAINER-ONLY at the cut and is named in the
  Queued row (`dev/PLANNING.md:304-321`).
* **9 Name the satisfier.** Each finding below names one.

**Findings (all non-blocking)**

1. **R5's comparison group may be empty after Answer 2.** C3.2 rewrites R5 to compare
   proposals written at medium with those written at high. With medium now the default,
   few proposals will be written at high, and the earlier 87 name no model at all (the
   Revision's own count). Ten medium proposals and zero high ones compares nothing.
   *Recommend:* the row says what to do then, for example "if fewer than three were
   written at high, report counts only and say so". Satisfier: that clause in the C3.2
   row text.
2. **Say which row and sentence carry the carve-out.** `doctrine/roles.md:42-43` lists
   "drafts proposals" under Strategy / Research, `roles.md:167-172` puts Strategy /
   Research at high, and the module has `| Strategy / Research | high |` at `:49`. C1.4
   says "proposal authoring is medium" without naming where, so two implementers could
   write different rules. Boundary C attack (2) asks whether a proposal needing both
   authoring and premise-checking has a gap; the plan can settle that now, since its own
   Scope already says a premise-check inside a proposal is spawned at high.
   *Recommend:* C1.4 names a new row (for example `| Proposal authoring | medium |`) in
   both module copies and a sentence in the `roles.md` standard/high-stakes bullets, each
   keeping the `| Proposal review | high |` and `| Plan review | medium |` rows byte-equal
   (those two are pinned, `:921-925`), and the carve-out sentence includes the
   premise-check rule. Satisfier: C1.4 text, plus the `test_proposal_authoring_is_medium_...`
   test it already lists.
3. **A stale scope note.** `dev/PLANNING.md:71` ("decide in the proposal whether to relax
   the condition that lets a cheaper author work under a check, which today requires a
   different maker's model") is wrong once C1 lands. *Recommend:* C3.2 adds a one-clause
   edit ("... relaxed 2026-10-26, same maker now counts") in the same row it already
   edits. Also, C2's gate row cites "the other session's `AGENTS.md` claim"; none exists at
   review time, so reword the Sequence cell to "if a claim is held at start". Satisfier:
   the C3.2 criterion and the Sequence cell.
4. **Boundary A mapping is missing the test closest to R2, and one figure is
   unsourced.** Add `bootstrap/tests/test_upgrade.py::TestTemplateGatingSafety` to the
   `AGENTS.md` row (it pins that `## Roles` is never inside a gated region and survives a
   solo install). "About 35 tests that read `AGENTS.md`" has no source:
   `git grep -lE "AGENTS\.md" -- bootstrap/tests | wc -l` gives 45 files. Because the
   mode is `full` this does not change the outcome, but the figure should come from a
   command or be dropped. Satisfier: the Boundary A table row and the Boundary B sentence.
5. **Narrow the new same-maker test and give it a mutant.** The three edited frozen
   patterns already pin that the new sentence is present in the module copies and in
   `roles.md`'s check-is-not-a-review paragraph, so
   `test_a_stronger_model_from_the_same_maker_counts_as_the_check` repeats that. What no
   frozen pattern covers is (a) `roles.md:221` (the fan-out paragraph), (b) the old text
   being absent from all six places, and (c) the same-tier exclusion. *Recommend:* the new
   node asserts exactly (a) to (c), and C2.3 adds a mutant (put one old clause back in one
   place) that goes red beside a green control, as the R2 test has. This matches the
   suite's rule that a test pins one property in one node, and answers Boundary C
   attack (7) before code review. Satisfier: C2.3 text and that node.
6. **Label the non-command criteria honestly, and note the circular one.** The plan's
   "Not turned into a command" paragraph is good. Not yet labelled: C1.2's "the three
   frozen patterns match it" is circular, because the implementer writes both the text
   and the pattern, so a pass shows only that they agree, not that the sentence says the
   right thing; the content is checked by finding 5's node and a person. C1.4's mapping
   row, C1.5's "about 6 lines" and "name the lanes" are reads by a person, not commands.
   *Recommend:* add them to that paragraph in one sentence. Satisfier: that paragraph.

**What I agree with, so the author need not re-justify it.** Keeping the label
`condition-a-is-a-different-model-architecture` with a one-line comment, rather than
renaming and asking the re-anchor to accept a dropped node, is the right trade: the
precedent is `cdffeb8a`, and a rename would add a `COLLECTION-DROPPED` to a Maintainer-only
ceremony for a cosmetic gain. The 8,520-token ceiling leaves a thin 23-token margin over
the Revision's measured 207; the plan already says to shorten R2 if over, which is the
right response.

**Header.** The Maintainer's chat word that the same-maker change needs no separate
Security Review stands; `Plan review: required(Internal)` is left as written and I do not
recommend otherwise. The plan's Security preflight S1-S5 reads soundly; I have no
objection to its "does not need its own Security Review" recommendation beyond what the
Maintainer has already said.

**Coverage line.** Not covered: I ran no test suite and did not set `CAIRN_FULL_SUITE`; I
did not read the new `AGENTS.md` R2 wording (it does not exist yet), so whether it trips
the carrier forbidden patterns (`_FORBIDDEN`, `:100-190` region) is untested; I did not
verify the Revision's 207-token figure, only the 8,290 baseline; I did not check the
Revision's "Strategy / Research may be lowered by Decision" interplay beyond finding 2; I
did not read `test_stewardship_rules_ship.py` or `test_writing_rules_ship.py` beyond their
headers; the harness claim in R3 (a resumed agent keeps its model) is outside the tree and
unchecked.

## Response -- plan author -- 2026-10-26

All six accepted; the operative cells above are revised in place and Status is `ready-to-implement`
(no second plan-review round). Cited lines were opened in the current tree first.

1. **Accepted.** C3.2's R5 row now says: if fewer than three of the ten proposals were written at
   high, report counts only and say the comparison is not available.
2. **Accepted.** C1.4 names the three places (new module row, `roles.md` Standard-stakes bullet,
   the High-stakes bullet it leaves), keeps the two pinned rows byte-equal, and settles the
   premise-check rule now: its own task at high, result handed to the medium draft.
3. **Accepted.** C3.2 replaces the quoted `dev/PLANNING.md:71` clause at the archive commit (shared
   board file); the C2 gate cell now reads "check `python tools/intent.py list` at C2's start".
4. **Accepted.** `test_upgrade.py::TestTemplateGatingSafety` is in Boundary A; "about 35" became 45
   test files that mention `AGENTS.md`, labelled a mention count.
5. **Accepted.** The same-maker node is renamed and narrowed to the fan-out paragraph, old-text
   absence in six places and the same-tier exclusion, with a mutant beside a green control.
6. **Accepted.** C1.2 no longer claims a passing pattern proves the sentence right; it and the
   other read-by-a-person criteria are listed in "Not turned into a command".
   Also: the Security Review question is recorded as answered (no), per the Maintainer.

## Implementation verification -- Claude Sonnet 5.5 (implementer) -- 2026-10-26

**Boundary B mode**: full (the plan's own record; see Verification above). The full suite was not run: it runs only as a certifying run, and `CAIRN_FULL_SUITE` was never set. **Certified by**: pending.

**Tested commit**: f8fc472c7400b3165e89f00f9fb0712d802638b2 (C2, the last of the three implementation commits).
**Reviewed range**: 50b5fbdf3a961b9ed34810caeb28d80161bb0404 (parent of C1) to f8fc472c. Three commits are this plan's: C1 `5702f27a`, C3 `9b9bb3c6`, C2 `f8fc472c`. Other sessions' commits sit between them in the log (for example `cb93f1d9`); read the plan's commits by path.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13. The token figure below used the system `python3` (tiktoken is installed only there); the lhm interpreter reports the characters-divided-by-four proxy, which reads 8,950 for the same file.
**Pre-run state** and **Post-run state**: every file the tests read was committed and unchanged. `git status --short` before and after showed `HEAD` f8fc472c with only other sessions' uncommitted edits to `templates/skills/_lib/session.py` and `tools/session.py` and the untracked `.claude/` and `dev/measurement/collision_log.md`. None of those is read by a test in the table, but I did not prove that for `session.py` and `tools/session.py`.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `pytest` on `test_review_stance_in_shipped_files.py`, `test_model_selection_stub.py`, `test_check_cairn_content.py`, the new `test_model_tier_rule_ships.py`, `test_upgrade.py::TestTemplateGatingSafety`, and the 12 other `AGENTS.md` readers the plan names | 0 | 1,108 passed, 0 failed, 0 skipped, 0 xfail, 0 xpass | 10 s |
| `pytest` on `test_claim_check_module.py`, `test_board_json_contract.py`, `test_verify_integrity.py`, `test_onboarding_seed_roster.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_upgrade_module.py` | 0 | 336 passed, same zeros | 9 s |
| `python scripts/check_model_selection.py` | 0 | mapping filled | 1 s |
| `python scripts/check_cairn.py` | 0 | 191 files, no issues | 1 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality fail=0, redundancy fail=0 | 2 s |
| `python scripts/claim_check.py` on the six edited Markdown files | 0 each | no flags | under 1 s each |
| `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/solo-greenfield.yml --target <empty dir>` | 0 | | 1 s |
| `python bootstrap/verify_integrity.py --target .` | 1 | 23 violations, all in other sessions' files; none of `AGENTS.md`, `CLAUDE.md`, `dev/modules/model-selection.md`, `dev/.cairn/model-selection-mapping.yml` | 1 s |
| `cmp templates/modules/team-gated/model-selection.md dev/modules/model-selection.md` | 0 | silent | 0 s |
| `git grep -nE "same maker is not one\|\*\*and\*\* (is )?a different model architecture" -- doctrine templates dev/modules docs` | 1 | no match; the same command returned 8 lines in 6 places before C1 | 0 s |
| `python3 scripts/token_budget.py` (tiktoken) | 0 | `AGENTS.md` 8,518 tokens; ceiling 8,520 | 1 s |

**Non-pass disposition**: no skip, xfail or xpass. The one non-zero exit is `verify_integrity` at 23 violations, the baseline the plan states, none among this plan's four lockfile files.

**Plan-specific acceptance commands**
* C1.3: `pytest --collect-only -q` on `test_review_stance_in_shipped_files.py` lists 464 node ids before and after, `cmp` silent; no label renamed; one comment on the label that now names the old subject.
* C1.6: the module's lockfile record was finalized by path (`dev/modules/model-selection.md` and the mapping); the mapping is `living_state` and holds no checked hash, so one hash advanced. The other session's commit `cb93f1d9` carried the lock file, so my module record landed there; my own commits did not name the lock until C2.
* C2.2 and C2.3: the new file has the six named tests plus a copy-equality and a proposal-authoring node (9 in all). Run against the pre-C1 text of the five files (a copy outside the tree), 8 of 8 non-install nodes fail; the install node needs the real tree. Each mutant is beside a control run on the real text.
* C2.4: 8,518 tokens against the ceiling of 8,520. **Deviation from the plan's wording, not its criterion**: another commit raised the `AGENTS.md` baseline from the plan's 8,290 to 8,367 before C2, leaving R2 153 tokens instead of the Revision's 207. R2 omits three of the Revision's clauses to fit: the pointer to `doctrine/roles.md`, "search helpers and wording-only edits: low" (still in `roles.md` and the module), and "author and reviewer names carry the model". It also reads "no Maintainer Decision quoted on it", without "or dated direction". The reviewer should read whether that loses a promise the Decision relied on.
* C2.5: `finalize` by path for `AGENTS.md` and `CLAUDE.md`; neither is in the integrity list.
* C3.1: the `CLAUDE.md` bullet is in `9b9bb3c6`; its lock record landed in `f8fc472c` because another session claimed the lock file when C3 was committed.
* C3.2 (the `dev/PLANNING.md` row, the Queued re-anchor row's file name, the stale clause at line 71, and the `CHANGELOG.md` line) is deferred to the archive commit by the plan and is not done.
* C3.3: `python tools/board.py` listed this plan (before this section; the Status line now reads `awaiting-code-review`).

**Known omissions**
* The full suite was not run. Everything above is scoped.
* The gate-manifest and AST re-anchors are Maintainer-only and not run; the edit to the frozen `test_review_stance_in_shipped_files.py` and the new test file wait for the re-anchor at the 0.5 cut. I did not run `_gate_manifest.py verify`.
* No test reads a spawn call, so "name the model at every spawn" and R3's claim that a resumed agent keeps its model are unchecked.
* Whether each of the six places says what the Decision says (C1.2), the C1.4 row and sentence placement, and C1.5's "names the lanes" and "about 6 lines" (the gating note is 8 lines) are for a person to read.
