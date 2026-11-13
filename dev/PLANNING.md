# Cairn — development board

This board lists the work left and its next step. The Maintainer reads the
status, waits and release sections. Agents also read **Working rules** and the
sections after it. Evidence, quotes and history live in each row's
**Record** column: an issue, strategy note, proposal, plan or guide, or the
Maintainer chat the item came from. Finished work leaves the board, except for
the numbered v0.7 rows retained below.

`python tools/board.py` lists every open proposal and plan with its status;
`python tools/board.py --maintainer` lists what waits on the Maintainer.

## Waiting on you

Lines marked **Waiting on Maintainer** are what `board.py --maintainer` lists,
together with any proposal awaiting your Decision.

### Sol choices not yet reviewed

The Maintainer reviewed the eight delegated Decisions and three safe-Git choices on 2026-11-10; each stands. The delegated choices below are not reviewed yet. Their records live in the named plan or commit, not here. Delete a line once it is reviewed.

- Safe-Git hook-index and sweep design (`2fd633b4`, `d062db38`) and old-Git mechanisms (`00aecab3`, `709133e0`): [safe-Git plan](plans/archive/2026-11-06-safe-git-reads.md).
- Meter public reporting input (`1a645c1e`): [Meter plan](plans/archive/2026-11-04-metered-cost.md).
- Historical measurement record (`4deae61b`).
- Three `modflow_tools` choices (raster-layer filter `38f21f9b`, figure writes `76009ef3`, and an audit interpretation at source `2bf8c2c4`), recorded in that project.

### Question for the Maintainer: the release candidate Decision

- **Waiting on Maintainer**: Decision naming the release candidate bytes

The re-anchor runbook (`bootstrap/REANCHOR_RUNBOOK.md`, "Preparing the forward baseline") says not to run the AST baseline correction "until a separate Maintainer Decision authorizes those exact candidate bytes". Three choices are yours, with my recommended defaults. **Candidate:** the final committed tip once the open agent work lands (the AST inputs have not changed since `91e17bf1`, so a fresh packet should repeat the 21 symbol changes already reviewed). **Route:** the forward baseline that is prepared; the ordinary ceremony would list 102 modified files, 3 missing files and 1,087 dropped test IDs as holds, each needing a recorded disposition. **Roster:** keep the three deleted names in the byte-pinned roster, and decide whether to add the POSIX-only test nodes created since the roster was frozen (55 to 56 found in the files I ran: 15 in `test_git_read.py`, 39 in `test_meter.py`, a few elsewhere) as posix-native-only entries. A strict Windows run rejects any skip that is not listed, so without them the Windows release record cannot validate. Either way the roster file's hard-coded digest and the runbook's digest change and the capped Security Review reopens (Decision 18). **Decided 2026-11-13:** the roster refresh is approved (Maintainer chat: "Refresh away. Do what's needed, not what you are narrowly confined by a word box"). My reading: it covers the nodes found in a full native Windows run, the new digests, and the Security look the change needs; it does not name the release candidate or the route, which stay open below. My reason for the default stands: those tests cannot run on Windows by design, and listing them loosens no check that ran before. Cost if wrong: a reader or the signed baseline binds to bytes you later change. The record `dev/measurement/reanchor-prep-2026-11-13.md` lists the other ten steps.

## Where Cairn stands

[Cairn 0.6.1 is released](https://github.com/MSUHydrogeology/cairn/releases/tag/v0.6.1).
Cairn builds itself with Cairn and is used in LHM and modflow_tools. The patch
is merged into `0.7-dev`; new v0.7 work proceeds there.

Standing direction from the Maintainer (2026-07-22): science projects come
first, and Cairn fixes what it already ships before building anything new. A
new tool or mechanism needs its own go-ahead. No outside project has yet run
Cairn end to end; that trial was waived for 0.4 and 0.5 and is still open
(see **Outside correctness trial**, below).

Standing direction from the Maintainer (2026-11-10): Windows is an equal partner with macOS and Linux, and the shipped tools support Python 3.12. Cairn's own certifying runs may stay on Python 3.13. Item 21 carries the Python 3.12 work; the Windows secrets-scan route is in the v0.8 secrets-scanning row.

## v0.7 — better software engineering with lower cost

The release must improve the software scientists build, not just make Cairn's
own process faster:

- **Engineering quality:** clearer architecture and interfaces, readable and
  reusable code, tests that catch meaningful scientific and software faults,
  and acceptance criteria connected to evidence.
- **Suite consolidation:** reduce repeated setup and redundant tests while
  preserving fault coverage and required scientific, security and release
  checks. Meet the existing runtime targets without treating fewer tests as
  success by itself.
- **Cost measurement:** gather actual usage per work item when reliable,
  otherwise daily, refreshed at handoff; expose missing attribution rather
  than guess. Use one collection and reporting design.

Coordinate the existing rows: suite consolidation with testing guidance and
acceptance criteria; code discovery with architecture guidance and visual
exploration; metered cost with lightweight team measurement. These are shared
workstreams, not additional processes or permission to remove outcomes.

Maintainer direction (chat, 2026-11-02):

> "I really want to make sure we get better software engineering into v0.7. I need those"

> "but let's get the suite consolidation and cost measurement in v0.7 too. Please write up this, and make a v0.8 cut with the deferred items."

> "Move the first five in v0.8 back into v0.7. Otherwise good!"

Existing proposal, review, Security Review and Maintainer requirements remain
where applicable. Release scheduling alone neither changes an accepted
contract nor authorizes implementation, a push or publication.

### Decisions to review when you return

Temporary authority, Maintainer chat 2026-11-11:

> Please proceed without me. Pass decisions that can be reversed an Opus agent and track them. I will be back online in the morning.

> I trust your decisions, please lean Haiku when you can. And only have Opus do what's absolutely necessary

Renewed overnight authority, Maintainer chat 2026-11-12:

> Please continue, and pass decisions that aren't proposal decisions to a Sol agent (or make them yourself). Keep a log of these so we can review them in the morning.

Rows 21 onward record this night's local choices. Proposal Decisions remain
the Maintainer's; the choices below do not grant publication or signing authority.

**Maintainer acceptance -- 2026-11-12:** Decisions 21–26 accepted.

> I accept all of the Decisions 21-26

Scribed by GPT-6.1 Terra, Implementation coordinator; elapsed approximately one minute, Tokens unknown.

**Maintainer acceptance -- 2026-11-12:** Decisions 1–20 accepted as recorded. Accepting a row accepts the choice and leaves its undo path in place. Row 19 stays marked superseded, because the reviews it waited for ran (`ff1acaeb`).

> Please record acceptance of the 1-20 decisions

Scribed by Claude Sonnet 5.5, Developer; elapsed approximately three minutes, Tokens unknown.

Reversible local work only. Pushes and the re-anchor remain Maintainer-owned. The accepted plan-template change is implemented and archived; it is no longer awaiting a Decision. Each row is the coordinating agent's call unless it says otherwise; undo it by reverting the cited commit.

| # | Decision | By | Why | How to undo |
|---|---|---|---|---|
| 1 | Plans 16 and 17 may archive without the single-final-commit wide test run; the 2026-11-10 acceptance (`088d4721`) stands as the waiver | Maintainer, chat 2026-11-11 ("Yes on acceptance") | The Maintainer had already conceded that run; the template has no waiver path, so the word is copied into each plan | Revert the archive commit; run the wide check at release verification (item 12) |
| 2 | The same reading applies to plan 2e | Agent | Its combined evidence is covered by the same 2026-11-10 acceptance | Same as row 1 |
| 3 | Omitted guarded readers, skips and failed-then-rerun tests in plans 2e, 16 and 17 are recorded as known omissions under the waiver, and each plan says `Dispositions: none`. No `defer` is used, because a `defer` needs the Maintainer's verbatim word; reconciling plan 16's 20-versus-33 reader count stays open in its record | Agent | The omissions are not new follow-ups, and item 12 already owns the final required checks | Edit the plan's Dispositions section |
| 4 | Accepted the Haiku builder's fixes for installer items 18 (`db8115d0`) and 19 (`f1c8f011`) after reading both diffs and running the two new tests; the batch's Security Review and the re-anchor are still due | Agent | Each is a small change with a behavior test that failed first; item 19's upgrade refusal for existing placeholder lockfiles matches how `{{...}}` was already treated | Revert the commit |
| 5 | Archived plan 16 (`8857f5fd` ready-to-archive, then `ea1c9365`) after a fresh review of the changes made since its code reviews found no weakened promise | Agent | The Maintainer waived the missing wide run (row 1), the reviewer returned READY, and the closeout record names the open 20-versus-33 count | Revert `ea1c9365`, then `8857f5fd` |
| 6 | Repaired three defects my `AGENTS.md` trim left behind (`885e993c`): the README pointed to `AGENTS.md` for the checks while `AGENTS.md` pointed back; the credentials ban lost "shared facts"; the queued-outcome rule lost its trial example | Agent | The plan 2e and 17 reviews found them, and each repair restores wording the trim cut without touching the 1,500-word files | Revert `885e993c` |
| 7 | Archived plan 2e after a REVISE (`f60f6deb`), two README repairs (`885e993c` and a follow-up) and a READY re-look (`8827460e`). Core `AGENTS.md` keeps one pointer line; the note path, trigger and manual checks live in the reflections README | Maintainer, chat 2026-11-11 ("You may record the scope delta on the AGENTS question.") | The Maintainer chose the scope delta over restoring about 45 words; it is recorded in the plan | Revert the archive commit, then delete the plan's Scope delta section |
| 8 | Archived plan 17 (`ready-to-archive`, then the archive commit) after a REVISE (`46c2e386`), a repair (`885e993c`) and a READY re-look (`950a7a39`). I judged its Scope row, which names `AGENTS.md` by letter for the trial example, covered by your 2026-11-10 authorization: the whole paragraph moved to the collaboration guide in the trim and the example moved with it | Agent | The content is intact in the guide and the closeout record names the move; unlike plan 2e, no content left the shipped files | Revert the archive commit, then the ready-to-archive commit |
| 9 | Posted one comment each on issues #54, #56 and #57 naming the fixing commit (`0eea3901`, `7fb0875c`); nothing closed, labeled or reassigned | Maintainer, chat 2026-11-11 ("You may comment on GitHub") | Plan 2e's C3 required #54 to cite its fixing commit; #56 and #57 had no citation | Delete the comments on GitHub |
| 10 | Released the two stale Sol claims on the metered-cost and promise-unit-testing plans (5 and 2 days old) | Agent | They blocked nothing but kept the handoff prune from running clean | Re-claim the files |
| 11 | Deleted the five plain-retire wording pins the functional-prose plan lists (`faf600fe`); left about 120 names in tests the plan keeps in part | Agent | Splitting pins out of real install, parity and behavior checks risks losing coverage for little gain | Revert `faf600fe` |
| 12 | Added changelog entries for the local note and for installer fixes 18 and 19 | Agent | Finishing work updates the changelog; adopters would notice each | Revert the archive commit |
| 13 | Chose the lighter lane for installer fixes 18 and 19: no separate Security Review. Fix 18 removes a write and fix 19 refuses more inputs; neither widens a trust boundary, both have a behavior test that failed first, and the item 12 re-anchor shows you the changed installer code | Agent | The lifecycle's rule for ordinary uncertainty is the lighter lane with a stated reason; row 23's installer change still needs its own Security Review | Ask for the review; it would be a High-tier (Opus) pass |
| 14 | Cut about 560 test functions in 13 batches (private-name tests, wording pins, tests of tests) from the agents' promise-list reports; held back 30 that the release security roster, a release document or a shipped script names | Agent, on your 2026-11-11 direction to cut | You said the strategy is promises only and that we are cutting; the 30 held ones would make the release gate's required list refuse | Revert the batch commit (each names its batch) or the restore commit `0b9e695f` |
| 15 | Had Opus reviewers decide every open row (149 questions, 508 CONVERT) and Sonnet agents write 51 public tests, deleting 202 private originals | Maintainer, chat 2026-11-11 ("I am going to need you and the Opus agent to decide that 153 open questions"; "keep the 80/20 principle in mind") | You handed the testing judgments to us; each group was mutation-checked in a scratch copy of the code | Revert the job commits `de414f9e`, `d98ea3af`, `55154dfc`, `299a824e`, `e15b596e`, `09e1d45d` |
| 16 | Restored 34 tests that the release roster, a release document, `SAFETY.md`, `SECURITY_MUTATIONS.md` or a shipped source comment names as a guard; held 9 registry checks for the Security Review | Agent | A cut must not leave a written claim, or the release gate, without its guard | Cut them again after the Security Review |
| 17 | Added item 24 for five possible product defects the new tests exposed, plus a list of stale test names in comments; no code changed | Agent | They are findings for you to prioritize, not fixes | Delete the row |
| 18 | Retired 3 of the 31 held tests (a count pin and two controls named only in a historical `SAFETY.md` paragraph); kept the other 28 and the 15 that wait for item 24 | Maintainer, chat 2026-11-12 ("retire now unless it disrupts the re-anchor"; "keep until item 24") | 24 are on the release roster (changing it reopens the capped Security Review), 2 are in shipped files, 1 is a parity check, 1 is a release-procedure step | Restore the three from `b5d91a91^` |
| 19 | The independent comparison and the Security Review wait until the Maintainer's credits reset; no high-tier agent is to be started before then | Maintainer, chat 2026-11-12 ("We need to wait on the Security Review until we get a credit reset") | It is the one safety net not yet run for the cuts; the suite passes and everything is committed and reversible | Superseded 2026-11-12: the reviews ran and were accepted (`ff1acaeb`); see item 22 |
| 20 | The test mapper (`tools/test_tiers.py for`) selects no tests when only `dev/PLANNING.md` or `CHANGELOG.md` changes | Agent, prompted by the Maintainer's remarks on 2026-11-12: nine minutes of tests for a planning edit is the testing we are trying to eliminate, and "Might as well check if this happens to changelog too" | The eight tests that mention the board and the six that mention the changelog build their own copies and none reads Cairn's; the certifying run still covers them; the board's public test failed first; the changelog change was committed without running tests, at the Maintainer's instruction | Revert `7313c50d` and `1b04502c` |
| 21 | Use a shared Ubuntu 24.04 ARM64 VM, `linux-dev` SSH alias, 2 CPUs, 3 GiB RAM and a 64 GiB sparse disk; install Git 2.56.1 in a user prefix | Root, implemented by Luna/Terra, 2026-11-12 | Supports actual Linux 3.12 checks and other projects. Automatic approval rejected a persistent Git PPA; verified upstream source was built separately without adding a package source. Access and separate-update responsibility are in [local development rules](rules/development-environment.md), `744f12f5` | Stop the VM before changing resources; remove the user Git PATH selection to use Ubuntu's retained Git. Preserve project data |
| 22 | Accept the tested prose-report repairs at the two-pass Security limit and continue to final verification | Sol, delegated non-proposal disposition `25e6ce71` | Focused public checks and ordinary review satisfy the reported fixes; no third Security Review or independent post-cap code assessment is claimed. Wide verification remains required | Reopen the disposition and seek the Maintainer's specific authorization for any further Security pass |
| 23 | Prepare already-accepted upgrade-growth and release-verification plans before the older plans archive | Root, 2026-11-12; openings `abd8efdb`, `326f9474` | Uses available authoring capacity and allows overlapping work to share final verification. All accepted outcomes, required reviews and checks remain | Restore the former preparation order while retaining both accepted outcomes |
| 24 | Allow the upgrade-growth opening to use 1,321 words against the 1,000-word target | Root, 2026-11-12; `abd8efdb` | Keeps the necessary High-designed isolation and finite comparison specification in one plan, without a sidecar | Shorten duplication while retaining the executable design and every accepted outcome |
| 25 | Archive the fulfilled keep-core Meter choice without manufacturing a no-op implementation plan; open Meter's existing testing eligibility condition | Sol interpretation, `749eadaa`, `41b94f01` | The Maintainer selected the existing installation contract. This satisfies the earlier rescoping prerequisite but clears no new Meter removals; current post-cut review duties and explicit holds remain | Revisit the lifecycle interpretation; the accepted core-install choice itself remains unchanged |
| 26 | Route newly opened scientific-evidence Issues #58–#59 and test-cost Issue #61 to existing v0.8 proposal preparation; link #60 to active v0.7 promise-testing work and close implemented #55 | Root, 2026-11-12 | All seven remaining open Issues have a board home. The new suggestions are not accepted scope; no current check is waived or accepted v0.7 outcome deferred. #55 has fixing commit `3bd9f8a7` and recorded native Windows checks | Reassign the queued proposals; reopen #55 if its demonstrated defect persists |
| 27 | The claims check at commit only warns and never blocks: change the shipped enforce-mode default from `block` to `warn` (roadmap item 28) | Maintainer, chat 2026-11-13 ("Go with warn only on the claims check") | Cairn's standing rule is that process tools warn and only genuine safety refuses; on 2026-11-10 the hook refused a commit under another session's fresh claim, which broke it. The claims log still shows overlaps. Cost: two sessions can overwrite each other's work more easily | Set `"enforce": "block"` in `dev/.cairn/intent-config.json`; the mode stays available |
| 28 | Refresh the Windows roster: add the POSIX-only (and any Windows-only) test nodes created since the roster was frozen to `NATIVE_ONLY_NODE_IDS` in `bootstrap/tests/security_manifest.py` by source classification, and update its policy identity and member counts (in progress 2026-11-13, not yet committed) | Maintainer, chat 2026-11-13 ("Refresh away. Do what's needed, not what you are narrowly confined by a word box") | A strict Windows run rejects any skip that is not listed, so without these entries the Windows release record cannot validate. The saved Windows reports show 55 to 56 unlisted skips (15 in `test_git_read.py`, 39 in `test_meter.py`, a few elsewhere). The classification reads source and collects test names only; no suite run | Revert the roster commit; the identity returns to `sha256:a3baa42d...` and the counts to 63 Windows-only and 650 POSIX-only |

### Current arc: completion and integration

Maintainer direction, chat 2026-11-12, applies to the remaining v0.7 work:

> Plan, review, code, review, test ONLY the code that was written--its public promises only. Decide dispositions, archive. Next plan, repeat. At the end--or at absolutely critical points--test integrations.

> This whole arc probably just needs a round or two at most of real testing.

Complete each plan with its changed-code public-promise checks, required reviews and dispositions, then archive it. The previous per-plan wide Boundary B completion requirement and blanket 25-entrypoint-by-three-platform runtime matrix are replaced for this arc by this direction. Feature scope and public promises remain intact. Item 12 owns one consolidated integration/certifying round after implementation, with only focused correction checks for failures; an earlier integration needs a specific critical shared boundary. Reuse unchanged evidence. A known failure of a changed public promise remains repair work, not an integration deferral. No extra proposal or review stage is required to apply this explicit direction.

### Release verification -- 2026-11-12/13

The one shuffled seed-0 certification run used clean committed `072d82d2` and canonical Python 3.13.13: **5,344 passed, 63 skipped, six failed**, 2,946.75 seconds. The strict release-membership comparison refused the report because a required file failed; the report is not a green certification. Skips remain unpassed. The fresh JUnit report and runner are in the local temporary `cairn-v07-cert-20261112-results` directory.

Five failures have focused passing corrections: ordinary plan-revision routing (`1701c6dd`, five cases), two stale hook-index injection wrappers (`07851a95`, two cases), and installation hash renewal plus the advisory fixture's newly earlier containment refusal (`d9708a0d`, seven cases). I inspected the changes: amendment authority still stops incomplete records, hook-index production code is unchanged, and hostile source paths remain refused. No replacement suite ran. The final neutrality/redundancy gate passed; the prose gate found one archive link, corrected with its affected-file check.

The remaining AST failure reports 21 changed baseline symbols, no missing or duplicate symbols, and 153 new symbols. The forward packet prepares a current correction without changing baseline membership or moving refs; independent readers assess it before the Maintainer's existing approval flow. AST correction, any still-required release checks, signing and publication remain release work. There is no claim that the original failing report has become green.

Maintainer transfer authorization, chat 2026-11-12:

> All transfers to and from VM are authorized

### Delivery order

Scheduling adds no scope or implementation authority, and rows saying "propose" still need their own accepted contract. The Maintainer approved the sequence on 2026-11-04 and moved only item 7c to v0.8: *"Let's move #7c to v0.8."* Later authoring and review keep their task-specific model floors.

Completed rows stay visible after their artifacts are archived, with **Complete** below the title. The label adds no lifecycle state. Maintainer chat, 2026-11-04: *"Rather than removing the items, will you add a bold complete under each one so I can easily see where we are at"*.

The second table is in the order to do the work (Maintainer, 2026-11-10: two tables, completed rows first). Its Step column gives the order, and letters are threads that can run in parallel, not instructions to edit the same file at once. Independent work advances when its named dependencies are ready; there is no whole-batch waiting gate. Use one writer where parallel lanes meet in shared templates and in session, gauge and install-registry edits.

The two tables below own the current order. The
[coordination note](strategy/2026-11-02-codex-v07-delivery-sequence.md)
keeps the strategy-retirement table; it is not a second work queue. Item
identifiers stay stable, and former row 7c (scientific-software dimensions and
governance) moved to v0.8.

Open Issues checked 2026-11-12: #52 and #60 are closed with implemented outcomes in rows 7e and 14/22. New #58–#59 have the v0.8 scientific-evidence proposal home, and #61 was closed on 2026-11-13 with the completed verification-guidance work in v0.7 below. #19 is in v0.8 and #34 in v0.9. The implemented Windows path fix #55 is now closed with its fixing commit and recorded native evidence; #54 and #56–#57 were already closed. #46–#51 and #53 are closed.

#### Completed in v0.7

| Work | What shipped | Record |
|---|---|---|
| **1a. Leaner reviews and finding-driven revisions.** (completed)<br>**Complete** | Reviews keep the three evidenced answers and drop repeated metadata; revisions follow findings. Readability wording moved to row 3. | [Archived proposal](proposals/archive/2026-11-03-claude-leaner-reviews.md); Maintainer chat, 2026-11-03: *"Go with one light proposal."* |
| **1c. Achievable plans with SMART goals.** (completed)<br>**Complete** | Guidance teaches achievable goals that can finish independently, without splitting work by default. | [Archived plan](plans/archive/2026-11-05-smart-goals.md); [accepted proposal](proposals/archive/2026-11-05-codex-atomic-implementation-plans.md); Decision `1fe81f7a`; Maintainer chat, 2026-11-05: *"The idea isn't to \"split work\", it's to make plans achievable. SMART goals"* |
| **2a. Consolidate the expensive test families without losing detection.** (completed)<br>**Complete** | The expensive test families run faster with the same detection. Release certification is separate. | [Archived plan](plans/archive/2026-11-04-suite-consolidation.md); [accepted proposal](proposals/archive/2026-11-02-codex-suite-consolidation.md) |
| **2c. Share claims across a clone's worktrees.** (completed)<br>**Complete** | Linked worktrees of one clone share the claims log; other layouts fall back locally with a stated reason. | [Archived plan](plans/archive/2026-11-04-shared-claims-across-worktrees.md); [accepted proposal](proposals/archive/2026-11-03-claude-shared-claims-across-worktrees.md); [coordination limits](../docs/methodology/coordination.md#scope-and-limits); Maintainer chat, 2026-11-03 |
| **2e. Local development environment notes for adopters.** (completed)<br>**Complete** | Adopters get an optional, untracked note for machine-specific setup facts, with manual checks that keep it private. A synthetic trial gave three eligible answers and sixteen declines; that is not a human usability measure. The Maintainer waived the single-final-commit wide test run (2026-11-11) and allowed a scope delta that leaves core `AGENTS.md` with one pointer line. | [Plan](plans/archive/2026-11-09-local-development-notes.md); [accepted proposal](proposals/archive/2026-11-04-codex-local-environment-notes.md); [#54](https://github.com/MSUHydrogeology/cairn/issues/54) |
| **2f. Deliver onboarding tasks once, without managing the board.** (completed)<br>**Complete** | Installation and first adoption deliver onboarding tasks once and leave project-owned board text alone. | [Archived plan](plans/archive/2026-11-05-one-time-onboarding.md); [accepted proposal](proposals/archive/2026-11-04-codex-one-time-onboarding.md); Decision `2a233544`; integration `3c7cbfc2`; verified commit `88679232`. |
| **2g. Fast goodnight checks, explicit slow-test triggers.** (completed)<br>**Complete** | Full handoffs run the configured quick check and report its limits; reflection-only work adds no test run. Slow and release checks keep their triggers. | [Archived plan](plans/archive/2026-11-05-fast-goodnight-testing.md); [accepted proposal](proposals/archive/2026-11-05-codex-fast-goodnight-testing.md); Decision `65b723fc`; verified commit `88679232`; [#53](https://github.com/MSUHydrogeology/cairn/issues/53). |
| **3. Readable, implementable plans that finish cheap follow-ups.** (completed)<br>**Complete** | Plans are readable and implementable, and finishing work resolves cheap follow-ups and updates the roadmap and changelog. Issues #46-#50 are closed. | [Archived plan](plans/archive/2026-11-06-readable-work-artifacts.md); [accepted proposal](proposals/archive/2026-11-04-codex-readable-plans-and-finish-work.md); Decision `27300e1e`; final verification `503f78af`. |
| **3a. Clear summaries of what will be built.** (completed)<br>**Complete** | Proposal, plan and strategy summaries name the material outputs within their budgets. Human usability is unmeasured. | [Proposal](proposals/archive/2026-11-06-codex-concrete-delivery-summaries.md); Maintainer chat, 2026-11-06: *"I love the Decision Summary in proposals. Can we extend it to clarify what is being built: new/removed tools, docs, etc.? Also, a similar Build Summary at the top of plans would be helpful for me. Can we get a similar Summary in strategy docs?"* |
| **3b. Bounded execution retries for adopters.** (completed)<br>**Complete** | Agents get up to two correction attempts at the same model level before moving up; capability, authority and review limits are unchanged. Issue #51 is closed. | [Accepted proposal](proposals/archive/2026-11-05-codex-adopter-execution-retries.md); [#51](https://github.com/MSUHydrogeology/cairn/issues/51); Maintainer chat, 2026-11-05: *"There's a new Cairn issue, #51. Please put this up on the v0.7 board"*; *"Go ahead and change the retry rule here, too."*; *"Just do the Cairn local version and then the full implementation can cover the rest"*. |
| **4. Finish agent-owned work without waiting for human operations.** (completed)<br>**Complete** | Plans finish when agent-owned scope, reviews and checks are done. Human trust and release operations are separate, evidence-backed board waits. | [Archived proposal](proposals/archive/2026-11-03-codex-implementation-plan-completion.md); [Archived plan](plans/archive/2026-11-04-implementation-plan-completion.md); Decision `e2aae09f`, Terra review `9b59ba4e`; Maintainer chat, 2026-11-03: *"Issues don't require releases. They require features and fixes. Releases are packaged sets of such things."* |
| **5. Permit only specifically authorized extra Security Review passes.** (**Complete**) | Extra Security Review passes need specific Maintainer authorization. Independently reviewed agent examples stood in for the human trial. | [Proposal](proposals/archive/2026-11-02-codex-security-review-pass-limit.md); [Archived plan](plans/archive/2026-11-04-security-review-pass-limit.md). |
| **6. Meaningful scientific tests and observable acceptance criteria.** (completed)<br>**Complete** | Testing guidance and examples cover scientific inputs and observable acceptance criteria. Automated checks are change evidence, not scientific validation. | [Proposal](proposals/archive/2026-11-02-codex-fault-centered-testing.md); [Archived plan](plans/archive/2026-11-04-fault-centered-testing.md); [Strategy](strategy/archive/2026-11-02-claude-outside-practices-for-better-software.md#tests-that-catch-real-faults); [acceptance guidance](strategy/archive/2026-11-02-claude-outside-practices-for-better-software.md#testable-acceptance-criteria) |
| **7a. Repair the strict release-security runner.** (completed)<br>**Complete** | The strict release-security runner records Mac and Windows results separately and joins them at one commit. The actual same-commit release records are a release wait (item 12). | [Archived plan](plans/archive/2026-11-05-strict-release-security-runner.md); [accepted proposal](proposals/archive/2026-11-05-codex-strict-release-security-runner.md); Decision `d042dd33`; mode allowance `210e2501`. |
| **7b. Tighten Plain Language for scientific and technical writing.** (completed)<br>**Complete** | Cairn Plain Language 1.1 is delivered in the governing, public and installed copies. Human usability is unmeasured; the January 2027 evaluation is tracked separately. | [Archived plan](plans/archive/2026-11-06-scientific-plain-language.md); [Strategy](strategy/archive/2026-10-27-antigravity-plain-language-and-scientific-writing.md#part-3-the-specific-gaps-to-close-for-direct-use-in-assai); Maintainer chat, 2026-11-04: *"Keep the tightening in v0.7. Add what you need based on your reading here."* |
| **8b. Agents that continue through authorized work.** (completed)<br>**Complete** | Agents continue through authorized work. A synthetic comparison established neither a prompt reduction nor a usability benefit. The optional loop and budget guard moved to the v0.9 proposal. | [Archived plan](plans/archive/2026-11-05-agent-continuation.md); [v0.9 proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [accepted proposal](proposals/archive/2026-11-03-claude-agent-continuation.md); Maintainer dispositions `896f2ac2`, `d0d82446`. |
| **9. Configuration-backed scanner cleanup.** (completed)<br>**Complete** | Scanner link and reference exceptions can live in validated settings files, with warning-only finding labels. Release certification is separate. | [Archived plan](plans/archive/2026-11-05-configuration-backed-scanner-cleanup.md); [accepted proposal](proposals/archive/2026-11-05-codex-configuration-backed-scanner-cleanup.md); Decision `92954c29`; settings-file allowance `0573c42c`. |
| **10. Consistent lifecycle guidance.** (completed)<br>**Complete** | Public and installed guides, the lifecycle diagram and the skills describe the same supported routes. The unsupported standalone-note promise is retired. | [Archived plan](plans/archive/2026-11-06-lifecycle-guidance-reconciliation.md); [accepted proposal](proposals/archive/2026-11-06-codex-lifecycle-guidance-reconciliation.md); Decision `e05c64fe`. |
| **11. Human-useful ceremony output and return on attention.** (completed)<br>**Complete** | Ceremony prompts explain purpose, risk and the exact approval while keeping comparison values visible. Real release operations are separate. | [Archived plan](plans/archive/2026-11-06-human-useful-ceremony.md); [accepted proposal](proposals/archive/2026-11-06-codex-human-useful-ceremony.md); Decision `036a0495`. |
| **16. Documentation for people using Cairn through chat.** (completed)<br>**Complete** | People using Cairn through chat get upgrade and session documentation written for them: a 22-file change, reviewed twice, with two agent journey checks passed. The Maintainer waived the single-final-commit wide test run (2026-11-11); that run is not a passed check. | [Plan](plans/archive/2026-11-09-person-facing-documentation.md); [accepted proposal](proposals/archive/2026-11-08-terra-person-facing-documentation.md); [#56](https://github.com/MSUHydrogeology/cairn/issues/56); [#57](https://github.com/MSUHydrogeology/cairn/issues/57) |
| **17. Achievable plan prerequisites.** (completed)<br>**Complete** | Plans use available prerequisites and queue unavailable approvals and passive calendar waits; required evidence, ready scientific work and unexpected permission stops stay in the existing rules. The 19-file joined map had 624 passes, and three onboarding-copy tests passed later at `ad508d15`. The Maintainer waived the single-final-commit wide run (2026-11-11), which is not a passed check; 32 guarded AGENTS readers stay omitted. | [Plan](plans/archive/2026-11-09-achievable-plan-prerequisites.md); [accepted proposal](proposals/archive/2026-11-09-terra-achievable-plan-prerequisites.md); Maintainer chat, 2026-11-09 and 2026-11-10; `97a0eab3`; `088d4721`. |
| **20. The next-step advisor stopped on a mistyped release id and gave the wrong reason.** (completed)<br>**Complete** | `board.py --next` works again. `intent release` now refuses an id that matches no claim and names the closest real ones, and the board says why it stops. Fix `b9a04a72`; the Maintainer waived a clean-commit test rerun, so none exists. | Maintainer chat, 2026-11-10: *"do parts 1-3 to fix this issue"*; `b9a04a72`; [accepted proposal](proposals/archive/2026-11-06-codex-repeated-claim-releases.md); `tools/board.py`, `tools/_intent/cli.py`. |
| **23. Ship a `RULES.md` router stub with every install.** (completed)<br>**Complete** | Installation seeds a project-owned starter and preserves existing rules and deletion choices. Focused public checks and ordinary/Security reviews passed; the plan is archived. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-12-rules-router-stub.md); [accepted proposal](proposals/archive/2026-11-12-terra-rules-router-stub.md); archive `add58405`. |
| **7d. Bound upgrade growth with a refusal rule and a Git trial.** (completed)<br>**Complete** | The refusal guidance is installed. The isolated comparison stopped before trial actions when the required isolation failed; the accepted incomplete-result route is documented, with no replacement-readiness claim. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-12-upgrade-growth.md); [accepted proposal](proposals/archive/2026-11-05-codex-upgrade-growth.md); archive `2334e214`, old-path cleanup `ad2bc17f`. |
| **7e. Make adopter release-signature verification an explicit choice.** (completed)<br>**Complete** | The ordinary release route and optional signature route are documented; local source, isolation and integrity controls passed and review findings are closed. Live adopter use and publication remain separate human operations. Issue #52 is closed; item 12 owns integration. | [Archived plan](plans/archive/2026-11-12-opt-in-release-verification.md); [accepted proposal](proposals/archive/2026-11-05-codex-opt-in-release-verification.md); archive `2c1ae99f`; [#52](https://github.com/MSUHydrogeology/cairn/issues/52). |
| **14. Promise-unit testing.** (completed)<br>**Complete** | Public-promise guidance, the advisory tool and eligible-family reductions are delivered and reviewed. The 15 held conversions are complete; 28 roster/source/parity/release guards remain in their current homes. Claims-family cuts remain conditionally excluded. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-08-promise-unit-testing.md); archive `546959c1`; [accepted proposal](proposals/archive/2026-11-08-claude-promise-unit-testing.md). |
| **22. Only promise tests stay in the suite.** (completed)<br>**Complete** | Development probes are temporary and permanent checks protect public promises. At committed `e45017ea`, definitions fell from 4,071 to 3,145 (926 fewer, 22.75%); this is source volume, not runtime or fault coverage. Both bounded post-cut comparisons and Security Reviews are complete. The temporary worklist is deleted; Issue #60 is closed. | [Archived plan](plans/archive/2026-11-08-promise-unit-testing.md); reviews `ff1acaeb`, `04444484`; [#60](https://github.com/MSUHydrogeology/cairn/issues/60). |
| **15. Functional-prose editing.** (completed)<br>**Complete** | Exact editing, a visible prose report and an installed replacer replace wording pins; drain, parity and real behavior checks remain. Report/output fixes and the later stale bindings have focused passing checks and completed dispositions. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-08-functional-prose-editing.md); archive `e45017ea`; tested repair `86a01163`, lock completion `0bb40e81`. |
| **2d. One safe Git helper for untrusted repositories.** (completed)<br>**Complete** | The shared helper and caller bindings are delivered with bounded subprocess cleanup and refusal checks. Capped-review repairs have the Maintainer disposition; Python 3.12 support is recorded separately. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-06-safe-git-reads.md); archive `12f74011`; [completed release-fix proposal](proposals/archive/2026-11-06-codex-repeated-claim-releases.md). |
| **8a. Architecture, reuse and the four-view visual pilot.** (completed)<br>**Complete** | Code mapping, helper-home guidance, legacy/new-system rubric and the owner guard are delivered and reviewed. The Maintainer moved the visual pilot to its v0.8 home; grouped strategy retirement remains with item 12. | [Archived plan](plans/archive/2026-11-05-architecture-and-reuse.md); archive `5efd2c45`; scope disposition `0eeb76b9`. |
| **24. Repair product defects exposed by public tests.** (completed)<br>**Complete** | Pre-write refusals, strict comparison normalization, parser cleanup and all 15 public conversions are delivered. Seven focused corrections passed and ordinary review closed the Security findings. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-12-public-contract-repairs.md); archive `c7fc8680`; repair `3e0b39c3`; review `896ccaa8`. |
| **25. Reduce unrelated test selections.** (completed)<br>**Complete** | The selector retains audited real lockfile/guide readers and excludes fixture-only references. The focused regression selection passed 214 cases; board and changelog edits select none. This is an audited mapping, not complete dependency discovery. Item 12 owns integration. | [Mapper](../tools/test_tiers.py); public selector contract `bootstrap/tests/contract/test_test_tiers.py`; implementation `a3c7b7cc`. |
| **2b. Meter real cost and report team/suite growth together.** (completed)<br>**Complete** | Opt-in collection, project/team pulse and synthetic accounting are delivered. Ordinary and capped Security findings are closed with focused corrections and prior native evidence. Private real-use comparisons and conditional Tokens retirement remain explicitly queued for v0.9; manual fields stay. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-04-metered-cost.md); archive `c526b47a`; [v0.9 work](proposals/2026-11-05-codex-budgeted-unattended-work.md). |
| **21. Support Python 3.12 in shipped tools.** (completed)<br>**Complete** | Mac, Linux and Windows core controls passed on actual 3.12 runtimes; Windows used x64 emulation. Installed-workflow fixtures, runtime guidance and digest repairs are reviewed, with focused checks passing. The 41 shipped Python files parse on 3.12. The blanket platform matrix was replaced by the Maintainer's current-arc direction, not claimed passed. Item 12 owns integration. | [Archived plan](plans/archive/2026-11-12-python312-support.md); archive `3b949bc1`; final ordinary review `0986bcaf`; [VM access](rules/development-environment.md). |
| **13. v0.7 weight review.** (completed)<br>**Complete** | Living plans and shorter records are implemented, exact editing replaces wording pins, and eligible tests were pruned. The Maintainer chose to keep Meter installed in core. No rule freeze or optional-module migration was adopted. Shared integration and grouped strategy retirement remain item 12 work. | [Weight review](strategy/archive/2026-11-06-claude-v07-weight-review.md); [living plans](plans/archive/2026-11-12-plan-records-and-living-plans.md); [Meter Decision](proposals/archive/2026-11-12-terra-meter-install-footprint.md). |
| **18. Old installs keep a retired key in `profile.yml`.** (completed)<br>**Complete** | The writer no longer restores retired `metrics_command`; the focused behavior check passed. The expected installer baseline update remains the separate release operation in item 12. | Fix `db8115d0`; Maintainer chat 2026-11-10; lane disposition above, decision 13. |
| **19. The plain install accepts an angle-bracket placeholder as a real value.** (completed)<br>**Complete** | Plain installation now rejects angle-bracket placeholders through the shared token check; its focused dry-run test passed. Stage/apply also refuse existing unfilled required values. The expected baseline update remains item 12. | Fix `f1c8f011`; Maintainer chat 2026-11-10; lane disposition above, decision 13. |
| **27. Release-route documentation snags.** (completed)<br>**Complete** | A fresh reader of the adopter docs reached ordinary installation and upgrade without any key approval, so the item 7e promise holds. The snags it found are repaired: `f4cf8e1c` (the default route, how to find the newest tag, the POSIX-shell note, the SECURITY.md and quickstart labels) and `6b7af99d`, `afb3ddf1` and `b2adf8c0` (verify before you edit, then record each edited file with `--finalize`, then verify again, in PROVENANCE, BOOTSTRAP, README and UPGRADE; the rule that a failed signature-route check never falls back; a start-here pointer in UPGRADE). The order came from the tools themselves (`verify_integrity.py`, `upgrade --finalize`), and no product defect was found. An ordinary review returned REVISE (applied) and a Security look returned ACCEPT; no second pass. Two small items moved to v0.8 (Maintainer, 2026-11-13): (1) the scaffold's printed next-steps list (`bootstrap/_scaffold/install.py` near line 2000) has no verify step, so someone following only that list skips the pre-edit check; it is code and an engine file, so it needs its own lane; (2) no PowerShell route exists, so Windows adopters use Git Bash. My earlier statement here that README.md and UPGRADE.md are lock-pinned was a grep miscount: neither is pinned or on a protected roster. Tests run: the nine files that name the edited guides, 334 passed. | [Archived plan](plans/archive/2026-11-12-opt-in-release-verification.md), Dispositions; Maintainer chat, 2026-11-13: "Okay, I want these items powered through. LFG!" |
| **26. Consistent focused verification for v0.7.** (completed)<br>**Complete** | Guidance, templates and public explanations now use focused public-promise checks, applicable evidence reuse and arc-level integration. Within an authorized arc, the coordinator chooses shared or separate planning/review coverage; all required assurance remains covered. Focused delivery checks and prose gates passed; no full suite reran. | [Archived plan](plans/archive/2026-11-13-focused-verification.md); [accepted proposal and Maintainer clarification](proposals/archive/2026-11-12-codex-focused-verification-cost.md); initial implementation `19ffac65`/`12ba3fab`, final clarification `2b27386e`; [Issue #61](https://github.com/MSUHydrogeology/cairn/issues/61) closed. |

#### In flight or not started, in the order to do them

All opened implementation plans are archived, including the focused-verification guidance. The remaining release follow-ups and future real-PR trial are below; their recorded scope remains. The bold numbers remain stable names for existing records.

| Step | Work | Next step | Record |
|---|---|---|---|
| 2e | **1b. Check instruction changes at pull-request merge.** (active)<br>**Implementation complete** | Implementation, scoped checks and joined final check are complete. Only the next qualifying real merged-PR trial remains. Keep it at merge time, with the merger's trusted scanner and human outcome judgment; add no pre-push or per-commit scan. | [Proposal](proposals/2026-11-03-claude-pr-merge-instruction-check.md); Maintainer chat, 2026-11-03: *"if I'm developing here I don't need to scan for prompt injection changes. But when I merge a PR, yes. But DON'T add mandatory scans before pushes"*; [content-security module](../templates/modules/team-gated/content-security.md) |
| 3 | **29. Windows test failures found by the native rerun.** (tests fixed 2026-11-13; one product defect and a roster refresh remain) | The native Windows rerun (record: `dev/measurement/windows-native-rerun-2026-11-13.md`) found 59 distinct failing tests that are not Windows-only roster nodes. They were test assumptions or VM setup gaps, and none was a product defect except one (item 31). Fixed in the tests only, with no assertion or roster entry changed: 42 in the first pass (`cef31650`, `26f89462`, `ac4c5c15`; three by Windows skips that name the native control) and 15 more plus the 16 web-hosting setup errors in the second (`bf5086c6`, `21803edf`, `803046ab`, `4a9a2542`, `9fd4ed9a`), each checked on the VM's x64 `lhm` environment and, for the edited files, on the Mac (454 and 305 passed). The helper children of the roster-family tests now carry `SYSTEMROOT` and `WINDIR` on Windows, a missing `openssl` is found under Git for Windows, and fixtures write bytes. `test_model_selection_stub.py` fails only in the ARM64 base environment, which lacks PyYAML: Windows runs use the x64 `lhm` environment (documented). Still open: (1) item 31, the `t6` test, a real defect; (2) the roster: a strict Windows release record validates every collected node, so each POSIX-only skip must be a posix-roster entry, and of 72 to 76 Windows skips in the files run, 55 to 56 are not (15 in `test_git_read.py`, 39 in `test_meter.py`, 1 to 2 elsewhere); listing them is a roster change in the byte-pinned `bootstrap/tests/security_manifest.py`, so it is the Maintainer's call (see the release-candidate Decision under Waiting on you); (3) the other 15 Windows-only roster nodes were not run, and files I did not run were not scanned for unlisted skips. | `dev/measurement/windows-native-rerun-2026-11-13.md`; Maintainer chat, 2026-11-13: "yeah we really shouldn't have a bunch of failing tests around. Please farm that out" |
| 3 | **31. Security-audit descendants outlive a timeout on Windows.** (found 2026-11-13 by the Windows rerun; a fix is being built) | `_run_tool` in the shipped `run_security_audit.py` cleans up a timed-out tool's descendants with a POSIX process group, and its own docstring says Windows is untested. On Windows a grandchild survives, keeps a temporary file open, and the temporary-folder cleanup raises `PermissionError: [WinError 32]` out of `_run_tool`, so the `timeout` status is never returned. The test `bootstrap/tests/test_security_stack.py::test_a_t6_descendants_do_not_outlive_the_timeout` reproduces it natively. A fix job (Windows Job Object with kill-on-close, POSIX path unchanged) is running; it is a shipped security-audit module, so it needs an ordinary review and a Security look before it lands. | `dev/measurement/windows-native-rerun-2026-11-13.md`; Maintainer chat, 2026-11-13: "Please farm that out" |
| 4 | **12. Integrated release verification and grouped strategy retirement.** (in progress) | The single certifying run at clean isolated `072d82d2`, Python 3.13.13, finished: 5,344 passed, 63 skipped, six failed in 49m06s. Five failures have focused passing corrections; the AST baseline remains unpassed pending the separate release correction. See the verification summary below. No replacement suite is planned. The release-closeout agent joins the completed ranges and existing evidence, performs the remaining required release checks, and coordinates human-only trust/publication operations separately from implementation-plan completion. Item 26 is complete. Refresh the final candidate packet and affected reader bindings once remaining release fixes are committed; reuse unchanged AST body analysis rather than repeatedly binding intermediate candidates. Owed checks named 2026-11-13, after a read-only review of the archived plans (Maintainer: "The rest you just take care of, please. I don't want loose ends left around."): (a) done 2026-11-13 (`3184f6c7`): an inventory of every Git-reading route and one public-entry check per route that lacked one (20 new cases in `bootstrap/tests/security/test_git_read_routes.py`, each shown to fail under one scratch fault; the other routes already had checks), under the accepted focused-verification guidance. It found item 30. It skips on Windows (the git stand-in is a script), so route-level Windows evidence is still missing; (b) Windows native reruns after the final changes: run 2026-11-13 at `bf1d7bff` on the VM the Maintainer authorized ("All transfers to and from VM are authorized"), on native ARM64 and x64 Python 3.13 (record: `dev/measurement/windows-native-rerun-2026-11-13.md`). The 48 Windows-only roster nodes in the files run (Meter, safe Git and prose tools among them) all passed; the other 15 `nt` roster nodes are in files not run; the 59 other failures are item 29 (fixed in the tests; item 31 and the roster refresh remain); (c) done 2026-11-13: the mapped installed-workflow checks on macOS Python 3.12.9, run from a clean copy of `bf1d7bff`, gave 252 passed and 12 skipped (the skips are the Windows-only worker controls) and none failed, which settles the four unitemised failures of an earlier bounded run; (d) three protected test files were deleted, not six (`test_loader_identity.py`, `test_lockfile_module.py`, `test_slotmerge_leaf.py`; 21 test IDs), the protected roster is byte-pinned so those names stay in it unless the Maintainer approves a new roster, and 2,466 of the 5,913 signed test IDs no longer exist; the exact lists and the Maintainer's eleven steps are in `dev/measurement/reanchor-prep-2026-11-13.md`; (e) after the re-anchor, decide whether to retire the 28 kept guard tests (Maintainer, 2026-11-12: "retire now unless it disrupts the re-anchor"; they stayed because retiring them would disrupt it). Batch frozen edits before required ceremonies where permitted; preserve every required check and byte-review boundary. Nine completed strategy notes are archived (`8669b8b4`); the sequence stays live until release, visual review stays for its v0.8 pilot, and the broad security register remains active. Global live links are repaired. No new release plan or per-note backlog rows. The Maintainer's release baseline operation also settles the two expected AST checks that rows 1c and 2f left unpassed. | [Retirement ownership](strategy/2026-11-02-codex-v07-delivery-sequence.md#retirement-ownership); [proposal owner](proposals/archive/2026-11-02-codex-architecture-and-reuse.md); Maintainer chat, 2026-11-03 |

2a slow-family evidence includes the 2026-11-04 2c final wide run: [archived Boundary B record](plans/archive/2026-11-04-shared-claims-across-worktrees.md#implementation-verification----codex-terra-implementation-medium----2026-11-04).


**Consolidation candidates, slowest first.** These are JUnit case-time sums from the single `072d82d2` certification run on Python 3.13.13, not whole-file wall times. All 51 owners above the 10-second diagnostic target are listed. The full run took 49m06s; this does not establish a speed improvement over earlier differently selected runs. This existing diagnostic list neither reopens completed plans nor adds another test run.

| Test owner | Case-time sum |
|---|---:|
| `bootstrap/tests/test_repin_ceremony.py` | 425.10 s |
| `bootstrap/tests/test_upgrade.py` | 239.96 s |
| `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py` | 161.77 s |
| `bootstrap/tests/test_gate_preflight.py` | 145.61 s |
| `bootstrap/tests/test_upgrade_module_additions.py` | 139.39 s |
| `bootstrap/tests/test_repin.py` | 135.37 s |
| `bootstrap/tests/test_intents_tool.py` | 125.94 s |
| `bootstrap/tests/test_portable_security_sweeps.py` | 120.63 s |
| `bootstrap/tests/security/test_prose_tools.py` | 84.85 s |
| `bootstrap/tests/test_security_stack.py` | 82.38 s |
| `bootstrap/tests/test_upgrade_removes_retired_files.py` | 75.71 s |
| `bootstrap/tests/test_reference_scripts.py` | 67.04 s |
| `bootstrap/tests/test_oracle.py` | 64.50 s |
| `bootstrap/tests/test_session_kernel.py` | 63.12 s |
| `bootstrap/tests/test_security_verification.py` | 52.09 s |
| `bootstrap/tests/test_reanchor.py` | 49.76 s |
| `bootstrap/tests/test_security_check.py` | 44.24 s |
| `bootstrap/tests/security/test_git_interpreter_binding_portable.py` | 42.24 s |
| `bootstrap/tests/test_install_time_onboarding.py` | 41.98 s |
| `bootstrap/tests/test_session_binding_untracked.py` | 41.52 s |
| `bootstrap/tests/test_session_writes_contained.py` | 40.69 s |
| `bootstrap/tests/test_session_failsafe.py` | 26.83 s |
| `bootstrap/tests/test_onboarding_seed_roster.py` | 24.83 s |
| `bootstrap/tests/security/test_code_map.py` | 22.70 s |
| `bootstrap/tests/test_security_net.py` | 22.60 s |
| `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` | 22.23 s |
| `bootstrap/tests/test_onboarding_slot_substitution.py` | 20.72 s |
| `bootstrap/tests/test_profile_grammar.py` | 19.63 s |
| `bootstrap/tests/test_doc_drift_tools.py` | 19.50 s |
| `bootstrap/tests/test_upgrade_added_slots.py` | 17.68 s |
| `bootstrap/tests/test_gate_reanchor.py` | 17.49 s |
| `bootstrap/tests/test_ceremony_review_report.py` | 17.29 s |
| `bootstrap/tests/test_scaffold.py` | 17.25 s |
| `bootstrap/tests/test_security_finding_confidentiality.py` | 17.17 s |
| `bootstrap/tests/test_status_vocabulary_advisory.py` | 15.50 s |
| `bootstrap/tests/test_session_binding_gate_and_printing_hold.py` | 14.99 s |
| `bootstrap/tests/test_incident_trackers_module.py` | 14.56 s |
| `bootstrap/tests/test_engine_copy_fallback_contained.py` | 14.04 s |
| `bootstrap/tests/test_gate_manifest.py` | 13.77 s |
| `bootstrap/tests/test_model_selection_stub.py` | 13.62 s |
| `bootstrap/tests/security/test_git_read.py` | 12.82 s |
| `bootstrap/tests/test_web_hosting_security.py` | 12.22 s |
| `bootstrap/tests/test_upgrade_side_door_parity.py` | 11.84 s |
| `bootstrap/tests/test_skills_security.py` | 11.64 s |
| `bootstrap/tests/test_security_capability_install.py` | 11.54 s |
| `bootstrap/tests/contract/test_test_tiers.py` | 11.43 s |
| `bootstrap/tests/test_broad_run_guard.py` | 10.75 s |
| `bootstrap/tests/test_board_json_contract.py` | 10.70 s |
| `bootstrap/tests/test_upgrade_lockfile_path_containment.py` | 10.68 s |
| `bootstrap/tests/test_session_routines.py` | 10.51 s |
| `bootstrap/tests/integration/test_gauge.py` | 10.31 s |

### Batching the verification

- Plans keep separate accepted outcomes and owed reviews. Group editing and
  test preparation where they share real surfaces, not the review authority.
  The spawning agent owns the joined verification; workers receive scoped
  checks, not repeated whole-tree runs.
- Select affected checks with `tools/test_tiers.py for <changed paths>`.
  At a natural post-review join, run the valid union once on the clean final
  commit and link that result from each covered record. Reuse evidence only
  while the covered bytes, inputs, environment and consumers are unchanged;
  review fixes get their required targeted look and affected recheck.
- Keep mutable fixtures independent and share immutable setup. Use the
  existing reporting owner in 2b; add no second collector or evidence ledger.
- Required scientific, security and release checks remain required. Run full
  certification only at its existing authorized points, not per item or
  review. Group protected edits when permitted so one reviewed ceremony can
  cover several completed implementations; this grants no signing authority.
  A known unmet check remains open, not a promise of a later green suite.

## v0.8 — settle the structure and ship the oversight tool

Retain the following work, sequenced after v0.7 rather than discarded. v0.8 settles Cairn's structure once: the repository layout and the work that lands in its new homes, the oversight tool, the scientific-software framing and the release safety checks. Incoming defect reports still receive normal triage, and no required release or correctness check is waived by this schedule. Maintainer direction, 2026-11-10: the oversight website is in v0.8 as an opt-in module, and outside-adopter feedback and the autonomy work are in v0.9, below.

The four-view visual pilot moved here by the Maintainer's recorded scope disposition (`0eeb76b9`); completed architecture guidance stays in v0.7. Any upgrade-engine replacement needs its own accepted proposal; the incomplete v0.7 comparison establishes no replacement readiness.

Scientific-software dimensions and governance also move here by the
Maintainer's 2026-11-04 instruction. This delays that broader framing, not
v0.7's scientific-testing guidance or any required correctness check. It follows the repository layout, because the deliverable axis edits `dimensions/`, which the layout moves into `install/`.

| Work | Next step | Record |
|---|---|---|
| **Repository layout: one folder per purpose, Cairn self-contained under `dev/`.** (accepted for v0.8) Rename `bootstrap/` to `install/`, move Cairn's tests and release machinery to their own folders, keep `templates/` to exactly what installs, and install every tool into one tools folder under `dev/`. Cairn adopts itself through its own installer. | Ordinary and Security reviews and revision are complete; the recorded Decision accepts the revised migration, self-lock reconciliation and trust transition. Heavy tier; open implementation at the start of v0.8 with no plans in flight, retaining all eleven outcomes and the separate Maintainer re-anchor. The placement assessment below remains explicit in the proposal. | [Accepted proposal](proposals/2026-11-09-claude-repository-layout.md); revision `68abed30`; recorded Maintainer Decision, 2026-11-12. |
| **Clear guide audiences and homes for Cairn-only procedures.** (accepted for v0.8) Organize guide navigation into Using Cairn, Reference and Contributing to Cairn; place the release procedure beside release machinery and separate internal count-maintenance instructions from adopter tool usage. Keep useful technical references in `docs/`. | Ordinary review and revision are complete and the Decision accepts the light companion proposal. Implement after the repository layout supplies its homes; preserve release duties, reconcile the documentation map and repair links without another guide hierarchy. No implementation started. | [Accepted proposal](proposals/2026-11-09-codex-docs-audience-and-homes.md); revision `6c8e1667`; recorded Maintainer Decision, 2026-11-12. |
| **Build out `examples/`.** (accepted for v0.8) Expand the minimal and scientific examples into runnable walkthroughs of a light change, a planned scientific change, adoption/upgrade and a handoff. Keep runnable examples at the root, distinct from installed templates. | The Maintainer released review in the 2026-11-12 batch; ordinary review, revision and acceptance are complete. Plan in v0.8 after layout and a local prior-release fixture are available. The upgrade demonstration must preserve a genuinely managed customization, not merely leave an unrelated file alone. No implementation started. | [Accepted proposal](proposals/2026-11-09-codex-worked-examples.md); [Examples](../examples/); revision `f0029dd9`; recorded Maintainer Decision, 2026-11-12. |
| **Ship `token_budget` and `verify_counts` to adopters.** (queued; proposal to write) `token_budget.py` joins the `documentation-plan` module and `verify_counts.py` joins `claim-check` with an empty registry, each with its doctrine paragraph; `audit_report.py` stays Cairn-only. | Write the proposal after the repository-layout plan lands, so both install straight into the new tools folder under `dev/`. | [Layout proposal, queued outcome](proposals/2026-11-09-claude-repository-layout.md#proposal); Maintainer chat, 2026-11-09 (shipping question answered "yes") |
| **One local oversight website with tabs: the release board and the code-change views.** (v0.8 proposal to write) | Maintainer direction, 2026-11-10: both the visual release board and the four-view pilot are graphical tools that help a person oversee the work, so build them as a single local website with tabs. One tab mimics the work tracker used in chat: completed work, implementation versus review and verification, blockers, dependencies and who acts next, generated from `board.py --json`, `git` and `gh` instead of kept by hand. Another tab carries the four-view pilot of code changes, postponed from the architecture plan (item 8a, C3), using LHM's scope-map page (`lhm/tools/scope_map.py` and `scope_map.html`) as the example. That page fills one HTML template with data, but it loads its drawing library and fonts from the internet, which this tool must not. Working assumption: one command writes one self-contained HTML file with the data embedded and no network needed. It works the same across agent tools, needs no vendor chat or hosted artifact, separates observed state from inferred progress and shows freshness. It builds on the board's JSON output and the board-view guide (`docs/build-a-board-view.md`). Consider a `passes` field only if the derived view shows the need, and keep no second hand-maintained source of status. The code-change tab waits on the reviewed safe-Git helper. Maintainer direction, 2026-11-10 (v0.8, as a module): ship it as an opt-in Cairn module that adopters choose in their profile's module list, not a default-on install. Reason: the v0.7 weight review found unconditional installs (`meter.py`, `git_read.py`) adding weight for every adopter. It installs into the single tools folder under `dev/` with its guide in `dev/modules/`, so it installs once. Whether the first slice starts before or after the layout lands is undecided; decide when v0.8 opens, using the layout's Decision state (see the dashboard design note). The layout test must count the module's files as install destinations. The Maintainer already uses a version of this tool in several projects; the module can start from those. Open for the proposal: which presets, if any, offer it by default. Maintainer direction, 2026-11-10: this is a dashboard for a person, showing at a glance how the project is and how it is changing, so they can monitor its growth. Five tabs: Development (the tracker above), Sankey diagrams of where work lands, Complexity, Growth over time (complexity and effort series), and Security (how the security-relevant surface is changing, with a since-last-release drill-down). Design every widget now, marked ready, partial or placeholder; ship a small first slice and grow it. Claims and agent-facing controls are out. Tokens stay placeholder until the v0.9 meter comparisons. | [Strategy note on this site](strategy/2026-11-10-claude-local-oversight-website.md); [earlier tracker strategy](strategy/2026-10-26-claude-work-tracker-and-the-board.md#recommendation); [architecture plan, C3](plans/archive/2026-11-05-architecture-and-reuse.md); Maintainer chat, 2026-11-09: *"I'm really finding myself needing a better visual tool to use to see where we are on development toward a version release. I want something that works the same across agents. This is a pain point."*; 2026-11-10: *"I want a single local website with tabs that mimicks the behavior of your artifact tracker tool here for the release board, and the example I passed for the four-view pilot of code changes."*; later 2026-11-10: *"I would like the oversight website in v0.8. We need a graphical tool. I've been using one in multiple projects and want this to be a Cairn module."*; [Oversight dashboard design](strategy/2026-11-10-claude-oversight-complexity-and-effort-tabs.md); same day: *"We can design it with widgets that don't quite work yet, and/or plan to make them work in v0.8."*; *"it's a dashboard, informing the user at a glance how things are and how they are changing. This is a tool so that a person can monitor the growth of their project."*; *"We will inevitably add/change/delete with time. But the key is to get it going so it can become useful."* |
| **Scientific-software dimensions and governance (#19; former 7c).** (deferred, Nov 2026) | In v0.8, propose the remaining doctrine sentence, deliverable axis, discipline list and governance reframe using existing project evidence and the delivered scientific-testing examples and architecture rubric. Preserve the full remaining scope; the separate outside-adopter trial is not a completion claim or a new prerequisite. Start after the repository layout lands, so edits to `dimensions/` land once in `install/`; if the axis becomes a machine-read profile axis it also touches the install contract (`bootstrap/_scaffold/config.py`) and would be heavy. | `independent-scientific-check` plan; [Issue #19](https://github.com/MSUHydrogeology/cairn/issues/19); Maintainer chat, 2026-11-04: *"Let's move #7c to v0.8."* This replaces only this item's earlier v0.7 scheduling. |
| **Scientific run evidence and accepted reference runs.** (v0.8 proposal to prepare) Evaluate stage-artifact comparisons for structural changes and a standing accepted reference run for each scientific model/mode. | The proposal author should reconcile #58 and #59 with current Verification guidance: identify when an artifact comparison is sufficient, how an immediate pre-change A/B isolates the change, where reference inputs/results live and who accepts a new reference. Preserve named scientific runs and required checks until a reviewed proposal changes them; these Issues grant no exception. | [Issue #58](https://github.com/MSUHydrogeology/cairn/issues/58); [Issue #59](https://github.com/MSUHydrogeology/cairn/issues/59); captured 2026-11-12. |
| **Secrets scanning in the release checklist, on Mac and Windows, and a better procedure for it.** (v0.8 proposal to write) | Add a secrets scan of Cairn's current files and Git history to `docs/release-process.md`, "Checks to run", and improve how the scan is run and read. Today no release step runs it: the checklist does not name it, the strict release check (`bootstrap/security_check.py`) runs the test orders, neutrality, redundancy, Bandit and the document check but not Gitleaks, and nothing runs it automatically. The scanner exists (`scripts/run_portable_security_sweeps.py`). Its approved-build list is empty (line 242), so a run reports findings but can only say "incomplete", never "clean". The module doc asks the Maintainer or a delegated Security Reviewer to evaluate the newest Gitleaks 8.x at each release. Gitleaks 8.30.1 is installed on the Maintainer's machine (measured 2026-11-10). To settle in the proposal: which result counts as passing at a release while the approved list is empty, how approving a build fits the release, what is recorded with the release notes, and the Windows route. Windows is an equal partner, so a Windows scanner build must be approved too. Sol's Windows interpretation (`4245c997`) left Windows runs at "incomplete" and is overridden by that direction. v0.7 item 7a expects Mac and Windows release records at the cut. Not established: what, if anything, blocks a Windows full run, and whether the runner's other requirements work on Windows. Approving the Windows build is a Maintainer step at the release. No scan has been run on Cairn's own files and history for this row. | Maintainer chat, 2026-11-10: *"Add a v0.8 item for improving the secrets scanning procedure and adding it to our Cairn release checklist"*; `docs/release-process.md`; `dev/modules/portable-security-sweeps.md`; `scripts/run_portable_security_sweeps.py`. Maintainer chat, 2026-11-10: *"We want full windows support--it is an equal partner."*; *"We can postpone the secret scan thing for windows to v0.8, combined with the row there"*. |
| **A security scan of all shipped templates before each release; prose templates leave the high-risk list.** (accepted for v0.8) | Terra ordinary and Sol Security reviews and revision are complete. The recorded heavy Decision accepts A-D and explicitly acknowledges development-checkout exposure before the release read. Implement the actual protected-surface authority change, complete shipped-prose inventory and exact-candidate release read/rechecks while retaining code/installer-structure protection. Starter adopter scan roots remain unchanged. Open the v0.8 plan under its required ordinary and Security reviews; no implementation started. | [Accepted proposal](proposals/2026-11-10-claude-template-scan-and-risk-list.md); revision `42e8c6b1`; recorded Maintainer Decision, 2026-11-12. |
| **Finish the release-route documentation: two small items left from item 27.** (moved to v0.8) | (1) The scaffold's printed next-steps list (`bootstrap/_scaffold/install.py` near line 2000) has no step telling the person to run `verify_integrity.py` before editing, so someone following only that list skips the pre-edit check; it is an installer engine file, so it needs its own lane. (2) No PowerShell route exists for the ordinary or the signature-verified route, so Windows adopters use Git Bash; the commands were not run in Git Bash beyond checking that `sh`, `mktemp` and `awk` exist there. Not started. | `bootstrap/BOOTSTRAP.md` II-2; Maintainer chat, 2026-11-13: *"Do it, move them to v0.8."* |
| **28. Make the claims check warn only (the Maintainer's 2026-11-13 Decision 27).** (decided; moved to v0.8) | Change the default in `_read_enforce_mode` (`tools/_intent/conflict.py` and its twin `templates/modules/team-gated/_intent/conflict.py`) from `block` to `warn`; correct the two places that call `block` the shipped default (`docs/methodology/coordination.md` near line 262 and `templates/modules/team-gated/coordination-tiers.md` near line 153); change the tests that pin refusal (`bootstrap/tests/test_intents_tool.py`) or retire those that only test it; then lift the promise-testing plan's fence on the claims-tool tests. It changes a shipped default and an installed-engine file, so it needs a light proposal and a decision on the AST baseline. Moved to v0.8 by the Maintainer. The refusal only affects adopters who installed the opt-in commit hook (`docs/methodology/coordination.md`), and the change would add to the pending AST re-anchor. Not started. | Maintainer chat, 2026-11-13: "Go with warn only on the claims check"; `dev/rules/working-agreements.md` line 10; [promise-testing plan](plans/archive/2026-11-08-promise-unit-testing.md), Dispositions; Maintainer chat, 2026-11-13: *"Do it, move them to v0.8."* |
| **30. The intent hook installer runs plain `git` from `PATH`.** (found 2026-11-13; moved to v0.8) | `tools/_intent/hooks.py` `_git_hooks_path` (and its twin `templates/modules/team-gated/_intent/hooks.py`) runs `subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=<repo>)`, which finds `git` through `PATH`, not through the safe Git reader. The job reproduced it: with `.` first on `PATH`, `intent.py install-hook` ran a `git` script at the repository root; on Windows the search also starts in the parent's current folder. The function's own docstring calls it a deliberate exception (it must honor `core.hooksPath` to find the file install may change), so the earlier reviews may have accepted it; the safe-Git plan's promise was that no reader bypasses the helper. Only the opt-in `install-hook`, `install-precommit` and uninstall commands use it. Fix options: resolve Git through the safe reader's executable choice and a sterile environment, or document the exception. It is an installed-engine file, so it needs a light proposal, a Security look and adds to the pending AST re-anchor; moved to v0.8 by the Maintainer. A second small finding: the Markdown link and snippet checks end with an uncaught `RuntimeError` and exit 1 when the safe reader refuses a read in a hostile repository (never clean, but a traceback and the same exit code as ordinary findings). | `bootstrap/tests/security/test_git_read_routes.py`; `3184f6c7`; [archived safe-Git plan](plans/archive/2026-11-06-safe-git-reads.md); Maintainer chat, 2026-11-13: *"Do it, move them to v0.8."* |
| **Remove the testing of non-shipped components from the release process.** (v0.8 proposal to write) | Maintainer direction, 2026-11-13: *"for a release, we do not need to test signing ceremony stuff, etc. That's not part of what we ship. A full run should only be done on what is shipped to adopters. We would find errors in what we run here when we run them."* Today `bootstrap/security_check.py` runs the whole engine suite (`bootstrap/tests`) natively on each host. Measured on the 2026-11-12 certifying run (5,413 tests, 49 minutes; the report is local and not committed): the Cairn-side ceremony and gate files (repin, re-anchor, gate preflight, manifest and transition, oracle, AST attestation, security check, ceremony review report, release publication check, quality gate), picked by file name only, are 20 files, 1,283 tests (24%) and 938 seconds (32% of the time). Most of the rest is the installer and upgrade tests, which are shipped, so this saves about a third, not most. A proposal has to settle the exact boundary (the checks adopters themselves run, such as `verify_integrity` and `verify-ref.sh`, ship and stay in), how the Cairn-side tests still run (when their own files change, through the test selector), and how the release record names what it did not certify. Maintainer position, 2026-11-13: *"I do not believe there is a real security threat from not testing something that our adopters don't use. We use it here."* The gate files (`security_check.py`, the roster, the release process) are signed and protected, so the change is made in the normal way, with the re-anchor and whatever review `AGENTS.md` sets for edits to them; the proposal's author sets the lane. Timing: v0.8, not before the 0.7 cut. | [Issue #61](https://github.com/MSUHydrogeology/cairn/issues/61) (test cost); `bootstrap/security_check.py` header; `docs/release-process.md` |
| **Trim bulk from the Cairn templates, the testing module and the collaboration guide.** (v0.8 proposal to write) | Maintainer direction, 2026-11-10: "There simply aren't 5000 words worth of instructions needed to develop in this repo. That is just bloat." The `AGENTS.md` trim (v0.7 item 13) took the shipped file from 4,343 to 1,111 words, but the moved rules now sit in `dev/agent_collaboration.md` (5,451 words shipped, up from 3,328 before the trim), so the three files an adopter reads for those topics fell only 10% (8,012 to 7,238). Next: measure the plan template (4,915 words), the proposal template (4,014), the testing-discipline module (2,148) and `dev/agent_collaboration.md`; move detail that agents do not need to documentation; rewrite what stays shorter, starting with the Boundary A, B and C and testing text because it drives test-building. Also trim the notes in the vendor wrapper template (`VENDOR.md`: 310 words, about 145 of them notes for the person renaming it) and keep the files loaded every session under the cap decided on 2026-11-10: `AGENTS.md`, the wrapper and `RULES.md` together at or under 2,000 words (1,500 until the Maintainer raised it on 2026-11-12), as a written rule with no test checking it for Cairn's own files (the item 23 candidate adds a test that holds the shipped three files to 1,500). The templates must not grow, and no test may pin the wording of the result. Input for that proposal, 2026-11-13 (a read-only review of the 11 plans archived on 2026-11-12 found nine with no Dispositions section): the section is owed only for follow-ups "explicitly deferred", so items left in "Not run" lists, "remaining burden" lines and a bare "item 12 owns it" escaped, and no tool checks for them. Fold the Dispositions into the closeout record, so there is one closing section instead of two: every "not run, not covered or remaining" line carries a Home (a roadmap row, an issue, a proposal or the Maintainer's quoted word), and an empty Home means the plan is not ready to archive. Add one advisory warning for a plan at `ready-to-archive` that lists such lines with no Home, in `tools/board.py` (which already reads that status); Cairn's tools warn and do not block. | [Stage 2 result](strategy/2026-11-10-claude-agents-md-diet.md); Maintainer chat, 2026-11-13: "Would some change to the plan template help make sure dispositions are caught?" |
| **Better treatment of rules: proposals and plans list the rule files that apply.** (v0.8; to write into the template-trim proposal) | Maintainer direction, 2026-11-12: local rules can get long, and agents should not hold all of them in context; "I like all of this" on the note's recommendation. Both templates gain one header line, `**Rules that apply**:`, holding rule file paths picked from the `RULES.md` routing table, never rule text. `RULES.md` stays as the router and the home of the bright lines; a rule that applies but is not listed is still followed and added to the line; reviewers check the line against Scope. About 20 template words, taken from the trim's savings; no test pins the wording. Next: write it into the trim proposal in the row above, so the templates get one heavy review. Decided 2026-11-12 (Maintainer: "Let's keep the cap on shipped rules."): the shipped files keep their 1,500-word limit, which a test in the item 23 candidate holds; the 2,000 cap is for Cairn's own files, which add project-specific rules on top. | [Strategy note](strategy/2026-11-12-claude-rules-listed-in-proposals-and-plans.md) |
| **Where `architecture_review.md` and `ceremony-record.md` belong.** (v0.8 assessment to do) | Maintainer note, 2026-11-10: the file seems out of place. It is the architecture-review module's record: `bootstrap/_scaffold/config.py` installs `architecture_review_template.md` to `dev/architecture_review.md`, so it sits in `dev/` beside the core files (`PLANNING.md`, `agent_collaboration.md`), while the other module notes install under `dev/modules/`. The Maintainer suggested `dev/measurement/`, since the file is evidence. That folder is installed for every adopter, but its README limits it to process-health records, and the first half of the file (current shape, helper homes) is living reference that the module tells agents to keep current, not dated evidence. Other candidates: `dev/modules/` or `docs/`. Assess together with the repository layout proposal. A move changes the install mapping (an engine file), the lockfile record and the upgrade of installs that already have the file, and Cairn's own copy would follow. The Maintainer also suggested `dev/.cairn/` for `dev/ceremony-record.md`; the re-anchor script, runbook and tests name that path, so a move is a trust-ceremony change. | [Repository layout proposal](proposals/2026-11-09-claude-repository-layout.md) |
| **One shared home for the outward-report templates.** (v0.8 proposal to write) | Maintainer direction, 2026-11-10: keep `.github` and `.gitlab` (each forge reads only its own fixed path), add no generic `.forge`, and put a Cairn fold-back template and an upstream-project template in `dev/upstream/`, which `dev/agent_collaboration.md` points to (decided 2026-11-10). Today the fold-back protocol exists only as Cairn's own `.github` issue and pull-request forms (526 and 461 words, not shipped). The dependency-report template is `dev/upstream/_template.md` (236 words) with a 368-word README; `dev/upstream/` ships to every adopter, has three tracked files, no draft has ever been committed there, and nothing in `AGENTS.md`, `RULES.md` or the collaboration guide names it. The folder must actually be used, not just shipped. It holds the Cairn fold-back template and either an upstream-project report template or instructions for fetching the dependency's own issue template and working with the user to fill it in and file it, and the collaboration guide tells agents to use it when they find a Cairn problem or a defect in a dependency. External reports are public, so the agent drafts and shows the user, files only on the user's word, and includes no unpublished data. Keep one statement of the fold-back protocol and have the other copy point to it. Adding a file to the install is an engine change, so it needs a proposal. | Maintainer chat, 2026-11-10 |
| **Every installed template and guide is pointed to.** (v0.8 audit to do) | Maintainer direction, 2026-11-10: make sure each installed template is pointed to by `AGENTS.md` or something similar. Extended 2026-11-11 to installed tools: a name screen of the docs, installed guides and templates found five shipped tools that none of them names (`tools/meter.py`, `tools/prune_intents.py`, `scripts/exact_replace.py` and the two label bootstrap scripts), so adopters learn of them only from the tool's own help text. First count, 2026-11-10, on a scratch install of the `collaborative-team` profile (name matching on paths, folders and file names only, leaving out dated reflections and merge snapshots): 20 of 35 markdown files are not named in `AGENTS.md` or `dev/agent_collaboration.md`. They are 12 module notes; the plan, proposal, strategy and upstream templates (`AGENTS.md` says to read "the current template" without a path); both skills; and `CONTRIBUTING.md` and `NOTICE.md`. Next: decide file by file whether to point to it from the collaboration guide or from a folder README the guide names, or to drop it from the install; skills and the two human-facing files may need no pointer. Keep the always-loaded files under their 2,000-word cap, so pointers go in the guide or a README, and use a one-off script, not a test. Added 2026-11-12: an install already writes a module inventory (from `templates/core/dev/modules/README.md`) with one row and one board task per selected module (`bootstrap/tests/test_onboarding_seed_roster.py` checks it), so count those as pointers. The shipped roster table in `templates/modules/README.md` has 12 rows for 22 module documents (counted 2026-11-12, not matched one to one), and its check runs one way only (`bootstrap/tests/test_module_roster.py`: a row must name a module that ships), so a module can ship with no row. | Maintainer chat, 2026-11-10 and 2026-11-12 |
| **Retry the Git-based upgrade comparison (item 7d's unrun trial).** (v0.8; proposal to write) | Maintainer direction, 2026-11-13: *"Give retrying the safe git upgrade a home on v0.8"*. The 7d trial stopped before any comparison ran: a harmless Python print exited 134 inside the operating-system write boundary (and the driver -6) on the trial host, cause undiagnosed; 2 of 39 baseline destinations (`AGENTS.md`, `dev/PLANNING.md`) do not reconstruct because the plan's recipe omits the security-module merge and the onboarding overlay; all six comparison cells and the 37-case hostile classification are unrun. A retry first diagnoses why the boundary cannot start Python, fixes the baseline recipe, then runs the three matched variants. It authorizes no engine replacement; the accepted result stays incomplete until a retry reports. | [Archived plan](plans/archive/2026-11-12-upgrade-growth.md), implementation result and Benefit versus cost line; [accepted proposal](proposals/archive/2026-11-05-codex-upgrade-growth.md); [strategy note](strategy/archive/2026-10-30-claude-upgrade-growth.md) |
| **A style guide, a short agent version and an onboarding task to start one.** (accepted for v0.8) Cairn gets a human-first style guide in `docs/`, a shorter agent version in `dev/rules/conventions.md`, documentation-module guidance and a seeded task in each preset. The sync note adds no pin. | Ordinary and Security reviews, revision and the recorded heavy Decision are complete. Installed duties stay in accessible authoritative homes; preference drift cannot override security, dependency or license rules. Plan and implement in v0.8 after layout supplies final paths and the rules stub is available, retaining required ordinary and Security assurance. No implementation started. | [Accepted proposal](proposals/2026-11-12-claude-style-guides.md); revision `4c633a6b`; recorded Maintainer Decision, 2026-11-12. |
| **Offer new and unselected modules at upgrade by asking the user.** (v0.8 proposal to write) | Maintainer direction, 2026-11-12: add new or omitted Cairn functionality to updates, not automatically but by querying the user. Today `upgrade --plan` prints one line, "new modules available (opt-in)", for every shipped module missing from the lockfile's module list (`new_modules` in `bootstrap/_scaffold/upgrade.py`; the code lists unselected modules too, though `bootstrap/UPGRADE.md` says "since install"), and `--adopt-module <name>` adds one deliberately. The line gives no description. New core and skills files are added automatically (`bootstrap/UPGRADE.md`, line 549). The change: when an upgrade finds functionality the project lacks, the agent says in plain language what each piece does and costs and asks whether to adopt it, then runs the adopt step on a yes; `--plan` stays read-only. Open question for the Maintainer: does "not automatically" also cover the core and skills files that auto-add today? Whether this is guidance only or an engine change decides its tier: an engine change is heavy with a Security Review and waits for the repository layout. | Maintainer chat, 2026-11-12: *"Adding new/omitted Cairn functionality to Cairn updates--not automatically but by querying the user"*. |

## v0.9 — outside evidence and autonomy

These rows are v0.9's scope as it is being planned: listing them authorizes no work. Maintainer chat, 2026-11-10, on a split by theme: *"Go ahead and update PLANNING.md with this list"*. v0.8 settles the structure; v0.9 learns from outside adopters and real use, then widens what agents can do unattended. Four rows moved here from v0.8 (the budget guard and unattended loop, the Stid interview, independent adopter feedback and #34), and the real-use meter comparisons moved up from Deferred follow-ups. Organized interviews, testimonials and the independent adoption trial belong here, so an outside adopter meets the settled layout once; incoming defect reports still receive normal triage. The cost of waiting is later evidence about outside usability. No outside trial is counted as completed, and no required release or correctness check is waived by this schedule. The board authorizes no outreach or testimonial publication.

| Work | Next step | Record |
|---|---|---|
| **Outside adopter interview and testimonial (Stid).** Refine the drafted questions and survey to find friction points and capture a testimonial. | In v0.9, after v0.8 ships, so the adopter meets the settled layout once, use the staged instrument with a consenting adopter, including human interruptions and usability of the continuation guidance. The v0.7 agent-operated comparison cannot establish those human outcomes. Publication of any quote or testimonial still requires explicit consent. | [Strategy](strategy/2026-10-27-antigravity-adopter-survey-instrument.md#recommendation); Maintainer, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"* |
| **Independent adopter feedback.** Learn whether someone outside Cairn can install and use a published release without relying on the team's setup or knowledge. The v0.5 signed bootstrap passed in the team's Windows VM; that is not an outside adoption trial. | In v0.9, when a willing outside adopter is available, invite feedback on a published release, ideally one that carries the v0.8 layout. The outside correctness trial remains open until actually performed. | Maintainer chat, 2026-11-01; **Outside correctness trial**, below |
| **Real-use meter comparisons and conditional Tokens retirement.** Queued after v0.7 and now scheduled in v0.9; the seven-day observation and independent `ccusage` comparison are unperformed. Keep manual Tokens and Elapsed until the prescribed comparisons and other meter checks justify retirement. | Condition to start: The collector passes its technical checks and the Maintainer opts into named local sources/projects. An agent then owns the comparisons with the existing privacy requirements; no private collection is currently enabled. | [Meter plan](plans/archive/2026-11-04-metered-cost.md), Maintainer disposition `97a0eab3`, 2026-11-09.  |
| **Cooperative budget guard and conditional unattended loop.** (queued for v0.9 planning) | Revisit the reviewed proposal during v0.9 planning, using v0.7 measurement and continuation results and the real-use meter comparisons above to decide what is worth building. It proposes a spending check before each unattended item; an automatic launcher remains a separate later choice. The guard cannot enforce a provider billing cap. Account/time source proof and human-benefit evidence remain absent. No implementation, activation or private collection is authorized. | [Joint proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [meter plan](plans/archive/2026-11-04-metered-cost.md); [continuation plan](plans/archive/2026-11-05-agent-continuation.md); Maintainer dispositions `896f2ac2` and `d0d82446`; Maintainer chat, 2026-11-06: *"Yeah go throw that 0.8 item on the planning file"*. |
| **Drain an adopter's current-release roadmap** ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)). Show candidates and a short plan, then move eligible items one at a time under their existing gates. A candidate, not authorization. | Write the v0.9 proposal, retaining existing lifecycle and Maintainer gates; this scheduling is not authorization for broader autonomous execution. | [Issue #34](https://github.com/MSUHydrogeology/cairn/issues/34) |

## Terms used here

- **Re-anchor** — the Maintainer's signed approval of the exact test files that
  guard Cairn's security checks. A **repin** is the routine version of it.
- **Trust baseline** — the set of approved files a re-anchor installs. The
  **v0.6.1 baseline** was installed at `977b5250`.
- **Certification** — one full test run on a clean commit, before a release or
  a re-anchor. Ordinary changes run only the tests that name the files they
  touch.
- **Protected (frozen) test** — a test file the gate pins by its hash; changing
  it owes a re-anchor.

## Working rules (for agents)

- **One branch.** Work on `0.7-dev` in the one shared checkout, with no topic
  branches and no worktrees for writing. `master` holds the released 0.6.1 and
  takes no development commits. A reviewer who must change code to test it
  works in a throwaway detached worktree of the reviewed commit and removes it
  afterwards. Maintainer, 2026-10-26: *"I actually would prefer that all work
  happen in the 0.5-dev branch, and that we use the intents board. This has
  gotten to be too many branches for me to interact with properly."* And,
  2026-10-28: *"create a 0.6-dev branch where we will do the other work going
  forward"*.
- **Claim, then commit by path.** Claim a file before editing it
  (`python tools/intent.py claim --files <paths> --action "<what>"`) and commit
  by explicit path, which releases the claim. `python tools/intent.py list`
  shows who holds what.
- **Check before each commit.** Every subagent in one session shares one claim
  identity, so one commit releases the others' claims: check `git diff` first.
- **Take turns with heavy test runs,** and give reviewers of long plans tight
  briefs.
- **Changelog.** Each change adds its entry under `## Unreleased` in
  `CHANGELOG.md`, in the same commit or the next, following the file's header.
  At the cut the section is renamed and a new `Unreleased` opened; the GitHub
  release notes are copied from it (`docs/release-process.md`, "The cut").
- **Merging to `master`, tagging and pushing are the Maintainer's.**

## Accepted limits and standing decisions

Each is known and accepted; none is a task.

- **The board and the status check disagree on an unknown status** such as
  `awaiting-decision-x`: the check flags it, `board.py --maintainer` still
  lists it. Making the board strict would edit a frozen test
  (`test_board_json_contract.py`). Maintainer: *"Leave the disagreement"*.
- **Three limits from the 0.5.0 upgrade lockfile-path fixes.** One finding got
  only a documentation answer, because the full fix breaks a frozen pin. A
  linked lockfile on `--adopt-collisions` or `--init-lock` still ends in a
  traceback, with nothing read or written outside the project. Profile preset,
  axis and module values are written unquoted, because quoting fails a
  byte-for-byte comparison test. Recorded in
  `bootstrap/_scaffold/SECURITY_MUTATIONS.md` and `bootstrap/UPGRADE.md`.
  Maintainer, 2026-10-26: *"Accept all three (Recommended)"*.
- **No new security-dispatcher legs.** Link and claim checks already run as
  documentation gates through `scripts/check_cairn.py`; separate dispatcher
  legs would add one-command access, not new detection. The web runner's
  passive mode is unauthenticated. Maintainer, 2026-11-01: *"Keep existing
  gates"*.
- **Templates stay longer than the nimbleness target.** The
  [template plan](plans/archive/2026-11-01-template-burden.md) cut 24 lines and
  274 words across the four proposal and plan templates, keeping other
  repetition for point-of-use guidance. The nimbleness note's 80–120-line
  target was not adopted as a requirement.
- **Interpreter binding on native Windows passed** at `66b19e4b` (2026-11-01):
  `python scripts/run_windows_interpreter_binding.py` on Windows ARM, Python
  3.13.17, 23 passed with no skips in 12.90 s, including the junction and
  reparse cases. This is not a full current-tree certification.
  [Plan](plans/archive/2026-10-30-git-interpreter-binding.md)

## Deferred follow-ups

Each returns to the release tables when its revival condition is met. Earlier
evidence stays in the named record and in this file's history.

| Follow-up | Revive when | Record |
|---|---|---|
| **Review-load check.** Count review commits (subjects containing `review` or `respon`) per archived proposal or plan, against the 6.9 baseline and a target of 3.5 or fewer. This is an indicator, not proof of value. | Measure on 2026-11-30 using the existing review history and 2b pulse where available, not a second collector. The scheduled comparison is still open. | [Proposal](proposals/archive/2026-10-30-claude-cut-the-apparatus.md) |
| **Watch the new review header.** The first ten reviewed on 2026-11-02 did not meet the specified incident trigger: several challenged the proposal's framing. | Continue noticing premise and alternative challenges, agent-chosen outside reads, thin evidence and lost scope challenges; report a worrying pattern. | `review-stance-and-lenses` plan; authority below |
| **Watch how proposals written at medium tier hold up.** The first ten review passes covered four medium- and three high-authored proposals; both groups had substantive blocking findings. The small, mixed sample does not establish a quality difference. | Continue watching; compare like work when enough evidence exists. | `model-tier-rules` plan (R5); the Maintainer's 2026-10-26 answer lowered proposal writing to medium |
| **Report only live slots after the module merge.** Print the install report after the merge and drop slots the install fills itself, so `solo-greenfield` shows 20, not 20 plus 2. Not built: it moves output a frozen test pins. | With the next change to that test. | `engine-batch-f8-slots` plan, Scope delta; Maintainer: *"Accept, leave 2 slots counted (Recommended)"* |
| **Decision rights after the collaboration agreement's removal.** Offering Cairn's rule for unsure cases to adopters needs its own proposal. | When a concrete conflict reaches a decision; then revisit the escalation wording. | `remove-collaboration-agreement` Decision, Q3 |
| **Naming sections and proving all were handled.** | When a second real rule needs a complete set of sections. The retired lifecycle checker is not the promised answer. | `2026-08-20-claude-review-loop-termination`, Deferred work |
| **Feature lists on entry pages go stale.** | A second stale list, or an adopter hitting one, may justify a doc-drift rule. | `dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` |
| **Withdrawal records can lose their reasoning.** Keep a corrected contract distinct from a summary that re-argues what was rejected, and test rules against the cases they claim. | On an independent repeat or a Maintainer call. | `scanner-claim-scope` revisions and reviews |
| **Pre-reviewing a revision.** Earlier tries found defects, but one fix quietly cut accepted scope; every fix still needs the purpose and scope check. | On a justified later review round or a Maintainer workflow choice. | Observations, 2026-08-19 |
| **Revisions that silently drop sections.** | A third instance may justify carrying a section inventory forward. | Observations, 2026-08-19 |
| **Dispositions go stale between commits.** | An independent repeat may justify recording the measured commit with each disposition. | Observations, 2026-08-19 |
| **Evaluate Cairn Plain Language 1.x after three months.** Adopted 2026-10-26. | Late January 2027: the Maintainer checks whether it worked, then decides on a standalone page with its own DOI. | [Strategy](strategy/2026-05-14-claude-human-ai-team-development-framework.md#candidate-future-moves-not-queued) |
| **Stage re-pins in a clean temporary worktree.** | If the dirty-tree refusal blocks the Maintainer twice. | `repin-build` proposal, "What is not carried" |
| **Warn at session start when a pin is stale.** Needs a threshold with evidence behind it; Cairn's tools warn, they do not block. | If a stale gate manifest or AST baseline goes unnoticed again. | `repin-build` proposal, item E |
| **A quickstart that adapts to the project.** | When adopters ask for a shorter next-step path again. | `adopter-entry-doc-refresh` follow-up |
| **More adopter-facing count checks.** | When another live count needs the verify-count guard. | `adopter-entry-doc-refresh` follow-up |

Monitoring authority, verbatim: *"Yes, we should keep watching."* and *"Keep
the monitoring row (Recommended)"*. The shared-working-tree observation came
from the first-ceremony batch, kept under: *"Yes, go ahead and close
everything else from these two plans out, including finding a permanent home
for any remaining items"*.

### Outside correctness trial

A consenting science repository that did not help write the doctrine still
needs to run the bootstrap end to end. It did not block 0.4 (waived
2026-10-19: *"Waive it for 0.4 — Go public once the batch lands. The README
says plainly that it hasn't yet had an outside test."*); the waiver is not a
completed trial. To revive, enroll a willing third party. That also revives
the scientific-check review (#19).

The first blind trial covered two plans and did not show that the guidance
catches later errors. When the trial resumes, these six results would show
the scientific check is not working:

1. every failing check was already caught elsewhere;
2. most bases are the author's own expectation;
3. work that changes assumptions claims the check does not apply;
4. failing runs are missing or cannot be reproduced;
5. checks only repeat what code review catches;
6. a no-effect result has no positive control and no stated reason for lacking one.

No failure and no later error means the trial is inconclusive. Also watch for
checks run after the code, expectations changed to fit results, false "data
in hand" claims, ritual checks on tooling, new discipline lists, and checks
that neither need data nor say what evidence was opened. Nothing counts these
automatically; issue #19 and the Maintainer's review are the reminders.

## Onboarding

The reading and tour tasks below are not yet confirmed done. They ask for no
extra ceremony.

* Try the session-start skill; its implementation is `tools/session.py`.
* Read `docs/methodology/lifecycle.md` for the proposal/plan lifecycle.
* Read `docs/methodology/coordination.md` for shared-tree coordination.
* Read `dev/modules/dual-review.md`; fresh independent review is the standing
  procedure, and an outside read is the Maintainer's call.
* Read `dev/modules/onboarding/dev-tour.md` for the worked lifecycle example.
* Review capability tiers and commit attribution with
  `dev/modules/onboarding/agent-team-onboarding.md`.

## Security findings

Open security residuals and their revival triggers live in the
[security strategy](strategy/2026-08-05-codex-security-strategy.md#live-residual-register).
Add a board row when a trigger fires, rather than copying the register here.

## Archive preconditions (proposals and plans)

Board housekeeping follows `dev/plans/_template.md` > Dispositions and
`docs/methodology/lifecycle.md` > Archive precondition. Completed rows leave once their
record is durable; unresolved tasks keep a real live home. An archived plan
is evidence, not a place to hide work still owed. Deferrals retain the
Maintainer's quoted authorization and a named live home.

For the board's self-contained scope vocabulary: **a scope-cut removes no
work**; removing a baseline outcome **is a scope reduction**, tested against
the commitments as *opened* before Decision and as *accepted* afterwards.
It takes one **grouped scope-remainder record** and **only the Maintainer may
concede** that loss. Completed and duplicate entries leave the board.

## Status taxonomy

Use `queued` for work not started, `active` for work in flight, `blocked` for
a named dependency, and `deferred` with a revival condition. Mark a
Maintainer-only next move on its own bulleted line starting
`**Waiting on Maintainer**: <what>`, as in **Waiting on you** above;
`board.py --maintainer` reads that line, not a table cell, and infers nothing.

## Removal preconditions

Confirm completion and its durable record before removing a task. For the
full lifecycle rule, see `docs/methodology/lifecycle.md` > Removal preconditions for a
roadmap item. Keep current tasks here and evidence in the source records.
