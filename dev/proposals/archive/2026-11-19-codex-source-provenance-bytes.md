# Check installer source bytes before calling a checkout clean

**Author**: Codex Sol
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-19
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/conventions.md, dev/rules/working-agreements.md
**In brief**: Warn when source files differ from the tagged commit even if Git reports a clean checkout.

## Decision summary

The installer can omit its warning when Git's file conversions hide a changed source file. Keep the existing warning and add a direct comparison of the checkout bytes with the tagged commit before treating the source as clean. This adds one bounded read of the tracked files on the clean tagged path. The warning remains advisory, and the signed release verification procedure stays in place.

## Context

The Security Review of the archived Git attributes proposal identified a conversion that can hide a local edit from the installer's Git status check. Release closeout investigated the finding and the Maintainer asked to fix it for v0.8. Install integrity hashes the files it installs, and the separate release verification procedure verifies signed source. This item concerns the installer's source warning.

## Proposal

In `install/_scaffold/install.py`, retain the existing source classification and dirty-status warning. In the case that would otherwise be silent for a tagged checkout, bind the tag, recursive tree listing and final revision check to the same commit. Use the existing verified Git reader for fixed read-only Git operations. Compare the bytes of each tracked regular file directly with the Git blob ID from that commit. Reuse the reader's bounded, identity-checked file read, and calculate the blob ID in Python. Keep the generic Git helper unchanged. Use the current release policy of checking out the committed bytes.

Validate the full NUL-delimited tree list before using its paths. Refuse to classify an unsafe path, malformed record, unsupported entry, incomplete read or budget overrun as clean. Apply an 8 MiB listing cap, 16 MiB per file and 128 MiB total. The current tracked tree has 1,095 files and about 49 MiB. A definite difference warns of uncommitted changes. An incomplete comparison warns that the source could not be classified. Ordinary export installs, the existing development flag and warning-only behavior stay as they are. Update the provenance guide to describe the byte comparison.

## Rationale

Comparing original bytes avoids relying on conversions to tell whether source has changed. This keeps the fix local to the installer warning and avoids repinning the Git helper and its callers.

## Alternatives considered

Add another check of Git attributes. That would require a new supported Git query and could miss other ways Git status classifies bytes as unchanged. Direct byte comparison addresses the underlying mismatch.

## Documentation / doctrine surface

Update `install/PROVENANCE.md`. No doctrine or release procedure change.

## Evidence / verification plan

Run the focused provenance cases in `tests/test_manifest.py` on macOS and Windows. Retain the clean tagged, dirty, untagged and export controls. Add one regression that checks the public warning when a tracked file differs but the status check reports clean, and one check that unavailable byte evidence cannot yield silence. Use a small synthetic checkout and check the actual clean release-sized comparison once for cost. No full suite in this plan.

### Security preflight

The tagged tree supplies file names, modes and expected blob IDs. Untrusted names, links and replaced files must fail classification without following them or leaking their contents. Compare raw bytes with validated IDs, using bounded reads and a stable commit ID. Existing verified Git commands remain read-only and offline. Signed provenance and installation safety checks remain separate, and a concurrent filesystem change can make the advisory unavailable.

### Independent scientific check

N/A. No scientific assumption or result changes.

## Signals the change is wrong

The warning stays silent on a changed or unreadable tracked source, or appears on a clean checkout of the committed release bytes.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. Ordinary and Security Review at each applicable stage because the installer changes how it classifies source. Verify the expected installer AST change and carry it into the grouped Maintainer release re-anchor. No signing, admission or release operation is part of this plan.

## Ordinary proposal review -- Terra (Reviewer, Medium) -- 2026-11-19

**Verdict: ACCEPT. Findings: none.** The proposal closes a gap in an advisory warning by comparing checked-out bytes with a single tagged commit, while retaining export and development behavior.

**Should this happen as framed?** Yes. `git_provenance_warning` currently returns silence after a clean status and exact tag; the proposed bounded comparison addresses changed bytes that status can conceal. The existing reader has bounded, identity-checked reads; incomplete evidence warns rather than blocks installation.

**Best alternative.** Checking attributes alone would add a Git query while leaving other conversion mechanisms to account for. Direct byte comparison is a smaller sound scope for the warning; the existing upgrade blob comparison also provides an implementation reference.

**What would show it wrong?** A public warning test that stays silent for concealed changes or unavailable evidence, or warns on a clean tagged checkout of committed bytes, would falsify the proposal. Native Mac and Windows controls and one release-sized cost check are proportionate to this scope.

**Coverage.** Read the proposal at `19d1f674`, current warning and reader code, and provenance test names. No exploit reproduction, tests, or Security Review were performed; concurrent-change and path-safety details remain for the planned Security Review and implementation plan.

**Elapsed**: unknown. **Tokens**: unknown.

## Security proposal review — Sol (High) — 2026-11-19

```text
Reviewed commit: 19d1f674736b92127503a76b20c5ac5377c4df12
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. Direct byte comparison strengthens the advisory warning with one bounded pass over tracked files. The reader already allows `ls-tree`, disables object replacement and lazy fetch, and checks path and file identity around a bounded read. Reuse leaves the helper and release authority intact. Evidence: `dev/tools/git_read.py:241-296`, `dev/tools/git_read.py:519-520`.
2. **Best alternative.** Check Git attributes as well as status. That still relies on Git's classification of working bytes. The existing upgrade comparison provides a local reference for blob hashing. Evidence: `install/_scaffold/install.py:2158-2213`, `install/_scaffold/upgrade.py:3194-3205`.
3. **What would show it wrong?** Public tests should warn on differing bytes or incomplete evidence and stay silent for a clean tagged checkout. The plan should require matching the Git worktree root to the installer source root, validating all paths before reads, and checking final HEAD against the original commit. Measure elapsed time once at release size. Evidence: `tests/test_manifest.py`, proposed verification plan.

**Coverage.** Read the proposal, installer warning, Git runner, and checked byte reader. No tests, performance measurements, or implementation review.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Codex) -- 2026-11-19

**Tier**: heavy
**Accepted.** Maintainer chat, 2026-11-19:

> Go ahead and pick up where Antigravity left off. Finish the Windows release checks and reviews, fix the Git provenance issue, and clear the remaining blockers. Keep tests focused until final certification. I would like to get this release cut. Work with agents at the lowest possible tier, and use the fewest possible tokens

This records the explicit direction to implement the provenance fix for v0.8. The reviewed byte-comparison approach is the implementation choice.

**Elapsed**: unknown. **Tokens**: unknown.
