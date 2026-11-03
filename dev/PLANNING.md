<!-- cairn-internal-ref-allow: docs/methodology/coordination.md docs/methodology/lifecycle.md reason=published methodology citations -->
# Cairn — development board

This board lists the work left and its next step. The Maintainer reads the
status, waits and release sections. Agents also read **Working rules** and the
sections after it. Evidence, quotes and history live in each row's
**Record** column: an issue, strategy note, proposal, plan or guide, or the
Maintainer chat the item came from. Finished work leaves the board.

`python tools/board.py` lists every open proposal and plan with its status;
`python tools/board.py --maintainer` lists what waits on the Maintainer.

## Where Cairn stands

<!-- cairn:slot project-status -->
Cairn 0.6.0 is released. Cairn builds itself with Cairn and is used in LHM and
modflow_tools. New v0.7 work proceeds on `0.7-dev`.

Standing direction from the Maintainer (2026-07-22): science projects come
first, and Cairn fixes what it already ships before building anything new. A
new tool or mechanism needs its own go-ahead. No outside project has yet run
Cairn end to end; that trial was waived for 0.4 and 0.5 and is still open
(see **Outside correctness trial**, below).
<!-- cairn:end project-status -->

## Waiting on you

Lines marked **Waiting on Maintainer** are what `board.py --maintainer` lists,
together with any proposal awaiting your Decision.

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

### Delivery order

Start with suite consolidation, metering/reporting and fault-centered testing;
then architecture/reuse, with local notes and the bounded upgrade trial able
to proceed independently; then focused wording, scanner and lifecycle cleanup.
The [delivery sequence](strategy/2026-11-02-codex-v07-delivery-sequence.md)
names shared editing windows and checks. These are workstreams, not new gates.
The rows below follow that order.

| Work | Next step | Record |
|---|---|---|
| **Explain additional Security Review rounds.** Keep the ordinary two-round limit and require a specific reason for a proposed exception. | Present the reviewed proposal for a Decision, then implement if accepted. | [Proposal](proposals/2026-11-02-codex-security-review-pass-limit.md); Maintainer moved this item from v0.6 to v0.7 on 2026-11-02. |
| **A smaller, faster test suite** (priority; costing time and money, Maintainer, 2026-10-30). The board's last reported full run was 24 min 55 s against a 10-minute target. The tier map (`tools/test_tiers.py`) landed in `8f514e05`. Mapped per-file call times over 10 s, slowest first across 2026-11-02 runs: `test_gate_preflight.py` 227.24 s; `test_upgrade.py` 72.40 s; `test_reanchor.py` 56.38 s; `test_upgrade_module_additions.py` 47.06 s; `test_upgrade_edit_check_runs_no_project_programs.py` 41.50 s; `test_security_marker.py` 29.79 s; `test_intents_tool.py` 24.47 s; `test_security_check.py` 21.89 s; `test_broad_run_guard.py` 20.15 s; `test_upgrade_lockfile_path_containment.py` 13.57 s. Additional slow files measured at `9f0bd13e` (Python 3.13.13, summed JUnit setup/call/teardown): `test_repin_ceremony.py` 540.11 s; `test_repin.py` 146.13 s; `test_ceremony_review_report.py` 19.28 s; `test_gate_reanchor.py` 18.10 s. | Open the accepted heavy-tier implementation plan, retaining declared reviews and detection, tier-folder, runtime and shared-reporting outcomes. The signed v0.6 baseline is installed; retain protected-path safeguards. | [Proposal](proposals/2026-11-02-codex-suite-consolidation.md); [Strategy](strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md#recommendation) |
| **Complete the deferred release security run -- required before v0.7 release.** The strict command remains unpassed. The Maintainer's v0.6.1-only exception does not authorize another carry-forward. | Own this with suite consolidation: implement and review a usable release path that reconciles duplicate whole-suite invocations and platform-specific skips while preserving required coverage and strict security outcomes, then run it on the exact clean v0.7 release candidate and record the result. This row is not complete with a proposal or another deferral. Do not waive missing checks automatically or call incomplete evidence passed. Keep focused Windows evidence distinct from full-tree certification. Include legacy full-handoff suite wording in `docs/methodology/session-routines.md` when reconciling run triggers. | Maintainer chat, 2026-11-03: *"Be sure that gets into the v0.7. We keep kicking this can down the road"*; v0.6.1-only exception: *"Authorize the v0.6.1-only exception"*; earlier direction, 2026-11-02: *"Put that security run in our v0.7 PLANNING list"*; [strict runner](../bootstrap/security_check.py); [suite owner](proposals/2026-11-02-codex-suite-consolidation.md); [focused Windows record](#accepted-limits-and-standing-decisions) |
| **Make repinning useful to humans.** `repin.py` presents raw fingerprints, line spans and JSON changes as an approval summary. | Retool the human ceremony output to explain behavior changes, purpose, risks, verification results and the exact action being authorized, without an agent translating. Keep hashes and structural diffs in separate technical/agent evidence and retain automated exact-byte checks. No extra Maintainer steps; queue the protected ceremony UX change for v0.7, not v0.6.1. | [Tool](../scripts/repin.py); [ceremony runbook](../bootstrap/REANCHOR_RUNBOOK.md); Maintainer chat, 2026-11-03: *"the output for the human ceremony should be human-useful"* |
| **Measure what agents cost from their tools' own logs.** Count real token and time use from the logs agent tools already keep, show it to the Maintainer, and stop unattended runs at a spending limit the Maintainer sets. Agents report nothing themselves. | Open the accepted heavy-tier plan, including its Security Review. Coordinate with lightweight team measurement so collection, attribution and pulse reporting are implemented once. | [Proposal](proposals/2026-10-30-claude-metered-cost.md) |
| **Lightweight team measurement.** Report words, tokens, review passes and model-tier mix; count review side-files toward their proposal or plan; count `bootstrap/_scaffold/` as product in `tools/gauge.py`, which now files it under other machinery; ship an `archive/` folder in `dev/measurement/`. | Reconcile this row with the accepted meter plan: retain size/pass/model reports, side-file attribution, product bucketing and the archive-folder outcome. Propose only uncovered work; do not add a second meter or pulse report. | [Strategy](strategy/2026-10-27-antigravity-lightweight-team-measurement.md) |
| **Agents that keep going.** Lower-tier agents stop after each finished step and wait to be told to continue. The board names the next step an agent may take, the post-commit hook prints it, and an optional bounded loop starts a fresh agent for each step. | Present the reviewed proposal for a Decision. Preserve project-owned current-release drain targets ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)); the loop uses the spending stop from the metered-cost plan. | [Proposal](proposals/2026-11-03-claude-agent-continuation.md); Maintainer chat, 2026-11-03: *"Please draft it, and put it on the 0.7 board."* |
| **Tests that catch real faults** (adopter guidance). Characterization tests for each function that carries a scientific claim, optional property tests for invariants, mutation checks on the lines a change touched, test-first, and a warning that agents weaken or fake tests to pass. Hypothesis and mutation tools stay optional recommendations. | Open the accepted standard-tier testing plan under its recorded Decision. Include the balanced-but-wrong example caught independently; tools remain optional and required checks remain required. | [Proposal](proposals/2026-11-02-codex-fault-centered-testing.md); [Strategy](strategy/2026-11-02-claude-outside-practices-for-better-software.md#tests-that-catch-real-faults) |
| **Testable acceptance criteria.** Optional prompts in the plan template: criteria written as "WHEN *condition* THE SYSTEM SHALL *behavior*" (EARS), and bug records stating current, expected and unchanged behavior. | Include the accepted optional prompts in the shared testing plan, connected to evidence without another review stage. | [Proposal](proposals/2026-11-02-codex-fault-centered-testing.md); [Strategy](strategy/2026-11-02-claude-outside-practices-for-better-software.md#testable-acceptance-criteria) |
| **Scientific-software dimensions and governance** ([#19](https://github.com/MSUHydrogeology/cairn/issues/19)). Guidance shipped; the doctrine sentence, deliverable axis, discipline list and governance reframe remain unfinished. | Bring the remaining scope into a v0.7 proposal using the existing project evidence. Keep the deliberately separate outside-adopter trial in v0.8; it is not a reason to leave this row without an owner or next step. | `independent-scientific-check` plan; Maintainer chat, 2026-11-03: *"All unresolved follow-ups (can you please list them) should be v0.7 then"* |
| **Finish agent-owned work without waiting for a release.** Plans finish on reviewed implementation; human trust/release operations remain separate. Resolved issues close against fixing commits, and roadmap/changelog housekeeping happens when work finishes ([#46](https://github.com/MSUHydrogeology/cairn/issues/46)). | Open the accepted heavy-tier completion plan. Include the Maintainer's issue-closure clarification in applicable live and shipped guidance: the implementing agent closes a fully resolved issue with its fix commit and evidence; partial fixes stay open; publication is separate unless the issue explicitly requests it. Reuse existing records, not another checklist or routine. | [Accepted proposal](proposals/2026-11-03-codex-implementation-plan-completion.md); Maintainer chat, 2026-11-03: *"Issues don't require releases. They require features and fixes. Releases are packaged sets of such things."* |
| **Local development environment notes.** Give adopters a simple, discoverable place to record machine-specific setup for people and agents, such as access to a test VM. Keep the notes out of committed history and keep credentials out of the notes. | Write a proposal for a lightweight local note and a way for agents to find it when needed. | Maintainer chat, 2026-11-01 |
| **Keep the upgrade engine from growing.** Two steps: each new upgrade refusal names the attack it stops under `bootstrap/SAFETY.md`'s threat model, or becomes a one-line accepted risk; and a one-session trial of upgrading through Git (install 0.5.0, customize it, upgrade to the current tree both ways, compare). | Propose the refusal rule and run the one-session trial. An engine replacement is not promised for v0.7; if the trial supports one, bring a heavy-tier proposal for v0.8. | [Strategy](strategy/2026-10-30-claude-upgrade-growth.md#recommendation) |
| **Make reading old code cheaper than writing new.** Agents copy code because finding it costs more: 15 groups of identical functions (676 lines) and 47 names defined in more than one file, measured 2026-10-30. | Open the accepted heavy-tier architecture/reuse plan, retaining declared reviews. Git-backed inspection needs the shared sterile helper; map, neighbors, critical homes and release assessment remain owed. | [Proposal](proposals/2026-11-02-codex-architecture-and-reuse.md); [Strategy](strategy/2026-10-30-claude-architecture-growth.md#recommendation-for-v07); [outside practices](strategy/2026-11-02-claude-outside-practices-for-better-software.md#mechanical-enforcement-and-cleanup); [EGM](https://github.com/google/elephant-goldfish-model) (Apache 2.0; ideas only, Maintainer chat 2026-11-02) |
| **Architecture review for legacy and new systems.** Help each kind of system set suitable engineering practices, building on the existing rubric and the testing module. | Include contrasting legacy/new/mixed assessments and explicit testing-guidance ownership in the accepted architecture/reuse plan; these capabilities also ship to selected adopter projects. | [Proposal](proposals/2026-11-02-codex-architecture-and-reuse.md); [Strategy](strategy/2026-10-27-codex-adopter-engineering-practices.md#recommendation) |
| **Visual review of a growing codebase.** Four linked views (workstreams, system shape, capabilities, growth) to help people review what agents build. Exploration only. | Include the accepted bounded pilot in the shared architecture/reuse plan: independent known-answer tasks, all four views and shared collection. A finished interface is not promised. | [Proposal](proposals/2026-11-02-codex-architecture-and-reuse.md); [Strategy](strategy/2026-10-28-codex-review-at-agent-scale.md#recommendation) |
| **One sterile `git` helper for untrusted repositories.** Upgrade code turns off risky `git` settings (file-system monitor, filters, hooks) one call at a time; one shared helper would make every call safe the same way. | Write a proposal; it changes a high-risk surface and needs a Security Review. | [Strategy](strategy/2026-08-05-codex-security-strategy.md#1-one-shared-sterile-git-runner-for-untrusted-repositories-bnd-3--tru-6) |
| **Share claims across a clone's worktrees.** Each checkout keeps its own claims log, so sessions in separate worktrees cannot see each other's claims and the commit hooks check the wrong log. Every checkout of one clone would use the main checkout's log, found from Git's pointer files without running `git`. | Review the proposal, with its Security Review, and present it for a Decision. | [Proposal](proposals/2026-11-03-claude-shared-claims-across-worktrees.md); [coordination limits](../docs/methodology/coordination.md#scope-and-limits); Maintainer chat, 2026-11-03 |
| **Check instruction changes before merging a pull request.** Nothing tells whoever merges a pull request to check its changes to agent-loaded files (templates, `AGENTS.md`, skills, `dev/`). Add one merge step: run the content scan on the changed files, then judge the logical outcome: what an agent following the new text would do differently, such as skipping a review, treating a status as approved, running a new command, dropping a check, or taking authority from the Maintainer. An optional no-tools reviewer can draft that outcome summary, treating the diff as data. A person decides. Not a pre-push or per-commit check. | Review the light proposal, then present it for a Decision. | [Proposal](proposals/2026-11-03-claude-pr-merge-instruction-check.md); Maintainer chat, 2026-11-03: *"if I'm developing here I don't need to scan for prompt injection changes. But when I merge a PR, yes. But DON'T add mandatory scans before pushes"*; [content-security module](../templates/modules/team-gated/content-security.md) |
| **Tighten Cairn Plain Language rules 2, 13 and 17.** Three small wording gaps found when an agent writes scientific prose: promotional vocabulary (rule 2), simulated versus measured results (rule 13), and honesty about which citations were checked (rules 14 and 17). | Propose the three wording fixes for v0.7; retain the separate late-January 2027 evaluation of Plain Language 1.0. | [Strategy](strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md#part-3-the-specific-gaps-to-close-for-direct-use-in-assai) |
| **Move allow comments into configuration.** The `link-check-allow` and `cairn-internal-ref-allow` comments at the top of Markdown files move to a config file. | Tooling change. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#5-finish-the-two-remaining-cleanup-items-from-the-august-sweep) |
| **No live finding ids in shipped prose.** Extend the rule against short-lived ids (such as `R5`) to shipped module docs, docs and release notes, with a warning-only scan in `scripts/check_cairn.py`. | Write a proposal; doctrine changes take the rate-limit gate. | Maintainer: *"Defer the new rule on coordinates for later bringing back up in PLANNING"* |
| **One file for routine multi-step work.** A standard change with two or three chunks carries its chunk and test plan in the proposal: one file, one review, one Decision. | First compare the outcome with the existing light-tier path, which already allows multi-area work without a plan. Propose only the remaining standard-lane gap, preserving the single-artifact outcome rather than adding duplicate lifecycle machinery. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#2-merge-proposal--plan-into-a-single-compact-artifact-for-standard-multi-step-work) |
| **Leaner reviews; proposals grow to absorb findings.** Reviews drop repeated metadata and duplicate Foundations lines so findings fit their limit; word budgets are soft; a revised proposal or plan may grow past its opening target, each addition answering a named finding. | Review the light proposal, then present it for a Decision. Retain the related v0.7 outcomes: cold-read readability rather than a new check ([#47](https://github.com/MSUHydrogeology/cairn/issues/47)), budgets rather than caps ([#48](https://github.com/MSUHydrogeology/cairn/issues/48)), and plan chunks implementable by their assigned model tier ([#49](https://github.com/MSUHydrogeology/cairn/issues/49)). Reconcile their scope before implementation rather than assuming this proposal already delivers all three. | [Proposal](proposals/2026-11-03-claude-leaner-reviews.md); Maintainer chat, 2026-11-03: *"Go with one light proposal."* |
| **Did the ceremony pay off?** At Decision, list the Maintainer steps and follow-ups a change creates; at archive, say in one sentence whether the result repaid its review cost. | First reconcile with the current Decision-options cost comparison. Identify the remaining Decision and archive outcomes before proposing extra fields or another assessment routine. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#4-add-lightweight-return-on-attention-accounting-to-proposals) |

### v0.7 strategy closeout

| Work | Next step | Record |
|---|---|---|
| **Retire completed v0.7 strategy notes.** One grouped closeout, not a new process or one ledger row per note. | Owner: the v0.7 release-closeout agent. At the cut, resolve every retirement-table entry, move lasting guidance to its durable home and archive completed notes. Keep unfinished work in a named live home and retain broad registers while their role persists. Retire the delivery-sequence note itself when the release or its replacement closes its job. | [Retirement ownership](strategy/2026-11-02-codex-v07-delivery-sequence.md#retirement-ownership); [proposal owner](proposals/2026-11-02-codex-architecture-and-reuse.md); Maintainer chat, 2026-11-03 |

## v0.8 — adopter feedback and workflow expansion

Retain the following work, sequenced after v0.7 rather than discarded.
Organized interviews, testimonials and the independent adoption trial belong
here; incoming defect reports still receive normal triage. The cost of waiting
is later evidence about outside usability. No outside trial is counted as
completed, and no required release or correctness check is waived by this
schedule. The board authorizes no outreach or testimonial publication.

Visual-review exploration remains in v0.7 because it may improve architectural
understanding; a full interface is not required for that release. Any
upgrade-engine replacement comes here only if the bounded v0.7 trial supports
it and its own proposal is accepted.

| Work | Next step | Record |
|---|---|---|
| **Outside adopter interview and testimonial (Stid).** Refine the drafted questions and survey to find friction points and capture a testimonial. | In v0.8, after v0.7 ships, use the staged instrument with a consenting adopter; publication of any quote or testimonial still requires explicit consent. | [Strategy](strategy/2026-10-27-antigravity-adopter-survey-instrument.md#recommendation); Maintainer, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"* |
| **Independent adopter feedback.** Learn whether someone outside Cairn can install and use a published release without relying on the team's setup or knowledge. The v0.5 signed bootstrap passed in the team's Windows VM; that is not an outside adoption trial. | In v0.8, when a willing outside adopter is available, invite feedback on a published release. The outside correctness trial remains open until actually performed. | Maintainer chat, 2026-11-01; **Outside correctness trial**, below |
| **Generate the hosted work tracker from `board.py --json`.** Build its rows from the board, `git` and `gh` instead of keeping 60 rows by hand. | In v0.8, generate from the existing board, git and issue data; consider a `passes` field only if the derived view demonstrates the need. | [Strategy](strategy/2026-10-26-claude-work-tracker-and-the-board.md#recommendation) |
| **Drain an adopter's current-release roadmap** ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)). Show candidates and a short plan, then move eligible items one at a time under their existing gates. A candidate, not authorization. | Write the v0.8 proposal, retaining existing lifecycle and Maintainer gates; this scheduling is not authorization for broader autonomous execution. | [Issue #34](https://github.com/MSUHydrogeology/cairn/issues/34) |

## Terms used here

- **Re-anchor** — the Maintainer's signed approval of the exact test files that
  guard Cairn's security checks. A **repin** is the routine version of it.
- **Trust baseline** — the set of approved files a re-anchor installs. The
  **v0.6 baseline** was installed at `67cdb805`.
- **Certification** — one full test run on a clean commit, before a release or
  a re-anchor. Ordinary changes run only the tests that name the files they
  touch.
- **Protected (frozen) test** — a test file the gate pins by its hash; changing
  it owes a re-anchor.

## Working rules (for agents)

- **One branch.** Work on `0.7-dev` in the one shared checkout, with no topic
  branches and no worktrees for writing. `master` holds the released 0.6.0 and
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
| **Review-load check.** Count review commits (subjects containing `review` or `respon`) per archived proposal or plan, against the 6.9 baseline and a target of 3.5 or fewer. This is an indicator, not proof of value. | Measure on 2026-11-30; independent of the v0.6 release. | [Proposal](proposals/archive/2026-10-30-claude-cut-the-apparatus.md) |
| **Agents taking their own review turns** ([#13](https://github.com/MSUHydrogeology/cairn/issues/13)). | After a recorded run of two agents driving reviews: propose a design meeting the four conditions set as MA-2, allowing for stale statuses and more than one holder. | `maintainer-attention` plan, Scope delta |
| **Watch the new review header.** The first ten reviewed on 2026-11-02 did not meet the specified incident trigger: several challenged the proposal's framing. | Continue noticing premise and alternative challenges, agent-chosen outside reads, thin evidence and lost scope challenges; report a worrying pattern. | `review-stance-and-lenses` plan; authority below |
| **Watch how proposals written at medium tier hold up.** The first ten review passes covered four medium- and three high-authored proposals; both groups had substantive blocking findings. The small, mixed sample does not establish a quality difference. | Continue watching; compare like work when enough evidence exists. | `model-tier-rules` plan (R5); the Maintainer's 2026-10-26 answer lowered proposal writing to medium |
| **Report only live slots after the module merge.** Print the install report after the merge and drop slots the install fills itself, so `solo-greenfield` shows 20, not 20 plus 2. Not built: it moves output a frozen test pins. | With the next change to that test. | `engine-batch-f8-slots` plan, Scope delta; Maintainer: *"Accept, leave 2 slots counted (Recommended)"* |
| **Decision rights after the collaboration agreement's removal.** Offering Cairn's rule for unsure cases to adopters needs its own proposal. | When a concrete conflict reaches a decision; then revisit the escalation wording. | `remove-collaboration-agreement` Decision, Q3 |
| **Naming sections and proving all were handled.** | When a second real rule needs a complete set of sections. The retired lifecycle checker is not the promised answer. | `2026-08-20-claude-review-loop-termination`, Deferred work |
| **Feature lists on entry pages go stale.** | A second stale list, or an adopter hitting one, may justify a doc-drift rule. | `dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` |
| **Withdrawal records can lose their reasoning.** Keep a corrected contract distinct from a summary that re-argues what was rejected, and test rules against the cases they claim. | On an independent repeat or a Maintainer call. | `scanner-claim-scope` revisions and reviews |
| **Delegated checks multiply broad test runs.** Working practice: the spawning agent verifies after joining; subagents get scoped tasks. | On the next fan-out plan or change to how briefs are built. | `review-efficient-lifecycle` observations; the 13-run count is in this file's history |
| **Pre-reviewing a revision.** Earlier tries found defects, but one fix quietly cut accepted scope; every fix still needs the purpose and scope check. | On a justified later review round or a Maintainer workflow choice. | Observations, 2026-08-19 |
| **Revisions that silently drop sections.** | A third instance may justify carrying a section inventory forward. | Observations, 2026-08-19 |
| **Dispositions go stale between commits.** | An independent repeat may justify recording the measured commit with each disposition. | Observations, 2026-08-19 |
| **Edit-check test gaps and one fail-open case.** (1) A `git` that answers some calls and then stops reads as "no guard", so `--apply` overwrote an edited file in a test; a project cannot cause it. (2) No test pins the `.git`-file case (a linked work tree or submodule). (3) No test pins a hang at `git --version` alone. | At the next edit to the edit check in `bootstrap/_scaffold/upgrade.py`, or when a project loses an edit. | Maintainer, 2026-10-26: *"On those other issues, Queue them if it's not simple to fix them now. No need to generate more work for us later."* |
| **Evaluate Cairn Plain Language 1.0 after three months.** Adopted 2026-10-26. | Late January 2027: the Maintainer checks whether it worked, then decides on a standalone page with its own DOI. | [Strategy](strategy/2026-05-14-claude-human-ai-team-development-framework.md#candidate-future-moves-not-queued) |
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

<!-- cairn:slot onboarding-tasks -->
<!-- preset: collaborative-team -->
* [seed; id: try-session-start-skill]
  Try the session-start skill; its implementation is `tools/session.py`.
* [seed; id: read-lifecycle-doctrine]
  Read `docs/methodology/lifecycle.md` for the proposal/plan lifecycle.
* [seed; id: read-coordination-doctrine]
  Read `docs/methodology/coordination.md` for shared-tree coordination.
* [seed; id: read-dual-review-module]
  Read `dev/modules/dual-review.md`; fresh independent review is the standing
  procedure, and an outside read is the Maintainer's call.
* [seed; id: walk-dev-tour]
  Read `dev/modules/onboarding/dev-tour.md` for the worked lifecycle example.
* [seed; id: agent-team-onboarding]
  Review capability tiers and commit attribution with
  `dev/modules/onboarding/agent-team-onboarding.md`.
<!-- cairn:end onboarding-tasks -->

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
