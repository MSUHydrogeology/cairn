# Independent transition packet read -- v0.8.1

## Foundations

1. **Should this happen as framed?** Yes, as a layout transition only. The
   eleven changed authority files trace to the path relocation from
   `bootstrap/` to `release/` and `tests/`, or to the accepted layout plan's
   transition mode. Since the v0.8 read at `ed893f0d`, only two members moved:
   the runbook (the card and the reader's pinned-digest paragraph) and
   `tests/_gate_preflight.py` (restores the new-file scan under `tests/`,
   commit `9c20accb`; it widens the scan, so it is stricter). --
   `dev/plans/archive/2026-11-17-repository-layout.md` > "Layout transition".
2. **Best alternative.** Use the maintained `ceremony --transition` with layout
   evidence; no new machinery. Leaving the anchor at P keeps the old layout
   unsigned. -- `release/REANCHOR_RUNBOOK.md` > "First cut after the layout move".
3. **What would show it wrong?** A member, roster, launcher or pinned-file byte
   differing from raw C; a net-change text that does not hash to the stated
   digest; a P signature not by the confirmed key; a values-file path that is a
   link or names the wrong checkout or key. Raw-object comparisons below
   challenged each. -- `git cat-file`, `shasum -a 256`, `git verify-commit`,
   `ssh-keygen -l`.

**Reader/model:** Claude Opus 5.5, independent ceremony reader; fresh reader,
not the code author. **Date:** 2026-11-23. **Elapsed at record:** approximately
15 minutes. **Tokens:** unknown.

**Verdict: ACCEPT -- transition packet only. Blocking findings: none.** This
record grants no agent authority to sign, move refs or release.

## Checks made (all plain commands, run in `/private/tmp/cairn-trusted`)

1. **Packet and launcher.** `shasum -a 256` of `c1/authorization-packet.txt`
   gives `6c6e5256...707e` and of `c1/reanchor-launcher.sh` gives
   `cd3fac8b...02bf`; both equal the prepared inputs. `diff` of
   `git cat-file blob C:release/reanchor-launcher.template.sh` against the
   launcher shows exactly one changed line, line 35: `@PACKET_SHA256@` replaced
   by the packet digest. The template has only that one slot.
2. **Members.** `git cat-file blob C:<path> | shasum -a 256` for all 12 equals
   the packet and reader inputs. Old paths came from `layout-paths.json` in
   `verifier-2` (`bootstrap/...` to `release/...` or `tests/...`). At P, 10
   members differ in content; `tests/_oracle_trust.py` has the same bytes as
   P's `bootstrap/tests/_oracle_trust.py` but a new path, which is why the tool
   counts 11 of 12 as changed; `dev/.cairn/allowed_signers` is the same blob
   (`55f821dc`) at P and C. It holds one line, one ED25519 key, and
   `ssh-keygen -l -f` gives `SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`,
   the fingerprint the Maintainer typed in chat on 2026-11-23.
3. **repin.py and Python.** `git cat-file blob C:release/repin.py | shasum -a 256`
   gives `7a4c92d7...fc6e`; `shasum -a 256` of
   `/Users/kendal30/conda_envs/lhm/bin/python3.13` gives `a0e58d65...df3e`.
   Both equal `preparer_sha256` and `python_sha256` in
   `verifier-2/verifier-evidence.json`, whose own digest is the layout evidence
   digest `23e77384...59a9`.
4. **P.** `git verify-commit` with `gpg.ssh.allowedSignersFile` set to a file
   holding only P's one-line roster: Good signature, key
   `SHA256:8R549gtP...ESsM`. `git merge-base --is-ancestor P C` succeeds.
   `git for-each-ref refs/replace` lists nothing; `.git/refs/replace` is absent.
   Working tree clean before the edit.
5. **Values file.** 13 lines, `shasum -a 256` gives `8a77bf92...92f0`, equal to
   the tool's printout. Every path is absolute and none is a link. `checkout`
   names `/private/tmp/cairn-trusted` (a directory). `signing_key` is
   `/Users/kendal30/.ssh/cairn_signing.pub`, a regular file whose
   `ssh-keygen -l -f` fingerprint is the confirmed one. `python` is the
   interpreter checked in 3. `git`, `env`, `mktemp`, `mkdir`, `shasum`, `sort`,
   `cat` are regular files; the `git` file's digest `5e5a622e...5537` equals
   the tool's (the tool reached it through the `/opt/homebrew/bin/git` link).
6. **Pinned files and net change.** I read all 203 lines of the net change.
   `git cat-file blob C:<path> | shasum -a 256` for the three pinned files
   equals the prepared lines. The net change text is lines 65 to 267 of
   `prepare-reader-output.txt`: the 203 lines after the tool's
   "203 lines follow." header and before its first pinned line, each ending in
   a newline. `sed -n '65,267p' | shasum -a 256` reproduces `858a0deb...01ae`.

**What the net change does, in plain words.**
- The install lock (103 rows): the 18 old `scripts/` rows and 15 old `tools/`
  rows are dropped; 35 `dev/tools/` rows are added (those 33 plus two new
  tools, `code_map.py` and `pulse.py`). `RULES.md` and `dev/DOCUMENTATION_PLAN.md`
  rows are added; `docs/DOCUMENTATION_PLAN.md` is dropped. 31 installed doc,
  skill and config rows get new content hashes. The module list gains
  `architecture-review`; the header's reference moves from
  `bootstrap/UPGRADE.md` to `install/UPGRADE.md`; `CLAUDE.md` gains
  `layout_keep`. No row at C still names `scripts/` or `tools/`.
- AST baseline (27 rows): every row is an existing installer symbol whose
  digest and line span changed; none added or removed.
- AST known-new (70 rows): mostly new symbols (layout move, transaction and
  receipt helpers) plus some changed digests; none removed.
- Nothing looked surprising for a layout-move release.

## Non-blocking findings for the Maintainer

- The packet itself states no `repin.py` or Python digest; those are stated in
  the layout evidence (`verifier-evidence.json`), which the packet flow binds
  by its digest. Checked there.
- The lock's `test_command` is still `python -m pytest bootstrap/tests` at P
  and C (unchanged by this net change). Stale after the layout move; worth a
  later fix, not a ceremony matter.
- Values file: `checkout` and `home` are directories, and `package` does not
  exist yet; both are by design (a fresh package path).
- The prepare-reader header reports "prior static verification HOLD"; the
  prior verifier's HOLD dispositions are the Maintainer's.

**Covered:** packet, launcher, values file, Python and repin digests, members,
signers file, P signature and ancestry, replace refs, the three pinned files
and the whole net change text, the `_gate_preflight.py` diff since the v0.8
read. **Not covered:** line-by-line review of the other members beyond their
digests, the HOLD dispositions, full certification, release readiness, host
containment, key-away state, executing any test or any `repin.py` subcommand.

## Protocol Data

read-commit 7467933dd2e30c9ae597b4d0a47e344ebc8a1c55
prior-anchor e5b7fd0adb0b6d0402e89e2789f57c5f42045e62
packet-sha256 6c6e5256327da7df5b635d2c9cdc3d39cb9ea38c833f3ee8801776a9f5fc707e
launcher-sha256 cd3fac8b87b0c21bf947a5a3c36f52025e62ddb0dbbd09dbd2c2aee267cc02bf
layout-evidence-sha256 23e77384891946276c6ffdea2cae5b650300483fcd2ad73fe830e72ee19a59a9
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
pinned-sha256 e7b9567ce7d6e5d62713f0312e9ed4be45940ec65757bb15a9b5d1934543d827 tests/fixtures/scaffold_ast_baseline.json
pinned-sha256 96391241ef21a5721f6f5320f3671af9a5e06b6f71be60d3392aa1b6f87be8c9 tests/fixtures/scaffold_ast_known_new.json
pinned-sha256 5dd84efbb02047de4174af0c21de5a016f4d5045d341ef5cb6b887500bd25c15 dev/.cairn/cairn-lock.yml
net-change-sha256 858a0debb43eedfc619926d0c01269505f29566e185ec8c5f6be35a2a10401ae
