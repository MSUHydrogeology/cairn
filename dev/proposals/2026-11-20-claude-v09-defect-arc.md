# Settle every open defect at the start of v0.9: five plans, one signing

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — plans B to E change the installer engine, the session reader, shipped Python tools and protected tests.
**Plan review**: required(Internal + Internal Security Review) — for plans B, C, D and E; plan A is prose only and takes required(Internal).
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Twelve open issues and some Windows and gate gaps get fixed, closed with a reason or deferred in five small plans and one signing, so v0.9 can be a clean bugfix release.

## Decision summary

**Conclusion.** Adopters reported defects after the v0.8 cut in the upgrade, the first session, the quickstart and two tools. I propose one arc of five small plans that fixes them, closes what is not a defect and defers three feature requests. I recommend all three choices below.

**Who each plan helps.**

- **Plan A, stale text.** Anyone reading the docs. The quickstart's PowerShell steps fail, the session-end prune command fails in PowerShell, and the prose check fails on a fresh clone.
- **Plan B, upgrading.** Anyone upgrading from 0.7.0 or 0.8.0. Today the security verification can stop working after an upgrade, a Windows clone fails with the wrong error, and a deleted `CLAUDE.md` blocks later upgrades.
- **Plan C, first session and tools.** Someone starting a first session on a fresh Windows install, and anyone using the usage meter or the security audit.
- **Plan D, gate and Windows checks.** The release operator. A check that the v0.8 file move narrowed comes back, and the older Windows test failures are measured, then repaired.
- **Plan E, one more file moves.** `docs/DOCUMENTATION_PLAN.md` moves into `dev/`, as the Maintainer asked on 2026-11-19. Adopters get the move through the upgrade.

**What the Maintainer is asked to choose.** He wrote (chat, 2026-11-20): "Once this is complete, please write the arc necessary for the defect fixes, including any in the Cairn Issues reported after the v0.8 cut. I really want a clean v0.9. Probably a bugfix releasee."

1. **Is v0.9 a bugfix release?** If yes, these parts of the roadmap wait for v0.10 with their scope kept:
   - section 3, scientific software: dimensions and governance (#19), the release module, test records;
   - section 4, monitoring: the oversight website, the four-view comparison, the real-use meter comparisons;
   - section 5, less supervision: delegating decisions, the budget guard, draining an adopter's roadmap;
   - in section 2, the release `.zip` (#94), which he asked for in v0.9 on 2026-11-19.

   The three-host verification in section 2 stays, because a clean release is one checked where adopters run it. *Recommended: yes, with that one exception.* Nothing is dropped. The oversight website is what waits longest.
2. **Defer three feature requests to v0.10?** #90 (find the repository root by a marker), #91 part 3 (a helper that archives a plan and repoints links) and #79 (a smaller entry file). Each is large and none is a defect. *Recommended: yes.* #90 would join the code-structure work.
3. **Accept the arc as grouped?** *Recommended: yes.*

**What the Maintainer does by hand.** This Decision. One signing: the re-anchor, which moves the signed checkpoint the gate trusts. And the release cut, where the strict Mac and Windows records and the secrets scans waived for 0.8 fall due. Nothing else, and no list of tests.

## Context

Twelve issues are open as defects or frictions: #79, #90, #91, #93 and #95 to #102 (measured). Section 1, "Defects first", of the v0.9 roadmap (`dev/PLANNING.md`) already schedules this work; I took the list from it. A high-tier Strategy agent (Claude Fable 5.2) grouped the fixes and set the defaults. I checked them against the repository and the issues and wrote this up; Strategy edited the wording before the opening commit.

- Measured: `python tests/check_cairn.py` exits 1 with five issues (a meter export file cited in four tracked files, and a link to an untracked page). `docs/quickstart.md` lines 202, 280 and 281 name `bootstrap\`, which no longer exists. The bash-only prune command appears in five files. `install/UPGRADE.md` never mentions the layout move.
- Read, not run: the session reader lists every `*.md` except the template (`dev/tools/session.py:1264`) and escapes the backslash (`:186-190`). The security dispatcher accepts seven record keys (`templates/modules/default-on/run_security_verification.py:136`); the upgrade writes others (`install/_scaffold/upgrade.py:4364`).
- Not measured: Windows behavior, an upgrade run, Bandit, any test. Those rest on the reporters and on reading code.

## Proposal

Each plan has at most five chunks. The five share one joined test run. Plans A, B and C touch different files and run side by side. The [appendix](2026-11-20-claude-v09-defect-arc--appendix.md) lists every item with its resolution, plan, host and protected surface.

- **Plan A, stale text (prose; any host; usual review).** It corrects text that names the pre-0.8 layout (#97, #99.5), adds the layout move and the line-ending note to `install/UPGRADE.md` (#99.2, #95), gives the prune command in both shell forms (#93), says what to run when `python` is not found (#98.4), and clears the five prose-check failures (#98.5). A generated file is never hand-edited. Three methodology pages get a path corrected; an edit that would change what a rule says stops and takes a Security Review.
- **Plan B, upgrading (installer engine; Security Review).** #95, #99.1, #99.3, #99.4, #100, #102 and #98.3. When it is done: the error on a Windows clone names the real cause, and Cairn's own repository has a root `.gitattributes`; the security verification runs after an upgrade that included the layout move; a shallow fetch gets its own message; the `claim_check_command` token follows the move; the record of a deleted vendor wrapper can be retired by a documented route, wrappers only; and the installer says what to do when the harness folder is absent. Defaults: do not widen what the security dispatcher accepts, heal trees already upgraded, and reproduce #99.4 before deciding to fix or close it.
- **Plan C, first session and tools (shipped Python; Security Review).** #98.1, #98.2, #91 part 2, #96, and #99.6 with #101. When it is done: session start lists no README as open work; paths print with forward slashes, and the escape policy is unchanged; the intent hook's execute-bit test works on Windows; the usage meter no longer reports UNKNOWN because of record types that carry no usage; and the security audit has a severity threshold the adopter sets, with the default unchanged (any finding fails).
- **Plan D, gate and Windows checks (protected tests; Security Review).** It restores the scan of new files under `tests/` (B3a). For `tests/test_fork_advisory.py` (B3b) it restores no word match: if the test must tell one refusal from another, it checks which record the refusal names. It measures the older Windows failures on the Windows host, then repairs what still fails (B2a, B2d, B2e). It chooses between accepting Windows path separators in the release-membership checker and recording that the check runs only on the Mac (B2b). It checks the published v0.8.0 tag through both documented release routes in Windows Git Bash. For the history freeze that fails on refs pointing at trees, the default is to document a freeze from a clean clone.
- **Plan E, the documentation plan moves (installer engine and install contract; Security Review).** It moves `docs/DOCUMENTATION_PLAN.md` into `dev/`, adds the upgrade move, and updates the shipped files that name the old path. It runs after plan B, because it uses the move machinery that plan B repairs.

**Closed or deferred.** #91 part 1 is closed; 0.8 delivered it. The AST baseline correction was fixed at `ed893f0d`, and the joined run confirms it. The "bootstrap" wording check is not restored, because it looked for one word in a refusal message (Maintainer, chat, 2026-11-20: "Drop it."). #90, #91 part 3 and #79 are deferred on choice 2. A full Windows suite as a release gate belongs to the roadmap row on verifying releases on three hosts.

**Order.** (1) The one-round review rules (`dev/proposals/archive/2026-11-20-claude-one-round-reviews.md`) ship first. (2) Plans A, B and C. (3) Plans D and E. (4) One joined run, on the canonical runtime and on Windows. (5) The re-anchor, signed once. (6) The light proposal `2026-11-19-codex-native-release-membership.md` is archived.

**The one signing.** `dev/proposals/2026-11-19-claude-simpler-reanchor-ceremony.md` stays a separate proposal with its own review and Decision. This arc depends on it in one way: every change to a file the gate pins lands before the signing. I read that order against `release/REANCHOR_RUNBOOK.md`; I did not run the gate.

**How each fix is shown.** Before a fix, a check fails for the reason the issue gives: a test for code; the prose check and a search for the old names for text. After the fix it passes. A claim that cannot be reproduced is closed with the evidence.

**Clean means:** every open issue on the list is closed at a fixing commit, closed with a recorded reason, or deferred with the Maintainer's quoted word; the prose check passes on a fresh clone; an upgrade from 0.7.0 and from 0.8.0 runs to the end on a test tree, and the security verification passes afterwards; a first session on a fresh Windows install lists no false open work; and there is one re-anchor.

## Rationale

Grouping by file keeps the Security Reviews to four plans and edits each shared file once. Landing every pinned-file change before the signing keeps the signing to one.

## Alternatives considered

- **Do nothing.** The issues stay open, and an upgrade can leave the security verification unable to run.
- **One plan per issue.** About twenty Security Reviews.
- **Keep v0.9 as scheduled.** Defects first, then roadmap sections 2 to 5 in one release.

## Documentation / doctrine surface

Plan A edits the quickstart, `install/UPGRADE.md`, profile comments, installed module text and three `docs/methodology/` pages (path corrections only). Plan E moves the documentation plan. After the Decision, `dev/PLANNING.md` moves the rows named in choice 1 to v0.10. This proposal edits none of them.

## Evidence / verification plan

### Tests required

Each plan names its promises and entry points and runs only the tests that name its changed files.

### Examples / smoke checks

`python tests/check_cairn.py` on a fresh clone; an upgrade of a test tree from 0.7.0 and from 0.8.0; session start on a fresh Windows install.

#### Security preflight

- **S1, who supplies the check's input.** Adopter files (lockfile, threshold setting, usage logs) and the upgraded tree's Git history. The thing judged supplies them, so each plan names its reader and refuses unknown or malformed values.
- **S2, can it fail.** Each fix starts with a test that fails on today's code. Each plan states any check that reads what it checks.
- **S3, what runs it.** `run_security_verification.py local` and `upgrade --plan` fire the checks; each plan quotes its adopter-facing sentence.
- **S4, which way it breaks.** Defaults land on less authority: unknown lock keys stay refused, the audit fails on any finding, an unreadable usage record keeps the meter incomplete.
- **S5, what still gets through.** Assumed: an attacker who writes the lockfile or threshold file. An adopter who sets the threshold high still passes, which is their choice; the audit still prints every finding. Closed by enumeration, not construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Any clean-means test fails, or a plan needs a second signing.

## Scope delta

**Scope delta**: preserved. This is the opening proposal; nothing accepted is removed.

## Assurance path

**Assurance path**: high-assurance. Plans B to E alter what the installer engine, the session reader, the security audit and protected tests do or accept.
