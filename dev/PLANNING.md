# Cairn — development board

This board lists the work left and its next step. The Maintainer reads the
status, waits and release sections. Agents also read **Working rules** and the
sections after it. Evidence, quotes and history live in each row's
**Record** column: an issue, strategy note, proposal, plan or guide, or the
Maintainer chat the item came from. Finished work leaves the board.

`python dev/tools/board.py` lists every open proposal and plan with its status;
`python dev/tools/board.py --maintainer` lists what waits on the Maintainer.

## Waiting on you

Lines marked **Waiting on Maintainer** are what `board.py --maintainer` lists,
together with any proposal awaiting your Decision.

Nothing is waiting on you now. The [simpler re-anchor proposal](proposals/2026-11-19-claude-simpler-reanchor-ceremony.md) needs its reviews before it reaches you.

## Where Cairn stands

[Cairn 0.8.0 is released](https://github.com/MSUHydrogeology/cairn/releases/tag/v0.8.0)
(2026-11-19; cut at `d59a4268`, signed tag `v0.8.0`, version DOI
[10.5281/zenodo.24381175](https://doi.org/10.5281/zenodo.24381175)).
Cairn builds itself with Cairn and is used in LHM and modflow_tools. v0.9 work proceeds on `0.9-dev` (see **Working rules**). Earlier development notes, with the rows and decisions that older records cite, are in Git history: v0.7 at `git show dbb83261:dev/PLANNING.md`, v0.8 at `git show 9be9474c:dev/PLANNING.md`.

Standing direction from the Maintainer (2026-07-22): science projects come
first, and Cairn fixes what it already ships before building anything new. A
new tool or mechanism needs its own go-ahead. No outside project has yet run
Cairn end to end; that trial was waived for 0.4 and 0.5 and is still open
(see **Outside correctness trial**, below).

Standing direction from the Maintainer (2026-11-10): Windows is an equal partner with macOS and Linux, and the shipped tools support Python 3.12. Cairn's own certifying runs may stay on Python 3.13. The Python 3.12 work shipped in 0.7; the Windows secrets-scan route shipped in 0.8.

Standing direction from the Maintainer (2026-11-19): *"Our primary goal--the whole reason Cairn exists--is to ship good scientific code. Not perfect code. Wherever procedures exist that interfere with that, they must be simplified or reduced."*

## v0.9 — fix what 0.8 shipped, simplify releases, then monitoring and autonomy

These rows are v0.9's scope as it is being planned: listing them authorizes no work. Defects come first (section 1). Then Cairn's own releases get simpler and verified on all three hosts (section 2), adopters get the scientific-software work (section 3), the postponed monitoring interface follows (section 4), and agents get more room to work unattended (section 5). Work moved here earlier keeps its full scope: the monitoring interface with its four-view pilot (Maintainer, 2026-11-13) and scientific-software dimensions and governance (#19, 2026-11-16). Adopter interviews and the independent adoption trial move to v0.10. No required release or correctness check is waived by this schedule.

### 1. Defects first

Before the rest of v0.9 starts, walk the open issues that report defects or adopter frictions and resolve each one way or another: fix it, close it on its accepted outcome with the reason recorded, or defer it with the Maintainer's quoted word. Add any defect found since, including those from upgrading projects to 0.8.

- **Open issues.** [#93](https://github.com/MSUHydrogeology/cairn/issues/93) (the session-end prune command is bash-only and fails in PowerShell; the bash form is written in the session-end skill and its base copy and in `dev/modules/coordination-tiers.md`; fix both forms, `$env:CAIRN_HANDOFF_OWNER = '1'; python ...` for PowerShell), [#91](https://github.com/MSUHydrogeology/cairn/issues/91) parts 2 and 3 (held in Deferred follow-ups), [#90](https://github.com/MSUHydrogeology/cairn/issues/90) (the repository-root standard) and [#79](https://github.com/MSUHydrogeology/cairn/issues/79) (the smaller entry file, a reconsider row).
- **The re-anchor.** The v0.8 re-anchor, deferred to v0.9 because the shipped files do not change, and the [proposal to let a re-anchor pass a long history and shrink the Maintainer's part](proposals/2026-11-19-claude-simpler-reanchor-ceremony.md) (awaiting review). Then restore the "bootstrap" wording check in `test_check_runs_against_the_live_repo_and_reports` after the re-anchor, as the Security review advised.
- **Checks waived at the 0.8 cut.** The strict Mac and Windows release records, their join and both candidate secrets scans were waived for 0.8; they are due at the 0.9 cut unless the verification row in section 2 changes them.
- **The published v0.8.0 tag.** Check it through both documented release routes in Windows Git Bash; the 2026-11-19 check used v0.7.0 and a disposable signed fixture.
- **Windows.** 9 older failures in `tests/contract/test_release_members_contract.py` (8 need `bash` on the SSH path, one is a timing flake), the release-membership checker refuses pytest's Windows `file=` paths with backslashes, no full Windows suite has run as a release gate, the portable secrets sweep has no test for Git being absent (it reports INCOMPLETE), and the 15 older Windows failures of 2026-11-16 if not already repaired; the Windows `[write]` staging failure is fixed (`12124ee2`) and passed on `cairn-windows` at `ed893f0d`.
- **Narrowings from the layout move.** New files under `tests/` are no longer scanned for new-file review (`tests/_gate_preflight.py`), and `tests/test_fork_advisory.py` checks only exit 2, not the refusal message.
- **`docs/DOCUMENTATION_PLAN.md`.** It is the one installed file outside `dev/` that is not a root entry or Git file: move it into `dev/` with the rest, which changes the install manifest, so add the upgrade move and update the shipped files that name the old path.

Record: Maintainer chat, 2026-11-19: *"Let's fix #93 in v0.9. I am sure there will be other defect fixes that need to be addressed as well. Let's make sure that fully addressing those other issues, one way or another, is done at the beginning of the v0.9 process"*; same day: *"Make sure that windows failure makes it onto our v0.9 defects round"* and *"Put the change to repin as a proposal (you write now) on the v0.9 defects to fix."* and *"I think DOCUMENTATION_PLAN.md should be in dev/ Please put that as a defect to fix for v0.9"*; *"Let's get those in the defects part of 0.9. I'm sure there will be more when I get through an upgrade cycle"*

### 2. Cairn's own releases: simpler, and verified on three hosts

| Work | Next step | Record |
|---|---|---|
| **Verify every release on Linux and Windows alongside Mac.** (v0.9; asked 2026-11-19) | A release is certified today by the full run on the Mac and only the native strict run on Windows, joined by the release check; no full Windows suite has run and Linux has none. From the next release, each host gets its own verification and record, and the join requires all three. `dev/rules/certifying-runs.md` and `release/RELEASE_PROCESS.md` describe a Mac-only full run today and change with this. Add Linux as a third verified host: run the native strict run on the shared Linux VM (`ssh linux-dev`, Ubuntu 24.04 ARM64; its Python is 3.12.3 today, so first decide the certifying Python and whether the guest needs a 3.13 build, per `dev/rules/development-environment.md`), name any Linux-only tests in the same native list the other two hosts use, require the Linux record in the release join, and record the command, interpreter and elapsed time as the Windows runs are recorded. Not part of 0.8. | Maintainer chat, 2026-11-19: *"Can you put a planning item for v0.9 to have a Linux certification too?"*; later the same day: *"for future releases, I want Linux and Windows verification alongside Mac."* |
| **Attach a release `.zip` that leaves out Cairn's own `dev/` folder.** (v0.9; asked 2026-11-19, [#94](https://github.com/MSUHydrogeology/cairn/issues/94)) | GitHub's automatic source archive for a tag includes `dev/`, so someone who only uses Cairn downloads its development history. Build a `.zip` from the exact tagged commit by a script that reads the committed keep list (#75; the release-cut work in #67), attach it to the GitHub Release beside the signed tag, name its contents in the release notes, extend `release/check_release_publication.py` to confirm the asset exists and matches the tagged commit, and check that nothing the archive keeps cites `dev/`. A new release tool needs its own proposal and Decision; not part of 0.8. | Maintainer chat, 2026-11-19: *"put a v0.9 issue to add a release .zip archive to that release, which omits Cairn's own dev folder"* |

### 3. What adopters get for scientific software

| Work | Next step | Record |
|---|---|---|
| **Scientific-software dimensions and governance (#19; former 7c).** (postponed from v0.8 to v0.9, 2026-11-16) | In v0.9, propose the remaining doctrine sentence, deliverable axis, discipline list and governance reframe using existing project evidence and the delivered scientific-testing examples and architecture rubric. Preserve the full remaining scope; the separate outside-adopter trial is not a completion claim or a new prerequisite. Start after the repository layout lands, so edits to `dimensions/` land once in `install/`; if the axis becomes a machine-read profile axis it also touches the install contract (`install/_scaffold/config.py`) and would be heavy. | `independent-scientific-check` plan; [Issue #19](https://github.com/MSUHydrogeology/cairn/issues/19); Maintainer chat, 2026-11-04: *"Let's move #7c to v0.8."* This replaces only this item's earlier v0.7 scheduling. Maintainer chat, 2026-11-16: *"Let's postpone the scientific software and dimensions"*, which moves it from v0.8 to v0.9 with its scope kept. |
| **A release module for adopters that ship software.** (v0.9 proposal to write) | [#82](https://github.com/MSUHydrogeology/cairn/issues/82): an optional module with a short release rule (when to cut, reconciling plans, a keep list and cut script, notices, verification, the tag, publication, citation metadata). [#83](https://github.com/MSUHydrogeology/cairn/issues/83): an audit of vendored and copied third-party files and their licenses. [#67](https://github.com/MSUHydrogeology/cairn/issues/67) and [#75](https://github.com/MSUHydrogeology/cairn/issues/75): the release-cut tooling, committed list of what a release keeps and the check run against it. Harvest from LHM's release rule (17 steps) and modflow_tools' releasing guide, and offer it by a trigger (the staged module offers delivered in 0.8). Both current adopters have their own rule, so this serves the next adopter. A new module needs its own go-ahead. Prerequisite, delivered in 0.8: [leaving Cairn out of a release](plans/archive/2026-11-18-release-without-dev.md). | [#82](https://github.com/MSUHydrogeology/cairn/issues/82), [#83](https://github.com/MSUHydrogeology/cairn/issues/83), [#67](https://github.com/MSUHydrogeology/cairn/issues/67), [#75](https://github.com/MSUHydrogeology/cairn/issues/75); [Grown-projects note](strategy/2026-11-16-claude-guidance-for-grown-projects.md) |
| **Test records, so a release reuses current results.** (v0.9; waits on adopter evidence) | [#81](https://github.com/MSUHydrogeology/cairn/issues/81): a contract for the test-tier listing and an optional record for each test file, keyed by the content of the files it depends on; a release is verified when every test has a current passing record. LHM is building one, and its plan stops if the measured saving is small. Decide from that measurement whether Cairn ships a tool. [#92](https://github.com/MSUHydrogeology/cairn/issues/92) (three test-cut helpers on offer) is considered here. Maintainer chat, 2026-11-16: *"let's consider that in v0.9--or potentially just apply it for good test building. I'm not sure how often cutting is necessary?"* Sort the three by use: the text-pin scan works while tests are being built, where it stops a wording pin from being written; the run comparer and the cut-ledger check serve only a cut. Decide the two cut tools from how often cuts recur: so far Cairn has made one large cut (933 test functions, in v0.7) and modflow_tools one small one (64 test nodes). The principle, without the tool, shipped with 0.8's [template trim](proposals/archive/2026-11-16-claude-template-trim-and-rules.md). | [#81](https://github.com/MSUHydrogeology/cairn/issues/81), [#92](https://github.com/MSUHydrogeology/cairn/issues/92); [Grown-projects note](strategy/2026-11-16-claude-guidance-for-grown-projects.md) |

### 4. Seeing the project: monitoring

| Work | Next step | Record |
|---|---|---|
| **One local oversight website with tabs: the release board and the code-change views.** (v0.9 proposal to write; postponed from v0.8) | Current schedule: v0.9, after v0.8's existing-feature reliability and testing work. The full interface and four-view pilot remain queued, with scope and prerequisites preserved. Prior design direction, 2026-11-10: both the visual release board and the four-view pilot are graphical tools that help a person oversee the work, so build them as a single local website with tabs. One tab mimics the work tracker used in chat: completed work, implementation versus review and verification, blockers, dependencies and who acts next, generated from `board.py --json`, `git` and `gh` instead of kept by hand. Another tab carries the four-view pilot of code changes, postponed from the archived architecture plan (C3), using LHM's scope-map page (`lhm/tools/scope_map.py` and `scope_map.html`) as the example. That page fills one HTML template with data, but it loads its drawing library and fonts from the internet, which this tool must not. Working assumption: one command writes one self-contained HTML file with the data embedded and no network needed. It works the same across agent tools, needs no vendor chat or hosted artifact, separates observed state from inferred progress and shows freshness. It builds on the board's JSON output and the board-view guide (`docs/build-a-board-view.md`). Consider a `passes` field only if the derived view shows the need, and keep no second hand-maintained source of status. The code-change tab waits on the reviewed safe-Git helper. Maintainer direction, 2026-11-10 (v0.8, as a module): ship it as an opt-in Cairn module that adopters choose in their profile's module list, not a default-on install. Reason: the v0.7 weight review found unconditional installs (`meter.py`, `git_read.py`) adding weight for every adopter. It installs into the single tools folder under `dev/` with its guide in `dev/modules/`, so it installs once. Start after v0.8, using the delivered repository layout and reviewed safe-Git helper when v0.9 planning opens (see the dashboard design note). The layout test must count the module's files as install destinations. The Maintainer already uses a version of this tool in several projects; the module can start from those. Open for the proposal: which presets, if any, offer it by default. Maintainer direction, 2026-11-10: this is a dashboard for a person, showing at a glance how the project is and how it is changing, so they can monitor its growth. Five tabs: Development (the tracker above), Sankey diagrams of where work lands, Complexity, Growth over time (complexity and effort series), and Security (how the security-relevant surface is changing, with a since-last-release drill-down). Design every widget now, marked ready, partial or placeholder; ship a small first slice and grow it. Claims and agent-facing controls are out. Tokens stay placeholder until the v0.9 meter comparisons. | [Strategy note on this site](strategy/2026-11-10-claude-local-oversight-website.md); [earlier tracker strategy](strategy/2026-10-26-claude-work-tracker-and-the-board.md#recommendation); [architecture plan, C3](plans/archive/2026-11-05-architecture-and-reuse.md); Maintainer chat, 2026-11-09: *"I'm really finding myself needing a better visual tool to use to see where we are on development toward a version release. I want something that works the same across agents. This is a pain point."*; 2026-11-10: *"I want a single local website with tabs that mimicks the behavior of your artifact tracker tool here for the release board, and the example I passed for the four-view pilot of code changes."*; later 2026-11-10: *"I would like the oversight website in v0.8. We need a graphical tool. I've been using one in multiple projects and want this to be a Cairn module."*; [Oversight dashboard design](strategy/2026-11-10-claude-oversight-complexity-and-effort-tabs.md); same day: *"We can design it with widgets that don't quite work yet, and/or plan to make them work in v0.8."*; *"it's a dashboard, informing the user at a glance how things are and how they are changing. This is a tool so that a person can monitor the growth of their project."*; *"We will inevitably add/change/delete with time. But the key is to get it going so it can become useful."*; Maintainer chat, 2026-11-13: *"Go ahead and move it"* -- postpones only this complete monitoring interface, including its code-change views, from v0.8 to v0.9. |
| **Run the independent four-view comparison on Cairn's own code map.** (v0.9; comparison pilot, queued since the architecture plan's C3, never run) | Done in 0.7: the text code map (`tools/code_map.py`, `docs/code-map.md`) was built and run on a clean copy of Cairn (900 files, 7,374 definitions), and `dev/architecture_review.md` records what it found. Not done: the visual views and the comparison. Per the archived plan's C3, a fresh reviewer prepares answers on duplication, drift, capability overclaim and justified growth; the author then trials manual board and gauge practice, the existing CodeCharta product (its license, execution and data transmission assessed before use) and a small offline report reusing LHM's scope-map page; record accuracy, time, setup effort, false alarms and misses; reject the visual approach if it improves neither understanding nor decisions. The shared Git reader it waited on is delivered. This trial decides what the code-change tab of the v0.9 oversight website should be; the full website stays in v0.9 (Maintainer, 2026-11-13). Also in scope: the broader endpoint-growth join the architecture review lists as queued. | Maintainer chat, 2026-11-13: *"Did we do the code map on Cairn? If not, put it on the v0.8 board please"*; [archived plan, C3](plans/archive/2026-11-05-architecture-and-reuse.md); scope disposition `0eeb76b9`; `dev/architecture_review.md`; Maintainer, chat 2026-11-18, relayed by the parent: reconfirmed the move to v0.9 with full scope preserved. |
| **Real-use meter comparisons and conditional Tokens retirement.** Queued after v0.7 and now scheduled in v0.9; the seven-day observation and independent `ccusage` comparison are unperformed. Keep manual Tokens and Elapsed until the prescribed comparisons and other meter checks justify retirement. | Condition to start: The collector passes its technical checks and the Maintainer opts into named local sources/projects. An agent then owns the comparisons with the existing privacy requirements; no private collection is currently enabled. | [Meter plan](plans/archive/2026-11-04-metered-cost.md), Maintainer disposition `97a0eab3`, 2026-11-09.  |

### 5. Less supervision: delegation and unattended work

| Work | Next step | Record |
|---|---|---|
| **How the Maintainer delegates decisions.** (v0.9 proposal to write) | [#84](https://github.com/MSUHydrogeology/cairn/issues/84): state the pattern Cairn already used in v0.7 (the delegated choices the Maintainer reviewed in November 2026, listed in this file at `9be9474c`): the delegating words quoted, a named higher-tier delegate who is not the author, what stays the Maintainer's, a review list for the return, and no carry-over to the next proposal. | [#84](https://github.com/MSUHydrogeology/cairn/issues/84) |
| **Cooperative budget guard and conditional unattended loop.** (queued for v0.9 planning) | Revisit the reviewed proposal during v0.9 planning, using v0.7 measurement and continuation results and the real-use meter comparisons above to decide what is worth building. It proposes a spending check before each unattended item; an automatic launcher remains a separate later choice. The guard cannot enforce a provider billing cap. Account/time source proof and human-benefit evidence remain absent. No implementation, activation or private collection is authorized. | [Joint proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [meter plan](plans/archive/2026-11-04-metered-cost.md); [continuation plan](plans/archive/2026-11-05-agent-continuation.md); Maintainer dispositions `896f2ac2` and `d0d82446`; Maintainer chat, 2026-11-06: *"Yeah go throw that 0.8 item on the planning file"*. |
| **Drain an adopter's current-release roadmap** ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)). Show candidates and a short plan, then move eligible items one at a time under their existing gates. A candidate, not authorization. | Write the v0.9 proposal, retaining existing lifecycle and Maintainer gates; this scheduling is not authorization for broader autonomous execution. | [Issue #34](https://github.com/MSUHydrogeology/cairn/issues/34) |

**Strategy notes that retire with v0.9.** [Work tracker and the board](strategy/2026-10-26-claude-work-tracker-and-the-board.md), [the local oversight website](strategy/2026-11-10-claude-local-oversight-website.md) and [the oversight dashboard design](strategy/2026-11-10-claude-oversight-complexity-and-effort-tabs.md) retire when the oversight-website proposal is accepted; [guidance for projects that have grown](strategy/2026-11-16-claude-guidance-for-grown-projects.md) when the release-module proposal is accepted and the test-records row is decided, the two rows its remaining modules feed. Two notes are living references and never retire: [the human and AI team development framework](strategy/2026-05-14-claude-human-ai-team-development-framework.md) and [the security strategy](strategy/2026-08-05-codex-security-strategy.md).

## v0.10 — outside adopters

Maintainer chat, 2026-11-19: *"We'll probably defer getting adopter feedback until v0.10."* Both rows moved here from v0.9 with their scope kept. Defect reports from adopters still get normal triage in v0.9. The board authorizes no outreach, and publishing any quote or testimonial still needs explicit consent.

| Work | Next step | Record |
|---|---|---|
| **Outside adopter interview and testimonial (Stid).** Refine the drafted questions and survey to find friction points and capture a testimonial. | In v0.10, so the adopter meets the settled layout once, use the staged instrument with a consenting adopter, including human interruptions and usability of the continuation guidance. The v0.7 agent-operated comparison cannot establish those human outcomes. Publication of any quote or testimonial still requires explicit consent. | [Strategy](strategy/2026-10-27-antigravity-adopter-survey-instrument.md#recommendation); Maintainer, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"* |
| **Independent adopter feedback.** Learn whether someone outside Cairn can install and use a published release without relying on the team's setup or knowledge. The v0.5 signed bootstrap passed in the team's Windows VM; that is not an outside adoption trial. | In v0.10, when a willing outside adopter is available, invite feedback on a published release that carries the 0.8 layout. The outside correctness trial remains open until actually performed. | Maintainer chat, 2026-11-01; **Outside correctness trial**, below |

**Strategy note that retires with v0.10.** [The adopter survey instrument](strategy/2026-10-27-antigravity-adopter-survey-instrument.md) retires after the interview is held.

## Terms used here

- **Re-anchor** — the Maintainer's signed approval of the exact test files that
  guard Cairn's security checks. A **repin** is the routine version of it.
- **Trust baseline** — the set of approved files a re-anchor installs. The
  current baseline, from the 0.7 cut, is `e5b7fd0a`; the 0.8 layout's
  re-anchor is in v0.9's defects.
- **Certification** — one full test run on a clean commit, before a release or
  a re-anchor. Ordinary changes run only the tests that name the files they
  touch.
- **Protected (frozen) test** — a test file the gate pins by its hash; changing
  it owes a re-anchor.

## Working rules (for agents)

- **Branch for v0.9.** Work proceeds on `0.9-dev`, made from the 0.8.0 release commit; `master` holds the release. Maintainer, 2026-11-19: *"Just make a 0.9-dev and put it there"*. No other topic branches and no worktrees for writing. A reviewer who must change code to test it
  works in a throwaway detached worktree of the reviewed commit and removes it
  afterwards. Maintainer, 2026-10-26: *"I actually would prefer that all work
  happen in the 0.5-dev branch, and that we use the intents board. This has
  gotten to be too many branches for me to interact with properly."* And,
  2026-10-28: *"create a 0.6-dev branch where we will do the other work going
  forward"*.
- **Claim, then commit by path.** Claim a file before editing it
  (`python dev/tools/intent.py claim --files <paths> --action "<what>"`) and commit
  by explicit path, which releases the claim. `python dev/tools/intent.py list`
  shows who holds what.
- **Check before each commit.** Every subagent in one session shares one claim
  identity, so one commit releases the others' claims: check `git diff` first.
- **Take turns with heavy test runs,** and give reviewers of long plans tight
  briefs.
- **Changelog.** Each change adds its entry under `## Unreleased` in
  `CHANGELOG.md`, in the same commit or the next, following the file's header.
  At the cut the section is renamed and a new `Unreleased` opened; the GitHub
  release notes are copied from it (`release/RELEASE_PROCESS.md`, "The cut").
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
  `install/_scaffold/SECURITY_MUTATIONS.md` and `install/UPGRADE.md`.
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
| **A smaller project-wide entry file (#79).** The accepted run-rules option (a) is complete; moving the remaining development process out of always-loaded AGENTS.md was not selected. | Reconsider if real run-only use shows the remaining reading cost outweighs upgrade conflicts. Requires its own proposal and Maintainer Decision. | [Delivered plan](plans/archive/2026-11-18-run-and-development-rules.md); [source Decision](proposals/archive/2026-11-16-claude-run-and-development-rules.md); [#79](https://github.com/MSUHydrogeology/cairn/issues/79) |
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
| **Adopter requests left for now (triaged 2026-11-16).** The two reported symlink-privilege tests in [#91](https://github.com/MSUHydrogeology/cairn/issues/91), part 2, were not found in Cairn; hold that repair until the reporting project identifies their owning paths (the accepted adopter-defects proposal records the search). A helper that moves a plan or proposal to its archive and repoints live links (#91, part 3); a repository-root helper and a check as an adopter-wide standard ([#90](https://github.com/MSUHydrogeology/cairn/issues/90)). Each is a new tool, and a new tool needs its own go-ahead. | The archive helper: when a missed link recurs after v0.8. The root standard: the layout now demonstrates the test-root helper in Cairn, so its proposal can be prepared; implementation or shipping still needs its own Decision. | [#90](https://github.com/MSUHydrogeology/cairn/issues/90), [#91](https://github.com/MSUHydrogeology/cairn/issues/91) |
| **Check instruction changes at pull-request merge (former item 1b).** Built and checked: the guidance, the scoped checks and the joined final check are complete. Only a first use on a real merged pull request remains. | When a pull request that changes agent-loaded files (`AGENTS.md`, skills, rule files) is about to be merged. The project has no other developers today, so that may be a long time. Then run the step at merge time, with the merger's trusted scanner and a human reading of what agents would do differently; add no pre-push or per-commit scan. | [Proposal](proposals/archive/2026-11-03-claude-pr-merge-instruction-check.md); Maintainer chat, 2026-11-03: *"if I'm developing here I don't need to scan for prompt injection changes. But when I merge a PR, yes. But DON'T add mandatory scans before pushes"*; [content-security module](../templates/modules/team-gated/content-security.md) Deferred by the Maintainer, 2026-11-13: *"Put that into the deferred list. We have no other developers right now. It's just us"*. |

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

* Try the session-start skill; its implementation is `dev/tools/session.py`.
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

Board housekeeping follows `dev/plans/_template.md` > Implementation closeout and
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
