# Reader handoff: ast_pin.py

**Verdict: run `--apply`. No blocking findings.** I rebuilt both corrected fixtures on my own. They match the script's digests byte for byte and make the two red AST tests pass.

Run it as `python3.13 -I <script> --apply`, after checking the sha256 again. `-I` stops a stray `.py` in the scratch folder from being imported. If apply ends in a traceback, run `git restore -- bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/tests/fixtures/scaffold_ast_known_new.json` and delete any `*.ast-pin.tmp`.

**Read in full:** `ast_pin.py` (sha256 verified), `handoff.md`, the runbook, and `repin.py` lines 1-805 and 1255-1308. I read `_ast_attest.py` lines 94-205.

**Probes:**
- Non-blocking: nothing writes to the working tree without `--apply`. The dry run leaves unreachable objects in `.git`, and its `worktree prune` can tidy other stale worktrees (none exist).
- Non-blocking: the script's own git calls are partly sterile. Hooks are off, GIT_* variables are dropped, and commit uses `--no-verify` with signing off. It lacks `--no-replace-objects`, `GIT_CONFIG_NOSYSTEM/GLOBAL` and `core.fsmonitor=false`. I measured 0 replace refs. The result is repin's (sterile, anchored), and I reproduced it independently.
- No `shell=True` and no command strings. Paths are constants, and the transaction's paths must equal them.
- Non-blocking: the deletion proofs refuse on any mismatch. They do not prove `fa86e2cb` was reviewed (a hard-coded claim). Its message names plan C4, "4 constants … gone".
- Non-blocking: if verification fails, HEAD's bytes go back with a clear message. An OSError on the second write is not caught: you get a traceback, the baseline is new, known-new is old, and a `.tmp` may remain. Nothing is committed, and the restore line above recovers.
- The printed commit names exactly the two fixture paths.
- Both fixtures are frozen gate files, so committing them owes the re-anchor ceremony. The script does not say so.

**Ran:**
- `repin status`: 21 CHANGED, 4 MISSING, 0 DUP; known-new 7 REKEYED, 23 ADDED, 4 DROPPED; no lockfile correction. Every name equals `handoff.md`.
- The dry run: output identical to `handoff.md`, with both digests. `git status` (including `--ignored`), the worktree list and the refs were unchanged.
- A detached worktree (`reader3`, now removed):
  - Fixtures derived via `_merge_current`/`_classify` gave the same digests.
  - Baseline diff: 173 to 169, and only `digest`/`span` change on the 21. Known-new: 62 to 81 keys.
  - `verify --known-new` ends "AST attestation OK — 169". `test_ast_attest.py`: 30 passed.
  - Control on HEAD's fixtures: verify exits 1, and 2 tests fail.

**Not checked:** `--apply` on the real repo, the restore branch, the full suite, and `fa86e2cb`'s review status.

I am a fresh same-vendor session that wrote nothing in the range; this is a statement, nothing checks it.
