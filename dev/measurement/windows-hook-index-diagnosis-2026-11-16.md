# Why the Windows commit hook cannot read staged paths (diagnosis), 2026-11-16

Evidence for the Maintainer's decision on Windows item 63.1 of
`dev/plans/2026-11-16-adopter-defects-0-7-0.md` (the C8 run:
`dev/measurement/archive/windows-defects-run-2026-11-16.md`, item (d)). Record only: no
shipped code, test or document was changed. Every fix below was tried on a
scratch copy; none is applied.

## Result

Two defects sit one behind the other in the Windows-only request for the
"hook-index" read (the read that gives Git a private copy of the index the hook
is committing). The first one fires today. The second is hidden behind it.

1. **The first (fires today).** `_capture_windows_git` builds the worker request's
   argument list from the finished command line, which already holds
   `--no-ext-diff --no-textconv` (inserted by `_argv`, lines 617 and 618). The worker then
   checks that list against the two allowed forms and rejects it at line 1533,
   with the reason `worker-request-invalid`. Both allowed forms are rejected, so
   every hook-index read on Windows fails, whatever the repository holds.
2. **The second (behind it).** With the first fixed, the worker rebuilds the
   command line with `_argv`, which asks for the Git version, which tries to
   start a second worker from inside the first; that fails at once with
   `verified-helper-buffer-unavailable`, because the worker was never given the
   helper bytes the parent holds in `_VERIFIED_SOURCE`. This is the cause the plan predicted from
   reading; it is real, but it only shows once defect 1 is out of the way.

It is **not** a request-encoding defect (the JSON, base64 and snapshot fields all
arrive intact). It is a logic error in how the parent builds the hook-index
request, plus a worker that calls code the worker cannot run. It reproduces on
macOS when the Windows route is forced, so it is not specific to Windows; it is
only reached on Windows in real use. It has been there since the route was
written (`459feeba`, 2026-11-06).

A 10-line change (below) let a real Windows pre-commit hook get past staged-path
discovery (it then printed its identity warning; see table 5). It is a small
follow-on proposal's worth of work, with the same pin cycle as chunk C7 and a
Security Review (it touches a check inside the helper). The diagnosis shows no
larger problem: the worker's other two operations work (a plain read, and one
`origin-config` read, measured); what was missing is any test of a successful
hook-index read through the Windows worker.

## What was measured, read and assumed

- **Measured on Windows** (the VM, real Git): the reason codes of the committed
  helper and of four instrumented or patched copies; which line fires; a real
  `git commit` through the pre-commit hook in the unpatched, the instrumented
  and the patched tree; timings; the existing hook-index tests' outcome.
- **Measured on macOS** (Git 2.53.0): the argument list the parent sends, and a
  prototype test that forces the Windows route.
- **Read from the code, not run:** the trust analysis of each fix; that no other
  caller exists (`git grep`); how long the defect has existed (`git log -S`).
- **Assumed:** nothing is relied on beyond the above. Not measured: other Git
  versions, other Windows hosts, the ARM64 interpreter, a repository with a
  linked worktree.

## Environment and folders

- Windows 11 (`ver` 10.0.26300.9974) under UTM; SSH alias `cairn-windows`.
  Interpreter: x64 `C:\ProgramData\miniconda3\envs\lhm\python.exe` (Python
  3.13.18). Git 2.56.0.windows.4. VM clock 11:52 to 11:58 (three hours behind
  EST; 14:52 to 14:58 EST).
- Tree: `git archive` of `6b7a4a09`, whose helper
  (`templates/skills/_lib/git_read.py`, byte-identical to `tools/git_read.py`)
  has SHA-256
  `b9f04cc22ec889dd7835c5f985fb910843b02142e6270c252b46090cb634bfb2`. The input was a scratch Git repository
  (`a.txt` committed, `b.txt` staged); no repository content or secret is
  involved.
- New folders under `C:\Users\cairn\` (listed at the end). No system setting
  was changed, no package installed, no network connection opened by me.

## Hypotheses and outcomes

From reading `_windows_worker_run` (lines 1484 to 1572) and the bootstrap
(lines 1175 to 1209). The code `worker-request-invalid` comes from eleven places:
the bootstrap's starting value of `stage` (line 1177), the bootstrap's size
check (1180) and the nine `raise GitReadError("worker-request-invalid")` sites in
`_windows_worker_run` (lines 1506, 1519, 1522, 1529, 1533, 1542, 1551, 1554,
1560).

| # | Hypothesis | Outcome |
|---|---|---|
| H1 | Line 1533: the list in `request["args"]` is not one of the two allowed forms, because `_argv` added flags and line 1314 slices them in | **Confirmed.** Instrumented copy reports `wri-L1533` (below) |
| H2 | After H1, `_argv` (line 601) calls `_git_version` and `_version_probe` inside the worker, reaching `_capture_windows_git`, where `_VERIFIED_SOURCE` is `None` (line 1296) | **Confirmed** by the patched copy `v1` |
| H3 | Line 1542: the worker's `_hook_snapshot_matches` disagrees with the parent's about the private index copy | Ruled out: the instrumented run stops earlier, and the patched copies pass this check |
| H4 | The bootstrap's own starting `stage` or size check (bad JSON, base64, over 2 MiB) | Ruled out: the instrumented copy gave those two places their own codes; neither appeared, and plain reads through the same bootstrap complete |
| H5 | Any other of the nine inner sites | Ruled out: only line 1533 appears in the worker's trace |

**How the sites were told apart (scratch only).** A script
(`mkdiag.py`, in the scratch folder) read the tree's helper and wrote a copy in
which each of the eleven sites above has its own code (`wri-L<line>`, plus
`wri-bootstrap-start` and `wri-bootstrap-size`), added to the allowed reason set,
and a small function that appends the exception to a text file from inside the
worker. The repository's own files were not edited.

## Windows measurements

**1. Baseline and instrumented copy**, calling `read_hook_index(<repo>, <form>,
index_file=".git/index")` from the repository folder, as the hook does
(`GIT_INDEX_FILE` was `.git/index` in the C8 run).

| Call | Committed helper | Instrumented copy |
|---|---|---|
| hook-index `diff --cached --name-only -z` | failed, `worker-request-invalid` | failed, **`wri-L1533`** |
| hook-index `diff --cached --name-status -M -z` | failed, `worker-request-invalid` | failed, **`wri-L1533`** |
| the same read with no `index_file` (outside a hook) | completed, `b.txt` | completed |
| `run_git` `rev-parse --verify HEAD` | completed | completed |
| `run_git` `diff --cached --name-only -z` | completed | completed |

**2. A real hook.** Instrumented tree, `install-precommit`, one staged file,
`git commit`: exit 0 and the hook's usual warning "staged path discovery is
unavailable"; after I cleared the trace file first, it held one entry,
`GitReadError wri-L1533`. (The hook stops after the first failed read, as
`_precommit_check_impl` does at lines 1013 to 1020, so the second form is not
tried in a hook; the direct calls in table 1 tried both.) So the failure in a
real hook is the same site the direct call shows. An earlier hook run in the
same tree left a second entry because I had not cleared the file; I discarded it
and repeated the run.

**3. The argument list the parent sends** (macOS, `_argv` over each allowed form
and the slice at line 1314):

```text
allowed  ('diff', '--cached', '--name-only', '-z')
sent     ('diff', '--no-ext-diff', '--no-textconv', '--cached', '--name-only', '-z')   not in the allowed set
```

The name-status form is rejected the same way. This is the input line 1533
rejects: a list of six or seven plain strings, one of them extra by two.

**4. Candidate fixes** (copies in the scratch folder; times are three runs each
in one process, indicative only):

| Copy | Change | Result | Seconds per read |
|---|---|---|---|
| `v1` | line 1314 sends the form without the two inserted flags | still fails: **`verified-helper-buffer-unavailable`** (trace: `_argv` at line 601, `_git_version`, `_version_probe`, `_capture_windows_git`) | n/a |
| `v2` | `v1` plus the bootstrap sets `module._VERIFIED_SOURCE` and `_VERIFIED_SHA256` **before** `exec` | still fails, same reason: the module's own line 87 (`_VERIFIED_SOURCE = None`) overwrites it | n/a |
| `v2b` | `v1` plus the same two lines **after** `exec` (as `load_verified_module` does) | **completes**, both forms | 1.43, 1.09, 1.00 |
| `v3` | `v1` plus `_argv` gets `skip_version_probe`, passed `True` only by the worker's hook-index branch | **completes**, both forms (stdout `b.txt\0`; `A\0b.txt\0`) | 0.95, 0.65, 0.62 |
| `v3clean` | `v3` without the diagnostic code | **completes**; used for the real hook run below | 0.89, 0.73, 0.79 |

`v2b` works because the worker then starts a second worker for the version
probe: three processes per read instead of two, about 0.3 to 0.4 s slower here.

**5. A real hook with the patched helper.** A copy of the tree with
`tools/git_read.py` replaced by `v3clean` and the one pin literal in
`tools/_intent/conflict.py` updated (scratch only). Same steps as C8 (d):
`git init`, one commit, `install-precommit`, a staged file, `git commit`. Result:
exit 0 and the hook printed its normal "PRE-COMMIT CHECK -- UNKNOWN IDENTITY"
message instead of "staged path discovery is unavailable". That identity warning
is printed after the staged paths are read, so the paths were read. (I did not
set an identity, so the claim-overlap logic itself was not exercised.)

**6. The existing hook-index tests on Windows** (`pytest -k hook_index
bootstrap/tests/security/test_git_read.py`, unpatched `templates/` helper):
2 passed, 1 skipped. The skip is
`test_hook_index_uses_private_snapshot_and_closed_child_environment`
("real Git 2.45 or newer is required for hook index reads", line 662): that test
never binds the worker source on Windows, so its read fails and it skips. The two
that pass check refusals only. **No existing test reads staged paths through the
Windows worker**, which is why this passed C7 and every earlier run.

**7. A sibling check.** The worker's third operation (`origin-config`) completed
once through the worker with the committed helper (stdout the origin URL). One
read, not a test; it shows the worker route is not broadly broken.

## Is this only a Windows problem, and who else is affected

- **Callers.** `git grep read_hook_index` finds two call sites outside tests:
  `_staged_paths_via_git` and `_rename_map_via_git` in
  `tools/_intent/conflict.py` (and the same two in
  `templates/modules/team-gated/_intent/conflict.py`), both called from the
  pre-commit check with `GIT_INDEX_FILE`. Any hook-index read with an index
  locator fails on Windows today, in either form (measured). A read without a
  locator goes through `run_git` and works (measured).
- **Portable reproduction.** On macOS (Git 2.53.0) a prototype forced the Windows
  route by making `_capture_process` call `_capture_windows_git`, then called
  `read_hook_index` over a repository with one staged file and a
  `next-index-123.lock` copy of the index. Committed helper: failed,
  `worker-request-invalid`, both forms. `v3clean` and `v2b`: completed, stdout
  `a.md\0` and `M\0a.md\0`. So defect 1 is a logic error on any operating system.
  Defect 2 is **invisible** on macOS: `v1` completed there, because the worker's
  `os.name` is `posix` and the version probe takes the POSIX route without the
  buffer. Defect 2 needs a Windows run (or an in-process test, below).
- **History.** `git log -S` finds both the line 1314 slice and the `--no-ext-diff`
  insertion in `459feeba` (2026-11-06, "Safe-Git C1: snapshot intent hook index
  safely"): the route has never worked on Windows.

## Proposal input (not applied)

**Smallest change that I measured to work (`v3clean`).** Only
`templates/skills/_lib/git_read.py` (then `cp` to `tools/git_read.py`), four
hunks in three places, about ten lines:

1. Line 1314: send the allowed form, not the finished command line, for example
   `request["args"] = [argv[argv.index("diff")], *argv[argv.index("diff") + 3:]]`
   (drops the two flags `_argv` inserted; couples to that insertion, which the
   test below pins).
2. `_argv` (line 588): add `skip_version_probe: bool = False` and wrap lines 601
   to 605 (the version request and the 2.45 floor) in `if not skip_version_probe:`.
3. Line 1547: the worker calls `_argv(..., skip_version_probe=True)`.

**What it changes about trust.** It changes how the request is encoded and which
process checks the Git version, not what the worker trusts: the worker still
rebuilds the command line from the verified Git snapshot, the target and one of
two fixed forms, and still checks the index snapshot. It stops re-checking the
version floor inside the worker. The parent has already run that check in
`_run_once` before it builds the request, and the plain `read` operation never
checked it in the worker. A new default-off argument on `_argv` is a new way to
skip a check, so the Security Review should look at it.

**Alternative with the smallest diff (`v2b`).** Fix line 1314 and add two lines
to the bootstrap after the `exec`. About three lines, measured to work. Cost: the
worker can start a worker (two more processes per read, about 0.3 s here), and
the worker module gets the same source binding the parent has, which is a wider
worker. The plan's predicted fix, placed where the plan says (`__verified_source__`
beside `_VERIFIED_SOURCE`, before `exec`), does not work (`v2`).

**Tests I would require.**

- *Windows-only* (`skipif(os.name != "nt")`, real worker, real Git 2.45 or newer):
  stage one file in a scratch repository, copy `index` to
  `.git/next-index-123.lock`, bind the worker source, call `read_hook_index` for
  both forms, and require `completed`, return code 0 and the staged path in the
  output. It must fail first on the committed helper
  (`worker-request-invalid`, measured) and, with only the line 1314 fix, fail with
  `verified-helper-buffer-unavailable` (measured). The existing line 609 test
  should not be left as the only hook-index success test, because it skips on
  Windows.
- *Portable* (any OS with Git 2.45 or newer): the macOS prototype above, as a
  test: monkeypatch `_capture_process` to call `_capture_windows_git`, bind
  `_VERIFIED_SOURCE` and `_VERIFIED_SHA256` (the test file's `_bind_worker_source`
  returns early off Windows, so the test needs its own monkeypatch), use the
  resolved temporary path (macOS `/var` is a link, and `hook-index-locator-outside-admin`
  results otherwise), and require both forms to complete. It fails first on the
  committed helper (measured on macOS). It catches defect 1 only.
- *Optional, not prototyped:* an in-process test that builds the request with the
  real `_capture_windows_git` and a fake `Popen`, runs `_windows_worker_run` on it
  with `_worker_job` and `_capture_windows_child` replaced, and makes
  `_git_version` fail the test if the worker calls it. That would catch defect 2
  on any OS.
- The C7 test that runs the real `_windows_worker_run` uses a nine-key `read`
  request, which is why it could not see the hook-index request shape.

**Cost.** Any helper edit stales the same 23 pin files and the two second-order
pins as chunk C7, plus the scoped `--finalize` and the Maintainer's re-anchor.

## Not determined

- Whether other Git versions or Windows hosts differ. One host, one Git, the
  x64 interpreter only.
- Whether the change in item 5 passes the Maintainer's full gates: I ran no
  suite and made no claim-overlap check with an identity set.
- The security effect of either fix beyond the reading above; that is the
  Security Review's question.
- How the control tree's `worker-incomplete` arose: I did not run the pre-plan
  helper. By reading, the pre-C7 reply carried no reason, so the same site would
  appear as `worker-incomplete`; unmeasured.
- Whether `hook-index` on a linked worktree (the `.git` file branch of
  `_hook_repository`) works on Windows; not tried.

## Left on the VM

Under `C:\Users\cairn\`, all new, all deletable by the Maintainer:
`cairn-hookdiag-20261116` (unpatched tree, now a Git repository with the hook
installed and two probe commits) and `cairn-hookdiag-20261116.tar`;
`cairn-hookdiag-inst-20261116` (instrumented helper); `cairn-hookdiag-fix-20261116`
(patched helper and one pin literal); `cairn-hookdiag-work` (scratch scripts, the
variants `inst0`, `v1`, `v2`, `v2b`, `v3`, `v3clean`, a scratch repository and the
worker trace). Nothing in the repository was touched except this file. The macOS
prototype and the variants' copies are in the session's scratch folder, not
committed.

**Elapsed:** about 20 minutes of agent time for the VM work (11:52 to 11:58 VM
time) after about 15 minutes of reading; both are estimates.
**Tokens:** unknown.
