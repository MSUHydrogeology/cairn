# Windows measurements for plan D2, 2026-11-22

**Role**: Implementation, measuring only. No code, test, rule or other record was changed. This is the one new file.
**Tree measured**: `891dfd6a` (the branch tip when the session began). The branch moved on while the session ran (`4434c7bd`, then `0d3f3a73`, which carries re-anchor driver changes), so the ceremony results in (e) describe the driver as it stood at `891dfd6a`, not the current one.
**Host**: `cairn-windows` (Windows 11 build 10.0.26300.9974 on ARM64; under UTM according to `dev/rules/development-environment.md`), account `cairn`, SSH login with `cmd.exe`. Python is the x64 build 3.13.18 at `C:\ProgramData\miniconda3\envs\lhm\python.exe`, pytest 9.2.0, Git 2.56.0.windows.4, GNU bash 5.3.15 (Git for Windows), curl 8.23.0 (all printed by the tools themselves on the VM).
**Elapsed**: about 35 minutes by the Mac's clock (12:09 to 12:44 EST); tokens `unknown`.

## Summary

- **No failure traced here comes from a broken VM or from Git Bash.** Each one I traced is a Windows rule that a Cairn test or the ceremony driver does not allow for. Three items work now: (a), (c) and (d). Three still fail: (b), (e) and (f).
- **(a) and (c): repaired.** The release-members contract test gives 139 passed, 1 skipped, 0 failed with Git Bash on the path (the nine older failures are gone). The fifteen failures of 2026-11-16 all pass or skip now; the file that held the fifteenth (`tests/security/test_git_read.py`) still has four other failures, one of which fails on the Mac too.
- **(d): both release routes ran to the end in Git Bash** on the published `v0.8.0` tag (ordinary route 16 s, stronger route 7 s), with the commit `d59a4268ba287d02cabf404def9a5faa694dda61` named in the release notes.
- **(e): giving Git a temporary-folder variable changes nothing.** The three ceremony files give 115 failed, 134 setup errors and 37 passed (249 of 286 not passing) both ways, test for test. Causes: the signing fixture's `ssh-keygen` call fails (136 tests; in a probe it exits 255 and `PROGRAMDATA` alone cures it), `termios` does not exist on Windows (43), the driver refuses `_socket.pyd` as a module outside its checked folders (35 at least); 35 tests are not classified.
- **(b) and (f):** the Git-absent test fails because its fake adapter has no file extension and Windows cannot find it. The socket failures (`WinError 10106`, 13 tests) come from tests that start a program with no `SYSTEMROOT`. The links were not a problem on this VM, and the gitleaks failures are the same two causes plus 51 tests I did not classify.

## How these were measured

- **Copies.** A `git bundle` of `0.9-dev` and the tags was sent with `scp` (SHA-256 `ab0f55c3cb8543f3dbeeb41fba6728af2276a79017523d74043f5d14f4e87888`, checked on the VM with `certutil`). Five clones were made from it in a new folder under `C:\Users\cairn\`, each with `core.autocrlf` false and a detached checkout of `891dfd6a`, clean at the start (`git status --short` empty). One clone each for: (a) to (c) and the probes, (f), the baseline ceremony run, the ceremony run with a temporary-folder variable, and one that held a single leftover test bed for a probe. The route checks in (d) needed no clone. On the Windows Server machine the ceremony tests left files behind in a repository root; see (e) for what I found here.
- **Every pytest run** used `-q -p no:cacheprovider -rfsE`, `PYTHONDONTWRITEBYTECODE=1`, and the x64 interpreter above. Elapsed times are pytest's own figure unless a wall-clock time is given (the VM's clock, three hours behind EST). Exit codes were read with `call echo exit=%^errorlevel%` or from the log.
- **One run per measurement**, with these extra runs, each named where it appears: the same single test rerun for per-test output (b), a verbose rerun of `test_git_read.py` (c), three nodes alone (c), the ceremony files once more with a temporary-folder variable (e, the measurement asked for), the sweeps file once more with `SYSTEMROOT` added (f), and two single tests rerun alone (f). No test was dropped or retried to get a better result.
- **Load.** Items (a) to (d) ran with nothing else of mine on the VM. In (e) and (f) I ran two streams at once to save time: the baseline ceremony run (9:23:04 to 9:26:58) overlapped the first two (f) files, and the second ceremony run (9:28:40 to 9:32:46) overlapped `test_upgrade_module_additions.py` (9:26:24 to 9:33:47). The Mac's load average read 4.81 at (a), 5.00 and 12.25 at the two (c) runs, 2.91 before the last (f) run (from `uptime`; another agent was running tests on the Mac). No failure looked like a timing failure. Where I checked, a single failure rerun alone failed the same way: the two (f) single tests, and the (c) test file rerun (same counts).
- **Probes** were small Python scripts kept outside the repository, run on the VM in new temporary folders and removed afterwards. **Harness plugins** for (e) and (f) were also outside the repository; each only adds environment variables to a program a test starts with an explicit environment, and counts what it changed (described where used). Nothing in the repository was edited, on the Mac or the VM.
- **Words.** "Measured" means I ran it and read the output. "Read" means I read the code and did not run that path. "Assumed" is marked as such.

## (a) The nine older failures in the release-members contract test

- **Command.** `cd /d C:\Users\cairn\<clone>` then `set "PATH=C:\Program Files\Git\bin;%PATH%"` then `python -m pytest -q -p no:cacheprovider -rfsE tests/contract/test_release_members_contract.py`, with `python` the x64 interpreter above. `where bash` printed `C:\Program Files\Git\bin\bash.exe`.
- **Result (measured).** Exit 0. **139 passed, 1 skipped, 0 failed in 20.55 s.** Started 9:14:32 on the VM's clock.
- **Skipped.** `test_backslash_file_field_is_refused_off_windows`, reason printed: "on Windows the backslash spelling is accepted; the next test covers it".
- **Failing tests.** None.
- **What changed from the earlier record.** The 2026-11-19 proposal record said nine failed here: eight needed `bash` (which the plain SSH login does not have) and one was a timing failure. I read the test file: eight tests start `bash -c` (two in `test_actual_pytest_identities_and_documented_sequence`, two in `test_actual_security_omission_fails_after_pytest_passes`, two in `test_adopter_owned_slow_selection_is_independent`, `test_pytest_failure_is_preserved_even_if_comparison_passes`, `test_documented_sequence_refuses_existing_report_path`). All pass with Git Bash on the path. The timing failure was fixed by plan D1 (`52cc8095`, as `dev/PLANNING.md` records); it did not recur in this single run.
- **Cause.** Not a failure now. The eight depended on `bash` being on the path (confirmed earlier today: `where bash` on the plain login found nothing).
- **Not run.** The same file without Git Bash on the path (the earlier record already measured it).

## (b) The Git-absent test in `tests/test_portable_security_sweeps.py`

- **Command.** `python -m pytest -q -p no:cacheprovider -rfsE "tests/test_portable_security_sweeps.py::test_absent_git_is_incomplete_for_the_history_leg"`, same interpreter and clone as (a).
- **Result (measured).** Exit 1. **1 failed in 1.36 s.** Failing test: `test_absent_git_is_incomplete_for_the_history_leg`. Message: `no 'history' leg in ['adapter']`.
- **Cause (measured).** The test writes a fake `gitleaks` as a file with no extension that starts with `#!<python path>`. On Windows nothing finds it. Evidence, in order:
  1. A probe that replays the test body without pytest printed the runner's whole answer: exit 5 with one leg, `adapter`, reason "'gitleaks' was not found on the trusted host path; the scan did not run", and a fake tool log with 0 lines (the fake never ran). The fake file existed in the folder on the child path.
  2. A second probe: `shutil.which` (what the runner calls) returned `None` for an extensionless file with a shebang, and found `gitleaks.EXE` once a file of that name sat beside it, with `PATHEXT` as printed (`.COM;.EXE;.BAT;.CMD;...`).
  So the run stops at the adapter leg. The history leg that the test wants to inspect is never created, and "Git is absent" is never tested. The exit code 5 the test expects first is reached for a different reason (the adapter is missing, not Git).
- **Check next (for D2).** Give the fake a Windows form the runner can run (a `.exe` or `.cmd` that the runner accepts as a trusted executable) and see whether the Git-absent case then reaches the history leg on Windows. I did not try it because that is a change to the test.

## (c) The fifteen failures of 2026-11-16

The list is in `dev/measurement/archive/windows-existing-failures-2026-11-16.md` (Run 1). The test files moved into `tests/` in the layout change (the old record names them under the old `bootstrap` folder); the two parametrised ids moved from `scripts/` to `dev/tools/`. I checked on the Mac (collection only) that all fifteen ids exist at `891dfd6a`.

- **Command 1** (the fourteen nodes in three files, from an argument file): `python -m pytest -q -p no:cacheprovider -rfsE @<file listing the 14 node ids>`. Exit 0. **13 passed, 1 skipped in 154.44 s** (9:16:14 to 9:18:51).
- **Command 2** (the fifteenth node's whole file, because, as the 2026-11-16 record found, that node fails only after an earlier test in the file leaves a cached Git version): `python -m pytest -q -p no:cacheprovider -rfsE tests/security/test_git_read.py`. Exit 1. **4 failed, 65 passed, 19 skipped in 26.74 s.** A verbose rerun (`-v -l --tb=short`) gave the same counts in 25.92 s.
- **The fifteen, one by one (measured).**
  - Passed (13): `TestProfileSizedAssembly::test_profile_change_solo_to_multi_reincludes_region`; `TestInitLock::test_review_inventory_theirs_excludes_local_edit_when_roster_matches`, `test_matching_historical_renderer_stages_inventory`, `test_historical_inventory_description_is_used_for_theirs`, `test_changed_historical_renderer_refuses_and_cleans_stage`, `test_changed_historical_metadata_refuses_and_cleans_stage` (all in `tests/test_upgrade.py`); `test_reflection_filename_is_session_distinct`, `test_session_end_WITH_handoff_DOES_emit_the_standing_capture_prompt`, `test_handoff_prunes_the_intent_surface`, `test_session_end_skips_intent_prune_in_linked_worktree` (in `tests/test_session_routines.py`); `test_real_discovery_cli_finds_planted_issue_without_decoy[link-dev/tools/link_check.py]` and `[snippet-dev/tools/sync_doc_snippets.py]`, `TestFilterSources::test_excludes_dev_archive_and_reflections` (in `tests/test_doc_drift_tools.py`) (13 in all; the command counted 13 passed).
  - Skipped (1): `tests/test_upgrade.py::TestDirtyTreeGuard::test_literal_pathspec_name_is_a_single_tracked_path`, reason printed: "Windows forbids colon and asterisks in filenames". The 2026-11-16 record named this skip as its proposed repair; it is in the tree now.
  - Passed in its file (1): `tests/security/test_git_read.py::test_read_origin_uses_git_parser_for_quoted_and_continued_values` (the verbose rerun lists it `PASSED`).
- **Four other failures in `tests/security/test_git_read.py` (not among the fifteen).**
  - `test_read_origin_ignores_the_worktree_config_extension[https]`, `[ssh]`, `[extension-after-origin]`. **Cause (measured):** the locals printed by the verbose rerun show `ReadResult(state='failed', returncode=None, stdout=b'', reason='verified-helper-buffer-unavailable')`, the unbound-worker refusal that `dev/rules/development-environment.md` describes. The helper `_real_git_config_control` reads the Git version and the origin without calling `_bind_worker_source`, which the neighbouring test (`test_read_origin_uses_git_parser_for_quoted_and_continued_values`) does call. Run alone, the three nodes skip ("real Git 2.44 or newer is required for the config control", 3 skipped in 0.80 s); they fail when run in the file's order. The 2026-11-16 record's explanation is an earlier test that leaves a cached Git version behind; I did not inspect the cache. This is the 2026-11-16 record's cause 8 again, in a new test. Windows only: the same three passed on the Mac (control, below).
  - `test_every_tool_pins_the_digest_of_the_helper_it_runs`. Message: `assert found >= 23` with `found` 22. **Not a Windows failure:** the Mac control failed the same way, and `git grep` for the three pin names over `dev/tools`, `tests`, `templates` and `install/_scaffold` finds 22 lines at `891dfd6a` (a text search; the test's own count is the one that matters). The message of commit `db4c86d4`, which set the floor of 23, says it found 24 pins then. Which two pin lines went since, and when: not traced.
- **Mac control (measured, one run).** `$HOME/conda_envs/lhm/bin/python3.13 -m pytest -q -p no:cacheprovider -rfsE` on the four nodes named above: 1 failed (the pin count), 3 passed, 0.97 s.
- **Answer.** Repaired: all fifteen. The old failures of causes 1 to 8 do not recur in the nodes I ran; cause 8's pattern recurs in three new nodes.
- **Not run.** The rest of the four files (I ran 14 of the 271 tests in `test_upgrade.py`, `test_session_routines.py` and `test_doc_drift_tools.py`), so a failure outside the fifteen in those files is unknown. Cause 1 of the old record (a copy with no `.git`) does not apply: the clone is a real repository.

## (d) The published v0.8.0 tag through both routes in `install/PROVENANCE.md`

**How the routes fetch and verify (read).**

- *Ordinary route.* Two `curl` calls with `--max-redirs 0` fetch the release API record and the release page for the tag; both must give HTTP 200. The person reads the release version and the full commit from the release notes. Then, with system, global and environment Git settings switched off, a new bare repository fetches only `refs/tags/<tag>` from the literal URL `https://github.com/MSUHydrogeology/cairn.git`. It requires `git cat-file -t` to print `tag`, peels the tag to a commit, compares it with the notes' commit, makes a detached worktree and requires `HEAD`, `git diff --quiet` and `git status --porcelain --untracked-files=all --ignored=matching` to agree. It checks no signature.
- *Stronger route.* The person writes a roster file (`principal key`) from a fingerprint compared on two channels, then the bootstrap block fetches the one tag the same way, requires an annotated tag object, binds the signed name to the requested name, runs `git verify-tag` against the roster passed by `-c gpg.ssh.allowedSignersFile`, peels the same tag object and makes the checkout with the same three checks.

**What I ran (measured).** The blocks were cut from `install/PROVENANCE.md` at `891dfd6a` by line range and run unchanged in `"C:\Program Files\Git\bin\bash.exe" <script>` (a non-interactive Git Bash, started by full path from the SSH login). The only edits were the documented inputs: the tag `v0.8.0` for the two placeholders in the first block, and the exports named in the text. `HOME` was pointed at a folder inside my disposable folder so the roster did not land in the account's real home. Git Bash tools: `sh`, `awk`, `mktemp`, `ssh-keygen` resolved to `/usr/bin` (Git's own copies), `git` and `curl` to `/clangarm64/bin`, `python` to the Windows Store stub under `WindowsApps` (as the document warns; no route command calls Python).

| Step | Result |
|---|---|
| Ordinary, step 1 (two `curl` calls) | Exit 0; both printed `200`. Release record: `tag_name` `v0.8.0`, canonical `html_url` `https://github.com/MSUHydrogeology/cairn/releases/tag/v0.8.0`, `draft` false, `prerelease` false, `published_at` 2026-11-19T22:08:40Z. The release notes state "cut at commit `d59a4268ba287d02cabf404def9a5faa694dda61`". 9:21:33 to 9:21:35. |
| Ordinary, steps 2 and 3 (inputs: tag `v0.8.0`, version `0.8.0`, that full commit) | Exit 0, 9:21:49 to 9:22:05 (16 s). `refs/tags/v0.8.0` was a `tag` object, `f410f4d2fd918edddc647075cfec6f6b3b68f70f`; its commit equalled the notes' commit; 1,100 tracked files in the checkout. Pre-execution checks: `rev-parse HEAD` printed the full commit, `git diff --quiet` exit 0, `git status --porcelain ...` printed nothing, exit 0. |
| Stronger, step 2 (roster) | The one signing key the forge's API returned for the account the release record names as its author (`ssh-ed25519`, created 2026-08-04). `ssh-keygen -l -f` printed `SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`. The same fingerprint is in the in-repository roster `dev/.cairn/allowed_signers`, which is not an independent channel and was used only as a cross-check. |
| Stronger, step 3 (bootstrap block, official URL) | Exit 0, 9:22:41 to 9:22:48 (7 s). `verify-tag` printed `Good "git" signature for cairn-release with ED25519 key SHA256:8R549...ESsM`; the block printed `PROVENANCED: tag 'v0.8.0' (object f410f4d2fd918edddc647075cfec6f6b3b68f70f), commit d59a4268ba287d02cabf404def9a5faa694dda61`. Same three pre-execution checks passed. |

The tag object and commit equal what the Mac's own repository holds (`git rev-parse v0.8.0^{commit}` and `^{tag}` on the Mac).

- **Answer.** Both routes work on the VM in Git Bash with no change to their commands. The VM reaches `api.github.com` and `github.com` over HTTPS.
- **Not run.** The two-channel fingerprint comparison (I used one channel, the forge API; the second channel, the ORCID record, was not fetched). A negative control (a wrong roster key; the 2026-11-16 run did one). The `python install/verify_integrity.py` step and the install. A Start-menu or login Git Bash. Windows' own `ssh-keygen.exe` first on the path. Refusal cases (substituted name, lightweight tag, redirect, non-200, dirty checkout). The route's workspaces under Git Bash's `/tmp` were removed by my scripts; the metadata folder too.

## (e) The ceremony tests and the temporary-folder variable

Files: `tests/test_repin.py` (79 test functions), `tests/test_repin_ceremony.py` (104), `tests/test_reanchor_driver_disclosures.py` (17); 286 tests collected once parametrised.

- **Baseline command.** `python -m pytest -q -p no:cacheprovider -rfsE --junitxml=<file> tests/test_repin.py tests/test_repin_ceremony.py tests/test_reanchor_driver_disclosures.py`. Exit 1. **115 failed, 37 passed, 134 errors in 231.88 s** (9:23:04 to 9:26:58). 249 of 286 do not pass. (The 2026-11-20 measurement on the Windows Server machine also found 249 of 286; I did not compare the two sets test by test.)
- **With a temporary-folder variable.** Same command, with a pytest plugin kept outside the repository (`PYTHONPATH` set to its folder, `-p` naming it). When a test starts a program with an explicit environment holding none of `TEMP`, `TMP` or `TMPDIR`, the plugin adds `TEMP` and `TMP` (the account's temporary folder) and nothing else. It also records each ceremony-driver stop message, per test. Counts it wrote: 1,083 `subprocess` starts with an explicit environment; 1,067 had none of the three variables and were changed; 933 of those were Git. Exit 1. **115 failed, 37 passed, 134 errors in 243.59 s** (9:28:40 to 9:32:46). **All 286 tests have the same outcome as in the baseline run** (compared per test from the two XML reports).
- **Answer.** No. Giving Git (and the driver) a temporary-folder variable through the tests' own environments does not make any further test run. The limit of this: the plugin changes only the environments the tests pass; environments the ceremony driver builds inside its own child processes are untouched. A separate probe ran the driver's `status` command in a test bed with and without `TEMP` and `TMP`: identical output both ways (below).
- **What does stop them (measured unless marked).** Classes of the 249, from the failure messages in the baseline report, plus the per-test stop records from the second run. A test is named in Appendix A with its class.

| Class | Tests | Evidence |
|---|---|---|
| The signing fixture's `ssh-keygen` call fails | 136 (134 setup errors and 1 failure in `test_repin_ceremony.py`, 1 failure in `test_repin.py`) | The setup error message is `AssertionError: (('ssh-keygen', '-q', '-t', 'ed25519', '-N', '', ...), '', '')`: the call exits non-zero with no output. A probe ran the same call with the test bed's closed environment: exit 255, no key, no message. Adding `TEMP` and `TMP`, `SYSTEMROOT`, `USERNAME`, or `SYSTEMROOT`, `TEMP`, `TMP` and `USERPROFILE` together, did not help; one probe adding each other variable of the parent environment alone found that **`PROGRAMDATA` alone makes it work**. The probe also showed Git for Windows' own `ssh-keygen` (`C:\Program Files\Git\usr\bin`) works in the closed environment. The first `ssh-keygen` on the SSH login's path is Windows' own (`C:\WINDOWS\System32\OpenSSH\ssh-keygen.exe`). The 134 setup errors come from one session fixture, so all tests that use it error. Not measured: whether those tests pass once the fixture's call works. |
| `No module named 'termios'` | 43 in `test_repin.py` | The message itself. `termios` is a Unix-only standard module. These tests need a Unix terminal (a pseudo-terminal), so they need Linux or Mac, or a different test. |
| The driver stops with "the module `_socket` loaded from `...\DLLs\_socket.pyd`, which is not on the checked list" | 35 (named by message or by the second run's per-test stop records; 58 stops of this kind were recorded, in 52 tests, some of which pass because they expect a refusal) | A probe ran `release/repin.py status` in a leftover test bed under four environments (as the bed gives it; plus `TEMP`/`TMP`; plus `SYSTEMROOT`; plus all three): exit 0, no standard output, the same refusal on standard error each time. **Read:** `check_loaded` in `release/repin.py` accepts a loaded module only if its file is under the interpreter's `stdlib` or `platstdlib` folder; on this Windows interpreter compiled modules sit in `DLLs`, outside both, so any import of `socket` by a checked module fails the check. That is a Windows assumption in Cairn's driver; I did not run it with a changed check. |
| Not classified | 35 | Messages vary (for example `assert 0 == 2`, "usage: repin", a missing file, a `repin stopped` refusal that names a tree or digest rather than `_socket`). The ceremony is written for Linux and macOS; which of these are Windows assumptions and which are further effects of the classes above I did not determine. Check next: after the three classes above are lifted in a disposable copy, rerun and read what remains. |

- **What still needs Linux or Mac tools (measured only where stated).** The 43 `termios` tests need a Unix terminal (measured: the module does not exist here). The rest of the 249 I cannot sort into "needs Unix" and "needs a Windows repair" without lifting the classes above; the two Windows repairs I verified are within reach are the `ssh-keygen` call (Git's copy works in the same closed environment; the file's own check requires `ssh-keygen` and `ssh-agent` on the path, and I did not run `ssh-agent` here) and the `_socket` check.
- **Stray files.** The 2026-11-20 note says the ceremony tests leave a stray file and a `tmp` folder in the repository root. After both runs here `git status --short --ignored -uall` in both ceremony clones was empty (lines for `__pycache__` folders filtered out; `PYTHONDONTWRITEBYTECODE` was set): not reproduced on this VM.

## (f) The socket, link and gitleaks failures seen on the Windows Server machine

**What was run.** The five files named for the 126 failures on the Windows Server machine, plus `tests/test_scaffold.py` (the 127th of that machine's first run), each as its own pytest command, one after the other, in one clone (`891dfd6a`).

| File | Result | Elapsed | Exit | Server machine, 2026-11-20 (at `76347908`) |
|---|---|---|---|---|
| `tests/test_portable_security_sweeps.py` | 96 failed, 55 passed, 3 skipped | 71.11 s | 1 | 105 failed |
| `tests/test_upgrade_module_additions.py` | 1 failed, 108 passed | 440.64 s | 1 | 11 failed |
| `tests/test_board_json_contract.py` | 219 passed, 1 skipped | 47.04 s | 0 | 7 failed |
| `tests/test_replacement_tools.py` | 36 passed, 2 skipped | 9.96 s | 0 | 2 failed |
| `tests/test_install_report_slots.py` | 1 failed, 6 passed | 23.66 s | 1 | 1 failed |
| `tests/test_scaffold.py` | 61 passed | 29.82 s | 0 | 1 failed (only in the plan record's 127-failure count) |

The two machines ran different commits (`76347908` against `891dfd6a`, with the repairs of 2026-11-20 to 11-22 in between) and are different hosts, so a smaller count here does not by itself say the host made the difference. Skips printed: named pipes unavailable (1, board file), "requires native posix test host" (2, replacement tools), POSIX admission matrix (2) and a POSIX shim test (1) in the sweeps file.

**Sockets (`WinError 10106`).** 13 tests in `test_portable_security_sweeps.py` fail with it here (the Server machine saw 13 as well; the 13 are listed in Appendix B). Measured:
1. A Python process on this VM that opens a socket fails with `[WinError 10106] The requested service provider could not be loaded or initialized` when its environment has no `SYSTEMROOT`, and succeeds when it has.
2. The tracebacks show the failing call is `socket.socket(...)` in the runner's `_Canary()` inside `cmd_verify_version_support`, in a child process that the test started with an environment of `PATH`, `HOME`, `LC_ALL` and `PYTHONDONTWRITEBYTECODE` only.
3. With a plugin that adds `SYSTEMROOT` to such explicit environments (253 starts seen, 231 changed), the 13 no longer show `10106`.
So the host sets the rule (Windows needs `SYSTEMROOT` to start sockets), the tests' closed environment omits it, and the runner does not supply it. It is not the shell. Two other test files carry a comment that says the same thing and add the variable themselves (`tests/test_api_access_security.py`, `tests/test_web_hosting_security.py`).
After the change the same 13 still fail, now for the gitleaks reason below, not for `10106`.

**Symbolic links.** On this VM the account is a member of Administrators and `SeCreateSymbolicLinkPrivilege` is enabled; a probe created a file link and a directory link. No log of the six files holds `WinError 1314` ("a required privilege is not held") and no skip reason names a link. So the link-making failures the Server machine showed are **not reproduced here**. The failing tests with "link" in the name (7 here) fail for the two causes below (names in Appendix B): adapter not found (2), fake never invoked (1), preflight stop (2, one of which then passes with `SYSTEMROOT`), and two not classified. **Cause on the Server machine: not determined.** What I would check next there: `whoami /priv` and one `os.symlink` probe on that machine (I was told not to touch it).

**gitleaks and the sweep runner.** Two causes, both measured:
1. **The preflight stop.** In 45 of the 96 failures the runner stops at a `preflight` leg: 27 print "the Windows private sweep workspace or worker could not be verified" and 18 show only the leg name `preflight`. A probe ran the runner (a copy, as the tests make it) on a small Git repository with the real `gitleaks.exe` 8.30.1 and `git.exe` on the child path: with the tests' environment it stopped at `preflight` with that reason (exit 20); with `SYSTEMROOT` added it ran the real gitleaks and ended at exit 5 "reduced provenance ... no admitted artifact is recorded for ('8.30.1', 'windows', 'arm64')". **Read, not run line by line:** the runner's Windows Git relay stops with "the Windows compiler root is unavailable" when `SystemRoot` is absent, and `run_sweep` replaces the refusals it catches by that one generic reason, so the real cause is hidden; the probe shows only that adding `SYSTEMROOT` lifts the stop. With the plugin that adds `SYSTEMROOT`, the second run of the whole sweeps file gave **85 failed, 66 passed, 3 skipped in 172.41 s** (against 96, 55, 3). 13 tests that failed now pass; 2 that passed now fail. Those two (`test_hung_or_oversized_adapter_or_git_output_is_never_clean[adapter-hangs]` and `[adapter-report-over-the-cap]`) expect exit 20, and the preflight stop gives 20: they passed for the wrong reason, and with the stop lifted they get 5 and fail. That is a measured outcome change, not a timing effect (0.35 s in the first run, about 2 s in the second).
2. **The fake adapter has no file extension.** The tests make their fake `gitleaks` as an extensionless `#!`-script (measured in (b): Windows cannot find or run it; one test shows `OSError: [WinError 193] %1 is not a valid Win32 application`). In the first run 11 failures print "'gitleaks' was not found on the trusted host path" and 8 say the fake was never invoked ("only 0 scan invocation(s)"). In the run with `SYSTEMROOT`, of the 85 failures 24 print the first message, 8 the second, 1 the `WinError 193` one and 1 a private-workspace refusal; **the other 51 print other messages that I did not classify one by one**, so I cannot say how many of those are this cause too. The real gitleaks works on this VM: `gitleaks version` printed `8.30.1`, exit 0, and the runner ran it in the probe above.

**The two other failing tests (measured).**
- `tests/test_upgrade_module_additions.py::test_adoption_treats_legacy_task_markers_as_project_text`. Failed again alone (together with the next, 4.98 s). The test writes `dev/PLANNING.md` with `write_text`, then searches its bytes for a block that has `\n` line ends. On this VM the file's bytes near the marker read `...\r\n<!-- cairn:module-task id=retired-module -->\r\n* [x] My preserved work\r\n...`: `write_text` turned each newline into a carriage return and newline. A test assumption about line ends (the same kind as cause 2 of the 2026-11-16 record).
- `tests/test_install_report_slots.py::test_removing_a_module_moves_every_slot_it_fills`. Failed again alone. A probe replayed the install and printed the second list's paths as the report gives them: `'AGENTS.md'`, `'dev\\agent_collaboration.md'`, `'dev\\plans\\_template.md'`, `'dev\\proposals\\_template.md'`. The test compares them with forward-slash spellings (`dev/plans/_template.md`); the three missing items are exactly the three with a folder in the path. A path-spelling assumption in the test.

**Answer.** Of the three named kinds: sockets are a Windows rule that Cairn's tests and runner do not allow for (not the shell, and not a fault of the VM); the gitleaks failures are the same missing variable plus a fake adapter Windows cannot run, with 51 failures not classified; links are not reproduced here and the Server machine's cause is not determined. Nothing measured points at the shell (Git Bash was not used for these runs; they ran from the SSH login's `cmd.exe`).

## Found along the way (outside the six questions)

- `tests/security/test_git_read.py::test_every_tool_pins_the_digest_of_the_helper_it_runs` fails at `891dfd6a` on the Mac as well as here (22 pin lines found, floor 23). Not a Windows matter; it needs a fix or a recount on every host.
- Two sweeps tests pass on Windows for the wrong reason (named in (f)).
- The sweep runner on Windows hides the underlying error behind one generic reason ("read": the `except` clause in `run_sweep`).
- The ceremony driver's loaded-module check (`check_loaded` in `release/repin.py`) cannot pass on this interpreter's layout.

## Cleanup

Everything this session made on the VM was removed at the end: the folder `C:\Users\cairn\cairn-d2m-20261122` (bundle, five clones, logs, probes, plugins), 54 entries it left in the account's temporary folder (names `repin-pyc*`, `cairn-release*`, `tmp*` and my probes' folders, all created after 9:10 today), and the `pytest-of-cairn` folders `pytest-296` to `pytest-298` and the `pytest-current` link (`pytest-281`, older than my first run, was left). A final check on the VM listed no `python.exe`, `git.exe`, `gitleaks.exe`, `bash.exe` or `curl.exe` process. No setting, package or existing folder was changed. Nothing was done to the Windows Server machine or any other host. On the Mac, one `git bundle` file and the logs live in this session's scratch folder; nothing in the repository was touched except this file.

## What I did not check

- Any whole-suite run (not allowed) and any file outside those named.
- (a): the contract file without Git Bash on the path.
- (c): 257 of the 271 tests in the three files besides `test_git_read.py`; the cause of the pin count's drop from 24 to 22.
- (d): the two-channel fingerprint comparison, a negative control, `verify_integrity.py`, an interactive or Start-menu Git Bash, Windows' own `ssh-keygen`, and the refusal cases.
- (e): whether the 134 signing-fixture tests pass once `ssh-keygen` works; what the 35 unclassified tests need; the ceremony at the current `HEAD` (the driver changed after `891dfd6a`); the driver's own child-process environments; the x64 interpreter only (no ARM64 interpreter run).
- (f): which of the 51 unclassified failures of the `SYSTEMROOT` run are the fake-adapter cause, and the 19 'other' failures of the first run, one by one; why the Server machine saw link failures; whether the Server machine's other counts (board 7, upgrade additions 11, replacement tools 2, scaffold 1) are the host or the earlier commit; a run with both `SYSTEMROOT` and a Windows-runnable fake adapter.
- Timing: no test of mine was timed under a quiet Mac; load was recorded, not controlled.
- Python 3.12 or the ARM64 interpreter; any host other than `cairn-windows`.

## Appendix A: the 249 ceremony tests that did not pass (baseline run)

Class: `ssh-keygen` (the signing fixture's call), `termios` (module missing), `_socket` (driver refuses the module), `not classified`.

| File | Test | Outcome | Class |
|---|---|---|---|
| `test_repin.py` | `test_the_extraction_ignores_gitattributes` | failed | _socket |
| `test_repin.py` | `test_baseline_preparation_refuses_substituted_external_roster_before_collection` | failed | not classified |
| `test_repin.py` | `test_forward_guided_ast_correction_needs_no_anchor_and_commits_only_reviewed_fixtures` | failed | not classified |
| `test_repin.py` | `test_forward_preparation_refuses_missing_or_duplicate_baseline_symbols[def other():\n    return 2\n-a baselined symbol is missing or defined twice]` | failed | not classified |
| `test_repin.py` | `test_forward_preparation_refuses_missing_or_duplicate_baseline_symbols[def f():\n    return 2\n\ndef f():\n    return 3\n-a baselined symbol is missing or defined twice]` | failed | not classified |
| `test_repin.py` | `test_forward_preparation_refuses_lockfile_debt` | failed | not classified |
| `test_repin.py` | `test_forward_review_refuses_mutated_review_inputs[packet]` | failed | not classified |
| `test_repin.py` | `test_forward_review_refuses_mutated_review_inputs[transaction]` | failed | not classified |
| `test_repin.py` | `test_forward_review_refuses_candidate_change_after_preparation` | failed | not classified |
| `test_repin.py` | `test_forward_guide_refuses_unreviewed_packet_without_writing` | failed | not classified |
| `test_repin.py` | `test_forward_guide_refuses_a_nonaccepting_review` | failed | not classified |
| `test_repin.py` | `test_forward_guide_refuses_review_binding_and_fixture_mutation` | failed | not classified |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[head]` | failed | termios |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[index]` | failed | termios |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[worktree]` | failed | termios |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[packet]` | failed | termios |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[review]` | failed | termios |
| `test_repin.py` | `test_forward_guide_refuses_changes_during_approval[fixture]` | failed | termios |
| `test_repin.py` | `test_baseline_preparation_requires_independent_inputs` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_refuses_nonobject_reader_record[[]]` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_refuses_nonobject_reader_record[null]` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_refuses_nonobject_reader_record["reader"]` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_refuses_nonobject_reader_record[42]` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_refuses_nonobject_reader_record[true]` | failed | not classified |
| `test_repin.py` | `test_baseline_preparation_builds_exact_package_after_reader_binding` | failed | ssh-keygen |
| `test_repin.py` | `test_a_case_colliding_tree_refuses_before_import` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/__init__.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_ast_attest.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_gate_manifest.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_gate_preflight.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_gate_reanchor.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_gate_transition.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_oracle.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_oracle_activation.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[tests/_oracle_trust.py]` | failed | not classified |
| `test_repin.py` | `test_each_imported_file_is_byte_compared_with_the_anchor_before_import[release/reanchor_ceremony.py]` | failed | not classified |
| `test_repin.py` | `test_a_tracked_compiled_file_refuses` | failed | not classified |
| `test_repin.py` | `test_a_loaded_local_module_outside_the_list_refuses` | failed | _socket |
| `test_repin.py` | `test_a_committed_parent_package_or_module_does_not_run_and_cannot_hide[install/__init__.py-install-ceremony]` | failed | _socket |
| `test_repin.py` | `test_a_committed_parent_package_or_module_does_not_run_and_cannot_hide[release/__init__.py-release-ceremony]` | failed | _socket |
| `test_repin.py` | `test_a_committed_parent_package_or_module_does_not_run_and_cannot_hide[release.py-release-ceremony]` | failed | _socket |
| `test_repin.py` | `test_a_committed_parent_package_or_module_does_not_run_and_cannot_hide[install.py-install-ceremony]` | failed | _socket |
| `test_repin.py` | `test_a_module_loaded_outside_the_list_is_refused_even_when_it_blanks_its_own_file_and_spec[__file__ = None]` | failed | _socket |
| `test_repin.py` | `test_a_module_loaded_outside_the_list_is_refused_even_when_it_blanks_its_own_file_and_spec[__file__ = None\n__spec__ = None]` | failed | _socket |
| `test_repin.py` | `test_the_extraction_is_never_on_the_search_path_of_a_pinned_module` | failed | not classified |
| `test_repin.py` | `test_a_tracked_symlink_or_submodule_refuses_before_import[a symlink]` | failed | not classified |
| `test_repin.py` | `test_a_tracked_symlink_or_submodule_refuses_before_import[a submodule]` | failed | not classified |
| `test_repin.py` | `test_an_unusable_tracked_path_refuses_and_writes_nothing_outside_the_extraction[..-an escaping path]` | failed | not classified |
| `test_repin.py` | `test_an_unusable_tracked_path_refuses_and_writes_nothing_outside_the_extraction[.GIT-a git folder name]` | failed | not classified |
| `test_repin.py` | `test_an_extracted_file_that_reads_back_differently_refuses` | failed | termios |
| `test_repin.py` | `test_the_repin_process_runs_isolated` | failed | _socket |
| `test_repin.py` | `test_an_edited_session_module_at_head_does_not_run` | failed | _socket |
| `test_repin.py` | `test_an_ordinary_commit_subject_prints_unchanged` | failed | _socket |
| `test_repin.py` | `test_a_tree_with_no_engine_module_refuses` | failed | _socket |
| `test_repin.py` | `test_an_untracked_engine_module_is_absent_until_committed` | failed | _socket |
| `test_repin.py` | `test_head_moving_during_a_run_refuses` | failed | _socket |
| `test_repin.py` | `test_provenance_names_the_plan_a_commit_message_cites` | failed | _socket |
| `test_repin.py` | `test_status_says_whether_repin_itself_is_anchored[anchored-release/repin.py: anchored]` | failed | _socket |
| `test_repin.py` | `test_status_says_whether_repin_itself_is_anchored[edited-release/repin.py: differs from the anchor]` | failed | _socket |
| `test_repin.py` | `test_status_says_whether_repin_itself_is_anchored[unpinned-release/repin.py: no anchored entry]` | failed | _socket |
| `test_repin.py` | `test_status_shows_a_closure_member_that_differs_from_the_anchor` | failed | _socket |
| `test_repin.py` | `test_a_different_interpreter_minor_is_shown` | failed | _socket |
| `test_repin.py` | `test_an_ast_pin_owed_lists_every_changed_symbol` | failed | _socket |
| `test_repin.py` | `test_manifest_status_lists_drift_and_says_it_skips_collection` | failed | _socket |
| `test_repin.py` | `test_manifest_status_lists_a_modified_frozen_file` | failed | _socket |
| `test_repin.py` | `test_dropped_nodes_with_a_surviving_file_print_first` | failed | _socket |
| `test_repin.py` | `test_the_apply_step_makes_no_commit_and_stops` | failed | termios |
| `test_repin.py` | `test_every_key_the_write_changes_is_on_screen_before_the_question` | failed | termios |
| `test_repin.py` | `test_only_the_exact_word_yes_writes[Yes]` | failed | termios |
| `test_repin.py` | `test_only_the_exact_word_yes_writes[y]` | failed | termios |
| `test_repin.py` | `test_only_the_exact_word_yes_writes[]` | failed | termios |
| `test_repin.py` | `test_only_the_exact_word_yes_writes[yes please]` | failed | termios |
| `test_repin.py` | `test_only_the_exact_word_yes_writes[None]` | failed | termios |
| `test_repin.py` | `test_a_pipe_on_stdin_or_stdout_refuses` | failed | termios |
| `test_repin.py` | `test_a_detached_head_refuses` | failed | termios |
| `test_repin.py` | `test_a_dirty_tracked_file_refuses_before_any_write` | failed | termios |
| `test_repin.py` | `test_a_staged_change_refuses` | failed | termios |
| `test_repin.py` | `test_an_index_bit_that_hides_changes_refuses[--assume-unchanged]` | failed | termios |
| `test_repin.py` | `test_an_index_bit_that_hides_changes_refuses[--skip-worktree]` | failed | termios |
| `test_repin.py` | `test_a_different_interpreter_minor_refuses` | failed | termios |
| `test_repin.py` | `test_head_moving_between_package_and_write_refuses` | failed | termios |
| `test_repin.py` | `test_a_file_changed_while_the_question_was_open_refuses` | failed | termios |
| `test_repin.py` | `test_a_transaction_naming_the_gate_manifest_or_any_other_path_refuses` | failed | termios |
| `test_repin.py` | `test_an_edited_output_byte_refuses` | failed | termios |
| `test_repin.py` | `test_summary_one_is_rendered_from_the_bytes_and_not_from_the_transactions_stored_text` | failed | termios |
| `test_repin.py` | `test_a_transaction_whose_stored_hash_does_not_match_its_bytes_refuses[new_sha256]` | failed | termios |
| `test_repin.py` | `test_a_transaction_whose_stored_hash_does_not_match_its_bytes_refuses[preimage_sha256]` | failed | termios |
| `test_repin.py` | `test_an_output_path_that_is_not_tracked_at_head_refuses` | failed | termios |
| `test_repin.py` | `test_a_clean_filter_cannot_hide_an_edit_from_the_tree_check` | failed | termios |
| `test_repin.py` | `test_bytes_that_change_while_the_files_are_replaced_are_caught_after_the_write` | failed | termios |
| `test_repin.py` | `test_a_second_file_that_changes_between_the_first_replace_and_its_own_refuses` | failed | termios |
| `test_repin.py` | `test_an_unsafe_transaction_file_refuses[a symlink-without following a link]` | failed | termios |
| `test_repin.py` | `test_an_unsafe_transaction_file_refuses[owned by someone else-only this user can write]` | failed | termios |
| `test_repin.py` | `test_an_unsafe_transaction_file_refuses[writable by others-only this user can write]` | failed | termios |
| `test_repin.py` | `test_a_symlinked_target_or_parent_is_not_followed` | failed | termios |
| `test_repin.py` | `test_a_directory_in_place_of_an_output_is_a_refusal_and_not_a_crash` | failed | termios |
| `test_repin.py` | `test_a_planted_temporary_name_link_is_not_followed` | failed | termios |
| `test_repin.py` | `test_a_failed_second_replace_names_what_was_replaced_and_restores_nothing` | failed | termios |
| `test_repin.py` | `test_an_extra_changed_path_after_the_write_refuses_and_prints_the_undo_line` | failed | termios |
| `test_repin.py` | `test_a_pin_that_adds_or_drops_a_baseline_key_refuses` | failed | termios |
| `test_repin.py` | `test_a_missing_or_duplicated_symbol_is_a_review_item_never_a_pin[missing]` | failed | _socket |
| `test_repin.py` | `test_a_missing_or_duplicated_symbol_is_a_review_item_never_a_pin[duplicate]` | failed | _socket |
| `test_repin.py` | `test_a_pin_owed_to_a_plain_change_packages` | failed | _socket |
| `test_repin.py` | `test_a_closure_member_change_refuses_an_ast_pin` | failed | _socket |
| `test_repin.py` | `test_two_trees_that_differ_only_in_a_kept_record_give_different_digests` | failed | _socket |
| `test_repin.py` | `test_package_in_a_detached_checkout_gives_one_digest` | failed | _socket |
| `test_repin.py` | `test_the_known_new_file_is_named_as_a_frozen_gate_file_only_when_it_changes` | failed | _socket |
| `test_repin.py` | `test_package_writes_only_into_the_ceremony_folder` | failed | _socket |
| `test_repin.py` | `test_the_lockfile_adapter_does_not_import_candidate_code` | failed | _socket |
| `test_repin.py` | `test_a_stale_record_is_dropped_and_a_missing_verbatim_record_added` | failed | _socket |
| `test_repin.py` | `test_a_verbatim_record_over_a_file_that_differs_from_its_template_refuses` | failed | _socket |
| `test_repin.py` | `test_the_lockfile_is_written_with_the_other_outputs_and_its_header_is_kept` | failed | termios |
| `test_repin.py` | `test_a_failed_second_of_three_replaces_names_what_was_replaced` | failed | termios |
| `test_repin_ceremony.py` | `test_reviewed_layout_reaches_stage_one_without_signing` | failed | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_full_ceremony_signs_once_with_the_typed_passphrase` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_end_prints_both_ids_the_record_and_the_push_line_and_runs_no_push` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_launcher_digest_that_differs_from_the_pasted_one_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Do the two digests match-Yes]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Do the two digests match-y]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Do the two digests match-]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Do the two digests match-None]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Does Summary 2-Yes]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Does Summary 2-y]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Does Summary 2-]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_word_yes_counts_at_every_question[Does Summary 2-None]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_pipe_on_stdin_refuses_the_ceremony` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_unsigned_anchor_refuses_without_first_run` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_anchor_signed_outside_the_roster_refuses_even_under_first_run` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_signing_key_outside_the_roster_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_failing_validate_refuses_before_the_report` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_roster_that_differs_from_the_packets_row_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_launcher_template_that_drops_a_closure_line_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_reanchor_script_that_the_packet_does_not_name_refuses_before_any_call` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_package_rewritten_between_the_report_and_the_yes_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_edited_listed_file_refuses_and_names_the_by_hand_runbook` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_edited_repin_refuses_ceremony_without_first_run` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_shows_the_unsigned_base_line_with_both_ids_and_the_count` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_with_nothing_owed_says_so` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_reviewed_commit_that_is_not_an_ancestor_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_change_to_repin_or_either_test_file_after_review_refuses_first_run[release/repin.py]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_change_to_repin_or_either_test_file_after_review_refuses_first_run[tests/test_repin.py]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_change_to_repin_or_either_test_file_after_review_refuses_first_run[tests/test_repin_ceremony.py]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_refuses_when_the_anchor_already_pins_repin` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_refuses_an_owed_ast_pin` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_shows_a_lockfile_only_correction_but_leaves_it_for_the_ordinary_ceremony` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_first_run_with_an_ast_pin_and_a_lockfile_correction_still_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_ceremony_refuses_unreviewed_lockfile_correction` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_owed_ast_pin_is_written_the_stop_line_printed_and_a_rerun_proceeds` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_matching_pin_commit_and_a_range_with_no_pin_pass_the_rerun_check` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_pin_commit_followed_by_an_unrelated_commit_is_still_checked` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_commit_touching_the_baseline_with_no_record_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_commit_adding_one_more_path_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_commit_that_holds_other_bytes_than_the_ones_shown_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_commit_whose_parent_is_not_the_recorded_head_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_merge_commit_that_changes_the_baseline_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_loaded_key_refuses_before_stage_one` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_key_loaded_after_stage_one_refuses_before_stage_two` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_key_in_a_second_agent_reached_only_through_the_login_lookup_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_unencrypted_key_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_an_agent_that_cannot_be_asked_is_shown_not_refused` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_loaded_key_signs_with_no_prompt_which_is_why_it_is_refused` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_wrong_passphrase_signs_nothing` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_signer_environment_is_a_short_fixed_list` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_signing_tools_resolve_by_absolute_path` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_typed_passphrase_appears_nowhere_the_script_writes` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_note_is_printed_again_after_a_stage_two_failure` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_stage_one_has_no_terminal_and_the_probe_prompts_with_one` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_stage_two_without_a_terminal_cannot_sign` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_ceremony_help_lists_no_test_seam` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_committed_module_named_like_the_standard_library_does_not_run_in_a_ceremony[release]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_committed_module_named_like_the_standard_library_does_not_run_in_a_ceremony[tests]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_committed_module_named_like_the_standard_library_does_not_run_in_a_ceremony[.]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_checkpoint_verification_wants_a_good_signature_by_the_expected_key_from_the_pinned_roster` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_verification_after_stage_two_decides_whether_the_ceremony_is_done` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_stage_two_that_exits_cleanly_without_moving_the_anchor_is_not_done` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_stage_two_that_moves_the_anchor_to_a_commit_that_is_not_ahead_of_the_old_one_is_not_done[an unrelated commit]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_stage_two_that_moves_the_anchor_to_a_commit_that_is_not_ahead_of_the_old_one_is_not_done[an older commit]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_launcher_is_hashed_again_before_each_of_its_two_runs[one-Do the two digests match]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_launcher_is_hashed_again_before_each_of_its_two_runs[two-Does Summary 2]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_every_signing_child_gets_a_short_fixed_environment_and_a_fixed_path` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_launcher_that_is_not_the_packets_pair_refuses_before_any_call` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_package_hash_the_launcher_reports_differently_refuses_before_summary_two` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prior_scanner_disagreement_stops_before_signing` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_launcher_is_hashed_again_before_each_reading_command[--validate]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_launcher_is_hashed_again_before_each_reading_command[--hash-package]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_launcher_is_hashed_again_before_each_reading_command[--show-report]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_ceremony_that_names_a_copied_python_runs_to_the_end` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_values_file_and_the_python_are_hashed_again_before_each_of_the_two_runs[one-Do the two digests match-values file]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_values_file_and_the_python_are_hashed_again_before_each_of_the_two_runs[one-Do the two digests match-python]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_values_file_and_the_python_are_hashed_again_before_each_of_the_two_runs[two-Does Summary 2-values file]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_values_file_and_the_python_are_hashed_again_before_each_of_the_two_runs[two-Does Summary 2-python]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_only_the_exact_word_yes_writes_the_ast_pin_through_the_command` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_packet_writes_the_same_bytes_as_the_test_helper_on_the_same_tree` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_packet_refuses_a_ceremony_that_changes_an_authority_file_and_writes_nothing` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_packet_refuses_a_folder_that_already_holds_one_and_changes_nothing` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_launcher_one_byte_off_the_anchors_template_refuses_before_any_child_runs` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_ceremony_with_no_record_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_that_names_another_commit_than_the_one_below_it_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_with_another_commit_on_top_of_it_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_commit_that_changes_another_path_refuses` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_that_names_other_digests_refuses[packet-damage0]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_that_names_other_digests_refuses[launcher-damage1]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_record_that_names_other_digests_refuses[a member-damage2]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_shows_the_reviewed_tools_and_package` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_the_page_command_that_scans_ignores_what_the_environment_and_the_home_folder_would_load` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_candidate_checker_that_hides_the_scan_cannot_change_what_the_page_prints` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_replace_entry_or_a_filter_in_the_repository_cannot_change_the_checker_the_page_runs` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_replace_entry_cannot_hide_an_unread_commit_from_the_record_checks` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_deletion_renamed_into_the_record_is_listed_by_the_record_check` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_replace_entry_cannot_make_a_tampered_launcher_equal_the_reviewed_template` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[packet]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[member]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[extra path]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[wrong parent]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[template]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_refuses_damaged_reader_bindings[launcher byte]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_starts_launcher_without_inherited_hostile_environment` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_git_ignores_git_environment_redirect` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_repository_configuration_cannot_make_the_verify_command_say_good` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_signature_program_named_in_the_repository_cannot_make_the_verify_command_say_good[gpg.program-PGP SIGNATURE]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_signature_program_named_in_the_repository_cannot_make_the_verify_command_say_good[gpg.openpgp.program-PGP SIGNATURE]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_signature_program_named_in_the_repository_cannot_make_the_verify_command_say_good[gpg.x509.program-SIGNED MESSAGE]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_checkpoint_verifier_accepts_only_the_expected_roster_key` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_driver_git_ignores_a_repository_configured_pager` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_record_check_uses_committed_objects_after_worktree_rewrite` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_inherited_child_marker_does_not_bypass_record_check_isolation` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepare_and_run_verifier_binds_signed_prior_to_raw_candidate` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prior_verifier_refuses_wrong_independent_fingerprint_before_collection` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prior_tool_or_observer_tamper_refuses_before_key_confirmation[prior/tests/_gate_manifest.py-prior verifier evidence changed at]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prior_tool_or_observer_tamper_refuses_before_key_confirmation[verifier-observer.py-collection observer differs from the reviewed preparation code]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_candidate_tamper_refuses_before_key_confirmation` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_hold_dispositions_bind_every_exact_item_to_the_report` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_verifier_binds_added_collection_nodes_as_ordinary_notes` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_verifier_binds_new_skip_marker_as_a_hold` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[ignored]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[dependency]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[target]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[symlink_parent]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[gitlink]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepared_verifier_refuses_untrusted_evidence_before_collection[python]` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_transition_packet_uses_signed_prior_authority_and_preserves_ordinary_refusal` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_a_transition_packet_drives_both_stages_against_a_disposable_signed_anchor` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_documented_verifier_then_ceremony_on_disposable_authority` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_prepare_values_writes_fresh_reviewable_inputs_without_overwriting` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_reader_inputs_bind_candidate_packet_and_prior_template_without_claiming_review` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_reviewed_ast_transaction_requires_record_before_write_and_stops` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_ceremony_refuses_unreviewed_ast_write` | setup error | ssh-keygen |
| `test_repin_ceremony.py` | `test_reviewed_symbol_deletion_is_exactly_named_recorded_and_written` | setup error | ssh-keygen |
| `test_reanchor_driver_disclosures.py` | `TestThePrintedCommandsAreTheOnesThatWork::test_each_printed_launcher_form_is_accepted_by_the_real_launcher` | failed | not classified |

## Appendix B: the 96 sweeps failures of the first run

Reason in the first run (as printed or inferred as stated in (f)), then the outcome in the run with `SYSTEMROOT` added. `preflight stop` is the Windows workspace refusal or a bare `preflight` leg.

| Test (in `tests/test_portable_security_sweeps.py`) | First-run reason | With `SYSTEMROOT` |
|---|---|---|
| `test_absent_git_is_incomplete_for_the_history_leg` | other | failed (other) |
| `test_a_repo_local_executable_is_refused` | adapter not found | failed (adapter not found) |
| `test_a_repo_local_symlink_to_an_outside_binary_is_refused` | adapter not found | failed (adapter not found) |
| `test_a_symlink_resolving_into_the_repo_is_refused` | adapter not found | failed (adapter not found) |
| `test_a_package_manager_symlink_outside_the_repo_is_accepted_and_both_paths_recorded` | other | failed (other) |
| `test_a_version_command_failure_is_degraded_not_incomplete` | adapter not found | failed (adapter not found) |
| `test_path_drift_between_validation_and_invocation_is_degraded` | adapter not found | failed (adapter not found) |
| `test_probe_version_is_guarded_by_revalidation` | adapter not found | failed (adapter not found) |
| `test_the_commit_reachability_probes_git_call_is_guarded_by_revalidation` | adapter not found | failed (adapter not found) |
| `test_reduced_mode_child_path_is_an_empty_off_tree_directory` | adapter not found | failed (adapter not found) |
| `test_full_mode_child_path_contains_only_the_verified_git_directory` | adapter not found | failed (adapter not found) |
| `test_the_adapter_config_flag_is_sent_and_a_candidate_toml_is_never_read` | fake never invoked | failed (fake never invoked) |
| `test_both_gitleaks_config_env_vars_are_dropped` | other | failed (other) |
| `test_the_ignore_gitleaks_allow_flag_is_sent` | fake never invoked | failed (fake never invoked) |
| `test_a_candidate_gitleaksignore_refuses_before_execution[regular file]` | preflight stop | passed |
| `test_a_candidate_gitleaksignore_refuses_before_execution[symlink]` | preflight stop | passed |
| `test_a_candidate_gitleaksignore_refuses_before_execution[nested]` | preflight stop | passed |
| `test_the_history_leg_argv_carries_text_no_textconv_and_no_ext_diff` | preflight stop | failed (other) |
| `test_hostile_repo_local_config_loses_to_the_counted_keys` | other | failed (other) |
| `test_every_inherited_git_variable_is_dropped` | other | failed (other) |
| `test_the_current_tree_leg_argv_disables_symlink_following` | fake never invoked | failed (fake never invoked) |
| `test_the_current_tree_leg_argv_adds_no_gitignore_filter` | fake never invoked | failed (fake never invoked) |
| `test_policy_fingerprints_reach_an_off_tree_ignore_file_only` | fake never invoked | failed (fake never invoked) |
| `test_the_gitleaks_timeout_is_strictly_inside_the_outer_deadline` | fake never invoked | failed (fake never invoked) |
| `test_the_adapter_timeout_is_sent_as_integer_seconds` | fake never invoked | failed (fake never invoked) |
| `test_a_flag_the_subcommand_does_not_declare_is_rejected_by_the_fake` | other | failed (other) |
| `test_the_admission_matrix_argv_is_accepted_by_the_flag_table` | WinError 10106 | failed (adapter not found) |
| `test_an_unlisted_hostile_local_config_key_refuses_before_execution` | preflight stop | passed |
| `test_an_include_path_injection_refuses` | preflight stop | passed |
| `test_the_screen_expands_includes` | other | failed (other) |
| `test_a_config_origin_outside_the_git_directory_refuses` | preflight stop | passed |
| `test_the_screen_accepts_an_ordinary_repository` | preflight stop | failed (other) |
| `test_a_dotted_branch_subsection_is_inert[dotted]` | preflight stop | failed (other) |
| `test_a_dotted_branch_subsection_is_inert[slashed]` | preflight stop | failed (other) |
| `test_a_dotted_branch_subsection_is_inert[vscode-merge-base]` | preflight stop | failed (other) |
| `test_a_dotted_remote_subsection_is_inert[dotted]` | preflight stop | passed |
| `test_a_dotted_remote_subsection_is_inert[glab-resolved]` | preflight stop | passed |
| `test_every_non_inert_key_is_named_in_one_refusal` | preflight stop | passed |
| `test_the_refusal_names_no_more_keys_than_the_cap` | preflight stop | passed |
| `test_the_refusal_states_how_many_keys_it_elided` | preflight stop | passed |
| `test_an_include_origin_outside_the_git_dir_refuses_immediately` | preflight stop | failed (other) |
| `test_a_linked_worktrees_ordinary_local_config_is_accepted` | preflight stop | failed (other) |
| `test_the_config_screens_second_git_call_is_guarded_by_revalidation` | adapter not found | failed (adapter not found) |
| `test_a_hostile_path_string_cannot_forge_a_report_line` | other | failed (other) |
| `test_bidi_and_nul_in_a_result_field_render_escaped` | other | failed (other) |
| `test_no_secret_bearing_field_reaches_any_sink` | preflight stop | failed (other) |
| `test_an_unknown_result_shape_is_degraded_not_clean[not json at all-not valid JSON]` | preflight stop | failed (other) |
| `test_an_unknown_result_shape_is_degraded_not_clean[{"results": []}-not a result list]` | preflight stop | failed (other) |
| `test_an_unknown_result_shape_is_degraded_not_clean[[{"RuleID": "x"}]-no string 'File']` | preflight stop | failed (other) |
| `test_an_unknown_result_shape_is_degraded_not_clean[[{"RuleID": "x", "File": "y", "Fingerprint": "z", "StartLine": "4"}]-no integer 'StartLine']` | preflight stop | failed (other) |
| `test_an_unknown_result_shape_is_degraded_not_clean[["a string"]-is not an object]` | preflight stop | failed (other) |
| `test_invalid_utf8_in_a_report_is_degraded` | preflight stop | failed (other) |
| `test_missing_redaction_is_degraded` | preflight stop | failed (other) |
| `test_an_undocumented_exit_code_is_degraded` | preflight stop | failed (other) |
| `test_a_findings_exit_is_not_the_adapters_usage_error_exit` | fake never invoked | failed (fake never invoked) |
| `test_an_invalid_argv_refuses_with_the_argv_reason_not_a_missing_report` | WinError 10106 | failed (adapter not found) |
| `test_a_findings_exit_with_no_reported_finding_is_degraded` | preflight stop | failed (other) |
| `test_signal_death_is_degraded` | preflight stop | failed (other) |
| `test_a_finding_is_not_hidden_by_an_incomplete_history_leg` | preflight stop | failed (other) |
| `test_not_applicable_is_distinct_from_incomplete` | preflight stop | failed (other) |
| `test_a_detached_head_with_its_only_branch_deleted_still_scans_history` | preflight stop | failed (other) |
| `test_a_shallow_clone_cannot_claim_full_history_coverage` | preflight stop | failed (other) |
| `test_a_non_git_export_runs_the_current_tree_leg_and_reports_history_incomplete` | preflight stop | failed (other) |
| `test_reduced_mode_never_emits_clean[tool0-5]` | preflight stop | passed |
| `test_reduced_mode_never_emits_clean[tool1-10]` | preflight stop | failed (other) |
| `test_reduced_mode_never_emits_clean[tool2-20]` | preflight stop | failed (other) |
| `test_reduced_mode_never_emits_clean[tool3-20]` | preflight stop | failed (other) |
| `test_the_child_document_is_bounded_strict_utf8_json` | other | failed (other) |
| `test_a_digest_mismatch_is_degraded_without_execution` | preflight stop | failed (other) |
| `test_an_unadmitted_platform_is_reduced_not_degraded` | preflight stop | failed (other) |
| `test_a_digest_match_is_the_only_route_to_full_mode` | preflight stop | failed (other) |
| `test_the_evidence_record_keeps_the_raw_version_banner` | WinError 10106 | failed (adapter not found) |
| `test_the_evidence_record_carries_a_measured_exit_row_per_subcommand` | WinError 10106 | failed (adapter not found) |
| `test_the_adapters_real_redaction_shape_passes_and_discards_match_context` | WinError 10106 | failed (adapter not found) |
| `test_a_matrix_without_a_planted_finding_row_refuses_to_admit` | WinError 10106 | failed (adapter not found) |
| `test_verify_version_support_refuses_a_candidate_that_invokes_an_unaccounted_git_subcommand` | WinError 10106 | failed (adapter not found) |
| `test_verify_version_support_refuses_a_candidate_that_drops_a_required_option` | WinError 10106 | failed (adapter not found) |
| `test_verify_version_support_refuses_a_candidate_that_contacts_a_remote` | WinError 10106 | failed (adapter not found) |
| `test_verify_version_support_refuses_a_candidate_with_an_output_schema_drift` | WinError 10106 | failed (adapter not found) |
| `test_verify_version_support_cannot_mutate_the_source_version_set` | WinError 10106 | failed (adapter not found) |
| `test_the_emitted_record_states_that_an_unadmitted_binary_was_executed` | WinError 10106 | failed (adapter not found) |
| `test_the_human_report_opens_with_the_unadmitted_execution_statement` | WinError 10106 | failed (adapter not found) |
| `test_reduced_mode_is_reachable_without_any_source_change` | preflight stop | failed (other) |
| `test_generated_git_shim_uses_bound_log_and_no_contact_url_forms` | preflight stop | failed (preflight stop) |
| `test_production_records_the_selected_git_version_read` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[git-config-hangs]` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[git-config-output-over-the-cap]` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[git-common-dir-empty]` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[git-common-dir-two-lines]` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[git-common-dir-relative]` | other | failed (other) |
| `test_hung_or_oversized_adapter_or_git_output_is_never_clean[control-adapter-answers]` | other | passed |
| `test_a_helper_planted_in_the_scanned_tree_never_runs` | other | failed (other) |
| `test_private_triage_record_isolates_findings_from_public_outputs` | adapter not found | failed (adapter not found) |
| `test_exit_zero_with_reported_findings_is_degraded` | preflight stop | failed (other) |
| `test_missing_match_redaction_marker_is_degraded` | preflight stop | failed (other) |
| `test_shallow_linked_worktree_marks_history_incomplete` | other | failed (other) |
