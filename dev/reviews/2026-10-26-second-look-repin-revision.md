# Code review -- second look at the `repin` revision -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

**Model**: Sonnet 5.5, fresh session; I did not write or implement any of it, and I am not the first code reviewer.
**Tier**: Internal. **Called by**: none. **Reviewed commit**: `e3cec581`, read against the first review's `595cbfdc`. Code last changed at `baca8a45` (`git diff baca8a45 e3cec581` over the three code files is empty), the commit M2's `--reviewed-commit` should name.
**Answers**: `dev/reviews/2026-10-26-code-review-repin-build.md` (B1, B2, N3). **Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).
**Where things ran**: detached worktrees of `e3cec581` and `595cbfdc` in the scratchpad (removed after), scratch beds only. No real key, `~/.ssh`, anchor, ceremony, re-anchor or `CAIRN_FULL_SUITE`.

**Verdict: no blocking findings.** B1 and B2 are fixed as the Maintainer chose, and the N3 check has no false-refusal path I could build. Three non-blocking points, each a line of test or output.

## Foundations
1. **Does it do what it claims?** Yes. The loader probes (below) never ran a committed byte outside the ten listed files; the control run of 24 selected nodes passes. -- `scripts/repin.py:208-267`, ledger L1-L6.
2. **Simpler or safer build?** None simpler. The loader's "never on the search path" is a belt that no test pins (N1). -- `scripts/repin.py:296-300`, mutant M8.
3. **What breaks it?** I found no input that runs unlisted code. A deliberate break of the loader (M8) does let a bare import run it, and no test notices (N1). -- ledger L7, M8.

## Findings (all non-blocking)
**N1. "The extraction is never on `sys.path`" is not pinned.** Mutant M8 (append the extraction to `sys.path` before the load) passes all 24 selected nodes, yet with a pinned `_oracle.py` doing a bare `import planted` the planted file runs (marker written) and is refused only afterwards. Control: marker absent. *Fix:* one test with that shape, asserting refusal and no marker.
**N2. A first run with nothing owed no longer prints "No pin is owed...".** `--first-run` skips `package()`, which printed it (old and new first-run output differ by exactly that line, measured with ids masked). *Fix:* print the line in `check_first_run` when `txn is None`, or leave as is and say so in the plan.
**N3a. The new stage-2 check compares for inequality only.** It cannot refuse a good ceremony (new checkpoint is always a different commit; the happy-path test passes). A stage 2 that exits 0 and leaves the anchor on some *other* roster-signed commit (a rollback) would still pass; reasoned, not measured (needs a second signed commit and a same-user writer, the accepted limit). *Fix if wanted:* `merge-base --is-ancestor <old> <new>`.

## Rulings
1. **Loader (B1).** Fixed. Ten files loaded by file location under dotted names; parents are empty in-memory packages; judged by `__spec__.origin` (a blanked `__file__` or `__spec__` no longer hides anything). Ten probe groups below (29 test runs, status and package): ran without the payload, or refused; never ran it.
2. **N3 addition.** One check, no false-refusal path found; one false-pass path (N3a), same-user.
3. **B2.** Matches the Maintainer's answer. First run shows a lockfile-only correction and leaves it; an owed AST pin (alone or with a lockfile one) still refuses; an ordinary ceremony applies it. `check_first_run` diff: only the `txn` condition, its message and the show; the one other first-run change is `raw = None if args.first_run else package(...)` (N2). Refusal output for an owed AST pin is identical but for the words "(the AST baseline)".
4. **Plan text** (`git diff 595cbfdc..e3cec581 -- dev/plans/repin-build.md`): the R5 row, the R5 criterion and M2 changed, as authorized; no other criterion or fence text changed. Also changed: Status, one budget-counting sentence, the dangling "Proposed paths" sentence, "three" entries, the appended record. The budget sentence is new rule text the first review asked for (item 9); the Maintainer's quoted answer is the option label only.
5. **Gates.** Bandit on `scripts/repin.py`: 7 LOW, 0 MEDIUM or higher; `ALLOWLIST` is `{}` and `bootstrap/security_check.py` untouched. Imports are standard library only (AST list, none outside `sys.stdlib_module_names`). The seven revision commits touch only `scripts/repin.py`, the two repin test files and the plan; the full range also holds other sessions' commits (`upgrade.py`, proposals, a plan) that I did not read.

## Falsification ledger (committed file in the tree; `status` unless noted; `package` also run, same results)
| # | Probe | Result (status line) |
|---|---|---|
| L1 | a package marker (init file) planted in the folders bootstrap and scripts, with a marker write, `__file__ = None`, `__spec__ = None`, `sys.modules.pop` | ran, rc 0, marker absent: "checked  10 files at HEAD equal the anchor's entries before any import" |
| L2 | modules named scripts and bootstrap at the root and inside bootstrap/tests and scripts, each alone and all at once | ran, marker absent, same line |
| L3 | `sitecustomize.py`, `usercustomize.py` (root, `scripts/`, `bootstrap/tests/`) | ran, marker absent (equivalent: `-I`, nothing on the path) |
| L4 | `.pth` files (root, `scripts/`, `bootstrap/tests/`) | ran, marker absent (equivalent) |
| L5 | 22 stdlib names (`types`, `ast`, `sysconfig`, `importlib/`, `tempfile`, `json`...) at root, `scripts/`, `bootstrap/`, `bootstrap/tests/` | ran, 0 of 22 markers, each place |
| L6 | tracked `.pyc` for a listed module | refused: "a compiled file is tracked: bootstrap/tests/_oracle_trust.pyc..." |
| L7 | pinned `_oracle_trust.py` loads `_gate_manifest.py` under another name | refused: "the module alias_gm loaded from ... which is not on the checked list. Nothing further was run." |
| L8 | pinned `_oracle.py` bare `import _oracle_activation`, with and without a `sys.path` insert | refused both ("No module named" / "the module _oracle_activation loaded from ...") |
| L9 | pinned module replaces `sys.modules['bootstrap']` | refused: "the module bootstrap loaded from None..." |
| L10 | control: anchored tree | ran, rc 0 |

| Mutant (detached worktree; control C = 24 passed) | Result |
|---|---|
| M1 first run refuses any pin again | killed (lockfile first-run test) |
| M2 first run applies the lockfile (`package()` not skipped) | killed (same test; the run took 298 s against 70 s) |
| M3 first run ignores every pin | killed (2: AST-owed, AST plus lockfile) |
| M4 first run ignores a pin whenever the lockfile is in it | killed (AST plus lockfile test) |
| M5 ordinary ceremony never applies | killed (lockfile apply test) |
| M6 N3 check removed | killed (the "not done" test) |
| M7 loaded modules judged by `__file__` again | killed (2: both blanking variants) |
| M8 extraction on `sys.path` | **survived** all 24; not equivalent (N1) |
| M9 `check_loaded` removed | killed (3) |

## Bounding
**Bounding**: FULL RUN REQUIRED. The record is mode `full`, `Certified by: pending`, from a shared tree that was not clean. I ran 24 selected nodes plus probes, not the 189 it cites. The next certifying run must contain `baca8a45`.

**Coverage.** Not covered: the anchored `_gate_*` modules' own lazy imports at call time (the post-import check runs once, after the load); the AST child's `sys.path.append` of `bootstrap/tests` (unchanged, standard-library names win there); the N7/N8 changes (launcher re-hash, output points); a real `launchctl`, agent or ceremony; NFD names; the 189-test record; other sessions' commits in the range.

## Addendum -- fixes read -- 2026-10-26

Read in full: `git diff e3cec581..5670dda9` over `scripts/repin.py` and the two repin test files (+58 lines, 3 commits: `f57b6f81`, `e37b08ac`, `5670dda9`). Detached scratch worktree of `5670dda9`, removed after; no key, anchor, ceremony or full suite.
- **N1: fixed as recommended.** New test commits a `planted.py` in all four folders, has a pinned `_oracle.py` bare-import it, asserts refusal and no marker, with a bare-`python` control. Mutant M8 again (extraction on `sys.path`): killed.
- **N2: fixed as recommended.** `check_first_run` prints the same line (now the constant `NOTHING_OWED`, shared with `package`) when nothing is owed; new test; mutant (line removed): killed.
- **N3a: fixed as recommended.** `merge-base --is-ancestor <old> <new>` after the unmoved check; a failure of git itself also refuses (fail-closed). Two new cases (unrelated commit, older commit), each with the signature check forced to accept, so ancestry alone decides; mutant (check removed): both killed.
- **False refusal on a good ceremony: none found.** A real checkpoint descends from the old anchor. 11 nodes passed on `5670dda9`: the full-ceremony test, the signing-children full run, the ordinary lockfile ceremony, the first-run tests, the unmoved and not-ahead tests, the verification test, the new N1 test.
- **Nothing else changed a meaning.** The diff holds only these three edits and their tests.
- **`--reviewed-commit`: `5670dda9`** is the last commit to edit the three code files, and I read the whole diff `e3cec581..5670dda9` above; the first diff `595cbfdc..e3cec581` was read in the pass above. The 189-test record and the certifying run are still pending.
