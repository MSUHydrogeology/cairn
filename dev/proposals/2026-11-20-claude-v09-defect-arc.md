# Settle every open defect at the start of v0.9: five plans, one signing

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — plans B to E change the installer engine, the session reader, shipped Python tools and protected tests.
**Plan review**: required(Internal + Internal Security Review) — for plans B, C, D and E; plan A is prose only and takes required(Internal).
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Twelve open issues and some Windows and gate gaps get fixed, closed with a reason or deferred in five small plans and one signing, so v0.9 starts clean before its rules are tightened.

## Decision summary

**Conclusion.** Adopters reported defects after the v0.8 cut in the upgrade, the first session, the quickstart and two tools. I propose one arc of five small plans that fixes them, closes what is not a defect, defers two feature requests and sends a third to the tightening proposal. I recommend all three choices below.

**Who each plan helps.**

- **Plan A, stale text.** Anyone reading the docs. The quickstart's PowerShell steps fail, the session-end prune command fails in PowerShell, and the prose check fails on a fresh clone.
- **Plan B, upgrading.** Anyone upgrading from 0.7.0 or 0.8.0. Today the security verification can stop working after an upgrade, a Windows clone fails with the wrong error, and a deleted `CLAUDE.md` blocks later upgrades.
- **Plan C, first session and tools.** Someone starting a first session on a fresh Windows install, and anyone using the usage meter or the security audit.
- **Plan D, gate and Windows checks.** The release operator. A check that the v0.8 file move narrowed comes back, and the older Windows test failures are measured, then repaired.
- **Plan E, one more file moves.** `docs/DOCUMENTATION_PLAN.md` moves into `dev/`, as the Maintainer asked on 2026-11-19. Adopters get the move through the upgrade.

**What the Maintainer is asked to choose.** He wrote (chat, 2026-11-20): "Once this is complete, please write the arc necessary for the defect fixes, including any in the Cairn Issues reported after the v0.8 cut. I really want a clean v0.9. Probably a bugfix releasee." He then set the release's shape (chat, same day): "I want a 0.9.1 bugfix, not a full version bugfix. I don't mind a 0.9 tightening with no notable new features, but not just defects alone" and "So we are going to do a comprehensive tightening. After the defects."

1. **Does v0.9 carry no notable new feature?** v0.9 is a tightening release: the defects in this arc first, then a comprehensive tightening of the rules, which gets its own proposal. A release that only fixes defects takes a point number, such as 0.9.1. If yes, these parts of the roadmap, each a new feature, wait for v0.10 with their scope kept:
   - section 3, scientific software: dimensions and governance (#19) and the release module. Test records are not decided here: he asked (chat, 2026-11-20) for an assessment of LHM's and modflow_tools' testing work first, and cheaper testing may belong to the tightening;
   - section 4, monitoring: the oversight website, the four-view comparison, the real-use meter comparisons;
   - section 5, less supervision: delegating decisions, the budget guard, draining an adopter's roadmap;
   - in section 2, the release `.zip` (#94), which he asked for in v0.9 (chat, 2026-11-19): "put a v0.9 issue to add a release .zip archive to that release, which omits Cairn's own dev folder".

   The three-host verification in section 2 stays, because a clean release is one checked where adopters run it. *Recommended: yes.* Nothing is dropped. The oversight website is what waits longest.
2. **Defer two feature requests to v0.10, and send one to the tightening?** #90 (find the repository root by a marker) and #91 part 3 (a helper that archives a plan and repoints links) are large and are not defects; they wait for v0.10. #79 asks for a smaller entry file, which is what the tightening is about, so it goes to that proposal. *Recommended: yes.* #90 would join the code-structure work.
3. **Accept the arc as grouped?** *Recommended: yes.*

**What the Maintainer does by hand.** This Decision, and the one on the separate re-anchor proposal. One signing: the re-anchor, his signed approval of the exact test files that guard Cairn's security checks, so that no agent can change them unseen. And the release cut, where the strict Mac and Windows records and the secrets scans waived for 0.8 fall due. Nothing else, and no list of tests.

## Context

Twelve issues are open as defects or frictions: #79, #90, #91, #93 and #95 to #102 (measured). Section 1, "Defects first", of the v0.9 roadmap (`dev/PLANNING.md`) already schedules this work; I took the list from it. A high-tier Strategy agent (Claude Fable 5.2) grouped the fixes and set the defaults. I checked them against the repository and the issues and wrote this up; Strategy edited the wording before the opening commit.

- Measured: `python tests/check_cairn.py` exits 1 with five issues (a meter export file cited in four tracked files, and a link to an untracked page). `docs/quickstart.md` lines 202, 280 and 281 name `bootstrap\`, which no longer exists. The bash-only prune command appears in five files. `install/UPGRADE.md` never mentions the layout move.
- Read, not run: the session reader lists every `*.md` except the template (`dev/tools/session.py:1264`) and escapes the backslash (`:186-190`). The security dispatcher accepts seven record keys (`templates/modules/default-on/run_security_verification.py:136`); the upgrade writes others (`install/_scaffold/upgrade.py:4364`).
- Not measured: Windows behavior, an upgrade run, Bandit, any test. Those rest on the reporters and on reading code.

## Proposal

Each plan has at most five chunks, and shows at its plan review how its items fit them; a plan that cannot is cut in two. The five share one joined test run. Plans A, B and C touch different files and run side by side. The [appendix](2026-11-20-claude-v09-defect-arc--appendix.md) lists every item with its resolution, plan, host and protected surface.

- **Plan A, stale text (prose; any host; usual review).** It corrects text that names the pre-0.8 layout (#97, #99.5), adds the layout move and the line-ending note to `install/UPGRADE.md` (#99.2, #95), gives the prune command in both shell forms (#93), says what to run when `python` is not found (#98.4), and clears the five prose-check failures (#98.5). A generated file is never hand-edited. Three methodology pages get a path corrected; an edit that would change what a rule says stops and takes a Security Review.
- **Plan B, upgrading (installer engine; Security Review).** The installer engine is the code that installs and upgrades Cairn in a project. #95, #99.1, #99.3, #99.4, #100, #102 and #98.3. When it is done: the error on a Windows clone names the real cause, and Cairn's own repository has a root `.gitattributes`; the security verification runs after an upgrade that included the layout move; a shallow fetch gets its own message; the `claim_check_command` token follows the move; the record of a deleted vendor wrapper can be retired by a documented route, wrappers only; and the installer says what to do when the harness folder is absent. Defaults: do not widen what the security dispatcher (the script that runs the security checks) accepts, heal trees already upgraded, and reproduce #99.4 before deciding to fix or close it.
- **Plan C, first session and tools (shipped Python; Security Review).** #98.1, #98.2, #91 part 2, #96, and #99.6 with #101. When it is done: session start lists no README as open work; paths print with forward slashes, and the escape policy is unchanged; the intent hook's execute-bit test works on Windows; the usage meter no longer reports UNKNOWN because of record types that carry no usage; and the security audit has a severity threshold the adopter sets, with the default unchanged (any finding fails) and the threshold in force printed on every audit result.
- **Plan D, gate and Windows checks (protected tests; Security Review).** It restores the scan of new files under `tests/` (B3a). For `tests/test_fork_advisory.py` (B3b) it restores no word match: if the test must tell one refusal from another, it checks which record the refusal names. It measures the older Windows failures on the Windows host, then repairs what still fails (B2a, B2d, B2e). It chooses between accepting Windows path separators in the release-membership checker and recording that the check runs only on the Mac (B2b). It checks the published v0.8.0 tag through both documented release routes in Windows Git Bash. For the history freeze that fails on refs pointing at trees, the default is to document a freeze from a clean clone.
- **Plan E, the documentation plan moves (installer engine and install contract; Security Review).** It moves `docs/DOCUMENTATION_PLAN.md` into `dev/`, adds the upgrade move, and updates the shipped files that name the old path. It runs after plan B, because it uses the move machinery that plan B repairs.

**Closed or deferred.** #91 part 1 is closed; 0.8 delivered it. The AST baseline correction was fixed at `ed893f0d`, and the joined run confirms it. The "bootstrap" wording check is not restored, because it looked for one word in a refusal message (Maintainer, chat, 2026-11-20: "Drop it."). On choice 2, #90 and #91 part 3 are deferred and #79 goes to the tightening proposal. A full Windows suite as a release gate belongs to the roadmap row on verifying releases on three hosts.

**Order.** (1) The one-round review rules (`dev/proposals/archive/2026-11-20-claude-one-round-reviews.md`) ship first. (2) Plans A, B and C. (3) Plans D and E, and the ceremony fix from the separate re-anchor proposal. (4) One joined run, on the canonical runtime and on Windows. (5) The re-anchor, signed once. (6) The light proposal `2026-11-19-codex-native-release-membership.md` is archived.

**The one signing.** `dev/proposals/archive/2026-11-19-claude-simpler-reanchor-ceremony.md` stays a separate proposal with its own review and Decision. This arc depends on it in two ways. Every change to a file the gate pins lands before the signing. The signing also needs that proposal accepted and implemented; its change to `release/repin.py` lands before step 4, so the joined run covers it. If it is not accepted, step 5 waits. Each plan records, for every protected file it changes, the reason the Maintainer will see at the signing. I read that order against `release/REANCHOR_RUNBOOK.md`; I did not run the gate.

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
- **S3, what runs it.** `run_security_verification.py local` and `upgrade --plan` fire the checks for plan B; session start runs plan C's and the gate runs plan D's. Each plan quotes its adopter-facing sentence.
- **S4, which way it breaks.** Defaults land on less authority: unknown lock keys stay refused, the audit fails on any finding, an unreadable usage record keeps the meter incomplete. Two items add authority: healing upgraded trees removes only the layout keys #99 names, and the retire route is run by the adopter, for wrapper files only.
- **S5, what still gets through.** Assumed: an attacker who writes the lockfile or threshold file. An adopter who sets the threshold high still passes, which is their choice; the audit still prints every finding. Closed by enumeration, not construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Any clean-means test fails, or a plan needs a second signing.

## Scope delta

**Scope delta**: preserved. This is the opening proposal; nothing accepted is removed.

## Assurance path

**Assurance path**: high-assurance. Plans B to E alter what the installer engine, the session reader, the security audit and protected tests do or accept.

## Review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

```
Reviewed commit: 76347908193838c31861e1b71cb06d2630d8435a
```

**Tier**: usual
**Findings**: raised (non-blocking only)
**Verdict**: ACCEPT

**Elapsed**: about 10 minutes
**Tokens**: unknown

The proposal tries to turn the roadmap's "Defects first" list into five reviewable plans and one signing, so v0.9 starts clean. I think it does.

**Foundations**

1. **Should this happen as framed?** Yes. Every open defect issue (#93, #95 to #102) and every bullet of roadmap section 1 appears in the appendix; the other open issues are listed as left alone -- `gh issue list`, `dev/PLANNING.md` lines 40-53, appendix.
2. **Best alternative?** Doing nothing leaves `check_cairn.py` failing; I ran it and it reports five issues, as the proposal says. One plan per issue costs more review -- `python tests/check_cairn.py`.
3. **What would show it wrong?** An upgrade of a test tree from 0.7.0 that still leaves the security verification unable to run, or a plan that needs a second signing -- the clean-means paragraph.

I spot-checked the code claims: `session.py:1264`, `:186-190`, the seven keys at `run_security_verification.py:136`, and `upgrade.py:4364` all match, as do the `bootstrap\` lines 202, 280 and 281 of `docs/quickstart.md`.

**Findings**

1. Non-blocking. Plan D lists about six pieces (B3a, B3b, the Windows measure-and-repair group, B2b, the tag check, the freeze), and plan B lists seven issues. The proposal never says how they fit five chunks each. Each plan should show its grouping at plan review.
2. Non-blocking. The Decision summary uses terms a scientist must translate: "re-anchor", "installer engine", "dispatcher". One plain sentence on what the signing protects would let him choose without help.
3. Non-blocking. Choice 1 defers #94, which he asked for in v0.9. The text says so; the Decision should quote it.

**Not covered**: I ran no upgrade, test or Windows check. I did not read the individual issue threads beyond titles. I did not read the re-anchor proposal or the runbook, so the signing order is checked only against the proposal's own text.

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-20

```
Reviewed commit: 6b53be20f51a6ad80efa4e7b42d46c094b4c091a
```

**Tier**: Security Review
**Findings**: raised (two blocking)
**Verdict**: REVISE

**Elapsed**: about 15 minutes
**Tokens**: unknown

The arc aims to fix every adopter-reported defect while keeping the signed gate anchor moving only once, after all pinned files settle. The defaults it states mostly lean the safe way.

**Foundations**

1. **Should this happen as framed?** Yes; issue #99 item 1 shows an upgrade silently disabling the security runners -- `gh issue view 99`.
2. **Best alternative?** Doing nothing leaves that disabled; per-issue plans multiply Security Reviews -- the Alternatives section.
3. **What would show it wrong?** `repin ceremony --transition` stopping on the 33 unrecorded lock and baseline commits -- `release/repin.py:2559`, as the re-anchor ceremony proposal measures.

**Findings**

1. Blocking. The Order omits the ceremony fix. Without it the transition ceremony refuses (re-anchor proposal, Context), and that fix edits `release/repin.py`, which the gate manifest freezes (`tests/fixtures/gate_manifest.json`, as `scripts/repin.py`). Add to "The one signing": "The signing also needs that proposal accepted and implemented; its change to `release/repin.py` lands before step 4, so the joined run covers it. If it is not accepted, step 5 waits."
2. Blocking. S4 says defaults land on less authority, but two items add write routes into the install lock: healing upgraded trees (#99.1) and retiring a wrapper's record (#102). Add to S4: "Two items add authority: healing upgraded trees removes only the layout keys #99 names, and the retire route is run by the adopter, for wrapper files only."
3. Non-blocking. The audit threshold (#101) lives in a file an agent can write. Plan C should print the threshold in force on every audit result.
4. Non-blocking. Plans B and D edit protected files (`upgrade.py`, `test_fork_advisory.py`), so the verifier will show HOLDs; each plan should record a reason ready for the Maintainer's dispositions.
5. Non-blocking. S3 misses session start and the gate, which fire plans C and D.

**Not covered**: plan-level design, Windows separator handling in B2b, the retire route's mechanism, any run of code or tests.

## Response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

Strategy grouped the arc, so Strategy answers the findings. Every finding is accepted, and each blocking one is closed with the reviewer's own sentence.

**Usual review**

1. Plans B and D are full: accepted. Each plan shows at its plan review how its items fit five chunks, and is cut in two if they do not.
2. Terms: accepted. The summary now says what the signing protects, and the Proposal says what the installer engine and the dispatcher are.
3. The release `.zip`: accepted. Choice 1 quotes the Maintainer's ask of 2026-11-19.

**Security Review**

1. Blocking, the ceremony fix was missing from the order: accepted. "The one signing" carries the reviewer's sentence, the Order names the fix in step 3, and the summary lists the second Decision the Maintainer makes.
2. Blocking, S4: accepted, with the reviewer's sentence.
3. The audit threshold: accepted. Every audit result prints the threshold in force.
4. HOLDs at the signing: accepted. Each plan records the reason for every protected file it changes.
5. S3: accepted. It now names session start and the gate.

The usual review did not read the runbook; the Security Review read its top section. Nobody has run the order of the signing.

**Elapsed**: about 10 minutes (estimate). **Tokens**: unknown. The harness reported 81,979 tokens and about 1 minute for the usual review, and 91,698 tokens and about 2 minutes for the Security Review.

### Withdrawn / superseded commitments

None.

## Response -- Claude Fable 5.2 (Strategy, to the Maintainer's direction) -- 2026-11-20

The Maintainer set the shape of v0.9 in chat on 2026-11-20, after the reviews and before a Decision. His words are quoted in the Decision summary. Choices 1 and 2 are revised in place to follow them.

1. **Choice 1.** It asked whether v0.9 is a bugfix release. He answered that a release of defects alone takes a point number, and that v0.9 is a tightening release with no notable new feature. Choice 1 now asks only which roadmap parts wait for v0.10 as new features.
2. **Test records leave choice 1.** He asked for an assessment of LHM's and modflow_tools' testing work first. That row is decided after it.
3. **Choice 2, #79.** A smaller entry file is the subject of the tightening, so #79 goes to that proposal and not to v0.10. The appendix row says the same.
4. **The tightening is not in this arc.** It gets its own proposal and runs after the defects, as he said.

The five plans, their order, the joined run and the signing are unchanged, so no scope was added to what the reviewers read and no further review pass follows. Not checked: whether a plan in this arc edits a rule file that the tightening will also edit. The tightening proposal has to read this arc's file lists.

**Elapsed**: about 15 minutes (estimate). **Tokens**: unknown.

### Withdrawn / superseded commitments

- "v0.9 is a bugfix release" (choice 1 as reviewed): replaced by a tightening release with no notable new feature, on the Maintainer's word.
- Test records waiting for v0.10: withdrawn. The row is decided after the assessment.
- #79 deferred to v0.10: replaced. It goes to the tightening proposal.

## Decision -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-20

**Elapsed**: under 1 minute; **Tokens**: unknown.

**Tier**: heavy

**ACCEPTED.** Asked "Do you accept the defect arc with all three choices as now worded, or do you want to change one?", the Maintainer's authorization, quoted verbatim (chat, 2026-11-20):

> "Go ahead on the defect arc."

This accepts the proposal as revised at `ef3590d0` (one link in it was repointed at `d4f3b1f0`), with all three choices as worded there. Choice 1: v0.9 carries no notable new feature, and the roadmap parts that choice lists wait for v0.10. Choice 2: #90 and #91 part 3 wait for v0.10, and #79 goes to the tightening proposal. Choice 3: the arc of five plans. He named no tier, so the tier is the one the proposal proposed: heavy. Plans B, C, D and E each get a usual review and a Security Review at the plan stage and at the code stage; plan A, prose only, gets a usual review at each.
