# Certification evidence

Test runs kept so a later release can reuse them instead of running the same tests again on the same inputs. The rule is the last paragraph of [Certifying runs](../../rules/certifying-runs.md). The Maintainer's word, 2026-11-22 (chat): *"Make sure that the evidence from this scan is preserved as evidence for the certification run. Re-running tests is wasteful and bad practice when literally nothing has changed."*

**What is here.** One run is three files: the junit report (`<date>-<platform>-<commit>.junit.xml.gz`, gzip, the pytest report as written), a per-file count table (`...-per-file.csv`: file, tests, passed, failed, errors, skipped, seconds), and a line for it below. The commit is the one the run was made at; the tree id lets you check that a later commit holds the same files.

**How a release uses it.** At the release commit R, for each platform: take the newest run's commit E, list what changed (`git diff --name-only --diff-filter=d E R`), and run again only the test files that failed at E or whose inputs changed (the rule says which inputs). The release note names E, how many files stand on it, and each file rerun with the changed path that put it there.

## Runs

| Platform | Commit E | Tree id | Python, pytest, git | Started (UTC) | Elapsed | Result |
|---|---|---|---|---|---|---|
| Linux, Ubuntu 24.04.5 on aarch64 (a VM), OpenSSL 3.0.13 | `891dfd6ab098f48f1fe7bacd9cfc2290307c53e8` | `df4279a4edf3a30fd6ae2bf40d6ee83e01c7806c` | 3.13.13, 9.0.3, 2.56.1 | 2026-11-22 17:29 | 51 min 01 s | 5,966 tests: 5,745 passed, 175 failed, 46 skipped |
| Windows 11 on ARM64 (a VM), x64 Python, Git for Windows with its `bash` on the path | `273d13aae9c690fa689318fb4d022c12abab4adf` | `e8d6d51b199faf8412a160c82ad1d82c3c5aade5` | 3.13.18, 9.2.0, 2.56.0 | 2026-11-22 17:51 (part 1), 21:52 (part 2) | part 1 about 3 h 43 min, stopped; part 2 14 min 03 s | 5,981 tests in two parts: 4,633 passed, 564 failed, 136 setup errors, 484 skipped, 164 not run (see below) |

The Linux run covered every test file (`tests/`), a wider set than the certification selection (`python tests/tier_inventory.py cert-files`, 126 of 142 files at that commit). Inside the selection, **106 files passed with nothing skipped, 12 passed with skips** (the 46 skips in the run are tests for Windows or the Mac, a case-insensitive disk, or a missing `zsh`; the report names every reason), **and 8 files had failures**. Outside it, the other 16 files are Cairn's own signing, gate and release tests, which run on the Mac only. The eight failing files and what came of each (all found and traced on the Linux VM on 2026-11-22):

| File | Failed | Cause | Resolution |
|---|---|---|---|
| `tests/test_security_check.py` | 77 | The strict native-evidence check refuses any platform but the Mac and Windows, by design | Skips on Linux, with the reason in the test (`67ac79de`) |
| `tests/test_upgrade_removes_retired_files.py` | 1 | Made `Scripts/` then wrote into `scripts/`, one folder only on a case-insensitive disk | Test makes `scripts/` (`591d756a`); the node passed on the VM and the Mac |
| `tests/test_security_net.py` | 1 | `openssl req -not_before` needs OpenSSL 3.4; Ubuntu has 3.0 | Test signs with `openssl ca` instead (`591d756a`); node passed |
| `tests/integration/test_meter.py` | 1 | An unlinked file's inode number is handed straight back on ext4, so the replacement looked like the same file | Test makes the replacement before removing the old file (`591d756a`); node passed |
| `tests/test_session_writes_contained.py` | 1 | The same inode reuse in the swapped-file test | Same repair (`591d756a`); node passed |
| `tests/security/test_git_read.py` | 1 | The floor on the count of pinned tools was 23; the code has 22 (the simple meter reads no Git) | Floor set to 22 (`273d13aa`); not rerun on Linux |
| `tests/test_quickstart_sequence.py` | 1 | The quickstart named a `docs/` folder a fresh install no longer makes | Quickstart text corrected (`1cc04a9d`); not rerun on Linux |
| `tests/test_ast_attest.py` | 1 | The engine package's recorded baseline is out of date until the Maintainer's baseline step | Waits for that step; fails on every platform until then |

The four nodes marked "passed" were run once each on the Linux VM and once on the Mac with the repaired test, by a helper, on 2026-11-22; their reports were not kept. They are node evidence only: at the release commit each of those files is run again, as the rule says for a file that failed at E.

**The Windows run came in two parts, and why.** The first part was the whole suite (`tests/`, seeded order), stopped by hand at 4,981 of 5,981 tests: ceremony tests of Cairn's own signing tool left an `ssh-agent` running that held the suite twice, for about 66 and 83 minutes, and the log, not a junit report, was all that survived. Its outcomes were recovered from the log by position against the seeded collection order (`...-part1-collect-order.txt.gz`; every percent mark in the log agrees with that order, which is the check that the mapping is right). The log's per-test characters are `.` pass, `F` fail, `E` setup error, `s` skip; the log has no message for a failure. The second part ran only the certification-selection tests the first part had not reached (836, node list in `...-part2-node-list.txt.gz`) as an ordinary junit run: 737 passed, 38 failed, 61 skipped. The 164 tests left unrun are Cairn-only or release-only. The per-file table (`...-per-file.csv`) merges the two parts and ends in a `not_run` column.

**Windows, inside the certification selection (the Windows list):** 244 tests failed, 206 in the first part and 38 in the second, in about 30 files. The largest groups are the portable security sweeps (91, in the first part), the session-writes-contained file (18) and the security-finding confidentiality file (13). Causes are not yet traced; the first part has no messages. Windows is an equal partner, so each is a defect until shown to be a test assumption.

**Not covered.** The Linux command line was not written down (the report holds 5,966 tests over `tests/`; the run was launched by hand on the VM). The Mac has no run in this folder; it runs the whole suite at the release commit. Windows: the first part's failures have no messages, and nothing here says which failures are tests assuming a Mac or Linux and which are product defects.
