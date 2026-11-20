# Plan: let the re-anchor pass a long history, and shrink the Maintainer's part

**Source proposal**: `dev/proposals/archive/2026-11-19-claude-simpler-reanchor-ceremony.md`
**Status**: awaiting-plan-review
**Waiting on Maintainer**: which Linux or macOS host runs the ceremony tests for C1 and C2; they cannot run on Windows (see Verification)
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
- `render_changes` (line 1082) refuses a baseline that gains or loses a key, which a net change over history will. C1 adds a display-only variant that shows those keys and reuses `parse_output`.
- The two old fixture paths (under the old `bootstrap` folder) are mapped inside `check_stop_records` only. C1 lifts that mapping so the display and the digest check share it.
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

One code review (usual and Security) after C3. No earlier review point: C2 changes only where `run_ceremony` stops, not what C1 accepts.

**Protected files, and the reason the Maintainer will see at the signing:**
- `release/repin.py`: the driver now checks the end state of the three pinned files and shows their net change, instead of walking history, and has a dry-run mode.
- `release/REANCHOR_RUNBOOK.md` (an authority-closure member): a one-page card and two notes are added; no existing step is removed.

`dev/rules/development-environment.md` and the tests are not on the protected list. **Staleness (read, not run):** the AST baseline stays current, because no engine file changes and its keys name no `release/` path (0 matches). The gate manifest names neither changed file. The install lock stays current except the `CHANGELOG.md` record (`living_state`); C3 refreshes it through the repository's own lock finalize, never by hand.

## Acceptance criteria

**C1.** The reader's record, in transition mode, lists a digest line for each of the three pinned files (raw Git blob, sha256) and one line recording the digest of the net-change text it read. `prepare-reader` prints both. The driver refuses a wrong, missing, duplicate or malformed line, and refuses a pinned file one byte off. It no longer calls `check_stop_records` in transition mode. Before stage 1 runs candidate code, it computes the net change from the old anchor to the candidate from Git objects, old paths mapped to new, key by key. It prints that text right before the Summary 2 prompt, and the `yes` covers it. The ordinary ceremony, `apply-reviewed-pin` and `commit-reviewed-pin` are unchanged. Tests (a), (b), (d), (e) pass.

**C2.** `ceremony --check-only` runs every check the real run makes before `key_checks` (line 3004), including the transition-mode digest check, and computes the launcher digest itself against the record. It runs no `ssh-keygen` or `ssh-add` against the private key (reading the public key's fingerprint stays), never starts stage 1, writes nothing in the ceremony folder, prompts for nothing, and exits 0 only if the real run would reach the key probe. It prints the Maintainer's command only after it passes. Test (c) covers a stale trusted checkout and a values file naming the wrong checkout, each refused by check-only and by the real run with the same reason.

**C3.** The runbook's first screen is the card (outline below). The reference stays below it, and its reader paragraph says the reader records three digests and the net-change digest. The pointer names where the graphical prompt applies. `python tests/check_cairn.py` and `python dev/tools/link_check.py` pass on every edited file. The changelog entry sits under Minor changes (Cairn's own ceremony tool).

**The card, in plain words.** What the agent hands over: the command, the fingerprint of the old signer you hold, and the reader's record with its launcher digest. What you check: the launcher digest at the first prompt (computed beside the one you paste); the package digest and your signing-key fingerprint at Summary 2; and the net change of the three pinned files, shown just before. What you type: the digest, `yes` at each prompt, and your key's passphrase once, in the terminal (the passphrase prompt gets no graphical helper here, because the signing stage receives only `HOME`, `PATH`, `TERM` and `LANG`). Do not run the launcher by hand.

**Security answers.** S1 to S5 as revised, and the three "Signals the change is wrong", hold unchanged. Re-answered where chunking matters: S2, the negative controls are (b) and (e) in C1, and check-only's exit is paired with the real run in C2. S3, `repin ceremony --transition` fires the check, over exactly three paths.

## Scope delta

**Scope delta**: preserved. Nothing accepted is removed.

## Verification

Entry points and homes. `repin ceremony --transition` (tests (a), (b), (d), (e)) and `repin ceremony --check-only` (test (c)) in `tests/test_repin_ceremony.py`; the displayed net change and the printed command in `tests/test_reanchor_driver_disclosures.py`. `tests/test_repin.py` changes only if a selected test breaks. Existing transition tests that relied on the history walk are updated, not deleted. A developmental probe of the display's length over the real range (the lock alone changed 248 lines added and 118 removed) is thrown away before archive.

Selection (measured): `python tests/tier_inventory.py for` the five paths above selects 7 test files, the three homes among them. At the starting commit the implementer measures all 7 once, keeps that failing list, and calls a failure a host failure only if it is on that list. I ran only the three homes once at `a611c044` on this host (Windows, Python 3.13.5, Anaconda): 37 passed, 115 failed and 134 errors in 276 seconds. By file, 249 failures or errors: 113 in `test_repin.py`, 135 in `test_repin_ceremony.py`, 1 in `test_reanchor_driver_disclosures.py`. The repeated message is git's `could not create temporary file`. Cause (Strategy; code read and one test run): the test bed gives Git an environment with no temporary-folder variable, and the ceremony is written for POSIX systems, meaning Linux or macOS (its `CHILD_PATH` is `/usr/bin:/bin`). So on Windows the ceremony tests cannot show C1 or C2 pass, and the implementer needs a POSIX host. Measured on 2026-11-20: the shared Linux host's name does not resolve from this machine, and this machine's Linux subsystem has Python 3.14.4, Git and the SSH tools but no pytest. Which host is used is the Maintainer's choice (header line).

Canonical runtime (`dev/rules/certifying-runs.md`). Checks on this host: the selected tests and the prose gates. The joined run, and any check that needs the canonical runtime, wait for the arc's joined run, to which this plan's `repin.py` change lands first. Not checked: any ceremony, any key, the real old-anchor range (the anchor ref is not in this checkout).
