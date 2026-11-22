# Plan: let the re-anchor pass a long history, and shrink the Maintainer's part

**Source proposal**: `dev/proposals/archive/2026-11-19-claude-simpler-reanchor-ceremony.md`
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Change the signing script so a repository whose lock file was rewritten many times can be re-anchored, add a dry-run that finds setup mistakes before the Maintainer starts, and put a one-page card at the top of the runbook.

## Build summary

The re-anchor script stops treating each routine lock rewrite as an unapproved change. It instead checks that the three pinned files match digests an independent reader recorded, and shows the Maintainer their net change once. A new `ceremony --check-only` lets an agent find setup mistakes first. The runbook opens with a card of what the Maintainer checks and types. No ceremony is run here; the re-anchor stays the Maintainer's operation, tracked on the roadmap.

## Source proposal

Accepted as revised at the heavy tier on 2026-11-20: in transition mode, a digest check and one net-change display replace the per-commit walk; a dry run stops before the key; a card opens the runbook. This plan reopens none of it.

## Scope

Surfaces: `release/repin.py`, `release/REANCHOR_RUNBOOK.md`, `dev/rules/development-environment.md`, the three test homes, `CHANGELOG.md` and the roadmap. Result: the next re-anchor needs no `repin.py` edit and no reading beyond the card.

**Where the code differs from the proposal's wording** (read at the current commit, not run):
- `render_changes` (line 1082) refuses a baseline that gains or loses a key, which a net change over history will. C1 adds a display-only keyword to `render_changes` that shows those keys; it already prints `(absent)` for a key on one side only. The default refusal stays, and its test (`tests/test_repin.py`, the add-or-drop refusal near line 1664) stays unchanged.
- The two old fixture paths (under the old `bootstrap` folder) are mapped inside `check_stop_records` only. C1 lifts that mapping for the display. The digest check reads the three new-layout paths and needs no mapping.
- The driver accepts only the lowercase word `yes` (`ask_yes`, line 1498), not `YES`. The card says `yes`; `YES` belongs to the separate key-away step of `verify-candidate`.
- `check_preconditions` demands a terminal, and the ceremony's `finally` always writes `ceremony-record.txt`. Check-only skips both.
- The layout evidence binds the digest of `repin.py` (line 2221). Any later edit to it, or to the runbook, makes that evidence stale, so these changes land before the evidence is prepared.

Out of scope: the ordinary ceremony still refuses routine lock updates (line 3003 stays unconditional for it); the re-anchor itself.

**Reuse.** `parse_output`, `blob_at`, `check_record`, `record_values` and the `legacy_moves` mapping. Searched `release/` and `tests/` for `net change`, `render_changes` and `stop record`; no other renderer exists.

### Documentation / doctrine surface

Descriptive layer only: the runbook and a pointer in `dev/rules/development-environment.md`. No `AGENTS.md` or adopter text changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Part 1, transition mode only | none | digest lines in the reader's record, the digest check, the net-change display, tests (a) (b) (d) (e) |
| C2 | Part 2, `ceremony --check-only` | C1 committed | the dry run, test (c) |
| C3 | Part 3 and the records | C1 and C2 final, so the card quotes real prompts | the card, askpass and trusted-checkout notes, the pointer, the reader's instructions, the changelog entry, the roadmap line |

One code review (usual and Security) after C3. No earlier review point: C2 changes where `run_ceremony` stops and adds one refusal, a `signing_key` that is not a `.pub` file; it does not change what C1 accepts.

**Protected files, and the reason the Maintainer will see at the signing:**
- `release/repin.py`: the driver now checks the end state of the three pinned files and shows their net change, instead of walking history, and has a dry-run mode. It also refuses a signing key path that is not a `.pub` file.
- `release/REANCHOR_RUNBOOK.md` (an authority-closure member): a one-page card and two notes are added; no existing step is removed.
- The ceremony test files (`tests/test_repin_ceremony.py`, `tests/test_reanchor_driver_disclosures.py`, and `tests/test_repin.py` only if a selected test breaks): tests for the new checks are added and tests that relied on the history walk are updated; none is deleted.

`dev/rules/development-environment.md` is not on the protected list. **Staleness (read, not run):** the AST baseline stays current, because no engine file changes and its keys name no `release/` path (0 matches). The manifest and roster name the changed `repin.py` and test files under pre-layout paths, so they are already out of step with HEAD until the re-anchor refreshes them. The install lock stays current except the `CHANGELOG.md` record (`living_state`); C3 refreshes it through the repository's own lock finalize, never by hand.

## Acceptance criteria

**C1.** The reader's record, in transition mode, lists a digest line for each of the three pinned files (raw Git blob, sha256) and one line recording the digest of the net-change text it read. `prepare-reader` prints both. The driver refuses a wrong, missing, duplicate or malformed line, and refuses a pinned file one byte off. It no longer calls `check_stop_records` in transition mode. Right after `check_record` (line 2945) and before `reading("validate")`, it computes the net change from the old anchor to the candidate from Git objects, old paths mapped to new, key by key. It refuses there if the text's digest differs from `net-change-sha256`; check-only makes the same check. It prints that text right before the Summary 2 prompt, and the `yes` covers it. The ordinary ceremony, `apply-reviewed-pin` and `commit-reviewed-pin` are unchanged. Tests (a), (b), (d), (e) pass. Test (b) includes a `net-change-sha256` line one digit off, which must refuse before `reading("validate")`.

Record lines: `pinned-sha256 <64 hex> <path>` for each of the three new-layout paths, and `net-change-sha256 <64 hex>`, the digest of the printed lines joined by newlines plus a final newline. `check_record` gains a keyword `net_change`; the lines are required exactly when it is passed, which only a transition `run_ceremony` does, and `prepare_reader_inputs` writes them exactly when `ctx['closure_changed']` is non-empty. `check_record` checks the lines' form and the three pinned digests and hands back the recorded `net-change-sha256`; the comparison with the computed text is the step after it. The driver holds the computed text in memory and prints that same text. A key on one side only prints `(absent)` on the other; a pinned file missing at the old anchor shows every key as added. Every key and value in the display passes through `d()`. Print the text just above the line `Summary 2: what you are about to sign`. Open it with a line the driver prints that gives the display's line count, so stage 1's relayed output cannot pass as part of it; that count line is not part of the digested text.

**C2.** `ceremony --check-only` runs every check the real run makes before `key_checks` (line 3004), including the transition-mode digest check, and computes the launcher digest itself against the record. It runs no `ssh-keygen` or `ssh-add` against the private key (reading the public key's fingerprint stays), never starts stage 1, writes nothing in the ceremony folder, prompts for nothing, and exits 0 only if the real run would reach the key probe. It prints the Maintainer's command only after it passes. Test (c) covers a stale trusted checkout and a values file naming the wrong checkout, each refused by check-only and by the real run with the same reason. `main` skips `write_record` and `finish` for it; `run_ceremony` calls `check_preconditions(ctx, need_terminal=False)`, skips the pasted-digest prompt and every `confirm`, returns just before line 3004, and prints the command as its own arguments with `--check-only` removed. Before reading any key file, check-only and the real run refuse unless `signing_key` ends in `.pub`. Test (c) also covers that refusal.

**C3.** The runbook's first screen is the card (outline below). The reference stays below it, and its reader paragraph says the reader records three digests and the net-change digest. The reader computes each `pinned-sha256` itself from `git cat-file blob <read-commit>:<path>`, reads the whole net-change text, and only then records its digest. The pointer names where the graphical prompt applies. `python tests/check_cairn.py` and `python dev/tools/link_check.py` pass on every edited file. The changelog entry sits under Minor changes (Cairn's own ceremony tool).

**The card, in plain words.** Have ready: your key is encrypted and in no ssh agent, and you are in a terminal window. What the agent hands over: the command, and the reader's record with its launcher digest. What you check: that `--expected-fingerprint` in the command is the old signer's fingerprint that you hold yourself, not one the agent supplied; the launcher digest at the first prompt (computed beside the one you paste); the package digest and your signing-key fingerprint at Summary 2; and the net change of the three pinned files, shown just before. What you type: the digest, `yes` at each prompt, `YES` once at `verify-candidate`, if asked to run it, and your key's passphrase once, in the terminal (the passphrase prompt gets no graphical helper here, because the signing stage receives only `HOME`, `PATH`, `TERM` and `LANG`). Do not run the launcher by hand.

**Security answers.** S1 to S5 as revised, and the three "Signals the change is wrong", hold unchanged. S1 rests on the reader computing the digests itself, which C3 requires. Re-answered where chunking matters: S2, the negative controls are (b) and (e) in C1, and check-only's exit is paired with the real run in C2. S3, `repin ceremony --transition` fires the check, over exactly three paths.

## Scope delta

**Scope delta**: preserved. Nothing accepted is removed.

## Verification

Entry points and homes. `repin ceremony --transition` (tests (a), (b), (d), (e)) and `repin ceremony --check-only` (test (c)) in `tests/test_repin_ceremony.py`; the displayed net change and the printed command in `tests/test_reanchor_driver_disclosures.py`. `tests/test_repin.py` changes only if a selected test breaks. Existing transition tests that relied on the history walk are updated, not deleted. A developmental probe of the display's length over the real range (the lock alone changed 248 lines added and 118 removed) is thrown away before archive.

Selection (measured): `python tests/tier_inventory.py for` the five paths above selects 7 test files, the three homes among them. At the starting commit the implementer measures all 7 once, keeps that failing list, and calls a failure a host failure only if it is on that list. I ran only the three homes once at `a611c044` on this host (Windows, Python 3.13.5, Anaconda): 37 passed, 115 failed and 134 errors in 276 seconds. By file, 249 failures or errors: 113 in `test_repin.py`, 135 in `test_repin_ceremony.py`, 1 in `test_reanchor_driver_disclosures.py`. The repeated message is git's `could not create temporary file`. Cause (Strategy; code read and one test run): the test bed gives Git an environment with no temporary-folder variable, and the ceremony is written for POSIX systems, meaning Linux or macOS (its `CHILD_PATH` is `/usr/bin:/bin`). So on Windows the ceremony tests cannot show C1 or C2 pass, and the implementer needs a POSIX host. The Maintainer decided where (chat, 2026-11-20): "We can use the mac for the re-anchor." The implementer and the code reviewers work in a session on the Mac, the host these tests were written for. What was learned first on this Windows machine's Linux subsystem (Ubuntu 26.04, Python 3.14.4), kept for the roadmap row on verifying releases on Linux: the ceremony test setup names fixed Mac tool paths (`/usr/bin/env`, `/bin/mkdir`, `/bin/cat`), and the signing launcher refuses any tool reached through a symbolic link (`release/reanchor.sh`, `no_symlink_on_path`), so no current Ubuntu runs these tests as written. In a scratch copy with the tools found by their real location, failures in the seven selected files fell from 120 to 99 of 895; most of the rest show the gate's requirement for Python 3.13. Nothing from that probe is committed.

Canonical runtime (`dev/rules/certifying-runs.md`). Checks on the Mac: the seven selected test files, measured once at the starting commit first, and the prose gates. The joined run, and any check that needs the canonical runtime, wait for the arc's joined run, to which this plan's `repin.py` change lands first. Not checked: any ceremony, any key, the real old-anchor range (the anchor ref is not in this checkout).

## Plan review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

```
Reviewed commit: 507766cf8757c8bb0cf710e6f58f4592f9ed2c8c
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised (four blocking)
**Verdict**: REVISE

**Elapsed**: about 20 minutes (estimate). **Tokens**: unknown.

The plan tries to let a long history pass by checking the end state and showing its net change once, and to give an agent a dry run. Its cited lines hold (1082, 1498, 2221, 3003, 3004), and the card's prompts match the driver.

**Foundations**

1. **Should this happen as framed?** Yes; C1 to C3 carry Parts 1 to 3 and S1 to S5 -- `release/repin.py:2559`, `3003`.
2. **Best alternative.** The display variant can be a keyword on `render_changes`, which already prints `(absent)` for a one-sided key -- `repin.py:1082-1090`.
3. **What would show it wrong.** A ceremony test where `--check-only` exits 0 and the real run then refuses before `key_checks`; test (c) is that test.

**Findings**

1. **Blocking.** Design left open. Add at the end of C1: "Record lines: `pinned-sha256 <64 hex> <path>` for each of the three new-layout paths, and `net-change-sha256 <64 hex>`, the digest of the printed lines joined by newlines plus a final newline. `check_record` gains a keyword `net_change`; the lines are required exactly when it is passed, which only a transition `run_ceremony` does, and `prepare_reader_inputs` writes them exactly when `ctx['closure_changed']` is non-empty. The driver holds the text in memory from before stage 1 and prints that text. A key on one side only prints `(absent)` on the other; a pinned file missing at the old anchor shows every key as added. Print the text just above the line `Summary 2: what you are about to sign`."
2. **Blocking.** Check-only has no mechanism. Add to C2: "`main` skips `write_record` and `finish` for it; `run_ceremony` calls `check_preconditions(ctx, need_terminal=False)`, skips the pasted-digest prompt and every `confirm`, returns just before line 3004, and prints the command as its own arguments with `--check-only` removed."
3. **Blocking.** The card sends the Maintainer wrong. In "What the agent hands over", replace "the fingerprint of the old signer you hold" with "the command"; under "What you check" add "that `--expected-fingerprint` in the command is the old signer's fingerprint that you hold yourself, not one the agent supplied", and under ready add "your key is encrypted and in no ssh agent, and you are in a terminal window". Add "`YES` once at `verify-candidate`, if asked to run it".
4. **Blocking.** The Scope sentence "the tests are not on the protected list" and "the gate manifest names neither changed file" are false. The manifest's protected roster and `frozen_files` name `repin.py` (old path `scripts/repin.py`) and the ceremony test homes (`tests/fixtures/gate_manifest.json`). Replace with: "The manifest and roster name the changed `repin.py` and test files under pre-layout paths, so they are already out of step with HEAD until the re-anchor refreshes them."
5. Non-blocking. Add a refusal of a wrong `net-change-sha256` to test (b); the plan names none.
6. Non-blocking. The digest check needs no old-path mapping, only the display. The plan runs about 1,500 words against a 1,000 target.

**Not covered**: no run, ceremony or key (over the word target because four blocking findings carry exact words); the real-range net change was measured by script only (about 100 changed fixture keys, 101 lock records); Security questions are left to that pass.

## Plan review -- Claude Opus 5.5 (Security reviewer) -- 2026-11-20

```
Reviewed commit: 8bc610406a8bba35a91d4874d2470a346a782387
```

**Obligation**: Internal Security Review
**Tier**: Security Review
**Findings**: raised (three blocking)
**Verdict**: REVISE

**Elapsed**: about 25 minutes (estimate). **Tokens**: unknown.

The plan keeps one deliberate approval of the end state and moves setup faults to an agent's dry run. Under the runbook's threat, honest agent mistakes (`REANCHOR_RUNBOOK.md:5`), the chunking keeps the proposal's protections, with three gaps.

**Foundations**

1. **Should this happen as framed?** Yes; transition is measured, not chosen, so the ordinary path is untouched -- `repin.py:2993-2997`, `3003`.
2. **Best alternative.** Check the net-change digest beside the other record digests, so check-only gets it free -- `check_record`, `repin.py:2945`.
3. **What would show it wrong.** Test (b) with `net-change-sha256` one digit off still reaching stage 1.

**Findings**

1. **Blocking.** The first candidate code is not stage 1: `reading("validate")` (line 2954) runs the candidate's `reanchor.sh`. In C1 replace "Before stage 1 runs candidate code, it computes" with "Right after `check_record` (line 2945) and before `reading(\"validate\")`, it computes", and add: "It refuses there if the text's digest differs from `net-change-sha256`; check-only makes the same check."
2. **Blocking.** Check-only can run `ssh-keygen` on the private key: `key_fingerprint` (line 2963) runs on `signing_key`, which may name the private file (line 2882), and line 2965 reads it as text. Add to C2: "Before reading any key file, check-only and the real run refuse unless `signing_key` ends in `.pub`."
3. **Blocking.** S1 needs the reader to compute digests, not copy them. Add to C3: "The reader computes each `pinned-sha256` itself from `git cat-file blob <read-commit>:<path>`, reads the whole net-change text, and only then records its digest."
4. Agree with the usual review's 1 to 4. Its finding 5 is blocking; its "holds the text in memory from before stage 1" is replaced by my finding 1.
5. Non-blocking. The display-only variant must keep `d()` on every key and value; `test_repin.py:1664` (the add/drop refusal) stays unchanged.
6. Non-blocking. Frame the display with a driver-printed line count, since stage 1's relayed output (line 3026) precedes it.

**Not covered**: no run, ceremony or key; `reanchor.sh` validate and the launcher read only where cited; the card's wording left to the usual review.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

Both reviews said REVISE. Every finding is accepted, and each blocking one is closed with its reviewer's own words. Where the two reviews touch the same sentence, the Security Review's words govern, as it asked.

**Usual review**

1. Blocking, design left open in C1: accepted, with the reviewer's paragraph. Its "from before stage 1" gives way to the Security Review's finding 1.
2. Blocking, check-only had no mechanism: accepted, with the reviewer's sentence in C2.
3. Blocking, the card: accepted. Swapping the fingerprint for "the command" would have printed "the command" twice, so the fingerprint is removed from what the agent hands over. The three additions are in.
4. Blocking, two false staleness claims: accepted, with the reviewer's sentence. One consequence is added: the ceremony test files join the protected-file list, with their reason.
5. A wrong `net-change-sha256` in test (b): accepted as blocking, as the Security Review rated it.
6. Accepted. The path mapping serves the display only, and the display is a keyword on `render_changes`, not a second renderer.

**Security Review**

1. Blocking, candidate code runs before stage 1: accepted, with the reviewer's words in C1.
2. Blocking, check-only could run `ssh-keygen` on the private key: accepted, with the reviewer's sentence in C2. Test (c) now covers that refusal, and the protected-file reason for `release/repin.py` names it.
3. Blocking, the reader must compute the digests: accepted, with the reviewer's sentence in C3.
4. Covered above.
5 and 6. Accepted: `d()` on every key and value, the add-or-drop refusal test unchanged, and a driver-printed line count before the display.

One sentence is Strategy's own, joining the two reviews: `check_record` checks the lines' form and the pinned digests and hands back the recorded net-change digest, and the comparison is the step after it. No reviewer read that sentence; the code review will.

Not checked: nothing was run. Which Linux or macOS host runs the ceremony tests is still the Maintainer's choice.

**Elapsed**: about 30 minutes. **Tokens**: unknown. The harness reported 168,952 tokens for the author, 145,722 for the usual review and 111,329 for the Security Review.
