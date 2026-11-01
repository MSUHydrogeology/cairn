<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=published methodology citations -->
# Cairn — development board

This board lists the work left and its next step. The Maintainer reads the
first four sections. Agents also read **Working rules** and the sections after
it. Evidence, quotes and history live in the document named in each row's
**Record** column: an issue, strategy note, proposal, plan or guide, or the
Maintainer chat the item came from. Finished work leaves the board.

`python tools/board.py` lists every open proposal and plan with its status;
`python tools/board.py --maintainer` lists what waits on the Maintainer.

## Where Cairn stands

<!-- cairn:slot project-status -->
Cairn 0.5.0 is released (tagged 2026-10-28). Its release gate failure was
waived at the cut; the [later correction](plans/archive/2026-10-29-release-evidence-environment.md)
is recorded. Cairn builds itself with Cairn and is used in LHM and
modflow_tools. Work toward 0.6 happens on the branch `0.6-dev`.

Standing direction from the Maintainer (2026-07-22): science projects come
first, and Cairn fixes what it already ships before building anything new. A
new tool or mechanism needs its own go-ahead. No outside project has yet run
Cairn end to end; that trial was waived for 0.4 and 0.5 and is still open
(see **Outside correctness trial**, below).
<!-- cairn:end project-status -->

## Waiting on you

Lines marked **Waiting on Maintainer** are what `board.py --maintainer` lists,
together with any proposal awaiting your Decision.

- **Waiting on Maintainer**: run the v0.6 trust-baseline ceremony at the
  release cut. It re-approves the test files Cairn's gate protects, after this
  release's changes to them; only you can run it. See **What the v0.6 baseline
  must include**, below. [Plan](plans/archive/2026-10-29-forward-trust-baseline.md)
- **Waiting on Maintainer**: check the 0.5.0 release from scratch: install from
  the pushed tag on a machine and model roster this repository did not supply.
  [Guide](../docs/release-process.md)

## v0.6 — fix what Cairn already ships

Ship 0.6 when new modules are findable and usable end to end, the defect and
security queue is resolved, and the chosen maintenance work is verified, using
the existing release and certification steps. New mechanisms are v0.7 work. A
release assignment authorizes no Decision, scope change, push or publication.

| Work | Next step | Record |
|---|---|---|
| **A folder where a tracked file belongs.** `upgrade` should refuse safely and keep the folder's contents. | Fix the one blocking Security Review finding, then a targeted re-review. | [Plan](plans/2026-10-30-upgrade-directory-collisions.md) |
| **Audit the docs for Cairn Plain Language.** Check `README.md`, `docs/`, shipped templates and module documents, and this board, against the 17 rules in `dev/agent_collaboration.md`. Technical content stays exact. Shipped templates carry the "Written in Cairn Plain Language 1.0" line under their title; other documents do not. | Review the plan. The changelog pass (`ca6cc14d`) and this board show the method; the board template's layout has its own row below. | [Plan](plans/2026-11-01-plain-language-docs.md); Maintainer chat, 2026-11-01: *"we don't need all docs to have the branding. Just the templates."* |
| **Give the shipped board template this board's layout.** `templates/core/dev/PLANNING.md` starts every adopter's board. Give it this board's shape: **Waiting on you** first, each release as Work, Next step and Record, a short terms list, and working rules marked for agents. If its releases become tables, keep each Maintainer wait on its own bulleted line: `board.py --maintainer` does not read the marker inside a table cell. | Write a proposal; it changes a shipped template. Coordinate with the docs audit so the template is rewritten once, and keep the scope wording `test_scope_reduction_trap.py` pins. | Maintainer chat, 2026-11-01 |
| **Retire the v0.6 decision master.** The note briefs v0.6's open decisions and holds; once v0.6 ships, its job is done. | At the v0.6 cut, confirm each of its items is done or on this board, change its role from living, then archive it. | [Strategy](strategy/2026-10-28-codex-v06-decision-master.md) |
| **Merge customized doctrine without losing its meaning** ([#35](https://github.com/MSUHydrogeology/cairn/issues/35)). | Needs a lighter design and Maintainer direction; the first proposal was rejected because its trigger, evidence and operator burden were not bounded. | [Proposal](proposals/archive/2026-10-30-codex-upgrade-semantic-adoption.md) |
| **Review-load check.** Did cutting review passes work? Count review commits (subjects containing `review` or `respon`) per archived proposal or plan, against the 6.9 baseline and a target of 3.5 or fewer. An indicator, not proof of value. | Measure on 2026-11-30. | [Proposal](proposals/archive/2026-10-30-claude-cut-the-apparatus.md) |

### What the v0.6 baseline must include

The baseline ceremony installs the reviewed machinery in one step. Before
installing, certify the clean candidate tree. Before release, run
`python bootstrap/security_check.py` on the clean release commit with every
required tool, and no skips, expected failures or unexpected passes. The
ceremony must account for:

- the protected-file packet, reader record and the Maintainer-only verifier,
  pinning and signing steps deferred by the
  [release-evidence plan](plans/archive/2026-10-29-release-evidence-environment.md);
- the first install of the signed list of protected tests, from the
  [test-trust plan](plans/archive/2026-10-28-test-trust-boundary.md), which
  narrows freezing to security and trust tests;
- the deferred baseline install from the
  [ceremony-commands plan](plans/archive/2026-10-29-ceremony-commands.md);
- the engine's AST baseline, owed since this release's engine changes:
  `bootstrap/tests/test_ast_attest.py` fails 2 of 30 tests at `657c7aea`
  ([upgrade growth](strategy/2026-10-30-claude-upgrade-growth.md#recommendation));
- the operator guidance in `bootstrap/REANCHOR_RUNBOOK.md` and
  `bootstrap/reanchor.sh` changed since the last pin;
- protected test files changed since the last pin: four from the
  [model-floor plan](plans/archive/2026-10-28-model-floor-alignment.md)
  (`test_model_tier_rule_ships.py`, `test_model_selection_stub.py`,
  `test_onboarding_seed_roster.py`, `test_review_stance_in_shipped_files.py`);
  `test_review_sweep_ships.py` from the
  [certification cost audit](plans/archive/2026-10-30-certification-cost-audit.md);
  `test_security_finding_confidentiality.py`, `test_repin.py` and
  `test_repin_ceremony.py` from the
  [certification test repairs](plans/archive/2026-10-30-certification-test-repairs.md);
  and `test_review_and_verification_rules_ship.py` and
  `test_verification_boundaries.py` from the
  [test-once proposal](proposals/archive/2026-10-30-claude-test-once-per-change.md).

Those plans did not repin or re-anchor themselves, and comparing against the
old anchor is unnecessary. Maintainer: *"They can each build the machinery,
the new baseline does not need to be part of their plans. It can be a work
board item for v0.6."*

## v0.7 — new capabilities and adopter feedback

Built on the corrected v0.6 baseline. Each item keeps its proposal, review and
Maintainer gates. The adopter interview happens after v0.6, and this board
authorizes no outreach or published testimonial.

| Work | Next step | Record |
|---|---|---|
| **A smaller, faster test suite** (priority; costing time and money, Maintainer, 2026-10-30). The full run takes 24 min 55 s against a 10-minute target. The tier map (`tools/test_tiers.py`) landed in `8f514e05`. | Write the consolidation proposal: each removed test's fault mapped to a kept check. Then move ordinary tests into tier folders at the v0.6 baseline, bring the full run under 10 minutes (a parallel runner only after consolidation), and add test-growth figures to `tools/gauge.py --pulse`. | [Strategy](strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md#recommendation) |
| **Make reading old code cheaper than writing new.** Agents copy code because finding it costs more: 15 groups of identical functions (676 lines) and 47 names defined in more than one file, measured 2026-10-30. | Write a proposal: a capability map, a neighbors report in plans and reviews, one home per critical capability, and a structure pass at each release. | [Strategy](strategy/2026-10-30-claude-architecture-growth.md#recommendation-for-v07) |
| **Architecture review for legacy and new systems.** Help each kind of system set suitable engineering practices, building on the existing rubric and the testing module. | Write a proposal. | [Strategy](strategy/2026-10-27-codex-adopter-engineering-practices.md#recommendation) |
| **Visual review of a growing codebase.** Four linked views (workstreams, system shape, capabilities, growth) to help people review what agents build. Exploration only. | Explore, reusing LHM's scope map; compose with the architecture review. | [Strategy](strategy/2026-10-28-codex-review-at-agent-scale.md#recommendation) |
| **Measure what agents cost from their tools' own logs.** Count real token and time use from the logs agent tools already keep, show it to the Maintainer, and stop unattended runs at a spending limit the Maintainer sets. Agents report nothing themselves. | Open the plan. The proposal is heavy tier, so the plan review includes a Security Review. Coordinate with lightweight team measurement, below, so tokens are counted once. | [Proposal](proposals/2026-10-30-claude-metered-cost.md) |
| **One sterile `git` helper for untrusted repositories.** Upgrade code turns off risky `git` settings (file-system monitor, filters, hooks) one call at a time; one shared helper would make every call safe the same way. | Write a proposal; it changes a high-risk surface and needs a Security Review. | [Strategy](strategy/2026-08-05-codex-security-strategy.md#1-one-shared-sterile-git-runner-for-untrusted-repositories-bnd-3--tru-6) |
| **Tighten Cairn Plain Language rules 2, 13 and 17.** Three small wording gaps found when an agent writes scientific prose: promotional vocabulary (rule 2), simulated versus measured results (rule 13), and honesty about which citations were checked (rules 14 and 17). | Write a proposal for version 1.1, considered with the January 2027 evaluation below. | [Strategy](strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md#part-3-the-specific-gaps-to-close-for-direct-use-in-assai) |
| **Keep the upgrade engine from growing.** Two steps: each new upgrade refusal names the attack it stops under `bootstrap/SAFETY.md`'s threat model, or becomes a one-line accepted risk; and a one-session trial of upgrading through Git (install 0.5.0, customize it, upgrade to the current tree both ways, compare). | Propose the refusal rule, since it changes review guidance, and run the trial. If the trial holds, write a heavy-tier proposal. | [Strategy](strategy/2026-10-30-claude-upgrade-growth.md#recommendation) |
| **Lightweight team measurement.** Report words, tokens, review passes and model-tier mix; count review side-files toward their proposal or plan; count `bootstrap/_scaffold/` as product in `tools/gauge.py`, which now files it under other machinery; ship an `archive/` folder in `dev/measurement/`. | Write a proposal. | [Strategy](strategy/2026-10-27-antigravity-lightweight-team-measurement.md) |
| **One file for routine multi-step work.** A standard change with two or three chunks carries its chunk and test plan in the proposal: one file, one review, one Decision. | Write a proposal; it changes lifecycle doctrine. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#2-merge-proposal--plan-into-a-single-compact-artifact-for-standard-multi-step-work) |
| **Did the ceremony pay off?** At Decision, list the Maintainer steps and follow-ups a change creates; at archive, say in one sentence whether the result repaid its review cost. | Write a proposal; it changes lifecycle doctrine. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#4-add-lightweight-return-on-attention-accounting-to-proposals) |
| **Move allow comments into configuration.** The `link-check-allow` and `cairn-internal-ref-allow` comments at the top of Markdown files move to a config file. | Tooling change. | [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#5-finish-the-two-remaining-cleanup-items-from-the-august-sweep) |
| **No live finding ids in shipped prose.** Extend the rule against short-lived ids (such as `R5`) to shipped module docs, docs and release notes, with a warning-only scan in `scripts/check_cairn.py`. | Write a proposal; doctrine changes take the rate-limit gate. | Maintainer: *"Defer the new rule on coordinates for later bringing back up in PLANNING"* |
| **Outside adopter interview and testimonial (Stid).** Refine the drafted questions and survey to find friction points and capture a testimonial. | After v0.6. | [Strategy](strategy/2026-10-27-antigravity-adopter-survey-instrument.md#recommendation); Maintainer, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"* |
| **Generate the hosted work tracker from `board.py --json`.** Build its rows from the board, `git` and `gh` instead of keeping 60 rows by hand. | Write the generator; optionally add a `passes` field to `cairn-board/1`. | [Strategy](strategy/2026-10-26-claude-work-tracker-and-the-board.md#recommendation) |
| **Drain an adopter's current-release roadmap** ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)). Show candidates and a short plan, then move eligible items one at a time under their existing gates. A candidate, not authorization. | Write a proposal. | [Issue #34](https://github.com/MSUHydrogeology/cairn/issues/34) |

## Terms used here

- **Re-anchor** — the Maintainer's signed approval of the exact test files that
  guard Cairn's security checks. A **repin** is the routine version of it.
- **Trust baseline** — the set of approved files a re-anchor installs. The
  **v0.6 baseline** is the next one.
- **Certification** — one full test run on a clean commit, before a release or
  a re-anchor. Ordinary changes run only the tests that name the files they
  touch.
- **Protected (frozen) test** — a test file the gate pins by its hash; changing
  it owes a re-anchor.

## Working rules (for agents)

- **One branch.** Work on `0.6-dev` in the one shared checkout, with no topic
  branches and no worktrees for writing. `master` holds the released 0.5.0 and
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
| **Agents taking their own review turns** ([#13](https://github.com/MSUHydrogeology/cairn/issues/13)). | After a recorded run of two agents driving reviews: propose a design meeting the four conditions set as MA-2, allowing for stale statuses and more than one holder. | `maintainer-attention` plan, Scope delta |
| **Scientific-check doctrine and its deliverable axis** ([#19](https://github.com/MSUHydrogeology/cairn/issues/19)). The guidance shipped; the doctrine sentence, the axis, the discipline list and the governance reframe did not. | When the outside trial moves, or on Maintainer direction after about ten real checks across two projects. See **Outside correctness trial**, below. | `independent-scientific-check` plan |
| **Watch the new review header.** | After ten proposal reviews, the handoff owner checks for premise and alternative challenges, outside reads an agent chose, thin evidence and lost scope challenges, and reports a worrying pattern to the Maintainer. | `review-stance-and-lenses` plan; authority below |
| **Watch how proposals written at medium tier hold up.** | After ten proposal reviews, the handoff owner compares proposals written at medium with those written at high. With fewer than three at high, report counts only. | `model-tier-rules` plan (R5); the Maintainer's 2026-10-26 answer lowered proposal writing to medium |
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
| **One stray finding id.** `(R5)` in `bootstrap/_scaffold/SECURITY_MUTATIONS.md` line 70 points into an ended review. `SR-1` stays on purpose: the frozen script `templates/modules/team-gated/run_security_audit.py` defines it. | When that file is next edited. | Maintainer, 2026-10-27: *"Please correct those cases you've found"* |
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
  Read `doctrine/lifecycle.md` for the proposal/plan lifecycle.
* [seed; id: read-coordination-doctrine]
  Read `doctrine/coordination.md` for shared-tree coordination.
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
`doctrine/lifecycle.md` > Archive precondition. Completed rows leave once their
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
full lifecycle rule, see `doctrine/lifecycle.md` > Removal preconditions for a
roadmap item. Keep current tasks here and evidence in the source records.
