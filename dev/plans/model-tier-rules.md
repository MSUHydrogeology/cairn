# Plan: Model-tier rules, with same-maker checks and medium proposal authoring

**Author**: Claude Sonnet 5.5 (Strategy, plan author)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-model-tier-rules.md](../proposals/archive/2026-10-26-claude-model-tier-rules.md)
**Status**: awaiting-plan-review
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
| C2 | Both `AGENTS.md` copies and the new test file | starts only after the other session's `AGENTS.md` claim releases | R2 and its tests |
| C3 | `CLAUDE.md` bullet; PLANNING row | none | R3, R5 |
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
   and both module copies, and the three frozen patterns match it:
   `pytest bootstrap/tests/test_review_stance_in_shipped_files.py` passes.
3. The frozen edit is narrow: `pytest --collect-only -q` on that file lists the same node ids
   before and after (a dropped node is a `COLLECTION-DROPPED` the re-anchor must accept, so no
   label is renamed); a label now naming the old subject gets one comment, as in `cdffeb8a`.
4. `roles.md` and both module copies say proposal authoring is medium, and Strategy /
   Research, proposal review, Security Review and scribing stay high; the pinned rows
   (`| Plan review | medium |` and the rest) are unchanged. `cmp
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

1. `python tools/intent.py list` shows no claim on either `AGENTS.md`; if one is held, wait.
2. The R2 block sits under `## Roles`, identical in both copies, with the Revision's clauses
   and one change: proposal authoring medium, and Security Review, proposal review,
   premise-checking and other bright-line work high. `python scripts/quality_gate.py --sub neutrality --sub redundancy`
   passes (no model or vendor named).
3. The new test file has: `test_both_agents_copies_carry_the_model_tier_rule`,
   `test_the_rule_sits_under_roles`, `test_deleting_the_name_the_model_sentence_is_reported`
   (mutant red beside a green control), `test_a_profile_with_no_module_still_installs_the_rule`
   (a real `solo-greenfield` install), `test_a_stronger_model_from_the_same_maker_counts_as_the_check`
   (new text present, old absent, in `roles.md` and both module copies) and
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
2. The `dev/PLANNING.md` deferred table has a row beside "Watch the new review header" with
   the Revision's R5 fields, reworded for Answer 2: after ten proposal reviews, compare
   proposals written at medium with those written at high. The Queued re-anchor row's "new
   unfrozen test files" sentence names `test_model_tier_rule_ships.py`.
3. `python scripts/check_cairn.py` and `python tools/board.py` run clean; the board lists this plan.

**C4.** The Verification record has every field `AGENTS.md` names for Boundary B.

**Not turned into a command.** Nothing sees a spawn call, so "name the model at every spawn" is checked
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

**Does it need its own Security Review? My recommendation: no.** None of the `AGENTS.md` high-risk
surfaces is edited in the sense that rule means: no engine code; R2 names no vendor; the lockfile
schema, fidelity manifest and `--manifest` do not change (only a content hash advances); and the
proposal's own test, "a trust boundary added, moved, or widened", fails here. The Maintainer has not
decided this. **Question, default no:** should plan review also run a Security Review of this change? If
yes, the header becomes `required(Internal + Internal Security Review)` before plan review starts.

## Verification

**Boundary A.** Tests that read each touched file, found by searching `bootstrap/tests/`, `scripts/` and
`tools/` for its name:

| Touched | Tests and gates |
|---|---|
| `roles.md`, module twins, mapping | `test_review_stance_in_shipped_files.py`, `test_model_selection_stub.py`, `test_check_cairn_content.py`; `check_model_selection.py`; `cmp` on the twins |
| both `AGENTS.md` | the new file, and the tests that read it: `test_writing_rules_ship.py`, `test_certifying_run_rule.py`, `test_comprehension_floor.py`, `test_review_and_verification_rules_ship.py`, `test_verification_boundaries.py`, `test_review_sweep_ships.py`, `test_scope_reduction_trap.py`, `test_stewardship_rules_ship.py`, `test_loop_fidelity_gate.py`, `test_agreement_retired.py`, `test_security_verification.py`, `test_module_merge_lockfile.py` |
| `CLAUDE.md`, PLANNING; every edited Markdown | `test_claim_check_module.py`, `test_board_json_contract.py`, `test_verify_integrity.py`; `claim_check.py <file>`, `check_cairn.py`, `link_check.py`, neutrality and redundancy legs |

**Boundary B mode: `full`.** The change edits a frozen gate test and installed templates whose bytes
feed the lockfile hash and about 35 tests that read `AGENTS.md`; I cannot bound those effects
confidently, so uncertainty resolves to `full`. The full suite runs only as a certifying run, so the
record (`Implementation verification -- <agent> -- YYYY-MM-DD`, after C3) holds the scoped runs above
and **`Certified by`: pending**. **Nobody sets `CAIRN_FULL_SUITE` for this change.**

**Boundary C: one code-review loop**, by a fresh session that is not the implementer. It should attack:
(1) the same-maker removal across the tree, not the diff, searching paraphrases such as "another
company"; (2) whether "authoring medium" and "premise-checking high" leave a gap for a proposal needing
both; (3) whether R2 contradicts the pinned wording-cleanup row; (4) the frozen file's node ids; (5)
that each `--finalize` named only its path; (6) the module twins' byte-identity; (7) the new test's
mutant and control, run against the old text.

**Scope delta**: preserved. The Revision's one removed unit (raising the writing floor on named
high-risk surfaces) is closed by Answer 4; no `defer` is owed.