# Reader hand-off: second ceremony (the AST pin through `repin`)

**Conclusion.** Nothing is wrong, so I committed the record: `3b898213d8635f023c06883320e6a504c3d62ae0` (`dev/ceremony-record.md`), the one commit on top of `137264be` (X). The checks pass: R1, the parent is X; R2, only the record changed; R4 SAME; E5 SAME twice.

I am a fresh same-vendor session that wrote nothing in the range; this is a statement, nothing checks it.

## What I verified (sterile git, as the runbook's `g`, at X)
- Packet sha256 `374b18cd...7cada` and launcher sha256 `c9079ff5...12304`: re-hashed, equal to what `repin packet` printed.
- All 11 `member` digests equal the blobs at X. `artifact_sha256` equals `bootstrap/reanchor.sh` at X.
- The launcher is the template at X with its one slot filled by the packet digest (`cmp` SAME; a zero digest in the slot gives DIFFERENT). Its `EXPECTED_PATHS` lists the packet's 11 paths in the same order.

## What I read
- In full: `git diff 2433453c 137264be`. It is one commit changing three prose files (`CHANGELOG.md`, `dev/PLANNING.md`, the archived ceremony plan). All are mode 100644; no code, test, fixture or closure file changed.
- All 11 closure blob ids at X equal the anchor's, so `repin`'s "0 of 11 differ" holds.

## Scan (the anchor's own checker, in a detached worktree of X, since removed)
- anchor..X: **0 hits**, nothing line-scanned, 3 paths outside coverage. Scan digest `96077707095cb263be2529a0341f62c7d3add030c7c9d68614b640bee076b4e5`.
- Control: one commit in a scratch clone adding `subprocess.run(cmd, shell=True)` to `scripts/repin.py`. It fired with 2 hits (process-start, shell-true).
- **For E7**, use the digest over anchor..record commit, not the one above. The report covers the candidate, so the record file counts as a fourth path outside coverage. Measured: 0 hits, `5b7350e677dc9e64ce9e91aafe418cf41dc335963952461fc6843d2ce210bfd9`.

## Surprising
1. `ceremony2/ceremony-record.txt` (06:55) shows that `repin ceremony` had already started once at HEAD X, before my record existed. That run would have stopped at the paste or record check. It is harmless, but someone should know about it.
2. In zsh, `g` is an alias here, so the runbook's `g() {...}` does not parse. I ran it as a bash script.
3. The intent hook warned (no claim) and did not block.

Not done: no test suite, no Bandit run, no launcher or `repin` run, no key access.
