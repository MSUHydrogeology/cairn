# The release secrets scan, reviewed (2026-11-23)

Role: Implementation. Follows `dev/measurement/secrets-scan-trial-2026-11-22.md`, which found two blockers: the history read was over its size cap, and 43 hits had no reviewer. The Maintainer's decision (chat, 2026-11-23): "A: raise the cap. This project is not large by comparison with many." No Security Review was asked for: the cap is a size bound of the same kind as before, not a new input.

## Answer

1. **The cap is raised and the scan now reads all of Cairn's history.** `HISTORY_MAX_BYTES` went from 64 MiB to 256 MiB in `dev/tools/git_read.py` and its twin (commit `b7e62006`). The history read is now 106,579,962 bytes (101.6 MiB), 40% of the new cap.
2. **The scan finds 43 hits, 23 in history and 20 in the current tree, and none is a credential.** 30 are file digests, 10 are public key fingerprints in example text, 3 are made-up test values. This is the same 23 and 20 the trial predicted.
3. **All 43 are recorded as reviewed** in `gitleaks.fingerprints` of `dev/tools/portable_security_policy.json` (and its shipped twin, which a test requires to be identical).
4. **A fresh clone then scans clean: exit 0** (see "The clean scan" below). That is the scan of one commit; the cut needs it again on the final commit.

## The clean scan

A new `git clone` of this repository at `/private/tmp/cairn-cut`, at `583f31aae494bfb800b0945229daff77a29e2f17` (`git rev-parse HEAD` in the clone; the commit that recorded the 43 entries and this record), then, from the repository root with Python 3.13.13 and gitleaks 8.30.1:

`python dev/tools/run_portable_security_sweeps.py --target /private/tmp/cairn-cut --policy dev/tools/portable_security_policy.json --json`

- **Exit 0.** Result 0, mode `full` ("admitted artifact ('8.30.1', 'darwin', 'arm64') matched digest f414bc2fb952... (evidence GL-2026-11-18-darwin-arm64-8.30.1)").
- **Current tree: CLEAN**, 0 findings. **History: CLEAN**, 0 findings.
- **Before the 43 entries** the same scan of a fresh clone one commit earlier gave exit 10: 20 tree findings and 23 history findings. **Same entries, clone at another path:** exit 10, tree 20 findings, history clean.
- **Scanned on the Mac only.** This record's own last edit (the commit that added this section) came after the scanned commit; it holds no digest or key-like line.

## How each hit was read

I read each hit's line with every token of 14 or more characters cut to its first four characters and its length, so no value was printed, copied or committed. I did not unmask a value or check one against a service. The hits by class:

| Class | Tree | History | What it is |
|---|---|---|---|
| File digest | 14 | 16 | A JSON line `"<repo path>": "<64 hex characters>"`. For all 4 distinct path and value pairs I checked that the value is the SHA-256 of a real version of the file the path names (4 of 4 matched; values not printed). The scanner reacts to words like `token` and `access` in the path. |
| Public key fingerprint | 5 | 5 | Example output of a signature check ("Good signature for ... with ED25519 key SHA256:...") in two old design documents, with made-up addresses. A fingerprint of a public key is not a secret. |
| Made-up test value | 1 | 2 | A planted marker string in a test about not leaking findings (tree and history), and a fake `api_key = "..."` literal in a test of the export scanner (history only). |
| Real credential | 0 | 0 | |

By file (history paths are the old paths at that commit; some begin with `bootstrap/`, which no longer exists):

| Leg | File | Hits | Class |
|---|---|---|---|
| tree | `dev/plans/archive/2026-10-28-test-trust-boundary/c1a-refresh-918638f.json` | 5 | digest |
| tree | `dev/plans/archive/2026-10-28-test-trust-boundary/c1b-evidence-6cc95fa7.json` | 3 | digest |
| tree | `dev/plans/archive/2026-10-28-test-trust-boundary/c1b-roster-6cc95fa7.json` | 3 | digest |
| tree | `tests/fixtures/protected_test_roster.json` | 3 | digest |
| tree | `dev/plans/archive/release-authenticity.md` | 1 | key fingerprint |
| tree | `dev/proposals/archive/2026-08-03-claude-release-authenticity.md` | 4 | key fingerprint |
| tree | `tests/test_security_finding_confidentiality.py` | 1 | test value |
| history | c1a-refresh digest file, commit `c387dec7` | 5 | digest |
| history | c1b-evidence digest file, commit `884e6d53` | 3 | digest |
| history | c1b-roster digest file, commit `884e6d53` | 3 | digest |
| history | the protected roster fixture, commit `979018d4` | 3 | digest |
| history | the gate manifest fixture, commits `6ac5eb6f` and `e5ecaa56` | 1 each | digest |
| history | release-authenticity plan, commit `606c360f` | 1 | key fingerprint |
| history | release-authenticity proposal, commits `7c0077b2` and `d0fa454e` | 2 each | key fingerprint |
| history | the finding-confidentiality test, commit `d2a3f4b1` | 1 | test value |
| history | the export-scan test, commit `a82dfed5` | 1 | test value |

## How the list can break (read before the cut)

- **History entries are tied to commit ids.** Each is `<commit>:<path>:<rule>:<line>`. If any of those 10 commits is rewritten (rebase, amend, history filter), its entries stop matching and the scan reports the hit again with exit 10. It fails loudly; it does not pass silently.
- **Tree entries are tied to the clone's absolute path, and to line numbers.** The runner resolves its target to an absolute path before scanning, so a tree entry reads `/private/tmp/cairn-cut/<path>:<rule>:<line>`. The 20 tree entries match only when the scanned clone sits at exactly `/private/tmp/cairn-cut`. A clone anywhere else gets exit 10 with the same 20 hits. The entries also name lines, so an edit that moves lines 253, 398 or 417 of `tests/fixtures/protected_test_roster.json`, line 133 of `tests/test_security_finding_confidentiality.py`, or any archived file listed above, breaks them. `release/RELEASE_PROCESS.md` step 3 does not name a clone path; this record does. A runner change to emit paths relative to the target would remove the dependence, but the runner is a protected surface and I did not touch it.
- **The scan must be repeated on the final release commit.** That commit will have more commits than the one scanned here (the version bump, the notes, any roster re-anchor). Run step 3 of "The cut" there, from a fresh clone at `/private/tmp/cairn-cut`, and put its exit and `git rev-parse HEAD` in the release notes. A new file with a long hex digest or a key-like line is a new hit, not a reviewed one.
- **The shipped twin carries the list.** `tests/test_portable_security_sweeps.py` requires `templates/modules/team-gated/portable_security_policy.json` to equal the installed policy byte for byte, so adopters receive these 43 entries. They match nothing in an adopter's repository.
- **The strict path is separate.** `release/security_check.py` scans a frozen history and a detached candidate checkout; its checkout will not be at `/private/tmp/cairn-cut`, so the 20 tree entries are unlikely to match there (I did not run it). The v0.8.1 cut does not use that path (`release/RELEASE_PROCESS.md`, "Strict release-security evidence").

## Cost of the larger cap

- **Memory.** The history read is held in memory up to the cap, as a byte buffer and then a copy of it, so the worst case is about two times the cap, 512 MiB, on the Mac and Linux. On Windows the worker replies in base64 text and the parent decodes it, several times the cap. That is read from the code, not measured at the cap or on Windows. Measured on the Mac with `/usr/bin/time -l`, one run of the whole scan: largest single process 296 MB, 15 seconds in all; `git log` alone takes 2.4 seconds of the 10-second read limit.
- **Headroom.** The trial measured about 30 MB of growth in three weeks; at that rate the history reaches 256 MiB in about 16 weeks. That is one interval, not a forecast.
- **Other readers of the constant.** `dev/tools/content_scan_runner.py` and `tests/gauge.py` read the same constant, so their cap moved too.

## Not covered

Rules beyond the scanner's defaults and the runner's own configuration; a branch or object that is not reachable from a ref in the clone; a value checked against a real service; Linux and Windows runs of the scan.
