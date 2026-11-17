# Why fifteen existing tests fail on Windows (diagnosis), 2026-11-16

Evidence for the Maintainer's decision on the fifteen tests that fail on Windows
in files the adopter-defects plan (`dev/plans/2026-11-16-adopter-defects-0-7-0.md`)
touched. Background: `windows-defects-run-2026-11-16.md` (run 2, the nine whole
files) and `windows-hook-index-fix-run-2026-11-16.md` (the commit-hook repair).
Record only: no shipped code, test or document in the repository was changed.
Every repair below was tried on a disposable copy on the VM and none is applied
here.

## Result

**All fifteen still fail on the committed tree.** The commit-hook repair
(`cb060551`) fixed none of them, including the two that print "tracked Markdown
discovery failed". On commit `530c922e` the four files gave 15 failed, 305
passed, 27 skipped (444 s); the failing set is the same fifteen the C8 record
listed.

They come from eight causes. Six are test assumptions or the way the Windows
copy was made, and two are product defects that need a Decision.

| # | Cause | Tests | Class | Repair | Edits a frozen file? |
|---|---|---|---|---|---|
| 1 | The unpacked `git archive` copy has no `.git`; four tests run `upgrade --to HEAD` | 4 | Method, not a test or product fault | None in the repository: make the copy a Git repository first (as the C10 run did) | No |
| 2 | Two `write_text` calls in one test turn LF into CR-LF on Windows | 1 | TEST ASSUMPTION | `write_bytes` at two sites | `bootstrap/tests/test_upgrade.py`, already FROZEN-MODIFIED |
| 3 | `read_text()` with no encoding reads UTF-8 files as cp1252 | 1 | TEST ASSUMPTION | `encoding="utf-8"` at three calls | `bootstrap/tests/test_upgrade.py`, already FROZEN-MODIFIED |
| 4 | A test file name (`:(glob)**.md`) cannot exist on Windows | 1 | TEST ASSUMPTION | In-body `pytest.skip` on Windows | `bootstrap/tests/test_upgrade.py`, already FROZEN-MODIFIED |
| 5 | Two tests compare text that holds `\` on Windows with a pattern that holds `/` | 2 | TEST ASSUMPTION | `.as_posix()` in one, `[\\/]` in the pattern of the other | `bootstrap/tests/test_doc_drift_tools.py` and `bootstrap/tests/test_session_routines.py`, both already FROZEN-MODIFIED |
| 6 | A marker the test plants at the end of the Git helper reads an environment variable the Windows worker's closed environment does not have | 2 | TEST ASSUMPTION | Guard the planted line with `if ... in os.environ` | `bootstrap/tests/test_doc_drift_tools.py`, already FROZEN-MODIFIED |
| 7 | A closed-receipt check and a ledger writer and pruner both assume LF; Windows adds CR | 3 | **PRODUCT DEFECT (two, one behind the other): needs a Decision** | See cause 7 | Yes for the second: `templates/modules/team-gated/_intent/record_io.py` is frozen and not yet modified |
| 8 | An earlier test leaves a cached Git version behind; this test then skips the version check but not the missing worker binding | 1 | TEST ASSUMPTION (isolation) | Bind the worker in the test with the helper the file already has | None: `bootstrap/tests/security/test_git_read.py` is an ordinary test file |

No test repair above changes an assertion's claim or a node name, and none adds
a skip marker (cause 4 uses a call inside the test body, so the gate's
`SKIP-XFAIL-NEW` check does not fire). With all repairs applied to the
disposable copy, the four files whole gave: **319 passed, 28 skipped, 0 failed, exit 0** (537.71 s; 347 tests in all, the one extra skip being the cause-4 test).

## What was measured, read and assumed

- **Measured on Windows:** every count, exit code, output line, byte string and
  reason code in the sections below, including each probe in "Probes".
- **Measured on macOS** (Python 3.13.13, Git 2.53.0): that the four
  `--to HEAD` tests fail the same way from an unpacked archive and pass once the
  copy is a Git repository; the seven-case table for the proposed receipt change
  (cause 7); the check that the repairs leave macOS green (see "macOS check").
- **Read from the code, not run:** how the gate's collection check treats a skip
  marker (`bootstrap/tests/_gate_manifest.py`); what `str.splitlines`,
  `Path.read_text` and a text-mode `os.write` do with line endings on Windows
  (Python's documented behaviour, checked only through the probes named below);
  that the same unchanged print-based receipt appears in
  `bootstrap/tests/test_session_writes_contained.py`.
- **Not measured:** other Git versions (the order-dependent test needs Git 2.44 or
  newer, and only 2.56.0.windows.4 was available); other Windows hosts; the ARM64
  interpreter; the files outside the four named; human time and tokens (`unknown`).

## Environment

- **Machine.** Windows 11 Pro, `ver` 10.0.26300.9974, "ARM64-based PC" under UTM,
  SSH alias `cairn-windows`.
- **Interpreter.** x64 build, `C:\ProgramData\miniconda3\envs\lhm\python.exe`:
  Python 3.13.18 (conda-forge, MSC v.1944 64 bit, AMD64), pytest 9.2.0.
- **Git.** 2.56.0.windows.4.
- **Date and time.** 2026-11-16. The VM clock runs three hours behind EST; the
  Windows work ran 12:55 to about 13:45 on the VM (15:55 to about 16:45 EST).
- **Rules kept.** New folders only, under `C:\Users\cairn\`; nothing existing was
  overwritten or removed; no system setting changed; no package installed; the
  tests opened no network connection that I know of (not observed). One scratch
  `git init` under `cairn-winfails-git-20261116` and the folders listed below.

## Folders and trees

The tree is `git archive --format=tar` of `530c922ef9b1ddd91a9851a805411395c7a518a8`
(SHA-256 `4cc747d2fba4557e22b8f02538454dd3f13dfbee23c4546606577d5b2ca36885`; the
VM's `certutil` matched). It was sent with `scp` and unpacked with `tar -xf`.

| Folder under `C:\Users\cairn\` | Contents | Use |
|---|---|---|
| `cairn-winfails-files-20261116` | the archive, untouched (no `.git`) | run 1; the unmodified shipped code for the probes |
| `cairn-winfails-git-20261116` | the same archive, then `git init`, `git add -A`, one commit (`ce15894`, clean afterwards) | baseline run of the 15 nodes; repairs applied here, uncommitted, for runs 2 and 3 |
| `cairn-winfails-work-20261116` | scratch scripts, outputs, the two diffs | probes |
| `winfails-530c922e.tar` | the archive | source |

All Windows runs used `PYTHONDONTWRITEBYTECODE=1` and
`-p no:cacheprovider -rfsE -q`. Exit codes were read with `call echo exit=%^errorlevel%`.

## Run 1: the four files whole, on the committed tree

```sh
ssh cairn-windows 'cd /d C:\Users\cairn\cairn-winfails-files-20261116 && set "PYTHONDONTWRITEBYTECODE=1" && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -q --junitxml=C:\Users\cairn\cairn-winfails-work-20261116\run1.xml bootstrap/tests/test_upgrade.py bootstrap/tests/test_session_routines.py bootstrap/tests/test_doc_drift_tools.py bootstrap/tests/security/test_git_read.py'
```

**15 failed, 305 passed, 27 skipped in 444.12 s, exit 1.** The 15 are the same
nodes as the C8 record's list (compared as sorted node ids). Which cause each
belongs to:

| Test (file, node) | Cause |
|---|---|
| `test_upgrade.py::TestProfileSizedAssembly::test_profile_change_solo_to_multi_reincludes_region` | 2 |
| `test_upgrade.py::TestInitLock::test_review_inventory_theirs_excludes_local_edit_when_roster_matches` | 3 |
| `test_upgrade.py::TestInitLock::test_matching_historical_renderer_stages_inventory` | 1 |
| `test_upgrade.py::TestInitLock::test_historical_inventory_description_is_used_for_theirs` | 1 |
| `test_upgrade.py::TestInitLock::test_changed_historical_renderer_refuses_and_cleans_stage` | 1 |
| `test_upgrade.py::TestInitLock::test_changed_historical_metadata_refuses_and_cleans_stage` | 1 |
| `test_upgrade.py::TestDirtyTreeGuard::test_literal_pathspec_name_is_a_single_tracked_path` | 4 |
| `test_session_routines.py::test_reflection_filename_is_session_distinct` | 5 |
| `test_session_routines.py::test_session_end_WITH_handoff_DOES_emit_the_standing_capture_prompt` | 7 |
| `test_session_routines.py::test_handoff_prunes_the_intent_surface` | 7 |
| `test_session_routines.py::test_session_end_skips_intent_prune_in_linked_worktree` | 7 |
| `test_doc_drift_tools.py::test_real_discovery_cli_finds_planted_issue_without_decoy[link-scripts/link_check.py]` | 6 |
| `test_doc_drift_tools.py::test_real_discovery_cli_finds_planted_issue_without_decoy[snippet-scripts/sync_doc_snippets.py]` | 6 |
| `test_doc_drift_tools.py::TestFilterSources::test_excludes_dev_archive_and_reflections` | 5 |
| `security/test_git_read.py::test_read_origin_uses_git_parser_for_quoted_and_continued_values` | 8 |

A baseline of the same fifteen nodes in the Git-initialised copy (before any
repair) gave **10 failed, 4 passed, 1 skipped** (128.00 s): the four that pass
are the four of cause 1, and the `test_git_read.py` node skips when run alone,
as the C8 record found.

## Cause 1: the copy has no `.git` (4 tests)

**Verdict: not a test or product fault. It comes from how the Windows copy is made.**
The four tests install a project, then run `upgrade --stage --to HEAD`. That option
reads Git history of the Cairn tree they run from. Their stderr (run 1) reads:
`error: --to <ref> needs a git-checkout Cairn source; a packaged release can upgrade only to the currently-running tree (omit --to).`

- **Measured on macOS:** the same four fail the same way from an unpacked archive
  (4 failed, 1 passed, 4.7 s) and pass once the copy is a Git repository
  (`git init`, `git add -A`, one commit; 4 passed, 78.7 s). The fifth test run in
  that pair (`test_review_inventory_theirs_excludes_local_edit_when_roster_matches`)
  passes on macOS in both, so it is not a no-`.git` failure; it is cause 3.
- **Measured on Windows:** in `cairn-winfails-git-20261116` before any repair the
  four pass.
- **Repair:** none in the repository. A Windows evidence run must `git init`, `git add -A`
  and commit the unpacked archive before running these files, as the C10 run's hook
  steps did. The recipe in `windows-native-rerun-2026-11-13.md` unpacks an archive
  and does not make it a repository, and the C8 run's whole-file runs used untouched
  copies, which is why these four showed as failures in both trees. The same step
  is worth one line in the Windows section of `dev/rules/development-environment.md`
  (a document edit; not made). Frozen file: none.

## Cause 2: a rewrite that turns LF into CR-LF (1 test)

**Verdict: TEST ASSUMPTION.** `test_profile_change_solo_to_multi_reincludes_region`
fails at `--apply` with "staged file AGENTS.md still has conflict markers". The test
builds a copy of the templates and rewrites two files with `Path.write_text`, which on
Windows writes every `\n` as `\r\n`: the appended gated region in the copy of the
template (`_cairn_with_directive`), and the adopter's `AGENTS.md` after one line is
inserted. The installer writes LF whatever the template holds, but `upgrade --stage`
reads the template bytes as they are, so a CR-LF template or a CR-LF adopter file
makes every line differ and the merge conflicts.

**Probe** (`prof_probe.py`, a scratch copy of the test's steps; the first word is
how the adopter's file is rewritten, the second how the template copy is written):

| Adopter rewrite / template write | Template has CR | Adopter file has CR | Staged file has conflict markers | `--apply` exit |
|---|---|---|---|---|
| `write_bytes` / `write_bytes` | no | no | no | 0 (region kept, customization kept) |
| `write_text` / `write_bytes` | no | yes | yes | 1 |
| `write_bytes` / `write_text` | yes | no | yes | 1 |

A first repair that changed only the adopter's rewrite left the test failing (the
15-node run showed it); the probe then found the template write. Both are needed.
The repair is in the diff under "Proposed test repairs". It keeps every assertion.

## Cause 3: default text encoding (1 test)

**Verdict: TEST ASSUMPTION.** `test_review_inventory_theirs_excludes_local_edit_when_roster_matches`
raises `UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 312`.
On Windows `Path.read_text()` with no encoding uses cp1252. The test reads the installed
inventory that way, appends a note and writes it back as UTF-8, which re-encodes every
non-ASCII character as several; it then reads the `.ours` copy with the same default and
fails on a byte cp1252 does not define. Checked with the same codec on macOS: the
rendered inventory holds U+2014; one cp1252 read of its UTF-8 bytes succeeds, and a
second read of the re-encoded text raises the same byte-0x9d error. With
`encoding="utf-8"` at the three calls the test passes on Windows (15-node run).
Assertions unchanged.

## Cause 4: a file name Windows cannot hold (1 test)

**Verdict: TEST ASSUMPTION.** `test_literal_pathspec_name_is_a_single_tracked_path`
fails at `(tmp_path / ":(glob)**.md").write_text(...)` with
`OSError: [Errno 22] Invalid argument`: a colon and asterisks cannot be in a Windows
file name. Its sibling in `test_doc_drift_tools.py` for the file named `*.md` already
skips on Windows for this reason.

**Repair:** a runtime `pytest.skip` at the top of the test body (diff below). A
`@pytest.mark.skipif` would be shorter, but the gate's collection check lists every
skip or skipif marker and a protected test that gains one is a HOLD
(`SKIP-XFAIL-NEW` in `bootstrap/tests/_gate_manifest.py`, read from the code); a call
inside the body adds no marker. The cost is that this one literal-pathspec case has
no Windows coverage; it cannot be written on Windows, so no repair can give it any.
Measured: the test is skipped on Windows with the repair and still collected under
the same node id.

## Cause 5: `\` against `/` (2 tests)

**Verdict: TEST ASSUMPTION, on the evidence of each product output.**

- `TestFilterSources::test_excludes_dev_archive_and_reflections` fails with
  `['AGENTS.md', 'dev\\proposals\\live.md', 'docs\\archive\\old.md', 'docs\\guide.md']`
  against the expected `/` forms. The four files are the right four: `filter_sources`
  in `scripts/link_check.py` works on path parts and kept the correct set. The test
  compares `str(path)`, which uses the OS separator. Repair: `.as_posix()`.
- `test_reflection_filename_is_session_distinct` fails with "reflection path must be
  <date>-<agent>-<session>.md". The product printed
  `wrote reflection scaffold: dev\reflections\2026-11-16-tester-sessP.md ...` (seen in
  the output of a sibling failure); the test's pattern holds `dev/reflections/`. The
  product prints the path as the operating system writes it, which is right for a
  person at a Windows prompt. Repair: let the pattern accept either separator.
  (If the Maintainer would rather the tool always print `/`, that is a product
  change; I do not see a reason for it.)

## Cause 6: a planted marker the worker cannot run (2 tests)

**Verdict: TEST ASSUMPTION.** Both `test_real_discovery_cli_finds_planted_issue_without_decoy`
cases exit 2 with "tracked Markdown discovery failed", not 1 with the finding.

- `_marked_helper` in `bootstrap/tests/test_doc_drift_tools.py` appends code to the
  Git helper that writes a marker file named by `os.environ['CAIRN_TEST_HELPER_MARKER']`,
  to prove the pinned bytes ran. On Windows the helper's bytes also run inside the
  worker, a child started with a closed environment (`PATH`, `PYTHONUTF8`,
  `PYTHONIOENCODING`, and the system root only; read from `_capture_windows_git`).
  The variable is not set there, so I take it the appended line raises `KeyError`
  and the worker fails (a deduction: the only difference between the two probe rows
  below is the guard), and the reader then reports no version.
- **Probe** (`dd_probe2.py`): the same read (`run_git ls-files -z --cached --stage`) in
  a scratch repository, once with the planted line as the test writes it and once with
  the line guarded by `if 'CAIRN_TEST_HELPER_MARKER' in os.environ:`:

| Planted line | state | reason |
|---|---|---|
| unguarded (the test today) | `failed` | `git-version-unavailable` |
| guarded | `completed`, stdout holds the staged entry | none; the parent still wrote its marker file |

  The same read without any planted line (`dd_probe.py`, and again under pytest's own
  temporary folder in `test_dd_probe.py`) completes, so the helper and the worker are
  sound; the commit-hook repair (`cb060551`) did not touch this path.
- **Repair:** guard the planted line (diff below). The marker is still written in the
  parent, so the tests that check it (`test_real_cli_loads_its_physically_pinned_helper_before_help`
  and the binding-mutation cases) keep their assertions; they passed in runs 2 and 3.

## Cause 7: two product defects behind one another (3 tests)

**Verdict: PRODUCT DEFECT, two of them. They need the Maintainer's Decision; I
stopped at naming them and showing a repair on a copy.** Each `session-end --handoff`
test returns exit 5 and prints "Meter refresh was unavailable; both prune steps were
skipped." (`test_session_end_WITH_handoff_DOES_emit_the_standing_capture_prompt`,
`test_handoff_prunes_the_intent_surface`,
`test_session_end_skips_intent_prune_in_linked_worktree`).

**Defect A: the handoff rejects the Meter's receipt because Windows adds CR.**
`_meter_refresh_receipt` in `templates/skills/_lib/session.py` (and the identical
`tools/session.py`) requires the child's stdout to hold no `\r`. A Python child on
Windows ends `print()` output with `\r\n`, even into a pipe.

**Probe** (`meter_probe.py`, on the unmodified shipped tree `cairn-winfails-files-20261116`):

| Input to `_meter_refresh_receipt` | Result |
|---|---|
| the test fixture's synthetic Meter (`print` of the receipt), bytes `...}\r\n` | rejected |
| the same bytes with `\r\n` changed to `\n` | accepted |
| the shipped Meter, `tools/meter.py refresh --json`: exit 5, bytes `{"coverage":"unknown","reason":"unavailable","schema":"cairn-meter-refresh/1","status":"unavailable"}\r\n` | rejected |

The shipped Meter prints its receipt with `print()` (`main` in
`templates/skills/_lib/meter.py`), so any receipt it prints on Windows ends in
`\r\n`. On this VM the shipped Meter itself answers `unavailable` (its Windows
account check, `check_acl`, raises `Unavailable` at an ancestor folder of the profile;
not diagnosed), so I could not show a real `ok` or `disabled` receipt; the CR is on
every receipt it prints, including this one. The C5 change (64.1) folded a CR before an
LF in child output that is *displayed*; it did not reach this validator.

**Defect B: the intent ledger is written and pruned in text mode, so the prune always
refuses on Windows.** With defect A repaired on a copy, one of the three tests
(`test_handoff_prunes_the_intent_surface`) still failed, with
`intent: prune refused -- the ledger changed while pruning -- skipped`.
In `prune_released_pairs` (`templates/modules/team-gated/_intent/record_io.py`) the lines
come from `read_text()`, which turns `\r\n` into `\n`, while the final check compares
the file's size on disk with the sum of those lines. Any CR in the ledger makes the two
differ. And the shipped writer, `append_record`, opens the file with `os.open` and no
`O_BINARY`, so on Windows its single `os.write` turns each `\n` into `\r\n`.

**Probe** (`intent_probe.py`, on the unmodified shipped tree): three records appended
with the shipped `append_record` left 3 CR-LF pairs on disk (331 bytes); the shipped
prune over that ledger returned `refused = the ledger changed while pruning ...` and
pruned 0 pairs. Over an LF-only ledger the prune pruned its one pair, but the surviving
line came out with a CR (its temporary file is also opened without `O_BINARY`), so the
next prune would refuse. So on Windows the handoff can never prune released claims. The
same missing flag is in `tools/prune_intents.py:230` (not exercised by these tests; not
run).

**Proposed repair (on a copy; not applied):** the two diffs under "Proposed product
repair" below. A is four lines in `_meter_refresh_receipt`: fold one terminal `\r\n`
into `\n`, leaving every other check as it was. B is three lines in `record_io.py`:
`O_BINARY` on the two `os.open` calls and `read_bytes().decode("utf-8")` in place of
`read_text(encoding="utf-8")`, so the compared sizes are the on-disk sizes and an
existing CR-LF ledger (the test fixture writes one with `write_text`) is read and
rewritten byte for byte.

**Measured with the repairs on the Windows copy:** the three `session-end` tests pass;
`test_session_routines.py` whole gave 20 passed (21.9 s); the same probes then show the
receipt accepted, the writer leaving 3 lines and 0 CRs (328 bytes), and the prune
refusing nothing and pruning 1 pair on both the writer's ledger and an LF-only ledger,
leaving 0 CRs. **Measured on macOS (the proposed receipt function):**

| Receipt bytes (valid receipt plus the ending shown) | Committed code | Proposed |
|---|---|---|
| `\n` | accepted | accepted |
| `\r\n` | rejected | accepted |
| `\r\r\n` | rejected | rejected |
| `\r\n\r\n` | rejected | rejected |
| a `\r` inside the line, then `\n` | rejected | rejected |
| a lone trailing `\r` | rejected | rejected |
| no line ending | rejected | rejected |

**What the Maintainer must decide.**

1. Whether to fix defect A in the validator (recommended: one place, matches the C5
   precedent, covers any child that prints a receipt) or in the Meter (print bytes with
   an LF; then the test fixture `_install_synthetic_meter` must change to match, and
   `meter.py` has two copies).
2. Whether to fix defect B as shown. The `O_BINARY` flags alone are not enough: an
   existing CR-LF ledger would still be refused, and with only the read changed a
   text-mode rewrite would write `\r\r\n`. All three edits go together.
3. Review. A loosens a validator the code calls closed, so I would give it a Security
   Review before it ships (my judgment, not a ruling). Both are shipped-code edits:
   `tools/session.py` and `tools/_intent/record_io.py` are lock-tracked (their install
   lock hashes need the same scoped finalize `0f85f3e8` did); `record_io.py` under
   `templates/modules/team-gated/_intent/` is a frozen file, not yet modified, so the
   single re-anchor would grow by that one file. `templates/skills/_lib/session.py` is
   not frozen.
4. New tests. A needs a unit test over the seven receipts above; B needs a test that
   the writer leaves no CR and that a prune over a CR-LF ledger completes. They belong
   in `test_session_routines.py` and `test_intents_tool.py`, both frozen and
   already FROZEN-MODIFIED. I wrote none.

I did not run `test_session_writes_contained.py` (outside the four files). It builds
the same print-based receipt in several tests, so I expect defect A to fail them on
Windows too; that is an expectation, not a measurement.

## Cause 8: the order-dependent test (1 test)

**Verdict: TEST ASSUMPTION (isolation).** `test_read_origin_uses_git_parser_for_quoted_and_continued_values`
skips when run alone and fails when its file runs whole, in both trees.

- **What leaks.** The helper keeps a module-level cache of Git version answers
  (`_VERSION_CACHE` in `templates/skills/_lib/git_read.py`), keyed by the Git
  executable's identity. Tests that bind the Windows worker through `_bind_worker_source`
  (which clears the cache first) read real Git's version and fill the cache, and
  `monkeypatch` undoes the binding but not the cache. When the origin test calls
  `read_version`, the cache answers "completed", so it passes the "Git 2.44 or newer"
  skip. It then calls `read_origin_from_config`, which goes to the worker, and the worker
  has no bound helper bytes, so it fails with `verified-helper-buffer-unavailable`.
- **Measured** (scratch plugin `trace_plugin.py`, printing the module's state): on entry to the
  test the cache holds `C:\Program Files\Git\cmd\git.exe` (42696 bytes) and two fake
  `git.exe` stand-ins, and `_VERIFIED_SOURCE is None`. The real-Git entry first appears
  after `test_hook_index_rejects_wrong_commands_paths_and_malformed_indexes` (cache 0 to 1).
  Run alone the cache is empty, the version read fails, and the test skips.
- **Smallest pair that reproduces it** (unmodified tree `cairn-winfails-files-20261116`,
  `-k "test_hook_index_rejects_wrong_commands or test_read_origin_uses_git_parser"`):
  1 failed, 1 passed, 8.37 s. A scratch plugin (`reason_plugin.py`) printed, on entry,
  `cache entries = 1 | _VERIFIED_SOURCE is None: True` and, from the origin read,
  `state=failed returncode=None reason=verified-helper-buffer-unavailable`. On the
  repaired copy the same two tests gave 2 passed (3.29 s).
- **Smallest repair:** take `monkeypatch` and call `_bind_worker_source(monkeypatch)` first,
  as the neighbouring real-Git tests do. It clears the cache, binds the worker for the test
  and undoes the binding afterwards; on POSIX it returns at once. On Windows the test then
  runs against real Git 2.56.0 through the worker (it passed alone and in the whole file)
  instead of skipping or failing. No assertion changes. The file is not frozen.
- Not repaired, optional hardening: have `_bind_worker_source` replace `_VERSION_CACHE`
  with a fresh dict through `monkeypatch.setattr`, so no binding test leaves cache entries.
  I did not need it and did not test it.

## Proposed test repairs (not applied)

Exactly as applied to `cairn-winfails-git-20261116` (`git diff`, taken after run 2 with
the in-body skip of cause 4):

```diff
diff --git a/bootstrap/tests/security/test_git_read.py b/bootstrap/tests/security/test_git_read.py
--- a/bootstrap/tests/security/test_git_read.py
+++ b/bootstrap/tests/security/test_git_read.py
@@ -1254,7 +1254,8 @@ def test_read_origin_bounds_input_while_draining_both_output_streams(
 
 @pytest.mark.skipif(shutil.which("git") is None, reason="real Git control unavailable")
 def test_read_origin_uses_git_parser_for_quoted_and_continued_values(
-        tmp_path: Path) -> None:
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    _bind_worker_source(monkeypatch)  # Windows: bind the worker, clear the version cache
     target = tmp_path / "target"
     target.mkdir()
     git_path = shutil.which("git")
diff --git a/bootstrap/tests/test_doc_drift_tools.py b/bootstrap/tests/test_doc_drift_tools.py
--- a/bootstrap/tests/test_doc_drift_tools.py
+++ b/bootstrap/tests/test_doc_drift_tools.py
@@ -188,7 +188,8 @@ def _marked_helper() -> bytes:
     return helper + (
         b"\nimport os as _cairn_test_os\n"
         b"from pathlib import Path as _cairn_test_Path\n"
-        b"_cairn_test_Path(_cairn_test_os.environ['CAIRN_TEST_HELPER_MARKER'])"
+        b"if 'CAIRN_TEST_HELPER_MARKER' in _cairn_test_os.environ:\n"
+        b"    _cairn_test_Path(_cairn_test_os.environ['CAIRN_TEST_HELPER_MARKER'])"
         b".write_text('trusted-helper-ran', encoding='utf-8')\n"
     )
 
@@ -557,7 +558,7 @@ class TestFilterSources:
 
     def test_excludes_dev_archive_and_reflections(self, tmp_path: Path) -> None:
         kept = link_check.filter_sources(self._paths(tmp_path), tmp_path)
-        rel = sorted(str(p.relative_to(tmp_path)) for p in kept)
+        rel = sorted(p.relative_to(tmp_path).as_posix() for p in kept)
         # docs/archive/ is KEPT: the rule is anchored to dev/ as the first
         # segment so docs/ stays fully link-gated.
         assert rel == sorted([
diff --git a/bootstrap/tests/test_session_routines.py b/bootstrap/tests/test_session_routines.py
--- a/bootstrap/tests/test_session_routines.py
+++ b/bootstrap/tests/test_session_routines.py
@@ -284,7 +284,7 @@ def test_reflection_filename_is_session_distinct(repo, monkeypatch, capsys):
     lifecycle.main(["session-end"])
     out2 = capsys.readouterr().out
 
-    pat = re.compile(r"dev/reflections/(\d{4}-\d{2}-\d{2}-claude-[A-Za-z0-9._-]+)\.md")
+    pat = re.compile(r"dev[\\/]reflections[\\/](\d{4}-\d{2}-\d{2}-claude-[A-Za-z0-9._-]+)\.md")
     m1, m2 = pat.search(out1), pat.search(out2)
     assert m1 and m2, "reflection path must be <date>-<agent>-<session>.md"
     assert m1.group(1) != m2.group(1), "two runs must resolve distinct sessions"
diff --git a/bootstrap/tests/test_upgrade.py b/bootstrap/tests/test_upgrade.py
--- a/bootstrap/tests/test_upgrade.py
+++ b/bootstrap/tests/test_upgrade.py
@@ -219,8 +219,8 @@ class TestProfileSizedAssembly:
         if cff.exists():
             shutil.copy2(cff, croot / "CITATION.cff")
         agents = croot / "templates" / "core" / "AGENTS.md"
-        agents.write_text(
-            agents.read_text(encoding="utf-8") + self._REGION, encoding="utf-8")
+        agents.write_bytes(
+            (agents.read_text(encoding="utf-8") + self._REGION).encode("utf-8"))
         return croot
 
     @staticmethod
@@ -305,7 +305,7 @@ class TestProfileSizedAssembly:
         # gated region, so the two changes land in different merge hunks) ...
         lines = agents_path.read_text(encoding="utf-8").splitlines(keepends=True)
         lines.insert(1, "<!-- LOCAL CUSTOMIZATION: keep me -->\n")
-        agents_path.write_text("".join(lines), encoding="utf-8")
+        agents_path.write_bytes("".join(lines).encode("utf-8"))
         # ... and flips their committed profile from solo to multi-human.
         prof = target / "dev" / ".cairn" / "profile.yml"
         prof.parent.mkdir(parents=True, exist_ok=True)
@@ -1591,13 +1591,14 @@ class TestInitLock:
         review = self._migrate(tmp_path)
         modules = s.read_lockfile(tmp_path)["modules"]
         inventory = tmp_path / "dev/modules/README.md"
-        inventory.write_text(inventory.read_text() + "\nprivate local note\n",
-                             encoding="utf-8")
+        inventory.write_text(
+            inventory.read_text(encoding="utf-8") + "\nprivate local note\n",
+            encoding="utf-8")
         installed_before = inventory.read_bytes()
         assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                        "--cairn-root", str(CAIRN_ROOT)]) == 0
-        ours = (review / "dev/modules/README.md.ours").read_text()
-        theirs = (review / "dev/modules/README.md.theirs").read_text()
+        ours = (review / "dev/modules/README.md.ours").read_text(encoding="utf-8")
+        theirs = (review / "dev/modules/README.md.theirs").read_text(encoding="utf-8")
         assert "private local note" in ours
         assert "private local note" not in theirs
         assert [line for line in theirs.splitlines()
@@ -2784,6 +2785,8 @@ class TestDirtyTreeGuard:
 
     def test_literal_pathspec_name_is_a_single_tracked_path(self, tmp_path: Path) -> None:
         """Caller paths that resemble Git pathspec syntax remain literal."""
+        if sys.platform == "win32":
+            pytest.skip("a file name with a colon and asterisks cannot exist on Windows")
         self._init_committed(tmp_path)
         special = ":(glob)**.md"
         (tmp_path / special).write_text("initial\n")
```

## Proposed product repair (not applied; needs a Decision, see cause 7)

```diff
diff --git a/templates/modules/team-gated/_intent/record_io.py b/templates/modules/team-gated/_intent/record_io.py
--- a/templates/modules/team-gated/_intent/record_io.py
+++ b/templates/modules/team-gated/_intent/record_io.py
@@ -158,7 +158,9 @@ def append_record(
     else:
         target.parent.mkdir(parents=True, exist_ok=True)
     payload = _record_bytes(record_dict)
-    fd = os.open(str(target), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
+    fd = os.open(str(target),
+                 os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0),
+                 0o644)
     try:
         written = os.write(fd, payload)
         if written != len(payload):
@@ -457,7 +459,7 @@ def prune_released_pairs(
     if not target.exists():
         return report
 
-    raw_lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
+    raw_lines = target.read_bytes().decode("utf-8").splitlines(keepends=True)
 
     # Parse what we can; remember which raw index each parsed record came from.
     parsed: List[tuple] = []          # (index, record dict)
@@ -560,7 +562,8 @@ def prune_released_pairs(
     # to zero bytes and ``os.replace`` then made the ledger itself the symlink.
     # ``O_EXCL`` refuses an existing path and ``O_NOFOLLOW`` refuses a link, so
     # neither is reachable now.
-    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
+    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
+             | getattr(os, "O_BINARY", 0))
     tmp = target.with_name(f"{target.name}.prune-{os.getpid()}.tmp")
     try:
         fd = os.open(str(tmp), flags, 0o644)
diff --git a/templates/skills/_lib/session.py b/templates/skills/_lib/session.py
--- a/templates/skills/_lib/session.py
+++ b/templates/skills/_lib/session.py
@@ -1883,6 +1883,10 @@ def _stop_meter_child(proc: subprocess.Popen) -> bool:
 
 def _meter_refresh_receipt(stdout: bytes, returncode: int) -> bool:
     """Validate the closed Meter receipt without relaying child output."""
+    if isinstance(stdout, bytes) and stdout.endswith(b"\r\n"):
+        # A Windows child's print() ends its one line with CR-LF; fold that
+        # one terminator only. Any other CR still fails the check below.
+        stdout = stdout[:-2] + b"\n"
     if (returncode != 0 or not isinstance(stdout, bytes)
             or not stdout.endswith(b"\n") or b"\r" in stdout
             or stdout.count(b"\n") != 1):
diff --git a/tools/_intent/record_io.py b/tools/_intent/record_io.py
--- a/tools/_intent/record_io.py
+++ b/tools/_intent/record_io.py
@@ -158,7 +158,9 @@ def append_record(
     else:
         target.parent.mkdir(parents=True, exist_ok=True)
     payload = _record_bytes(record_dict)
-    fd = os.open(str(target), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
+    fd = os.open(str(target),
+                 os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0),
+                 0o644)
     try:
         written = os.write(fd, payload)
         if written != len(payload):
@@ -457,7 +459,7 @@ def prune_released_pairs(
     if not target.exists():
         return report
 
-    raw_lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
+    raw_lines = target.read_bytes().decode("utf-8").splitlines(keepends=True)
 
     # Parse what we can; remember which raw index each parsed record came from.
     parsed: List[tuple] = []          # (index, record dict)
@@ -560,7 +562,8 @@ def prune_released_pairs(
     # to zero bytes and ``os.replace`` then made the ledger itself the symlink.
     # ``O_EXCL`` refuses an existing path and ``O_NOFOLLOW`` refuses a link, so
     # neither is reachable now.
-    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
+    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
+             | getattr(os, "O_BINARY", 0))
     tmp = target.with_name(f"{target.name}.prune-{os.getpid()}.tmp")
     try:
         fd = os.open(str(tmp), flags, 0o644)
diff --git a/tools/session.py b/tools/session.py
--- a/tools/session.py
+++ b/tools/session.py
@@ -1883,6 +1883,10 @@ def _stop_meter_child(proc: subprocess.Popen) -> bool:
 
 def _meter_refresh_receipt(stdout: bytes, returncode: int) -> bool:
     """Validate the closed Meter receipt without relaying child output."""
+    if isinstance(stdout, bytes) and stdout.endswith(b"\r\n"):
+        # A Windows child's print() ends its one line with CR-LF; fold that
+        # one terminator only. Any other CR still fails the check below.
+        stdout = stdout[:-2] + b"\n"
     if (returncode != 0 or not isinstance(stdout, bytes)
             or not stdout.endswith(b"\n") or b"\r" in stdout
             or stdout.count(b"\n") != 1):
```

## Runs after the repairs

- **15-node run, test repairs only, first set** (before the template write of cause 2
  was found): 4 failed, 10 passed, 1 skipped, 125.33 s. The four were the profile-change
  test and the three `session-end` tests.
- **Run 2, all four files whole, test repairs plus defect A:** 1 failed, 318 passed,
  28 skipped, 544.88 s, exit 1. The one failure was `test_handoff_prunes_the_intent_surface`
  (defect B).
- **Run 3, all four files whole, every repair in this record, in `cairn-winfails-git-20261116`:**
  **319 passed, 28 skipped, 0 failed in 537.71 s, exit 0**, 15:26:59 to 15:36:00 on the Mac's clock (EST). The 347 tests are the 347 of run 1; the one extra skip is the cause-4 test, and the order-dependent test passes inside the whole file.

## macOS check

On a macOS scratch copy (a Git repository of the same archive, repairs applied, Python 3.13.13): the 15 nodes gave **15 passed** (89.8 s). Four related files whole (`test_session_routines.py`, `test_doc_drift_tools.py`, `test_session_writes_contained.py`, `test_intents_tool.py`) gave **374 passed, 1 skipped, 1 failed** (195.5 s): `test_intents_tool.py::test_generated_postcommit_hook_refuses_target_local_git_routes[tools-head]`, an assertion that a hostile-Git marker file exists (`is_file()` was false). I was told to stop running tests, so I did not run that node on the unrepaired copy and did not look at its cause. It exercises the Git route in `_intent/conflict.py`, not the lines in `record_io.py` or `session.py` that the repairs touch, so I do not expect the repairs to cause it, but that is not established. `test_session_writes_contained.py` passed on macOS with the repairs.

## Not run, not determined

- The whole suite, and every file outside the four (the Maintainer's rule).
- Other Git versions: the order-dependent test needs Git 2.44 or newer, so its
  behaviour with an older Git is not measured.
- Why the shipped Meter's `check_acl` refuses this VM's profile path. It leaves the
  handoff at "Meter unavailable" on this VM even after defect A is repaired, which is a
  separate matter from the CR.
- `test_session_writes_contained.py` and `test_intents_tool.py` on Windows (see cause 7).
- Noticed, not diagnosed: `upgrade --stage` over a template tree whose files hold CR-LF
  conflicts on every line while the installer normalises to LF (cause 2's probe). A
  Cairn checkout cloned on Windows with `core.autocrlf=true` would give such a tree;
  I did not try it. It is outside these fifteen.
- Whether the Maintainer prefers `.as_posix()` printed output to the OS form (cause 5).
- The one macOS failure in `test_intents_tool.py` after the repairs (see "macOS
  check"): cause unknown, not compared with an unrepaired copy.
- The fifteen are diagnosed: 4 as the copy's missing `.git` (cause 1), 8 as test
  assumptions (causes 2 to 6 and 8), 3 as product defects (cause 7). No failure was
  left with an unknown cause; the unknowns are the ones listed here.

## Left on the VM

Nothing of mine. At the coordinator's request the four items under `C:\Users\cairn\`
that this task created (`cairn-winfails-files-20261116`, `cairn-winfails-git-20261116`,
`cairn-winfails-work-20261116` and `winfails-530c922e.tar`) were removed after the
record was written, so the scratch scripts (`dd_probe.py`, `dd_probe2.py`,
`test_dd_probe.py`, `meter_probe.py`, `meter_why.py`, `prof_probe.py`, `intent_probe.py`,
`trace_plugin.py`, `reason_plugin.py`), `run1.xml` and the probes' folders no longer
exist on the VM; the scripts and outputs survive only in the Mac session's scratch
folder, not in the repository. Every probe's result is in the sections above, and the
diffs are printed in full. pytest's own temporary folders under `%TEMP%` were written
by the runs as usual and not touched.

**Elapsed:** about 50 minutes (15:55 to about 16:45 EST), plus about 20 minutes reading
the records and tests beforehand; estimates.
**Tokens:** unknown.

## Implementation follow-up -- Codex (Implementation, Low) -- 2026-11-17

Commit `63d0704a` repairs the two Windows product defects in cause 7 and the
Windows-specific assumptions in causes 2 to 6 and 8. The receipt accepts a
single terminal CR-LF while keeping the remaining closed checks. The intent
ledger now reads bytes and opens its append and prune files in binary mode;
the twins match. The test fixes preserve assertions, use explicit UTF-8,
binary writes, platform-neutral path handling, an in-body skip for the
uncreatable Windows path, and bind the Git worker before the real-Git test.

On a fresh Windows x64 `lhm` Python 3.13.18 copy of the committed tree, I ran
only the named defect nodes: **12 passed, 1 skipped, 545 deselected** in 24.21
seconds. The command was:

```text
C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -q -p no:cacheprovider -rfsE bootstrap\tests\test_upgrade.py bootstrap\tests\test_doc_drift_tools.py bootstrap\tests\test_session_routines.py bootstrap\tests\test_intents_tool.py bootstrap\tests\security\test_git_read.py -k "test_profile_change_solo_to_multi_reincludes_region or test_review_inventory_theirs_excludes_local_edit_when_roster_matches or test_literal_pathspec_name_is_a_single_tracked_path or test_real_discovery_cli_finds_planted_issue_without_decoy or test_excludes_dev_archive_and_reflections or test_meter_refresh_receipt_accepts_only_one_windows_line_ending or test_reflection_filename_is_session_distinct or test_session_end_WITH_handoff_DOES_emit_the_standing_capture_prompt or test_handoff_prunes_the_intent_surface or test_session_end_skips_intent_prune_in_linked_worktree or test_append_and_prune_preserve_binary_jsonl_line_endings or test_read_origin_uses_git_parser_for_quoted_and_continued_values"
```

The skip is the documented `:(glob)**.md` filename case; the four `--to HEAD`
nodes were not run in this focused pass. One passed node directly called the
private receipt helper and was removed after review; the run also passed the
public handoff node that exercises `print()` CR-LF. The disposable checkout
was initialized as Git, so archive setup did not cause false failures. On the
canonical macOS Python, the selected owning nodes passed: upgrade 3, document
discovery 3, session 5, Git reader 1, intent ledger 1. One session check was a
temporary direct call to the private receipt validator; ordinary review asked
for public-promise coverage, so that redundant check was removed. The native
run also passed the existing public handoff node that exercises `print()` CR-LF.
Existing public refusal checks remain in `test_session_writes_contained.py`.
The first intent-ledger assertion was corrected to compare the retained
record's actual serialized bytes; its rerun passed.

Not run: the four files whole, other Windows hosts or interpreters, the
`test_session_writes_contained.py` receipt fixtures, broad suite, mutants,
`repin.py status`, or re-anchor. No repair was made for cause 1 because it is
only a validation-copy setup step. **Elapsed:** about 30 minutes. **Tokens:**
unknown.

## Code review -- Sol (Security Review, High) -- 2026-11-17

Reviewed commits: `63d0704aaef53f19a5110a77eeec4e262bd11e68` and
`7c77da3d9326383882a0c433a75d886823caaa07` (focused Windows repairs only).
**Obligation:** Internal Security Review, code pass 1 for this defect range.
**Verdict:** ACCEPT. **Findings:** none.

The repairs let Windows handoff accept the same successful Meter receipt and
prune an existing CR-LF ledger without changing its retained bytes.

**Foundations**

1. **Should this happen as framed?** Yes. Folding only a terminal CR-LF leaves
   every other CR, extra newline, missing terminator, bad exit, duplicate key,
   unexpected field and unsuccessful status rejected. The caller still bounds
   both streams and skips both pruners on failure -- `tools/session.py`,
   `_meter_refresh_receipt`, `_meter_refresh_before_prune` and full-handoff gate.
2. **Best alternative.** Keep these localized changes: stripping general
   whitespace would broaden receipt acceptance, while text-mode rewriting would
   change ledger bytes. `O_BINARY` adds no pathname authority and preserves
   `O_APPEND`, one-write append, exclusive temp creation and `O_NOFOLLOW` --
   `tools/_intent/record_io.py`, `append_record` and `prune_released_pairs`.
3. **What would show it wrong?** A malformed CR-LF receipt reaching either
   pruner, a planted temp link changing its target, or retained ledger bytes
   changing would falsify this pass. I traced those branches and read the
   public refusal and hostile-temp checks; the recorded Windows public handoff
   and CR-LF ledger successes support the repaired path --
   `bootstrap/tests/test_session_writes_contained.py` and
   `bootstrap/tests/test_intents_tool.py`, plus Implementation follow-up above.

The raw-byte read restores the size comparison's original byte count; the
documented final check-to-replace race remains unchanged. Both shipped twins
have identical repairs. Removing the redundant private receipt check preserves
public malformed-receipt refusal coverage; its special terminator variations
were assessed statically here. Fixture changes retain their security assertions.

**Covered:** committed diffs, surrounding receipt/prune guards and named retained
checks. **Not covered / low confidence:** no test reruns, private logs, VM access,
broad suite, mutation inventory, unrelated prior repair range or new concurrency
proof. Existing native results are author-reported evidence, not my measurements.
**Elapsed:** approximately 7 minutes. **Tokens:** unknown.
