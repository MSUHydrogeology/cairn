# Reader hand-off: first re-anchor under the new design

**Conclusion.** I found no defect that needs a code change, so I committed the record: `55d31f1e59a95c5185b08cb5242b7c23bd73debc` (`dev/ceremony-record.md`), on top of `38965e4a`. All four record checks pass. R1 parent `38965e4a`; R2 only the record; R4 SAME; E5 SAME twice. I re-hashed the packet and launcher, and all eleven member digests equal the blobs at X.

I am a fresh same-vendor session that wrote nothing in the range; this is a statement, nothing checks it.

## What I read
- **In full** (anchor to `38965e4a`): the five closure files that changed: `_gate_preflight.py`, `_gate_manifest.py`, `reanchor.sh` and the launcher template, plus the runbook (all of it at X, and its removed lines). The other six, `allowed_signers` included, are unchanged. I also read all of `security_check.py`, and of `_scaffold`: `security.py`, `lockfile.py`, `merge.py`, `cli.py` and `__init__.py`.
- **In part**: `scripts/repin.py` (lines 1-330, 355-380, 450-462, 570-830 and 940-1309; the AST-pin internals skipped); `scripts/reanchor_ceremony.py` (every added line, not the 289 removed); `_scaffold/upgrade.py` (only its new git call); `config.py` and `install.py` (only their scan hits).
- Unchanged: `conftest.py`; no `.pth` or pytest settings file changed.
- **Not read**: the 45 changed test files and the rest of the 286 changed paths.

## Scanners, each with a planted control
- **Range report**: 77 hits in 17 scanned files, none suspicious. My one-line explanations, grouped by file, are in the record. Scan digest for anchor..`55d31f1e`: `4dd3e815a4f549a37101555a4dcf502eaa16f7d06374ddb794c99ee321c346e7`.
  - The control fired on 5 of 7 plants: an added `conftest.py` process start, `curl ... | sh` in `reanchor.sh`, `shell=True` in `repin.py`, a `.pth` file under `bootstrap/` (caught by its content) and a tracked `.pyc`.
  - It did not fire, by design, on a `.pth` file at the repository root or on `os.system` added to a test file. Tests run at stage 1 and are not scanned.
- **Bandit** (`security_check.run_bandit`, the same targets the test uses; 72 files including the closure and `repin.py`): clean.
  - The control `subprocess.run(cmd, shell=True)` fired (HIGH).
  - A literal `subprocess.run("...", shell=True)` did **not** fire: it is LOW, below the MEDIUM gate.
- **I did not run `security_check.py` itself**: its phase 3 runs the whole suite.

## Dropped test nodes (collect-only at X, Python 3.13)
4612 nodes pinned, 5479 collected, **168 dropped**:
- 86 from seven deleted test files: 77 by `6e9c068d` (onboarding C2) and 9 by `fed00f7b` (ceremony C3).
- 82 from eight kept files, mostly renamed classes in `test_reanchor.py` (`b748de2d`, `8df7e2a2`, `ae1d47c2`, `fccefaab`), plus `fa86e2cb` (15), `6e9c068d` (4) and `50b4ad70` (1).

`verify --no-collect`: HOLD, with 29 FROZEN-MODIFIED (each with FROZEN-OID), 17 FROZEN-MISSING and 19 FROZEN-NEW.

**Known reds for Y4**: that HOLD set, and the AST attestation tests. `_scaffold` changed in 30 commits while the AST baseline did not change. Assumed from history; not run.

## Surprising or small
1. Y3 asks for an explanation of every hit **in the record**, but my brief said to keep the record's free text short. I added 13 short comment lines to cover it.
2. The page lists `reanchor.sh` as "not line-scanned" because of its file mode, but it was scanned (4 hits).
3. The page tells you to "Run E7". At this first ceremony E7 cannot run, as the runbook's first-ceremony section says.
4. The scan's file classes come from the files on disk in the checkout, not only from git. So the 17 deleted pinned files show as "outside-coverage", and the digest can depend on stray files there.
5. All 470 commits are unsigned. (reported, not a verdict).
6. An older worktree, `scratchpad/cert` at `b15dda53`, is 68 commits before X. I saw no certifying run at X.
