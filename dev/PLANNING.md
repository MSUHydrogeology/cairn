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

The six previously waiting v0.7 proposals now have delegated Sol Decisions, listed below for the Maintainer’s review. The separate v0.8 guard/launcher proposal remains awaiting a Decision; it does not block current v0.7 implementation.

### Decisions to review when you return

Temporary authority, Maintainer chat 2026-11-06:

> I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome.

Sol accepted the following reversible local work, retaining heavy assurance and all required checks. Actual release/publication, trust operations and private access remain human-owned. Each source records Sol’s reasoning and the delegation; these are Sol’s choices, not claimed verbatim human choices.

| Proposal | Sol Decision | Main reason |
|---|---|---|
| [Safe Git reads](proposals/archive/2026-11-04-codex-safe-git-reads.md) | Accept — `05ea5d90` | Close false-clean paths through one shared boundary. |
| [Local environment notes](proposals/2026-11-04-codex-local-environment-notes.md) | Accept — `90f5ab32` | Manual discovery without an automatic note reader. |
| [Readable plans and finishing](proposals/2026-11-04-codex-readable-plans-and-finish-work.md) | Accept — `27300e1e` | Address documented gaps with existing records. |
| [Adopter execution retries](proposals/2026-11-05-codex-adopter-execution-retries.md) | Accept — `f499cb12` | Bounded correction while preserving capability floors. |
| [Release verification choice](proposals/2026-11-05-codex-opt-in-release-verification.md) | Accept local preparation — `f2bbc04d` | Make reduced origin assurance explicit; real use/publication remains human-owned while away. |
| [Scientific writing](proposals/2026-11-05-terra-scientific-plain-language.md) | Accept — `d3b653d2` | Improve precision and source honesty without new machinery. |

**Scoped scheduling Decision — Sol, 2026-11-06.** Under the quoted temporary delegation, Sol authorizes opening only the accepted safe-Git prerequisite plan while architecture/reuse remains active. Its implemented and reviewed boundary is needed for the four-view pilot; waiting for architecture to finish first would deadlock accepted scope. Other queued plans retain the existing hold. This adds one independently finishable plan and its existing reviews, with no scope concession, new ceremony or release authority. Source: delegated Sol decision in this chat, 2026-11-06.

**Other-chat interpretation.** For `modflow_tools development` at source `2bf8c2c4`, Sol found that unchanged content findings can reuse a recorded human review, but the searched evidence did not establish those two occurrence-specific human approvals. Its audit exit 10 remains a non-pass; a narrower Bandit test does not override it. The evidenced advice was returned to that chat; no release or waived check was authorized.

**One-fix verification schedule — Sol, `a3687971`.** For the inaccurate signing explanation in the [ceremony plan](plans/2026-11-06-human-useful-ceremony.md), run the focused regression before the targeted reviews and keep the complete mapped checks for the final integration run. No required check is removed. Saved-transcript comprehension evidence and both review findings still need closure; this does not permit archive or release before verification passes.

**Windows sweep interpretation — Sol, `4245c997`.** The [safe-Git plan](plans/2026-11-06-safe-git-reads.md) preserves existing Windows behavior and moves ordinary Git reads through the native safety helper. It adds no Windows full-sweep admission: an unsupported full run reports incomplete. Sol traced the platform contract, found no established full route removed, and rejected a new launcher dependency. Revisit if an established route is identified; required Windows checks remain due.

Combined canonical Python 3.13.13 prose checks passed at `dca68ee1`; nine external links were not probed. The active `modflow_tools development` chat was notified to route decision requests here for a Sol decision.

Meter implementation can continue with synthetic inputs. Actual private collection and its later comparison trial will need separate opt-in once a concrete collector is ready; that permission is not the current implementation blocker.

## Where Cairn stands

[Cairn 0.6.1 is released](https://github.com/MSUHydrogeology/cairn/releases/tag/v0.6.1).
Cairn builds itself with Cairn and is used in LHM and modflow_tools. The patch
is merged into `0.7-dev`; new v0.7 work proceeds there.

Standing direction from the Maintainer (2026-07-22): science projects come
first, and Cairn fixes what it already ships before building anything new. A
new tool or mechanism needs its own go-ahead. No outside project has yet run
Cairn end to end; that trial was waived for 0.4 and 0.5 and is still open
(see **Outside correctness trial**, below).

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

### Delivery order (Nov 2026; batch 1 active)

Starting snapshot on 2026-11-04: **10 accepted proposals, no open plans and seven
open GitHub issues**. The two accepted light proposals have no plan; the
other eight follow their Decisions and declared review obligations.
Rows saying "propose" still need their own accepted contract. Scheduling
adds no scope or implementation authority.

Maintainer approved the sequence on 2026-11-04 and moved only item 7c to
v0.8: *"Let's move #7c to v0.8."* Batch 1 is assigned in parallel to Luna
implementation agents, the lowest permitted tier. Later authoring and review
retain their task-specific model floors.

For v0.7 only, completed numbered rows stay visible, including after their
artifacts are archived, with **Complete** below the title. This display label
adds no lifecycle state. Maintainer chat, 2026-11-04:
*"Rather than removing the items, will you add a bold complete under each one so I can easily see where we are at"*.

Numbers 1-12 are the approved tackle order, with new 1c prioritized by the
Maintainer on 2026-11-05 to guide remaining v0.7 planning. Letters are parallel
candidates,
not instructions to edit the same file at once. Independent work can advance
when its named dependencies are ready; there is no whole-batch waiting gate.
Draft 2d/2e while the foundation work proceeds so they do not hold up later
integration. Use one writer for the shared template window in 3-6 and for
session, gauge and install-registry edits where the parallel lanes meet.

The numbered board owns the current order. The earlier
[coordination note](strategy/2026-11-02-codex-v07-delivery-sequence.md)
retains the strategy-retirement table; its original order is not a second
work queue. All 27 former v0.7 rows retain their scope and source records in
the grouped work below or, for scientific-software dimensions and governance
(former 7c), in v0.8. The remaining item identifiers stay stable.

GitHub issues #19, #34 and #46-#50 remain open; checked 2026-11-05 05:34 UTC.
None was closed.

Issues #51, #52 and #54 remain open from the 2026-11-05 check. #51 stays with item 3; #54 joins item 2e; #52 has its own v0.7 row. Issue #53 was closed after item 2g finished on 2026-11-05.

| Work | Next step | Record |
|---|---|---|
| **1a. Leaner reviews and finding-driven revisions.** (completed)<br>**Complete** | Implementation, scoped checks and the eligible next-two-review format trial are complete. The original 15-file run and supplemental 25-file run cover 2,602 unique nodes with no overlap; 21 guarded direct readers remain omitted by policy, so this is not a whole-tree claim. The supplement records 146.65 s pytest and 148.50 s wall; combined pytest time was 174.90 s, while total Boundary B wall time is unknown. Keep Foundations and required evidence; retire no Tokens field before 2b passes. Uncovered readability/plan-quality wording belongs to 3. Evidence: [archived proposal verification record](proposals/archive/2026-11-03-claude-leaner-reviews.md). | [Archived proposal](proposals/archive/2026-11-03-claude-leaner-reviews.md); Maintainer chat, 2026-11-03: *"Go with one light proposal."* |
| **1b. Check instruction changes at pull-request merge.** (active)<br>**Implementation complete** | Implementation, scoped checks and joined final check are complete. Only the next qualifying real merged-PR trial remains. Keep it at merge time, with the merger's trusted scanner and human outcome judgment; add no pre-push or per-commit scan. | [Proposal](proposals/2026-11-03-claude-pr-merge-instruction-check.md); Maintainer chat, 2026-11-03: *"if I'm developing here I don't need to scan for prompt injection changes. But when I merge a PR, yes. But DON'T add mandatory scans before pushes"*; [content-security module](../templates/modules/team-gated/content-security.md) |
| **1c. Achievable plans with SMART goals.** (completed)<br>**Complete** | Local and shipped guidance now teaches achievable, independently finishable goals without splitting by default. The Cairn-local rule records expected AST mismatch as unpassed until the separate release baseline, without making it an archive prerequisite. Ordinary code review accepted; the final wide check passed 1,640 tests and the class-aware prose gate. Two historical URL flags remain documented for the stricter raw scan; no Security Review was required. | [Archived plan](plans/archive/2026-11-05-smart-goals.md); [accepted proposal](proposals/archive/2026-11-05-codex-atomic-implementation-plans.md); Decision `1fe81f7a`; Maintainer chat, 2026-11-05: *"The idea isn't to \"split work\", it's to make plans achievable. SMART goals"* |
| **2a. Consolidate the expensive test families without losing detection.** (completed)<br>**Complete** | Source, required reviews and wide verification are complete. The release follow-up check found and closed the missing second ordering for the final fixture batch: all 815 cases passed at seed 1 with exactly the same identities and outcomes as existing seed 0. Scoped ceremony savings remain about 59–62 seconds to 9 seconds, not a whole-suite claim. Release certification and baseline work remain separate. | [Archived plan](plans/archive/2026-11-04-suite-consolidation.md); [accepted proposal](proposals/archive/2026-11-02-codex-suite-consolidation.md) |
| **2b. Meter real cost and report team/suite growth together.** (active) | Public growth/runtime reporting is complete. Synthetic usage, project binding and private ledger/claim helpers have focused checks; live collection remains closed. Windows status validation remains open; copied-fork accounting and the dated token index have focused synthetic checks. Finish producer, project export and handoff integration before the separate private opt-in trial and conditional Tokens retirement. The separate [reporting correction](proposals/archive/2026-11-06-codex-honest-measurement-reporting.md) is complete and archived after 221 mapped tests passed. The [archive-home plan](plans/2026-11-06-measurement-archive-home.md) has passed both plan reviews and is being implemented. | [Plan](plans/2026-11-04-metered-cost.md); [v0.8 proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [archived accepted proposal](proposals/archive/2026-10-30-claude-metered-cost.md); [Strategy](strategy/2026-10-27-antigravity-lightweight-team-measurement.md) |
| **2c. Share claims across a clone's worktrees.** (completed)<br>**Complete** | Verified linked worktrees of one clone share the claims log; other layouts retain reasoned local fallbacks. Final wide Boundary B: 56 files, 2,794 nodes, 2,785 passed, 9 Mac platform skips; eight additional native Windows checks passed. Both code reviews SHIP with findings closed. Recorded limits remain: pointer agreement is not authentication, physical shared-resolver junctions and external links were not probed, and legacy final-log symlink behavior is unchanged. No full suite, signing or repin. | [Archived plan](plans/archive/2026-11-04-shared-claims-across-worktrees.md); [accepted proposal](proposals/archive/2026-11-03-claude-shared-claims-across-worktrees.md); [coordination limits](../docs/methodology/coordination.md#scope-and-limits); Maintainer chat, 2026-11-03 |
| **2d. One safe Git helper for untrusted repositories.** (accepted; planning next) | Sol accepted the [proposal](proposals/archive/2026-11-04-codex-safe-git-reads.md) under temporary delegation (`05ea5d90`). Prepare its heavy prerequisite plan under the scoped scheduling allowance above; other new plans stay queued. Implementation follows its required plan reviews. Response `59bd3d54` closes its usual and Security proposal round; implementation waits for required plan reviews. Retain the caller inventory, sterile settings, deferred edit-check failure, linked-worktree/version-hang gaps and intentional no-Git case. Git-backed architecture views depend on this boundary. | [Strategy](strategy/2026-08-05-codex-security-strategy.md#1-one-shared-sterile-git-runner-for-untrusted-repositories-bnd-3--tru-6); [deferred findings N1-N3](plans/archive/upgrade-edit-check-no-repository-programs.md); [Proposal](proposals/archive/2026-11-04-codex-safe-git-reads.md) |
| **2e. Local development environment notes for adopters.** (accepted; queued for plan) | Sol accepted the [proposal](proposals/2026-11-04-codex-local-environment-notes.md) under temporary delegation (`90f5ab32`); prepare its heavy plan when the shared source window is available. Response `b5942fce` closes its usual and Security proposal round; no implementation is authorized. Issue #54's ignored, discoverable machine-local note is the same outcome; its suggested path is an example, while the proposal names a note under the existing reflections ignore. Confirm the per-checkout/worktree explanation and never turn note text into executable interpreter authority. Keep notes credential-free; coordinate later session edits with 2b, 2c and 8b. | Maintainer chat, 2026-11-01; [Proposal](proposals/2026-11-04-codex-local-environment-notes.md); [#54](https://github.com/MSUHydrogeology/cairn/issues/54) |
| **2f. Deliver onboarding tasks once, without managing the board.** (completed)<br>**Complete** | Installation and first adoption deliver usable tasks once while preserving project-owned board text, inventory and lock safeguards. Required reviews and final joined change verification are complete; the two expected AST checks remain unpassed for the separate release baseline. No additional implementation follow-up was deferred. | [Archived plan](plans/archive/2026-11-05-one-time-onboarding.md); [accepted proposal](proposals/archive/2026-11-04-codex-one-time-onboarding.md); Decision `2a233544`; integration `3c7cbfc2`; verified commit `88679232`. |
| **2g. Fast goodnight checks, explicit slow-test triggers.** (completed)<br>**Complete** | Full handoffs use the configured quick check and report its limits; reflection-only work adds no test run. The release comparison checks existing fresh results without adding a suite. Both independent code reviews and final joined change verification are complete; the later release and security runs remain due at their own triggers. | [Archived plan](plans/archive/2026-11-05-fast-goodnight-testing.md); [accepted proposal](proposals/archive/2026-11-05-codex-fast-goodnight-testing.md); Decision `65b723fc`; verified commit `88679232`; [#53](https://github.com/MSUHydrogeology/cairn/issues/53). |
| **3. Readable, implementable plans that finish cheap follow-ups.** (accepted; #51 local rule applied) | The [readable-plans proposal](proposals/2026-11-04-codex-readable-plans-and-finish-work.md) was accepted by Sol under temporary delegation (`27300e1e`) after both reviews and its response; preserve grouped scope for issues #46-#50. Cairn's local AGENTS rule already permits two feedback-driven same-tier retries. The distinct [adopter retry proposal](proposals/2026-11-05-codex-adopter-execution-retries.md) now has its ordinary and Security reviews and author response; Sol accepted it under delegation (`f499cb12`); required planning and reviews precede shipped doctrine changes. Capability-floor, review, check, authority/fence, data-governance and prior-effect safeguards remain, and #51 stays open until the adopter rule is implemented. | [#46](https://github.com/MSUHydrogeology/cairn/issues/46), [#47](https://github.com/MSUHydrogeology/cairn/issues/47), [#48](https://github.com/MSUHydrogeology/cairn/issues/48), [#49](https://github.com/MSUHydrogeology/cairn/issues/49), [#50](https://github.com/MSUHydrogeology/cairn/issues/50), [#51](https://github.com/MSUHydrogeology/cairn/issues/51); Maintainer chat, 2026-11-05: *"There's a new Cairn issue, #51. Please put this up on the v0.7 board"*; *"Go ahead and change the retry rule here, too."*; *"Just do the Cairn local version and then the full implementation can cover the rest"* |
| **3a. Clear summaries of what will be built.** (proposal review) | Finish the compact template proposal's reviews and response, then route the Decision through the temporary Sol delegation. It names material outputs in the existing proposal summary and adds brief plan/strategy summaries, preserving budgets and authority. Coordinate implementation with readable-plans work and current template writers. | [Proposal](proposals/2026-11-06-codex-concrete-delivery-summaries.md); Maintainer chat, 2026-11-06: *"I love the Decision Summary in proposals. Can we extend it to clarify what is being built: new/removed tools, docs, etc.? Also, a similar Build Summary at the top of plans would be helpful for me. Can we get a similar Summary in strategy docs?"* |
| **4. Finish agent-owned work without waiting for human operations.** (completed)<br>**Complete** | Agent-owned scope, reviews and applicable checks are complete. Human trust and release operations remain separate evidence-backed waits; archive grants no activation or release authority. | [Archived proposal](proposals/archive/2026-11-03-codex-implementation-plan-completion.md); [Archived plan](plans/archive/2026-11-04-implementation-plan-completion.md); Decision `e2aae09f`, Terra review `9b59ba4e`; Maintainer chat, 2026-11-03: *"Issues don't require releases. They require features and fixes. Releases are packaged sets of such things."* |
| **5. Permit only specifically authorized extra Security Review passes.** (**Complete**) | Implementation and required reviews are complete; the Maintainer authorized independently reviewed agent examples in place of the human trial, without direct human-interpretation evidence. | [Proposal](proposals/archive/2026-11-02-codex-security-review-pass-limit.md); [Archived plan](plans/archive/2026-11-04-security-review-pass-limit.md). |
| **6. Meaningful scientific tests and observable acceptance criteria.** (completed)<br>**Complete** | Testing guidance and examples are implemented, reviewed, and verified. The recorded automated checks are change evidence, not scientific validation; no A totals were added. | [Proposal](proposals/archive/2026-11-02-codex-fault-centered-testing.md); [Archived plan](plans/archive/2026-11-04-fault-centered-testing.md); [Strategy](strategy/2026-11-02-claude-outside-practices-for-better-software.md#tests-that-catch-real-faults); [acceptance guidance](strategy/2026-11-02-claude-outside-practices-for-better-software.md#testable-acceptance-criteria) |
| **7a. Repair the strict release-security runner.** (completed)<br>**Complete** | Windows mode handling, source-reviewed native policy, per-order records and the join are delivered. Required reviews and final wide verification are complete: 4,043 passed with four Windows-only skips. Actual same-commit Mac/Windows release records and their join remain the standalone release wait in item 12. | [Archived plan](plans/archive/2026-11-05-strict-release-security-runner.md); [accepted proposal](proposals/archive/2026-11-05-codex-strict-release-security-runner.md); Decision `d042dd33`; mode allowance `210e2501`. |
| **7b. Tighten Plain Language for scientific and technical writing.** (accepted; queued for plan) | The [proposal](proposals/2026-11-05-terra-scientific-plain-language.md) now has ordinary and Security ACCEPT reviews and an author response. It preserves established technical terms, distinguishes simulated from measured results and discloses source-check limits proportionately, without a new scanner or a first-person diary on static reference pages. The late-January 2027 evaluation remains separate. Sol accepted it under temporary delegation (`d3b653d2`); required planning and reviews precede implementation. | [Strategy](strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md#part-3-the-specific-gaps-to-close-for-direct-use-in-assai); Maintainer chat, 2026-11-04: *"Keep the tightening in v0.7. Add what you need based on your reading here."* |
| **7d. Bound upgrade growth with a refusal rule and a Git trial.** (accepted; plan not opened) | The Maintainer accepted the refusal-review rule and the bounded isolated Git comparison. Finish existing plans before opening another; then preserve both outcomes and required ordinary and Security plan reviews. The trial does not authorize an engine replacement. | [Accepted proposal](proposals/2026-11-05-codex-upgrade-growth.md); Decision `15264bf4`; [Strategy](strategy/2026-10-30-claude-upgrade-growth.md#recommendation). |
| **7e. Make adopter release-signature verification an explicit choice.** (accepted local preparation; queued for plan) | The [proposal](proposals/2026-11-05-codex-opt-in-release-verification.md) now binds ordinary selection to the official release source and optional signature verification to the executed checkout. It proposes a manual URL/tag/version/full-commit record in the adopter's same install/upgrade Git commit; that is auditable, not machine-enforced, and has no equivalent for a non-Git target. Sol accepted local preparation and the stated assurance loss under delegation (`f2bbc04d`); actual ordinary-route use and publication remain human-owned while away. No default has changed. Preserve developer-side release checks and install integrity. | [#52](https://github.com/MSUHydrogeology/cairn/issues/52); [current provenance procedure](../bootstrap/PROVENANCE.md) |
| **8a. Architecture, reuse and the four-view visual pilot.** (active) | The filesystem map, local-NTFS Windows backend and architecture rubric/helper guidance are implemented and reviewed. Final mapped verification for those slices is complete: 5,441 passed with 13 expected Windows-only skips; native backend/deadline checks are recorded separately. The filesystem assessment is in the architecture record. Git-backed views and the independent four-view pilot await the shared Git-helper Decision; broader growth join, C4 retirement and whole-plan completion remain open. | [Proposal](proposals/archive/2026-11-02-codex-architecture-and-reuse.md); [Plan](plans/2026-11-05-architecture-and-reuse.md); [Strategy](strategy/2026-10-30-claude-architecture-growth.md#recommendation-for-v07); [outside practices](strategy/2026-11-02-claude-outside-practices-for-better-software.md#mechanical-enforcement-and-cleanup); [EGM](https://github.com/google/elephant-goldfish-model) (Apache 2.0; ideas only, Maintainer chat 2026-11-02); [Strategy](strategy/2026-10-27-codex-adopter-engineering-practices.md#recommendation); [Strategy](strategy/2026-10-28-codex-review-at-agent-scale.md#recommendation) |
| **8b. Agents that continue through authorized work.** (completed)<br>**Complete** | A-C, required reviews and final wide verification are complete: 2,218 passed with one expected native-Windows skip. The approved synthetic comparison needed 0 baseline versus 2 guided post-stop prompts; it establishes neither a prompt reduction nor a human-usability benefit. The optional loop and budget guard remain with the current v0.8 proposal; human feedback stays with adopter work. | [Archived plan](plans/archive/2026-11-05-agent-continuation.md); [v0.8 proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [accepted proposal](proposals/archive/2026-11-03-claude-agent-continuation.md); Maintainer dispositions `896f2ac2`, `d0d82446`. |
| **9. Configuration-backed scanner cleanup.** (completed)<br>**Complete** | Configuration, migration and warning-only finding labels are delivered. Required ordinary and Security findings are closed. Final wide checks passed 5,657 cases with nine expected native-Windows skips; source verification is complete, with guarded-reader limits recorded. Release certification remains separate. | [Archived plan](plans/archive/2026-11-05-configuration-backed-scanner-cleanup.md); [accepted proposal](proposals/archive/2026-11-05-codex-configuration-backed-scanner-cleanup.md); Decision `92954c29`; settings-file allowance `0573c42c`. |
| **10. One file for routine multi-step work.** (active; implementation) | The Maintainer accepted retiring the unsupported parentless standard-note promise. The [reconciliation plan](plans/2026-11-06-lifecycle-guidance-reconciliation.md) has passed both plan reviews and is being implemented. Correct all current public and installed routing, including diagrams and skills; preserve historical records and chosen standard/heavy assurance. Light remains the existing one-proposal path for eligible work. | [Accepted proposal](proposals/archive/2026-11-06-codex-lifecycle-guidance-reconciliation.md); Decision `e05c64fe`; [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#2-merge-proposal--plan-into-a-single-compact-artifact-for-standard-multi-step-work) |
| **11. Human-useful ceremony output and return on attention.** (active; implementation) | The [implementation plan](plans/2026-11-06-human-useful-ceremony.md) has passed both plan reviews; implementation is starting with the driver and runbook. Explain behavior, purpose, risk, evidence and the exact approval at existing entry points; keep required hashes and fingerprints visible for their comparisons. Clarify existing cost records and add one short closing benefit-versus-effort judgment, with no duplicate ledger or extra Maintainer step. Retain all exact-byte checks and authority boundaries. | [Accepted proposal](proposals/archive/2026-11-06-codex-human-useful-ceremony.md); Decision `036a0495`; [Tool](../scripts/repin.py); [ceremony runbook](../bootstrap/REANCHOR_RUNBOOK.md); Maintainer chat, 2026-11-03: *"the output for the human ceremony should be human-useful"*; [Strategy](strategy/2026-08-21-claude-nimbleness-recovery.md#4-add-lightweight-return-on-attention-accounting-to-proposals) |
| **12. Integrated release verification and grouped strategy retirement.** (queued) | The release-closeout agent joins the completed ranges and existing evidence, performs all required final release checks, and coordinates human-only trust/publication operations separately from implementation-plan completion. Batch frozen edits before required ceremonies where permitted; preserve every required check and byte-review boundary. Resolve the retirement table, archive completed notes/assets and repair links; keep unfinished scope in a named live home and broad residual registers active. No new release plan or per-note backlog rows. | [Retirement ownership](strategy/2026-11-02-codex-v07-delivery-sequence.md#retirement-ownership); [proposal owner](proposals/archive/2026-11-02-codex-architecture-and-reuse.md); Maintainer chat, 2026-11-03 |

2a slow-family evidence includes the 2026-11-04 2c final wide run: [archived Boundary B record](plans/archive/2026-11-04-shared-claims-across-worktrees.md#implementation-verification----codex-terra-implementation-medium----2026-11-04).

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

Scientific-software dimensions and governance also move here by the
Maintainer's 2026-11-04 instruction. This delays that broader framing, not
v0.7's scientific-testing guidance or any required correctness check.

| Work | Next step | Record |
|---|---|---|
| **Cooperative budget guard and conditional unattended loop.** (v0.8 proposal awaiting decision) | Both proposal reviews and the author response are complete. Decide the joint proposal for later v0.8 work; the recommendation is guard first, retaining the later keep/drop choice for D. The revised proposal defines cooperative single-item boundaries and caller-approved settings, with their setup costs and limits. Account/time source proof and human-benefit evidence remain absent. No implementation, activation or private collection is authorized. | [Joint proposal](proposals/2026-11-05-codex-budgeted-unattended-work.md); [meter plan](plans/2026-11-04-metered-cost.md); [continuation plan](plans/archive/2026-11-05-agent-continuation.md); Maintainer dispositions `896f2ac2` and `d0d82446`. |
| **Scientific-software dimensions and governance (#19; former 7c).** (deferred, Nov 2026) | In v0.8, propose the remaining doctrine sentence, deliverable axis, discipline list and governance reframe using existing project evidence and the delivered scientific-testing examples and architecture rubric. Preserve the full remaining scope; the separate outside-adopter trial is not a completion claim or a new prerequisite. | `independent-scientific-check` plan; [Issue #19](https://github.com/MSUHydrogeology/cairn/issues/19); Maintainer chat, 2026-11-04: *"Let's move #7c to v0.8."* This replaces only this item's earlier v0.7 scheduling. |
| **Outside adopter interview and testimonial (Stid).** Refine the drafted questions and survey to find friction points and capture a testimonial. | In v0.8, after v0.7 ships, use the staged instrument with a consenting adopter, including human interruptions and usability of the continuation guidance. The v0.7 agent-operated comparison cannot establish those human outcomes. Publication of any quote or testimonial still requires explicit consent. | [Strategy](strategy/2026-10-27-antigravity-adopter-survey-instrument.md#recommendation); Maintainer, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"* |
| **Independent adopter feedback.** Learn whether someone outside Cairn can install and use a published release without relying on the team's setup or knowledge. The v0.5 signed bootstrap passed in the team's Windows VM; that is not an outside adoption trial. | In v0.8, when a willing outside adopter is available, invite feedback on a published release. The outside correctness trial remains open until actually performed. | Maintainer chat, 2026-11-01; **Outside correctness trial**, below |
| **Generate the hosted work tracker from `board.py --json`.** Build its rows from the board, `git` and `gh` instead of keeping 60 rows by hand. | In v0.8, generate from the existing board, git and issue data; consider a `passes` field only if the derived view demonstrates the need. | [Strategy](strategy/2026-10-26-claude-work-tracker-and-the-board.md#recommendation) |
| **Drain an adopter's current-release roadmap** ([#34](https://github.com/MSUHydrogeology/cairn/issues/34)). Show candidates and a short plan, then move eligible items one at a time under their existing gates. A candidate, not authorization. | Write the v0.8 proposal, retaining existing lifecycle and Maintainer gates; this scheduling is not authorization for broader autonomous execution. | [Issue #34](https://github.com/MSUHydrogeology/cairn/issues/34) |

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
