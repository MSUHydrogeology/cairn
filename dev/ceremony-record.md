# Independent engine-pin read -- v0.8.1

## Foundations

1. **Should this happen as framed?** Yes, as an engine pin only. Every one of
   the 6 changed baseline symbols, 5 rekeyed and 26 added known-new symbols
   traces to a commit under reviewed work: defect arc B (upgrading), defect
   arc E (the documentation plan moves), the Windows installer containment
   fix and its Security Review, or the Maintainer's recorded decision to raise
   the Git history read cap (`b7e62006`). The one lock row records a file the
   engine already installs. -- `dev/plans/archive/2026-11-20-defect-arc-b-upgrading.md`,
   `dev/plans/archive/2026-11-20-defect-arc-e-documentation-plan-moves.md`,
   `dev/measurement/windows-installer-containment-security-review-2026-11-22.md`.
2. **Best alternative.** Use the maintained `repin.py package` /
   `apply-reviewed-pin` / `commit-reviewed-pin` path; no new machinery. Not
   pinning leaves the AST gate failing on symbols that were reviewed, and
   leaves the rekeyed rows (which the baseline gate cannot see) unrecorded. --
   `release/REANCHOR_RUNBOOK.md` > "Preparing reusable inputs".
3. **What would show it wrong?** A member, packet, launcher or transaction byte
   differing from the read commit; a transaction preimage that is not the
   committed file; a changed row beyond digest and span; a removed key; a
   symbol whose introducing commit is under no reviewed work; a helper pin that
   does not equal the helper's bytes. Raw-object comparisons below challenged
   each. -- `git cat-file`, `shasum -a 256`, `diff`, `git log -S/-G/-L`,
   `git verify-commit`, `ssh-keygen -l`.

**Reader/model:** Claude Opus 5.5 (`claude-opus-5-5`), independent ceremony
reader; fresh reader, not the author of any of this code. **Date:** 2026-11-23.
**Elapsed at record:** under 30 minutes (the shell clock read 2 minutes at
drafting, which I do not trust; see Not covered). **Tokens:** unknown.

**Verdict: ACCEPT -- engine pin only. Blocking findings: none.** This record
grants no agent authority to sign, move refs, apply the pin or release.

## Checks made (all plain commands, run in `/private/tmp/cairn-trusted`)

1. **Read commit.** `git rev-parse HEAD` gives `5f8825ab...9c39`; `git status
   --porcelain` printed nothing; `git for-each-ref refs/replace` printed
   nothing; `git merge-base --is-ancestor 5ca6b38c... HEAD` succeeds. The prior
   anchor `5ca6b38c` verifies (`git verify-commit` with a signers file holding
   only HEAD's `dev/.cairn/allowed_signers`): Good signature, key
   `SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM` (`ssh-keygen -l` of
   that one-line file gives the same fingerprint).
2. **Packet, launcher, transaction.** `shasum -a 256` gives packet
   `6c6e5256...707e`, launcher `cd3fac8b...02bf`, transaction
   `202fbab9...2a50`; all three equal the reader inputs. `diff` of
   `git show HEAD:release/reanchor-launcher.template.sh` against the launcher
   shows one changed line, line 35: `@PACKET_SHA256@` replaced by the packet
   digest. The packet's 12 member lines and its `artifact_sha256` for
   `release/reanchor.sh` equal what I computed.
3. **Members.** `git cat-file blob 5f8825ab...:<path> | shasum -a 256` for all
   12 paths, then `diff` against the 12 `member` lines of the reader inputs:
   identical.
4. **The transaction, read whole.** Schema `repin-ast-transaction/v1`; `head`
   is the read commit, `anchor` is `5ca6b38c`; `reviewed_deletions` is empty;
   38 summary lines (6 + 31 + 1). For each of the three outputs, the
   `preimage_blob` equals `git rev-parse HEAD:<path>` and the
   `preimage_sha256` equals `git cat-file blob HEAD:<path> | shasum -a 256`;
   each `new_text` hashes to its `new_sha256`. Comparing old and new parsed
   contents:
   - `scaffold_ast_baseline.json`: 169 keys before and after, none added or
     removed; exactly the 6 named keys differ, and only in `digest` and `span`
     (`_MODULE_MAPPINGS` in `digest` only; its span is unchanged).
   - `scaffold_ast_known_new.json`: 173 keys to 199; none removed; exactly
     the 5 named keys change digest; exactly 26 keys are added, the 26 listed
     in the table below.
   - `cairn-lock.yml`: the comment header and every top-level field other than
     `files` are identical; `files` goes from 74 to 75 rows; no row removed or
     altered; the one added row is `.gitattributes`, `src core/gitattributes.txt`,
     verbatim, hash and base hash `sha256:3845da5f...607f`.
   - **The `.gitattributes` row.** `src` is relative to `templates/`, like
     every other row (there is no `core/gitattributes.txt` at the repository
     root). `git cat-file blob HEAD:templates/core/gitattributes.txt | shasum -a 256`
     gives `3845da5f...607f`, equal to the row; `cmp` with the committed root
     `.gitattributes` reports the same bytes. The engine has installed this
     mapping since `c139612b` (in `_SKILLS_MAPPINGS`, `install/_scaffold/config.py`
     937, before the last pin `ed893f0d`; the source file came from `ac76f0c8`,
     "the accepted Git attributes plan"); the root file arrived with arc B C1
     (`68dc7726`). The row records Cairn's own install of it.
5. **Tracing.** Last pin: `git log -1 -- tests/fixtures/scaffold_ast_baseline.json`
   gives `ed893f0d`. Since then 17 commits touch `install/_scaffold/`. I found
   each symbol's introducing commit with `git log -S<name>`, the commits that
   touch each changed body with `git log -L<start>,<end>:<file>` (spans from
   the transaction, which I matched to the `def` and last `return` lines at
   HEAD), and read `git diff ed893f0d HEAD` for `cli.py`, `config.py`,
   `install.py`, `lockfile.py`, `__init__.py` and all 785 lines of the
   `upgrade.py` diff.
6. **Helper pin.** `_GIT_READ_SHA256` is in `install/_scaffold/lockfile.py` 52
   and equals `e29f3893...5a7a`. `git cat-file blob HEAD:dev/tools/git_read.py`
   and `HEAD:templates/skills/_lib/git_read.py` both hash to `e29f3893...5a7a`.
   `git log -G` shows only `b7e62006` changed that line since the last pin,
   and its diff there is the one digest (with `HISTORY_MAX_BYTES` 64 to 256 MiB
   in `git_read.py`, the reason for the new digest). The lock's
   `dev/tools/git_read.py` row carries the same hash.

### Changed baseline symbols (diff since `ed893f0d`)

| Symbol | Commits | Logic or motion |
|---|---|---|
| `Assign:_MODULE_MAPPINGS` (config.py) | `5d34f839` Plan E C1; `9dcb802b` arc B C3 (comments only) | Logic, one value: the documentation plan installs to `dev/DOCUMENTATION_PLAN.md` instead of `docs/`. Other edits are comments. Nothing surprising. |
| `FunctionDef:_cmd_finalize_lockfile` (upgrade.py) | `21667cd9` arc B C5; `029532a0` arc B review fixes | Logic: skips a wrapper retired on purpose; drops `adopter_deleted` when the file is back. Nothing surprising. |
| `FunctionDef:_compute_upgrade` (upgrade.py) | `21667cd9`; `029532a0` | Logic: a retired wrapper plans as up-to-date; missing-wrapper messages name `--retire-wrapper`. Nothing surprising. |
| `FunctionDef:cmd_upgrade` (upgrade.py) | `68dc7726` C1, `df96fe64` C2, `bfaaabb3` C4, `21667cd9` C5, `031ef837` Plan E C2 | Logic: three new options wired in, mutually exclusive with the others, refused with `--to`, behind the same profile-link refusal; helper-binding message; report lines. Nothing surprising. |
| `FunctionDef:_emit_skill_copy_fallback` (install.py) | `a3435faa`; `92844ae1` (Security Review N1) | Logic, security-bearing: Windows-only link and junction refusals; no new call on Mac or Linux. Read in full; matches the commit message and the Security Review. |
| `FunctionDef:main` (cli.py) | `68dc7726` arc B C1 | Logic, message only: the "harness folder missing" line now names the folder and says what to run. Nothing surprising. |

### Rekeyed known-new rows (invisible to the baseline gate)

| Symbol | Commits | What changed |
|---|---|---|
| `Assign:_GIT_READ_SHA256` (lockfile.py) | `b7e62006` | New helper digest; checked in 6. |
| `Assign:_MODULE_DISCOVERY` (config.py) | `5d34f839` Plan E C1 | One string, `docs/` to `dev/DOCUMENTATION_PLAN.md`. |
| `FunctionDef:_layout_command` (upgrade.py) | `df96fe64`, `bfaaabb3`, `21667cd9`, `031ef837` | New options counted as mutating; a heal hint after a layout apply. |
| `FunctionDef:_layout_plan` (upgrade.py) | `df96fe64`, `9dcb802b`, `21667cd9` | Stops writing the three layout lock keys; shallow-clone block text; a retired wrapper is not adopted; ancestry is also proved when a verbatim file's live bytes equal the historical blob (this is arc B C3's stale-hash fix, written in the plan at line 80). |
| `FunctionDef:_layout_target` (upgrade.py) | `68dc7726` | Gives the helper-binding refusal text before the old message. |

### Added known-new rows

| Commit (work) | Symbols |
|---|---|
| `68dc7726` arc B C1 | `_GIT_READ_CRLF_TEXT`, `_GIT_READ_OTHER_TEXT`, `_git_read_binding_refusal`, `_git_read_helper_path`, `_git_read_plain_bytes` |
| `df96fe64` arc B C2 | `_LAYOUT_LOCK_KEYS`, `_cmd_heal_layout`, `_layout_heal_findings` |
| `9dcb802b` arc B C3 | `_cairn_git_is_shallow` |
| `bfaaabb3` arc B C4 | `_layout_heal_rendered` |
| `21667cd9` arc B C5 | `_NOT_A_VENDOR_WRAPPER`, `_cmd_retire_wrapper`, `_wrapper_record_fits`, `_wrapper_retired` |
| `031ef837`, `f7b644c3` Plan E | `_DOCPLAN_NEW`, `_DOCPLAN_OLD`, `_DOCPLAN_SRC`, `_DOCPLAN_STEPS`, `_DOCPLAN_NOTE`, `_cmd_documentation_plan_moved`, `_documentation_plan_move_lines` |
| `a3435faa` Windows containment | `_ON_WINDOWS`, `_is_redirect`, `_link_in_path`, `_created_elsewhere`, `_remove_created` |

Both plans are archived, heavy tier, with a usual review and a Security Review
at plan and code stage recorded in the plan files. Plan E's later wording
commits (`e6b7caae`, `f7b644c3`, `3434491f`) precede its code reviews
(2026-11-21, 14:26 onwards); `e20f1ef7` and arc B's `029532a0` are the
responses to those reviews.

### Security-bearing symbols, and whether I read them

All read in full in the diff:
- **Path containment and link or junction refusal, temporary-file races
  (Windows):** `_emit_skill_copy_fallback`, `_ON_WINDOWS`, `_is_redirect`,
  `_link_in_path`, `_created_elsewhere`, `_remove_created`.
- **Helper-hash pinning:** `_GIT_READ_SHA256`; and the diagnostics beside it,
  `_git_read_binding_refusal`, `_git_read_helper_path`, `_git_read_plain_bytes`
  (these only choose which refusal text to print; they never run or bind the
  bytes they read).
- **Containment before reads and writes in new commands:** `_cmd_heal_layout`,
  `_layout_heal_rendered`, `_cmd_retire_wrapper`, `_cmd_documentation_plan_moved`
  (each calls `_assert_safe_write` before reading or writing a project path).
- **Integrity decisions:** `_wrapper_retired`, `_wrapper_record_fits` (decide
  when an absent wrapper is accepted), `_layout_plan` (the ancestry proof),
  `_cairn_git_is_shallow` (runs Git only through the pinned helper).

## What the change does, in plain words

- **AST baseline (6 rows):** six existing installer functions changed; the pin
  records their new fingerprints and line positions. No symbol added or
  removed.
- **AST known-new (5 changed, 26 added):** the pin records the new commands
  `upgrade --heal-layout`, `--retire-wrapper` and `--documentation-plan-moved`,
  the clearer messages for a Windows line-ending clone and a shallow clone,
  the Windows link refusals in the skill copy, and the new helper digest.
- **Install lock (1 row):** Cairn's own lock now records the root
  `.gitattributes` it already has.
- Nothing looked surprising for these three pieces of work.

## Non-blocking findings for the Maintainer

- **The new lock file is re-sorted.** The new text lists all 75 rows in
  `dst` order; the committed file is not in that order. A plain `git diff`
  after apply will show many moved lines. Parsed, it is exactly one added row
  and nothing else changed (check 4).
- **The Windows fix had a code change after its Security Review.** `92844ae1`
  (the N1 fix) and `4581eb59` (comments) followed the review; the response is
  recorded (`aea41ef2`) but there is no later review pass. I read the change:
  it only adds a refusal condition (the open file must be the entry at the
  temporary name). The original fix ran under the defect-fix rule on the
  Maintainer's chat words, with a Security Review rather than a plan.
- **`b7e62006` has a recorded Maintainer decision but no review.** Its only
  engine change is the one digest, which I checked against both helper copies.
- **The brief named the layout plan for arc B.** The arc B symbols are under
  `dev/plans/archive/2026-11-20-defect-arc-b-upgrading.md` (defect arc B), not
  `2026-11-17-repository-layout.md`.
- **`_git_read_plain_bytes` looks, then opens.** A link put in between could
  change which refusal message prints. It never runs or trusts the bytes, so
  this affects only the message.

**Covered:** read commit, cleanliness, replace refs, ancestry and the prior
anchor's signature; packet, launcher (and its template diff) and transaction
digests; all 12 members; the whole transaction, including preimages, new-text
digests and a parsed comparison of all three outputs; the `.gitattributes`
source and root bytes; the trace of every changed, rekeyed and added symbol;
the full engine diff since the last pin; the helper pin against both copies.
**Not covered:** I did not recompute any AST digest or span (that needs the
engine's own code, which I may not run), so the fingerprints themselves rest on
`repin.py package`; I matched the spans only to `def` and last lines. I did
not run any test, `repin.py` or `claim_check.py` (outside my allowed commands),
or read members' bodies beyond their digests, or judge release readiness,
certification, host containment or key-away state. I did not check every
caller of `fan_out_skills` behind the `next(...)` lookup in `main`. The elapsed
time is an estimate.

## Protocol Data

read-commit 5f8825abad1ce13989e6d166852af29c959ff39c
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
ast-transaction-sha256 202fbab9d902e144dace1690ee3266d102a7e258b007c34fc0d4d3dfff922a50
