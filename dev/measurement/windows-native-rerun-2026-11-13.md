# Windows native rerun, 2026-11-13

A record of one native Windows rerun and what it did and did not show. It is
evidence for roadmap item 12 (owed check b) and item 29, not a release record.

## What was run

- **Code:** a clean copy of the committed tree at `bf1d7bff`, made with
  `git archive`, sent to the Windows VM (alias `cairn-windows`, Windows ARM64
  under UTM, Git for Windows 2.56.0) and unpacked into a new folder. Nothing
  uncommitted was included.
- **Run 1:** native ARM64 Python 3.13.17, pytest 9.2.0. The 24 nodes the
  Python 3.12 plan maps to installed workflows, plus all of `test_meter.py`
  and `test_prose_tools.py`. Result: 583 passed, 49 failed, 76 skipped,
  1 error, 6 minutes 10 seconds.
- **Run 2:** x64 (emulated) Python 3.13.18 in the VM's `lhm` environment, on
  seven files (`test_git_read`, `test_meter`, `test_prose_tools`,
  `test_api_access_security`, `test_model_selection_stub`,
  `test_security_stack`, `test_web_hosting_security`). Result: 671 passed,
  58 failed, 72 skipped, 16 errors, 8 minutes 39 seconds.
- **Run 3:** the same x64 Python on three roster-family files with Git's
  tools folder added to `PATH`. Result: 236 passed, 27 failed, 1 skipped.

## What it showed

- **The Windows-native roster nodes passed.** The security manifest lists
  63 Windows-only (`nt`) nodes. The 48 that live in the files I ran all
  passed, in both Python builds. The other 15 are in files I did not run.
- **59 distinct non-native tests failed** across runs 1 and 2:
  - `test_git_read.py` (19). These build a fake `git` from a `#!/bin/sh`
    script (`_fake_git`, used by 27 tests), which Windows cannot run, so the
    helper reports Git as absent. One more calls `os.killpg`, which Windows
    lacks. They look like POSIX-only tests without a Windows skip.
  - `test_meter.py` (24). Most report `Unavailable`. The cause is not
    confirmed; it may be the same fake-Git fixture.
  - `test_prose_tools.py` (4). Two compare `\r\n` with `\n` (a line-ending
    difference, either in the test or in the replacer on Windows). Two are
    not diagnosed.
  - `test_model_selection_stub.py` (1), not diagnosed.
  - `test_api_access_security.py` (9) and `test_security_stack.py` (2).
    These files are in the security roster family. The first run reported
    that `openssl` was missing on the VM. With Git's tools folder on `PATH`
    27 still failed across three files (web-hosting, API-access and
    security-stack); I did not read those causes.
- **Ruled out:** the failures are not specific to ARM64 (the x64 build failed
  the same way). An early probe that imported the Git helper directly and got
  "verified-helper-buffer-unavailable" proved nothing: that message is the
  designed result of importing it without the test fixtures.

## Not known

- Whether the roster-family failures (11 nodes, plus the web-hosting group)
  would block the Windows release record. SECURITY.md says portable cases in
  the roster must pass on each host; I did not confirm which nodes count.
- Whether the other 15 `nt` roster nodes pass.
- Whether these tests ever passed on Windows before the 2026-11-11 test cut.

## Reproduce

```sh
git archive --format=zip -o cairn-head.zip <commit>
scp cairn-head.zip cairn-windows:cairn-head.zip
ssh cairn-windows 'powershell -NoProfile -Command "Expand-Archive -LiteralPath cairn-head.zip -DestinationPath cairn-rerun -Force"'
ssh cairn-windows 'cd /d C:\Users\cairn\cairn-rerun && C:\ProgramData\miniconda3\python.exe -m pytest -q -p no:cacheprovider -rfsE <files>'
```

**Elapsed:** unknown. **Tokens:** unknown.
