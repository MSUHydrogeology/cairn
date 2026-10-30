<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=published methodology citations -->
# Cairn — development roadmap

Current work and follow-ups, release queue organized 2026-10-27.
Plans and proposals own their designs and evidence; this board names the remaining work and its next move.
Completed work leaves the board. The commit history retains earlier versions.

## Where the project stands

<!-- cairn:slot project-status -->
Cairn is at **v0.5.0** (tagged 2026-10-28; its release gate failure was waived
at the cut; the later correction is recorded in
`dev/plans/archive/2026-10-29-release-evidence-environment.md`), self-hosting and used in LHM and modflow_tools.
**0.6 work happens on branch `0.6-dev`.** The external correctness trial remains
open; it was expressly waived as a condition of publishing 0.4 and 0.5.

Standing direction: **postdoc-first** and **fix defects, build nothing new**
(Maintainer, 2026-07-22). A new tool or mechanism needs its own go-ahead.
The broad-look and subtraction-sweep work is complete; their records are
`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` and
`dev/plans/archive/subtraction-sweep.md`.
<!-- cairn:end project-status -->

## Active

Use `python tools/board.py` for current plan/proposal status and
`python tools/board.py --maintainer` for declared waits. These read the
artifacts; this board does not maintain a second status table.

## Release path

### v0.6 — Make existing capabilities work right

**Release boundary (Maintainer direction, 2026-10-27):** correct and complete
what Cairn already ships. This includes making installed modules findable and
adding a suitable onboarding/activation task for each. It includes existing
behavior defects, security corrections, doctrine consistency and test-suite
maintenance.

**Recommended cut:** ship when the existing-module discovery and first-use path
works end to end, the v0.6 defect/security queue is dispositioned through its
own lifecycle, and the selected consistency and maintenance work is verified.
Use the existing release and certification ceremony. New mechanisms and new
adopter guidance below are v0.7 work; a release assignment grants no proposal
Decision, scope deviation, push or publication authority.

**Suggested order:** queued defects/security work; module discovery and onboarding;
doctrine routing before compression; narrow test freezing before consolidation.
Check the current tree (0.5.0 or later) before reviving a ceremony correction.

| Work | Gate | Notes |
|---|---|---|
| **Test once per change ([#41](https://github.com/MSUHydrogeology/cairn/issues/41))** | Light proposal; Maintainer Decision | Proposal: `dev/proposals/2026-10-30-claude-test-once-per-change.md`. Iteration runs only the tests that name a changed file (`tools/test_tiers.py for`); review stays targeted; Boundary B runs once, after code review; the full suite runs only before a release cut or re-anchor, or on request. Placed in v0.6 by the Maintainer (chat, 2026-10-30). |
| **Nimbleness 1: Governing-file compression delivered; template tutorial and wording simplification unverified** | Recheck remaining scope before proposing work; no blanket per-change re-anchor | The accepted apparatus reduction (`3cceb2c0`) compressed `AGENTS.md` and governing text. The 2026-08 strategy Item 1's remaining claims need verification: move tutorial commentary from `dev/proposals/_template.md` and `dev/plans/_template.md` into doctrine and relax the named prose-wording tests. Current templates remain 471 and 464 lines, respectively, not the strategy's 80–120-line target; do not assume that simplification landed. Apply the current re-anchor rules to any later scoped change. |
| **Cut the review apparatus** | Completed; indicator due 2026-11-30 | The accepted [proposal](proposals/archive/2026-10-30-claude-cut-the-apparatus.md) and [plan](plans/archive/2026-10-30-cut-the-apparatus.md) are implemented and archived. Follow up once: count review commits per archived artifact (subjects containing `review` or `respon`) divided by Markdown files added under plan and proposal archives; report against the 6.9 baseline and ≤3.5 target as an indicator, not proof of value. |
| **Nimbleness 3: Narrow gate-manifest freezing to security and trust tests** | Machinery complete; installation in forward-baseline item | The reviewed machinery is complete in `dev/plans/archive/2026-10-28-test-trust-boundary.md`; actual baseline installation and its proof are included in the separate v0.6 forward-baseline row below. Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 3) and `dev/strategy/2026-08-05-codex-security-strategy.md` [TRU-4]. |
| **Unify shipped-executable discovery [VER-5]** | Proposal first | Promoted from queued work. One traversal for install, manifest, security scan and upgrade. |
| **Security cluster strategic items** | Security Review, trust-apparatus | Strategy note: `dev/strategy/2026-08-05-codex-security-strategy.md`. Delivered: trust-root ceremony tidy (`bootstrap/reanchor.sh:414` runs Stage A under `env -i` and Python `-E -s -S`; `bootstrap/REANCHOR_RUNBOOK.md:350-355` publishes branch and anchor with `push --atomic`); terminal escaping and invisible-path rejection (`dev/plans/archive/2026-10-30-upgrade-install-integrity.md:26-38, 394-399`, archived with mapped criteria complete). Remaining: **Security-verification follow-on (`[VER-3 / SP8-3]`)**: assess separate link/claim-check legs and API/web credential pass-through; the content-security tripwire does not close these gaps. Maintainer authorization, 2026-10-27: *"Let's add those security items to v0.6"*. |
| **Run interpreter binding checks on native Windows** | Windows environment | Run `python scripts/run_windows_interpreter_binding.py` with Python 3.13 on native Windows and record discovery, junction and reparse results, including any unsupported or privilege-blocked cases. The [plan](plans/archive/2026-10-30-git-interpreter-binding.md) records the Maintainer's allowance to follow up; the Windows cases have not passed yet. |
| **Handle directory collisions in `upgrade --plan`/`--stage`** | Defect fix, engine | Promoted from queued work. Report a clean conflict instead of crashing with `IsADirectoryError` when an adopter replaces a tracked file with a directory. Maintainer instruction, 2026-10-27: *"Do those three queued items as well"*. |

#### v0.6 queued corrections and release follow-through

The detailed evidence and authorizations below are retained from the queue.
Overlapping summary rows above are one scope, not additional work. A
row may close earlier through its own lifecycle.

Issue #16 was already closed before its paragraph landed; any change to its
closure reason remains the Maintainer's choice.
* **Cold bootstrap acceptance run against the pushed release tag (`v0.5.0`).** Run the
  bootstrap block cold against the pushed tag using a machine and roster not
  supplied by this repository (`dev/plans/archive/release-authenticity.md`,
  `docs/release-process.md`).

| Work | Gate | Notes |
|---|---|---|
| **Upgrade semantic-adoption gap ([#35](https://github.com/MSUHydrogeology/cairn/issues/35))** | Future redesign; new proposal and Maintainer direction | The current proposal was rejected as framed because its trigger, evidence binding and operator burden were not sufficiently bounded (`dev/proposals/2026-10-30-codex-upgrade-semantic-adoption.md`). Retain the underlying concern for a lower-burden redesign; no engine implementation is authorized. The ancestor-integrity and display work in `dev/plans/archive/2026-10-30-upgrade-install-integrity.md` does not resolve semantic adoption. |
| **Disposition the remaining certification request ([#33](https://github.com/MSUHydrogeology/cairn/issues/33))** | Maintainer disposition of the requested terminology/semantics | `dev/plans/archive/2026-10-28-scoped-change-verification.md` shipped scoped change verification and `bounded`/`wide`, while retaining separate whole-tree certification. Reconcile that outcome with the issue's request that certification itself be scoped; record whether the retained distinction satisfies the adopter or further change is wanted. Do not re-run or reopen the implementation merely because the issue is open. |
| **Ceremony hardening: the one deferred item (I)** | Check, then a small change to closure members (one ceremony to pin) | From the repin-hardening decision (2026-10-27): the checker's internal messages that the launcher does not print. Deferred with two triggers: the first ceremony refusal the operator's screen did not explain, and the next edit to `bootstrap/reanchor.sh` or the launcher template. The other deferred items were delivered by the ceremony rewrite (one values reader, a one-page runbook, the launcher check in `scripts/repin.py`); E (subprocess use in the interpreter trust root) was not built and F and G were dropped. The first ceremony's stage-1 key probe timing out without explanation is a candidate trigger; read it with the "first-ceremony page and report fixes" row. |
| **Establish the v0.6 forward baseline** | Separate v0.6 work item; Maintainer authorization for actual installation | Establish the new baseline as a separate release task using the reviewed machinery in `dev/plans/archive/2026-10-29-forward-trust-baseline.md`. Before installation, certify the clean candidate tree; before release, run `python bootstrap/security_check.py` on the clean release commit with required tools and no skips, xfails or xpasses. This includes the release-evidence plan’s deferred protected-file packet, reader record, and Maintainer-only prior-verifier decisions, pinning and signing steps ([plan](plans/archive/2026-10-29-release-evidence-environment.md)); the scoped-verification plan’s deferred frozen-file re-anchor, the test-trust-boundary plan’s initial authority installation and proof against the installed signed roster, and the ceremony-command plan’s deferred actual baseline installation and proof (`dev/plans/archive/2026-10-29-ceremony-commands.md`). The same installation must account for frozen-file changes recorded in `dev/plans/archive/2026-10-28-model-floor-alignment.md` (four files: `test_model_tier_rule_ships.py`, `test_model_selection_stub.py`, `test_onboarding_seed_roster.py`, `test_review_stance_in_shipped_files.py`), `dev/plans/archive/2026-10-30-certification-cost-audit.md` (`test_review_sweep_ships.py`), and `dev/plans/archive/2026-10-30-certification-test-repairs.md` (`test_security_finding_confidentiality.py`, `test_repin.py`, `test_repin_ceremony.py`). Their recorded refusal controls and owning test-family checks passed; the frozen-file ceremony remains due for all these changes. They did not perform per-plan repin or re-anchor. Comparison with the old anchor is unnecessary; installation is not a prerequisite for archiving machinery. Maintainer: “They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.” |
| **Faster certifying runs** | Proposal first (a parallel runner is a new dev-only dependency; `bootstrap/DEPENDENCY_BUDGET.md`) | Measured 2026-10-27 at `b15dda53`, Python 3.13.13: 5,291 passed, 2 failed (the owed AST tests) in 20 minutes 4 seconds, one process, with other agents running; 14 cores; `pytest-xdist` is not installed. Measured again 2026-10-28 at `7c910851`: 5,479 passed in 24 minutes 55 seconds, one process, nothing else running (the gate's own suite phase at `3bb27388` took 19 minutes 34 seconds). Levers: a parallel runner that keeps the fixed shuffle seed; a consolidation pass on the slowest tests (the suite budget in `AGENTS.md` is 10 minutes); timing a run with nothing else running first. Maintainer, 2026-10-27: *"If you feel there are follow-ups, please put them into the Queue for v0.6 and we can triage them later"*. |
| **First-ceremony page and report fixes** | Docs and checker prose, closure members (one ceremony to pin) | From the first ceremony and its reader (2026-10-28): the report lists `reanchor.sh` as "not line-scanned" though its 4 hits were scanned; the page does not say that the stage-1 key probe waits 10 seconds for you to decline the passphrase prompt by pressing Return (it timed out once); the scan's file classes come from the files on disk, so deleted pinned files show as outside coverage and the digest can depend on stray files; a literal-string `shell=True` rates LOW and passes Bandit's MEDIUM gate; the report's authorization wording asks the Maintainer to author text instead of affirming a prepared one; the `compare.sh` process look listed an unrelated orphaned test process (a temp-folder shell blocked on a FIFO), so the look should filter to the ceremony's own processes. The later maintained workflow replaces the obsolete first-ceremony E7 instruction and shell helper with verifier and ceremony commands and displays the Y1–Y5 summary (`dev/plans/archive/2026-10-29-ceremony-commands.md`). Remaining items are historical reader findings without later closure evidence. Evidence: `dev/measurement/ceremony-scripts-2026-10-28/`. Maintainer, 2026-10-28: *"That is what this entire automated routine is for, but here we are pretending that I am doing something"* and *"I could definitely do a `reanchor` and a `repin` and confirm shas and enter my passphrase"*. |

### v0.7 — New capabilities and adopter feedback

Build on the corrected v0.6 baseline. These are scheduled candidates, each
retaining its proposal, review and Maintainer gates. Earlier v0.6 candidate
assignments below are superseded by this release split, not discarded scope.
The adopter survey/interview happens after v0.6; its strategy note's earlier
timing is superseded here. No outreach or testimonial publication is
authorized by this roadmap.

| Work | Gate | Notes |
|---|---|---|
| **Priority — testing strategy: a smaller, faster Cairn suite and better adopter guidance** | Proposal first; security/trust-test changes keep their gates; folder moves and freeze installation ride the forward-baseline ceremony | Costing time and money now (Maintainer, 2026-10-30). Strategy: `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md`. Landed `8f514e05`: tier map (`tools/test_tiers.py`) and testing-discipline selection guidance. Remaining: (1) install the narrowed freeze and move ordinary tests into tier folders at the forward baseline; (2) consolidation proposal, each removed test's fault mapped to a retained check, ratio a diagnostic only; (3) certifying run back under its 10-minute budget (24 min 55 s at `7c910851`), parallel runner only after consolidation; (4) test-growth figures in `tools/gauge.py --pulse`. |
| **Lightweight team measurement** | Proposal first | Strategy note: `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`. Three items: (1) upgrade `tools/gauge.py` to fix product bucketing and add `--pulse` (artifact words/tokens, review passes, model-tier mix, prompt tax); (2) update `tools/audit_report.py` and `tools/gauge.py` to attribute and sum standalone review side-files into their parent proposal/plan (closing the side-file length/pass loophole); (3) add an `archive/` subfolder to `dev/measurement/` and ship it with `.gitkeep` to adopters via `bootstrap/_scaffold/install.py` and the `incident-trackers` module. |
| **Nimbleness 2: Single compact artifact for standard multi-step work** | Proposal first, lifecycle doctrine | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 2). Allow standard 2–3 chunk work to carry its compact chunk/test plan directly in the proposal (one file, one pre-code review, one Maintainer Decision -> `ready-to-implement`), ending double proposal+plan ceremony for routine changes. |
| **Nimbleness 4: Return-on-Attention accounting** | Lifecycle doctrine | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 4). Add Maintainer steps & follow-ups spawned at Decision; add one sentence on whether the delivered outcome repaid review/ceremony cost at archive. |
| **Nimbleness 5: Move link-check and doctrine-ref allow comments to config** | Tooling | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 5). Move inline HTML `link-check-allow` and `cairn-internal-ref-allow` comments out of Markdown file headers into configuration, completing the August sweep pattern. |
| **Extend coordinates rule to shipped prose, and scan for it** | Proposal first, rate-limit gate | Promoted from deferred follow-ups (deferred 2026-10-27 for next release planning). (1) One sentence in the durable-artifacts rule (`AGENTS.md`, reasoning in `doctrine/rationale.md`) so it covers shipped module docs, docs and release notes, using the test the ceremony scan already uses; (2) warning-only scan of shipped files against a named list of live ids in `scripts/check_cairn.py`. Maintainer: "Defer the new rule on coordinates for later bringing back up in PLANNING". |
| **Outside-adopter interview & testimonial (Stid)** | Adopter evidence | Strategy note: `dev/strategy/2026-10-27-antigravity-adopter-survey-instrument.md`. Refine the drafted interview question set and survey instrument (staged until after v0.6) to gather qualitative feedback, measure friction points, and capture a testimonial. Maintainer direction, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"*. Timing superseded by Maintainer direction, 2026-10-27: survey after v0.6; no outreach authorized by scheduling. |
| **Automate the work tracker from `board.py --json`** | Tooling / hosted sync | Strategy note: `dev/strategy/2026-10-26-claude-work-tracker-and-the-board.md`. Build a generator script to derive hosted tracker rows automatically from `tools/board.py --json`, `git`, and `gh` rather than hand-keeping 60 hosted rows, and optionally add a `passes` field to `cairn-board/1`. Maintainer authorization, 2026-10-27: *"Yes, let's put automating the work tracker on the v0.6 list"*. |
| **Potential feature: drain the adopter's current-release roadmap ([#34](https://github.com/MSUHydrogeology/cairn/issues/34))** | Proposal first; v0.7 capability candidate | Use the adopting project's own release roadmap, show candidates and a short plan, then advance eligible items individually under their existing lifecycle and Maintainer gates. Keep the current board target; leave other releases, deferred, blocked and fenced work untouched. The issue explicitly leaves release placement to triage; this is a candidate, not implementation authorization. |
| **Architecture-review support for legacy and new systems** | Proposal first; adopter capability expansion | Strategy: `dev/strategy/2026-10-27-codex-adopter-engineering-practices.md`. Extend the existing rubric to help legacy, new and mixed systems establish appropriate engineering practices; connect to testing-discipline. Existing-module discovery/onboarding repairs stay in v0.6. |
| **Potential feature: visual codebase review at agent scale** | Proposal first; exploratory v0.7 candidate | Strategy: `dev/strategy/2026-10-28-codex-review-at-agent-scale.md`. Keep routine change review with agents while helping humans review evolving capabilities, architecture and consolidation opportunities. Explore four linked views (workstreams, system shape, capabilities, growth), reusing LHM's scope map and existing analysis tools; compose with architecture-review support rather than creating a parallel rubric. This roadmap entry authorizes exploration, not implementation. |

## Retained operating notes and accepted limits

These are observations or an explicitly accepted edge, not new feature tasks.

* **The board's Maintainer list and the status advisory disagree on a status
  such as `awaiting-decision-x`.** The advisory flags it as unknown; the board's
  `--maintainer` view still lists it as a wait. Making the board strict would
  edit the frozen golden and the waits-recipe test (`test_board_json_contract.py`)
  and owe a re-anchor. The Maintainer chose to leave it.
  Recorded so the disagreement is a known edge, not a surprise. Answer, verbatim:

  > "Leave the disagreement"

* **Three lessons kept from the old handoff file.** Found in the file the
  `NEXT_SESSION` change deleted (its migration record is in
  `dev/plans/archive/next-session-local-note.md`); they had no other home.
  (1) Every subagent in one session shares one work-intent agent id, so one
  commit releases the others' claims: check `git diff` before each commit.
  (2) Heavy test runs should take turns. (3) A review of a long plan is
  expensive, so give tight briefs. Kept as written there; the planning
  session's note, not doctrine (doctrine text takes the rate-limit gate).

* **Working rules for 0.6.** One branch, `0.6-dev`, in the one shared checkout;
  no topic branches and no worktrees for writing. `master` holds the released
  0.5.0 and takes no development commits. Before editing a file, record a claim
  with `python tools/intent.py claim --files <paths> --action "<what>"`; commit
  by explicit path, which releases the claim. `python tools/intent.py list` shows
  who holds what; `python tools/board.py` shows every proposal and plan on the
  branch. A reviewer who must mutate code does it in a throwaway detached
  worktree of the reviewed commit and removes it afterward. Merging to `master`,
  tagging and pushing are the Maintainer's. The Maintainer, 2026-10-26:

  > "I actually would prefer that all work happen in the 0.5-dev branch, and that
  > we use the intents board. This has gotten to be too many branches for me to
  > interact with properly."

  and, 2026-10-28, on the next release: *"create a 0.6-dev branch where we will
  do the other work going forward"*.
* **Each change lands with its changelog entry.** Under `## Unreleased` in
  `CHANGELOG.md`, in the same commit or the next, in the file's entry shape (one
  or a few lines, with a link to the durable record). At the cut the section is
  renamed and a fresh `Unreleased` opened; the GitHub release notes are copied
  from it, not drafted in a separate file (`docs/release-process.md`, "The cut").
* **Three accepted limits from the upgrade lockfile-path fixes (0.5.0).**
  The full split of one finding got only a documentation answer, because the
  split breaks a frozen pin; a linked lockfile on `--adopt-collisions` and
  `--init-lock` still ends in a traceback with nothing read or written outside
  the project; and the profile's preset, axis and module values are written
  unquoted, because quoting fails the differential oracle's byte comparison.
  Recorded in `bootstrap/_scaffold/SECURITY_MUTATIONS.md` and
  `bootstrap/UPGRADE.md`. The Maintainer, 2026-10-26: *"Accept all three
  (Recommended)"*. The interpreter binding's limit is recorded in
  `bootstrap/SAFETY.md`; moving it into `.git` is a v0.6 row.

## Deferred follow-ups (durable home)

Deferred candidates return to the queue when their revival condition is met.
Their earlier reproductions and deliberation remain in the named records and
this file's history.

| Follow-up | What remains / when to revisit | Evidence or owner |
|---|---|---|
| Agents taking their own review turns (#13) | After a recorded two-agent drive, propose a design meeting MA-2's four conditions; account for stale statuses and multiple holders. | `maintainer-attention` scope delta; issue #13 remains open. |
| Scientific-check doctrine and deliverable axis (#19) | Revisit when the third-party trial moves, or on Maintainer direction after about ten real non-N/A checks across two projects. Guidance shipped; the doctrine sentence, axis, disciplines and governance reframe did not. | `independent-scientific-check` C1 and archive; issue #19. Details below. |
| Watch the new review header | After ten proposal reviews, the goodnight scrub owner checks premise/alternative challenges, agent-selected outside reads, thin evidence and lost scope challenges. Put a concerning pattern to the Maintainer. | `review-stance-and-lenses` archive; quoted authority below. |
| Watch how far proposals written at medium hold up | After ten proposal reviews, the goodnight scrub owner compares proposals written at medium with those written at high. If fewer than three of the ten were written at high, report counts only and say the comparison is not available. Put a concerning pattern to the Maintainer. | `model-tier-rules` archive (R5); the Maintainer's 2026-10-26 answer lowered proposal authoring to medium. |
| Report only live slots after the module merge | The second form of the install-report change: print the report after the module-merge pass and drop the slots the install fills itself, so `solo-greenfield` shows 20 rather than 20 plus 2 listed apart. Not built because it moves output a frozen test pins; reason: over the cost bar. Revisit with the next change to that test. Authorization, verbatim: "Accept, leave 2 slots counted (Recommended)" | `engine-batch-f8-slots` archive, Scope delta. |
| Decision rights after agreement removal | Offering Cairn's unsure-case rule to adopters needs its own proposal. Revisit lifecycle escalation wording when a concrete conflict reaches a decision. Neither ships in the 0.4 removal. | `remove-collaboration-agreement` Decision Q3; authority quoted below. |
| Stable section identity and complete-set claims | A second actual rule needing section-set completeness would revive this; naming sections and proving all were handled are one scope. The retired lifecycle checker is not a promised future satisfier. | `2026-08-20-claude-review-loop-termination`, Deferred work. |
| Entry-page feature claims drift | A second stale feature list, or an adopter hitting one, may justify a doc-drift rule. | `dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` fold-up candidates. |
| Withdrawal ledgers can lose the reasoning | Synthesize on an independent recurrence or a Maintainer call; preserve the distinction between a corrected contract and a summary that re-derives its rejected argument. Also test invariants against their claimed space, not vacuous wording. | `scanner-claim-scope` revisions/reviews; original observations Aug 20. |
| Delegated verification multiplies broad runs | On the next fan-out plan or change to brief composition, reassess the working practice: the spawner verifies after joining; leaves receive scoped tasks. The run ledger was retired, so there is no promised collector. | `review-efficient-lifecycle` H1 observations, Aug 13–19; board history contains the 13-run count and its limits. |
| Pre-reviewing a revision | Revisit on a justified later proposal-review round or a Maintainer choice of workflow. Earlier probes found defects but one fix silently reduced accepted scope; every suggested fix still needs the purpose/scope check. | Aug 19 observations; no new review round or doctrine is authorized here. |
| Complete-contract revisions silently omit sections | A third instance or routine synthesis may justify carrying forward a section inventory. The omission ledger did not detect its own omissions; there is no live lifecycle checker to extend. | Aug 19 two-instance observation; the earlier local mitigation was a heading inventory. |
| Dispositions go stale between commits | An independent recurrence may justify recording the measured commit with a disposition. No doctrine change is authorized by the original one-session evidence. | Aug 19 figures/dispositions observation, formerly under first re-anchor ceremony. |
| Edit-check test gaps and one fail-open window | Revive at the next edit to the edit check in `bootstrap/_scaffold/upgrade.py`, or when a project is reported to lose an edit. Three non-blocking findings from the edit-check code review: (1) a `git` that answers some calls and then stops starting reads as "no guard", so `--apply` overwrote an edited file in the reviewer's test; a project cannot cause it, a `git` earlier on `PATH` is already trusted, and the review treated it as not a deviation; (2) no test pins the `.git` file half of the repository look (a linked work tree or submodule); (3) no test pins a hang at `git --version` alone. Not simple: (2) and (3) are new tests with new stand-ins on a trust surface, and (1) is a design call. | Maintainer, 2026-10-26: "On those other issues, Queue them if it's not simple to fix them now. No need to generate more work for us later." |
| Last stray finding ids | Fix after the thirteenth change's code review closes, because that change is editing the file: `(R5)` in `bootstrap/_scaffold/SECURITY_MUTATIONS.md` line 70 (an id into an ended review). Left alone on purpose: `SR-1` as the name of the integrity preflight inside the frozen script `templates/modules/team-gated/run_security_audit.py` and a comment in `bootstrap/_scaffold/config.py` (live vocabulary the script itself defines; editing a frozen file owes a re-anchor entry). Six shipped module docs had `B3`, `SR-1`, `R1` or `P4`; corrected 2026-10-27 in `e24d9ebd`. | Maintainer, 2026-10-27: "Please correct those cases you've found". |
| Stage re-pins in a sterile temporary worktree | Revisit if the dirty-tree refusal blocks the Maintainer twice. At 5 protected-path commits since the last pin it was not a bottleneck. | Same proposal, item G; `repin-build` proposal, "What is not carried". |
| Warn at session start when a pin is stale | Revive if a stale gate manifest or AST baseline goes unnoticed again. Needs a threshold with evidence behind it (the proposal's 25 commits is a guess). Cairn's tools warn, they do not block. | Same proposal, item E. |
| Context-aware quickstart | Propose a trimmed scaffold next-step path when the adopter need recurs. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |
| More adopter-facing count checks | Extend the existing verify-count guard beyond the quickstart's two counts when another live count needs it. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |

Authorizations for the first, second and fourth rows are in their archived
plans (`maintainer-attention`, `independent-scientific-check`,
`remove-collaboration-agreement`). Monitoring authority, verbatim:

> "Yes, we should keep watching."

> "Keep the monitoring row (Recommended)"

The surviving shared-working-tree observation came from the first-ceremony
batch, retained under this authorization:

> "Yes, go ahead and close everything else from these two plans out, including
> finding a permanent home for any remaining items"

### External correctness trial and scientific-check evidence

A consenting scientific repository that did not contribute the doctrine still
needs to run the bootstrap end to end. **It does not block 0.4 publication**
(waived 2026-10-19: *"Waive it for 0.4 — Go public once the batch lands. The
README says plainly that it hasn't yet had an outside test."*), and that
release waiver is not a completed trial. Revival: enroll a willing third
party. This also revives the scientific-check/axis review (#19).

The C1 blind trial covered two plans. One check targeted a different real risk;
the other was drafted with and without a data-status prompt. It did not
establish that the guidance catches later errors or validates the independent
basis. The Maintainer superseded the original stop result; the saved C1 and
archive records retain the drafts and scoring.

At revival, retain the six falsifiers: every failing check was already caught
elsewhere; most bases are an author's own expectation; assumption-changing
work claims N/A; failing runs are absent or irreproducible; checks only repeat
what code review catches; or a no-effect result has no positive control or
stated inability to supply one. No failure and no later error is inconclusive.
Watch for post-code checks, expectations changed to fit results, false
"data in hand" claims, ritual checks on tooling, new discipline lists, and
checks that neither need data nor say what evidence was opened. Nothing
counts these automatically; issue #19 and the Maintainer's review remain the
reminders.

## Onboarding

The original reading/tour seeds remain unconfirmed. The installed-hook task
is complete (`python tools/intent.py hooks-status`, 2026-10-19); the retired
signing seed is covered by the live agreement-removal plan and is no longer
a separate task here. These remaining seeds request no extra ceremony.

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

## Security-cluster routing

Security residuals and their revival triggers live in
`dev/strategy/2026-08-05-codex-security-strategy.md`, under **Live residual
register**. Its Cluster map decides when findings are one scope; the owning
plan carries reproducers and evidence. Add a board task when a trigger fires,
rather than duplicating the residual register here.

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

Use `queued` for work not started, `active` for in-flight work, `blocked` for
an actual named dependency, and `deferred` with a revival condition. Completed
work is removed after migration. Mark a Maintainer-only next move with the
literal header spelling `**Waiting on Maintainer**: <what>` inside its row;
the board command reads that declaration, not an inferred need for approval.

## Removal preconditions

Confirm completion and its durable record before removing a task. For the
full lifecycle rule, see `doctrine/lifecycle.md` > Removal preconditions for a
roadmap item. Keep current tasks here and evidence in the source records.
