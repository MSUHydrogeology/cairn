# Windows run of the Git attributes checks, 2026-11-17

Evidence for C5 of `dev/plans/archive/2026-11-16-git-attributes-file.md`. This records
the public install checks and a Windows checkout with
`core.autocrlf=true`; it is not a release certification.

## Result

All 10 checks in `bootstrap/tests/test_gitattributes_install.py` passed on the
Windows VM; none failed or skipped. The attributes-enabled checkout was clean
and had no working-tree CRLF labels. The adopter-owned control reproduced
working-tree CRLF labels and an upgrade plan mentioning line endings.

| Check | Result |
|---|---|
| Windows pytest file | 10 passed, 0 failed, 0 skipped; 25.57 seconds |
| `proj-attr` working-tree status | 0 lines |
| `proj-attr` `attr/text=auto eol=lf` lines | 84 |
| `proj-attr` `w/crlf` lines | 0 |
| `proj-own-crlf` `w/crlf` lines | 81 |
| `proj-attr` upgrade plan contains `line endings` or `review-only` | No |
| `proj-own-crlf` upgrade plan contains `line endings` | Yes |
| `proj-own` lockfile records `.gitattributes` | No |

## Environment and source

- Windows 11 ARM64 in UTM, build `10.0.26300.0`, SSH alias `cairn-windows`.
- x64 emulated Python `C:\ProgramData\miniconda3\envs\lhm\python.exe`,
  Python 3.13.18; pytest 9.2.0.
- Git for Windows 2.56.0.windows.4. System `core.autocrlf` was `false`;
  both test clones used `-c core.autocrlf=true`.
- The VM source snapshot was
  `C:\Users\cairn\cairn-pulse-native-f9cca5f3`, Git HEAD
  `885447dcac1884ce6e9002f07269018c6eeb5994`. Its working tree held the
  Group 1 Meter/Pulse changes. The test tree was copied locally from that
  snapshot without `.git`; the nine C1–C4 files were then transferred
  individually. Their SHA-256 hashes matched the host files at C4 commit
  `8bc30bc6`. This was a reconstructed tree, not a clean archive of C4.

## Folders and commands

The validation tree was
`C:\Users\cairn\cairn-gitattr-tree-20261117`. The successful project run and
its clones were in
`C:\Users\cairn\cairn-gitattr-work-retry-20261117`; nothing existing was
overwritten and no system setting or package was changed.

The focused check ran as:

```text
C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -p no:cacheprovider -rfsE -v bootstrap/tests/test_gitattributes_install.py
```

The work folder used `profile.yml` with `project_name: Demo`,
`test_command: pytest`, and `preset: solo-greenfield`. It created `proj` and
`proj-own` with `bootstrap\scaffold.py --config profile.yml --target <folder>
--cairn-root <tree> --allow-dev`, initialized Git, added with
`git -c core.autocrlf=false add -A`, and made one local test commit in each.
`proj-own` started with `# none` in `.gitattributes`; its bytes matched the
saved copy after install. Project commits were `080c2d7121f2bb974e491a36b44f20392a24d917`
(`proj`) and `251b98a8d80df516c06a55032542fd2f285fb8e5` (`proj-own`).

Both were cloned with
`git -c core.autocrlf=true clone`. In `proj-attr`, `.gitattributes` matched
`templates/core/gitattributes.txt`; `git status --porcelain` was empty, and
`git ls-files --eol` showed 84 `attr/text=auto eol=lf` lines and no `w/crlf`.
The saved `proj-own` copy remained unchanged, and its lockfile had no
`.gitattributes` destination record. `upgrade --plan` was run over both
clones: `proj-attr` had no line-ending or review-only row; `proj-own-crlf` had
81 `w/crlf` lines and a line-ending plan entry.

The first SSH pytest stream ended before its last node and summary, so the
focused file was completed once more with output collected through process
exit. The complete result above is from that run. Two workflow setup attempts
also stopped before their checks: one lacked a pre-created target directory;
the next exposed a PowerShell wrapper argument error after scaffolding `proj`.
Those folders were left untouched; the successful run used the separate
`work-retry` folder.

## Not run

The II-2b renormalization steps end to end, native ARM64 Python, older Git, a
physical Windows machine, and any other test file were not run. Elapsed human
time and token use are unknown.
