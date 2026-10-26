# Remove untouched copies of retired files when a project upgrades

**Author**: Claude Sonnet 5.5 (Strategy; model id `claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) — the plan edits the scaffold engine (`bootstrap/_scaffold/`), a named high-risk surface, and adds the first engine code that deletes a file in a project
**Opened**: 2026-10-26
**In brief**: A new `upgrade` step deletes retired Cairn files a project never edited and clears the records of ones it already deleted, so tidying up stops breaking `--finalize` and the integrity check.

**The Maintainer's words.** This change started with his direction, not with an incident. The planning session asked him on 2026-10-26 whether to add it to 0.5, queue it after, or skip it (`dev/PLANNING.md:50`). His answer:

> "Add it to 0.5"

The same board row adds one scope condition from the onboarding Security Review (commit `0dceb28d`, its SR1): a modified copy is reported by name, kept in place, and never folded into a count; and a bare `--finalize` must not bless it. I adopt all three (Proposal, rules 2 and 6; parts 4 and 6).

**Authoring tier.** Doctrine puts proposal authoring at the medium tier (`doctrine/roles.md:174-180`), and Cairn's mapping gives that tier to Sonnet (`dev/.cairn/model-selection-mapping.yml:25-30`). I wrote at that tier and ran no separate high-tier premise check; the proposal review is that read.

## In brief

**Conclusion.** Add one `upgrade` action, `--remove-retired`. For each file on a short list inside Cairn's engine (11 today), it deletes the project's copy only if that copy is byte-for-byte what Cairn shipped, and it clears the lockfile record. A copy the project changed stays, with its record, and `--plan` and the step name it. A copy the project already deleted loses its record, and a bare `--finalize` clears that record too. Nothing is added to the install, the templates or the lockfile format.

### Your decisions

Five questions. Each has my default; an unanswered question takes it.

1. **Should Cairn keep its own list of the files it retired?** *Default: yes.* The engine carries 11 file pairs (source template, destination) and removes only files on the list. To delete safely, Cairn must know for itself what it stopped shipping, because a lockfile cannot say so: a cloned repository can carry any lockfile. I added a record naming an ordinary project file to a scratch lockfile, and `upgrade --plan` counted it as `removed-upstream` and raised no objection. The cost is one list row for each future retirement, added in the same change; a forgotten row leaves the file alone, which is today's behaviour. *Alternative:* treat every `removed-upstream` record as retired (Alternatives, 1). I reject it.
2. **Does `--apply` delete, or is deleting its own step?** *Default: its own step,* `upgrade --target <repo> --remove-retired`. `--plan` shows first what the step would do; `--apply` stays as it is. *Alternative:* delete inside `--apply`. That saves one command, but the most-used `upgrade` command would delete files for the first time. I would revisit after one release has used the step.
3. **What happens to a retired file the project changed, and to one it already deleted?** *Default:* a changed file stays, with its record, and is named one per line in `--plan` and in the step. A bare `--finalize` will not record the edit; `--finalize <path>` does, on purpose. A deleted file's record is cleared by the step and by `--finalize`, so tidying by hand is no longer punished. This reaches projects that already deleted the files.
4. **Does it also cover the 0.4 collaboration agreement file** (the one `bootstrap/UPGRADE.md:46` names)? *Default: yes,* beside the NEXT_SESSION copy and the nine onboarding files. Same defect, same rule; a changed copy stays. The price is two assertions in the frozen `bootstrap/tests/test_agreement_retired.py` (`:85`, `:109`), a file the onboarding change already edits. *Alternative:* leave the agreement as 0.4 left it.
5. **May the Decision say the rate-limit gate is not engaged?** *Default: yes.* The gate limits doctrine changes (`doctrine/rationale.md:433-453`). I found no doctrine file to edit (Documentation surface), so it may not apply at all. I ask as the model-tier proposal did, because your direction, not an incident, started this change; you answered yes there (`dev/proposals/archive/2026-10-26-claude-model-tier-rules.md`, Decision).

### What I found

* **Today a retired file is never removed and its record is never cleared** (measured, seven cases, Context). If a project deletes the files, a bare `upgrade --finalize` exits 1, also with `--force`, and `verify_integrity` prints one `missing:` line for each non-living-state file.
* **`removed-upstream` does not mean retired** (measured). A planted record is accepted, and `upgrade --plan --to v0.3.0` labelled five files that Cairn ships today as `removed-upstream`. That is why the list lives in the engine.
* **The proof that a copy is untouched is `base_hash`, not `hash`** (measured). `--finalize` rewrites `hash` from the disk, so a finalized edit looks untouched against `hash`.
* **The onboarding change leaves Cairn's own integrity check with nine new `missing:` lines** (measured on a scratch copy of HEAD, 0 before and 9 after). This change clears them. See "For the planning session" below.
* **Review declared:** `usual + Security Review`, a plan with `required(Internal + Internal Security Review)`, the deliberate lane, high assurance. Reasons are under Proposal 8.
* **Not checked:** I ran no test, read neither adopter repository, and measured one install profile. The full list is under "What I did not check".

**For the planning session, not a question.** The onboarding proposal (opening Context, inventory table) says Cairn's lockfile keeps nine orphan records "as it already does for the collaboration agreement". The analogy holds for the agreement because its record is living-state and the integrity check skips it (`bootstrap/verify_integrity.py:450-455`). The nine records are not living-state, so once the onboarding change deletes Cairn's own nine files the check reports them missing. The check is already red on that copy (23 `modified` lines, which I did not investigate), so this adds to a red check. The order is the Maintainer's. If it stands, the onboarding plan should record the nine lines as expected until this change lands.

## Context

**How I searched.** `git grep` for `removed-upstream` over the live tree finds the engine (`bootstrap/_scaffold/upgrade.py:360`, `:543`, `:883`), `bootstrap/UPGRADE.md:50` and one test (`bootstrap/tests/test_agreement_retired.py:96`); the control is the test's own line. For code that deletes, `git grep -n -E 'unlink|rmtree|os\.remove|rmdir' -- bootstrap/_scaffold` finds the review-area cleanup (`upgrade.py:1008`, `:2532`), temporary-file cleanup (`security.py:82`, `:104`; `upgrade.py:1622`) and the skills-link probe and swap (`install.py:527`, `:540`); each known use is a hit, so the pattern can match. **No existing code deletes a file the lockfile tracks.** I reuse these instead: `_check_lockfile_paths` and `_contained_lockfile_path` (`upgrade.py:166`, `:234`), `_assert_safe_write` (`security.py:110`), `_read_regular_bytes` (`security.py:29`), `_write_by_replacing` (`security.py:90`), `_sha256_hex` (`lockfile.py:121`), `_embedded_axes`, `substitute_tokens` and `strip_conditional_regions` (the rebuild at `upgrade.py:589-612`). New code is the list, a classifier (it sorts each retired record into the states in Proposal 3), the step and one guarded delete. I searched every file under `bootstrap/tests/` for the names and strings the touched code carries and marked which are among the 195 frozen files of the gate manifest; the result is under Inventory.

**Terms.** A *record* is one entry of `dev/.cairn/cairn-lock.yml`: source template (`src`), destination (`dst`), `hash` (the file's digest when last recorded), and for most files `base_hash` (the digest of what Cairn shipped). A *verbatim* file (a script) has no cached template; a *mergeable* file (Markdown) has one under `dev/.cairn/base/`. *Living-state* records (`lockfile.py:83`) are project-owned files the integrity check skips. *Retired* means Cairn stopped shipping the file. A *frozen file* has its checksum pinned in the gate manifest; editing one owes an entry in the *re-anchor*, the Maintainer's ceremony at the cut. The *AST baseline* pins the parsed structure of each engine symbol and is re-anchored in the same ceremony.

**The mechanism today** (read at `252e0392`).

* `_compute_upgrade` reads the project's file first (`upgrade.py:540`), then asks for the upstream template; if it is absent the plan is `removed-upstream` (`:541-545`). Nothing else decides "retired".
* The report prints one line per kind with the first six names (`:877-892`). It does not tell an edited copy from an untouched one.
* `--stage` never stages the kind (`_ADVANCING_KINDS`, `:369`) but checks every planned destination for links (`:1018-1019`). `--apply` copies unapplied records over unchanged (`:2423-2426`, `:2451-2492`).
* `--finalize` refuses when any tracked file is missing (`:2118-2123`, `:2139-2147`), skips the hash for living-state records (`:2124-2130`), and otherwise rewrites `hash` from the disk (`:2135-2138`). `verify_integrity` prints `missing:` for a gone file unless it is living-state (`bootstrap/verify_integrity.py:450-462`).
* **What the NEXT_SESSION path lacks:** the line prints and nothing more. There is no removal, no way to clear the record, and no way to tell a copy the project changed.

**Measured** (scratch, commit `b117ead8`; the folders were removed afterwards). I extracted `git archive` twice into fresh folders. One copy had the nine onboarding templates, the NEXT_SESSION template and its table row deleted and `_ALWAYS_ON_MAPPINGS` emptied; it is not the sibling changes, only a model of a file Cairn stopped shipping. A `collaborative-team` project installed by the first copy was committed in a scratch git repository, copied once per case, then upgraded by the second. Python 3.13.13.

| # | Case (retired files) | `--plan` | `--stage`, `--apply` | bare `--finalize`, also `--force` | `verify_integrity` |
|---|---|---|---|---|---|
| 1 | Untouched | one line, `removed-upstream 10` | exit 0 both; 68 records and every file unchanged; the line prints again | exit 0 | OK |
| 2 | Two scripts and NEXT_SESSION edited, committed | same line; the edits are not mentioned | exit 0 both; files kept | exit 0; `hash` of the two scripts advances, `base_hash` stays | OK |
| 3 | All ten deleted, committed | same line; says nothing about missing files | exit 0 both | **exit 1** ("10 tracked file(s) missing on disk"), also with `--force` | **exit 1**, 9 `missing:` (NEXT_SESSION is living-state) |
| 4 | One file replaced by a link to a file outside | exit 2, containment refusal | exit 2 | exit 2 | exit 1 |
| 5 | A folder above them replaced by a link outside | exit 2 | exit 2 | exit 2 | exit 1 |
| 6 | One file replaced by a link inside the project | exit 0, reads through the link | `--stage` exit 2 ("symlinked destination"), so no `--apply` | exit 0; records the digest of what the link points at | OK |
| 7 | A folder where a file was | traceback, `IsADirectoryError`, exit 1 (`upgrade.py:540`) | exit 1 | exit 1 ("missing") | exit 1 |

Rows 4 and 5 are the existing whole-lockfile containment check (`upgrade.py:234`, run at `:2762`); this change reuses it unchanged. Row 7 is a crash by line 540 for any tracked file; I measured only the retired case.

**Why `removed-upstream` cannot be the test** (measured, same scratch). (a) I added a record for `analysis.py`, a plain project file, with a `src` that exists nowhere and `base_hash` set to the file's own digest. `--plan` counted eleven `removed-upstream` records and refused nothing. A delete rule keyed on that label would delete the file. (b) A clone at `b117ead8` run with `--plan --to v0.3.0` labelled `NOTICE.md`, `dev/modules/security-verification.md`, the installed security-verification runner, `tools/board.py` and `tools/session.py` as `removed-upstream`, because `--to` judges against the older ref (`upgrade.py:331-339`). All five ship today.

**What proves a copy untouched.** `hash` cannot: `--finalize` (`upgrade.py:2135-2138`) and `--init-lock` (`:1480`) write it from the disk. `base_hash` can: install writes it from the shipped template (`install.py:2065`) or the shipped script (`:2073`), `--apply` rewrites it from the applied upstream bytes (`upgrade.py:2470-2491`), and `--finalize` only fills it in when absent (`:2133-2134`). Measured: after an edit and a finalize, `hash` matched the edit and `base_hash` matched the original. For a mergeable copy I rebuilt the installed text from its cached template, the lockfile tokens and the embedded profile; on NEXT_SESSION it matched the file byte for byte when untouched and did not after one line was added.

**Cairn's own tree** (read at `252e0392`). The lockfile has 73 records. Eleven are for files Cairn retired or is retiring: the nine onboarding files (verbatim, with `base_hash`), NEXT_SESSION and the agreement (mergeable, living-state, `unrecoverable_base`, no cached template). The agreement file is already gone, and a bare `--finalize` on Cairn's tree already refuses for it (the NEXT_SESSION proposal's R6).

## Proposal

One new action, one engine list, no template, install row or lockfile field.

**1. The list.** `bootstrap/_scaffold/config.py` gains a tuple of `(src, dst)` pairs (proposed name `_RETIRED_INSTALLS`), beside `_CORE_MAPPINGS`. It holds 11 pairs: the agreement, NEXT_SESSION, and the nine onboarding files. A record is *retired* only if its `src` and its `dst` both equal a pair on the list **and** its template is absent from the running Cairn tree. Any other `removed-upstream` record is reported as today and never touched. A test pins that no pair is still shipped (no `src` under `templates/`, no `dst` among the `install_manifest()` destinations), so a bad row cannot delete a live file.

**2. What "untouched" means.** The copy must equal what Cairn shipped:

* *Verbatim record:* the file's SHA-256 equals `base_hash`. No `base_hash`: keep.
* *Mergeable record:* the file equals the text rebuilt from the cached template (a regular file inside the project whose own digest equals `base_hash`), the lockfile tokens and the embedded profile, by the same calls `_compute_upgrade` uses (`:589-612`). No cached template (`unrecoverable_base`): keep.
* `hash` is never the evidence.

**3. The step.** `scaffold.py upgrade --target <repo> --remove-retired` runs after the existing lockfile checks, as `--finalize` does (`upgrade.py:2762-2769`), so it inherits the containment check, the `.git` rule and the linked-lockfile refusal. It joins the mutually exclusive actions (`:2674-2687`). It classifies each retired record and acts on it:

| State | Meaning | Action |
|---|---|---|
| untouched | a regular file, equal to what Cairn shipped | remove the file (and, for a mergeable copy, its cached template); clear the record |
| gone | nothing at the name | clear the record |
| changed | differs from what Cairn shipped | keep file and record; name it |
| cannot tell | no `base_hash`, no usable cached template | keep file and record; name it |
| blocked | a link at the name or above it, or a folder, device or other non-file | keep; name it; read nothing through it |

It asks no question: `--plan` is the preview, and it is read-only. The step prints one line per record, the summary last, and says to commit the removal. Nothing to do is exit 0. A kept file is not an error.

**Rules, as rules.**

1. **Only the list decides what may be removed.** A lockfile record can add a name to nothing.
2. **Only an untouched copy is removed.** Changed, unreadable, unprovable and blocked copies are kept. A copy that cannot be proven unchanged is treated as changed.
3. **Never through or outside a link.** The name and every folder above it must pass `_assert_safe_write` (no link, inside the project); the file is opened without following links and must be a regular file. A name that fails is kept and reported. Nothing outside the project is read or removed.
4. **Judged twice.** The bytes are compared when the state is decided and again just before removal, on the same file (device and inode). Any mismatch keeps the file.
5. **Files first, lockfile last.** The lockfile is replaced after the files are gone (`_write_by_replacing`). A run that stops halfway leaves "file gone, record kept", and the next run clears the record.
6. **A changed copy is named, kept, and never blessed.** It is listed by name, one per line, never inside a count (`--plan` and the step). Only an explicit `--finalize <path>` records an edit to it.
7. **Running tree only.** `--remove-retired` refuses `--to`, as `--adopt-collisions` does (`upgrade.py:2773-2776`).
8. **Nothing else is deleted.** No other file, no pattern, no recursion. After a removal, the file's folder goes if it is now empty, and only that one folder. Files the lockfile does not name (the activation log, the profile copy, `__pycache__`) stay.

**4. `--plan` shows it first.** `_compute_upgrade` no longer reads the project's file before it knows the record is retired (the classifier reads it safely; this ends the crash in row 7) and emits three kinds in place of `removed-upstream` for list records: *retired, never edited*, *retired, already deleted* and *retired, kept*. Every kept file also gets its own `[flag]` line with the reason, not cut to six names. The report ends with the command to run. `removed-upstream` stays for records not on the list. `--stage` and `--apply` treat the new kinds as they treat `removed-upstream` now: never staged, records carried over. `--plan` writes nothing, as today.

**5. A test that the plan and the step agree.** The names `--plan` calls removable are exactly the files the step removes, on the same tree.

**6. `--finalize`.** (a) For a retired record whose file is gone, `--finalize` clears the record instead of refusing with "missing on disk", and says so. (b) For a retired record whose file is present and not provably untouched, and whose hash `--finalize` would advance (not a living-state record, which it already skips), a bare `--finalize` skips it, leaves its `hash`, and prints its name with "retired file you changed; not recorded; `--finalize <path>` records it, or restore it from history". The scoped form `--finalize <path>` records it as today and prints one line saying so. `verify_integrity` is untouched and keeps reporting the edit until then. This answers the onboarding Security Review's measurement that a bare finalize records a committed edit to an old helper.

**7. Docs and Cairn's own tree.** `bootstrap/UPGRADE.md` gets one section, "Files Cairn stopped shipping", in place of the agreement section (`:46-75`) and the two sections the sibling changes add: what `--plan` shows, what the step does, what stays, and "commit the removal; `git restore <path>` brings back a file you want". `bootstrap/_scaffold/SECURITY_MUTATIONS.md` gets the delete in Class A and the classifier's reads in Class D. The changelog gets one entry from the plan's owner at the serialization point. After this lands, one run of the step on Cairn's own tree is an acceptance check: it should clear the 11 records and leave `verify_integrity` free of the nine `missing:` lines.

**8. Order and headers.** This change lands last, after the NEXT_SESSION and onboarding changes (`dev/PLANNING.md:50`). *Review: usual + Security Review*, because it edits the scaffold engine and deletes files in a project, the first bullet of "High-risk surfaces" in `AGENTS.md`, and a one-line engine change already takes a Security Review there. *Plan review: required(Internal + Internal Security Review)*, because the plan edits the same surface and its code review must carry the falsification ledger. *Lane: deliberate* (`doctrine/lifecycle.md:47-58`): it touches a high-risk surface and widens a contract with a new action. A plan is needed (`doctrine/plans.md:175`): many files and areas. Boundary B (the verification run the plan records before code review) is `full`, because the engine is a high-risk surface and bounded mode refuses; it is recorded `Certified by: pending` until the next certifying run. Nobody sets `CAIRN_FULL_SUITE=1` for this change.

Proposed paths:
* `bootstrap/tests/test_upgrade_removes_retired_files.py`
* `bootstrap/tests/test_install_time_onboarding.py`

## Rationale

The Maintainer asked for it, and the measurements show the cost of waiting. Every existing project keeps nine unmaintained executables and a repeating `removed-upstream` line, and the one tidy-up an adopter can do, deleting the files, makes `--finalize` and the integrity check fail. The design spends its care on one question, which file may be deleted. It answers with two independent proofs: Cairn's own list says the path is retired, and the project's `base_hash` says the bytes are Cairn's. Either alone is weaker. The list alone could delete an edited file. The digest alone could delete any project file a lockfile names.

## Alternatives considered

1. **No list: remove any `removed-upstream` record whose bytes match its digest (the strongest alternative I rejected).** It is the simplest, and it needs no upkeep when Cairn retires a file. It loses on two measured facts: a record the project wrote is accepted for any project file (a, above), and `--to` makes shipped files look removed (b). Both let a hostile or merely wrong lockfile name what gets deleted.
2. **Do nothing; document that adopters leave the files.** It costs nothing in code. The files stay forever in every project, `--plan` repeats the line on every run, and the sibling guides already tell adopters not to delete them. It is what 0.4 did for the agreement, and the board row exists because the Maintainer does not want that to continue.
3. **Tell adopters to delete the files and edit the lockfile by hand.** It works: I deleted the ten records from a scratch copy with the engine's own reader and writer, and `--finalize` exited 0, `verify_integrity` passed and the line vanished. I did not try a text edit. But the lockfile's own header says "tool-owned; regenerate-only; do not hand-edit" and `verify_integrity` attests against it, so the fix is to edit the thing the check trusts, ten records at a time, by people who may drop another one.
4. **Only clear the record when the file is already gone.** This is smaller and safer: no delete, no proof of "untouched", no new guarded primitive. It cures the punishment. It does not remove the stale executables, because adopters must delete the files themselves, and most will not: they do nothing. My design keeps this path separable: the "gone" row of the table does not depend on the delete. If the Security Review does not clear the delete, this is the fallback; it narrows the Maintainer's row and so needs his word, not mine.
5. **Delete inside `--apply`.** One command fewer. It changes the meaning of the most-used command and ties removal to a complete upgrade (no conflicts, no review-only files). I recommend a separate step first (Question 2).
6. **Mark kept files as the project's own (drop the record, keep the file).** It ends the repeating line. It also removes an edited executable from the integrity check, and the check then cannot see a later tamper. Rejected: a kept file stays attested.

## What this does not do

* It removes only files the lockfile names. Three untracked leftovers from the onboarding change (the tour-page copy, the profile copy and the activation log, named in the onboarding Security Review, SR2) are not covered; they are safe to delete by hand.
* It never removes a changed copy. Those stay, named, until the project deletes or restores them.
* It does not make retirement automatic: each future retirement needs one list row.
* It does not change `verify_integrity.py`, the lockfile format, the templates or the install.

## Documentation / doctrine surface

Routed by layer, per `docs/DOCUMENTATION_PLAN.md`. *Descriptive layer:* `bootstrap/UPGRADE.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, the `--help` text of the new flag, and the changelog entry. No governing doctrine changes: `git grep -i -I -e removed-upstream -e 'stopped shipping' -e 'lock record' -- doctrine templates docs on-ramp AGENTS.md README.md bootstrap/BOOTSTRAP.md` finds nothing that describes this behaviour (the control is `bootstrap/UPGRADE.md:50`, outside that path set). `bootstrap/SAFETY.md` I read for upgrade and delete wording and found none to change today. The accepted onboarding change adds a sentence there saying pre-0.5 installs keep the retired helper "until the 12th row removes it"; this change rewrites that sentence to name `upgrade --remove-retired`. The new sentences name no model or vendor.

## Evidence / verification plan

Cairn has no CI; a person triggers every check below.

| Surface | Check | What triggers it |
|---|---|---|
| Edited Markdown | `python scripts/check_cairn.py`; `python scripts/claim_check.py <file>`; `python scripts/link_check.py <file>` | a person, before commit |
| Neutrality | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | a person; the certifying run before a push |
| The step and the report | the new test file (below) | `pytest`, scoped by the implementer |
| Containment of the new action | the new action joins `_ACTIONS` in the containment sweep (Inventory) | `pytest` |
| Engine symbols and frozen files | `bootstrap/tests/_ast_attest.py verify`; `bootstrap/tests/_gate_manifest.py verify` | a person, in the Maintainer's re-anchor |
| Adopter-facing sentence | **a reviewer reading `UPGRADE.md`** against the printed lines | a person |

### Tests required

New file `bootstrap/tests/test_upgrade_removes_retired_files.py`, driving the real `scaffold.py` over a real install, as `bootstrap/tests/test_agreement_retired.py:28-69` does. One node per property; each has a one-line mutant that the plan's ledger runs beside an unmutated control.

| Property | Mutant |
|---|---|
| An untouched verbatim copy is removed, its record cleared, `verify_integrity` passes | compare against `hash` instead of `base_hash`: the edit-then-finalize case must fail |
| A changed copy, including a finalized edit, is kept and named by name; bare `--finalize` does not advance its `hash`; `--finalize <path>` does | drop the name from the report; let bare finalize advance it |
| An untouched mergeable copy (NEXT_SESSION) goes with its cached template; one added line keeps it | rebuild from `hash` |
| No `base_hash`, or `unrecoverable_base`: kept | treat absence as untouched |
| A planted record for a plain project file is never removed | delete the list check |
| A link at the name, a linked folder above, a folder in place: kept, nothing outside touched | delete the `_assert_safe_write` call |
| Bytes change between the decision and the removal: kept | skip the second read |
| A deleted file's record is cleared by the step and by bare `--finalize` | restore the refusal |
| A stop after the files and before the lockfile write: the rerun clears the record | write the lockfile first |
| `--to` refused; a hostile lockfile refused | accept `--to` |
| The list is consistent (no pair still shipped) | add a shipped pair |
| An emptied folder goes; a non-empty one stays | remove recursively |
| `--plan` names exactly the files the step removes | let the step remove one more |

Existing frozen tests that need edits are listed under Inventory. The plan's mapping owns the scoped list; unknown scope falls back to the certifying run. Boundary B is `full` (engine, install contract and frozen files).

### Examples / smoke checks

`python bootstrap/scaffold.py upgrade --target <scratch> --plan` and `--remove-retired` over the scratch project above, and then over a copy of Cairn's own tree after the siblings land.

#### Security preflight

* **S1 — Who supplied it?** The step decides two things. *Which path may go:* the engine list, supplied by Cairn's source tree, not by the project. *Whether the bytes are Cairn's:* the file and the record's `base_hash`, `base_cache` and tokens, all supplied by the project, the thing being decided about. So a project, or a repository it cloned, can make a changed file look untouched and have it removed. The loss is bounded to a file at a retired path that Cairn no longer ships; the list is what bounds it.
* **S2 — Can it fail?** Each check has a one-line mutant in the table above. The mutants for the list, the digest and the link check are not derived from the object they check. I ran none of them; the test file does not exist. Measured only: the `hash`/`base_hash` difference and the planted-record acceptance.
* **S3 — What fires it, over what?** A person runs `scaffold.py upgrade --remove-retired` (and `--plan` before it). It covers records whose pair is on the list and whose template is absent from the running tree. The sentence `UPGRADE.md` gives adopters ("run `--remove-retired`") must match the line `--plan` prints; a test pins that both name the flag.
* **S4 — Which way does it break?** Every parse, read and comparison failure lands on *keep*: less authority. A crash between files and lockfile leaves a record for a gone file, which the next run clears. The one path to more authority is a wrong list row; the consistency test and the "template absent" condition both block a still-shipped path.
* **S5 — Who still wins?** I assume an attacker who can edit the committed project, lockfile included. They can still edit a retired file and its `base_hash` together, and the operator's run then removes that file; it is recoverable from git history if it was committed, and it sits at a path Cairn no longer ships. A process on the machine that swaps the file, or a parent folder for a link, between the second read and the unlink can still win; this is the Layer-4 model `bootstrap/SAFETY.md` accepts for writes, and a delete is the same exposure. Whether to narrow it with a folder-relative unlink where the platform has one (`os.unlink(..., dir_fd=...)`, not on Windows) is a question for the Security Review. The class is closed by enumeration (the list), not by construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Inventory

*Engine, proposed names (`bootstrap/_scaffold/`).* **New, 4:** the list (`config.py`, `Assign:_RETIRED_INSTALLS`); a classifier for retired records (`upgrade.py`, used by `_compute_upgrade`, the step and `--finalize`); the step (`upgrade.py`, `_cmd_remove_retired`); one guarded delete (`security.py`, the leaf that owns every other adopter-tree mutation; it checks the name and the bytes again, then removes the file). **Changed, 5:** `_compute_upgrade`, `_KIND_DISPLAY_LABEL`, `_print_upgrade_report`, `cmd_upgrade`, `_cmd_finalize_lockfile`. Three of the five (`_print_upgrade_report`, `cmd_upgrade`, `_cmd_finalize_lockfile`) are already in today's 12 changed symbols (runbook step 1 on a scratch HEAD extraction); `_compute_upgrade` and `_KIND_DISPLAY_LABEL` are also changed by the onboarding change. None of my symbols is in `_UPDATE_ALLOWLIST` (`bootstrap/tests/_ast_attest.py:143`), so the AST correction is the Maintainer's run. I delete no pinned symbol.

*Shipped files.* None. No template, no manifest row, no lockfile field; `scaffold.py --manifest` is unchanged. Existing projects meet the change when they update their Cairn checkout.

*Docs.* `bootstrap/UPGRADE.md` (including the accepted onboarding section: its "do not delete" and "run `verify_integrity` before `--finalize`" advice no longer holds for retired files, and the NEXT_SESSION section must keep promising nothing it does not do); `bootstrap/SAFETY.md` (one sentence, above); `bootstrap/_scaffold/SECURITY_MUTATIONS.md`; `CHANGELOG.md`. I do not edit `dev/PLANNING.md`.

*Tests (searched by the names and strings the touched code carries, 14 patterns over `bootstrap/tests/*.py`; control: `removed-upstream` finds `test_agreement_retired.py`).*

* **Frozen, edited:** `test_upgrade_lockfile_path_containment.py` (add the action to `_ACTIONS`, `:67-74`, so the "every action refuses a bad record" sweep covers it); `test_security_leaf.py` (add the step to `_GUARDED_WRITE_FUNCS`, `:32`); `test_agreement_retired.py` (the two assertions, if Question 4 is yes; the onboarding change edits this file too).
* **Not frozen, no re-anchor:** `test_upgrade_refuses_hostile_project_data.py`, `test_upgrade_added_slots.py`.
* **Frozen, scoped runs only:** `test_upgrade.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_upgrade_side_door_parity.py`, `test_skills_upgrade.py` (they call `_compute_upgrade`); `test_verify_integrity.py` and `test_review_stance_in_shipped_files.py` (they read `UPGRADE.md`).
* **New:** `bootstrap/tests/test_upgrade_removes_retired_files.py`; it freezes at the cut.
* **Written by the onboarding change, edited here:** `bootstrap/tests/test_install_time_onboarding.py` pins the guide's "do not delete" and loose-files sentences and runs bare `--finalize` over untouched copies. This change rewrites the first, and keeps the second and the exit-0 results true. That file is new and unfrozen until the cut, so the edit costs no frozen entry if this lands before it.

*Install contract.* Lockfile schema: unchanged (records are dropped, none added, no new key). Published `--manifest`: unchanged. Fidelity manifest: unchanged (`bootstrap/fidelity-check.md:28` mentions `--finalize` only as context). Gate manifest: the edits above. `bootstrap/verify_integrity.py`, a frozen trust anchor, is untouched.

*Differential oracle.* This change touches one sensitive-roster entry, `bootstrap/_scaffold/` (`bootstrap/tests/_oracle_activation.py:34-37`); the plan names it, as `dev/plans/archive/model-mapping-install-path.md` did. The oracle compares fresh installs, which this change does not alter; I expect it unmoved and have not run it.

*Re-anchor sets, as formulas* (the planning session re-derives the final sets at the cut with `verify`). **AST:** changed set at the landing tree = the owed set there ∪ {`_compute_upgrade`, `_KIND_DISPLAY_LABEL`, `_print_upgrade_report`, `cmd_upgrade`, `_cmd_finalize_lockfile`}; new = the four above; dropped or rekeyed keys from this change = none. The implementer does not edit the AST fixtures; the plan lists these keys for the Maintainer's run (`bootstrap/AST_BASELINE_RUNBOOK.md`, step 3 onward). **Gate manifest:** the owed set at the landing tree ∪ {`test_upgrade_lockfile_path_containment.py`, `test_security_leaf.py`} ∪ {`test_agreement_retired.py`, if not already there from the onboarding change} ∪ {the new test file}; no frozen file deleted, no collected node dropped. Whoever implements records their own pins from the landed tree.

## What I did not check

* I ran no test and no suite, and implemented nothing. The only runs were the scratch measurements above and the runbook's read-only symbol count.
* I measured one profile (`collaborative-team`) and a model of the retirement, not the sibling changes themselves.
* I never built an agreement-era mergeable record, so the mergeable proof is measured on NEXT_SESSION only.
* I did not read either adopter repository, so I do not know how many adopter lockfiles lack `base_hash`; those copies would be kept.
* I did not test the race (rule 4), hard links, Windows, or a case-insensitive disk. I did not run the differential oracle.
* The edit-by-hand alternative (3) was done with the engine's reader and writer, not a text editor.
* I prototyped nothing: the step, the three plan kinds and the `--finalize` changes are design (expected behaviour), not measured behaviour.
* The 23 `modified` lines in Cairn's own integrity check, and the working-tree edit to `upgrade.py` another session has open, I did not investigate; my line numbers are at `252e0392`.

**Found on the way, not changed here.** Row 7 shows a traceback when a folder stands where any tracked file was (`upgrade.py:540`); this change ends it only for retired records. Row 6 shows that a retired file replaced by an in-project link blocks `--stage` for the whole upgrade (`:1018-1019`).

## Signals the change is wrong

* A project reports a changed file removed, or any removal of a file whose bytes were not what Cairn shipped. That withdraws the "untouched" rule.
* The Security Review finds a way to reach a path off the list, or through a link. I would withdraw the step and offer Alternative 4 instead.
* A still-shipped path appears on the list; the consistency test should stop it.
* `--plan` names one set of files and the step removes another.
* Retirements keep coming and rows are forgotten, so files stay. Then the list needs a generator or a check that fires when a template is deleted; I have no such check now.
* The step is run by almost nobody. I cannot measure that: Cairn collects no usage data from adopters.

## Scope delta

**Scope delta**: preserved (opening revision; nothing removed).

The board row's outcome, removing untouched copies of files Cairn stopped shipping, is delivered for all 11 files Cairn has stopped shipping so far. Two limits are recorded, not conceded. Only files on the engine list are removable (Question 1). Untracked leftovers are out of reach (What this does not do). The row's added condition (SR1) is met by rules 2 and 6 and parts 4 and 6.

## Assurance path

**Assurance path**: high-assurance

The change touches the scaffold engine and a frozen gate set, and it deletes files in a project's tree. The engine and the gate set are in the template's trigger list (`dev/proposals/_template.md`, "Assurance path"); uncertainty resolves to high-assurance.
