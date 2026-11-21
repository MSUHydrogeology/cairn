# A Security Review read of the six files the v0.9 signing page does not scan

**Author**: Claude Opus 5.5 (Security Review)
**Model**: claude-opus-5-5
**Date**: 2026-11-21
**Status**: settled

## Conclusion

You can sign these six files as they are. None runs a shell command, touches the network or writes outside the project unless asked, and none makes a security check pass when it should fail. Before signing, confirm one thing beyond the six: eight other new code files may also be missing from the page (first finding below).

Git confirms the six are the only files added under `tests/` and `dev/tools/` since `e5b7fd0a` once moved files are followed and test modules are left out. `refs/cairn/gate-anchor` is absent in this checkout, so I used `e5b7fd0a`.

## The six files

**`dev/tools/pulse.py`** (1,399 lines) builds a measurement summary from test reports, test counts, token usage and review files that the caller names on the command line. It opens only those paths, refuses links, hard links and special files, caps every size, rejects XML entity tricks and duplicate JSON keys, and prints to the screen. It runs no program and writes nothing. It is byte-identical to the shipped `templates/skills/_lib/pulse.py`, so this read covers both.

**`tests/security_manifest.py`** (691) decides which tests run when. It names 14 security test files that run at the release ceremony instead of on every change, 16 Maintainer-only test files left out of the release selection, and 425 test IDs (63 Windows-only, 362 POSIX-only) allowed to skip on the other platform. Against `e5b7fd0a`: three re-anchor and preflight test files left the security family, the 16 exclusions are new, and no Windows-only ID was added. Your Decision of 2026-11-16 adopted these changes, recorded in `dev/plans/archive/2026-11-16-release-tests-shipped-only.md`. Its two validators refuse an excluded security or required file and a changed skip list.

**`tests/gauge.py`** (371) counts lines added each week by kind of file, using `git log` through the hash-pinned Git reader. With `--snapshot` it writes one dated file under `dev/measurement/`.

**`tests/README.md`** (41) tells maintainers how to re-check numbers cited in documents.

**`dev/tools/prose_roots.txt`** (17) lists the folders and files whose wording the prose checks treat as functional. Against the old `scripts/prose_roots.txt` it only renames paths and adds `install`, `release` and `tests`, which widens the check.

**`tests/_repo_root.py`** (13) finds the repository by looking upward for `.zenodo.json`.

## Findings

1. **should fix** (outside the six). Eight more new code files sit outside the old scanner's new-file folders (`scripts/`, `bootstrap/`) and outside its sensitive list, which names old paths: `install/scaffold.py`, `install/_scaffold/layout_catalog.py`, `install/_scaffold/layout_migration.py`, `release/check_release_test_members.py`, three `templates/modules/default-on/*.py` files, and `templates/skills/_lib/pulse.py`. I did not check whether the page shows them by another route. Before signing, check whether the page lists each as scanned. My read covers only the pulse copy.
2. **note** `tests/gauge.py:225-236` runs `dev/tools/pulse.py` with no hash or link check, unlike `git_read.py` (lines 63-157, hash verified to match). This trusts nothing beyond the checkout.
3. **note** `tests/security_manifest.py:656-690`: the skip list's fingerprint sits in the same file, so it catches accidental edits, not deliberate ones. The file's protection is the gate, which is why this read matters.
4. **note** At a Mac signing run the 63 Windows-only tests may skip. That was also true at `e5b7fd0a`.
5. **note** `dev/tools/pulse.py:1056` lets a review-file label carry invisible control characters that lines 335 and 1317 refuse. The label is printed (line 942). Minor: you supply the file.
6. **note** `tests/gauge.py:308` and `tests/gauge.py:358-365`: `--root` can point at any folder, and `--snapshot` then writes there and follows a linked `dev/measurement` folder. The date in the file name is checked, so the name cannot escape.
7. **note** `tests/_repo_root.py:10-12` would accept a `.zenodo.json` in a folder above the project.
8. **note** `tests/gauge.py:32-33`: the usage text names the old path `tools/gauge.py`.

No secrets or personal data appear; the only name is yours, in three copyright lines.

## What I did not check

I ran no test. I loaded both versions of `security_manifest.py` in a scratch folder to compare their lists and ran its two validators, which passed. I did not read `git_read.py`, `conftest.py`, `release/security_check.py` or `tests/verify_counts.py`, so I accept on trust that the Git reader runs no project programs and that `tests/README.md` correctly says the count check runs no commands. I did not reproduce the signing page.
