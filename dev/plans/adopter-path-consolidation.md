# Plan: retire the adoption levels

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md`
**Status**: ready-to-implement
**Plan review**: required(Internal)
**Assurance path**: high-assurance — inherited: the change edits
`doctrine/onboarding.md`, removes code from adopter-executed scripts, and
changes frozen files.
**Opened**: 2026-10-01

## Source proposal

Accepted 2026-10-01 as Revision 2 (`79fe14bd`). Cairn stops publishing adoption
levels. There are two ways to use it — read the doctrine, or install it with the
scaffold — and the profile, not a level, sizes the install. The hand-copy route
is gone from every recommended path; the quickstart stays a throwaway shakedown
that points at the real route. The four level triggers and the one "Level 1→2
graduation" prompt are deleted. The Decision deferred F8 (the post-install
report, deposited at `9276833c`), waived the External floor, and ruled out a
second review round.

## Scope

Revision 2's items 1–10 and its `doctrine/onboarding.md` change, and nothing
else. Every outcome is mapped to a chunk in *Scope fidelity* below.

**Not touched:** `bootstrap/_scaffold/` (so no AST re-anchor), the action
triggers, the `collab-agreement-signing` and `second-agent-type` prompt rows
other than removing the row between them, and `CHANGELOG.md` until the archive
step.

### Constraints the planning search found

Each is a test that reads a file this plan edits. Breaking one is a defect,
not a re-baseline.

* **`bootstrap/tests/test_practice_modules.py::TestLadderCorrespondence`**
  requires `on-ramp/README.md` to carry `## Level N` headings that match a
  `## The maturity ladder` section. That is the property this plan retires, so
  the class is removed in the same commit as the on-ramp rewrite (C3), not
  edited to pass. Frozen file: it joins the re-anchor set.
* **`bootstrap/tests/test_active_surfacing_render.py`** looks the graduation row
  up with `next(...)` and asserts its body names `BOOTSTRAP.md`. With the row
  gone that raises, so the graduation-specific test is removed with the row
  (C1).
* **`bootstrap/tests/test_presets.py`** parses the YAML block under
  `<!-- solo-legacy-recipe: canonical-profile -->` in
  `docs/solo-legacy-recipe.md` and pins `preset`, `age`, `modules_add` and the
  resulting roster. That block stays byte-identical; the prose around it
  changes.
* **`bootstrap/tests/test_quickstart_sequence.py`** (frozen, not edited) reads
  `**N** modules listed` and `**N unfilled block slots**` from
  `docs/quickstart.md`. Both phrases stay.
* **`bootstrap/tests/test_profile_grammar.py`** reads marked blocks in
  `bootstrap/BOOTSTRAP.md`; C5's edits stay outside those markers.
* **`bootstrap/tests/test_onboarding_activation_helper.py:460`** asserts an
  error message names `doctrine/onboarding.md`. The file keeps existing.

### Documentation / doctrine surface

**Doctrine:** `doctrine/onboarding.md` (C2). **Entry and descriptive layers:**
the pages in C3–C6. No `AGENTS.md` change.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **Delete the level triggers and the graduation prompt.** In `scripts/_onboarding/` and its twin `templates/modules/default-on/_onboarding/`: `evaluate_maturity_triggers` and its four triggers (`triggers.py`); the four `LEVEL_{1,2}_DEEPEN_*_THRESHOLD` constants and the two archived-count helpers (`triggers.py:41-72`), which nothing else uses; their re-exports and the evaluator's (`__init__.py:111-119`, `:129`); the evaluator's call in the union evaluator, and that function's docstring (`triggers.py:438`); and the `Level-1-to-2-graduation` row (`prompts.py`). The launcher's docstring, `scripts/onboarding_activate.py:8` and its twin, stops saying "maturity + action". In the three `templates/onboarding/*.md` presets and Cairn's copy `dev/modules/onboarding/collaborative-team.md`: the `### Row 2 -- Level 1→2 graduation prompt` sections; the whole `[trigger: level-1-to-2; id: graduate-to-level-2]` deferred-task entry, body included; and any intro line that counts "three active-surfacing rows". The remaining rows keep their heading labels. Tests: `test_trigger_evaluation_maturity.py` is rewritten to pin the negative invariant, using literal counts; `test_active_surfacing_mechanism.py` drops its two graduation tests; `test_active_surfacing_render.py` drops the graduation row, its graduation-specific test, and the stale counts in its docstring and in the `TestTwelveCombinations` name. Scoped lockfile finalize in the same commit. | `ready-to-implement` **and** the Maintainer's allowance on the narrowed `verify_integrity` criterion (*Scope delta*), quoted in this plan | one commit |
| C2 | **Doctrine.** `doctrine/onboarding.md`: remove the maturity-ladder trigger kind (`:62-77`) and its claim to observe the on-ramp; activation's "maturity-ladder transitions" (`:26`); the "Level 1 → 2 graduation" entry in the priority order (`:218-221`); "all three active-surfacing rows" (`:288-289`) and the three named rows (`:118-123`), which become two; and the description of `on-ramp/README.md` as the ladder the triggers observe (`:350-351`). `doctrine/session-routines.md:375`: the goodnight helper no longer scans for maturity-ladder transitions. | C1 | one commit |
| C3 | **The on-ramp.** `on-ramp/README.md` rewritten: read it or install it; choosing a profile; growing an install (`scaffold.py upgrade --adopt-module <name>`); the migration note (Revision 2 item 9). `bootstrap/UPGRADE.md` gains one line naming hand-copied trees in "Migrating a tree installed before upgrade support". `TestLadderCorrespondence` removed, with the module docstring's two lines about the ladder (`test_practice_modules.py:2`, `:8-10`). | — | one commit |
| C4 | **Entry pages.** `README.md` (the three-level block and `:266`); `docs/getting-started.md` (`:4`, `:84-86`); `docs/quickstart.md` (real-install statement, the real route in "What to do next", "pick a level" at `:339` and the "maturity ladder" pointer at `:367`, the level summary at `:350-353` removed, `NOTICE.md` added to `:194`, "Time: ~30 seconds" at `:296` removed). | C3 | one commit |
| C5 | **The install route.** `docs/solo-legacy-recipe.md` ("Which level" removed; scaffold route; roster corrected to eight); the three `bootstrap/profiles/*.yml` header comments; `bootstrap/BOOTSTRAP.md` (`:7`, `:231`); `bootstrap/prompts/bootstrap-lite.md` (including "the three adoption levels" at `:52` and `:159`); `templates/codebase-readiness-report.md` (`:340-347`, scores map to how small to start). | C3 | one commit |
| C6 | **Every remaining reference.** `templates/README.md` (`:82-86`); both example READMEs (including "Level-1" at `examples/minimal/README.md:48`); `docs/agent-team-onboarding.md:9` and Cairn's copy `dev/modules/onboarding/agent-team-onboarding.md`; `docs/workflow-role.md:83`; `docs/further-reading.md:30`; any level wording left in the presets and Cairn's copies. Ends with the completeness grep. | C1–C5 | one commit |
| C7 | **Boundary B**, then `## Implementation verification`; status → `awaiting-code-review`. | C6 | one commit |
| M | **MAINTAINER-ONLY — the gate-manifest re-anchor.** This plan's eight changed frozen files, and every pinned test node it drops or adds (*Verification* > Expected non-pass), join the batch already queued in `dev/PLANNING.md`, as Revision 2 item 10 specifies; the re-anchor runs with that batch, per `bootstrap/REANCHOR_RUNBOOK.md`. **An implementing agent must not perform it.** The agent's part is the board update at archive. | code review cleared | Maintainer |

The order keeps the suite green at every chunk boundary, and the one test that
pins the old ladder leaves in the commit that removes the ladder (C3). Code and
doctrine disagree for one commit only: C2 lands directly after C1.

## Acceptance criteria

* **C1 — negative invariant.** The union trigger evaluator returns no id
  beginning `level-` on any of four trees, chosen so each deleted trigger would
  fire on at least one: a fresh `solo-greenfield` install; a tree with a
  lockfile, 5 archived proposals and 3 archived plans; a tree **without** a
  lockfile, at 5 and 3 (`level-0-to-1`, `level-1-deepen`); and a tree with a
  lockfile at 15 and 10 (`level-1-to-2`, `level-2-deepen`). The counts are
  literals, because the threshold constants are deleted. Rewritten
  `test_trigger_evaluation_maturity.py` asserts all four, and fails if any one
  of the four deleted `out.add("level-...")` lines is restored.
* **C1 — the prompt registry.** `_ACTIVE_SURFACING_ROWS` has two rows; every
  preset × remaining-row pair still renders a non-empty body
  (`test_active_surfacing_render.py`).
* **C1 — twins.** `diff -r --exclude=__pycache__ scripts/_onboarding
  templates/modules/default-on/_onboarding` prints nothing.
* **C1 — lockfile.** `python bootstrap/scaffold.py upgrade --finalize
  scripts/_onboarding/triggers.py scripts/_onboarding/prompts.py
  scripts/_onboarding/__init__.py scripts/onboarding_activate.py --target .`
  runs in the C1 commit. **The tree does not pass `verify_integrity` today**:
  `python bootstrap/verify_integrity.py --target .` exits 1 with 21 hash
  mismatches (measured 2026-10-01), and all three `scripts/_onboarding/` files
  are among them, left by earlier unfinalized changes; the launcher is not. So
  the criterion is the drop, not a pass. **Immediately before C1**, record the
  current finding list. After C1, it reports no finding for any
  `scripts/_onboarding/` file or `scripts/onboarding_activate.py`, and every
  other finding on the recorded list is unchanged.
* **C2 — doctrine matches code.** Every trigger id named in
  `doctrine/onboarding.md` is one the trigger evaluators can return, and none
  begins `level-`. Neither `doctrine/onboarding.md` nor
  `doctrine/session-routines.md` matches the C6 pattern below.
* **C3 — migration note.** It carries the literal
  `upgrade --target <repo> --init-lock` sequence, says the tree gets no
  upgrades and no onboarding prompts until it runs, and says not to re-run the
  install with `--force`.
* **C4 — quickstart.** The teardown and the throwaway signature-check waiver
  are unchanged; the real route names release-tag verification as required.
  `test_quickstart_sequence.py` passes unedited.
* **C5 — recipe.** `test_presets.py` passes with the canonical-profile block
  untouched; a scaffold run of that profile into a fresh repository reports
  eight modules and zero staffability warnings.
* **C6 — completeness.** `grep -rlE "Level[ -][012]|level-[012]-|Level-1-to-2|hand-copy([^i]|$)|[Mm]aturity[- ]ladder|adoption levels?|(pick|choose|which) (an? )?(adoption )?level\b"
  --exclude-dir=dev --exclude-dir=.git --exclude-dir=.claude
  --exclude=CHANGELOG.md .` returns 31 files before C1 (positive control,
  measured 2026-10-01: Revision 2's 29 plus `test_practice_modules.py` and
  `doctrine/session-routines.md`). After C6 it returns only
  `bootstrap/tests/fixtures/gate_manifest.json` (cleared by M) and the
  rewritten `test_trigger_evaluation_maturity.py` (names the retired ids on
  purpose). The same pattern over `dev/modules/onboarding/` matches both of
  Cairn's copies before and nothing after. This pattern is wider than
  Revision 2's, which missed spellings in use ("Level-1", "pick a level",
  "maturity ladder", "adoption levels").
* **Throughout — the published manifest does not move.**
  `python bootstrap/scaffold.py --manifest` is byte-identical before C1 and
  after C6.
* **Throughout — no frozen file is deleted.** A deleted frozen file reddens
  `test_gate_manifest.py` until M; this plan edits frozen files instead.

  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
  <!-- cairn:end acceptance-doc-tooling -->

### Scope fidelity

Revision 2's outcomes, each to its chunk: item 1 → C3; 2 → C4; 3 → C4;
4 → C4; 5 → C5; 6 → C5; 7 → C5 and C6; 8 → C1; 9 → C3; 10 → C1 (finalize,
`verify_integrity`) and M; `doctrine/onboarding.md` → C2. The completeness,
negative-invariant, doctrine, twin and manifest criteria → C1, C2, C6.
Boundary B full → C7.

**Two surfaces Revision 2 did not list by name**, each reached by an accepted
item rather than added to it:

* `doctrine/session-routines.md:375` (C2) — a second doctrine file, which says
  the goodnight helper scans for maturity-ladder transitions. Item 7, "every
  remaining level reference", reaches it, and item 8's deletion makes it false.
* `scripts/onboarding_activate.py:8` and its twin (C1) — the launcher's
  docstring, which says "maturity + action" trigger evaluation. Item 8's
  deletion makes it false. The `scripts/` copy is frozen, so it is the eighth
  frozen file.

## Scope delta

**Scope delta**: preserved. Nothing accepted is dropped. F8 was deferred by the
Decision itself and is already on the board (`9276833c`).

**One accepted criterion cannot be met as worded, and needs the Maintainer's
allowance.** Revision 2 says `bootstrap/verify_integrity.py` "passes on Cairn's
own tree after the lockfile re-finalize". It cannot: the tree fails today with
21 mismatches, 18 of them in files this change never touches (for example
`scripts/claim_check.py`, `tools/_intent/conflict.py`). Finalizing those would
record unreviewed drift as trusted, which is outside this plan. The plan holds
the criterion to the files it changes — C1 removes the three `scripts/_onboarding/`
findings and leaves the other 18 as they are. The outcome Revision 2 names, the
lockfile re-finalized for `scripts/_onboarding/`, is delivered in full.

**The allowance is C1's gate.** C1 does not start until the Maintainer's
allowance is appended to this plan, quoted verbatim. The "other 18" figure is
re-measured immediately before C1, not carried forward from 2026-10-01.

## Verification

**Boundary A (iteration, scoped)** — the reviewed mapping, per chunk:

* **C1:** the files that import or read `_onboarding` —
  `test_trigger_evaluation_maturity.py`, `test_trigger_evaluation_action.py`,
  `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`,
  `test_onboarding_activation_helper.py`, `test_onboarding_seed_roster.py`,
  `test_onboarding_slot_substitution.py`, `test_onboarding_review_tiers.py`,
  `test_skills_onboarding.py`, `test_deferred_task_store.py`,
  `test_upgrade_side_door_parity.py`, `test_install_module.py`,
  `test_module_merge_lockfile.py`, `test_hardening.py`,
  `test_facade_loader_cleanup.py`, `test_security_leaf.py`,
  `test_cairn_prefix_links.py` — plus the twin `diff` and `verify_integrity`.
* **C2:** `test_onboarding_activation_helper.py`.
* **C3:** `test_practice_modules.py`.
* **C4:** `test_quickstart_sequence.py`.
* **C5:** `test_presets.py`, `test_profiles_smoke.py`, `test_profile_grammar.py`,
  `test_quickstart_sequence.py` (reads `solo-greenfield.yml`), and the two
  scaffold runs (`solo-greenfield`; the recipe's profile).
* **C6:** `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
  `test_onboarding_review_tiers.py` (reads the presets),
  `test_claim_check_module.py`, `test_link_check_exclusions.py`,
  `test_cairn_prefix_links.py`, and the completeness grep.
* **Every chunk:** `scripts/claim_check.py`, `scripts/link_check.py` and
  `scripts/check_cairn.py` over the touched files.

<!-- cairn:slot verification-commands -->
Before implementation, make Boundary A a **reviewed mapping**: for each changed
invariant and public path, name the exact affected test node/file and every
standing non-pytest gate for the touched surface. Run that scope while
iterating. There is no permanent fast tier; if a substantive code surface has
no reviewed mapping or cannot be bounded confidently, run the full suite.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the canonical interpreter. The default is the **full
suite**; a plan whose reviewed mapping **bounds the change's effects
confidently** may instead run that mapping plus every standing gate for every
touched surface. Bounded mode **refuses** — run full — when the change touches a
**contract surface** (install contract, fidelity or gate manifest, lockfile
schema, published `scaffold.py --manifest`) or a **trust-ceremony surface**
(any high-risk surface `AGENTS.md` names, or release/security ceremony work).
**Uncertainty resolves to `full`.** The commands:

* **Engine + seed-0 order coverage** — `python -m pytest bootstrap/tests
  --quality-gate-shuffle-seed=0`.
* **Static quality legs** — `python scripts/quality_gate.py --sub neutrality
  --sub redundancy` (does not dispatch pytest again).
* **Prose integrity** — `python scripts/check_cairn.py`.
* **Write-time claim check** — `python scripts/claim_check.py <file>` once for
  each authored proposal, plan, or doc.
* **Plan-specific acceptance commands** — the mapped tests, security budgets,
  doc-drift gates, public-path smokes, and other commands named above.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full SHA.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  `HEAD`.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.
<!-- cairn:end verification-commands -->

**Boundary B (integration) — `full`, fixed.** The change edits frozen files
covered by the gate manifest, a contract surface, so bounded mode refuses. The
pair, under `/Users/kendal30/conda_envs/lhm/bin/python3.13`:
`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests
--quality-gate-shuffle-seed=0`, then
`python scripts/quality_gate.py --sub neutrality --sub redundancy`. Run it with
no other session's suite running, and say so in the record.

**Expected non-pass, to be disposed of rather than treated as noise:** none
from `test_gate_manifest.py`, because no frozen file is deleted; the manifest
is stale for the eight changed frozen files, which a green run does not show
(`AGENTS.md` > Operational pitfalls). The record lists the eight by path.

**The manifest also pins test node IDs**, and the re-anchor ceremony shows the
Maintainer a change in the collection count, so the record accounts for it. It
lists, by node ID and by chunk, every pinned node this plan drops and every
node it adds. Known before implementation, 19 dropped:
* C1 — all 12 current nodes of `test_trigger_evaluation_maturity.py`, which the
  rewrite replaces;
* C1 — in `test_active_surfacing_render.py`,
  `test_level_graduation_drafts_concrete_per_preset_p3_9` and the three
  `TestTwelveCombinations` cases parametrized on `Level-1-to-2-graduation`;
  renaming that class changes the IDs of its remaining cases too;
* C1 — in `test_active_surfacing_mechanism.py`,
  `TestPriorityOrder::test_collab_agreement_wins_over_level_graduation` and
  `::test_level_graduation_wins_over_second_agent`;
* C3 — `test_practice_modules.py::TestLadderCorrespondence::test_ladder_levels_match_adoption_levels`.

**Boundary C** is the code reviewer's. Attack at least: the negative invariant
(restore one `out.add` line and confirm the test fails); the completeness grep's
before-set; and whether any remaining onboarding prompt still renders.

**Security preflight.** N/A, as in the proposal: no trust boundary added,
moved, or widened. The chunking changes no answer.

## Dispositions

*Filled at archive-preparation.* Expected: F8 is already deposited
(`9276833c`); at archive, this plan's eight changed frozen files, and the
dropped and added test node IDs from the implementation record, are added to
the queued re-anchor row in `dev/PLANNING.md`, which Revision 2 item 10
authorizes; and `CHANGELOG.md` > Unreleased gets one entry for the retired
levels.

## Plan review -- Claude (Internal, fresh-context subagent) -- 2026-10-01

**Model**: claude-opus-5-5

Reviewed commit: fbdc0ed94367169d489157cd05cb7ae13ab8c3cf
Target: the plan as opened -- all sections
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**What holds.** Each item below was checked against the tree at the reviewed
commit, not taken from the plan.

* **Scope.** Every Revision 2 outcome (items 1–10 and the
  `doctrine/onboarding.md` change) maps to a chunk, and the plan adds no
  outcome Revision 2 did not accept.
* **The frozen set is seven, and correct.** I looked each touched file up in
  the keys of `frozen_files` (183 entries), with
  `templates/modules/default-on/_onboarding/triggers.py` as the known-present
  control. The seven are the three template `_onboarding/` files, the three
  named tests, and `test_practice_modules.py`. `test_presets.py` and
  `test_quickstart_sequence.py` are frozen but not edited. Every doc, profile,
  preset, `scripts/_onboarding/` file and the lockfile is free.
* **The suite stays green at each chunk boundary.** Outside the two
  `_onboarding/` packages and the three test files C1 names, no Python file
  references the row, a `level-` trigger id or `evaluate_maturity_triggers`. No test counts a preset's deferred tasks, and
  none reads the chosen active prompt without an override. No link targets an
  on-ramp section by fragment, so C3–C6 leave no broken anchor between
  commits.
* **Measured figures.** The completeness grep returns 29 files today. The
  output of `verify_integrity` matches the plan (exit 1, 21 violations, the
  three `scripts/_onboarding/` files among them). C5's eight modules are
  `_DEFAULT_ON_MODULES` (six) plus the two the recipe adds, which
  `test_presets.py` derives.
* **The narrower `verify_integrity` reading is sound.** Item 10's outcome
  (re-finalize `scripts/_onboarding/`, run the check) is delivered in full.
  Finalizing the other 18 would re-attest drift that nobody reviewed in this
  change. [P4] covers the one gap in how the plan asks for the allowance.

### Findings

**[P1] blocking — the negative-invariant test cannot catch two of the four
restorations.** Each deleted trigger has its own firing condition
(`scripts/_onboarding/triggers.py:41-50`, `:110-121`). `level-1-deepen` fires
only *without* a lockfile, at 5 archived proposals and 3 archived plans.
`level-2-deepen` fires only *with* a lockfile, at 15 and 10. Both of the
criterion's fixtures carry a lockfile: the fresh `solo-greenfield` install,
and the lockfile tree with 5 and 3. Neither reaches 15 and 10. So restoring
`out.add("level-1-deepen")` or `out.add("level-2-deepen")` leaves the
rewritten test green, and the Boundary C probe in this plan would expose it.
*Close:* in *Acceptance criteria* > C1 — negative invariant, keep Revision 2's
two fixtures and add two more, so that every deleted trigger would fire on at
least one fixture:
* a tree **without** a lockfile, with 5 archived proposals and 3 archived
  plans (this exercises `level-0-to-1` and `level-1-deepen`);
* a tree **with** a lockfile, with 15 archived proposals and 10 archived plans
  (this exercises `level-1-to-2` and `level-2-deepen`).

**[P2] blocking — the re-anchor handoff does not account for the test nodes
the plan removes.** The gate manifest pins pytest node IDs as well as file
bytes. Its verifier treats a dropped node as a hold
(`bootstrap/tests/_gate_manifest.py:33-36`, `:672-680`), and the ceremony
shows the Maintainer the change in the collection count
(`bootstrap/tests/_gate_preflight.py:1958-1959`). Counted against
`collection.node_ids` in `bootstrap/tests/fixtures/gate_manifest.json`, the
plan drops 19 pinned nodes:
* in C1, all 12 current nodes of `test_trigger_evaluation_maturity.py`, which
  the rewrite replaces;
* in C1, four in `test_active_surfacing_render.py`:
  `test_level_graduation_drafts_concrete_per_preset_p3_9` and the three
  `TestTwelveCombinations` cases parametrized on `Level-1-to-2-graduation`;
* in C1, two in `test_active_surfacing_mechanism.py`:
  `TestPriorityOrder::test_collab_agreement_wins_over_level_graduation` and
  `::test_level_graduation_wins_over_second_agent`;
* in C3, `test_practice_modules.py::TestLadderCorrespondence::test_ladder_levels_match_adoption_levels`.

The *Expected non-pass* cell, the M row and *Dispositions* name only the seven
files. A smaller collection is the signal the gate exists to raise, and as
written it would reach the Maintainer's supervised ceremony with no
explanation. Earlier plans attributed theirs
(`dev/plans/archive/profile-parse-fail-open.md:901`). *Close:* in the
*Expected non-pass* cell, the M row and *Dispositions*, require the
implementation record to list every pinned node this plan drops and every
node it adds, by node ID and by chunk. Carry that list into the queued
re-anchor row at archive.

**[P3] blocking — some level vocabulary is reached by neither the chunk cells
nor the completeness grep.**
*(a) Doctrine.* C2 names only `doctrine/onboarding.md:62-77` and `:118-123`.
Four other passages in the same file still describe the levels:
* `:26` says activation fires on "maturity-ladder transitions";
* `:218-221` lists "Level 1 → 2 graduation" in the priority order;
* `:288-289` says v1 ships "all three active-surfacing rows";
* `:350-351` describes `on-ramp/README.md` as the ladder the triggers observe.

A second doctrine file, `doctrine/session-routines.md:375`, describes the
goodnight helper as scanning for maturity-ladder transitions. C2's criterion
checks trigger ids only, so it passes with every one of these passages still
in place.
*(b) The grep's spelling gaps.* The C6 pattern misses spellings that are in
use today in files this plan edits:
* `examples/minimal/README.md:48`: "Level-1";
* `docs/quickstart.md:339`: "pick a level";
* `docs/quickstart.md:367`: "maturity ladder";
* `bootstrap/prompts/bootstrap-lite.md:52` and `:159`: "the three adoption
  levels";
* `scripts/_onboarding/triggers.py:438` and its twin: the union docstring.

C4 names only `docs/quickstart.md:350-353`. Once those lines are gone, the
file drops out of the grep's results while `:339` and `:367` still point at a
ladder that C3 removes.
*Close:* (a) Widen C2's cell to cover the four further passages and
`doctrine/session-routines.md:375`. In *Scope fidelity*, record that item 7's
"every remaining level reference" reaches this second doctrine file, so the
Maintainer sees the change named rather than finding it later. (b) Widen the
C6 pattern. Measured today, `grep -rlE "Level[ -][012]|level-[012]-|Level-1-to-2|hand-copy([^i]|$)|[Mm]aturity[- ]ladder|adoption levels?|(pick|choose|which) (an? )?(adoption )?level\b"`,
with the same excludes, returns 31 files: the 29 plus
`bootstrap/tests/test_practice_modules.py` and `doctrine/session-routines.md`.
Every line the added terms match is a true positive. The after-set stays the
same two files. Over `dev/modules/onboarding/`, the widened pattern matches
both Cairn copies before C6 and nothing after.

**[P4] non-blocking — the requested allowance has no landing point.**
*Scope delta* says the narrowed `verify_integrity` criterion "needs the
Maintainer's allowance". No chunk, gate or record point asks for it, though.
The template has this review's fold carry the plan straight to
`ready-to-implement` (`dev/plans/_template.md:35-43`), so C1 would run against
a criterion nobody ratified. *Close:* make the quoted allowance C1's gate,
appended to this plan before C1 runs. Alternatively, argue in *Scope delta*
that no allowance is owed, because item 10's outcome is delivered whole and
only the proposal's acceptance wording narrows. Either way, take the "other
18" figure immediately before C1 rather than carrying today's number forward.

**[P5] non-blocking — C1 leaves the maturity evaluator's helpers behind.**
Some helpers have no remaining consumer once `evaluate_maturity_triggers` is
gone. They are the four `LEVEL_{1,2}_DEEPEN_*_THRESHOLD` constants
(`scripts/_onboarding/triggers.py:41-50`) and the two archived-count helpers
(`:53-72`). Inside the package, nothing else uses them. Outside it, the only
reader is the maturity test that C1 rewrites. All six are re-exported at
`scripts/_onboarding/__init__.py:111-119`, and the completeness grep cannot
see an underscore-and-capitals name like `LEVEL_1_DEEPEN`. *Close:* say in
C1's cell that these six names and their re-exports are deleted with the
evaluator, or say that they stay and why. If they go, [P1]'s fixtures use
literal counts.

**Disposition:** `revising-plan`. Three blocking findings, each closed by an
edit to a cell. The plan's structure, chunk order, frozen set and test
mapping are sound.

## Response to plan review -- Claude (author) -- 2026-10-01

All five findings were verified against the tree before folding (thresholds
5/3 and 15/10 at `scripts/_onboarding/triggers.py:41-50`; 19 dropped nodes in
`collection.node_ids`; every P3 line; the widened grep's 31 files; the helpers'
only consumers). Each is answered in an operative cell; this table points at
them.

| Finding | Disposition | Where |
|---|---|---|
| [P1] negative invariant misses two triggers | accepted | *Acceptance criteria* > C1 — negative invariant: four trees, literal counts |
| [P2] dropped test nodes unaccounted for | accepted | *Verification* > Expected non-pass (the 19, by chunk); the M row; *Dispositions* |
| [P3] level wording outside the cells and the grep | accepted | *Sequence* C2 (four passages, `doctrine/session-routines.md:375`), C4 (`:339`, `:367`), C5 (`:52`, `:159`), C6 (`:48`); *Acceptance criteria* > C2, C6 (widened pattern, 31 before); *Scope fidelity* names the second doctrine file |
| [P4] the allowance has no landing point | accepted, as C1's gate | *Sequence* C1 gate; *Scope delta* (gate, re-measure before C1); *Acceptance criteria* > C1 — lockfile |
| [P5] maturity helpers left behind | accepted, deleted | *Sequence* C1 (constants, count helpers, re-exports) |

From the review's "noticed but not recorded" list, also folded: the launcher
docstring (C1; the eighth frozen file, named in *Scope fidelity*); the whole
deferred-task entry, the "three active-surfacing rows" intro line, and the
render test's stale counts and class name (C1); the one-commit gap between code
and doctrine, now stated (*Sequence*); `test_onboarding_review_tiers.py` in C6's
mapping. Not folded: `docs/vision.md:77` ("the graduated on-ramp"), which
describes the on-ramp as gradual rather than naming a level.

Status `revising-plan` -> `ready-to-implement`. C1 waits on its gate.

## Maintainer allowance -- Anthony Kendall (Maintainer) -- 2026-10-16

The Maintainer's words, quoted **verbatim and visually isolated**:

> "Yes, that's fine, go ahead with C1"

*Scribe's note, separate from the quoted words:* this answers the question put
to the Maintainer in chat on 2026-10-16: whether the accepted criterion
"`bootstrap/verify_integrity.py` passes on Cairn's own tree after the lockfile
re-finalize" may be held to the files this plan changes, as *Scope delta*
describes, given that 18 of the tree's 21 current mismatches are in files this
plan never touches. It satisfies C1's gate. Scribed by Claude
(claude-opus-5-5) on the Maintainer's instruction.
