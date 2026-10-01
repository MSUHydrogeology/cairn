# Plan: retire the adoption levels

**Source proposal**: `dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md`
**Status**: awaiting-plan-review
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
| C1 | **Delete the level triggers and the graduation prompt.** In `scripts/_onboarding/` and its twin `templates/modules/default-on/_onboarding/`: `evaluate_maturity_triggers` and its four triggers (`triggers.py`), its export (`__init__.py`), its call in the union evaluator, and the `Level-1-to-2-graduation` row (`prompts.py`). In the three `templates/onboarding/*.md` presets and Cairn's copy `dev/modules/onboarding/collaborative-team.md`: the `### Row 2 -- Level 1→2 graduation prompt` sections and the `[trigger: level-1-to-2; ...]` tag; the remaining rows keep their heading labels. Tests: `test_trigger_evaluation_maturity.py` is rewritten to pin the negative invariant; `test_active_surfacing_mechanism.py` and `test_active_surfacing_render.py` drop the row. Scoped lockfile finalize for the three `scripts/_onboarding/` files in the same commit. | `ready-to-implement` | one commit |
| C2 | **Doctrine.** `doctrine/onboarding.md`: remove the maturity-ladder trigger kind (`:62-77`) and its claim to observe the on-ramp; the active-surfacing section's three named rows (`:118-123`) become two. | C1 | one commit |
| C3 | **The on-ramp.** `on-ramp/README.md` rewritten: read it or install it; choosing a profile; growing an install (`scaffold.py upgrade --adopt-module <name>`); the migration note (Revision 2 item 9). `bootstrap/UPGRADE.md` gains one line naming hand-copied trees in "Migrating a tree installed before upgrade support". `TestLadderCorrespondence` removed. | — | one commit |
| C4 | **Entry pages.** `README.md` (the three-level block and `:266`); `docs/getting-started.md` (`:4`, `:84-86`); `docs/quickstart.md` (real-install statement, the real route in "What to do next", the level summary at `:350-353` removed, `NOTICE.md` added to `:194`, "Time: ~30 seconds" at `:296` removed). | C3 | one commit |
| C5 | **The install route.** `docs/solo-legacy-recipe.md` ("Which level" removed; scaffold route; roster corrected to eight); the three `bootstrap/profiles/*.yml` header comments; `bootstrap/BOOTSTRAP.md` (`:7`, `:231`); `bootstrap/prompts/bootstrap-lite.md`; `templates/codebase-readiness-report.md` (`:340-347`, scores map to how small to start). | C3 | one commit |
| C6 | **Every remaining reference.** `templates/README.md` (`:82-86`); both example READMEs; `docs/agent-team-onboarding.md:9` and Cairn's copy `dev/modules/onboarding/agent-team-onboarding.md`; `docs/workflow-role.md:83`; `docs/further-reading.md:30`; any level wording left in the presets and Cairn's copies. Ends with the completeness grep. | C1–C5 | one commit |
| C7 | **Boundary B**, then `## Implementation verification`; status → `awaiting-code-review`. | C6 | one commit |
| M | **MAINTAINER-ONLY — the gate-manifest re-anchor.** This plan's changed frozen files join the batch already queued in `dev/PLANNING.md`, as Revision 2 item 10 specifies; the re-anchor runs with that batch, per `bootstrap/REANCHOR_RUNBOOK.md`. **An implementing agent must not perform it.** The agent's part is the board update at archive. | code review cleared | Maintainer |

The chunks are ordered so that code and doctrine agree at every commit (C1 then
C2), and the one test that pins the old ladder leaves in the commit that removes
the ladder (C3).

## Acceptance criteria

* **C1 — negative invariant.** The union trigger evaluator returns no id
  beginning `level-` on a fresh `solo-greenfield` install, nor on a tree with a
  lockfile, five archived proposals and three archived plans. Rewritten
  `test_trigger_evaluation_maturity.py` asserts both, and fails if any one of
  the four deleted `out.add("level-...")` lines is restored.
* **C1 — the prompt registry.** `_ACTIVE_SURFACING_ROWS` has two rows; every
  preset × remaining-row pair still renders a non-empty body
  (`test_active_surfacing_render.py`).
* **C1 — twins.** `diff -r --exclude=__pycache__ scripts/_onboarding
  templates/modules/default-on/_onboarding` prints nothing.
* **C1 — lockfile.** `python bootstrap/scaffold.py upgrade --finalize
  scripts/_onboarding/triggers.py scripts/_onboarding/prompts.py
  scripts/_onboarding/__init__.py --target .` runs in the C1 commit. **The tree
  does not pass `verify_integrity` today**: `python bootstrap/verify_integrity.py
  --target .` exits 1 with 21 hash mismatches (measured 2026-10-01), and all
  three `scripts/_onboarding/` files are among them, left by earlier unfinalized
  changes. So the criterion is the drop, not a pass: after C1 it reports no
  `scripts/_onboarding/` finding, and the other 18 are unchanged.
* **C2 — doctrine matches code.** Every trigger id named in
  `doctrine/onboarding.md` is one the trigger evaluators can return, and none
  begins `level-`.
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
* **C6 — completeness.** `grep -rlE "Level [012]|level-[012]-|Level-1-to-2|hand-copy([^i]|$)"
  --exclude-dir=dev --exclude-dir=.git --exclude-dir=.claude
  --exclude=CHANGELOG.md .` returns 29 files before C1 (positive control) and,
  after C6, only `bootstrap/tests/fixtures/gate_manifest.json` (cleared by M)
  and the rewritten `test_trigger_evaluation_maturity.py` (names the retired
  ids on purpose). The same pattern over `dev/modules/onboarding/` returns
  nothing.
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
is stale for the seven changed frozen files, which a green run does not show
(`AGENTS.md` > Operational pitfalls). The record lists the seven by path.

**Boundary C** is the code reviewer's. Attack at least: the negative invariant
(restore one `out.add` line and confirm the test fails); the completeness grep's
before-set; and whether any remaining onboarding prompt still renders.

**Security preflight.** N/A, as in the proposal: no trust boundary added,
moved, or widened. The chunking changes no answer.

## Dispositions

*Filled at archive-preparation.* Expected: F8 is already deposited
(`9276833c`); at archive, this plan's seven changed frozen files are added to
the queued re-anchor row in `dev/PLANNING.md`, which Revision 2 item 10
authorizes; and `CHANGELOG.md` > Unreleased gets one entry for the retired
levels.
