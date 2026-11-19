# Verify installer source before treating it as clean

**Author**: Codex Sol (Implementation)
**Source proposal**: dev/proposals/archive/2026-11-19-codex-source-provenance-bytes.md
**Status**: awaiting-plan-review
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

Resolve `HEAD` via `rev-parse --verify HEAD` to a validated 40- or 64-character lowercase hex ID. Use it in the exact-match `describe` call. Preserve the existing status warning. On the otherwise silent path, require `rev-parse --show-toplevel` to identify the canonical source root and repeat `rev-parse --verify HEAD` after comparison. Enumerate blobs with `ls-tree -r -z --full-tree <oid>`, capped at 8 MiB. Require a complete, nonempty, NUL-terminated listing. Parse all entries before opening files, accepting only supported regular modes, blob kind, the selected ID width and unique root-relative paths. Reject empty components, dot components, parent traversal, absolute or drive-relative names, backslashes, and Git administration names. On Windows also reject names Windows aliases or treats as devices, alternate streams or reserved paths, and normalized duplicate names.

Read each validated path using `_checked_bytes` with the smaller of 16 MiB and the remaining 128 MiB allowance. Compute the Git blob ID over its length header and bytes using the commit's hash format. A definite mismatch warns of changes; failed listing, read, validation or revision check warns evidence is unavailable. Warn without naming file contents or an untrusted path. Plain exports and `--allow-dev` keep their behavior.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Add installer comparison, warning guide and focused checks | Both plan reviews | Advisory tagged-source byte check |
| C2 | Verify on Mac and Windows, then resolve independent code reviews | C1 | Focused evidence and reviewed repair |

## Acceptance criteria

**C1.** Clean tagged source remains silent. Changed tracked bytes warn even if status reports clean, and an unavailable comparison warns. Existing dirty, untagged, export and development-override cases retain their outcomes. Invalid names fail before any file read. No new Git helper route, tool, or config.

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
