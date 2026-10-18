# Plan: the model mapping on every install path -- a notice where agents install, a check that is right both ways, and a write that cannot escape

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-model-mapping-install-path.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance -- inherited: the change edits the scaffold engine (`bootstrap/_scaffold/`), a script every adopter runs verbatim, and the onboarding seeds written into preset adopters' `dev/PLANNING.md`
**Opened**: 2026-10-18

## In brief

**The problem.** Cairn asks a project to record which AI model plays each of three roles: high, medium and low capability. The record is a small file, the *mapping* (`dev/.cairn/model-selection-mapping.yml`). The install creates it as a placeholder, the *stub*, in which every field reads `FILL ME`. A short script, the *check* (`scripts/check_model_selection.py`), fails while any placeholder remains. Cairn's own mapping sat on the stub for four months, the check failing the whole time, and nobody saw. Four holes allowed it:

1. **An agent installing has no keyboard,** so Cairn skips its questions, and it said nothing at all. That is how agents install.
2. **Nothing runs the check.** Cairn has no automated test service, so it runs only when a person or agent remembers.
3. **The check is wrong in both directions.** It fails a mapping that was filled correctly if the stub's explanatory comments were left in, and it passes a file that has no rows at all.
4. **`upgrade` and `--adopt-module` never mention the mapping.** The stub reached the Maintainer's other project that way.

A fifth, found on the way: the step that writes the answers has no protection against a *link*. A link (symlink) is a file that points at another file. If the mapping were one, the answers would be written into the file it points at, outside the project.

**What this plan does,** in five chunks that each land as one commit:

* **C1, the check.** Comments no longer count as placeholders, a mapping needs at least one row, and with PyYAML (a common but optional Python library) the check also reads the values the way YAML does, so a placeholder hidden by clever spelling is still found.
* **C2, the words and the reminder.** The stub's example says to name a model *family* and never a version. A "Filling the mapping" paragraph joins the module document. The installer's acceptance checklist (II-5) gains one item asking that the check pass. Two presets (`collaborative-team`, `high-rigor-legacy`) seed a row, `**Waiting on Maintainer**: fill the model mapping`, which `python tools/board.py --maintainer` lists on day one.
* **C3, the notice on install.** A fixed notice prints on every install, including one run by an agent, while the mapping is unfilled. It tells the agent to ask the Maintainer which model family fills each tier, and not to guess.
* **C4, the safe write.** The interactive capture refuses a link before it asks anything, and writes by creating a fresh temporary file and renaming it over the mapping, so no link or second name for an outside file can redirect the write.
* **C5, the notice on adopt and upgrade.** `--adopt-module` and `upgrade --plan`, `--stage` and `--apply` print the same notice. `--apply` prints it only after the apply succeeded, which is the run that delivers the stub to a project that predates it.

**What it costs the Maintainer.** Nothing is pushed, and no re-anchor is performed by an implementing agent. Two ceremonies are owed, and both belong to the Maintainer. First, the *gate-manifest re-anchor*: five *frozen files* (files whose exact bytes the gate manifest records) change, and one pinned test node leaves on purpose, because you reversed the rule it pinned. The opening commit adds these to the queued row on `dev/PLANNING.md`. Second, the *AST correction*: the engine's fingerprint file records the exact shape of each engine function, and this plan changes four functions and adds two (none is on the list an agent may repair itself). That is a Maintainer-run correction. It is already owed for the `.gitignore` repair, whose four functions show as changed today; three of this plan's four are among them, so the correction covers five functions in all. One adopter-visible cost, accepted at the Decision: a project whose stub header was rewritten (LHM is one) meets one merge conflict at its next upgrade, and keeping its own side resolves it.

**How we will know it worked.** Each of these is a test that fails if the property is broken, and a mutation run (a deliberate break made to see whether any test notices) confirms it:

* a no-terminal install prints the notice and exits 0; a filled mapping, or a project without the module, gets silence;
* a hand-filled stub with its comments left in passes the check, and a mapping with no rows fails it;
* the engine and the check agree, line for line, on a generated set of 108 awkward files;
* a mapping that is a link, or sits behind one, is refused before any question, and the file it points at is byte-identical afterwards;
* Cairn's own mapping passes its own check, and the test fails if it returns to the stub;
* `python tools/board.py --maintainer` lists the seeded row on a fresh install from either preset.

**Terms.** *Mapping*, *stub*, *check*, *link* and *frozen file* are defined above. *Non-interactive* means an install run with `--non-interactive` or without a terminal on standard input, which is how an agent's shell runs. *Containment guard* is the engine's refusal to write through a link or outside the project (`_assert_safe_write`). *Boundary A, B and C* are the three verification jobs in `AGENTS.md`: scoped checks while building, one integration run on a clean commit, and the code reviewer's independent attempt to break it. *Bare path* means the check running without PyYAML.

## Source proposal

Accepted 2026-10-18 at `7f1bcdf0`. Revision 2 binds over Revision 1 where they differ. The Security Review (`3c133398`, SEC-1 to SEC-8) cleared its blocking findings in the closure pass (`0f61d81f`, CL-1 to CL-4); SEC-3 to SEC-8 and CL-1 to CL-4 are carried into this plan, and its Internal Security Review checks them (*The security findings ledger* below). The Decision's words were "accept as answered", and the Maintainer's answers, each the recommended option, bind this plan:

* **Q1, the check:** "Yes to both". It skips full-line comments, and a mapping with no rows fails.
* **Q2, Scope delta:** "Allow two presets". The seed goes in `collaborative-team` and `high-rigor-legacy`, not `solo-greenfield` (*Scope delta* below).
* **Q3, the Waiting row:** "Yes". Fresh installs from those two presets seed the `**Waiting on Maintainer**` row.
* **Q5, the stub example:** "Yes, edit it". The example block says to name a model family, never a version. The Maintainer's direction, recorded in `47b38074`, is "Versions should not be named here, rather the latest version should be used". The accepted cost is one merge conflict for an adopter whose stub header was rewritten.
* **Q4, onboarding prompts in goodnight:** not part of this contract. It is carried as a board item at archive (*Dispositions*).

The plan executes the accepted text. It does not re-argue it.

## Scope

Measured at `72434d73`, the HEAD when this plan was written.

**Touched.**

| Surface | Files | Chunk |
|---|---|---|
| The check | `templates/modules/team-gated/check_model_selection.py` and its byte-identical copy `scripts/check_model_selection.py`; `bootstrap/tests/test_model_selection_stub.py` | C1 |
| Words and seeds | `templates/modules/team-gated/model_selection_mapping_stub.yml` (the example block only); `templates/modules/team-gated/model-selection.md` and its byte-identical copy `dev/modules/model-selection.md`; `bootstrap/BOOTSTRAP.md` (II-5 and the vendor-neutrality list inside it); `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md`; `bootstrap/tests/test_onboarding_seed_roster.py` | C2 |
| Install notice | `bootstrap/_scaffold/install.py`, `bootstrap/_scaffold/cli.py`; one comment in `bootstrap/_scaffold/lockfile.py`; `test_model_selection_stub.py` | C3 |
| Capture write | `install.py`, `cli.py`; `bootstrap/_scaffold/SECURITY_MUTATIONS.md`; `bootstrap/tests/test_security_leaf.py`; `test_model_selection_stub.py` | C4 |
| Adopt and upgrade | `bootstrap/_scaffold/upgrade.py`; `test_model_selection_stub.py` | C5 |
| Cairn's install record | `dev/.cairn/cairn-lock.yml`: two records, `scripts/check_model_selection.py` (C1) and `dev/modules/model-selection.md` (C2) | C1, C2 |
| Board and changelog | `dev/PLANNING.md` (the opening commit joins the re-anchor row; the archive commit adds the node note and the deferrals); `CHANGELOG.md` (the archive commit) | opening, archive |

**Not touched,** each checked by `git diff --stat` over the implementation range (C6): `bootstrap/_scaffold/config.py`, `security.py`, `slotmerge.py`, and `lockfile.py` apart from the one comment; `bootstrap/scaffold.py`; Cairn's own filled mapping `dev/.cairn/model-selection-mapping.yml`; `tools/session.py` and `templates/skills/_lib/session.py`; `scripts/_onboarding/`; `templates/onboarding/solo-greenfield.md`; Cairn's own onboarding slot in `dev/PLANNING.md` and its installed preset copy `dev/modules/onboarding/collaborative-team.md` (the lockfile does not track it, and it already differs from the template); the profile schema; the gate-manifest fixture; and the two AST fixtures, which only the Maintainer writes (*Frozen files, AST and the oracle*).

**Dry runs and other upgrade actions.** `scaffold.py --dry-run` returns before any module file is written, so it stays silent. `upgrade --init-lock`, `--finalize` and `--adopt-collisions` stay silent too: the accepted text names install, `--adopt-module` and `--plan`, `--stage` and `--apply`, and nothing else.

### What the exit codes are now (re-derived from the code at `72434d73`)

The proposal's exit-code text predates the `.gitignore` repair, and the repair changed it twice. `b8a402c6` wrapped all of `main` in one catch that returned 2. `fde3054c` withdrew that wrapper, because the differential oracle pins the traceback and exit 1 of every other install-time refusal. What stands now is three small preflights plus the older local catches. Every row was read in the code; the install and `--adopt-module` rows were also run in a scratch tree.

| Where | Refusal | What prints | Exit |
|---|---|---|---|
| install (`main`) | a linked `.gitignore`, asked before the first write, dry run included | `error: .gitignore seed refused (containment): ` and **the exception text** | 2 |
| install | the skills fan-out | `error: skills fan-out refused (containment): ` and the exception text | 2 |
| install | the onboarding install | `error: onboarding install refused: ` and the exception text | 2 |
| install | **every other containment refusal**: a linked `AGENTS.md`, a linked `dev/.cairn` (stops in `write_local_env`) | a traceback ending `ScaffoldSecurityError` | **1** (the oracle pins this) |
| `upgrade --adopt-module` | a linked `.gitignore`, before anything is recorded | the `.gitignore` line, with the exception text | 2 |
| `upgrade --adopt-module` | every other containment refusal (a linked `dev/.cairn`: run and confirmed) | a traceback | **1** |
| `upgrade --apply`, `--stage` | a linked `.gitignore`, before any write | the `.gitignore` line | 2 |
| `upgrade --apply`, `--stage` | a refusal inside `_apply_upgrade` or `_write_stage` | `error: upgrade --apply refused (containment): ` or `--stage`, and the exception text | 2 |
| `upgrade --adopt-collisions` | a refusal | `error: upgrade --adopt-collisions refused (containment): ` and the exception text | 2 |
| `upgrade --plan`, `--finalize`, `--init-lock` | none is caught | a traceback | **1** |
| `_apply_upgrade` itself | its own refusals (leftover conflict markers, a dirty tree) | an error line | 1, returned |

So the chain is: there is **no single catch**; each caller that wanted a clean exit catches where it chooses, and everywhere else a refusal ends in a traceback and exit 1. Two further facts matter. First, **no refusal line is fixed text**: all of them append the exception text, which names the path the tree chose, and `_assert_safe_write`'s third wording ("outside the target directory") names a resolved link target. Second, this plan adds one catch (the capture's, in `main`), and it prints a constant.

**Where the proposal's text is stale,** said plainly:

* **CL-2** says `main` wraps the whole CLI in one catch, that the capture call moved into a `_run_cli` function, and that `SECURITY_MUTATIONS.md` lines 12-13 are true as they stand. None of it holds at HEAD. There is no wrapper and no `_run_cli`; the capture call is back in `main` (`bootstrap/_scaffold/cli.py:666`).
* **SEC-4 and Revision 2** say `main` catches two refusals. It catches three today, and four after C4.
* **`SECURITY_MUTATIONS.md` lines 12-13** say the guards' error is "caught once at the CLI top level (exit 2)". That is false again, so the correction Revision 2 asked for is owed after all, with the wording above. C4 writes it.
* **The "fixed refusal line"** the entry brief and Revision 2 imply is a fixed prefix followed by exception text. Only the capture's new line is constant.
* **Revision 2's claim that a linked `dev/.cairn` stops early in `write_local_env` with a traceback and exit 1** is still true. It was re-run.
* **The AST count.** Revision 1 says "4 CHANGED, 2 NEW" against a baseline that was clean. The baseline is not clean now; see below.
* **The entry condition holds:** `seed_gitignore` is in `_GUARDED_WRITE_FUNCS` (`bootstrap/tests/test_security_leaf.py`) and has a Class A row in `SECURITY_MUTATIONS.md`. C1's gate re-reads both at its parent.

### Frozen files, AST and the oracle

**Frozen files: six, measured.** Read from `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys) and intersected by script with every file this plan edits. The instrument was checked against a known key (`bootstrap/tests/test_scaffold.py` is reported frozen). The six:

* edited by an implementing agent (five): `templates/modules/team-gated/check_model_selection.py`, `scripts/check_model_selection.py` (C1); `bootstrap/tests/test_model_selection_stub.py` (C1, C3, C4, C5); `bootstrap/tests/test_onboarding_seed_roster.py` (C2); `bootstrap/tests/test_security_leaf.py` (C4);
* written by the Maintainer's AST ceremony (one): `bootstrap/tests/fixtures/scaffold_ast_known_new.json`. The proposal's table lists it as touched. It is, but only the Maintainer-run correction may write it, because no symbol here is allowlisted; the repair that preceded this plan left its new symbol for the same ceremony. This is a sequencing fact, not a reduction: the outcome, that the new symbols are pinned, is delivered by the ceremony.

`bootstrap/tests/fixtures/scaffold_ast_baseline.json` is cascade-mutable in the manifest, not hash-pinned, and also Maintainer-written. Not frozen, though edited: every engine file, `SECURITY_MUTATIONS.md`, `BOOTSTRAP.md`, the stub, the module pair and both presets. Frozen files that **read** these surfaces and must stay green **unedited**: `test_scaffold.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_onboarding_slot_substitution.py`, `test_active_surfacing_render.py`, `test_trigger_evaluation_action.py`, `test_skills_onboarding.py`, `test_onboarding_review_tiers.py` (if `review-stance-and-lenses` has not already deleted it), `test_default_security_stance.py`, `test_profile_grammar.py` (it reads two example fences in `BOOTSTRAP.md`, not II-5), `test_upgrade.py`, `test_upgrade_module.py`, `test_security_capability_install.py`, `test_security_verification.py` and `_oracle.py`.

**The pinned collection moves.** New classes join `test_model_selection_stub.py` and `test_onboarding_seed_roster.py`; their node IDs are listed in the *Implementation verification* record. **One pinned node leaves on purpose:** `bootstrap/tests/test_model_selection_stub.py::TestFidelityCheck::test_fill_me_in_comment_fails` pins the rule the Maintainer reversed (Q1). It is replaced by `TestCommentsAreNotPlaceholders`, not renamed in place, because a node called "a comment fails" that asserts the opposite would mislead. `test_pyyaml_absent_degrades_gracefully` keeps its ID with a changed fixture (it needs a row; see C1). Changed frozen bytes do not redden `test_gate_manifest.py`, which verifies a freshly produced manifest and never diffs the committed fixture, so a green suite is no evidence the re-anchor is paid. **The re-anchor is the Maintainer's alone** (`bootstrap/REANCHOR_RUNBOOK.md`). The opening commit adds this plan's files to the queued row, marked planned and not yet changed; the archive commit adds the node IDs.

**AST: measured, not assumed.** The method is `bootstrap/AST_BASELINE_RUNBOOK.md` Step 1, run at `72434d73` (no file under `bootstrap/_scaffold/` has an uncommitted change). The baseline is **already red:** `CHANGED 4, MISSING 0, DUPLICATE 0` (`main` in `cli.py`, `seed_gitignore` in `install.py`, `_cmd_adopt_module` and `cmd_upgrade` in `upgrade.py`), all from the `.gitignore` repair, and `test_ast_attest.py` fails 2 of 30 nodes. This plan's delta against that:

* **already CHANGED, change again** (no new entry for the Maintainer): `main`, `_cmd_adopt_module`, `cmd_upgrade`;
* **newly CHANGED:** `capture_model_selection_mapping` (baselined; C4);
* **NEW, to be pinned in `scaffold_ast_known_new.json`:** `_mapping_is_unfilled` and `model_selection_notice_lines` (C3), both in `install.py`;
* **comment-only, no AST effect:** `lockfile.py` (the attestation parses code and sees no comments; C3 proves it by showing no `lockfile.py` symbol among the CHANGED);
* **not changed by this plan:** `seed_gitignore` (it stays CHANGED from the repair, and is the fifth of the five), `_write_stage` (it only joins a test list), `_yaml_dq`, and the `_MODEL_SELECTION_*` constants.

Expected end state: **5 CHANGED, 2 new NEW.** The figure is a pointer, not the instrument: C6 derives it again at the parent and at the tested commit and requires the difference to be exactly the delta above. **No symbol here is in `_UPDATE_ALLOWLIST`** (`_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`), so the correction is a Maintainer-run, dry-run-verified direct correction that an implementing agent does not perform. Imports are not attested, so the new standard-library imports cost nothing, and `test_install_module.py::test_install_depends_only_downward` (install imports only its lower siblings) is unaffected.

**The oracle.** `bootstrap/_scaffold/` is on the differential oracle's sensitive roster (`bootstrap/tests/_oracle_activation.py`). Against the gate anchor `bd66a70c`, five engine paths already differ at HEAD: `cli.py`, `install.py`, `upgrade.py`, `slotmerge.py` and `SECURITY_MUTATIONS.md`. The comment in `lockfile.py` makes it a sixth changed path for the ceremony's path check, a small real cost of an edit the accepted text asked for. The oracle's fresh-install scenario installs each preset non-interactively with the **current** templates and byte-compares the resulting trees; notice lines go to standard output, which it does not compare, and the stub, seeds and checker are templates both engines read. So the oracle should be unmoved, and Boundary B shows it.

### Lockfile

`python bootstrap/verify_integrity.py --target .` reports **18** violations at `72434d73`, none of them a file this plan edits. Two edited files match their record today and go stale when edited: `scripts/check_model_selection.py` (C1) and `dev/modules/model-selection.md` (C2). Each is reconciled by a scoped finalize of that one path in the commit that edits it (precedent `2ea3f869`), so the count stays 18. An unscoped finalize is never the fix, since it would re-attest the drifted 18. Cairn's own mapping is a living-state record and is not edited. The lockfile schema is untouched.

### Install contract

`scaffold.py --manifest` lists destination, source and mode, with no content hashes. No file is added to or removed from the install set. C6 shows its output byte-identical to the parent's.

### Found while planning, not widened

* **A pinned test needs a row under the new rule.** `test_pyyaml_absent_degrades_gracefully` checks that the bare path degrades gracefully, using the file `mapping: [unclosed`. That file has no row, so the new rule fails it with exit 1 and the test would go red for the wrong reason. C1 gives its fixture a row line; the assertion and the node ID are unchanged.
* **The checker can crash on deeply nested YAML.** `yaml.safe_load` raises `RecursionError` at about 500 nested flow sequences. `_structural_validate` catches only `yaml.YAMLError`, so today the checker ends in a raw traceback. The new value scan touches this path, so C1 catches it and reports exit 3, "not valid YAML" (*Plan decisions*, P8).
* **`_commit_lock_and_caches` has the hole the capture is being fixed to avoid.** It writes its lockfile and caches through a temporary file with a **fixed** name beside the target. A hard link planted at that name passes the guard, and the write goes through to the file the link points at. Measured in a scratch tree: a hard link at the lockfile's temporary name to an outside file left that file holding the lockfile's text. Git cannot carry a hard link, so it needs someone already on the machine, and the risk is low. It is outside this proposal, so it is **not fixed here** (fixing it would change a symbol that `scaffold_ast_known_new.json` pins by digest, which the proposal does not name). C4 does not copy that recipe. It is carried to *Dispositions* as a deferral that needs the Maintainer's authorization.
* **The `Waiting on Maintainer` marker on the queued row names only the gate-manifest re-anchor.** The AST correction is a separate ceremony with its own runbook. The row's prose can carry it, but the marker, and so `board.py --maintainer`, does not list it. Whether the AST ceremony needs its own marked row is the Maintainer's call; this plan declares no Waiting line, and the question is put at archive (*Dispositions*).
* **Citations from other plans.** `review-stance-and-lenses` cites `templates/modules/team-gated/model-selection.md:128-131`; C2 inserts its paragraph below line 158, so those lines hold (a criterion). It also cites `bootstrap/_scaffold/install.py` around line 1012, which moves when C3 and C4 land; it is an evidence note in a record, and `claim_check` checks only that a cited line is in bounds. `independent-scientific-check` states the AST baseline as two changed symbols; it is four now (above), and its own criterion says to derive the figure again.
* **The proposal's own line citations moved** (`cli.py:625` is now 635, and so on). This plan cites by function name and uses a line number only where it says "at `72434d73`".

### Plan decisions the proposal left open

The accepted text fixes the behaviour, not every shape. These are this plan's choices; plan review may overrule any of them.

* **P1, where the notice is gated.** Each call site calls the helper only when the module is in play: `main` inside `if "model-selection" in modules`, adopt when the name is `model-selection`, upgrade when `"model-selection"` is in the lockfile's module list as read at the start. The helper is also silent on a missing file (CL-3), so a project without the module gets silence twice over.
* **P2, the temporary file.** `tempfile.mkstemp(dir=<the mapping's folder>)`: a random name, created exclusively, so a file or link already waiting anywhere cannot be written through. The capture's signature does not change.
* **P3, CL-4: widen, and name the rest.** The bare row test accepts a quoted `tier` key and a one-line list whose first item begins with `tier`, on top of the anchored forms. A prototype in a scratch copy, over 21 hand-built spellings, showed the anchored pattern rejecting three spellings that PyYAML reads as rows (a double-quoted key, a single-quoted key, a one-line list), and the widened pattern accepting all three. The differences that remain are all in the bare path's stricter direction, which is the louder side: a one-line list whose first key is not `tier`, and a `tier:` that sits inside another value. The parity test asserts those differences as an explicit list, in the direction they occur.
* **P4, the order of the checker's decisions.** Scan for `FILL ME` (exit 1), then with PyYAML the structure (exit 3 for a parse error or a non-mapping), then the row requirement (exit 1). So a comments-only file exits 1 on the bare path and 3 with PyYAML; both are non-zero, and the difference is listed in the parity test.
* **P5, the "could not read" wording.** CL-3 asked that it say "That file was not changed", since "Nothing was changed" reads wrongly after a successful apply. The final text is quoted in C3.
* **P6, the capture's refusal line.** `error: model-selection capture refused (containment)` on standard error, matching its sibling lines, followed by nothing from the exception.
* **P7, where the notice prints.** `main`: after the capture block, whether the capture ran, was skipped or was interrupted. Adopt: right after the "Adopted module" line. `--plan` and `--stage`: the last output before `return 0`. `--apply`: after the `try`/`except` that wraps `_apply_upgrade`, only when it returned 0, so a notice can never be reported as an apply refusal.
* **P8, the checker's loader.** It catches `RecursionError` from `safe_load` (exit 3) and walks the loaded value with an explicit stack, visiting each object once, so neither depth nor aliasing can blow it up. This adds two lines beyond the accepted text and removes nothing.
* **P9, no read-size cap.** The helper and the capture read the whole file. A multi-gigabyte regular file in a hostile tree could slow an install, but the checker and every other read in the engine do the same. Named as a residual, not built.
* **P10, the notice's second line.** For a file with no rows at all, "still holds the FILL ME stub" is imprecise. The quoted text binds, so it is kept and the imprecision is named. The first line, "is not filled in", and the instruction to write one row per tier stay true.
* **P11, the AST fixtures.** Neither is edited by an implementing agent (above).
* **P12, names.** Every test class and node is named for the property it pins. No finding id, chunk letter or plan row appears in an added comment, docstring or test name (a criterion in C6, with a control).

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Governing | none; nothing under `doctrine/` and no `AGENTS.md` changes, so the doctrine rate-limit gate is not engaged |
| Descriptive | none. Searched `docs/`, `README.md`, `bootstrap/*.md`, `dimensions/` and the template core for `model-selection`, `check_model_selection` and the mapping's name: no page describes the capture or the check. The one mention (`docs/solo-legacy-recipe.md`) says only when to add the module |
| Module text | the module pair (C2) |
| Install guide | `bootstrap/BOOTSTRAP.md`, II-5 (C2). The module document names II-5 without a path, because `BOOTSTRAP.md` is not installed |
| Deliberation | this plan; `dev/PLANNING.md` (the re-anchor row now; the deferrals at archive) |
| Changelog | one entry, written by the archive commit |

All shipped text stays vendor-neutral. The neutrality gate (`python scripts/quality_gate.py --sub neutrality`) reads `fail=0` at HEAD, so the criterion is **stays zero**. Every shipped block this plan quotes was scanned with the II-5 pattern and the gate's own denylist, with a control that did match (a line naming three of the denylisted names).

### Sequencing with the other plans

Three plans are open ahead of this one, in this order: `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`. `board-as-basis` is planned beside it (opened at `10ae6428`) and, as *Recommendation* below says, I think it should go ahead of this plan too. **This plan starts only when each plan ahead of it has reached `awaiting-code-review` or later.** Implementation is sequential because every plan commits to the same `master`, and interleaving would make each Boundary B range ambiguous. Plan review can run alongside, since a review writes only its own section. Files were read from each plan's own text at `72434d73` (`board-as-basis` at `10ae6428`).

| Plan | Files shared with this one | What each does there | Effect |
|---|---|---|---|
| **`neutrality-and-upgrade-slots`** (implementing; its C7 landed) | `dev/.cairn/cairn-lock.yml` | its twelve records (done in C2-C5) against this plan's two | disjoint records; read fresh, check the lockfile diff before each commit |
| | `dev/PLANNING.md`, `CHANGELOG.md` | its re-anchor-row paragraph; its archive entry | commit by path, read fresh |
| | the neutrality checker | stricter, and now zero | everything this plan ships is held to it: **stays zero** |
| | `bootstrap/_scaffold/` | not touched by it | its C12 compares the AST set at parent and tested commit; it must derive four changed symbols, not the two its text names |
| | `scripts/check_model_selection.py` | listed there as not touched | no overlap |
| **`independent-scientific-check`** (ready) | `bootstrap/BOOTSTRAP.md` | one sentence in the I-2 paragraph | this plan edits II-5; different sections, so a textual rebase. Cite headings, not lines |
| | `dev/PLANNING.md`, `CHANGELOG.md` | at its archive | commit by path |
| | the gate-manifest re-anchor row | its one new test file joins the row | one row, several paragraphs |
| **`review-stance-and-lenses`** (`ready-to-implement`; goes third) | `templates/modules/team-gated/model-selection.md` and `dev/modules/model-selection.md` | its C3: the role table, the downshift condition, the bright-line list, the diversity reference | this plan adds a paragraph and one sentence in the Mapping-record schema block, below its edits; **it lands first, so this plan finalizes the lock record second**. Its stance test must pass with this plan's text: the word "family" is forbidden there only in the downshift condition (a), and this plan uses it for mapping rows |
| | `templates/onboarding/collaborative-team.md`, `high-rigor-legacy.md` | its C7 rewords External-tier sentences | this plan appends one seed after the last seed (`walk-foldback-protocol`), before "Active-surfacing prompt content"; different paragraphs |
| | `bootstrap/tests/test_onboarding_seed_roster.py` | its plan runs it unedited | it runs first; this plan adds its seed tests afterwards |
| | `scripts/check_model_selection.py`, its template, `dev/.cairn/model-selection-mapping.yml` | its criterion: `git diff --stat` shows them untouched in its range | holds, because this plan's edits are outside its range |
| | `dev/.cairn/cairn-lock.yml`, `dev/PLANNING.md`, `CHANGELOG.md` | the `model-selection.md` record and its row paragraph | same record, sequentially |
| **`board-as-basis`** (plan open at `10ae6428`; recommended ahead of this one) | **the `board.py --maintainer` output** (installed from `templates/skills/_lib/board.py`) | its C1 pins the terminal board and `--maintainer` byte for byte, then its C2 moves the roadmap-row reader into one function shared with `--json` | this plan reads the output in one seed test and pins only the substring `fill the model mapping` and the word `declared`, never the column layout. If this plan runs second, its seed test is the first to run against the finished reader |
| | **the `dev/PLANNING.md` row grammar** (what counts as a row that declares a wait) | its golden tree covers rows in plain, indented, sub-bullet and dash-bullet forms and a marker mentioned inside a sentence, and its C2 test mutates the grammar | this plan's seed puts the marker on a two-space-indented continuation line inside a `* [seed; ...]` item: `**Waiting on Maintainer**: fill the model mapping` (22 characters, under the board's 48; measured to list at `dev/PLANNING.md:100` in a scratch install). I did not check that its "indented" form is this exact shape, so this plan's seed test is a second pin on exactly this shape: a grammar change that stops listing an indented seed line turns it red, whichever plan lands first |
| | `dev/PLANNING.md` (the re-anchor row) | its paragraph is already in the row (`10ae6428`) | this plan's opening commit adds its own after it and before the Waiting line, re-reading the file first |
| | `dev/.cairn/cairn-lock.yml` | its `tools/board.py` record | disjoint |
| | `CHANGELOG.md` | its archive entry | commit by path |

`stewardship-and-reuse` (accepted, no plan yet) edits the plan templates' *Scope*, *Dispositions* and deviation sentence, and `AGENTS.md`; it shares nothing with this plan.

**Recommendation: `board-as-basis` goes before this plan.** I wrote the opposite first and changed it after reading that plan. Three of its four reasons hold. The fourth (the rows this plan seeds would appear on the page from day one) does not, because the seed reaches fresh installs, not Cairn's own board. Two reasons of mine did not hold either: the "live defect" (below) and the "longer critical path", since both plans carry an Internal Security Review.

* **It has a user waiting; this plan has no pending case.** The hand-synced board page goes stale several times a day. Both known unfilled mappings are already filled (Cairn's own, and the Maintainer's other project's), so what this plan guards is the next install or upgrade into a tree whose mapping is not filled. That is a real risk, but nobody is hurt by it this week. My first draft called it a live defect, and that was too strong.
* **It changes no engine file,** so its position cannot change what the AST ceremony owes. This plan is the only open one that does.
* **The one argument for going first is the AST ceremony, and it is under the Maintainer's control.** The correction is owed once, for the repair's four functions and this plan's four (three are the same functions), five in all. If it runs before this plan lands, a second pass is owed. It has no deadline, and the queued row records the Maintainer's wish not to re-anchor early. **So hold the AST correction until this plan archives, whichever plan goes first.** That removes the argument.
* **The two share no implementation file.** The only couplings are the pinned `--maintainer` output and the row grammar (both in the table above); its C1 pins the output before anything else changes, so neither order costs a rewrite. If it lands first, this plan's seed test is written against the final board, which is a slightly better place to be.
* **The order is the Maintainer's to set,** and nothing breaks if it is reversed.

## Sequence

The chunks run in order. Each lands as one commit; nothing is pushed.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The check.** Both copies of the checker: YAML 1.1 line breaks only, full-line comments skipped, at least one row, the widened bare row pattern, the value scan when PyYAML is present, the `RecursionError` catch, the docstring and "whole-file scan" comment rewritten. In `test_model_selection_stub.py`: `TestCommentsAreNotPlaceholders` replaces the reversed node; the row, value-scan, bare-residual and Cairn's-own-mapping classes; the corpus generator and the checker side of the parity test; `test_pyyaml_absent_degrades_gracefully` gets a row. Scoped finalize of `scripts/check_model_selection.py`. | plan review landed (`ready-to-implement`); every plan the Maintainer has put ahead of it at `awaiting-code-review` or later; the entry condition re-read | one commit |
| C2 | **The words and the reminder.** The stub's example block; the module pair (paragraph and corrected sentence); the II-5 block and the fourth allowed match in `BOOTSTRAP.md`; the seed in both presets; the seed, II-5 and stub tests; the `TestFamilyNotVersionReachesEverySite` class with its C2 sites. Scoped finalize of `dev/modules/model-selection.md`. | C1 (the paragraph says what the check does) | one commit |
| C3 | **The notice on install.** In `install.py`: `_mapping_is_unfilled` and `model_selection_notice_lines`, with both variants as constants. In `cli.py`: the call after the capture block, and the old interactive-only line removed. The comment in `lockfile.py`. Tests: the install-path rows, constant text, the named pipe, the missing-file silence, and the engine side of the parity test. | C1 (the parity test compares the two rules), C2 | one commit |
| C4 | **The safe write.** `capture_model_selection_mapping`: early guard, strict read, write-time guard, `mkstemp`, guard on the temp file, copied mode bits, `os.replace`, cleanup on failure, the family prompt and header, the docstring. `main` catches the refusal (constant line, exit 2). `test_security_leaf.py` gains the capture and `_write_stage`; `SECURITY_MUTATIONS.md` gains the capture row and the corrected exit-code paragraph. | C3 | one commit |
| C5 | **The notice on adopt and upgrade.** `_cmd_adopt_module` and `cmd_upgrade`: five call sites in all. Tests: adopt, `--plan`, `--stage`, the delivering `--apply`, a refused `--apply`, and the no-module silence. | C3 | one commit |
| C6 | **Boundary B, the evidence the suite cannot give, then the record.** One full run on a clean commit; the mutation ledger; the stub merge measurement; the smoke checks; the AST, frozen and lockfile derivations. Appended as `## Implementation verification`. Status moves to `awaiting-code-review`. A surviving mutant sends the work back to its chunk and Boundary B is redone. | C1-C5 | one commit |
| M | **MAINTAINER-ONLY, no new ceremony.** The gate-manifest re-anchor and the AST correction. The five frozen files and the node changes join the queued row; the AST delta is in the record. **An implementing agent must not perform either.** The agent's part is the board note at archive. | code review cleared | Maintainer |

No Waiting line in this plan: the wait is already declared on the marked board row.

## Acceptance criteria

Each criterion says how it fails. A criterion that cannot fail is not one. Test classes are named for the property they pin. Every new test is red before the code that makes it green, and the commit body names the commit where it was red.

### Checks every chunk repeats

* **Claim check.** `python scripts/claim_check.py` on each edited document exits 0 with no hard flag.
* **Prose integrity.** `python scripts/check_cairn.py` shows no issue in a file the chunk edits. Any other issue is recorded and shown unchanged.
* **Neutrality stays zero.** `python scripts/quality_gate.py --sub neutrality` reads `fail=0` before and after.
* **Twins.** `cmp` on each pair in the chunk exits 0: the checker pair (C1) and the module pair (C2).
* **No process words in durable text.** `git diff -U0 <parent>..HEAD` over the chunk, added lines only, searched for finding ids, chunk letters and plan rows (`SEC-[0-9]`, `CL-[0-9]`, `MM-[0-9]`, `SR[0-9]`, `\bC[1-6]\b`, "plan review"), returns no process reference. The Unicode term "C1 control" is not one and is explained if it appears. A control: the same search over this plan file returns matches, so the instrument can match.
* **Lockfile.** After a scoped finalize, `python bootstrap/verify_integrity.py --target .` still lists exactly the 18 files it listed at the base, and the lockfile diff touches only the finalized record.

### C1 -- The check

* **A mapping you filled by hand passes.** The shipped stub with its row replaced by real values and every comment kept exits 0. The shipped stub exits 1. *Red when:* the comment skip is removed.
* **A placeholder in a value still fails,** including in a trailing comment on a value line: exit 1. *Red when:* the skip is widened to trailing comments.
* **The loss is pinned, not hidden.** A `# TODO: FILL ME` comment above filled rows exits 0, in a test whose docstring says why: the check attests shape, not intent. This is the property the reversed node used to hold.
* **Only a space before `#` makes a comment.** A line led by a tab, a no-break space, a form feed or a byte-order mark is scanned. Lines split on exactly `\r\n`, `\n`, `\r`, U+0085, U+2028 and U+2029: a `FILL ME` value behind U+2028 or U+0085 is found, and CR-only and CRLF files read like LF. *Red when:* `str.splitlines()` is used (it also splits on form feed and vertical tab, which would turn a form-feed-led comment into its own comment line), or a tab is treated as blank.
* **A mapping needs a row.** `mapping: []` with header comments exits 1 on both paths. A comments-only file exits 1 on the bare path and 3 with PyYAML (P4). The failure message says there are no rows, and does not say `FILL ME`. *Red when:* the row requirement is dropped.
* **The bare row test is anchored and widened (P3).** A `tier:` inside another value is not a row. A block row, a flow item, a quoted key and a one-line list starting with `tier` are rows. The corpus holds both CL-4 spellings.
* **With PyYAML, every value is scanned,** once each, by identity, with an explicit stack: strings, dict keys, set members, and bytes decoded as text. Each of these exits 1 with PyYAML: a `#` line inside a block scalar, a plain or quoted value folded over two lines, a line continuation, `"FILL\x20ME"`, a repeated empty `mapping:` key, `!!binary RklMTCBNRQ==`, and `!!set {"FILL\x20ME"}`. *Red when:* the scan is removed, or limited to strings.
* **The bare path's residual is pinned.** The same files exit 0 on the bare path, in a test that says they are the named residual. If that ever changes, the test is rewritten on purpose.
* **Aliasing and depth are safe.** A 22-level nested-alias document completes in a fixed time (run as a subprocess with a timeout of a few seconds; unmutated it takes milliseconds, without the visited set about eight seconds). A document 5000 flow-sequences deep exits 3 with no traceback.
* **The generated corpus.** Leads {none, space, tab, no-break space, form feed, byte-order mark} times breaks {the six above} times positions {comment, value, row}: 108 files. The expected verdict depends on the lead and the position, never on the break. The PyYAML checker's verdict differs from the bare checker's only on two explicit lists, one for each direction: stricter with PyYAML (the value spellings above) and looser with PyYAML (a one-line list whose first key is not `tier`; a row that is a mapping without a `tier` key; a `tier:` inside another value). A difference outside both lists fails. *Red when:* U+2028 is dropped from one copy's break set.
* **Cairn's own mapping passes its own check,** with and without PyYAML (by blocking the import). *Red when:* the mapping is reset to the stub, shown in a separate copy.
* **The pair is identical** (`cmp`), the docstring and the "whole-file scan" comment describe the new rule, and the residual class is named in the docstring: a value whose `FILL ME` is not spelled out on one non-comment line reads as filled on the bare path.
* **Existing nodes.** `test_pyyaml_absent_degrades_gracefully` keeps its ID, its assertion, and the "structural validation skipped" note, with a row added to its fixture. The other 23 pinned nodes of the file pass unedited.
* **Lockfile.** The scoped finalize of `scripts/check_model_selection.py` is in this commit.

### C2 -- The words and the reminder

* **The stub's diff is the example block and nothing else.** `git diff -U0` against the parent shows hunks only inside the lines that begin "Replace the placeholder row below" through `model: vendor-a/flagship-family`. The placeholder row (five fields, each `FILL ME`) and its trailing comments are byte-identical. A test pins the row as one list item with five `FILL ME` fields, and the example block as containing "family" and "never a version", with none of the gate's denylisted names.
* **The module pair** gains the "Filling the mapping" paragraph and the corrected sentence, quoted below. The hunks begin below line 158, so `model-selection.md:128-131` still says what review-stance cites. The corrected sentence replaces "surfaced by an existing routine".
* **II-5 names the check** (`TestAcceptanceChecklistNamesTheMappingCheck`). The block sits after the vendor-neutrality block and before the dogfood gate; "Three classes of match" becomes "Four", and the fourth is the filled mapping, described without naming a model. The installer's closing steps still print "Run the R-F acceptance gate (II-5)". *Red when:* either is missing. `test_profile_grammar.py`, which reads two example fences in `BOOTSTRAP.md`, passes unedited. No live document cites a `BOOTSTRAP.md` line after 544 (searched, with a control that found the proposal's own citations).
* **Measured, on the drafted wording:** in a scratch copy of `72434d73` with the seeds and the stub edit applied, twelve test files (the onboarding family in the C2 row of *Verification*, plus `test_model_selection_stub.py`) pass, 202 tests in all, `test_slot_seed_count_matches_source` among them.
* **The seed renders where it should.** Installing `collaborative-team` and `high-rigor-legacy` at their own settings puts `fill-model-selection-mapping` and the Waiting line in `dev/PLANNING.md`. The same preset with `complexity: simple`, and `solo-greenfield`, render neither. *Measured:* all four, in a scratch install. `python tools/board.py --maintainer --root <install>` lists one row, `declared`, text `fill the model mapping`, and the line number it names holds the Waiting line.
* **The seed outlives a removed module, knowingly.** A profile that removes `model-selection` from a moderate preset still gets the row; a test pins that, so a later roster gate is a deliberate rewrite. The seed's "If ... exists" opening is why it does no harm.
* **A live install writes a clean lockfile** for both presets at their default axes, so the onboarding overlay the lockfile precomputes agrees with the one installed.
* **Family, never a version,** at the C2 sites (the stub, the module paragraph, the II-5 block, both seeds): a parametrized test asserts each says it. The set of sites is listed from the tree by searching for the phrase, not from this plan. *Red when:* the phrase is removed from any one.
* **Lockfile.** The scoped finalize of `dev/modules/model-selection.md` is in this commit.

### C3 -- The notice on install

The two texts, final (P5). They are constants, defined inside the helper:

```
NOTE (model-selection) -- the tier-to-model mapping is not filled in:
  dev/.cairn/model-selection-mapping.yml still holds the FILL ME stub.
Until it is filled, `python scripts/check_model_selection.py` fails. Nothing runs
that check automatically. Ask the Maintainer which model family fills each tier
(high, medium, low); do not guess. Name the family, never a version: the latest
release is meant. The stub holds one placeholder row: replace it with one row per
tier, copying its shape (tier, model, date_verified, task_family, source), and say
in `source` who assigned the model.
Schema: dev/modules/model-selection.md, "Mapping-record schema".
```

```
NOTE (model-selection) -- could not read dev/.cairn/model-selection-mapping.yml
(it is a link, sits behind one, is not a plain file, or is not valid text).
That file was not changed. Open it yourself, then run
`python scripts/check_model_selection.py`.
```

* **The helper decides in this order.** (1) `lstat` the path: a missing entry (`FileNotFoundError`) returns `[]`, first, and nothing else is tried; any other `OSError` returns the second text. (2) Anything that is not a regular file (a link, including a dangling one, a directory, a named pipe, a socket, a device) returns the second text and is never opened. (3) A refusal from `_assert_safe_write` (a link above it, an escape) returns the second text. (4) A strict UTF-8 read; an `OSError` or decode error returns the second text. (5) `_mapping_is_unfilled(text)` true returns the first text, otherwise `[]`. It never raises. *Red when:* the missing-file branch is dropped (a project without the module is told it could not read a file it never had), or the pipe is opened.
* **A named pipe at the path returns within a timeout.** Run in a subprocess with a timeout; the unmutated helper returns at once, a helper that opens the pipe hangs.
* **The text ignores the tree.** The first text is byte-identical for different unfilled files, including one holding terminal control sequences. The second is byte-identical for a link, a link whose target name is distinctive, a link above the path, a directory, a pipe, a non-UTF-8 file and a dangling link. Neither contains file content, the link's target, an OS error text, or an escape character.
* **`main` prints it on every install path that selects the module.** A no-terminal install (`--non-interactive`, and separately a non-tty standard input) prints the first text on standard output and exits 0. An interactive install that skips every tier prints it. An interactive install that fills a tier prints nothing. A filled mapping is silent. An install without the module (a `solo-greenfield` install, and a moderate preset with the module removed) prints neither text. *Red when:* the helper is stubbed to return `[]` (the install-path rows fail).
* **The old interactive-only line is gone,** and the interrupt line stays: `kept the FILL ME stub` no longer appears in `cli.py`.
* **The engine and the bare checker agree** on the 108-file corpus from C1, exactly. *Red when:* U+2028 is dropped from the engine's break set while the checker's is intact.
* **`lockfile.py` changes by one comment.** It states the answer to its own revisit note: keep the reuse of the write guard on a read, and add the file-type check at the call site. No `lockfile.py` symbol appears among the AST CHANGED. `git diff` on the file shows comment lines only.
* **Exit codes are unchanged** for every install path; the notice changes no code.

### C4 -- The safe write

The order inside `capture_model_selection_mapping`:

1. return `False` at once if the install is non-interactive or the path is not a regular file;
2. **the early guard,** `_assert_safe_write(mapping, target)`, before any read, print or prompt;
3. a strict UTF-8 read in a `try`; a file that cannot be read or is not text is left alone and the function returns `False`; a file that is not unfilled returns `False`;
4. the prints and prompts (the family wording);
5. after the answers, **the write-time guard** on the mapping, then `tempfile.mkstemp` in the mapping's folder, the content written through the returned descriptor, **a guard on the temporary file,** the old file's mode bits copied to it, `os.replace` over the mapping, and the temporary file removed on any failure.

* **A link at or above the mapping is refused before anything is asked** (`TestCaptureRefusesBeforeAskingAnything`). Called directly with a prompt that fails the test if it is ever called, and with standard output captured: for a link to a regular file and for a linked `dev/.cairn`, the prompt is not called, nothing is printed, a `ScaffoldSecurityError` is raised, and the outside file is byte-identical. A dangling link is not a regular file, so step 1 returns `False` and the helper gives it the second text. *Red when:* the early guard is removed.
* **A real install proves the capture itself refused.** The fixture is an interactive install over a tree whose `dev/.cairn` links to a folder that already holds `local-env.json`, the onboarding activation log and a stub, so every earlier write skips; otherwise the install stops earlier, in `write_local_env`, and the test would pass for the wrong reason. It asserts exit 2, the constant line `error: model-selection capture refused (containment)` on standard error, **no text from the exception** (the link target uses a distinctive name that must be absent), and no lockfile. *Red when:* the catch prints the exception.
* **A hard link at the mapping is harmless.** The mapping is a second name for an outside file holding `FILL ME`. After the capture the outside file is byte-identical, and the mapping is a fresh file with a link count of 1 holding the captured rows. *Red when:* the write goes into the old file (`write_text`).
* **A planted name cannot redirect the write.** A hard link and a symbolic link are planted at the obvious fixed temporary names beside the mapping (the mapping's name with `.tmp` appended, and a leading-dot variant). The capture completes, and both outside files are byte-identical. *Red when:* a fixed temporary name is written with `write_text`.
* **A link swapped in while the person answers is refused at write time.** A prompt that replaces the mapping with a symbolic link as it "answers" makes the capture raise, and the outside file is byte-identical. *Red when:* the write-time guard is removed.
* **The mode bits survive, and nothing is left behind.** A mapping with mode `0o640` is `0o640` afterwards. If `os.replace` is made to fail, the temporary file is gone and the mapping is unchanged.
* **An unreadable mapping does not crash the install.** A non-UTF-8 mapping, a directory and a named pipe at the path: an interactive install exits 0, the file is unchanged, and the second notice text prints (C3).
* **A mapping that is already filled is never touched.** The hand-filled stub with its comments kept, interactive: the prompt is never called and the bytes are unchanged.
* **The asymmetry is pinned.** Non-interactive with a linked mapping: exit 0, the second text, nothing written. Interactive: exit 2, nothing written, no lockfile. Re-running the interactive install over that tree afterwards exits 0 and writes the lockfile.
* **Family, never a version** at the two engine sites: the prompt reads `<tier> tier -- model family, not a version (blank to skip):` and the header the capture writes carries one line saying so. The class from C2 gains both.
* **The inventory.** `capture_model_selection_mapping` and `_write_stage` are in `_GUARDED_WRITE_FUNCS`, and `test_guarded_write_functions_still_call_a_containment_guard` passes. `SECURITY_MUTATIONS.md` gains the capture's Class A row, stating both guards, the exclusive temporary file and the rename; its opening paragraph is corrected to the table above (no single catch, each caller chooses, everything else a traceback with exit 1). The `seed_gitignore` row is untouched. *Red when:* the capture's call to the guard is removed (`test_security_leaf` fails).
* **No new top-level symbol** beyond C3's two, so the AST delta is as declared.

### C5 -- The notice on adopt and upgrade

* **Five call sites,** listed from the tree (`grep` for `model_selection_notice_lines`): `main`, `_cmd_adopt_module`, and three in `cmd_upgrade`. Each prints for a stub and is silent for a filled mapping.
* **Adopt:** `--adopt-module model-selection` over a tree that has the stub prints the first text right after the "Adopted module" line. Adopting another module prints nothing. A refused adopt (a linked `.gitignore`) prints no notice.
* **`--plan` and `--stage`** print it as their last output, and are **silent on a tree where the file is absent** (the mapping that a delivering apply will add).
* **`--apply` prints it only after a successful apply.** The delivering apply: a tree whose mapping is absent from disk and from the lockfile is planned (silent), staged (silent), then applied; the file appears and the notice prints. A refused apply prints none: a leftover conflict marker (returns 1) and a linked `.gitignore` (exit 2). *Red when:* the call moves ahead of `_apply_upgrade`, or runs when the return code is not 0.
* **The notice sits outside the `try`.** A failure while printing it cannot be reported as an apply refusal.
* **A project without the module** gets neither text from `--plan`, `--stage` or `--apply`, nor from adopting another module (P1, CL-3).
* **Exit codes are unchanged** on every path in the table above; the existing refusal tests in `test_intents_tool.py` and `test_upgrade.py` pass unedited.
* **The quiet case is documented, not hidden.** If a step after the lockfile write refuses (the `.gitignore` seed for a newly added skill), the apply has delivered the file and exits 2, so no notice prints; the next `upgrade --plan` does.

### C6 -- Boundary B, the evidence, and the record

* **The record is complete,** with the template's fields, and it lists the new node IDs, the one node that left, and the AST derivation for the Maintainer's use: the CHANGED set and the digests of the two new symbols at the tested commit.
* **The mutation ledger** (*Verification*) is complete: every row has a result of killed, survived or equivalent, beside an unmutated control run. Equivalence is measured: a behaviour test through the real entry point passes under the mutation, and where another site is said to recover the value, mutating that site fails. An unmeasured equivalence is reported as a survivor. A survivor is fixed in its chunk, and the record is redone.
* **The stub merge measurement** (*Verification*) is recorded, with the three outcomes and the fail-closed apply.
* **The AST derivation matches the declared delta:** the set at the tested commit minus the set at its parent is exactly the delta in *Frozen files, AST and the oracle*, and no other symbol moved. The same four symbols the repair changed show the same classification.
* **The frozen list matches:** the six, derived by script, with the control.
* **The install contract is unchanged:** `scaffold.py --manifest` output is byte-identical to the parent's.
* **`git diff --stat` over the range** shows none of the files under *Not touched*, and `lockfile.py` as comment lines only.

### The security findings ledger

Every finding the accepted text carried into this plan, and where it is closed. Nothing is dropped.

| Finding | What the accepted text requires | Where it is checked |
|---|---|---|
| SEC-1 | the plan starts from a tree holding the `.gitignore` repair and makes no containment claim about it | the entry condition (C1's gate); C4 leaves the `seed_gitignore` row alone |
| SEC-2 | the upgrade notice after an action finishes: after `--plan` and `--stage` reports, after a successful `--apply` only; the delivering apply tested | C5 |
| SEC-3 | an early guard, a write-time guard, a temporary file beside the mapping, a guard on it, `os.replace`; the hard link named in S5 | C4; S5 below |
| CL-1 | the temporary file created exclusively, so a waiting hard link or link cannot redirect the write | C4 (`mkstemp`, the planted-names test); mutation M15 |
| SEC-4 | the true exit-code story; the capture's line a constant; the test proves the capture itself refused; the quiet side and the asymmetry stated; `SECURITY_MUTATIONS.md` corrected | *What the exit codes are now*; C4 |
| CL-2 | re-derive against HEAD; do not apply the old correction as written; keep the capture's catch with its constant line | the same section; C4 |
| SEC-5 | the residual named as a class; every value scanned; the bare row test anchored | C1; *Named residuals* below |
| CL-4 | both spellings in the corpus; widen the pattern or name them | C1 (P3) |
| SEC-6 | `lstat` first, never open a non-regular file; the capture treats an undecodable file as the helper does | C3, C4 |
| CL-3 | a missing mapping stays silent, first; a dangling link is not missing; the wording "That file was not changed" | C3 (P5), C5 |
| SEC-7 | a generated corpus; the U+2028 mutation; the version gap named | C1, C3; mutation M8; *Named residuals* |
| SEC-8 | the revisit note in `lockfile.py` answered in the comment; the file-type check at the call site; `_write_stage` in `_GUARDED_WRITE_FUNCS` | C3, C4 |
| Neutrality of the shipped text | every quoted shipped block scanned | measured here; `--sub neutrality` stays zero at every chunk |

## Scope delta

**Scope delta**: degraded -- one unit, **allowed by the Maintainer.** The baseline is the proposal as accepted. Every outcome maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| a notice on every install, including a no-terminal one | C3 |
| the notice on `--adopt-module` and on `upgrade --plan`, `--stage`, `--apply` (after a successful apply) | C5 |
| the II-5 item and the fourth allowed match | C2 |
| the check skips full-line comments; a mapping needs a row; values scanned with PyYAML; the anchored and widened row test; YAML line breaks | C1 |
| the seed and its Waiting row in two presets | C2 |
| Cairn's suite fails if its mapping returns to the stub | C1 |
| the capture refuses a link before any question, exits 2, writes by rename; the hard link and the planted name closed | C4 |
| the module document's paragraph and its corrected sentence | C2 |
| family, never a version, at every site, and the stub's example edit | C2, C3, C4 |
| the upgrade-conflict cost measured on the real commit | C6 |
| the true exit-code story and `SECURITY_MUTATIONS.md` corrected; `_write_stage` in the pinned set | C4 |
| the comment in `lockfile.py` | C3 |
| the named residuals recorded where a reader finds them | C1, C3 and *Named residuals* |
| the mutation ledger and the generated parity corpus | C1, C3, C6 |
| the scoped finalizes of the checker and the module document | C1, C2 |
| Boundary B full | C6 |

Not in the baseline: Q4, which the Decision left out of this contract.

* **The seed in `solo-greenfield`.** The opening text said "installs from a preset get one". That preset's own settings (`complexity: simple`) never select the module, so the seed could never render, and it would turn two pinned tests red. **disposition**: wontfix, for that reason. The outcome, a durable line, is delivered in the two presets that install the module; a solo adopter who raises complexity still gets the notice and the II-5 item. The Maintainer's allowance, quoted: the answer to Q2 was "Allow two presets", and the Decision was:

  > "accept as answered"

Additions, not removals: the `upgrade` notice, the II-5 item, the row requirement, the family wording, the module-document fix, the `lockfile.py` comment, the `RecursionError` catch (P8).

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own what it touches, found by searching `bootstrap/tests` for each touched symbol, file and flag, and not by expectation. All are in `bootstrap/tests/`. Plus the standing gates: `python scripts/check_cairn.py` and `python scripts/claim_check.py <file>` for each edited document; `python scripts/quality_gate.py --sub neutrality`; `--sub redundancy` for scripts; and `python bootstrap/verify_integrity.py --target .` after any finalize.

| Chunk | Tests |
|---|---|
| C1 | `test_model_selection_stub.py`, `test_scaffold.py` (module registration), `test_security_lint.py`, `test_security_check.py` (the Bandit gate sees the script) |
| C2 | `test_model_selection_stub.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_active_surfacing_render.py`, `test_trigger_evaluation_action.py`, `test_skills_onboarding.py`, `test_onboarding_review_tiers.py`, `test_onboarding_activation_helper.py`, `test_deferred_task_store.py`, `test_default_security_stance.py`, `test_profile_grammar.py`, `test_scaffold.py` |
| C3, C4 | `test_model_selection_stub.py`, `test_security_leaf.py`, `test_install_module.py`, `test_intents_tool.py` (the `.gitignore` refusals), `test_scaffold.py`, `test_ast_attest.py` (the same 2 nodes red, no more), `test_oracle.py`, `test_oracle_activation.py`, `test_lockfile_module.py`, `test_security_capability_install.py`, `test_security_verification.py` |
| C5 | the C3 and C4 set plus `test_upgrade.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_upgrade_side_door_parity.py`, `test_skills_upgrade.py`, `test_lockfile_provenance.py`, `test_security_stack.py`, `test_portable_security_sweeps.py` |

This is not a confident bound. 39 test files import the scaffold's entry point or its facade, and the engine files here sit on the install path of all of them, so **Boundary B is the real check.** If `board-as-basis` has landed first, add its contract test and `test_replacement_tools.py` to the C2 row, since the seed test reads the board's `--maintainer` output.

**Test classes this plan adds,** named for the property each pins. All are in `bootstrap/tests/test_model_selection_stub.py` unless noted.

* **C1:** `TestCommentsAreNotPlaceholders`, `TestAMappingNeedsAtLeastOneRow`, `TestParsedValuesAreScannedWhenYamlIsPresent`, `TestBarePathResidualIsPinned`, `TestValueScanVisitsEachObjectOnce`, `TestThisRepositorysMappingIsFilled`, and `TestEngineAndCheckerAgreeOnUnfilled` (the checker side; the engine side joins in C3).
* **C2:** `TestStubExampleNamesAFamilyNotAVersion`, `TestAcceptanceChecklistNamesTheMappingCheck`, `TestFamilyNotVersionReachesEverySite` (grows in C3 and C4). In `test_onboarding_seed_roster.py`: the seed renders at moderate and complex in the two presets, strips at simple, is absent from `solo-greenfield`, survives a removed module, is listed by `board.py --maintainer`, and a live install writes a clean lockfile.
* **C3:** `TestNoticeOnEveryInstallPath` (the install rows), `TestNoticeTextIgnoresFileContent`, `TestNoticeNeverOpensAnythingButARegularFile`.
* **C4:** `TestCaptureRefusesBeforeAskingAnything`, `TestCaptureWritesByReplacing`, `TestCaptureLeavesUnreadableMappingsAlone`, `TestCaptureNeverClobbersAHandFilledMapping`, `TestCaptureRefusalIsAConstantLine`.
* **C5:** `TestNoticeOnEveryInstallPath` gains the adopt and upgrade rows; `TestNoticeComesOnlyAfterAnApplySucceeds`.
* **Removed:** `TestFidelityCheck::test_fill_me_in_comment_fails`, replaced by `TestCommentsAreNotPlaceholders`.

**Boundary B mode**: **full.** The refusal rules in `AGENTS.md` settle it, four ways:

1. **A contract surface and the install path are touched.** `install.py`, `cli.py` and `upgrade.py` print new output on every install and upgrade, and the published `--manifest` and the lockfile must be shown unchanged. Bounded mode refuses.
2. **A trust-ceremony surface is touched.** The scaffold and merge engine is a high-risk surface that `AGENTS.md` names, and the work adds a containment guard and an exit-code change to it.
3. **A frozen file changes and the pinned collection moves.** Five frozen files change, one pinned node leaves, and new nodes join.
4. **A verbatim adopter script changes.** The checker is shipped byte for byte, so its behaviour reaches every adopter.

Uncertainty resolves to full, and the accepted text says full.

**How it runs.** After C5, against a clean, unchanged commit, under the canonical interpreter (Python 3.13.x, `/Users/kendal30/conda_envs/lhm/bin/python3.13`):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

then `check_cairn.py`, and `claim_check.py` on each edited file. Run it from a separate worktree at the tested commit: a worktree shares refs, so the gate anchor is present, and other sessions' uncommitted files stay out of the count. Name the interpreter next to every figure.

**Expected non-pass,** each disposed of rather than treated as noise:

* **`test_ast_attest.py`: the same 2 nodes** (`test_committed_baseline_accounted_for_across_the_engine_package` and `test_ast_gate_passes_over_the_full_scaffold_module_set`) fail, as they do at the base, and for the same reason: the baseline is stale. The disposition shows the CHANGED set equals the declared delta, so nothing unintended moved, and that the failure ends when the Maintainer runs the correction.
* **`test_gate_manifest.py`:** no expected failure. Changed frozen bytes do not redden it.
* **The neutrality leg:** `fail=0`, no expected failure.

**Mutation ledger.** Run in a separate copy of the tested commit (a detached worktree, in a fresh empty folder, never the shared tree), each mutant beside an unmutated control run. Sets are listed from the tree, not the diff.

| # | Mutant | Killed by |
|---|---|---|
| M1 | the checker stops skipping full-line comments | the hand-filled stub test |
| M2 | the checker treats a leading tab as blank | the tab members of the corpus |
| M3 | the checker uses `str.splitlines()` | the form-feed members of the corpus |
| M4 | the bare row requirement is dropped | the no-row test |
| M5 | the PyYAML value scan is dropped | the block-scalar, escape, binary and set cases |
| M6 | the visited-set is dropped | the alias-document timeout |
| M7 | the widened row pattern reverts to the anchored one | the two CL-4 spellings in the corpus |
| M8 | U+2028 is dropped from the engine's break set | the parity corpus |
| M9 | `model_selection_notice_lines` returns `[]` | the install, adopt and upgrade rows |
| M10 | the helper opens the path before `lstat` | the named-pipe test |
| M11 | the missing-file branch is dropped | the no-module rows |
| M12 | the early guard is removed from the capture | the refuse-before-asking tests |
| M13 | the write-time guard is removed | the swap-while-answering test |
| M14 | `os.replace` is swapped for `write_text` on the mapping | the hard-link test |
| M15 | `mkstemp` is swapped for `write_text` on a fixed temporary name | the planted-names test |
| M16 | the call is removed from one site at a time: `main`, adopt, plan, stage, apply (the set of five, from `grep`) | the matching row, five mutants |
| M17 | the apply notice moves before `_apply_upgrade` | the delivering-apply test |
| M18 | the apply notice prints when the return code is not 0 | the refused-apply test |
| M19 | the Waiting line is dropped from one preset's seed at a time | the board-listing test, two mutants |
| M20 | "never a version" is removed from one site at a time: the eight sites listed from the tree (stub, notice, capture prompt, capture header, II-5, both seeds, module paragraph) | the per-site parametrized test, eight mutants |
| M21 | Cairn's mapping is reset to the stub | the repository's-mapping test |
| M22 | the capture's guard is removed | `test_guarded_write_functions_still_call_a_containment_guard` |
| M23 | the capture's catch prints the exception text | the real-install refusal test |

**The stub merge measurement** (C6, on the real commit). The real merge, with the parent's stub as the common base and the edited stub as theirs, over four of the adopter's files: (a) an untouched stub; (b) a hand-filled stub with its comments kept; (c) a file written by the interactive capture, whose header was rewritten; (d) a file whose header was rewritten by hand. Expected: (a) and (b) clean, (c) and (d) conflict. Then, for (c), `upgrade --apply` refuses while conflict markers remain and writes nothing. The author measured this on the drafted edit; C6 repeats it on the commit.

**Smoke checks** (C6). `scaffold.py --config <profile> --target <tmp> --non-interactive` prints the first text. `upgrade --plan` on that tree prints it. `board.py --maintainer --root <tmp>` lists the seed. The II-5 vendor-neutrality grep over a scratch install holding Cairn's filled mapping matches only that file, which is the fourth allowed class. The checker returns 1, 0 and 0 on the stub, a hand-filled stub and Cairn's file. `scaffold.py --manifest` is byte-identical before and after.

**Boundary C** is the code reviewer's, run after Boundary B. The points worth attacking:

* **The order inside the capture.** Is any read, print or prompt reachable before the early guard? Does the temporary file get a name another process can predict?
* **The silent cases.** Can any path print the second text for a project that never had the module, or stay silent for a stub?
* **The parity corpus.** Is it fitted to a claim, or does it contain a member that the engine and the checker disagree on? List the corpus members from the tree.
* **The seed, read cold as an adopter.** Does the Waiting row make sense on day one, and does deleting it work?
* **The lockfile diff.** Confined to two records?

**Security preflight, re-answered where the chunking changes an answer.**

* **S2, can it fail.** The ledger above is the answer, and it runs once, at C6, against the finished commits. A surviving mutant sends the work back to its chunk.
* **S3, what fires it, over what.** The notice: `scaffold.py` install, `upgrade --adopt-module`, and `upgrade --plan`, `--stage` and `--apply`, over one fixed path. The check: an agent following II-5, a person running the script, `board.py --maintainer` showing the seeded row, and `TestThisRepositorysMappingIsFilled` in Cairn's suite. **Said plainly, nothing fires any of these unprompted.** Opened to the end: no git hook and no CI configuration runs the suite (`.git/hooks` holds only the work-intent pair, and Cairn has no CI). The test runs when a person or agent performs Boundary B, which every implementation plan requires, so its chain ends at a person or agent following `AGENTS.md`. The proposal's "only the suite reaches a machine" is therefore a test that exists, not a machine that runs it.
* **S5, who still wins.** Someone who can write the tree can enter plausible model names, edit the tree-local checker, or spell a placeholder so the bare path misses it. A link swapped in the last instant before the rename narrows the window to one rename and does not eliminate it; the threat model is "no concurrent filesystem attacker" (`bootstrap/SAFETY.md`, "Documented residual risks (Layer 4)"). **The hard-link case is closed by construction** (exclusive creation, then a rename that never writes into the old file).

### Named residuals

* **Staleness.** Nothing reads `date_verified` or the re-verification field; the module paragraph says so.
* **A class, not a case, on the bare path and in the engine:** a value whose `FILL ME` is not spelled out on one non-comment line (a block scalar, a value folded over lines, a continuation, an escape, a tag) reads as filled, and so does a repeated `mapping:` key. The engine erring toward "filled" never overwrites and may stay quiet. With PyYAML the checker catches the class. Each needs a deliberate spelling by someone who could edit the checker anyway.
* **The bare path is stricter than PyYAML** for a one-line list whose first key is not `tier` and for a `tier:` inside another value (P3). That is the louder side.
* **A version gap.** An adopter's checker is whatever they last upgraded to, while the engine is current. Between `upgrade --plan` and `--apply`, a hand-filled file can be silent in the new engine and fail the old checker. The apply updates the verbatim checker and closes it. A comment on `_mapping_is_unfilled` says where the other copy lives and which test pins their agreement.
* A `FILL ME` in a trailing comment fails; in a leading comment it passes. One tier filled passes, as the module document allows. Invented but plausible names pass.
* **The second notice line is imprecise for a file with no rows** (P10), and there is no read-size cap (P9).
* **A profile that removes the module from a moderate preset** gets a Waiting row naming a file it lacks; a test pins it.
* **Non-interactive and interactive installs disagree on a bad mapping path** (exit 0 with a notice, and exit 2). Neither writes anything.
* **The stub edit costs one merge conflict** for an adopter whose header was rewritten. `lhm` is one; keeping its side resolves it, and `--apply` refuses until then, so a half-merged mapping is never written.

## Dispositions

*Filled at archive-preparation.* Known now:

* **Q4, goodnight running the activation helper.** `defer`. The accepted text assigns it to the board: Revision 1 says "a separate board item at the next scrub, not in this change", and the Decision says it "is not part of this contract". The archive commit deposits the board row and quotes both, with the Decision's words "accept as answered". Until then this plan is its live home.
* **`_commit_lock_and_caches` writes through a pre-planted hard link at its fixed temporary name** (*Found while planning*). `defer`, as one batch with Q4 at archive. It needs the Maintainer's authorization quoted verbatim, so this plan does not deposit it. It reaches an adopter's machine only through local access, so it is not a release blocker.
* **The solo-greenfield seed.** `wontfix`, with the Maintainer's allowance quoted in *Scope delta*.
* **Whether the AST ceremony needs its own marked board row.** The Maintainer's call, raised in the report; if yes, the archive commit adds the row.
* **The archive commit writes this plan's `CHANGELOG.md` entry,** and adds the node note and the AST delta to the queued re-anchor row.
