# Independent signing read -- v0.8.1 engine pin re-sign

## Foundations

1. **Should this happen as framed?** Yes, as an ordinary re-sign only. The
   one change since the anchor that the signed manifest cares about is the AST
   pin commit `c89c9ba1`, and its three files are byte-for-byte the outputs of
   the pin transaction the previous reader accepted (`a11b704e`). None of the 12
   trust-root members changed since the anchor. -- `git show a11b704e:dev/ceremony-record.md`,
   `/private/tmp/cairn-ceremony/p2/ast-pin-transaction.json`.
2. **Best alternative.** None better: the maintained ordinary ceremony with the
   builder's packet and launcher. Not re-signing leaves the gate manifest
   disagreeing with the pinned known-new file. -- `release/REANCHOR_RUNBOOK.md`
   > "The card", "Preparing reusable inputs".
3. **What would show it wrong?** A commit between the anchor and HEAD other
   than the three expected; a pinned file whose bytes differ from the
   transaction's output; a lock change beyond the one `.gitattributes` row; a
   member, packet or launcher digest differing from the read commit or the
   reader inputs; a values-file path that is a link, names another checkout or
   key, or points at an existing package. The checks below challenged each. --
   `git`, `shasum -a 256`, `ssh-keygen -l`, `diff`, `sort`, `grep`, `ls -ld`.

**Reader/model:** Claude Opus 5.5 (`claude-opus-5-5`), independent ceremony
reader; fresh reader, not the author of any of this code. **Date:** 2026-11-23.
**Elapsed at record:** about 3 minutes by the shell clock (12:18 to 12:21 EST).
**Tokens:** unknown.

**Verdict: ACCEPT -- ordinary re-sign at `c89c9ba1`. Blocking findings: none.**
This record grants no agent authority to sign, move refs, push or release.

## Checks made (plain commands only, run in `/private/tmp/cairn-trusted`)

No Python, no script, no `repin.py` subcommand, no test and no candidate code
was run.

1. **Read commit and anchor.** `git rev-parse HEAD` gives `c89c9ba1...1bf69`;
   `git status --porcelain` and `git for-each-ref refs/replace` print nothing;
   `git merge-base --is-ancestor 5ca6b38c... HEAD` succeeds.
   `dev/.cairn/allowed_signers` holds one line; I copied it alone to a scratch
   file and ran `git -c gpg.ssh.allowedSignersFile=<that file> verify-commit 5ca6b38c...`:
   Good "git" signature, ED25519 key
   `SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`. `ssh-keygen -l -f
   dev/.cairn/allowed_signers` gives the same fingerprint, which is the one the
   Maintainer supplied in chat.
2. **History since the anchor.** `git rev-list --parents -n1 HEAD` shows
   `c89c9ba1` with the single parent `a11b704e`. `git log --oneline 5ca6b38c..HEAD`
   lists exactly three commits: `c89c9ba1` (AST pin), `a11b704e` (engine-pin
   record), `5f8825ab` (board). Nothing else. `git diff --stat a11b704e HEAD`
   lists exactly `dev/.cairn/cairn-lock.yml`,
   `tests/fixtures/scaffold_ast_baseline.json` and
   `tests/fixtures/scaffold_ast_known_new.json`.
3. **The pin equals what was accepted.** The transaction file hashes to
   `202fbab9...2a50`, the digest in the previous record.
   - **Whole-file check.** For each of the three files,
     `git cat-file blob HEAD:<path> | shasum -a 256` equals that file's
     `new_sha256` in the transaction (lock `d1730e5b...fdd5`, baseline
     `5f5a8aaa...4fb0`, known-new `8b311ac4...fa3e`), and the same at
     `a11b704e` equals its `preimage_sha256` (`5dd84efb...5c15`,
     `e7b9567c...d827`, `96391241...e8c9`). So the commit wrote exactly the
     bytes the earlier reader accepted, onto exactly the files that reader saw.
   - **Baseline, row by row.** `git diff a11b704e HEAD` on the baseline shows
     six keys changed, each matching the `to` side of the transaction summary:
     `_MODULE_MAPPINGS` digest `f17e8fad31f012d9`, span 1040-1431 unchanged;
     `_cmd_finalize_lockfile` `f600b25d52b60371` 2952-3151; `_compute_upgrade`
     `b5299f1f4f296fa5` 891-1331; `_emit_skill_copy_fallback`
     `6137565cf459a7c7` 901-1095; `cmd_upgrade` `5b6abdabbf526668` 5025-5520;
     `main` `91b0f73ba5acd74f` 192-834. Nothing else changed.
   - **Known-new.** 26 added keys (counted with `grep -c '^+  "'`), 0 removed
     (`grep -c '^-  "'`), 5 rekeyed (`_GIT_READ_SHA256` `6120c373a914b44f`,
     `_MODULE_DISCOVERY` `e5cb1cbc0d063706`, `_layout_command`
     `c670bb4f79cb29d6`, `_layout_plan` `e2c77d071e535cde`, `_layout_target`
     `2ebb6608bd374ca7`). Every added key and digest equals a summary row.
   - **Lock.** I sorted the old and new lock text line by line and compared:
     the only difference is 7 added lines, which together form one row
     (`dst .gitattributes`, `src core/gitattributes.txt`, verbatim, hash and
     base hash `sha256:3845da5f...607f`). Line count goes 575 to 582 and the
     `"dst":` count 74 to 75. The large raw diff is re-sorting only.
     `git cat-file blob HEAD:templates/core/gitattributes.txt` and
     `HEAD:.gitattributes` both hash to `3845da5f...607f`.
4. **Packet and launcher.** `shasum -a 256` gives packet `6c6e5256...707e`
   and launcher `cd3fac8b...02bf`; both equal the reader inputs. `diff` of
   `git cat-file blob HEAD:release/reanchor-launcher.template.sh` against the
   launcher shows one changed line, line 35: `@PACKET_SHA256@` replaced by the
   packet's own digest. The packet's `artifact_sha256` equals the
   `release/reanchor.sh` member digest.
5. **Members.** `git cat-file blob HEAD:<path> | shasum -a 256` for all 12
   paths; `diff` against the 12 `member` lines of the reader inputs and of the
   packet: identical. `git diff --stat 5ca6b38c HEAD -- <the 12 paths>` prints
   nothing; the same command with `dev/ceremony-record.md` and the known-new
   file added does list those two, so the empty result is a real negative.
6. **Values file** (`/private/tmp/cairn-ceremony/ceremony-values-3`, 13
   lines, `shasum -a 256` `423e2c6f...a6de`, equal to the builder's printout).
   Every path is absolute; `ls -ld` shows none is a symbolic link, nor is any
   parent folder I listed. `checkout` is `/private/tmp/cairn-trusted`.
   `signing_key` `/Users/kendal30/.ssh/cairn_signing.pub` is a regular file;
   `ssh-keygen -l` gives `SHA256:8R549gtP...ESsM`, and its key text equals the
   roster line's. `package`
   `/private/tmp/cairn-ceremony/p3/authorization-package-8293a118e2073d1520a601dd251a657c.json`
   is inside `p3/` and does not exist yet. `python`
   `/Users/kendal30/conda_envs/lhm/bin/python3.13` is a regular file hashing
   to `a0e58d65114a537560a551b09d5a3c2d06f6c3a199d9ed819138080cd58ddf3e`,
   equal to the first signing's record (`a0e58d65...df3e`) and to
   `python_sha256` in `verifier-2/verifier-evidence.json`. `git`
   `/opt/homebrew/Cellar/git/2.53.0/bin/git` is already a regular file (no
   link to follow), hashing to
   `5e5a622e407fb7deb74173cab9e47ff214952cc6bfcd036449cf9edbaa305537`. `env`,
   `mktemp`, `mkdir`, `shasum`, `sort`, `cat` are regular system files under
   `/usr/bin` or `/bin`; `home` is `/Users/kendal30`, a directory.

## What the change does, in plain words

- The engine (the installer code) was pinned in the previous step: its AST
  fingerprint files and Cairn's own install lock were updated, reviewed by the
  previous reader and committed as `c89c9ba1`.
- One of those files, the known-new list, is a file the signed gate manifest
  freezes. So the manifest must be re-signed to match it. That is all this
  ceremony does.
- **The signing will cover:** a new signed manifest at the read commit, whose
  member digests are the 12 listed below (unchanged since the anchor) and
  whose frozen files now include the pinned known-new file.
- **The signing will not cover:** any review of the 12 members beyond their
  digests (they are byte-identical to the last signed anchor); any new review
  of the pinned symbols (that was the previous reader's job, and I checked
  only that the commit matches what they accepted); publication.

## Non-blocking findings for the Maintainer

- **The packet and launcher are the same files as in the pin step.** `p2/` and
  `p3/` hold byte-identical packets (`6c6e5256...707e`) and launchers
  (`cd3fac8b...02bf`). That is expected: the packet binds the 12 members,
  which did not change; it names no commit. The read commit is bound by this
  record and by the driver requiring it at `HEAD`.
- **The new anchor's net change will show the three pinned files.** At the
  card's step 5 (just before Summary 2) expect the lock, baseline and
  known-new files; the lock's text diff looks large because it was re-sorted.
  Their digests at the read commit are in check 3.
- **I took "the known-new file is frozen" from the brief.** I saw it listed in
  `tests/_gate_manifest.py` (line 144, the `ast-attest-verify` command) but did
  not trace the manifest's frozen-file list in code.

**Covered:** read commit, cleanliness, replace refs, ancestry and the prior
anchor's signature against the one-line roster; the three commits since the
anchor; the pin commit's three files against the accepted transaction (whole
file and row by row); packet and launcher digests and the launcher's template
diff; all 12 members, and that none changed since the anchor; every line of
the values file, its paths, links, key fingerprint, Python and Git digests.
**Not covered:** I ran no verifier collection, no test, no `repin.py`
subcommand, no `--check-only` and no `claim_check.py` (outside my allowed
commands). I did not read members' bodies, recompute AST fingerprints, or
re-review the pinned symbols. I did not judge host containment, key-away
state, release readiness or the contents of Python's library folder. The
commit holding this record is not signed by me and is not checked here.

## Protocol Data

read-commit c89c9ba17ae9370ae06c700c59825ce1bdc1bf69
prior-anchor 5ca6b38c7e9aff39d8619277297d6ab1663f66df
packet-sha256 6c6e5256327da7df5b635d2c9cdc3d39cb9ea38c833f3ee8801776a9f5fc707e
launcher-sha256 cd3fac8b87b0c21bf947a5a3c36f52025e62ddb0dbbd09dbd2c2aee267cc02bf
member 8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242 dev/.cairn/allowed_signers
member 3f0374068fc8ba736cbd365bc97302e60a1c46f51b6edec4bd6d952d85f7fb40 release/REANCHOR_RUNBOOK.md
member a9f437fa1d17d9d1595370c7380250d9263ebc38eb3e574cc6995de100baee7c release/reanchor-launcher.template.sh
member e41010d0c9dad22b2ea0d456e2cb6c745daa284a58284c628d226daf802c0be0 release/reanchor.sh
member 79b58258bff21794a5f73d2258ba1608d717b8d0a97dd7bcebbdc684b5ebdb9f tests/_gate_manifest.py
member 50479b661dcde4cfd7536f8d836f1c0bef3a01434e7cdf91894324ae2cf9650e tests/_gate_preflight.py
member 46a0bfe407e501e9cb277f455722c739aef4bc60bd78d7092431c59dd133348d tests/_gate_reanchor.py
member 495ecbab9fb5bbd2607434d880796a9f81f6e2308d82207ac972f5db6a0ae397 tests/_gate_transition.py
member 3fb76b01ee92f7b24c1b90a3fe7defbea5abc14eb5d64d9c4c8937ccd52f22da tests/_oracle.py
member 4afb36485d00f5f4cdf09155f7c50f80eed69c779a2b33e357e11dfd85abea27 tests/_oracle_activation.py
member 725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42 tests/_oracle_trust.py
member 098734196db5962be8a11850c7481abdf8a52d53cd0f1b0d7e177305356f82e6 tests/fixtures/protected_test_roster.json
