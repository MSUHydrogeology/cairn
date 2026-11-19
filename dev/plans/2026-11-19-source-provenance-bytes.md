# Verify installer source before treating it as clean

**Author**: Codex Sol (Implementation)
**Source proposal**: dev/proposals/archive/2026-11-19-codex-source-provenance-bytes.md
**Status**: ready-to-archive
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-19
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/conventions.md, dev/rules/working-agreements.md
**In brief**: Warn about a difference between tagged source and checkout bytes.

## Build summary

Add a bounded byte comparison to the installer's clean tagged checkout path. Revise its provenance guide and extend the existing warning tests. Keep the warning advisory and use the existing Git reader unchanged. Allow roughly 30 minutes for implementation and focused checks, with Windows setup and file-read cost as the main uncertainties.

## Source proposal

The Maintainer asked for this repair for v0.8 (`52505f38`). Both proposal reviews accepted the bounded direct comparison.

## Scope

Change `git_provenance_warning` in `install/_scaffold/install.py`, `install/PROVENANCE.md` and the existing public warning cases in `tests/test_manifest.py`. Reuse fixed operations through `_git_read_helper` and its `_checked_bytes` file reader. Leave the verified Git helper and install safety and signature gates unchanged.

Resolve `HEAD` via `rev-parse --verify HEAD` to a validated 40- or 64-character lowercase hex ID. Use it in the exact-match `describe` call. Preserve the existing status warning. On the otherwise silent path, canonicalize the absolute output of `rev-parse --show-toplevel` and require exact equality with canonical `cairn_root`; mismatch warns unavailable and repeat `rev-parse --verify HEAD` after comparison. Enumerate blobs with `ls-tree -r -z --full-tree <oid>`, capped at 8 MiB. Require a complete, nonempty, NUL-terminated listing. Parse all entries before opening files, accepting only supported regular modes, blob kind, lowercase hexadecimal at the selected ID width, and unique root-relative paths. Reject empty components, dot components, parent traversal, absolute or drive-relative names, backslashes, and Git administration names regardless of case. On Windows reject reserved names, device and stream syntax, trailing spaces or periods, and case-equivalent duplicates. Require strict real-path spelling to equal the validated path under Windows case normalization before any content read, so short-name aliases or redirected components cannot substitute another location. Keep the existing guarded read as a separate identity check.

Read each validated path using `_checked_bytes` with the smaller of 16 MiB and the remaining 128 MiB allowance. Compute the Git blob ID over its length header and bytes using the commit's hash format. A definite mismatch warns of changes; failed listing, read, validation or revision check warns evidence is unavailable. Warn without naming file contents or an untrusted path. Plain exports and `--allow-dev` keep their behavior.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Add installer comparison, warning guide and focused checks | Both plan reviews | Advisory tagged-source byte check |
| C2 | Verify on Mac and Windows, then resolve independent code reviews | C1 | Focused evidence and reviewed repair |

## Acceptance criteria

**C1.** Clean tagged source remains silent. Changed tracked bytes warn even if status reports clean, and an unavailable comparison warns. Existing dirty, untagged, export and development-override cases retain their outcomes. Nested sources warn unavailable because the enclosing Git root differs. Invalid names fail before any file content read. No new Git helper route, tool, or config.

**C2.** Run only the focused provenance cases on canonical Mac Python and native Windows Python. Record one elapsed check against a clean release-sized checkout, including byte count and runtime. Apply scoped prose gates, inspect expected AST drift and obtain ordinary and Security code reviews. The Maintainer's grouped re-anchor and final release checks remain separate.

## Scope delta

**Scope delta**: preserved.

## Verification

Map the three paths with `tests/tier_inventory.py`. Use `tests/test_manifest.py::TestProvenanceWarning` and the applicable document checks. Exercise raw bytes independently of reported status with a synthetic fixture and retain the clean control. Run no full suite here. Record interpreter, results and elapsed time, with tokens unknown if unavailable.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-19

Reviewed commit: dba989c6618f60636febda9a2414ea101a13f79f

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** The bounded comparison and controls deliver the accepted repair, but the source-root binding needs an explicit equality check (finding below). -- plan Scope and C1; accepted proposal, Security proposal review
2. **Best alternative.** Reusing the existing checked reader and blob-hash pattern is simpler than adding a Git helper route and retains the accepted byte comparison. -- `dev/tools/git_read.py::_checked_bytes`; `install/_scaffold/upgrade.py` blob_id
3. **What would show it wrong?** A public warning case with a source directory nested inside another Git worktree must warn unavailable; a clean tagged source must stay silent. -- plan Scope and C1; `tests/test_manifest.py::TestProvenanceWarning`

**Blocking -- bind the root.** Scope requires `--show-toplevel` to identify a canonical source root, but does not say to compare that root with the canonical `cairn_root` passed to the warning. A nested source could otherwise be classified against its enclosing repository. Specify equality, unavailable on mismatch, and a focused public warning case. -- plan Scope; `install/_scaffold/install.py::git_provenance_warning`; accepted proposal, Security proposal review

**Coverage.** Read the committed plan, accepted proposal, existing warning, checked reader and public warning cases. The permanent cases target public behavior. No tests, reproduction, Windows execution or security review were performed; path-safety and race details remain outside this pass.

**Elapsed**: unknown. **Tokens**: unknown.

## Plan review -- Sol (Security Reviewer, High) -- 2026-11-19

Reviewed commit: dba989c6618f60636febda9a2414ea101a13f79f

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes, once pre-read validation is explicit. A pinned revision, bounded listing and identity-checked reads deliver the advisory comparison. See Scope and `templates/skills/_lib/git_read.py:241-303`.
2. **Best alternative.** Reuse the verified reader for the fixed operations and local reads. This preserves the existing Git restrictions and releases no new authority. See `install/_scaffold/lockfile.py:51-69` and `templates/skills/_lib/git_read.py:46-57`.
3. **What would show it wrong?** A malformed blob ID or administrative path alias reaches a file read, or a clean tagged checkout warns. Extend a focused public warning case in `tests/test_manifest.py::TestProvenanceWarning`.

**Blocking.** Require every blob ID to be lowercase hex of the pinned width. Explicitly reject filesystem aliases for Git administration paths, including Windows short names and equivalent names on case-insensitive filesystems. The checked reader checks links and identity, so the caller must complete these checks first. See Scope and `templates/skills/_lib/git_read.py:209-299`.

**Coverage.** Read the committed plan, accepted proposal, installer warning and verified reader. No tests, vulnerability reproduction or platform checks were run.

**Elapsed**: unknown. **Tokens**: unknown.

## Response -- Codex Sol (author) -- 2026-11-19

Accept both findings. Scope now requires source-root equality and precise object ID and Windows path validation. C1 names the nested source check. **Disposition**: ready-to-implement. Elapsed: unknown. Tokens: unknown.

## Ordinary code review -- Terra (Reviewer, Medium) -- 2026-11-19

**Verdict: ACCEPT. Findings: none.** The repair checks tagged source bytes before silence and keeps the warning advisory.

**Should this happen as framed?** Yes. `c07569cd` binds the tag and listing to a validated commit ID, requires the Git root to match the source root, and rechecks HEAD. Existing dirty, untagged, export and override paths remain; the guide reflects the warning.

**Best alternative.** Reusing the checked reader and Git blob hashing avoids a new Git helper route. Reads are bounded by the planned per-file and total limits; release-sized cost remains to be measured under C2.

**What would show it wrong?** Silence for concealed changed bytes or unavailable evidence, or a warning for clean committed bytes, would falsify the repair. The focused public cases exercise those outcomes and nested-root refusal.

**Coverage.** Read commit `c07569cd`, the reviewed plan and guide. The commit reports 12 focused Mac cases passed; I did not rerun them, measure release-sized cost, run Windows checks or perform Security Review. Those C2 checks remain outstanding.

**Elapsed**: unknown. **Tokens**: unknown.

## Security code review — Sol (High) — 2026-11-19

**Obligation**: Internal Security Review
**Verdict**: REVISE

**Should this happen as framed?** Yes. At `c07569cd`, the validated commit ID binds tag lookup and tree listing. The complete listing is checked before content reads, file identity is checked around each bounded read, and final HEAD must match before the installer can be silent. See `install/_scaffold/install.py:2159-2216` and `dev/tools/git_read.py:241-303`.

**Best alternative.** Match the existing Git blob hash calculation in `install/_scaffold/upgrade.py:3194-3205`. Git dictates the hash format. Signed provenance stays separate.

**What would show it wrong?** A nested source, invalid tree entry, or unproved content comparison that stays silent would fail C1. A clean tagged checkout with a legal trailing space in its macOS root name should also stay silent.

**Blocking.** Bandit B324 reports the default SHA-1 constructor as high severity. The release scan includes the scaffold and blocks high findings. Use `usedforsecurity=False` for the advisory Git object comparison and verify focused lint. See `install/_scaffold/install.py:2208` and `release/security_check.py:1425-1430`.

**Blocking.** The root parser strips path whitespace as well as Git's line terminator, so it may compare the wrong root. Preserve path whitespace and remove only the terminator. See `install/_scaffold/install.py:2168-2171`.

**Coverage.** Read the committed diff, reviewed plan, checked reader, and installed B324 implementation. Git documents HFS+ administrative-name equivalence. This pass establishes casefold checks and Windows resolved-spelling checks by inspection. HFS+ alias behavior, native tests, lint results, and release-sized cost were not exercised in this pass.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Security code review, pass 2 — Sol (High) — 2026-11-19

**Obligation**: Internal Security Review
**Verdict**: ACCEPT. Both blocking findings are resolved.

**Should this happen as framed?** Yes. In `be2f941e`, the SHA-1 constructor marks its use as a Git object checksum for the advisory comparison. The root parser removes one line terminator and keeps significant whitespace. Before reading any content, the administrative-name check also compares each component with Unicode format characters removed. The Windows branch uses the standard reserved-name check where available and retains the older runtime fallback.

**Best alternative.** Use the existing Git blob-checksum convention and preserve Git's path bytes up to the terminator. These changes implement that directly in `install/_scaffold/install.py`.

**What would show it wrong?** A focused Bandit finding, a warning for a clean root ending in a space, or a content read for the invalid administrative name would falsify this disposition. The corrective commit reports three affected Mac cases passing on Python 3.13.13 and focused Bandit passing.

**Coverage.** Read the correction and the affected cases in `tests/test_manifest.py`. This pass covers the specific format-character rejection by inspection. Actual HFS+ behavior, corrected native Windows evidence, and release-sized cost were outside the pass. I reran no checks on implementation code.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## Implementation closeout -- Codex -- 2026-11-19

C1 and C2 hold. The clean tagged, changed-byte, unavailable and invalid-path checks passed. Ordinary review accepted. The first Security code review identified lint and path handling defects. Commit `be2f941e` corrected them, and the focused second pass accepted.

Python 3.13.13 on Mac and 3.13.18 on native Windows: 12 provenance tests passed on `c07569cd` on each host. Reran three affected checks on each host on the correction: Mac 3 passed in 4.31 seconds and Windows 3 passed in 5.51 seconds. Focused Bandit and prose checks passed. A clean tagged test copy of `c07569cd` on Mac read 51,639,730 bytes across 1,097 tracked files in 1.89 seconds and produced no warning.

**Benefit versus cost**: worth it -- the warning detects a byte mismatch even when Git reports clean. The tagged clean path took 1.89 seconds on the measured tree; ongoing cost is one bounded read and three public warning cases added to an existing suite. Revisit if release size approaches the read cap.

Remaining: apply the reviewed AST correction for the changed warning and added helper as part of the grouped re-anchor. Home: the v0.8 trust-operation wait in dev/PLANNING.md. The AST gate remains unpassed.

Not run: final tree certification and native strict release records. Home: the v0.8 cut in dev/PLANNING.md and release/RELEASE_PROCESS.md.

Elapsed and tokens: unknown.
