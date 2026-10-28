# Reader hand-off: second ceremony, the AST pin (record on 000b0e9a)

**Conclusion.** I found nothing wrong, so I committed the record. The record commit is `5267f3639d6ce5a86db4c7d32e0d23d034d1e7d6` (`dev/ceremony-record.md`). It is the one commit on top of X = `000b0e9a`. The page's checks pass: R1 (the only parent is X), R2 (only the record changed), R4 SAME, E5 SAME twice, and E1/R3 (the launcher and packet digests equal the record's).

I am a fresh same-vendor session that wrote nothing in the range; this is a statement, nothing checks it.

## What I verified (sterile git, at X)
- The packet hashes to `374b18cd...7cada` and the launcher to `c9079ff5...12304`.
- All 11 `member` digests equal the blobs at X, and `artifact_sha256` equals `bootstrap/reanchor.sh`.
- The launcher is the template with the packet digest in its one slot (`cmp` SAME). As a control, a zero digest in the slot gives DIFFERENT.
- All 11 closure blob ids at X equal the anchor's, so 0 of 11 differ.

## What I read
- `git diff 2433453c X` changes six files, all mode 100644: three prose files, the record (the previous reader's), and the two AST fixtures. No code or test changed.
- **The AST pin.** The baseline goes from 173 to 169 keys. The 4 deleted keys are exactly the four `_ONBOARDING_*` constants that `dev/plans/archive/install-time-onboarding.md` names. `fa86e2cb` removed them from `install.py`: they are present in its parent and absent at X. The other 21 entries change only `digest` and `span`. Known-new has 23 added, 7 rekeyed and 4 dropped. The fixture digests equal the builder's (`ce501a09...`, `6e8c03dd...`).
- **The AST checks**, in a detached worktree of X with Python 3.13.13 (worktree now removed):
  - `verify --known-new` ends "AST attestation OK" for 169 symbols.
  - `test_ast_attest.py` gives 30 passed.
  - Control: the parent's fixtures make verify exit 1.

## The scan (the checker's own `range_review_report`, rendered by the Python inside `reanchor.sh`)
- Anchor to X: **0 hits** and 0 paths line-scanned. Not line-scanned: 4 outside coverage, 1 frozen, 1 cascade-mutable. The report says the anchor's checker made it.
- The scan digest is `dbac70a6980522636d511a551b9c9860b8c030b8a1f1a63a093201ecbe0c46f6`. It is the same over anchor to the record commit, because the record file was already in the range. **E7 should print this.**
- Control: I added `subprocess.run(cmd, shell=True)` to `scripts/repin.py` in a scratch clone and committed it there. The scan fired with 2 hits (process-start, shell-true). The clone is deleted.

## Surprising
1. `000b0e9a`'s commit message is only a subject line. It has no body, no verification snapshot and no Co-Authored-By line.
2. The scan classes the two fixtures differently: the baseline is cascade-mutable (role "other") and known-new is frozen (role "pinned"). Neither is line-scanned, because both are JSON.
3. The intent hook warned that no claim was held. It did not block.

Not done: no full test suite, no launcher run, no `repin` run, no signing and no key access.
