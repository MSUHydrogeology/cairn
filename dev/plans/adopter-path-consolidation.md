# Plan: retire the adoption levels

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md`
**Status**: ready-to-archive
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

## Implementation verification -- Claude (claude-opus-5-5) -- 2026-10-16

* **Boundary B mode**: full — the change edits eight frozen files covered by
  the gate manifest, a contract surface, so bounded mode refuses.
* **Tested commit**: `9c0e002a6471216641540466ffd9782eb0eb2ff3`
* **Reviewed range**: `c0980506` (the commit before C1) .. `9c0e002a` — C1
  `3b44bc72`, C2 `7e423915`, C3 `e1a9933b`, C4 `6eb5a448`, C5 `5e6cb155`,
  C6 `9c0e002a`.
* **Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` —
  CPython 3.13.13 (conda-forge).
* **Pre-run state**: `HEAD` `9c0e002a`; tracked tree clean; untracked only
  `.claude/` and `dev/measurement/collision_log.md`, both pre-existing and
  outside this plan. No other test run in progress and no active work
  intents.
* **Post-run state**: `HEAD` `9c0e002a`, unchanged; the same two untracked
  paths.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | 0 | 3229 passed; 0 failed, 0 skipped, 0 xfail, 0 xpass; 3 warnings | 692 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality fail=74, info=21; redundancy fail=0 | 1 s |

**Non-pass disposition**

* **Neutrality fail=74 is pre-existing.** The same gate on the pre-C1 tree
  (`c0980506`, extracted with `git archive`) reports 77. The three no longer
  reported were vendor names in the maturity evaluator's docstring, which C1
  deleted. No (file, token) pair is new, and no failure sits on a line this
  plan changed (394 changed lines intersected with 61 failing lines; the
  intersection was checked with a synthetic overlap as control).
* **3 warnings**: a `verify_requirements` deprecation from the third-party
  `stevedore` package in the dev environment; unrelated to this change.
* **`check_cairn`: 1 report, expected.** The plan review cites line 438 of
  `scripts/_onboarding/triggers.py` as of its reviewed commit; C1 shortened
  the file to 355 lines. The review section is the reviewer's and is not
  edited.

**Plan-specific acceptance commands**

* **C1 — negative invariant.** The rewritten test passes on all four trees.
  Restoring each deleted trigger in turn turned it red: `level-0-to-1` 3
  failed, `level-1-to-2` 3 failed, `level-1-deepen` 1 failed, `level-2-deepen`
  1 failed.
* **C1 — registry.** `_ACTIVE_SURFACING_ROWS` has two rows; every row ×
  preset renders a non-empty, distinct body (in the suite above).
* **C1 — twins.** `diff -r --exclude=__pycache__ scripts/_onboarding
  templates/modules/default-on/_onboarding` and the launcher pair print
  nothing.
* **C1 — lockfile.** `verify_integrity --target .` reported 21 findings
  immediately before C1 and 18 after; the three removed are the
  `scripts/_onboarding/` files, none was added, and the launcher was never
  among them. Unchanged at 18 after C6's re-finalize of `triggers.py`.
* **C2 — doctrine matches code.** The trigger ids `doctrine/onboarding.md`
  names equal the ids the code can emit (8 = 8); the completeness pattern
  finds nothing in either doctrine file.
* **C3 — migration note.** Carries the literal `--init-lock` sequence (run on
  a scratch hand-copied tree, 2026-10-01; `bootstrap/_scaffold/` is untouched
  since), the no-upgrades consequence, and the `--force` warning.
* **C4 — quickstart.** `test_quickstart_sequence.py` passes unedited; the
  teardown and the throwaway signature-check waiver are unchanged.
* **C5 — recipe.** `test_presets.py` passes with the canonical-profile block
  byte-identical. The recipe's profile scaffolded into a fresh repository:
  exit 0, eight modules, zero staffability warnings, lockfile written;
  `solo-greenfield`: exit 0, six modules.
* **C6 — completeness.** The plan's pattern returns exactly
  `bootstrap/tests/fixtures/gate_manifest.json` and the rewritten
  `test_trigger_evaluation_maturity.py`; nothing in `dev/modules/onboarding/`.
  Spellings the pattern misses, found during C4–C5 ("Hand-copy", "Cairn
  level"), searched separately: nothing.
* **Manifest.** `scaffold.py --manifest` is byte-identical to `c0980506`'s
  (98 lines).
* **No frozen file deleted.**

**Changed frozen files, for the re-anchor (M)** — filtered from the keys of
`frozen_files`, not transcribed:
`templates/modules/default-on/_onboarding/__init__.py`,
`templates/modules/default-on/_onboarding/prompts.py`,
`templates/modules/default-on/_onboarding/triggers.py`,
`scripts/onboarding_activate.py`,
`bootstrap/tests/test_trigger_evaluation_maturity.py`,
`bootstrap/tests/test_active_surfacing_mechanism.py`,
`bootstrap/tests/test_active_surfacing_render.py`,
`bootstrap/tests/test_practice_modules.py`.

**Test nodes this plan dropped and added**, against the pre-C1 collection
(3,244 → 3,229: 25 dropped, 10 added). All paths under `bootstrap/tests/`.

* C1, dropped — `test_trigger_evaluation_maturity.py`, all 12:
  `TestLevel0to1::{test_fires_after_first_archived_proposal,
  test_does_not_fire_with_no_archived_proposals}`;
  `TestLevel1to2::{test_fires_when_lockfile_present,
  test_does_not_fire_without_lockfile}`;
  `TestLevel1Deepen::{test_fires_at_threshold_without_level_2,
  test_suppressed_when_level_2_also_fires, test_does_not_fire_below_threshold}`;
  `TestLevel2Deepen::{test_fires_when_level_2_and_high_thresholds_met,
  test_does_not_fire_below_level_2, test_does_not_fire_below_high_threshold}`;
  `TestMixedFixture::{test_level_1_install_with_deepen_threshold_fires_two,
  test_template_does_not_count_as_archived_proposal}`.
* C1, dropped — `test_active_surfacing_render.py`:
  `TestTwelveCombinations::test_renders_non_empty_body[<row>-<preset>]` for
  all 9 row × preset pairs (3 for `Level-1-to-2-graduation`; the 6 for the
  remaining rows are renamed, below), and
  `TestPerPresetDistinguishingLanguage::test_level_graduation_drafts_concrete_per_preset_p3_9`.
* C1, dropped — `test_active_surfacing_mechanism.py`:
  `TestPriorityOrder::test_collab_agreement_wins_over_level_graduation`,
  `TestPriorityOrder::test_level_graduation_wins_over_second_agent`.
* C3, dropped — `test_practice_modules.py::TestLadderCorrespondence::test_ladder_levels_match_adoption_levels`.
* C1, added — `test_trigger_evaluation_maturity.py::TestNoTriggerClassifiesAnAdoptionLevel::{test_fresh_install,
  test_activity_states[lockfile-5-3], test_activity_states[no-lockfile-5-3],
  test_activity_states[lockfile-15-10]}`; and
  `test_active_surfacing_render.py::TestEveryRowRendersForEveryPreset::test_renders_non_empty_body[<row>-<preset>]`
  for the 6 remaining row × preset pairs (the rename).

The plan predicted 19 dropped; the other 6 are the renamed cases, which drop
and re-add under the new class name. The committed manifest is older than
this plan: compared with it directly, a further 62 added nodes (and the four
from `a1a58f93`) belong to work already queued for re-anchor, not to this
plan.

**Known omissions**

* The `--init-lock` sequence was exercised on 2026-10-01, not at the tested
  commit; the code path it runs (`bootstrap/_scaffold/`) is unchanged across
  the reviewed range.
* `base_hash` trails `hash` for the four finalized scripts, as for any
  self-hosted verbatim script: `--finalize` advances `hash` only.
* Nothing is re-anchored here; M is the Maintainer's.

## Code review -- Claude (External, fresh-context subagent) -- 2026-10-16

**Model**: claude-opus-5-5

Reviewed commit: 8d500f269294b07c1232f8114876f44f33bec172
Target: the implementation range c0980506..9c0e002a (C1-C6) and its Boundary B record
Prior findings: none

**Tier**: External
**Findings**: raised

**Verdict.** Land it. The strongest rejected alternative, A5 (keep the levels
and redefine them by staffing), gets no support from the code: no engine path
reads a level, and the only onboarding trigger that keyed on the lockfile is
the one C1 deletes. The change would be shown wrong by the signals the proposal
lists, such as adopters asking "which level am I?". Nothing in this range shows
them. I raise three findings, all non-blocking, all on the hand-copy migration
wording.

### The record, checked against the range

I measured each item on `git archive` extractions of `c0980506` and HEAD, or
read-only in the tree, under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13).

* **Eight changed frozen files.** Intersecting `git diff --name-only
  c0980506 9c0e002a` with the keys of `frozen_files` (183 entries; the control
  `templates/modules/default-on/_onboarding/triggers.py` is present) gives
  exactly the record's eight. `test_presets.py` and `test_quickstart_sequence.py`
  are frozen and not edited.
* **Test nodes.** `--collect-only` on both extractions gives 3,244 → 3,229:
  25 dropped and 10 added, with the same node IDs the record lists. All 25
  dropped nodes are pinned in the committed `collection.node_ids`. Base minus
  manifest is 66, which matches the record's 62 + 4.
* **`verify_integrity`.** Base reports 21 findings and HEAD 18. The difference
  is exactly the three `scripts/_onboarding/` files, and the launcher is in
  neither set. The lockfile diff touches only four `hash` lines. The three stale
  hashes attested content from `c8e172a4`. Finalizing now also attests the later
  `30a55d27` and `a1a58f93` edits, which Revision 2 item 10 asks for.
* **Twins.** `diff -r --exclude=__pycache__` over both `_onboarding/` packages,
  and over the launcher pair, prints nothing.
* **Manifest.** `scaffold.py --manifest` gives 98 lines at both commits, and
  `cmp` finds them identical.
* **Neutrality 77 → 74.** Reproduced. Counted per (file, token) pair, the only
  change is three fewer hits in the template `triggers.py`. No pair is new.
* **`check_cairn`.** It reports one issue, the line-438 citation in the plan
  review, as recorded.
* **Bytes after the record.** `9c0e002a..HEAD` changes only this plan.

### Falsification ledger

| Probe | What it would show if the work were wrong | Result |
|---|---|---|
| Restore each deleted `out.add("level-...")` line into the template package (the base `triggers.py`, with the other three neutralised), then run the rewritten test | a restoration the test misses | All four go red: `level-0-to-1` 3 failed, `level-1-to-2` 3, `level-1-deepen` 1, `level-2-deepen` 1. With all four restored, 4 failed. Unmutated control: 4 passed. |
| Each deleted trigger's firing condition against the four fixtures | a trigger condition left uncovered | Every condition is met by at least one fixture: ≥1 archived proposal; a lockfile; no lockfile at 5/3; a lockfile at 15/10. |
| Render both remaining rows through both launchers, from every template preset, from Cairn's `dev/modules/onboarding/collaborative-team.md`, and from the three **pre-change** presets (an existing adopter's installed copy) | a row that no longer renders, or a stale Level section leaking into a body | Every pair renders a non-empty body, and no body contains "Level". `select_active_prompt_to_fire` ignores a stale `level-1-to-2` id. |
| Grep for `evaluate_maturity_triggers`, the `LEVEL_*_DEEPEN` constants, the count helpers, the row name, every `level-*` id and `graduate-to-level`; read the trigger tags in the presets and the manifest's `mapping_symbols` | a consumer still pointing at removed code | Hits only in `CHANGELOG.md` history, archived records, this plan, and `bootstrap/tests/fixtures/gate_manifest.json` (node IDs, which M clears). |
| Run the plan's C6 pattern at both commits. Then run wider sweeps: case-insensitive `level[ -_]?[012]`, `levels? (zero\|one\|two)`, `ladder`, `rung`, `graduat`, `hand-?cop` and `by hand`, and read every prose hit for `\blevels?\b` | a page that still teaches a level | The pattern goes from 31 files to the expected 2, and `dev/modules/onboarding/` from 2 to 0. The wider sweeps find only unrelated senses (`top-level`, `module-level`, the skills table's `level` column) and the on-ramp's own "no rung" sentence. |
| Compare the trigger ids named in the doctrine with the `out.add` ids in the code | doctrine naming a trigger that cannot fire | 8 = 8. |
| Run the rewritten docs' commands at HEAD and check what they cite against the code: `upgrade --help`; `--init-lock` on a tree with `dev/.cairn/` removed and on a tree copied from `templates/core/`; `--adopt-module doc-drift-prevention` on an install; `--summary`, then an install, of the recipe's YAML into a repository that has its own `README.md` and `CHANGELOG.md`; module names against `_MODULE_MAPPINGS`; the readiness report's eleven sections; Act II-3 to II-6 against the installer's printout | a flag, behaviour, name or count the docs get wrong | All hold. `--init-lock` exits 2 with exactly four placeholders, and after they are filled exits 0 and writes a lockfile. `--adopt-module` exits 0 and installs the module's three files. The recipe installs 8 modules with 0 staffability warnings, writes the lockfile, and leaves both of the repository's files untouched. `--force` is documented as an overwrite. |
| The canonical YAML block and the quickstart's pinned phrases | a pinned byte that moved | The block's sha256 is identical at both commits, and both phrases are present. 14 mapped test files (presets, quickstart, profiles, the onboarding family, render, mechanism, maturity, practice modules): 229 passed. |
| What the lockfile does in onboarding once the level triggers are gone | a doc claim about the lockfile that the code no longer supports | **Contradicted**, see [CR1]. |
| What hand-copying `core/` and the modules actually yields, and what a re-install over it does | a doc claim about the hand-copy route that the scaffold contradicts | **Contradicted**, see [CR2] and [CR3]. |

**A fresh full run is not owed.** None of Boundary C's triggers applies:

* the record is valid and in `full` mode;
* it reports 0 skip, 0 xfail and 0 xpass;
* no implementation, test, template or fixture byte changed after it;
* the collection and gate figures above reproduce exactly;
* no unrecorded cross-surface dependency turned up. The manifest's
  `mapping_symbols` names none of the removed symbols.

### Findings

**[CR1] non-blocking: the docs say a tree without a lockfile gets no
onboarding prompts, and the code says otherwise.** `on-ramp/README.md:91-93`
and `templates/README.md:88-92` both say this.

* **Nothing in the onboarding engine reads the lockfile.** `grep -c
  "cairn-lock\|lockfile"` returns 0 for every file in `scripts/_onboarding/`
  and for the launcher. As a control, `PLANNING` or `onboarding-activated`
  matches 39 times in the same package. The one thing that keyed on the
  lockfile was `level-1-to-2`, and C1 deleted it.
* **Probe.** I installed `solo-greenfield`, removed `cairn-lock.yml` and the
  base cache, and added one archived proposal. Running
  `scripts/onboarding_activate.py --dry-run` then activated two tasks and
  printed the `collab-agreement-signing` prompt.
* **What actually stops the prompts.** A kernel copied from `templates/core/`
  gets no prompts because it has neither the helper nor the preset. The
  missing lockfile is not the cause.
* **Where the wording comes from.** The sentence is Revision 2 item 9's own
  wording, and the C3 criterion requires it, so the implementation met its
  criterion. The claim is still one the code contradicts.

*Close:* rewrite both sentences to say only what the code supports. For
example: "receives no upgrades, and lacks the files only the installer adds,
the onboarding helper among them". Or drop "no onboarding prompts". Either way
it changes accepted wording, so name it in the archive dispositions.

**[CR2] non-blocking: `templates/README.md` says hand-copying gives "the
same files" and "the same tree". It does not.** See `templates/README.md:88-95`.

* **Files outside `core/`.** The scaffold delivers always-on files that are in
  neither `core/` nor any module. On a tree copied from `templates/core/` and
  given a lockfile, `upgrade --plan` reports "new core/skills (added) 14".
  Among them are `tools/session.py`, `tools/board.py`,
  `.agents/skills/session-start/SKILL.md` and `scripts/onboarding_activate.py`.
* **Install state.** The scaffold also writes the `dev/.cairn/` state.
* **The page contradicts itself.** The rewritten bullet names one difference
  (no lockfile). The unchanged sentence after it then says the result is the
  same tree.

*Close:* say that the scaffold also installs the session tools, the skills and
the onboarding helper, and records a lockfile. Then drop "Either way the
*result* is the same tree".

**[CR3] non-blocking: for hand-copied trees, the migration section recommends
a re-install that only works with the `--force` the on-ramp forbids.**

* **How the reader gets there.** C3 added hand-copied trees to
  `bootstrap/UPGRADE.md:172-173`, and the on-ramp sends that reader to the
  section for details (`on-ramp/README.md:101-103`).
* **The advice.** The section closes by telling the reader to re-install for
  clean 3-way merges, "so a full lockfile + base cache is written"
  (`bootstrap/UPGRADE.md:185-187`).
* **What a re-install actually does.** Over a hand-copied kernel, a re-install
  without `--force` skips every existing file and writes no lockfile. Probe:
  `[warn] dev/.cairn/cairn-lock.yml NOT written: 9 installed file(s) differ
  from a clean install`, followed by a pointer to `upgrade --init-lock`.
* **The contradiction.** The advice therefore works only with `--force`, which
  `on-ramp/README.md:105-106` says not to use. The tool's own warning redirects
  safely, so nothing is lost, but the two pages disagree on the route this
  change built.
* **Same advice in the tool, out of scope.** The `--init-lock` output carries
  the same re-install advice. It lives in `bootstrap/_scaffold/`, which this
  plan does not touch.

*Close:* qualify the re-install sentence. Over files that differ from a clean
install, a re-install writes no lockfile without `--force`, so a hand-copied
tree keeps the review-only diffs for its token-substituted files.

**Seen but not raised.**

* `docs/vision.md:77` changed even though the plan's Response marked it "not
  folded". Item 7 reaches it, and the C6 commit body names it.
* C5 corrected the default-on roster in all three profile comments and in
  BOOTSTRAP's Act I example, beyond the cited lines. The corrections match
  `_DEFAULT_ON_MODULES`.
* A legacy repository that already has its own `AGENTS.md` gets no lockfile
  from the recipe's install. The scaffold warns and points at `--init-lock`,
  and the recipe's no-overwrite sentence is true.

**Disposition:** `ready-to-archive`. I reproduced every acceptance criterion
and found it met. The three non-blocking findings are on the hand-copy wording,
and each closes with a sentence-level edit.

## Response to code review -- Claude (implementer) -- 2026-10-16

All three findings are non-blocking and were verified against the code before
answering. Each is a prose correction inside an item the plan already
carries; no implementation, test, executable-template or fixture bytes
change, so the Boundary B record stands.

| Finding | Disposition | What changed |
|---|---|---|
| [CR1] "no onboarding prompts" blamed on the missing lockfile | accepted | `on-ramp/README.md`: the accepted words stand, with the true cause — a hand copy lacks the lockfile *and* the installer-added files, including the onboarding helper (no file in `scripts/_onboarding/` reads the lockfile). Added: after `--init-lock`, `upgrade --plan` lists those files as additions and `--stage` / `--apply` bring them in (measured on a scratch hand-copied tree: 14 additions listed) |
| [CR2] a copy by hand is "the same tree" | accepted | `templates/README.md`: a copy by hand is the kernel alone; only the scaffold produces the complete tree |
| [CR3] `UPGRADE.md`'s re-install advice reaches hand-copied trees | accepted | `bootstrap/UPGRADE.md`: the advice does not apply to a hand-copied tree (measured at `995e05c7`: re-install without `--force` skipped 17 files, wrote no lockfile, and kept the adopter's own line) |

Not changed: the same re-install sentence printed by `upgrade --init-lock`
itself, which lives in `bootstrap/_scaffold/` and is outside this plan. It is
dispositioned at archive.

## Code review -- Claude (fresh-context subagent) -- 2026-10-16 -- init-lock note fix

**Model**: claude-opus-5-5

Reviewed commit: f3c839a7f22919b027e11c5f79d37ca2914fcb56
Target: f3c839a7 -- bootstrap/_scaffold/upgrade.py (_cmd_init_lock note) and its test
Prior findings: none

**Findings**: raised

The fix holds. Every claim in the new note is true, the new test fails on the
old message, and the commit touches nothing but the note and the test. I raise
three non-blocking findings. One is about the test. The other two are places
that still give the advice this commit removed, and the first of them now
contradicts the new note.

Every probe ran under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13), in scratch trees and `git archive` extractions outside this
repository. "Copied kernel" below means a fresh git repository holding a copy of
`templates/core/`, given a lockfile by `upgrade --init-lock` once the four
profile placeholders were filled.

### Ledger

| Check | What it would show if the change were wrong | Result |
|---|---|---|
| `upgrade --stage` writes both versions side by side | a migrated file with no pair to merge from | **Holds.** `bootstrap/_scaffold/upgrade.py:866-889` writes `<file>.theirs` (new upstream) and `<file>.ours` (the on-disk copy) into the stage's `review-only/` directory, and the `--plan` next-step line (`bootstrap/_scaffold/upgrade.py:734-738`) says the same. Probe on the copied kernel: 17 review-only files, 17 pairs; `AGENTS.md.ours` is byte-identical to the file on disk. |
| An install over the tree skips every file already there and writes no lockfile | an existing file rewritten, or a lockfile written | **Holds.** The skip is at `bootstrap/_scaffold/install.py:297`; any file that differs from a clean install refuses the lockfile (`bootstrap/_scaffold/install.py:1787`, `:1812`). Probe on the copied kernel, no `--force`: 17 `[skip]` lines, `cairn-lock.yml NOT written: 9 installed file(s) differ`, the migrated lockfile's sha256 unchanged, and `git diff` shows only two lines appended to `.gitignore`. Its one limit: a lockfile *is* written when every tracked file still matches a clean install of the running Cairn. No adopter with a reason to upgrade has such a tree; one edited line is enough to miss it (see [IL2]). |
| `--force` overwrites edits | an adopter's line surviving `--force` | **Holds.** A committed marker line in `AGENTS.md` is gone, and git shows the 9 files that differed rewritten. `--force` also writes a full lockfile, so the note is right to present it as the cost, not the route. |
| The new test can fail | a test that stays green on the old message | **Holds.** With the message restored byte-for-byte to the parent's (an extraction of `f3c839a7`), `TestInitLock` gives 1 failed (the `re-install` assertion) and 4 passed. Unmutated: 5 passed. |
| The defect-repair conditions | other bytes in the commit, or more than one changed engine symbol | **Hold.** Two files changed, 6 and 21 lines. The runbook's read-only Step 1 snippet gives CHANGED 1 (`FunctionDef:_cmd_init_lock`, `a6fbdd4d4104cf53` to `ca185206bd3910b7`), MISSING 0, DUPLICATE 0, NEW 86 at `f3c839a7`, and CHANGED 0, NEW 86 on the parent's engine bytes. The engine family the commit names: 329 passed. One of its tests upgrades `--to HEAD`, which needs git metadata, so it ran in a git-initialised extraction. |
| Other places giving the same advice | a page or message that still sends the adopter to a re-install that cannot work | **Found**, see [IL2] and [IL3]. The `--finalize` error's "fix or re-install first" (`bootstrap/_scaffold/upgrade.py:1855`) is sound: it concerns missing files, and a plain install does restore those. |

### Findings

**[IL1] non-blocking: the test forbids one spelling of the advice.**
`bootstrap/tests/test_upgrade.py:956` asserts `"re-install" not in out.lower()`.
The property its docstring names is wider: the note never advises reinstalling.
Probe: in an extraction, I replaced the note's last sentence with "For clean
merges, reinstall from an upgrade-capable Cairn." and kept the `--stage` clause.
`TestInitLock` gave 5 passed. *Close:* strip hyphens before matching
`reinstall`, or also assert the sentence that warns against installing over the
tree.

**[IL2] non-blocking: `bootstrap/UPGRADE.md` still recommends the re-install,
and now contradicts the note.**

* **The page.** `bootstrap/UPGRADE.md:185-190` keeps the re-install for
  scaffold-installed trees and exempts only hand-copied ones. That carve-out
  was the answer to [CR3].
* **The code draws no such line.** The install skips a file because it exists,
  and refuses the lockfile because a file differs. How the tree was made does
  not enter.
* **Probe.** I ran a scaffold install, deleted the lockfile and base cache to
  match a tree installed before upgrade support, and appended one line to
  `dev/NEXT_SESSION.md`. A re-install without `--force` printed `1 installed
  file(s) differ from a clean install (dev/NEXT_SESSION.md)` and wrote no
  lockfile.
* **The contradiction.** The note prints for every migrated tree and says not
  to install over it. The page that explains the note still says to.
  `bootstrap/fidelity-check.md:106-108` offers the same route, "or re-installs
  from an upgrade-capable Cairn", as an alternative to `--init-lock`.

*Close:* make both say what the note says, for every pre-lockfile tree. This is
prose only.

**[IL3] non-blocking: the vendor-wrapper warning in `--init-lock` gives the
same advice.**

* **The warning.** It reads "Rename it to a known vendor filename or
  re-install from an upgrade-capable Cairn"
  (`bootstrap/_scaffold/upgrade.py:1224-1225`).
* **Why neither remedy works.** The warning prints in the same run that writes
  the migrated lockfile, and `--init-lock` refuses to run once a lockfile
  exists (`bootstrap/_scaffold/upgrade.py:1167`).
* **Probe: re-install.** On a copied kernel with no wrapper, a re-install
  without `--force` wrote a fresh `VENDOR.md` but no lockfile, so the lockfile
  still has no wrapper record. The next `upgrade --plan` lists `VENDOR.md` as a
  BLOCKED new core file. That is worse than before the re-install.
* **Probe: rename.** A `CLAUDE.md` wrapper added after the run leaves the
  lockfile unchanged, and `upgrade --plan` offers to add `VENDOR.md`.

Neither remedy tracks the wrapper unless the adopter deletes the migrated
lockfile and runs `--init-lock` again. It is the same defect, in an engine file
this commit did not touch. *Close:* a separate repair with its own failing
test, or the archive dispositions.

**Seen but not raised.**

* For a review-only file, the staged `.theirs` is the raw template:
  `AGENTS.md.theirs` keeps its three `{{...}}` placeholders, although the
  migrated lockfile records the profile's token values. This predates the
  commit and does not make the note false.
* Over a migrated tree, the install's own refusal (`bootstrap/_scaffold/install.py:1812`)
  points at `upgrade --init-lock`, which then reports that a lockfile already
  exists. Nothing is written either way.

**Disposition:** the fix stands, and the plan stays `ready-to-archive`. [IL1]
is a small test tightening. [IL2] and [IL3] belong with the archive
dispositions, next to the residual of [CR3].
