# Plan: Make the next-session handoff a local note

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-next-session-local-note.md](../proposals/archive/2026-10-26-claude-next-session-local-note.md)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-26
**In brief**: Cairn stops shipping the file that tells the next work session where to start; the owner writes a short local note instead, so a stale tracked copy can no longer mislead an agent.

The Internal Security Review is a separate pass from the ordinary plan review, and the ordinary pass never clears it. The plan edits a row of the installer's core-file table, an engine file, and one line in `bootstrap/_scaffold/config.py`, which the differential oracle's roster covers.

## Source proposal

Accepted 2026-10-26 as revised. **Revision 3 is the contract**; it supersedes Revisions 1 and 2. Seven proposals: stop shipping the file; the local note and its rules; the read side; the `verify_stems.py` skip; what existing projects are told; Cairn's own tree; counts and sequence. The Decision's answers 1-3 and 5-7 take their defaults. **Answer 4 differs:** an upgrade is to remove an untouched `dev/NEXT_SESSION.md` and clear its lockfile record; a changed copy is named and left. That is the engine change of the twelfth 0.5 row, which lands **after** this change and after onboarding. So this plan's text for existing projects says what is true at landing: the project keeps its file until that change ships, and once it ships an untouched copy is removed. It promises nothing earlier. SR5 (promise nothing for the twelfth row) is superseded by that answer.

## Scope

**In.** Revision 3's Proposals 1 to 7, as the chunks below. **Out.** Any tool that reads or writes the note, the twelfth row's engine change, onboarding, pushing, and `scaffold_ast_known_new.json` and the AST baseline (the implementer never edits them).

**Reuse.** Searched `git grep -l 'removed-upstream' -- bootstrap/tests` (finds only `test_agreement_retired.py`, the model for the new test file, so the pattern can match) and `git grep -n -i -I -E 'next[_-]session'` over the tracked tree minus history (the proposal's search; it finds the template, so it can match). Reused: the `removed-upstream` path and `_LIVING_STATE_DSTS` as they are; the reflections ignore line (`.gitignore:9`). No new function, option or ignore pattern.

**Doctrine surface.** Governing layer (`AGENTS.md`, both copies) and `doctrine/session-routines.md`, whose handoff section keeps its rewrite rule and five-element shape and gains Revision 3's paragraph (Proposal 2, verbatim). The doctrine files `plans.md`, `proposals.md` and `doc-governance.md` that call the file a home get a reworded sentence. Rate-limit gate: not engaged (Decision, question 6).

**Frozen files, derived** from `_frozen_files` in `bootstrap/tests/_gate_manifest.py` (globs `bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`, `templates/modules/**/*.py`) and the `frozen_files` keys of `bootstrap/tests/fixtures/gate_manifest.json`. `python bootstrap/tests/_gate_manifest.py verify --no-collect` on 2026-10-26 already lists `FROZEN-MODIFIED` for other files, so "owes a re-anchor" below means this change adds an entry.

| File | Chunk | Effect |
|---|---|---|
| `bootstrap/tests/test_next_session_local_note.py` (new) | C1-C5 | glob match, no keyed entry: `FROZEN-NEW`, allowed |
| `scripts/verify_stems.py`, `templates/modules/default-on/verify_stems.py` | C4 | keyed, edited: **re-anchor owed** (two new entries) |
| `bootstrap/tests/test_notice_install.py` (:184 pin), `bootstrap/tests/test_upgrade.py` (:1795 assertion) | C1 | keyed, edited: **re-anchor owed** |
| `bootstrap/tests/test_quickstart_sequence.py` (:197 path list) | C1 | keyed, edited: re-anchor owed; already `FROZEN-MODIFIED` today, so no new entry |
| `bootstrap/tests/test_review_stance_in_shipped_files.py` | C1 | file **not edited**; its parametrized node `[templates-core-dev-NEXT_SESSION.md]` disappears with the template: `COLLECTION-DROPPED` |
| `bootstrap/tests/test_verify_stems.py` | C4 | keyed, not edited (its fixture at :79 writes a regular file); must still pass |
| `bootstrap/_scaffold/config.py`, `lockfile.py` | C1 | not frozen (a subfolder is outside `bootstrap/*.py`); AST-attested; `config.py` is on the oracle's sensitive roster (`_oracle_activation.py:34-47`) |
| both `session.py`, both `AGENTS.md`, all four skills, the doctrine and docs | C2-C6 | not frozen |

The planning session re-derives every set at the cut with `verify`; none of these figures is carried forward.

## Sequence

How to work: directly on `0.5-dev`. **Every chunk's first criterion** has three parts. (a) `python tools/intent.py list` shows no other claim on the chunk's files; the chunk's own claim names `dev/.cairn/cairn-lock.yml` too, and the lockfile is committed by path with the file it records. If another session's claim covers a chunk file (on 2026-10-26: `docs/quickstart.md`, a C1 file, held since 2026-10-19 by `claude-e4f56026`, action `rename-slug`, many files), the implementer reports it to the planning session and waits; it never overrides or releases another session's claim. (b) Before the chunk's first edit, list its finalize targets that `python bootstrap/verify_integrity.py --target .` already reports as hash mismatches (on 2026-10-26: `tools/session.py`, both `.agents/skills/` skills, `dev/README.md`, `docs/DOCUMENTATION_PLAN.md`; `scripts/verify_stems.py`, `dev/reflections/README.md`, `dev/agent_collaboration.md` and `AGENTS.md` match). For each, find the last commit whose bytes match the record's `hash` (`git log --format=%h -- <path>`; `sha256` of `git show <commit>:<path>`; measured for `tools/session.py`: `7832d057`) and read `git diff <that commit> HEAD -- <path>`. Found: the earlier edits are read and named in the commit body, then finalized with the chunk's own. Not found: the commit author of the earlier edit is named, and the finalize waits for that owner's word or the earlier edit is recorded in the commit body as unverified. (c) Before the `AGENTS.md` and `session.py` edits (C2, C3), the Plain Language `--finalize` and the security-findings fixer have landed: the two rows at `dev/PLANNING.md:39` and `:44` no longer say "handed to an implementation agent" or "a fixer answers", and `intent.py list` shows no claim on `AGENTS.md`, `dev/agent_collaboration.md`, `tools/session.py` or `bootstrap/_scaffold/`; if unsure, ask the planning session. Commit by explicit path; the two `session.py` copies stay byte-identical; both `verify_stems.py` twins stay byte-identical. Order is C1 to C6, then C7. This change lands first, then onboarding (it re-derives its pins from the tree after this lands), then the twelfth row.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Stop shipping: delete `templates/core/dev/NEXT_SESSION.md` and the `config.py:549` row; keep the living-state entry; reword the two comments (`config.py:756`, `lockfile.py:62`); update `bootstrap/fidelity-check.md:142`, `bootstrap/BOOTSTRAP.md:507`, `:631`, `docs/quickstart.md:298`; the three pinned tests | none | engine row, install contract |
| C2 | The note's rules, write side: `doctrine/session-routines.md` paragraph and `:113-115`; Goodnight bullet of both `AGENTS.md` and the landmark list of the root `AGENTS.md` only (`templates/core/AGENTS.md` has none); both `session-end` skills; `agent_collaboration.md` and its template; three `session.py` strings; both reflections READMEs; the other prose that names the file (`dev/README.md` and template, both `dev-tour.md`, `documentation_plan_template.md` and `docs/DOCUMENTATION_PLAN.md`; every spot in `plans.md:1031, 1034`, `proposals.md:135, 350, 382, 385` and `doc-governance.md`) | none | doctrine, prose |
| C3 | The read side: Session start bullet of both `AGENTS.md`; step 3 of both `session-start` skills; one cold-start probe | none | skills, `AGENTS.md` |
| C4 | `verify_stems.py` skip, both twins | none | a verbatim script |
| C5 | `bootstrap/UPGRADE.md`: the new section and the agreement-section defect fix | none | adopter guide |
| C6 | Cairn's own tree: read the whole file, table of each section's durable content and home, then `git rm dev/NEXT_SESSION.md` last | none | the proof tree |
| C7 | The AST attestation and gate-manifest re-anchors at the cut | **MAINTAINER-ONLY**, not scheduled for an agent | re-pinned checksums |

**C7 fence.** The Maintainer's authorization at the cut must name `bootstrap/_scaffold/config.py` (oracle-sensitive roster, SR4; the roster entry is the whole `bootstrap/_scaffold/` directory) and every `bootstrap/_scaffold/` file changed since `refs/cairn/gate-anchor`, including `lockfile.py`, listed at the cut with `git diff --name-only refs/cairn/gate-anchor HEAD -- bootstrap/_scaffold/`; if one is missed the gate stays shut and does not pass. `Assign:_CORE_MAPPINGS` is the one new AST change. The implementer never edits `scaffold_ast_known_new.json` or the AST baseline. When work reaches C7, write `**Waiting on Maintainer**: re-anchor at the cut`. `test_ast_attest` is red until then, by design.

## Acceptance criteria

Each criterion names a test or command; refusals have a control that passes. Test nodes are in `bootstrap/tests/test_next_session_local_note.py` (modelled on `test_agreement_retired.py:72-121`), named for the property they pin. Proposed paths: the new test file and the local note, neither of which exists yet.

Proposed paths:
* `bootstrap/tests/test_next_session_local_note.py`
* `dev/reflections/next-session.md`

**C1.**
* `python bootstrap/scaffold.py --manifest` differs from `HEAD` by exactly the `dev/NEXT_SESSION.md` row. The pin at `test_notice_install.py:184` is `len(install_manifest(modules=None))` at the landing tree minus 1 (95 today; printed lines are the pin plus 1). Mutant: restore the row, and the new node `test_a_fresh_install_writes_no_handoff_file_record_or_row` fails (control: the unedited tree passes).
* The same node pins that `dev/NEXT_SESSION.md` stays in `_LIVING_STATE_DSTS`. Mutant: remove the entry, and `test_upgrade_plan_reports_the_retired_handoff_once_and_apply_leaves_it` fails. That node expects exactly one `removed-upstream 1: dev/NEXT_SESSION.md` line from `upgrade --plan`, `--apply` leaving file, record and cached base copy unchanged, and `verify_integrity` passing.
* `docs/quickstart.md:298` equals the unfilled-slot count of `python bootstrap/scaffold.py --dry-run` on `solo-greenfield` at the landing tree (20 becomes 19 today; the other two profiles, 23 becomes 22, are measured, not quoted).
* Boundary A: `test_agreement_retired`, `test_upgrade` (`TestLivingStatePartition`), `test_quickstart_sequence`, `test_notice_install`, `test_manifest`, `test_core_dev_folders`, `test_lockfile_module`, `test_scaffold`, `test_review_stance_in_shipped_files`. Gates: `check_cairn.py`; `scripts/quality_gate.py --sub neutrality --sub redundancy`. `test_ast_attest` and `test_gate_manifest` are expected red until C7; the record names each failure and its cause.

**C2.**
* The paragraph in `doctrine/session-routines.md` is Revision 3 Proposal 2's text, word for word, and it carries the "do not copy" and link-or-folder-or-tracked sentences (SR1, SR2). Both `session-end` skills carry the "do not copy", link-or-folder-or-tracked and `git check-ignore -q` sentences, with the `.gitignore` remedy only "if that fails and git does not track the path".
* `test_the_note_path_is_ignored_and_both_prunes_spare_it`: `git check-ignore -q dev/reflections/next-session.md` exits 0; both prunes (`tools/session.py` and `templates/modules/default-on/prune_reflections.py`, dry run) list a dated control file and never the note (controls: `dev/reflections/README.md` is not ignored; an old dated file is listed).
* `test_no_shipped_source_tells_a_reader_to_read_or_write_the_retired_file` (pattern of `test_agreement_retired.py:155-175`), listing shipped sources from the tree. Exempt, by name in the test: `bootstrap/UPGRADE.md`, both `verify_stems.py` twins, `bootstrap/_scaffold/lockfile.py` and `config.py` (they name the path on purpose). Control: a planted instruction to read the file in a shipped prose file fails.
* `grep -n 'NEXT_SESSION' tools/session.py templates/skills/_lib/session.py` finds none; `cmp` of the two copies is identical; `git diff` shows no change inside `_resolve_interpreter` or any call, argument or warning; the phrase pinned at `test_session_failsafe.py:104` survives.
* The `doctrine/session-routines.md:113-115` edit says the commit makes the roadmap scrub durable, the note is local, and a goodnight whose scrub changes nothing makes no commit, so `session-start` falls back with a warning.
* Boundary A: `test_session_failsafe`, `test_prune_tools`, `test_session_routines`, `test_session_kernel`, `test_skill_contract`, `test_core_dev_folders`, `test_review_stance_in_shipped_files`, plus a search for tests that read each touched doctrine file. Gates: `check_cairn.py`, `link_check.py`, neutrality (no vendor name in doctrine or templates).
* Each edited file with a lockfile record is finalized by path, after the first criterion's (b) read of any earlier unrecorded edit and then its whole diff: `python bootstrap/scaffold.py upgrade --target . --finalize <path>`, never bare (a bare one refuses in this tree).

**C3.**
* Both `AGENTS.md` copies and both `session-start` skills carry the read clause as Revision 3 gives it. `test_every_read_copy_says_the_note_is_data_not_instructions` lists the four copies from the tree. Mutant: delete the phrase from one copy at a time, in separate copies; each of the four fails it (control: unmutated passes).
* `test_every_copy_of_the_note_rules_refuses_a_link_a_folder_or_a_tracked_path` pins the sentence in the doctrine and the four skills, listed from the tree; same one-at-a-time mutants.
* The cold-start probe, run once by a fresh agent on a scratch install, given only the installed `AGENTS.md`: it names `dev/reflections/next-session.md`, opens it, and treats the content as data. The record states the result. A failure is reported, not fixed here (the print of the note's age becomes a later proposal).
* Boundary A: `test_skill_contract`, `test_session_start_drain_rules`, `test_skills_install`, `test_review_stance_in_shipped_files`, plus a search for tests that read either `AGENTS.md`. Finalize the changed copies by path, as C2 does.

**C4.**
* In both twins, only `dev/NEXT_SESSION.md` is skipped (Proposal 4), and only when no `--scan` was given and nothing exists at the path (not even a link or folder). An absent `dev/PLANNING.md` still reports "file not found". `main` passes the default tuple itself (`verify_stems.py:187`), so the skip is keyed on the command line having no `--scan`. The skip prints `verify_stems: skipped <path> (absent)`; the OK line names only files read.
* Nodes run the script (a subprocess) or `main`, in both twins, never `check_stems` alone. Nodes: `test_verify_stems_skips_an_absent_default_file_and_says_so` (OK line names only `dev/PLANNING.md`); `test_verify_stems_flags_a_stem_in_a_present_handoff_file`; `test_verify_stems_refuses_an_explicit_scan_of_a_missing_file` (the missing file itself); `test_verify_stems_refuses_a_folder_or_dangling_link_at_the_default_path`; `test_verify_stems_still_refuses_an_absent_planning_file` (absent `dev/PLANNING.md` exits non-zero; control: absent handoff file skipped). Mutant: key the skip on default-list membership; the last three fail (control: the specified skip passes). Run each against both twins, and `cmp` them.
* Boundary A: `test_verify_stems` and the new nodes, `scripts/verify_stems.py` run on this tree. Finalize `scripts/verify_stems.py` by path.

**C5.**
* `bootstrap/UPGRADE.md` gains a section beside the agreement section. Today's truth only: `upgrade --plan` prints one `removed-upstream 1: dev/NEXT_SESSION.md` line and repeats it; the project keeps its file; keep it, shrink it to a line, or empty it; do not delete it or untrack it (a bare `--finalize` then refuses; `verify_integrity.py` still passes, its slot note counting one unreadable); if deleted, restore an empty file. One sentence for the later change: when the `upgrade` change that removes untouched retired files ships, an untouched copy is removed and its record cleared, and a changed copy is named and left; nothing before then, no release or date named. The twelfth row's own plan edits this section when it lands.
* `test_the_upgrade_guide_names_the_path_the_plan_line_prints` pins that the new section and the printed line name the same path, and that the new section names no release, version or date.
* The agreement section's "report it unreadable" (`UPGRADE.md:56-59`) is corrected to the same measured behaviour. Commit body: `Defect fix: UPGRADE.md:56-59 -> bootstrap/UPGRADE.md -- test bootstrap/tests/test_next_session_local_note.py::test_a_deleted_handoff_leaves_integrity_passing_and_an_emptied_one_lists_no_slot -- changes no rule text`. That node covers both paths: deleted file, `verify_integrity` exit 0 with "unreadable 1"; emptied file, no slot listed.
* Boundary A: that node, `test_upgrade_lockfile_path_containment`, `test_verify_integrity`; a search for tests that read `bootstrap/UPGRADE.md` (it finds `test_review_stance_in_shipped_files.py:1318` among others). Gates: `check_cairn.py`.

**C6.**
* Before any deletion, append `## Migration record -- <agent> -- <date>`: the whole file read, citing the blob read (`git rev-parse HEAD:dev/NEXT_SESSION.md`; the file is rewritten at each goodnight); one row per section of `dev/NEXT_SESSION.md` (preface and five headed sections) with its durable content and its home (a board row, a plan, an issue, doctrine, or "stale, dropped"). The three lessons in "Notes for whoever coordinates next" have no home: their home is one `dev/PLANNING.md` row, written at the archive commit (the planning session's serialization point, not doctrine, which takes the rate-limit gate). Placement follows `docs/DOCUMENTATION_PLAN.md`; the record, not memory, is checked.
* Then, last: recheck `git rev-parse HEAD:dev/NEXT_SESSION.md` equals the cited blob (if not, read the diff and update the record first), then `git rm dev/NEXT_SESSION.md && git commit dev/NEXT_SESSION.md`. Afterwards `git ls-files dev/NEXT_SESSION.md` prints nothing, the lockfile record at `dev/.cairn/cairn-lock.yml:52-55` is unchanged, and the `python bootstrap/verify_integrity.py --target .` list of mismatched paths (23 on 2026-10-26) is the same before and after, so no failure is caused by this path.
* The nine lockfile finalizes (C2-C4: `tools/session.py`, `scripts/verify_stems.py`, both `.agents/skills/` skills, `dev/reflections/README.md`, `dev/README.md`, `dev/agent_collaboration.md`, `docs/DOCUMENTATION_PLAN.md`, `AGENTS.md`) were each by path; over the whole range, `git diff` of the lockfile names no other path. `dev-tour.md` has no record.
* `python scripts/claim_check.py` and `check_cairn.py` over the touched Cairn-only prose (`bootstrap/BOOTSTRAP.md`, `bootstrap/fidelity-check.md`).
* The archive commit (the plan's owner) writes the `CHANGELOG.md` entry (`doctrine/plans.md:1036`), saying what is true at landing as in C5, turns the historical link at `CHANGELOG.md:2922` into plain code text, and retires the board row at `dev/PLANNING.md:511`. `case-studies/modflow_tools-fidelity-manifest.yml` stays.

**Security Review findings, where each lands.**

| Finding | Chunk | Test or check |
|---|---|---|
| SR1 note carries no authority | C2, C3 | `test_every_read_copy_says_the_note_is_data_not_instructions`; "do not copy" in the doctrine and both `session-end` skills |
| SR2 no link, folder or tracked path | C2, C3 | `test_every_copy_of_the_note_rules_refuses_a_link_a_folder_or_a_tracked_path`; the `.gitignore` remedy only for an untracked path |
| SR3 the skip cannot pass silently | C4 | `test_verify_stems_refuses_an_explicit_scan_of_a_missing_file`, `test_verify_stems_refuses_a_folder_or_dangling_link_at_the_default_path` |
| SR4 oracle roster | C7 | the Maintainer's authorization names `bootstrap/_scaffold/config.py` |
| SR5 promise nothing for the twelfth row | C5, archive | superseded by the Decision's answer 4; the wording is the C5 criterion |

## Scope delta

**Scope delta**: preserved. No outcome of Revision 3 is removed. The one change from the proposal's default is the Decision's answer 4, which adds the sentence about the later cleanup to C5 and the changelog and moves the cleanup itself to the twelfth row.

## Verification

**Boundary A** is the mapping under each chunk, found by searching for what imports or reads each touched file, plus the standing gates named there.

**Boundary B mode: `full`.** The change edits the install contract (the manifest and the fidelity spec), an engine file and a trust-ceremony surface (`config.py`), so bounded mode refuses. The record is scoped: `**Certified by**: pending` until the next certifying run on a clean committed tree under Python 3.13.x. **Nobody sets `CAIRN_FULL_SUITE=1`.** After the last implementation commit the implementer appends `## Implementation verification -- <agent> -- <date>` with the fields the template names, `test_ast_attest` and `test_gate_manifest` red until C7, and a smoke of `scaffold.py --manifest` and `--dry-run` on `solo-greenfield`. The implementer never runs the re-anchor.

**What the code reviewer should attack** (one code-review loop). Each mutant in its own copy, beside a control: restore the table row; remove the living-state entry; key the skip on list membership; delete "data, not instructions" from each of the four read copies; remove the link-or-folder-or-tracked sentence from each of the five rule copies (list the sets from the tree). Also: the manifest differs by exactly one row; the twins are byte-identical; `_resolve_interpreter` is untouched; the `UPGRADE.md` and changelog wording promises nothing before the twelfth change ships; the C6 table covers all six parts of the file; the lockfile diff shows only the nine paths; the finalizes were by path.

## Plan review -- Plan reviewer (fresh session, Internal) -- 2026-10-26

**Tier**: Internal
**Model**: Sonnet 5.5, fresh session
**Reviewed commit**: c1b4ec6a
**Obligation**: ordinary plan review only. The Internal Security Review owed by the header is a separate pass; this one does not write or discharge it.

**Foundations**
1. *Does the plan deliver the settled premise?* Yes, with two gaps. All seven proposals and the tests map to chunks (C1 to C6), and the answer-4 wording is right at landing: the C5 sentence and the changelog line promise nothing earlier (plan lines 14, 90, 100, 110; Decision at the proposal's lines 1068-1088). Gaps: B1 and B2 below.
2. *Simpler path to the same outcomes?* None that keeps every outcome. Each chunk owns a distinct surface, the order is forced (C4 before C6; C1 before C5), and the new test file is one file. I recommend no cut (plan lines 43-51).
3. *What result would show it cannot deliver?* A fresh install that still writes the file; an upgraded tree that fails `verify_integrity` or prints other than one `removed-upstream` line; a skip that lets a missing board file pass (B1); a finalize that seals someone else's edit (B2); a failed cold-start probe (C3). Backed by C1 nodes 1-2, C4 nodes, C3 probe.

**Findings**
* **B1 -- blocking. The C4 skip is wider than Proposal 4.** The proposal skips only `dev/NEXT_SESSION.md`; C4 says "a default file". As worded, an absent `dev/PLANNING.md` also passes. `verify_stems.py:117` reports "file not found" for it today, and no node pins that. Also `main` passes the default tuple itself (`verify_stems.py:187`), so only the command line can tell that `--scan` was absent. Fix: name the one skippable path; add a node (absent `PLANNING.md` still errors, control: absent handoff skipped); say the nodes run `main` or the script, in both twins.
* **B2 -- blocking. The finalize rule is not checkable as written.** `python bootstrap/verify_integrity.py --target .` today lists `tools/session.py`, both `.agents/skills/` skills, `dev/README.md` and `docs/DOCUMENTATION_PLAN.md` as hash mismatches: 5 of the 9 finalize targets already carry edits that are not recorded (`git status` shows none uncommitted; they are committed and unfinalized). A by-path finalize seals those too, and the tool keeps only a hash, so "read its whole diff" has no base. "The lockfile diff names no other path" cannot see this, and "have landed" (line 41) has no test. Fix: each chunk's first criterion lists the chunk's paths that mismatch before the first edit, and names the commits since each path's last finalize. The implementer finalizes only after that list is empty or read. The lockfile joins the intent claim and is committed by path with the file it records.
* **N1 -- non-blocking. The C7 fence names one file.** The roster entry is the directory `bootstrap/_scaffold/` (`_oracle_activation.py:36`), and C1 also edits `lockfile.py`, which already has a post-anchor commit (`9af86ae4`). Fix: the authorization names every `bootstrap/_scaffold/` file changed since `refs/cairn/gate-anchor`, listed at the cut with `git diff --name-only`. Fails closed if missed, so not blocking.
* **N2 -- non-blocking. C2 omits two Proposal 2 items.** The `session-routines.md:113-115` criterion drops "a goodnight whose scrub changes nothing makes no commit, so `session-start` falls back with a warning". And `templates/core/AGENTS.md` has no landmark list or file name (`git grep` finds none); only the root `AGENTS.md:471` does. Fix: add the clause; say "both" applies to the Goodnight bullet only.
* **N3 -- non-blocking. The "no source tells a reader" test needs its exemptions named.** Both `verify_stems.py` twins still name the path after C4, and `UPGRADE.md`, `lockfile.py` and `config.py` name it on purpose. Fix: list the exempt files in the C2 criterion with a control (a planted instruction in a shipped prose file fails).
* **N4 -- non-blocking. C6 is thin in three places.** (a) The file is rewritten at each goodnight (last commit `9f61e8c8`); the record should cite the blob read and recheck it is unchanged at `git rm`. (b) The three lessons need a named home: a `dev/PLANNING.md` row, not doctrine, since doctrine text takes the rate-limit gate and the Maintainer. (c) The tree is already red under `verify_integrity` (23 mismatches), so "no failure caused by this path" means the mismatch list is the same before and after. The criterion "all nine finalizes were by path" belongs in C2 to C4, where they happen.
* **N5 -- non-blocking. A stale claim blocks C1.** `python tools/intent.py list` shows a 2026-10-19 claim by `claude-e4f56026` on `docs/quickstart.md` and `bootstrap/tests/test_lockfile_provenance.py`. The first-criterion rule makes C1 wait on it. Fix: its owner releases it or confirms it stale before C1.
* **N6 -- non-blocking. C5 can check its own promise.** Add to `test_the_upgrade_guide_names_the_path_the_plan_line_prints` that the new section names no release, version or date.

**Lens evidence**
1. *Claims.* Opened and found real: `config.py:549, 756`; `lockfile.py:62, 85`; `fidelity-check.md:142`; `BOOTSTRAP.md:507, 631`; `quickstart.md:298`; `test_notice_install.py:184`; `test_upgrade.py:1795`; `test_quickstart_sequence.py:197`; `PLANNING.md:511`; `CHANGELOG.md:2922`; `plans.md:1036`; `.gitignore:9-10` (`check-ignore` exits 0 for the note, 1 for the README); the dropped node at `gate_manifest.json:2311`. The cited five headed sections plus preface of `dev/NEXT_SESSION.md` match.
2. *Production path.* B1 above. C1 nodes run install and `upgrade --plan` through their entry points, as `test_agreement_retired.py:72-121` does.
3. *Design completeness.* N3, N4.
4. *Fail-closed.* B1, B2, N1. The living-state entry is kept, which fails closed.
5. *Cross-document.* Re-ran the plan's search plus `git grep -l -i -E 'next[_-]session'`: every tracked hit is listed in a chunk or is history (`CHANGELOG.md`, `dev/strategy/archive`, `case-studies`); `removed-upstream` search finds only `test_agreement_retired.py` (positive control: it exists there). `doctrine/plans.md:1031` and `proposals.md:135, 350, 382` have several spots, and C2 should touch each.
6. *Drift.* Frozen set re-derived: all six keyed files are keys in `frozen_files`; the new test file is not (`FROZEN-NEW`, allowed once tracked, `_gate_manifest.py:669`). The 4+1+1 counts match Proposal 7. C1 edits no frozen file beyond that table.
7. *Lifecycle.* The sequence (this, onboarding, twelfth row) is stated at line 41; C5 hands its section to the twelfth plan; C7 has a Waiting line and no agent step runs a re-anchor.
8. *Scope.* Scope delta "preserved" holds against Revision 3; no outcome removed.
9. *Satisfiers.* Each finding names one.

**For the code reviewer.** Mutate each member of the sets listed at line 122 from the tree, plus: absent `PLANNING.md` with the skip on; finalize of a path that was already mismatched.

**Coverage.** Covered: lenses 1-9 above. Not covered: no test run, no scratch install or `upgrade` run, so every behaviour claim is read, not measured; the Revision 3 prose's other line cites (the `session.py` strings, skill step numbers) were spot-checked, not all opened; the twelfth row's proposal was not read; the Internal Security Review is not done here and stays owed; the cold-start probe has not been run.

## Response -- plan author -- 2026-10-26

Operative cells revised in place (Sequence first criterion, C2 to C6, C7 fence). Facts re-measured on 2026-10-26 (`verify_integrity`: 23 mismatches; the five finalize targets the review named still mismatch; the other four match; `intent.py list`: the 2026-10-19 `docs/quickstart.md` claim is still live).
* **B1 -- accepted.** C4 skips only `dev/NEXT_SESSION.md`; a new node pins that an absent `dev/PLANNING.md` still fails; the nodes run the script or `main` in both twins.
* **B2 -- accepted.** The first criterion now lists pre-mismatched finalize targets, finds the last matching commit by hash (measured for `tools/session.py`: `7832d057`), names the owner or records the earlier edit if none is found, puts the lockfile in each claim, and gives "have landed" a command.
* **N1 -- accepted.** The C7 fence names the whole `bootstrap/_scaffold/` directory and lists changed files since the anchor, `lockfile.py` included.
* **N2 -- accepted.** C2 gains the no-commit-goodnight clause; the landmark list is the root `AGENTS.md` only.
* **N3 -- accepted.** The exempt files are named in the C2 test, with a planted-instruction control.
* **N4 -- accepted.** C6 cites and rechecks the blob, homes the three lessons in a `dev/PLANNING.md` row at the archive commit, compares the mismatch list before and after; the finalize-by-path claim moves to C2-C4.
* **N5 -- accepted.** The stale claim blocks C1; the implementer reports it to the planning session and never overrides or releases it. It is still live today.
* **N6 -- accepted.** C5's test also pins that the new section names no release, version or date.

The review round is over. The plan holds at `awaiting-plan-review` for the Internal Security Review next, which is a separate pass by someone else; it is not `ready-to-implement`.

## Plan review -- Security Review -- 2026-10-26

**Reviewed commit**: 17f3851c
**Target**: the whole plan; the proposal's Revision 3, Decision and Security Review (`c6802ee4`) as context.
**Prior findings**: none of this tier. The ordinary pass (`d1ca9741`) and its Response are context, not clearance.
**Assurance path**: high-assurance
**Obligation**: the Internal Security Review owed by the header line `Plan review: required(Internal + Internal Security Review)` (line 6). This pass is that review. It clears on conditions B1 to B3; a Response that carries them owes no second Security Review unless it changes the design.
**Tier**: Internal Security Review
**Model**: Opus 5.5, fresh session
**Findings**: raised (3 blocking, 5 non-blocking)

**Conclusion.** The engine row, the `verify_stems.py` skip and the `session.py` strings are safe as planned. Three gaps are open: the note rules miss a linked parent folder (B1); a by-path finalize seals whatever bytes are on disk (B2); two sentences the Security Review required have no test that can fail (B3). Each has a short fix. Status moves to `revising-plan`.

**Foundations**
1. *Does the plan close the risk it was raised against?* Partly. SR3 is closed: the C4 nodes kill the list-membership mutant on all three refusals (line 86). SR4 is closed by the C7 fence (line 53). SR1 and SR2 are carried in words but not all tested, and SR2's wording misses one route. -- lines 70, 79-80, 106-107; B1, B3.
2. *Simpler, safer alternative.* No simpler plan. Two safer details: seal only committed bytes, and check the folder as well as the note path. -- `bootstrap/_scaffold/upgrade.py:2033-2130` (the dirty-tree guard runs only for a bare finalize).
3. *What would show it fails.* A clone whose `dev/reflections` is a tracked link: every check the rule names passes, and the note is written outside the clone. -- ledger P1.

**Findings**
* **B1 -- blocking. A linked `dev/reflections` folder defeats SR2.** SR2 refuses a link at the note path, not at its folder. In a scratch clone of a repository that tracks `dev/reflections` as a link out of the tree, the note path is neither a link nor a folder, `git ls-files` prints nothing, and `git check-ignore -q` exits 128 ("beyond a symbolic link"). The rule then says add an ignore line and write, and the write landed outside the clone (P1). This is SR2's own threat, a tracked link in a clone. The paragraph is the Decision's verbatim text, so only the Maintainer can widen it. Recommend: ask him to add "or the `dev/reflections` folder is a link" and "if `git check-ignore` exits other than 0 or 1, stop" to the doctrine paragraph and the four skills, pinned by the C3 rules node; failing that, record his acceptance of the risk.
* **B2 -- blocking. A by-path finalize seals on-disk bytes, not committed ones.** `--finalize <path>` hashes the file as it sits on disk, with no dirty-tree check (`upgrade.py`, the guard is in the `only is None` branch). Criterion (b) reads history, never the working tree. So another session's uncommitted edit to `tools/session.py`, the interpreter-binding trust root's module, is sealed and then committed with the chunk. And "or ... recorded in the commit body as unverified" (line 41) lets the implementer seal bytes nobody checked. Recommend: before each finalize, `git diff <path>` shows only the chunk's edit and `git status --short dev/.cairn/cairn-lock.yml` is empty; after the commit, the record's hash equals the `sha256` of `git show HEAD:<path>` and `git status --short <path> dev/.cairn/cairn-lock.yml` prints nothing; strike the "unverified" escape (not found means that path waits). For `tools/session.py`, the commit body names the review that cleared each of the four unsealed commits since `7832d057` (`a773e753`, `c5daabe4`, `50b5fbdf`, `62508ef0`: +220/-38 lines, some inside `_binding_untrusted` and `_resolve_interpreter`).
* **B3 -- blocking. Two required sentences have no test that can fail.** SR1's "Do not copy text from an issue, a web page or a comment into the note" and SR2's `.gitignore` remedy "only if git does not track the path" are named at line 70 and in the table (lines 106-107) with no test or command, against the plan's rule at line 57. The onboarding change edits `session-start` step 3 and `doctrine/session-routines.md` next, so an untested sentence can be lost mid-sequence. Recommend: the C3 rules node also pins both phrases in the doctrine and both `session-end` skills, with the same one-at-a-time mutants.
* **N1 -- non-blocking. Nothing pins "no tool reads the note".** The Security Review asked to refuse such a tool in this change (proposal, Answers item 7); C2 greps `session.py` only for `NEXT_SESSION`. Today no Python file names the note: `git grep -n -i -E 'next-session\.md|next_session' 17f3851c -- '*.py'` finds only the old path, so the pattern can match. Recommend: a node that no shipped `.py` file names `next-session.md`.
* **N2 -- non-blocking. Make the `session.py` check mechanical.** The three strings are fixed text with no inserted values: a docstring line (`:1960`) and two `_emit` texts (`:1971`, `:2052`), all after `cmd_session_end` begins at `:1948`. `encode_display` begins at `:189` and `_resolve_interpreter` at `:931`; the two copies are identical at 17f3851c (`cmp`). Recommend: `git diff -U0` of each copy shows exactly three one-line hunks, all after line 1948, in place of "shows no change inside".
* **N3 -- non-blocking. "Expected red" hides new failures.** `test_gate_manifest` should stay green: it checks a freshly produced manifest (`bootstrap/tests/test_gate_manifest.py:78-100`; `AGENTS.md`, "Operational pitfalls"), so lines 67 and 120 mislabel it. While `test_ast_attest` is red, a further engine change (the twelfth row edits `upgrade.py`) adds no new red. Recommend: the record lists the measured AST changed set (the prior set plus `Assign:_CORE_MAPPINGS`, nothing else) and the entries this change adds to `_gate_manifest.py verify --no-collect`; any other entry is a failure.
* **N4 -- non-blocking. Widen the never-edit list and the fence.** The self-service AST update refuses while other symbols differ (`bootstrap/tests/_ast_attest.py`, `update_symbol`), so that route is shut. Hand edits are not: line 18 names the AST baseline and `scaffold_ast_known_new.json`, not `bootstrap/tests/fixtures/gate_manifest.json` or `refs/cairn/gate-anchor`. One authorization naming `config.py` also covers onboarding's edits to it. Recommend: name both in the never-edit sentence; the fence lists commits per file with `git log --oneline refs/cairn/gate-anchor..HEAD -- bootstrap/_scaffold/`.
* **N5 -- non-blocking. The old file can come back unnoticed.** `git rm` refuses a file with unstaged edits (P2), so C6 fails closed against a goodnight rewrite in progress. But a session started before C2 can write and commit `dev/NEXT_SESSION.md` after C6, and nothing flags it (living state, so `verify_integrity` skips it). Recommend: the archive commit checks that `git ls-files dev/NEXT_SESSION.md` prints nothing.

**Falsification ledger** (scratch repositories under the scratchpad, removed afterward)
* P1: a tracked link `dev/reflections` pointing outside, then a clone. The rule's checks pass, `check-ignore` exits 128, a plain write lands outside. Plan fails (B1).
* P2: `git rm` of a tracked file with an unstaged edit: exit 1, file kept. Plan holds.
* P3: each finalize target's record hash matched to a commit (`git log`, `sha256` of each blob). Five mismatch, all found: `tools/session.py` 4 commits since, `session-start` skill 11, `session-end` skill 2, `dev/README.md` 2, `docs/DOCUMENTATION_PLAN.md` 6. Four match HEAD. The "not found" branch is unreached today.
* Read, not run: `scripts/verify_stems.py:98-206` (`main` is the only caller of `check_stems`; `args.scan` is `None` without `--scan`); `bootstrap/tests/_oracle_activation.py:34-47` (the entry is the whole directory); `config.py:756` and `lockfile.py:62` are comments, so `Assign:_CORE_MAPPINGS` stays the one new AST change.

**Lens evidence.** 1 Claims: cites above opened at 17f3851c. 2 Production path: C4 nodes run the script or `main` (line 86); the note rules have no entry point but an agent, so the cold-start probe and a reader are their test. 3 Design: B1, B2. 4 Fail-closed: B2's escape, N3, P2. 5 Cross-document: onboarding shares the edited sentences (B3). 6 Drift: N3. 7 Lifecycle: C7 is MAINTAINER-ONLY with a Waiting line (line 53). 8 Scope: B1 needs the Maintainer's word; nothing else adds an outcome. 9 Satisfiers: each finding names one.

**Coverage.** Covered: the seven questions in the brief, by reading and three probes. Not covered: no test file or suite run; no agent watched reading or writing a note, so whether the wording changes behaviour is reasoning; Windows, case-insensitive disks and hard links not probed; a finalize of a target that is itself a link not probed; the onboarding and twelfth proposals not read beyond this plan's account; the four earlier `session.py` commits listed, not reviewed.
