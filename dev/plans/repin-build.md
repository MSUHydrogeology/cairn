# Plan: Build `repin`, one script for the re-anchor ceremony

**Author**: Claude (Strategy)
**Source proposal**: [dev/proposals/archive/2026-10-26-claude-repin-build.md](../proposals/archive/2026-10-26-claude-repin-build.md)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-26
**In brief**: Build one tested script that runs the Maintainer's checksum re-pins and the signed re-anchor, so he compares two digests, answers two summaries and types one passphrase instead of pasting commands an agent wrote.

The Internal Security Review is a separate pass from the ordinary plan review. It checks that the proposal's Security Review findings (SR-1 to SR-7 and SR2-1 to SR2-6) are carried into this plan, by the table under Acceptance criteria. The ordinary pass does not clear it.

## Source proposal

Accepted 2026-10-26 as revised. **Revision 3 is the contract** (it supersedes Revisions 1 and 2 for reading). One script, `scripts/repin.py`, with three verbs: `status` (reads, writes nothing), `package` (computes the AST pin's transaction and prints its digest) and `ceremony` (the whole sequence, 11 steps). The Decision's answers bind: **one key** signs releases and the anchor (recorded departure); the same-user limit for signing is accepted as stated; and **the script does not commit the AST pin**. After the Maintainer's yes it writes the pin, checks what it wrote, prints the `git commit <paths>` line and stops. This differs from Revision 3's default, so no chunk contains a commit step for the AST pin.

## Scope

**In.** R1 to R6 as Revision 3 cuts them. **Out.** Pushing (the script never pushes), the launcher template joining the authority files, any second signing key, a risk trigger, and the two inherited gaps the Security Review put on the board (unsigned anchor commit; inherited `PYTEST_*` variables).

**Reuse.** Searched `scripts/` and `bootstrap/tests/` for what the driver and the checkers already do (`rg 'def (compare|check_packet_pair|values_field)' scripts bootstrap/tests`). Imported after the reading order's step 4: the driver's `compare`, `check_packet_pair`, `values_field`. Not imported: its `key_fingerprint` and `key_in_agent` (they use `PATH`; `repin` has absolute-path versions) and `bootstrap/_scaffold/_guard.py` (the AST baseline attests it). `bootstrap/reanchor.sh` and the launcher are called unchanged. Test beds reuse the builders in `bootstrap/tests/test_reanchor.py` (`bed`, `ceremony`, `_compose_packet`, `_instantiate`, `_launch`), read, not edited.

**Doctrine surface.** None: no rule text changes. `bootstrap/AST_BASELINE_RUNBOOK.md` (descriptive) is cut to one page in R6. `bootstrap/REANCHOR_RUNBOOK.md` is a closure member and is not touched.

**Frozen files, derived from `bootstrap/tests/_gate_manifest.py` `_frozen_files` (globs `bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`, `templates/modules/**/*.py`) and the committed `frozen_files` keys:**

| File | Frozen? | Effect |
|---|---|---|
| `scripts/repin.py` (new) | glob matches; no anchored entry | `FROZEN-NEW`, allowed (`_gate_manifest.py:669`). Entry pinned by the first key ceremony. |
| `bootstrap/tests/test_repin.py`, `test_repin_ceremony.py` (new) | glob matches (`bootstrap/tests/**/*.py`) | `FROZEN-NEW`, allowed. No existing test file is edited by R1 to R5. |
| `scripts/reanchor_ceremony.py` | yes (keyed) | R6 edit owes the ceremony. |
| `scripts/correct_pinned_digests.py`, `bootstrap/tests/test_correct_pinned_digests.py` | yes (keyed) | R6 deletes both and drops their pinned nodes: `FROZEN-MISSING`, `COLLECTION-DROPPED`. |
| `bootstrap/tests/fixtures/scaffold_ast_known_new.json` | yes (keyed) | Written only if an AST pin changes it; then a ceremony is owed. |
| `bootstrap/tests/fixtures/scaffold_ast_baseline.json` | no (cascade-mutable) | The AST write's target. |
| `bootstrap/AST_BASELINE_RUNBOOK.md`, `dev/plans/repin-build.md` | no | Prose; no test or manifest pins their bytes (searched `bootstrap/tests/*.py` and the manifest). |
| `bootstrap/security_check.py` (the Bandit `ALLOWLIST`, empty) | yes | **Not edited.** `scripts/repin.py` is Bandit-scanned (`scan_targets`, `scripts/*.py`), so it must scan clean without an allowlist entry. |

`scripts/repin.py` is in no install mapping (R1 confirms with `python bootstrap/scaffold.py --manifest`).

**Tests run in a scratch world.** Every test builds a scratch repository with its own anchor, a **throwaway key** made in a scratch folder, a scratch agent, and `HOME` pointed at a scratch folder. Nothing reads `~/.ssh`, the real anchor `refs/cairn/gate-anchor`, or the Maintainer's key. Signing tests need `ssh-keygen` and `ssh-agent`; if absent they skip with a named reason, and the record says so.

## Sequence

How to work: directly on `0.5-dev` in the shared checkout, no branch or worktree for writing. `python tools/intent.py claim --files <paths> --action "<what>"` before editing; commit by explicit path. **An agent chunk never signs, never pushes, never runs a re-anchor, never types a passphrase.**

| # | Chunk | Gate | Budget (lines, excluding tests) |
|---|---|---|---|
| R1 | Shared core and AST `status`: the reading order, provenance as a test fixture, refusals, controls, safe-write and display helpers. Read only. | none | R1+R3 about 300 |
| R2 | The AST transaction: `package`, Summary 1's render, the write (the **apply step**, `ceremony` step 5), the working-tree check, the stop line. Scratch repository. | none; budget check | about 300 |
| R3 | Manifest `status` and `--dropped-from`. Read only. | none | (with R1) |
| R4 | `ceremony`: digest check, roster and anchor check, key checks, stages 1 and 2, Summary 2, verification, record, end. Throwaway key. | none until first real run; budget check | about 300 |
| R5 | Lockfile adapter, **only if a correction is owed** when R4 lands. | none | none stated |
| R6 | Retire the old runner, remove `drive()` and `--run`, cut the AST runbook. | **MAINTAINER-ONLY** (see below) | none |

**Maintainer-only steps (the fences).** Each writes a `**Waiting on Maintainer**` line when work reaches it.
* **M1. MAINTAINER-ONLY: the first real apply step** (the AST write against the real tree). It waits for M2.
* **M2. MAINTAINER-ONLY: the key ceremony that pins `repin`.** The AST pin by hand once more under `bootstrap/AST_BASELINE_RUNBOOK.md`, then `python scripts/repin.py ceremony --values <file> --ceremony-dir <dir> --first-run --reviewed-commit <id>`, where `<id>` is the commit the R4 code review names. Anything that signs or asks for a passphrase is his. A fresh agent runs the same `git diff <id> HEAD -- scripts/repin.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py` in a clean checkout and reports the output (the check that can fail if `repin` was edited).
* **M3. MAINTAINER-ONLY: every re-anchor**, including the ones R6 owes.
* **R6b. MAINTAINER-ONLY: the frozen-file edit and its ceremony** (below).

If a size budget fires (checked at the end of R1, R2 and R4), stop at `status`, keep later code on an unmerged branch and do the steps by hand as today. That branch is the one exception to "no branches", and is the Maintainer's call.

## Acceptance criteria

Each criterion names its test or command. Each refusal test has a control that passes when the condition is fine. Tests are named for the property (`test_a_loaded_key_refuses_before_stage_one`), never for a finding or chunk. A comment or docstring explains the code, not the review that asked for it. Test paths: `bootstrap/tests/test_repin.py` (R1 to R3, R5) and `bootstrap/tests/test_repin_ceremony.py` (R4). Proposed paths are declared at the end of this section.

**R1: core and AST `status`.**
* The fixed six-step reading order runs before anything is shown: `HEAD` and the anchor resolved once; the anchored manifest read as data; `HEAD` extracted by `git archive`; each of `bootstrap/tests/__init__.py`, `_ast_attest.py`, `_gate_manifest.py`, `_gate_preflight.py`, `scripts/reanchor_ceremony.py` and `scripts/repin.py` byte-compared with its anchored `frozen_files` entry **before any import** (`test_each_imported_file_is_byte_compared_with_the_anchor_before_import`: one mutated file per list member refuses; control: anchored bytes pass); the AST work in a child run under `python -I -X pycache_prefix=<fresh folder>` (`test_the_ast_child_runs_isolated_with_a_fresh_pycache_prefix`, reading the child's `sys.flags` and `sys.pycache_prefix`); after import, a loaded local module outside the list refuses.
* A tracked `.pyc` under an import root refuses. A candidate commit changing `_ast_attest.py` refuses with no write. A closure-member blob change refuses an AST pin (control: an unrelated change passes).
* An untracked engine module in the working tree is absent from the output; once committed it appears. `HEAD` moving refuses.
* Provenance lines read "the message names `<stem>` (status `<Status>`)" or "the message names no plan or proposal", and no refusal depends on them. A commit subject with ESC and CR prints escaped through `encode_display` (control: an ordinary subject is unchanged). Git output is read as bytes.
* Zero-member sets refuse. `status` writes nothing: a before-and-after tree comparison in the test.
* Standing: Bandit scan (`bootstrap/tests/test_security_lint.py`) clean with the `ALLOWLIST` unchanged; `python bootstrap/tests/_gate_manifest.py verify` lists only `FROZEN-NEW` for the new files.

**R2: the AST transaction and the apply step.**
* **No `repin` path writes `gate_manifest.json`.** The output set is hard-coded (the AST baseline, `scaffold_ast_known_new.json`, the lockfile if R5 is built). A transaction naming `gate_manifest.json` or any other path refuses, and the manifest's blob id is unchanged (control: the baseline alone passes).
* The transaction is one JSON file bound by its SHA-256: head and anchor ids, each output's preimage blob id and SHA-256, the influences outside the tracked tree (interpreter, git, blob id of `encode_display`), the full new bytes and the rendered summary. Two trees that differ only in a kept record give different digests; an edited output byte refuses.
* The apply step reads the transaction once into memory and **renders Summary 1 itself from the bytes it will write**: a key-by-key comparison of the file on disk with the output, never stored text and never `_classify` (`test_every_key_the_write_changes_is_on_screen_before_the_question`; control: drop one row from the render and the test fails). Only the exact word `yes` from a terminal writes; `Yes`, `y`, an empty line, end of input and a pipe are no.
* Safe writes: `mkstemp` in the target's folder; refuse a symlinked target or parent, an untracked or non-regular target, a transaction file that is a symlink, not the user's own or writable by others; `O_NOFOLLOW`; compare-and-swap immediately before `os.replace`; with two outputs, both temporaries written and checked before either is replaced; after a partial failure print what was replaced and the exact `git restore --source=<head-id> -- <path>` line, exit non-zero, restore nothing (tests: changed preimage; symlinked target; symlinked parent; outside path; a planted `<name>.tmp` link). `repin` writes its own containment rule and says in a comment why it does not import `_guard.py`.
* **No commit.** After the write the script checks, with sterile git and hooks off, that only the named paths differ from `HEAD` and that each blob equals `git hash-object --no-filters` of the bytes shown; on a mismatch it refuses and prints the undo line without running it. It then prints the `git commit <paths>` line, the digests to put in the commit body, and "commit these paths, then run ceremony again", and **stops** (`test_the_apply_step_makes_no_commit_and_stops`: `HEAD` unchanged; control: the check passes on a clean write). An AST pin with `MISSING` or `DUPLICATE` symbols, or a pin that adds or drops a baseline key, refuses (it is a review item). When the known-new file is an output, the screen says it changes a frozen gate file and owes a re-anchor.
* `package` at a commit and again in a detached checkout gives one digest.
* Standing: `test_ast_attest.py` (owns the baseline), `test_security_lint.py`, redundancy gate.

**R3: manifest `status`.** After the reading order it calls `verify(..., do_collect=False)` on the extraction and lists `FROZEN-MODIFIED`, `FROZEN-MISSING` and new frozen files, and says it does not check collection (`test_manifest_status_lists_drift_and_says_it_skips_collection`). `status --dropped-from <file>` prints first the dropped nodes whose test file still exists (`test_dropped_nodes_with_a_surviving_file_print_first`). Standing: `test_gate_manifest.py`.

**R4: `ceremony`.** All tests drive the real command line.
* *Digests and trust start.* A launcher digest differing from the pasted one refuses (control: match passes). An unsigned anchor refuses without `--first-run` (control: signed passes); an anchor signed outside the roster refuses; a roster differing from the packet's row refuses. With `--first-run` the screen shows the unsigned-base line with both ids and the count.
* *`repin` itself.* An edited `scripts/repin.py` refuses `ceremony` without `--first-run` (control: anchored bytes pass). `--first-run` means "the anchored entry is absent or different": it refuses when the entry equals the running file, refuses an owed AST pin, and refuses on any output from the reviewed-commit diff.
* *Scripts before they run.* `bootstrap/reanchor.sh` differing from the packet's row refuses before `validate`, `show-report` and `hash-package` (control: match passes). **First task of R4: test whether the script runs from a private copy of the hashed bytes.** If it does, run the copy; if not, hash it immediately before each call, and the record names that gap. A package rewritten between the report and the yes refuses (control: unchanged passes); the launcher's `hash-package` and the script's own `hashlib` must agree.
* *Key checks.* A key loaded in a scratch agent refuses before stage 1 and again before stage 2 (control: unloaded passes); a key in a second agent reached only through an injected `launchctl` lookup refuses (control: absent passes); an unencrypted key (`ssh-keygen -y -P ''` exits 0, no terminal, stdin closed) refuses (control: encrypted passes). "Could not ask" is shown, not refused. The refusal prints `SSH_AUTH_SOCK=<path> /usr/bin/ssh-add -d <key>.pub`. All tool calls use absolute paths (a test with `PATH` emptied still runs).
* *Signer environment.* With `SSH_AUTH_SOCK`, `SSH_ASKPASS`, `SSH_ASKPASS_REQUIRE`, `DISPLAY` and `WAYLAND_DISPLAY` set in the parent, the stage-2 child holds none and only `HOME`, `PATH`, `TERM`, `LANG` at most (control: a copied environment signs with no person).
* *One prompt, and the passphrase is the only control.* On a pseudo-terminal with the key unloaded, a scratch ceremony counts exactly one passphrase prompt (control: socket left in, zero prompts); no terminal, no signature. The script never reads, stores or passes the passphrase: a test greps its source for stdin, `getpass` and environment reads in the signing path, and a test that types a wrong passphrase sees the script do nothing with it. The script prints "asked once, now" before stage 2. This test says a pseudo-terminal can satisfy a terminal check and pins only "a pipe cannot".
* *The launcher's advice.* The note that the `ssh-add` advice does not apply is printed before stage 2 and after a stage-2 failure, and "load it and re-run" is never relayed (control: remove the line and the test fails).
* *Stage 1* runs in a new session with no controlling terminal, stdin closed and a short environment (control: with a terminal the probe prompts). Each disclosure the called tools make (candidate-code banner, anchor note, untracked-files record, interpreter-minor hold, unsigned-anchor state) appears in output (control: remove the line, the test fails). The list is built from the tools' source at R4 and named in the commit body.
* *Verification and end.* `git verify-commit` against the packet-pinned roster refuses an unsigned checkpoint, one signed by a key outside the roster, and one checked against the candidate's roster (control: a good one passes). "Done" prints only for a good signature by the expected fingerprint. The end prints both new ids, the record's path and digest, the "not in either agent when asked" line and the push line; it runs no push (test: no `git push` in the child's calls). Summary 2 refuses `no`.
* Standing: `test_reanchor.py` (launcher, unchanged), `test_gate_reanchor.py`, Bandit, redundancy.

**R5: lockfile (only if owed).** Parses the mappings from the `HEAD` blob with `ast`, never imports them (`test_the_lockfile_adapter_does_not_import_candidate_code`, with a marker module that must not run); reads of a record's `dst` stay inside the repository. If no correction is owed, the plan's record says so and R5 is closed with no code.

**R6: retire the old paths.**
* **R6a (agent, prose).** `bootstrap/AST_BASELINE_RUNBOOK.md` cut to one page; `python scripts/check_cairn.py` and `python scripts/link_check.py` clean (the runbook is cited by `AGENTS.md` without an anchor). A one-line status pointer in the strategy note.
* **R6b, MAINTAINER-ONLY.** Delete `scripts/correct_pinned_digests.py` and `bootstrap/tests/test_correct_pinned_digests.py`; remove `drive()` and `--run` from `scripts/reanchor_ceremony.py`. The edit is to frozen files. Expected report from `python bootstrap/tests/_gate_manifest.py verify` (derived, not carried forward): `FROZEN-MODIFIED` for `scripts/reanchor_ceremony.py`, `FROZEN-MISSING` for the two deleted files, and the dropped nodes of `test_correct_pinned_digests.py` (nine in the committed manifest, which lists them). The Maintainer's ceremony follows and lands just before the 0.5 cut's. Afterwards `rg 'drive\(|--run' scripts/reanchor_ceremony.py` finds nothing (control: the same grep finds both on the parent commit).

**Security Review findings, and where each closes.** The ids appear here only.

| Finding | Chunk | Test or command that closes it |
|---|---|---|
| SR-1 reading order, attest-module change, tracked `.pyc`, closure change | R1 | the byte-comparison, isolation, `.pyc`, `_ast_attest.py` and closure tests above |
| SR-2 no `repin` path writes the manifest | R2 | the hard-coded output set test; the `gate_manifest.json` refusal |
| SR-3 summary rendered from the bytes to be written | R2 | `test_every_key_the_write_changes_is_on_screen_before_the_question` (its "typed code" is replaced by the yes, by Revision 3) |
| SR-4 extraction of `HEAD`; untracked module not in output | R1, R2 | the untracked-module and `HEAD`-moves tests; one digest from `package` in two checkouts |
| SR-5 safe-write specifics (a) to (f) | R2 | the safe-write tests; the comment on `_guard.py` |
| SR-6 untrusted text through `encode_display` | R1 | the ESC and CR subject test; bytes read; the blob id of `encode_display` is in the transaction |
| SR-7 lockfile mappings parsed, not imported | R5 | the marker-module test (only if built) |
| SR2-1 loaded or unencrypted key refused, twice, in both agents | R4 | the three key-check tests with controls |
| SR2-2 passphrase is the only control; "asked once, now" | R4 | the one-prompt test; the passphrase-never-read test |
| SR2-3 launcher digest; anchor signature against the packet roster | R4 | the digest, unsigned-anchor, outside-roster and roster-row tests |
| SR2-4 `reanchor.sh` hashed before each call; package digest bound to the yes | R4 | the artifact-differs and package-rewritten tests |
| SR2-5 `repin.py` in the hashed list; `--first-run` is "absent or different" | R1, R4 | the byte-comparison test (R1); the edited-`repin` tests (R4) |
| SR2-6 (a) check the AST write | R2 | **Departs from the review's wording**: the script makes no commit (Decision), so the check reads the working tree, not a commit object. The Internal Security Review judges this. |
| SR2-6 (b) `ssh-add` advice overridden | R4 | the advice test |
| SR2-6 (c) absolute tool paths | R4 | the emptied-`PATH` test |
| SR2-6 (d) only `yes` counts; record says "yes typed on a terminal" | R2, R4 | the answers test; the record's text |
| SR-8 (inherited gaps) | outside | board rows, not this plan |

Proposed paths:
* `scripts/repin.py`
* `bootstrap/tests/test_repin.py`
* `bootstrap/tests/test_repin_ceremony.py`

## Scope delta

**Scope delta**: degraded, as Revision 3 declares and the Decision allows ("each scope reduction in the Revision's Scope delta is allowed as listed"). Carried unchanged: the transaction and safe write, the reading order, the manifest-not-written rule, the extraction, the provenance listing, the per-chunk budget. The one change this plan makes to the contract is the Maintainer's own answer: no AST commit by the script. Nothing is dropped beyond the Revision's list.

## Verification

**Boundary A (iteration, scoped).** Per chunk, the tests and gates named in its criteria, always with `python -m pytest <the named files>` (never the bare suite) plus the standing gates: `python scripts/quality_gate.py --sub neutrality --sub redundancy`, `python scripts/check_cairn.py`, and `python scripts/claim_check.py <file>` for each authored Markdown file. Bandit runs through `bootstrap/tests/test_security_lint.py`. A test that reads the touched files but is not named is found by `rg -l '<path or name>' bootstrap/tests`.

**Boundary B (integration).** **Boundary B mode**: `full`. This plan touches a trust-ceremony surface and the gate manifest, so bounded mode refuses. It runs once, after the last implementation commit, on a clean committed tree under Python 3.13.x: `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` then `python scripts/quality_gate.py --sub neutrality --sub redundancy`. Because nobody sets `CAIRN_FULL_SUITE` for an implementation, the plan's record is scoped and carries `**Certified by**: pending` until the next certifying run (before a push, the re-anchor or a release cut). The record is appended as `## Implementation verification -- <agent> -- <date>` with the template's fields, and lists any skipped signing test with its reason.

**Boundary C (code review, one loop).** One review of the reviewed range, then one revision answering it; a second pass only for new defects. The reviewer attacks, in order: (1) the byte comparison before import (mutate each list member, in a separate copy); (2) the signing route: a key loaded at any moment the script does not check, a stored passphrase, the stage-2 environment; (3) whether any `repin` path can reach `gate_manifest.json`; (4) the safe writes under a symlink race; (5) whether every disclosure test fails when its line is removed; (6) the SR2-6 (a) departure; (7) the budgets. The reviewer never runs the full suite.

**Stopping rule.** A size budget that fires, a refusal that fires on two ordinary runs in a row, two different outputs under one digest, or a signing form that signs with no person on the script's route: stop and put it to the Maintainer.

## Plan review -- Claude Sonnet 5.5 (Internal, fresh session) -- 2026-10-26

**Conclusion.** The plan delivers the Decision's premise and keeps its three binding answers (one key, no AST commit by the script, the same-user limit). It is not ready to implement as written. I raise three blocking findings, each a one-cell fix, and eleven non-blocking ones. The plan's five departures from Revision 3 are sound, with one change I would make to each of two of them (N2, N3). The Internal Security Review is a separate pass; this pass does not discharge it.

```
Reviewed commit: 63445e53
Target: the whole plan (Source proposal, Scope, Sequence, Acceptance criteria, Scope delta, Verification), read against Revision 3 and the Decision of the source proposal and against the current tree
Prior findings: none
Assurance path: required(Internal + Internal Security Review); this pass is the Internal one
```

**Obligation**: the ordinary (Internal) plan review declared in the header. It does not clear the Internal Security Review.
**Tier**: Internal
**Model**: Sonnet 5.5, fresh session; I did not write the plan
**Reviewed commit**: 63445e53
**Findings**: raised (3 blocking, 11 non-blocking)

**Foundations**

1. **Should this happen as framed?** Yes, the plan delivers the Decision's premise: every Revision 3 requirement (three verbs, the 11 steps, the reading order, key checks, transaction, safe writes, first run, chunks R1 to R6) has a chunk, and the R4 criteria carry a control for each refusal. Gaps in what each criterion names are N1. The one binding answer that changes the build is carried: no commit step exists for the AST pin (R2, plan line 79). -- `dev/plans/repin-build.md:66-101` against `dev/proposals/archive/2026-10-26-claude-repin-build.md:1118-1176` and `:1278-1312`.
2. **Best alternative.** The plan's shape is already the simple one: no `apply` verb, no commit step, one script. The simpler and safer build is to read `HEAD` as raw objects (`ls-tree -r -z` plus `cat-file blob`), as Cairn already does, and not through `git archive` (B3). The second simplification is order: remove `drive()` after the first real `repin` ceremony, not before it (B1). -- `bootstrap/tests/_gate_preflight.py:413-440`, `bootstrap/REANCHOR_RUNBOOK.md:259-260`.
3. **What would show it wrong.** Any of these on the first run of the plan's own controls: (a) the R1 control "anchored bytes pass" fails because importing `_gate_preflight` loads five modules outside the plan's list (B2); (b) `repin ceremony` refuses at its own reading order after R6b edits `scripts/reanchor_ceremony.py` (B1); (c) the emptied-`PATH` test fails because the reused `compare` and `_git` call a bare `git` (N8); (d) no scratch bed reaches a real signature, so the one-prompt and verification tests cannot run (N5). -- `bootstrap/tests/_gate_preflight.py:49-53`, `scripts/reanchor_ceremony.py:108-117`, `bootstrap/tests/_gate_manifest.py:228`, `bootstrap/tests/test_reanchor.py:957-985`.

### Blocking findings

**B1. R6b cannot be run by the tool it helps build, and the plan does not say so.** Reading-order step 4 byte-compares `scripts/reanchor_ceremony.py` with its anchored entry and refuses on any difference (plan line 67; Revision 3 step 4). R6b edits that file (plan line 101). From that commit until a ceremony anchors the new bytes, `repin ceremony` refuses at its own reading order. "The Maintainer's ceremony follows" does not say how that ceremony runs. It also collides with M2: if R6b lands before the first `--first-run`, M2 refuses; and the Decision puts that first run at the 0.5 cut. The file is not in the ten-member authority closure (`bootstrap/tests/_gate_preflight.py:600-621`), so this needs no transition ceremony, only a hand ceremony. The same refusal will hold for any later edit to any of the six listed files; the plan should say that is by design. *Satisfier:* write in R6b and M3 that the ceremony that anchors R6b's bytes is by hand under `bootstrap/REANCHOR_RUNBOOK.md`, and fix the order: either R6b lands after M2 (an extra by-hand ceremony beyond the cut's one), or R6b is held until the cut's ceremony is by hand and `repin`'s first run moves after it. This is the Maintainer's call and costs a ceremony either way, so put it as one plain question with a default (default: R6b after M2, the extra ceremony by hand). Add to R4 one test: an edited `scripts/reanchor_ceremony.py` refuses `ceremony` with a message naming the by-hand runbook (control: anchored bytes pass).

**B2. The R1 list of byte-compared files cannot satisfy R1's own "loaded module outside the list refuses" rule, and two imports are unaccounted for.** The list is `bootstrap/tests/__init__.py`, `_ast_attest.py`, `_gate_manifest.py`, `_gate_preflight.py`, `scripts/reanchor_ceremony.py`, `scripts/repin.py` (plan line 67). `_gate_preflight.py` imports `_gate_reanchor` at module top (`bootstrap/tests/_gate_preflight.py:49-53`), and `_gate_reanchor.py` imports `_oracle`, `_oracle_activation`, `_gate_transition`, `_gate_manifest` and `_oracle_trust` (`bootstrap/tests/_gate_reanchor.py:48-58`; `_oracle.py:77` adds `_oracle_trust`). None of those five is in the list, so importing `_gate_preflight` runs unverified bytes, or trips the post-import refusal on every honest run. Separately, SR-6 requires `encode_display` (`templates/skills/_lib/session.py:189`); `tools/session.py` and that file are byte-identical today (`cmp`), neither is frozen (`_gate_manifest.py:339-363`) and neither is in the list, and the plan never says where `repin` imports it from. *Satisfier:* in R1, state for each of `_gate_preflight`, `encode_display`, and `compare`/`check_packet_pair`/`values_field`: which process imports it, from which file, and whether its bytes are compared first. Then either (a) extend the list to the transitive imports (stricter, and the list is `repin`'s own), or (b) do not import `_gate_preflight` (use only `_gate_manifest`'s `verify` and read the ten closure members from `HEAD` blobs yourself). Name the mutation test: one mutated transitive module per member refuses before it runs (control: anchored bytes pass), using a marker module that must not execute. The Security Review should check this against SR-1.

**B3. `git archive` is the wrong extraction tool, and Cairn's own record says why.** R1 and Revision 3 step 3 extract `HEAD` with `git archive` (plan line 67). `git archive` reads in-tree `.gitattributes`, so a tracked `export-ignore` or `export-subst` changes what lands. Cairn has reproduced this: `_gate_preflight._tree_entries` says a tracked file marked `export-ignore` was silently absent and "reproduced, not theorised" (`bootstrap/tests/_gate_preflight.py:413-440`), and `REANCHOR_RUNBOOK.md:259-260` says "`git archive` is not used". The plan's tests (untracked module absent, once committed present; zero-member refuses) do not catch it: an engine file dropped by `export-ignore` just shrinks the AST output, and the pin would bless a smaller engine. There is no `.gitattributes` in the tree today (`git ls-files`), which is why nothing has failed. *Satisfier:* build the extraction from `ls-tree -r -z --full-tree` plus `cat-file blob`, written in `repin` (`_gate_preflight` cannot be imported cheaply, see B2), and add `test_the_extraction_ignores_gitattributes`: a `.gitattributes` with `export-ignore` on an engine file and with `export-subst` on a listed file, and the extraction still holds both files byte-for-byte (control: no attributes file). This changes the mechanism, not the Decision: "extract `HEAD`" stays.

### Non-blocking findings

**N1. Several Revision 3 refusals have no named test.** Present in Revision 3 and absent from the R2 and R4 criteria: step 2's refusals (stdin or stdout not a terminal; `HEAD` not on a branch; a dirty tracked file; interpreter minor differs; `reanchor.sh validate` fails); a signing-key fingerprint not in the roster (step 3); a transaction file that is a symlink, not the user's, or writable by others (listed as a refusal at plan line 78, no test in that line); the answers test for the digest question and for Summary 2 (only `no` on Summary 2 is tested; SR2-6(d) cites an "answers test" in R4 that R4 lacks); Summary 2's content (authority-file changes, anchor signature state, key fingerprint); the record's content and "yes typed on a terminal". The dirty-tracked-file refusal matters most: the post-write check in R2 ("only the named paths differ", plan line 79) is exact only because step 2 refused a dirty tree first. *Satisfier:* one bullet each, with a control, in R2 and R4.

**N2. SR2-6(a), the working-tree check: sound as far as it goes; I would add a commit-object check on re-run.** The script cannot check a commit it does not make, so reading the working tree is the right replacement, and it is exact given N1's dirty-tree refusal. What it cannot see is what the Maintainer then commits. I would have the next `ceremony` run read the record of the previous run (the record is outside the repository and the plan already writes it) and check from the commit object that `HEAD`'s last commit changed only the recorded paths to the recorded blob ids, and show "not checked: no record" otherwise. It needs no commit step and restores the property Revision 3 asked for. Leave the judgement to the Security Review; I recommend it. Use `git diff --no-ext-diff` with `core.fsmonitor=false` for the working-tree read, and name the stat-cache case (a same-size, same-mtime edit) by comparing `hash-object --no-filters` of the file with the index entry, not only `git status`.

**N3. The passphrase source-grep is a weak instrument alone.** A grep for `stdin`, `getpass` and environment reads in the signing path fails only on the spellings it names, and says nothing about a child. Per `AGENTS.md` "Confirm the instrument", pair it with a behavioural test: the test's own known throwaway passphrase, typed on the pseudo-terminal, appears in no argv, no environment, no record file and none of the script's output (control: the test finds the same string in its own harness buffer, so the search can match), and a planted `getpass.getpass()` in a copy of the signing function makes the grep test fail. Keep the grep as a tripwire only.

**N4. Two test files: sound.** The split keeps R4's heavy bed apart from the fast R1 to R3 tests, adds only a `FROZEN-NEW` entry, and the M2 diff already names all three paths (plan line 56). One change: R4's `--first-run` criterion (plan line 87) should name all three paths and add a test that a change to `test_repin_ceremony.py` alone refuses; Revision 3's own Q6 listed two.

**N5. The reuse of the `test_reanchor.py` builders may not reach a real signature.** The `ceremony` fixture commits stub closure files and a marker `reanchor.sh` that only writes a file (`bootstrap/tests/test_reanchor.py:940-985`). Stage 2's real signing path is `_gate_preflight.py:2630` and needs the real checker, the real `reanchor.sh` and a collection. Revision 3 listed this as "not measured" (source proposal, line 1110). The plan's R4 tests ("one passphrase prompt", "a good signature passes") need a scratch bed that runs the real stages. *Satisfier:* make "build and run a scratch bed that reaches a real stage-2 signature with a throwaway key" the first R4 task, beside the existing copy-of-`reanchor.sh` task, and say what happens if it cannot (the stopping rule's "put it to the Maintainer").

**N6. The R1 standing check is false in the current tree.** "`_gate_manifest.py verify` lists only `FROZEN-NEW` for the new files" (plan line 72). Frozen files already differ from the anchored manifest (`dev/PLANNING.md:285-307`: owed `FROZEN-MODIFIED` rows), and `verify` runs a pytest collection unless given `--no-collect`. *Satisfier:* "the `FROZEN-*` lines of `verify --no-collect` before the chunk and after it differ by exactly the `FROZEN-NEW` lines for the new files". R6b's derived report (plan line 101) stays derived at that time, which is right.

**N7. Two of the plan's own fences are looser than they read.** "An agent chunk never signs" (plan line 43) conflicts with R4's tests, which sign scratch commits with a throwaway key. Say: never signs except with a throwaway key in a scratch folder; never reads `~/.ssh` or the real anchor; never runs `repin ceremony`, `--first-run` or step 5 against the working repository (`status` and `package` are read-only and allowed). The other MAINTAINER-ONLY steps (M1, M2, M3, R6b) each name who acts and no agent chunk contains a push, a re-anchor or a passphrase; I found no step that reaches one.

**N8. "All tool calls use absolute paths" (plan line 89) cannot pass with the reused helpers.** `reanchor_ceremony.git` runs `["git", ...]` through `PATH` (`scripts/reanchor_ceremony.py:108-117`) and so does `_gate_manifest._git` (`bootstrap/tests/_gate_manifest.py:228`). A test with `PATH` emptied fails on the first `compare` call. Revision 3 puts the sentence under Key checks, and S5 accepts a substituted `git`. *Satisfier:* scope the emptied-`PATH` test to `ssh-keygen`, `ssh-add`, `launchctl` and the shell, and say that `git` resolves through `PATH` as before (an accepted residual), or resolve `git` to one absolute path once and pass it to the reused helpers.

**N9. R5 has no trigger test and no budget.** "Only if a correction is owed when R4 lands" names no command that decides "owed" (plan line 97); Revision 3 also gave R5 no budget (plan line 52 says "none stated", which is honest). The stopping rule then has nothing to fire on. I would add a number (about 100 lines, my choice, not a measure) and a command that reports whether `dev/.cairn/cairn-lock.yml` differs from what the `HEAD` mappings give. If R5 is built, the transaction has three outputs and the "both temporaries written and checked before either is replaced" test must be run with three.

**N10. R6a should wait for a real `repin` AST pin.** Cutting `bootstrap/AST_BASELINE_RUNBOOK.md` from 194 lines to one page removes the by-hand procedure that `AGENTS.md:528` points at, and that the plan's own fallback ("do the steps by hand as today", plan line 60) and M2's "AST pin by hand once more" both use. Sequence R6a after M1 has run once on the real tree; until then the full runbook stays. It is prose no test or manifest pins (`git grep` finds it only in `AGENTS.md` and archived records).

**N11. `--reviewed-commit` after a code-review revision.** Plan line 56 says `<id>` is "the commit the R4 code review names", and line 140 says one code review of the whole range. If the revision that answers the review edits `scripts/repin.py` or its tests, `git diff <id> HEAD` is not empty and `--first-run` refuses, which is the check working. State which commit `<id>` is in that case (the revision's last commit, named in a short addendum by the code reviewer or by the Maintainer), so the first run does not stop on its own safeguard. The reuse search (plan line 20) also omits the repository's own sterile git launcher and raw-tree reader (`_gate_manifest._git`, `_gate_preflight._tree_entries`); name them as reused or as set aside, with the reason (B2, B3).

**Departures, one line each.** No `apply` verb: sound; Revision 3 never had one, and the Decision's "apply" is `ceremony` step 5 (but R2's tests need a named entry point before `ceremony` exists, and R4 owes an end-to-end test that an owed AST pin is written, the stop line printed, `HEAD` unchanged, and a re-run proceeds; see N1). SR2-6(a): see N2. Source grep: see N3. Two test files: sound (N4). R5 without a budget: matches Revision 3, but I would add one (N9).

### Lenses used (each with its evidence)

* **1 Claims.** Checked against the current tree: the frozen-file table is right (`gate_manifest.json` has 195 `frozen_files` keys; `scripts/reanchor_ceremony.py`, `correct_pinned_digests.py`, its test, `scaffold_ast_known_new.json` and `security_check.py` are keyed; `scaffold_ast_baseline.json` is `cascade_mutable`; `scripts/repin.py` and the two test files are absent and match the globs at `bootstrap/tests/_gate_manifest.py:339-363`); `FROZEN-NEW` is allowed at `:669`; nine pinned nodes of `test_correct_pinned_digests.py` exist (counted from the fixture); `ALLOWLIST` is empty at `bootstrap/security_check.py:138` and `scan_targets` globs `scripts/*.py` (`:718-725`), so the Bandit claim holds, but the plan names no fallback if a MEDIUM finding appears (editing `security_check.py` is a frozen-file edit; I would say "fix the code or give the line a rationale'd `# nosec`, never edit `ALLOWLIST`"); `values_field`, `compare`, `check_packet_pair` exist at `scripts/reanchor_ceremony.py:146`, `:184` and `:266`; the builders exist at `bootstrap/tests/test_reanchor.py:70`, `:957`, `:988`, `:1005` and `:1025`; `AGENTS.md:528` cites the AST runbook without an anchor. The plan has no stale line citation.
* **2 Production path exercised by tests.** R2's apply step has no command-line entry until R4 builds `ceremony` (N1); the R4 bed may not sign for real (N5); the extraction test does not exercise attributes (B3).
* **3 Design completeness.** Import graph of the byte-compared list (B2); R6b ordering (B1); `--reviewed-commit` after a revision (N11).
* **4 Silent failure / fail-closed.** `export-ignore` shrinks the extraction silently (B3); the commit the Maintainer makes is never checked (N2); a transitive module executes unverified (B2).
* **5 Cross-document consistency.** Re-ran the plan's reuse search (`rg 'def (compare|check_packet_pair|values_field)' scripts bootstrap/tests`, which matched all three, so the pattern can match) and searched for the sterile git launcher and the raw tree reader, which the plan does not name (N11); `git grep correct_pinned_digests` finds the file only in its own test, the fixture and archived records, so R6b's deletion strands no live caller; `AST_BASELINE_RUNBOOK.md` (N10).
* **6 Drift.** The R1 standing check no longer matches the tree (N6); the "all tool calls" sentence no longer matches the reused helpers (N8).
* **7 Lifecycle / process placement.** Fences and Waiting lines match the template (`dev/plans/_template.md:44-55`); fence gaps in N7; ceremony order and who runs each by-hand step in B1 and N10.
* **8 Scope.** Two test files and an R5 budget are plan-level choices inside Revision 3's Scope delta; no accepted scope is removed. B1's by-hand ceremony and N10's order move work but drop no accepted outcome; B1's default adds one by-hand ceremony, which is why it goes to the Maintainer.
* **9 Name the satisfier.** Each finding above ends in its satisfier.

**Status.** Findings are raised, so the Status line moves to `revising-plan` (`dev/plans/_template.md:12-14`). The author folds B1 to B3 and N1 to N11 into the operative cells and answers with a disposition table (no second plan-review pass). B1's ordering goes to the Maintainer as one question with its default.

**Coverage.** *Covered:* the lenses above, Revision 3 against every chunk, the frozen-file derivation, the Bandit claim, the cited paths, and every MAINTAINER-ONLY fence. *Not covered / low confidence:* I ran no tests and did not run `verify`, `ssh-keygen`, `ssh-agent` or the launcher, so every claim about runtime behaviour is from reading source; I did not measure whether importing `_gate_preflight` really loads the five modules under `python -I` (I read the import statements, not a run); I did not check the Security Review's findings table (SR-1 to SR2-6) for completeness or judge the SR2-6(a) departure, which is the Internal Security Review's pass and is a separate pass this review does not discharge; I did not read Revisions 1 and 2, the first Review, or either Security Review beyond what Revision 3 quotes; Linux, timing, and the Maintainer's passphrase habit are unmeasured, as Revision 3 says.
