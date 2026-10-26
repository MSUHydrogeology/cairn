# Onboard at install: retire the delayed onboarding prompts

**Author**: Claude Sonnet 5.5 (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-26
**In brief**: Cairn's follow-up onboarding prompts, which were meant to appear later after a trigger, have never appeared, so this removes that machinery and moves what the prompts said into the short day-one task list the install already writes, without making that list or the install report meaningfully longer.

**The Maintainer's direction**, chat, 2026-10-26, relayed to me by the coordinating session. His words, in the order the board row "Onboarding happens at install" in `dev/PLANNING.md` quotes them:

> "I don't know why we have delayed prompts at all. They should onboard when we onboard!"

> "I don't want them delayed. I want them fixed so that they actually happen when someone installs Cairn."

> "This belongs in v 0.5. Please write the proposal and coordinate with the Cairn v0.5 Planning session"

**Authoring tier.** Proposal authoring is medium (`AGENTS.md:194-201`). I wrote this at Sonnet 5.5, which is medium, so no floor is lowered. The Security Review and the proposal review stay at high.

## In brief

### Your decisions

Five questions. Each has my default; an unanswered question takes it.

1. **Where do the former prompts show up at install?** *Default:* in the list the install already writes into `dev/PLANNING.md` (section "Onboarding"), with no new tasks, plus one new line at the end of the install report that says where the list is. The nine former prompts become five short sentences added to tasks already on the list. Three need no new text because the install already says the same thing, and one repeats another. The list grows by 9, 29 and 38 words for the three profiles (4%, 6% and 7%), and the report by one line (142 to 186 lines today). *Alternatives:* print the prompts in the report, which lengthens the first thing a new adopter reads; or show open tasks whenever a session starts, which edits the module that holds the interpreter binding and needs its own Security Review.
2. **Do you agree with what I do with each of the nine?** The table in Context gives them one by one. Two findings are stale. First, the two "first cross-agent review shipped" prompts (rows 6 and 7): their trigger fires on word matches, and their idea of a cross-agent review predates the rule that only you call one. I rewrite the legacy one and rely on the install's existing text for the other. Second, one clause in row 3, "the second through fifth shape the steady-state", for which I found no measurement; I drop that clause and keep the rest. *Default:* yes to all nine as tabled.
3. **What are existing installs told?** *Default:* nothing is pushed into their files. `upgrade --plan` prints one new informational line, `removed-upstream 9: ...` (measured on a rehearsal). `bootstrap/UPGRADE.md` gets a short section and the changelog an entry. The section says: leave the nine old files alone (they do nothing unless someone runs them); do not delete them, because deleting makes `upgrade --finalize` refuse and `verify_integrity` fail (measured); the new day-one tasks are for new installs, and a project that wants them can copy them from the profile's file in Cairn. *Alternatives:* say nothing (the line would be unexplained); or teach `upgrade` to remove an untouched copy of a file Cairn stopped shipping, which is new engine logic with its own Security Review. I would queue that as its own board row, because nine files make this trap larger than the one file in the 0.4 removal.
4. **Shrink or delete `doctrine/onboarding.md`?** *Default:* shrink it in place, from 327 lines to about 80 (my estimate): the install-time model, the tour pages, the unrelated section "Dispatching an agent session" unchanged, and the cross-references. *Alternative:* delete the file and move "Dispatching an agent session" into `doctrine/roles.md`; that edits a second doctrine file for no gain I can name.
5. **Is your direction the origin of this change, so the rate-limit gate is not engaged?** *Default:* yes; the Decision records your answer in one line. I ask for no edit to the gate. Same question as in the model-tier proposal, which you answered yes.

### What I found

* **Nothing has ever run the helper.** I found no skill, tool, script, git hook or CI file that calls it. The activation log has had one commit, on 2026-06-12, and no commit has ever added an activation line to it (136 days). The doctrine tells the goodnight owner to run it (`doctrine/session-routines.md:362-393`); nobody does.
* **The mechanism is larger than the helper script.** It is 9 verbatim files, 1,964 lines, installed into every adopter, plus a copy of each in Cairn's own tree. It reaches 16 symbols of the scaffold engine, 15 frozen files to delete and 12 to edit, and the published install manifest (96 rows now, 87 after).
* **The nine former prompts need very little text at install.** Three say what the install already says. One repeats another. Five become one sentence each.
* **The upgrade is safe on a rehearsal, with one trap.** On a scratch install, `upgrade --plan`, `--stage`, `--apply` and `--finalize` all exit 0 and leave the nine old files in place. If the adopter deletes them, `--finalize` exits 1 even with `--force`.
* **Headers.** `Review: usual + Security Review`, because the change edits the scaffold engine, the published install manifest and `bootstrap/SAFETY.md`, each named in `AGENTS.md` ("High-risk surfaces") or in the proposal template's triggers. A plan is needed. The lane is deliberate.
* **What I could not show** is listed at the end of Context.

## Context

**Terms.** A *profile* is a named install shape (`solo-greenfield`, `collaborative-team`, `high-rigor-legacy`); the config key is `preset`. A *seed task* is a day-one line the install writes into the `onboarding-tasks` slot of `dev/PLANNING.md`. A *delayed prompt* is a line marked `[trigger: ...]` in a profile's file, or a terminal prompt (a "Row 1" section), that the *helper* (`scripts/onboarding_activate.py`) is meant to show later, when its trigger is true. A *frozen file* has its hash pinned in `bootstrap/tests/fixtures/gate_manifest.json`; changing one needs your *re-anchor* (the supervised ceremony in `bootstrap/REANCHOR_RUNBOOK.md`). The *AST baseline* is the committed fingerprint of the engine's top-level definitions (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`). The *lockfile* (`dev/.cairn/cairn-lock.yml`) records, per installed file, where it came from and its hash. `removed-upstream` is the upgrade's word for a tracked file Cairn no longer ships.

**The design today** (`doctrine/onboarding.md:24-28`, `:61-111`). The install writes seed tasks. It also copies the full profile file to `dev/modules/onboarding/<profile>.md` and installs the helper and an empty log. At each goodnight the helper is meant to read seven triggers (`scripts/_onboarding/triggers.py:271-318`), move any matching delayed task into `dev/PLANNING.md`, print at most one terminal prompt, and append a line to `dev/.cairn/onboarding-activated.jsonl`. The caps are one prompt and three tasks per goodnight (`scripts/_onboarding/prompts.py:30-33`).

**Measured today (2026-10-26, interpreter 3.13.13, HEAD `1d5a047b`).**

* **Nothing runs it.** `git grep -l -i "onboarding_activate\|_onboarding"` over `tools`, `.agents` and `templates/skills` returns 0 files; the same pattern over `templates/modules/default-on` returns 6, so the pattern can match. No file in `scripts/` outside the helper names it. `.git/hooks` holds only `post-commit` and `pre-commit`, and neither mentions onboarding; `.github/` holds issue and pull-request templates and `labels.yml`, no workflow. Every instruction to run it is prose: `doctrine/session-routines.md:362-393`, `doctrine/onboarding.md:202-219` and the helper's own description (`scripts/_onboarding/cli.py:462-463`).
* **The log is empty.** `dev/.cairn/onboarding-activated.jsonl` is 303 bytes: five comment lines. It has one commit, `7519c5da` (2026-06-12, the self-hosting commit). `git log -p` over it adds 0 lines starting `{`; the same command over a file that holds JSON (`dev/reviews/2026-07-11-first-session-internal-panel.json`) adds 1, so the count can see one. The helper has never written a delayed-task id into Cairn's `dev/PLANNING.md`: `git log -S` over that file finds `post-first-proposal` only in the 0.5 board row (`1e7a3e7c`) and `spin-up-second-agent` nowhere, while the same search finds the seed id `try-session-start-skill` (control, `7519c5da`).
* **Two prompts are pending in Cairn's own tree.** `python scripts/onboarding_activate.py --dry-run` lists `post-first-proposal-team` (trigger: first proposal archived; `dev/proposals/archive/` holds 87 files) and `post-first-cross-type` (trigger: first cross-type review). The dry run wrote nothing: the log is still 303 bytes and `git diff` over `dev/.cairn` and `dev/PLANNING.md` was empty. Its last line says "log appended: 2 line(s)"; that counts what it would write.
* **Seven triggers are coded, three are used.** The helper evaluates seven (`scripts/_onboarding/triggers.py:271-318`); the profile files use three: first proposal archived, second agent type, first cross-type review (`grep -h "^\* \[trigger" templates/onboarding/*.md`: six tasks). One terminal prompt row exists (`scripts/_onboarding/prompts.py:22-24`).
* **The mechanism has needed repair before.** `30a55d27` (2026-08-28) retired a trigger that could never fire and made its task a day-one seed. `3b44bc72` (2026-10-16) deleted four level triggers that fired on states carrying no such meaning. `2cc6b260` (2026-10-19) retired the signing prompt with the collaboration agreement.

**What the install does today with onboarding** (measured on three scratch installs in a scratch directory, `python bootstrap/scaffold.py --config bootstrap/profiles/<profile>.yml --non-interactive`, 2026-10-26):

| | solo-greenfield | collaborative-team | high-rigor-legacy |
|---|---|---|---|
| Seed tasks in the `onboarding-tasks` slot | 6 | 10 | 11 |
| Slot size, non-blank lines / words | 29 / 209 | 61 / 451 | 72 / 508 |
| Install report, lines (includes one provenance warning that a release checkout would not print) | 142 | 183 | 186 |
| Slots the report lists to fill | 20 (+2 listed apart) | 23 | 23 |

The report prints no seed text. It prints the line "Installing progressive onboarding (...)" near the top (`bootstrap/_scaffold/cli.py:564-587`) and ends with a fixed "Next steps" block (`bootstrap/_scaffold/install.py:1727-1733`). It names the onboarding tasks once, inside the work-intent hooks note (`bootstrap/_scaffold/cli.py:734`). The model-mapping reminder reaches the adopter twice: a nine-line `NOTE (model-selection)` in the report (`bootstrap/_scaffold/install.py:859-869`) and the seed `fill-model-selection-mapping` (collaborative and legacy profiles). **So the install already delivers its important items at install, and in two places; nothing of that kind exists for the nine former prompts.**

**The seeds are written but not shown again.** `python tools/session.py session-start` in a scratch collaborative-team install printed no onboarding task, and `git grep -i onboarding` over `templates/skills`, `tools` and `.agents` returns nothing. A new session sees the list only if it opens `dev/PLANNING.md`. Cairn's own list shows what that costs: the 2026-06-12 copy held 8 seeds (`git show 7519c5da:dev/PLANNING.md`); today it holds 6. One was completed (the hooks task) and one was retired with the signing prompt. This is not a fair rate, because Cairn's maintainers already know the material, but it shows the list is not a prompt. That is why Question 1 adds one line to the install report.

**The nine former prompts, one by one.** Line numbers are in `templates/onboarding/`.

| # | Former prompt (file:line; fired by) | What it says | True today? | Where it lands at install |
|---|---|---|---|---|
| 1 | `post-first-proposal` (`solo-greenfield.md:58`; first proposal archived) | `strategy/` and `reflections/` are the next places to explore | Yes | No new text. `docs/dev-tour.md:41-55` covers both, and all three profiles seed the tour |
| 2 | `post-first-proposal-team` (`collaborative-team.md:91`; same) | Same, and reflections are gitignored by default, so track them only if agents hand work through them | Yes; the install seeds the ignore entry and the tour says so (`docs/dev-tour.md:52-55`) | Clause B, on the seed `walk-dev-tour` |
| 3 | `post-first-proposal-legacy` (`high-rigor-legacy.md:104`; same) | Calibrate the security-review, dual-language-tests and legacy-agent modules; "the first cycle is the diagnostic; the second through fifth shape the steady-state" | The first part, yes. I found no measurement behind "second through fifth" | Clause D, on the seed `walk-dev-tour`, without the second part |
| 4 | `spin-up-second-agent` (`solo-greenfield.md:65`; roster lists two agent types) | A second agent type would help; fresh sessions already do every review; walk the adoption page | The advice matches today's review rule. The premise "you are at the point" cannot hold at install | Clause A, on the seed `skim-coordination-doctrine`, as "when you add one" |
| 5 | Row 1 prompt, solo (`solo-greenfield.md:87`; same trigger) | The same message as row 4 | Same as row 4 | Clause A again; no separate text |
| 6 | `post-first-cross-type` (`collaborative-team.md:97`; a review names a different vendor than the author) | "Your first cross-agent-type review just shipped ... ask for it again when you want more distance; a fresh session remains the usual review" | **Stale** in its trigger and its reader; the advice still matches | No new text. `templates/core/AGENTS.md:91-108` says it; the seed `fill-team-roster-day-one` (`collaborative-team.md:82`) says a read the Maintainer calls can be staffed; and the seed `read-dual-review-module` (`collaborative-team.md:61`) points at the module that staffs it |
| 7 | `post-first-cross-type-legacy` (`high-rigor-legacy.md:111`; same) | The same, and a different agent type is useful distance on a protected change | **Stale**, as row 6 | Clause E, on the seed `agent-team-onboarding-legacy`. The legacy profile has no `read-dual-review-module` seed, so this one needs text |
| 8 | Row 1 prompt, collaborative (`collaborative-team.md:124`; second agent type) | Walk the adoption page; a second type makes a more distant read available | Yes | Clause C, on the seed `fill-team-roster-day-one`, which always shows. The seed `agent-team-onboarding` (`collaborative-team.md:74`) shows only when the team has several agent types |
| 9 | Row 1 prompt, legacy (`high-rigor-legacy.md:142`; same) | Walk the adoption page; calibrate the second type against the security-review bar | Yes | No new text. The seed `agent-team-onboarding-legacy` (`high-rigor-legacy.md:92`) says it |

**Why rows 6 and 7 are stale.** The helper calls a review "cross-type" when a name from its vendor list appears in the review heading or its first ten lines and differs from the author's (`scripts/_onboarding/triggers.py:207-232`). Today an External read is one the Maintainer called, recorded with a `Called by` line, and a roster the Maintainer sets adds no read (`templates/core/AGENTS.md:93-108`). The two ideas differ. I tested the detector. A file with a Codex reviewer and a Claude author fires it (control). A file with two Claude passes and no other words does not (control). A file with two Claude passes whose review text says "continue" and "metadata" fires it, because the vendor list matches substrings (`continue`, `meta`, `google` and `gpt` among them, `scripts/_onboarding/triggers.py:44-55`). In Cairn's own tree 62 of 153 proposal and plan files fire it. I did not read those 62 to split real cross-vendor reviews from word matches.

**The five sentences** (word counts by `wc -w`; the plan may polish wording but not add tasks):

* **A** (solo; appended to `skim-coordination-doctrine`, 9 words): "When you add a second agent type, walk `dev/modules/onboarding/agent-team-onboarding.md`."
* **B** (collaborative; appended to `walk-dev-tour`, 17 words): "Reflections are gitignored by default; track them only if agents hand work to each other through them."
* **C** (collaborative; appended to `fill-team-roster-day-one`, 12 words): "When you add another agent type, record it there and walk `dev/modules/onboarding/agent-team-onboarding.md`."
* **D** (legacy; appended to `walk-dev-tour`, 18 words): "Treat that first proposal as the diagnostic for calibrating the security-review, dual-language-tests and legacy-agent modules against your tree."
* **E** (legacy; appended to `agent-team-onboarding-legacy`, 20 words): "A read from the second type is the Maintainer's call (`AGENTS.md` > Review); the usual review stays a fresh session."

Added words: solo 9 of 209 (4%), collaborative 29 of 451 (6%), legacy 38 of 508 (7%). Added report lines: 1 of 142, 183 or 186.

**The inventory.** I searched `git grep -lI -i -E` at HEAD `1d5a047b` for `onboarding_activate`, `onboarding-activated`, `first-proposal-archived`, `first-cross-type-review`, `first-foldback`, `\[trigger:`, `active[- ]surfacing`, `doctrine/onboarding.md`, `_onboarding`, `deferred[- ]task`, then for `second-agent-type`, `progressive onboarding`, `onboarding-tasks`, and a few symbol names. Each pattern was first run against a file known to hold it (one control failed because I chose a file that does not contain its own path; I re-ran it against `scripts/_onboarding/cli.py` and it matched). The tests the names do not reach I found by reading, and one more by its row-count pin (`bootstrap/tests/test_notice_install.py:184`). Result: **119 files hit, 52 of them records I leave alone** (45 archived proposals, plans and strategy notes; the changelog; four review records; the consolidation table; one measurement note), and **67 live files**. A 68th, `test_notice_install.py`, I found by its row-count pin, and I also edit `bootstrap/UPGRADE.md`, which no search hit:

| Group | Files | What happens |
|---|---|---|
| Shipped helper, as installed into adopters | 9 (`templates/modules/default-on/onboarding_activate.py`, 88 lines, and 8 files in `_onboarding/`, 1,876 lines) | Deleted. They install as `scripts/onboarding_activate.py` and `scripts/_onboarding/*.py` |
| Cairn's own copies | 9 in `scripts/`, byte-identical to the shipped ones (`cmp`, all nine) | Deleted. Cairn's lockfile keeps nine orphan records, as it already does for the collaboration agreement |
| Profile files | 3 in `templates/onboarding/`, plus Cairn's installed copy `dev/modules/onboarding/collaborative-team.md` | The six `[trigger:]` items and three Row 1 sections go; the preface is rewritten; five sentences added. The installed copy is deleted: its only reader was the helper |
| Doctrine | `doctrine/onboarding.md`, `doctrine/session-routines.md` | See Proposal 4 |
| Docs and templates | `docs/agent-team-onboarding.md` and its installed copy, `docs/vision.md:78`, `on-ramp/README.md:92-97`, `templates/core/dev/PLANNING.md:31-47`, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `bootstrap/UPGRADE.md` (a new section and line 75), `bootstrap/AST_BASELINE_RUNBOOK.md` (mentions `install_onboarding`, which stays) | Reworded as Proposal 4 says. `dev/PLANNING.md` mentions the files only on the board; I do not edit it |
| Scaffold engine | `config.py`, `install.py`, `upgrade.py`, `cli.py`, `__init__.py`, `slotmerge.py` (comment only) in `bootstrap/_scaffold/`, and `bootstrap/security_check.py` | 16 symbols; see below |
| Tests | 21 files by name, plus `test_notice_install.py` | See below |
| Fixtures | `gate_manifest.json`, `scaffold_ast_baseline.json`, `scaffold_ast_known_new.json` | Re-anchored at the cut |
| State | `dev/.cairn/cairn-lock.yml`, `dev/.cairn/claim-check-allow.json` (lines 32, 33, 64, 198-202, 277), `dev/.cairn/onboarding-activated.jsonl` | The log is deleted; the allow-config loses retired entries; the lockfile is tool-owned and never hand-edited |

**The engine: 16 symbols.** Found by reading the files and parsing their top-level names, not by running the attest tool on a change that does not exist yet.

* **Deleted, 8.** In the baseline: `_ONBOARDING_HELPER_SRC_REL`, `_ONBOARDING_HELPER_DST_REL`, `_ONBOARDING_LOG_REL` and `_ONBOARDING_LOG_HEADER` (`bootstrap/_scaffold/install.py:1195-1210`). In the known-new manifest: `_ALWAYS_ON_MAPPINGS` (`config.py:684-703`), `missing_always_on_sources` and `assert_always_on_complete` (`install.py:1222-1279`), and `_always_on_group_complete` (`upgrade.py:322-334`).
* **Changed, 8.** In the baseline: `install_onboarding` (`install.py:1282-1503`), `install_manifest`, `write_install_lockfile`, `_compute_upgrade` and `main`. In the known-new manifest: `_assert_mapping_ownership`, `_cmd_adopt_collisions`, and a docstring in `duplicate_destinations`.
* **Already owed, so no addition:** `main` and `print_report` are already in the set the engine batch owes, so the one report line adds no symbol.
* **Not attested:** `bootstrap/security_check.py` (`scan_targets`, `:683-755`) is frozen but not AST-attested.
* **What the tool prints today:** the read-only `bootstrap/tests/_ast_attest.py verify` on the committed tree lists 10 changed symbols and 3 known-new with changed bodies, which is the owed set on the board row "Re-anchor the gate manifest". Mine would add to it.
* **Who corrects it:** self-service repair reaches only `install_onboarding`, and only when it is the only changed symbol. A deleted pinned key is refused outright (`bootstrap/tests/_ast_attest.py:143-148, 321-334`). So the correction is Maintainer-run, in the single 0.5 re-anchor.

**Frozen files and tests.** The gate manifest lists 195 frozen files and pins 4,612 test nodes (`collection.node_count`). By name this change touches 32 frozen files and, by the row-count pin, a 33rd:

* **Deleted, 15:** `scripts/onboarding_activate.py`; the eight `templates/modules/default-on/_onboarding/*.py`; and six test files: `test_active_surfacing_mechanism`, `test_active_surfacing_render`, `test_deferred_task_store`, `test_onboarding_activation_helper`, `test_trigger_evaluation_action`, `test_trigger_evaluation_maturity` (in `bootstrap/tests/`). Together the six drop 77 collected nodes (8, 10, 6, 31, 18 and 4, from the manifest's `node_ids`). The template launcher (`templates/modules/default-on/onboarding_activate.py`) is not frozen but is listed as phase-mutable (`bootstrap/tests/_gate_manifest.py:110`); that entry goes.
* **Edited, 12:** `bootstrap/security_check.py`; `bootstrap/tests/_gate_manifest.py`; `scaffold_ast_known_new.json`; and in `bootstrap/tests/`: `test_agreement_retired` (it imports the helper's trigger code), `test_facade_loader_cleanup` (one row of its facade list), `test_gate_manifest` (line 74 asserts the launcher is not frozen), `test_hardening` (loads the launcher at `:149`), `test_onboarding_slot_substitution`, `test_review_stance_in_shipped_files` (its exemption for `doctrine/onboarding.md` at `:1890` and the control at `:1982`), `test_security_check` (`:336`, the always-on loop), `test_upgrade_side_door_parity` and `test_notice_install` (`:184`, 96 becomes 87).
* **Mention the mechanism but need no edit, 6:** `_ast_attest.py` (comments; `install_onboarding` stays on its allowlist), `test_install_module`, `test_module_merge_lockfile`, `test_onboarding_seed_roster`, `test_security_leaf` and `test_skills_onboarding` (its seeds are not triggers, which stays true).
* `test_upgrade_side_door_parity` guards two things. One is the completeness group, which goes with it. The other is general: a new tracked file that lands on a path the adopter already occupies must not overwrite it, and the tests use the launcher as the example. I re-point those tests at another tracked file; I do not delete them, or the general protection loses its tests.

Deleting frozen files and dropping nodes show up as `FROZEN-MISSING` and `COLLECTION-DROPPED` until the re-anchor. The 0.5 cut already includes one re-anchor (the board row "Re-anchor the gate manifest" owes it), so these join it.

**The install contract.** The published manifest (`python bootstrap/scaffold.py --manifest`) has 96 rows, nine of them these files (all `verbatim`); it will have 87. The lockfile schema does not change; new lockfiles simply carry nine fewer records. I searched `bootstrap/fidelity-check.md` for the file names and found none, so the fidelity manifest does not change. I found one row-count pin (`test_notice_install.py:184`), by searching the tests for the numbers 95 to 97 with a pattern that matched the known pin.

**Existing adopters.** Two adopter projects exist. I did not read either, as instructed. I do not know whether their lockfiles hold the nine records; an install since the side-door-parity change does (`CHANGELOG.md:1069-1093`), an older one does not and would see no new line. I rehearsed the upgrade on a scratch collaborative-team install (`cp` of a fresh install), against a scratch copy of the engine with the nine templates deleted and `_ALWAYS_ON_MAPPINGS` emptied. That copy is not the real change; it tests only what upgrade does with a file Cairn stops shipping.

* `upgrade --plan` printed one grouped line: `removed-upstream 9: scripts/_onboarding/__init__.py, ... (list truncated after six)`.
* `--stage` and `--apply` exited 0. The next `--plan` printed the same line again. The nine files stayed on disk, and the old helper still ran (`--dry-run`: "no eligible activations").
* A bare `--finalize` exited 0 and `verify_integrity` exited 0.
* After I deleted the nine files and committed, a bare `--finalize` exited 1 ("9 tracked file(s) missing on disk"), `--finalize --force` exited 1, and `verify_integrity` exited 1 with nine `missing:` lines. This is the trap `bootstrap/UPGRADE.md:44-75` already warns about for the agreement file. I found no board row that releases a lock record (I searched `dev/PLANNING.md` for lock release, `removed-upstream`, orphan and forget-a-record).
* The log and the profile copy under `dev/modules/onboarding/` are not in the lockfile (0 hits for either in a fresh install's lock), so upgrade never touches them. Delayed tasks that were never activated sit in that profile copy and simply never appear. Tasks the helper had already copied into an adopter's `onboarding-tasks` slot stay: slot text is the adopter's, and upgrade does not rewrite it (`bootstrap/_scaffold/upgrade.py:1055-1058`).

**The gate.** This is a doctrine change, so it meets the rate-limit gate (`doctrine/rationale.md:443-452`), which answers single incidents. This change did not start from an incident. It started from the Maintainer's direction above, so the gate is not engaged, and the Decision records that in one line (Question 5). I ask for no edit to the gate. I do not rely on a recurrence reading, but for context three earlier repairs of this same mechanism are on record (`30a55d27`, `3b44bc72`, `2cc6b260`).

**Interactions with other 0.5 rows.** The engine batch is archived (`dev/plans/archive/engine-batch-f8-slots.md`); its re-anchor is owed, and this change adds to the same ceremony. The `repin` plan touches no onboarding file (`dev/plans/repin-build.md`). The board row "`NEXT_SESSION` becomes a local note" also edits the engine and the install manifest; if it removes a manifest row, it and this change both edit the row-count pin at `test_notice_install.py:184`, so whichever lands second re-reads it. Cairn Plain Language 1.0 edits `AGENTS.md` and `dev/agent_collaboration.md`; I edit neither.

**What I did not check.**

* I did not read either adopter repository.
* I ran no test and no full suite. My rehearsals ran against a scratch copy of the engine, not the real change, and I ran only `upgrade --plan`, `--stage`, `--apply`, `--finalize` and `verify_integrity` there.
* I did not measure whether anyone acts on seed tasks. I have no data; Cairn's own list is the only figure and it is not a fair rate.
* I did not read the 62 files that fire the cross-type trigger.
* I derived the 16 engine symbols and the frozen-file edits by reading and by a parse of top-level names. The plan re-derives them with `_ast_attest.py verify` and `_gate_manifest.py verify` on its final commit.
* I did not list every test that goes red when nine files leave the install. I searched by name and by the one count pin; the plan's scoped runs find the rest.
* I did not check how the changelog's old lines about the helper fare under `claim_check` once the files are gone. The 0.4 removal found two such lines and fixed them with allow-config entries (`2cc6b260`); I expect the same here and have not measured it.

## Proposal

Seven parts. No new file, tool, gate, status or config key, apart from one test file.

**What "at install" means.** The install does three things for onboarding, all while the scaffold runs, and nothing after. It writes the profile's seed tasks into the `onboarding-tasks` slot of `dev/PLANNING.md` (`install_onboarding`, `bootstrap/_scaffold/install.py:1282-1503`). It copies the two tour pages to `dev/modules/onboarding/`. It prints one line in the report saying where the list is. Nothing watches the project later and nothing is added to the list later.

**How first contact stays short.** (1) One list, not two: the report points at the list and does not repeat it. (2) No new tasks: the seed counts stay 6, 10 and 11, and a test pins them. (3) Five sentences of 9 to 20 words, 9 to 38 words per profile. (4) Each sentence sits at the end of a seed the adopter reads at that moment (a tour, a roster, a coordination read), so the text appears where they are already looking. (5) One report line, unnumbered, in a report of 142 to 186 lines. (6) No change to `AGENTS.md`, which every agent loads every session. These are expected effects, pinned by tests; I have not measured the finished install, because it does not exist.

**1. Stop shipping and installing the helper and its log.** Delete the nine shipped files and Cairn's nine copies. Stop seeding `dev/.cairn/onboarding-activated.jsonl`; delete Cairn's copy. Stop copying the profile file to `dev/modules/onboarding/<profile>.md` (its only reader was the helper); delete Cairn's copy. Keep the slot seeding, the `<!-- preset: <name> -->` comment (it records which profile chose the tasks, and removing it would edit `_render_onboarding_slot` for no gain) and the two tour pages, which install with any profile.

**2. Remove the always-on group from the engine, with its members.** The group exists only to keep the helper's launcher and engine together (`bootstrap/_scaffold/config.py:662-682`). With no member, `assert_always_on_complete` and its siblings check nothing, and I would not keep guard code that has no member and no test. A future always-on helper can add the registry back in the commit that adds it; git history keeps this one. `install_onboarding` keeps the slot write and the tour pages. The report gets one line, after the existing "Next steps" block and unnumbered because those numbers mirror steps of `bootstrap/BOOTSTRAP.md` Act II: "Day-one tasks for your profile are in dev/PLANNING.md under Onboarding." It prints only when the install seeded the slot; the plan chooses how `print_report` learns that (`main` already passes `modules=`). `main`'s label for an install with no profile ("helper + log only; no preset", `cli.py:572-574`) and its dry-run text (`cli.py:478-483`) are reworded.

**3. Profile files.** Delete the six `[trigger:]` items and the three Row 1 sections. Rewrite the preface, which today describes three kinds of content, to describe one. Append sentences A to E as quoted in Context. The seed counts stay 6, 10 and 11. I leave every other seed, and the report's two notes (model mapping, work-intent hooks), as they are.

**4. Doctrine and docs.**

* `doctrine/onboarding.md` becomes the install-time model, in its own words: "Cairn onboards once, at install. The install writes a short list of day-one tasks, chosen by the profile, into the `onboarding-tasks` slot of `dev/PLANNING.md`, and installs two tour pages beside it. Nothing activates later: no tool watches the project to decide when to add a task, and no log records what was shown." The premise "tasks that activate as the adopter's relationship with Cairn deepens" (`:24-28`) is the sentence it replaces. Components 2 and 3, the state-file schema, the caps, the goodnight invocation, the existing-adopter recipe and the v1.x candidates go (`:61-111`, `:134-284`). Component 1 and Component 4 stay in short form, "Dispatching an agent session" (`:285-311`) stays word for word, and the cross-references stay.
* `doctrine/session-routines.md:362-393`, the goodnight step that runs the helper, is deleted.
* `docs/agent-team-onboarding.md` and its installed copy (which `test_review_stance_in_shipped_files.py` requires to be equal) lose two passages that teach the triggers: the last paragraph of Step 1 (`:39-41`), and item 1 (`:74-78`) and the last paragraph (`:83-85`) of Step 4. Step 4 keeps its second reason to try one called read (`:79-81`).
* `docs/vision.md:78`, `on-ramp/README.md:92-97`, `templates/core/dev/PLANNING.md:31-47`, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md` and `bootstrap/UPGRADE.md:75` are reworded to match.
* `bootstrap/UPGRADE.md` gets a section beside the agreement section, as Question 3 describes. The changelog gets one entry, written by the plan's owner at the serialization point.

**5. Existing installs.** As Question 3. No engine change for them: the rehearsal shows `upgrade` already handles a file Cairn stops shipping.

**6. Tests.** Delete the six test files. Edit the nine test files and the three other frozen files listed in Context. Add `bootstrap/tests/test_install_time_onboarding.py` with these properties, each with a one-line mutant the plan's ledger runs beside an unmutated control:

* `TestNoProfileSchedulesAPromptForLater`: no profile file holds a `[trigger:` line or an "Active-surfacing" heading. Mutant: add a trigger line to one profile.
* `TestTheOnboardingListDoesNotGrow`: a real install of each profile seeds 6, 10 and 11 tasks. Mutant: add a seed.
* `TestEveryFormerPromptHasAnInstallTimeHome`: sentences A to E appear in the installed slot of the right profiles. Mutant: delete one.
* `TestInstallReportPointsAtTheList`: the report ends with the pointer line when a profile seeded the slot, and not otherwise. Mutant: remove the line.
* `TestInstallWritesNoActivationMachinery`: none of `scripts/onboarding_activate.py`, `scripts/_onboarding/`, `dev/.cairn/onboarding-activated.jsonl` and `dev/modules/onboarding/<profile>.md` is written, and both tour pages still are. Mutant: restore one write.
* `TestUpgradeLeavesAnOldHelperAlone`: my rehearsal as a test. It builds an old project the way `bootstrap/tests/test_agreement_retired.py` builds one (a fresh install, then the nine files and their lock records added by hand), runs `upgrade --plan`, `--stage`, `--apply` and bare `--finalize`, and checks that all exit 0 and the nine files are untouched. Mutant: make the planner delete a removed file.

**7. Order, so the Security Review is not the critical path.** The plan can land the text half first (profile files, doctrine, docs) and the machinery half after (deletions, engine, tests, manifest). Both halves are in scope; this sets only their order. The plan's Boundary B mode is `full` (contract and trust-ceremony surfaces, `AGENTS.md` "Verification boundaries"), recorded `Certified by: pending` until the next certifying run. Nobody sets `CAIRN_FULL_SUITE=1` for this change.

**Review and plan headers.** *Security Review owed:* the change edits the scaffold engine (`config.py`, `install.py`, `upgrade.py`, `cli.py`), `bootstrap/security_check.py`, `bootstrap/SAFETY.md` and the published install manifest, each named in `AGENTS.md` ("High-risk surfaces") or in the proposal template's triggers. *Plan needed:* it lands across many commits and areas, and Boundary B is `full` (`doctrine/plans.md:175-203`). *Lane:* deliberate (`doctrine/lifecycle.md:47-58`: it touches a high-risk surface and widens a contract).

## Rationale

The Maintainer asked for onboarding at install, not later. The measurements agree with him. The delayed design has run zero times in 136 days, and its detector confuses a word match with a cross-agent review. Delivered at install, the nine prompts come to five sentences of 9 to 38 words per profile, once the three that the install already says are set aside. So the saving a delay buys (a short first day) is small: at most 4% to 7% of the list. What it costs is nine shipped files, 1,964 lines per copy, a trigger engine to keep correct, an engine group, 77 or more test nodes, and shipped pages that tell adopters a trigger fires at the next goodnight when none does.

## Alternatives considered

* **Do nothing.** The helper stays unrun. Every adopter keeps nine executables, nine lock records and nine manifest rows for a feature that has not fired once. Shipped text keeps saying it works: `docs/agent-team-onboarding.md:39-41` and `:83-85` tell the adopter that a trigger fires at the next goodnight, and `doctrine/session-routines.md:362-393` tells the owner to run it. The Maintainer has said he does not want it delayed.
* **Wire the helper into `session-end --handoff` (the strongest alternative I rejected).** It keeps the design and makes it run, and it keeps the short first day that delay buys. It loses for five reasons. (1) The step cannot be prose alone. A line in the `session-end` skill (`templates/skills/session-end/SKILL.md`) asks the owner to remember, which is the arrangement that has produced zero runs since the helper shipped. To run it from the tool, `tools/session.py` and its byte-identical twin `templates/skills/_lib/session.py` would start a program with the resolved interpreter; those files hold the interpreter binding, which `AGENTS.md` names as a high-risk surface, and a new subprocess use there is a second Security Review. (2) The prompts would still arrive after the adopter has done a lot, which is what the Maintainer's words reject. (3) The detector would be wrong some of the time: the cross-type trigger fires on word matches (measured), and a first run today would activate two items at once. (4) Three of the nine say what the install already says, so a working helper would repeat the install to the adopter. (5) The saving it protects is 4% to 7% of the list. I would pick it only if the prompts were long or well-aimed; they are neither.
* **Move the content but leave the machinery.** The cheapest way to put the content at install: edit the profile files and docs, leave the helper and engine group in place. It loses because the helper would then read profile files with no triggers, and every adopter would keep nine executables that do nothing. The plan order in Proposal 7 gets the same early benefit without this end state.
* **Print the former prompts in the install report.** Adds lines to the first thing a new adopter reads (142 to 186 today), for advice that is for later. Rejected on first contact.
* **Add nine new seed tasks.** Each profile has three of the nine (rows 1, 4, 5; 2, 6, 8; 3, 7, 9), so the lists would grow from 6, 10 and 11 tasks to 9, 13 and 14: 50%, 30% and 27% longer. Rejected on first contact.
* **Point at the list from `AGENTS.md`.** Every agent loads `AGENTS.md` every session, so a line there costs every turn for a one-time need. The install report is one-time too. Rejected.
* **Show open onboarding tasks at `session-start`.** Would solve "written but not shown" more fully than one report line. It edits `tools/session.py`, a Security Review surface, to serve a list that matters for a few sessions. Not in this proposal. If the report line proves too weak, this is the next step, and it belongs in its own proposal.
* **Teach `upgrade` to remove an untouched copy of a file Cairn stopped shipping.** Removes the repeating line and the delete trap for all removals, now and later. It is new engine logic and a second Security Review, and the 0.5 release already carries other engine work (the engine batch and the security fixes). Offered as Question 3's alternative; I would queue it as a board row.

## Documentation / doctrine surface

Routed by layer, per `docs/DOCUMENTATION_PLAN.md`. *Governing layer (prescription):* `doctrine/onboarding.md` (rewritten as the install-time model) and `doctrine/session-routines.md` (one step removed). `AGENTS.md` and `templates/core/AGENTS.md` are unchanged. *Descriptive layer:* `docs/agent-team-onboarding.md`, `docs/vision.md`, `on-ramp/README.md`, `bootstrap/UPGRADE.md`, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. *Shipped templates:* the three profile files and `templates/core/dev/PLANNING.md`. *Deliberation layer:* this proposal, the plan, and the board row, which the planning session owns. The new sentences name no model or vendor (`python scripts/quality_gate.py --sub neutrality`).

## Evidence / verification plan

Prose and text pins carry most of the change; the machinery half is deletion plus the engine edits listed above.

| Surface | Check | What triggers it |
|---|---|---|
| All edited Markdown | `python scripts/check_cairn.py`; `python scripts/claim_check.py <file>`; `python scripts/link_check.py <file>` | a person or agent, before commit (no CI) |
| Profile files, doctrine, templates | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | a person; the certifying run before a push includes it |
| The six properties in Proposal 6 | `bootstrap/tests/test_install_time_onboarding.py` | `pytest`, scoped by the implementer; the certifying run before a push |
| Install and manifest | `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/<profile>.yml`; `--manifest` (87 rows, no `onboarding` row) | a person |
| Upgrade of an old install | the rehearsal as `TestUpgradeLeavesAnOldHelperAlone` | `pytest` |
| Engine symbols and frozen files | `bootstrap/tests/_ast_attest.py verify`; `bootstrap/tests/_gate_manifest.py verify` | a person, in the re-anchor ceremony; nothing runs either automatically |

I found the owning tests by searching the patterns in Context against `bootstrap/tests/`, `scripts/` and `tools/`; the plan's mapping repeats that search on the final tree and records any test it adds. Anything the mapping cannot bound falls back to the certifying run.

### Tests required

Proposed paths:
- `bootstrap/tests/test_install_time_onboarding.py` — the six properties in Proposal 6; lands with the implementing commits.

Scoped nodes: the files in Context's "Edited" list, the files in "Mention but need no edit", `test_manifest.py`, `test_notice_install.py`, `test_install_*`, `test_upgrade*` and `test_verify_integrity*` as the plan's search finds them.

#### Security preflight

The change touches the scaffold engine and the install contract, so I answer all five questions.

* **S1 — Who supplied it?** The one decision this change adds to is which lockfile records become `removed-upstream`. `upgrade` decides that by whether the record's `src` path exists in the upstream templates (`bootstrap/_scaffold/upgrade.py:521-524`). The adopter's tree supplies `src`, as it does today for every record; the change adds no new input and no new channel. I did not re-audit that existing path's containment.
* **S2 — Can it fail?** The checks this change relies on are the new tests. The one-line mutant for each is in Proposal 6. I have run none of them, because the tests do not exist yet; the plan's ledger runs them beside a control. The checks I deleted (`assert_always_on_complete` and its siblings) guarded a group that no longer exists.
* **S3 — What fires it, over what?** `pytest` over `bootstrap/tests/test_install_time_onboarding.py` and the edited files, run by the implementer and in the certifying run; nothing runs it on commit. The adopter-facing sentences are the new `bootstrap/UPGRADE.md` section and the report line; the tests pin the line and the section's key sentence ("do not delete").
* **S4 — Which way does it break?** An upgraded project keeps nine executables that Cairn no longer refreshes or release-scans. That is stale code, not more authority: it writes only when someone runs it, and through its own containment guards (`scripts/_onboarding/security.py`). A later guard fix will not reach it. I ask the Security Review to decide whether the section should tell projects to leave the files, as I propose, or to blank them. I expect blanking to make `verify_integrity` report them modified until each is finalized by path; I measured deleting, not blanking.
* **S5 — Who still wins?** The assumed attacker can edit files in an adopter's repository. `verify_integrity` still reports an edited copy of the old helper while its lock record stays. An attacker still wins if the project then records the edit with `--finalize <path>`: the lockfile then holds the attacker's hash, and the check attests what was recorded, not what is safe. This change does not alter that limit. The class is closed by enumeration (nine records), not by construction; the follow-up in Question 3 would close it by construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Written now, while I am least motivated to hedge.

* A new project's agents still never open the Onboarding list, and the report line does not change that. I cannot measure this: Cairn collects no usage data from adopters. An adopter issue or the Maintainer's own use would show it.
* The list grows after this lands: any seed beyond 6, 10 and 11, or a profile file regaining a `[trigger:` line. The tests pin both.
* The real change differs from my rehearsal: `upgrade --plan` prints something other than one grouped `removed-upstream` line for the nine, or a bare `--finalize` refuses when no file was deleted. Either means the engine edit did more than remove rows.
* The Security Review finds that leaving stale executables in adopters' trees is not acceptable. Then Question 3's second alternative moves into this proposal's scope.
* The Maintainer or an adopter asks for a prompt to come back at a later moment. That is the recurrence that would justify a delayed design, and it would have to be a design with a working trigger and a runner.
* One of the five sentences becomes false (for example, reflections stop being gitignored). The text test in Proposal 6 pins the sentences' presence, not their truth; a reader has to notice.

## Scope delta

**Scope delta**: preserved (opening revision; nothing removed).

The baseline outcomes are: retire the helper, the triggers and the log; deliver the former prompts' content at install, rewritten where stale; replace the doctrine premise; ship in 0.5; keep first contact short. The nine-row table in Context shows where each prompt's content lands, including the three that need no new text because the install already says it, with the file and line that says it. The one piece of former text I drop outright is the clause "the second through fifth shape the steady-state" (row 3), for which I found no basis. Question 2 puts the three and the clause to you.

## Assurance path

**Assurance path**: high-assurance

The change touches the scaffold engine, the install contract, the published install manifest, a frozen gate set and governing doctrine, each in the template's trigger list (`dev/proposals/_template.md`, "Assurance path").

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-26

```
Reviewed commit: ac47a5848c91a95221968064f9675b32c461b476
Target: the whole proposal, except Security preflight answers S1 to S5 (left to the Security Review pass)
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised (2 blocking, 8 non-blocking)
**Verdict**: REVISE

**Method.** I extracted `ac47a584` with `git archive` into a fresh folder, ran the three profile installs there with `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), read the cited files, and ran only read-only probes. I ran no test and no suite. I did not read either adopter repository or the sibling NEXT_SESSION proposal.

**Foundations**

1. **Should this happen as framed?** Yes in direction, no in one detail. Retiring a mechanism nothing calls and moving its content into the install is what you asked for. The delivery step is the weak part: one report line, placed where the report does not end, for a list no routine shows. -- `git grep -l -i 'onboarding_activate\|_onboarding' -- tools .agents templates/skills` returns 0 files (control over `templates/modules/default-on`: 6); in my collaborative-team install "Next steps" is report line 137 of 182.
2. **Best alternative.** Doing nothing loses: your direction rejects it and the shipped pages say a trigger fires when none does. The strongest alternative is this proposal plus two docs-only pointers it did not weigh (`bootstrap/BOOTSTRAP.md` Act II, and the `session-start` skill), not the `session-end` wiring. -- `git grep -i onboarding -- bootstrap/BOOTSTRAP.md docs/quickstart.md` returns nothing; `templates/skills/session-start/SKILL.md` has 0 hits in `bootstrap/tests/fixtures/gate_manifest.json`.
3. **What would show it wrong.** A fresh agent session on a new install that never names the Onboarding list. The proposal's first signal (line 246) calls this unmeasurable; one session run by you on a scratch install observes it. -- `python tools/session.py session-start` in my scratch install prints no task (commits, tree state, threads, intents, interpreter only).

**Rulings**

* **(a) Delivers the content, not yet the attention.** The nine prompts' content does reach the installed files at install. Whether a reader sees it still depends on someone opening `dev/PLANNING.md`. A new adopter today sees reports of 141, 182 and 185 lines (the proposal's 142, 183, 186 include one provenance warning a release checkout omits), seed counts 6, 10, 11, no seed text in the report, and no task from `session-start`. A more direct route fits the same budget (R2). The report line itself is mis-placed (R1).
* **(b) The nine dispositions hold, with two gaps.** I checked all nine against `templates/onboarding/*.md`: every cited line matches. Row 1 is covered by the tour (`docs/dev-tour.md:41-55`); row 2's fact holds, because the install writes `dev/reflections/*` to `.gitignore` and the installed tour says reflections are gitignored. Rows 6, 7 and sentence E match `templates/core/AGENTS.md` "## Review" (line 61). The "second through fifth" clause has no basis anywhere: outside the profile file and this proposal, `git grep` finds nothing. No kept sentence is stale under the single review stance: A, C and E all leave a second type's read to you. Gaps: R4 (a conditional seed carries E and row 9) and the wording of C.
* **(c) The counts I re-derived match, except for the omissions in R3 and R6.** See "What matched" below.
* **(d) The rejection is fair.** Reason (2) decides it on its own: wiring the helper into `session-end` keeps the prompts delayed, and your second message says you do not want them delayed. Reason (1) is sound: a prose step is the arrangement that produced zero runs, and `tools/session.py` holds the interpreter binding. Reasons (3) to (5) are weaker: (3) is about the detector, which a wiring change could narrow to the three triggers used, and (5) weighs list length when the cost is timing. Drop them or mark them secondary. "Do nothing" is weighed fairly. The unweighed alternative is R2.
* **(e) Acceptable for this change, with one condition.** Leaving the nine files is safe as measured and matches the 0.4 precedent (`bootstrap/UPGRADE.md:44-75`). Do not fold "remove untouched copies" into this change: it adds a delete path to the upgrade engine and a second Security Review, and the delayed prompts are not its cause. What is lost by keeping it out: every existing project keeps about 1,964 lines of dead executable code and a repeating `removed-upstream 9` line until the follow-up lands. Whether to accept that is yours (Question 3). The condition is R8.
* **(f) Headers are right; the order has a hazard.** `usual + Security Review`, plan `required(Internal + Internal Security Review)`, deliberate lane and high-assurance follow `AGENTS.md` "Review" and `doctrine/lifecycle.md:47-49` (a) and (b). The text-first order breaks a test in between (R5). Sequencing against the sibling proposal gets one sentence and needs more (R9).

**Findings**

* **R1 (blocking). The report line goes in a place the report does not have.** Context line 64 says the report "ends with a fixed Next steps block"; Question 1 and Proposal 2 put the new line "at the end ... after the existing Next steps block"; `TestInstallReportPointsAtTheList` pins "ends with". In my collaborative-team install "Next steps" is line 137 of 182. About 45 lines follow it: the module-merge pass, the security-verification NOTE, the model-selection NOTE (line 148), the hooks note (line 171) and the lockfile line (182, last). A line printed after the block in `print_report` (`install.py:1727-1733`) lands above all of those, and a test pinning "ends with" fails or pins the wrong place. Fix: choose the position and say it. The most visible is the last line of the run, printed from `main` after the lockfile write (`main` is already in the changed set); restate Question 1 and the test to match.
* **R2 (blocking, on the weighing only; the author may decline). A more direct delivery fits the budget and was not weighed.** (i) The report does not grow: 11 lines in every profile name files this change stops installing (nine helper files, the log, the profile copy; I counted 11 of 141, 182 and 185), so net change is about minus 10, not plus 1. (ii) `bootstrap/BOOTSTRAP.md`, the script an adopting agent follows, never mentions the day-one list; Act II-6 ("Dogfood") is where the seeds' first proposal belongs. (iii) `session-start` step 3 already tells the agent to read the board and any custom steps; one sentence there ("name the first open Onboarding task") is a template edit, not `tools/session.py`, and reaches existing installs through ordinary upgrade, which the report line cannot. The author's reason against prose steps (zero runs) was about a goodnight step that is not in the `session-end` skill at all (0 hits for "onboarding" in `templates/skills`); a line in the routine run first is a different case. I did not measure whether agents follow either. Cost: two more prose files, and the skill tests that compare skill bytes must run. Fix: add (ii) and (iii) to Proposal 3 or 4, or put them in Alternatives with a reason to decline.
* **R3 (non-blocking). The proposal found one count pin; there are three.** `test_notice_install.py:184` pins 96 rows. Also pinned, and not named: `test_notice_install.py::test_manifest_has_the_expected_py_source_count` (44 `.py` manifest sources, 9 of them the mechanism, so 35), and `test_security_lint.py::test_templates_py_count_is_pinned` (40 `.py` under `templates/`, so 31). The second file is frozen and is on neither the "Edited, 12" nor the "mention" list, so edited frozen files are 13 and frozen files touched 34, not 33. The test's own text requires both pins to move in the same commit. I found them by a wider pattern sweep of `bootstrap/tests`; controls: `find templates -name '*.py'` gives 40 and `install_manifest()` gives 44 `.py` rows. Fix: add both, and state the same-commit rule in the plan.
* **R4 (non-blocking). Sentence E and row 9 ride on a conditional seed.** `agent-team-onboarding-legacy` sits inside `cairn:if agent_team in concurrent-multi-type` (`high-rigor-legacy.md:91-97`). A legacy adopter who sets `single` or `concurrent-single-type` gets neither the seed, nor E, nor row 9's calibration advice, and that adopter is the one who adds a second type later. The default profile sets `concurrent-multi-type` (`bootstrap/profiles/high-rigor-legacy.yml:12`), so the loss is limited to overrides. The proposal flagged the same condition for the collaborative profile (row 8) but not here. Also, C's "record it there" has no antecedent after the seed's last sentence. Fix: attach E to `walk-dev-tour` (legacy, which already takes D), or say the loss; run `TestEveryFormerPromptHasAnInstallTimeHome` once with a non-default `agent_team`; reword C.
* **R5 (non-blocking). Proposal 7's order breaks a test in between.** `test_active_surfacing_render.py:35,83` reads the three real profile files. Removing the Row 1 sections in the "text half first" step turns its 10 nodes red until the machinery half deletes it. I read this; I did not run it. Fix: make the profile-file edit and the deletion of the tests that read those files one step, and say that `FROZEN-MISSING` is expected until the re-anchor.
* **R6 (non-blocking). The engine symbol count of 16 omits two constants.** The group's own failure kind, `new-core-incomplete-group`, is named in `_KIND_DISPLAY_LABEL` (`upgrade.py:365`, in the baseline) and `_BLOCKED_ADDITION_KINDS` (`upgrade.py:926-931`, in the known-new manifest), and pinned in `test_upgrade_side_door_parity.py:376-402`. Either the plan deletes the dead kind (count at least 18, consistent with Proposal 2's "no guard code that has no member") or leaves a dead kind in a fail-closed list. Fix: say which; the Security Review reads this list. My AST scan found exactly the 8 deleted and 8 changed the proposal names, plus these two.
* **R7 (non-blocking). Some edits are not listed, and one claim is wider than its evidence.** Not listed: `docs/agent-team-onboarding.md:56` ("The onboarding helper does not read it"), `:72` ("worth doing for two reasons" is false once item 1 goes), the sentence "Commit the roster edit." inside the :39-41 paragraph the proposal deletes whole, `templates/README.md:91` ("the onboarding helper"), and `test_review_stance_in_shipped_files.py:1759`, which asserts Cairn's installed profile copy exists. The inventory patterns lack "onboarding helper" and "activation helper"; those two find the prose ones. Separately, In brief says the prompts "have never appeared": measured only in Cairn's tree (log 303 bytes), not in the two adopter repos you asked me not to read. Fix: add the two patterns to the plan's search and scope the sentence.
* **R8 (non-blocking). Make the follow-up a named 0.5 row.** The author's own search found no supported way to clear a lock record, so each removal leaves a permanent `removed-upstream` line, and this one is nine times the 0.4 case. Fix: queue "have `upgrade` remove untouched copies of files Cairn stopped shipping" as a named row, not "possible", and have the new UPGRADE.md section say no supported way to clear the records exists yet. Security question S4 (stale executables left in place) stays with the Security Review.
* **R9 (non-blocking). Sequencing against the sibling proposal is one sentence.** The "87" appears in the Evidence table (line 215) and in Context; if the sibling removes a manifest row, 87 is wrong when it is checked. Both proposals edit engine files, the same count pins (R3) and the one re-anchor. Fix: write the target as "rows in `install_manifest()` at the landing tree minus 9", say the planning session sets the landing order, and say the second lander re-derives the pins and the AST changed set. I did not read the sibling.
* **R10 (non-blocking). Questions 3 and 5 need a translator.** Q3 uses `removed-upstream`, `--finalize` and `verify_integrity` unexplained; Q5 asks about the "rate-limit gate", defined about 100 lines below; Q2 depends on table row numbers; the In brief sentence (line 8) is 55 words. Suggested Q3: "Projects that already installed Cairn keep nine old files that now do nothing. If someone deletes them, the upgrade tool refuses to finish until it is fixed by hand. Default: tell them to leave the files alone." Suggested Q5: "Does this change need a justification beyond your request? I say no."

**What matched.** Figure, then how I checked it (each pattern first run against a known-present case).
* Mechanism 9 files, 1,964 lines: `wc -l` 88 plus 8 files; `cmp` shows all 9 copies in `scripts/` identical.
* Manifest 96 rows, 9 of them the mechanism: `install_manifest(modules=None)`; 87 is 96 minus 9; pin at `test_notice_install.py:184` confirmed.
* Gate manifest 195 frozen files and 4,612 nodes; the six deleted test files drop 77 nodes (8, 10, 6, 31, 18, 4 from `node_ids`); the 15 deleted frozen names match.
* 16 symbols: 8 deleted and 8 changed, placed in baseline or known-new as stated (`grep -w`), plus R6.
* Cross-type trigger: 62 of 154 files fire (153 plus this proposal), using the helper's own lister and detector; controls: Codex author with a Claude reviewer fires, two plain Claude passes do not, "continue" plus "metadata" fires.
* Install reports 141, 182, 185 lines (the author's minus the provenance warning); seeds 6, 10, 11; slot words 209, 451, 508.
* Inventory: the ten patterns return 119 files at `ac47a584` (118 at `1d5a047b`, so the proposal's own file is one of them); 52 are records.
* Nothing runs the helper: 0 hits in `tools`, `.agents`, `templates/skills`; hooks are `post-commit` and `pre-commit` only; `.github/` has no workflow; the log is 303 bytes with one commit (`7519c5da`, 2026-06-12, 136 days).
* `python scripts/claim_check.py` on this file: no flags (three exempted forward paths). By hand, every file name resolves (bare fixture names and `labels.yml` resolve under `bootstrap/tests/fixtures/` and `.github/`), the six cited commits exist, and about 35 cited line ranges I opened match.

**Blocking findings: yes, R1 and R2.** R1 changes what Question 1 promises. R2 asks only that the Response weigh the docs-only routes; the author may decline with a reason.

**Coverage.** Not checked: the upgrade rehearsal (`removed-upstream 9`, the finalize exits), which I did not re-run because it needs a patched engine; the word counts of sentences A to E; the report's "20 / 23 / 23 slots" figures; the `claim-check-allow.json` line numbers and the contents of `bootstrap/SAFETY.md` and `SECURITY_MUTATIONS.md`; the 12 "edited" versus 6 "mention" split beyond R3's sweep; whether `doctrine/onboarding.md` shrinks to about 80 lines (its parts total plausibly that, unmeasured); the 4%/6%/7% growth percentages. Left for the Security Review pass: S1 to S5, whether deleting the completeness-group guard (`assert_always_on_complete` and its siblings) weakens a fail-closed protection any future always-on helper needs, leaving stale executables in existing installs (S4), the `bootstrap/security_check.py` and `scan_targets` edit, and the AST correction route. No Security Review is cleared or ruled on here.
