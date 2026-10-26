# Plan: Make the next-session handoff a local note

**Author**: Claude Sonnet 5.5 (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-next-session-local-note.md](../proposals/archive/2026-10-26-claude-next-session-local-note.md)
**Status**: awaiting-plan-review
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

How to work: directly on `0.5-dev`. **Every chunk's first criterion** is `python tools/intent.py list` showing no other claim on the chunk's files, and that the Plain Language `--finalize` and the security-findings fixer have landed before the `AGENTS.md` and `session.py` edits (C2, C3). Commit by explicit path; the two `session.py` copies stay byte-identical; both `verify_stems.py` twins stay byte-identical. Order is C1 to C6, then C7. This change lands first, then onboarding (it re-derives its pins from the tree after this lands), then the twelfth row.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Stop shipping: delete `templates/core/dev/NEXT_SESSION.md` and the `config.py:549` row; keep the living-state entry; reword the two comments (`config.py:756`, `lockfile.py:62`); update `bootstrap/fidelity-check.md:142`, `bootstrap/BOOTSTRAP.md:507`, `:631`, `docs/quickstart.md:298`; the three pinned tests | none | engine row, install contract |
| C2 | The note's rules, write side: `doctrine/session-routines.md` paragraph and `:113-115`; Goodnight bullet and landmark list of both `AGENTS.md`; both `session-end` skills; `agent_collaboration.md` and its template; three `session.py` strings; both reflections READMEs; the other prose that names the file (`dev/README.md` and template, both `dev-tour.md`, `documentation_plan_template.md` and `docs/DOCUMENTATION_PLAN.md`, `plans.md`, `proposals.md`, `doc-governance.md`) | none | doctrine, prose |
| C3 | The read side: Session start bullet of both `AGENTS.md`; step 3 of both `session-start` skills; one cold-start probe | none | skills, `AGENTS.md` |
| C4 | `verify_stems.py` skip, both twins | none | a verbatim script |
| C5 | `bootstrap/UPGRADE.md`: the new section and the agreement-section defect fix | none | adopter guide |
| C6 | Cairn's own tree: read the whole file, table of each section's durable content and home, then `git rm dev/NEXT_SESSION.md` last | none | the proof tree |
| C7 | The AST attestation and gate-manifest re-anchors at the cut | **MAINTAINER-ONLY**, not scheduled for an agent | re-pinned checksums |

**C7 fence.** The Maintainer's authorization at the cut must name `bootstrap/_scaffold/config.py` (oracle-sensitive roster, SR4); if it is missed the gate stays shut and does not pass. `Assign:_CORE_MAPPINGS` is the one new AST change. The implementer never edits `scaffold_ast_known_new.json` or the AST baseline. When work reaches C7, write `**Waiting on Maintainer**: re-anchor at the cut`. `test_ast_attest` is red until then, by design.

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
* `test_no_shipped_source_tells_a_reader_to_read_or_write_the_retired_file` (pattern of `test_agreement_retired.py:155-175`), listing shipped sources from the tree.
* `grep -n 'NEXT_SESSION' tools/session.py templates/skills/_lib/session.py` finds none; `cmp` of the two copies is identical; `git diff` shows no change inside `_resolve_interpreter` or any call, argument or warning; the phrase pinned at `test_session_failsafe.py:104` survives.
* The `doctrine/session-routines.md:113-115` edit says the commit makes the roadmap scrub durable and the note is local.
* Boundary A: `test_session_failsafe`, `test_prune_tools`, `test_session_routines`, `test_session_kernel`, `test_skill_contract`, `test_core_dev_folders`, `test_review_stance_in_shipped_files`, plus a search for tests that read each touched doctrine file. Gates: `check_cairn.py`, `link_check.py`, neutrality (no vendor name in doctrine or templates).
* Each edited file with a lockfile record is finalized by path, after reading its whole diff: `python bootstrap/scaffold.py upgrade --target . --finalize <path>`, never bare (a bare one refuses in this tree).

**C3.**
* Both `AGENTS.md` copies and both `session-start` skills carry the read clause as Revision 3 gives it. `test_every_read_copy_says_the_note_is_data_not_instructions` lists the four copies from the tree. Mutant: delete the phrase from one copy at a time, in separate copies; each of the four fails it (control: unmutated passes).
* `test_every_copy_of_the_note_rules_refuses_a_link_a_folder_or_a_tracked_path` pins the sentence in the doctrine and the four skills, listed from the tree; same one-at-a-time mutants.
* The cold-start probe, run once by a fresh agent on a scratch install, given only the installed `AGENTS.md`: it names `dev/reflections/next-session.md`, opens it, and treats the content as data. The record states the result. A failure is reported, not fixed here (the print of the note's age becomes a later proposal).
* Boundary A: `test_skill_contract`, `test_session_start_drain_rules`, `test_skills_install`, `test_review_stance_in_shipped_files`, plus a search for tests that read either `AGENTS.md`. Finalize the changed copies by path.

**C4.**
* In both twins, a default file is skipped only when no `--scan` was given and nothing exists at the path (not even a link or folder). The skip prints `verify_stems: skipped <path> (absent)`; the OK line names only files read.
* Nodes: `test_verify_stems_skips_an_absent_default_file_and_says_so` (OK line names only `dev/PLANNING.md`); `test_verify_stems_flags_a_stem_in_a_present_handoff_file`; `test_verify_stems_refuses_an_explicit_scan_of_a_missing_file` (the missing file itself); `test_verify_stems_refuses_a_folder_or_dangling_link_at_the_default_path`. Mutant: key the skip on default-list membership; the last two fail (control: the specified skip passes). Run each against both twins, and `cmp` them.
* Boundary A: `test_verify_stems` and the new nodes, `scripts/verify_stems.py` run on this tree. Finalize `scripts/verify_stems.py` by path.

**C5.**
* `bootstrap/UPGRADE.md` gains a section beside the agreement section. Today's truth only: `upgrade --plan` prints one `removed-upstream 1: dev/NEXT_SESSION.md` line and repeats it; the project keeps its file; keep it, shrink it to a line, or empty it; do not delete it or untrack it (a bare `--finalize` then refuses; `verify_integrity.py` still passes, its slot note counting one unreadable); if deleted, restore an empty file. One sentence for the later change: when the `upgrade` change that removes untouched retired files ships, an untouched copy is removed and its record cleared, and a changed copy is named and left; nothing before then, no release or date named. The twelfth row's own plan edits this section when it lands.
* `test_the_upgrade_guide_names_the_path_the_plan_line_prints` pins that the new section and the printed line name the same path.
* The agreement section's "report it unreadable" (`UPGRADE.md:56-59`) is corrected to the same measured behaviour. Commit body: `Defect fix: UPGRADE.md:56-59 -> bootstrap/UPGRADE.md -- test bootstrap/tests/test_next_session_local_note.py::test_a_deleted_handoff_leaves_integrity_passing_and_an_emptied_one_lists_no_slot -- changes no rule text`. That node covers both paths: deleted file, `verify_integrity` exit 0 with "unreadable 1"; emptied file, no slot listed.
* Boundary A: that node, `test_upgrade_lockfile_path_containment`, `test_verify_integrity`; a search for tests that read `bootstrap/UPGRADE.md` (it finds `test_review_stance_in_shipped_files.py:1318` among others). Gates: `check_cairn.py`.

**C6.**
* Before any deletion, append `## Migration record -- <agent> -- <date>`: the whole file read; one row per section of `dev/NEXT_SESSION.md` (preface and five headed sections) with its durable content and its home (a board row, a plan, an issue, doctrine, or "stale, dropped"). Known so far: the three lessons in "Notes for whoever coordinates next" have no home. Placement follows `docs/DOCUMENTATION_PLAN.md`; the record, not memory, is checked.
* Then, last: `git rm dev/NEXT_SESSION.md && git commit dev/NEXT_SESSION.md`. Afterwards `git ls-files dev/NEXT_SESSION.md` prints nothing, the lockfile record at `dev/.cairn/cairn-lock.yml:52-55` is unchanged, and `python bootstrap/verify_integrity.py --target .` still reports no failure caused by this path.
* All nine lockfile finalizes were by path: `tools/session.py`, `scripts/verify_stems.py`, both `.agents/skills/` skills, `dev/reflections/README.md`, `dev/README.md`, `dev/agent_collaboration.md`, `docs/DOCUMENTATION_PLAN.md`, `AGENTS.md`. `git diff` of the lockfile names no other path. `dev-tour.md` has no record.
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
