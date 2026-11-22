# A trial of the release secrets scan on the Mac (2026-11-22)

Job 7 of the Mac session (board, "Waiting on you"): before the cut, check that the secrets scan can report clean on the Mac. The Maintainer's word: *"You have my permission for all items on this board"* (chat, 2026-11-22).

## Answer

**It cannot report clean today, for two separate reasons, and either one stops the cut** (`release/RELEASE_PROCESS.md`, "The cut", step 3: only exit 0 passes).

1. **The history read has a size cap that Cairn's own history is over.** `dev/tools/git_read.py` line 38 sets `HISTORY_MAX_BYTES` to 64 MiB (67,108,864 bytes). The whole history read the scan needs (`git log -p -U0 --full-history --all`) is 104,078,935 bytes. Both legs then report `DEGRADED` ("the required Git history operation did not complete successfully", exit 20), with no scan done.
2. **Under the cap it finds 43 hits, none yet reviewed.** `dev/tools/portable_security_policy.json` holds a list of reviewed false positives, `gitleaks.fingerprints`, and it is empty. Read through masked context, all of the hits look like false positives (below), but a person has not accepted them.

The scanner itself works: the admitted Mac build matched its recorded digest (gitleaks 8.30.1, evidence `GL-2026-11-18-darwin-arm64-8.30.1`, mode `full`), and a two-commit repository scanned clean (exit 0).

## What was measured

Fresh single-history clones of the local repository, scanned with `python dev/tools/run_portable_security_sweeps.py --target <clone> --policy dev/tools/portable_security_policy.json --json`, Python 3.13.13, gitleaks 8.30.1, on the Mac:

| History | Commits | `git log -p` output | Result |
|---|---|---|---|
| v0.2.0 | 160 | not measured | exit 0, both legs clean |
| v0.3.0 | 467 | not measured | exit 10: 2 findings in each leg |
| v0.4.0 | 2,606 | 47,685,039 bytes | exit 10: tree 6, history 9 |
| v0.5.0 | 3,084 | 54,629,741 bytes | exit 10 |
| v0.6.0 | 4,493 | 75,077,874 bytes | exit 20, degraded (over the cap) |
| `0.9-dev` at `891dfd6a` | 7,845 | 104,078,935 bytes | exit 20, degraded (over the cap) |

Each scan took 2 to 8 seconds. The runner verifies the bytes of its Git helper before it loads it, so a copy with a raised cap was refused; that control worked as designed, and the repository's own files were not edited. To count what a full scan would find, I ran the admitted `gitleaks` directly on the pristine clone with its default rules and secrets redacted. At v0.4.0 that gives the runner's own counts exactly (history 9, tree 6), so I take the counts below to predict the runner's.

At `891dfd6a`: **history 23 hits** (all rule `generic-api-key`; 9 files, 10 commits) and **current tree 20 hits** (7 files: 12 in `dev/plans/archive/`, 4 in `dev/proposals/archive/`, 3 in `tests/fixtures/protected_test_roster.json`, 1 in `tests/test_security_finding_confidentiality.py`).

## What the hits are

I read each of the 23 history hits with every long token masked to its first four characters and its length. By that reading: 15 are `"<path>.py": "<64 hex characters>"`, the SHA-256 file digests of roster, manifest and evidence JSON; 6 are public SSH key fingerprints (`SHA256:` and 43 characters) quoted in two old documents, with the made-up addresses `maint@example.org` and `attacker@evil.com`; 1 is a short made-up value in `test_security_finding_confidentiality.py`, a test about not leaking findings; and 1 is `api_key = "abc1…"` in `test_foldback_export_scan.py`, a test of the scanner. None looks like a credential. This is my reading of masked text: I did not unmask any value or check one against a real service, and the 20 tree hits were counted but not read line by line (they are in the same files as the history hits).

## What a clean scan needs

- **The cap.** Raise `HISTORY_MAX_BYTES` (the history read grew from 75 MB at v0.6.0 to 104 MB now, about 30 MB in three weeks), or read the history in ranges. Raising it is not one constant: `dev/tools/git_read.py` and its shipped twin (`templates/skills/_lib/git_read.py`) change, and 22 other files name the helper's pinned SHA-256 and must take the new one in step: 8 tools under `dev/tools/`, 9 shipped twins under `templates/`, `install/_scaffold/lockfile.py`, 4 test helpers (`tests/gauge.py`, `tests/gen_legacy_code_review_passes.py`, `tests/measurements.py`, `tests/tier_inventory.py`) and the install lock. About 25 protected files change together, they all appear on the next signing page, and a change to what a security tool accepts takes a Security Review. A range option in the runner alone (scan only commits after a named tag) would touch two files, but it scans less than "every branch and tag", which the release step says.
- **The reviewed list.** Someone accepts the false positives and the 43 fingerprints go into `gitleaks.fingerprints`. The runner's `--triage-record` writes them in the form the list takes.
- **Or a waiver.** The scan was waived for 0.8; waiving it again for 0.8.1 needs the Maintainer's word and a line in the release notes.

My recommendation: raise the cap, review the fingerprints, and scan, since the hits are test data and digests and the cap is one constant. That is for the Maintainer to decide; nothing here is built.

## Not checked

Whether any of the 20 tree hits differs in kind from the history hits; the hits under a different rule set (the runner may add rules: it matched gitleaks' defaults at v0.4.0 only); a run on the release commit itself; Linux and Windows. The clone was made from the local repository, so a fresh clone from GitHub was not tried. Nothing was committed to Cairn's own files for this trial.
