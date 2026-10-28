# Scripts and records from the first two re-anchor ceremonies (2026-10-28)

Kept as evidence for the v0.6 rows "The ceremony as two commands: `reanchor` and `repin`" and
"First-ceremony page and report fixes" in `dev/PLANNING.md`. The Maintainer's point, 2026-10-28: the
ceremony should be a script they run, confirming shas and typing a passphrase, not a page of commands
they type. These scripts are a working draft of that, written during the ceremony.

Result: the first ceremony signed anchor `2433453c` and the second, the AST pin, signed anchor `443de20f` (both pushed; `repin status` runs; the gate manifest verifies 197 frozen files and 5479 pinned nodes).

What is here:

* `first-ceremony/`: the transition ceremony (the authority closure changed, so `repin` refused it).
  `precheck.sh` (the page's checks before stage 1), `stage1.sh`, `compare.sh` (the comparisons),
  `stage2.sh` (signing and the signature check), `push.sh` (one atomic push and a read-back),
  `build.sh` and `handoff.md` (the builder's packet and launcher), `reader-handoff.md`, the packet,
  the stage 1 `report.txt`, and the Maintainer's authorization.
* `second-ceremony/`: the AST-pin ceremony. The same scripts, reading the candidate and file names from
  `ceremony.env`, plus E7 (the anchor's own scan digest) and `H.txt`-based comparisons; `repin1.sh` and
  `repin2.sh` (the two `repin` attempts, the second stopped by a deletion `repin` will not pin); both
  readers' notes, the packet, `report.txt` and the authorization.
* `ast-correction/`: `ast_pin.py` (the one-off correction that reuses `repin package` in a scratch
  worktree, with its dry run, tests, `run.sh` wrapper and both notes).

What they are not: tested only on stand-in values files (with negative controls for `precheck.sh`),
never against the Maintainer's values file before the ceremony; they hard-code the two candidates and
digests; they name the Maintainer's home paths. Do not run them as they stand for a later ceremony.

What the ceremony showed, for the rows above: `repin ceremony` asks for a reader's record before it
writes an AST pin; it refuses to pin a deleted baselined symbol; a hand edit of the baseline makes a
later `repin ceremony` refuse; the stage 1 key probe waits 10 seconds for a declined passphrase prompt; the
page's `g` helper breaks in zsh when `g` is an alias; the Y1 to Y5 questions are read by no program.
